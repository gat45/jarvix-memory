"""JEV remote provider — TypeSafe System One API (jev-latest).

One POST to /v1/systemone per call; questions are evaluated in parallel
server-side (70-500 ms). Answers use typed constraints: noul (yes/no
probability), choice (option + distribution), score (rubric 0..N).

The API key is NEVER committed: JARVIX_JEV_API_KEY env or config.json.
Every method returns the same shaped dict as RuleBasedProvider plus a
"provider" field — callers get policies without knowing who judged.
"""

import json
import os
import logging
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional
from .jev import DecisionProvider, RuleBasedProvider

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://api.typesafe.ai/v1"
DEFAULT_MODEL = "jev-latest"


class JevRemoteProvider(DecisionProvider):
    """System One typed judgements. Same DecisionProvider contract as rules."""

    MEM_LAYERS = ["episodic", "semantic", "procedural", "decision",
                  "hypothesis", "strategy", "recovery", "evidence", "graph"]

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None,
                 timeout: float = 30.0, config_path: Path = None):
        # Key priority: explicit arg > env > config.json (gitignored)
        self.api_key = api_key or os.environ.get("JARVIX_JEV_API_KEY") \
            or os.environ.get("TYPESAFE_API_KEY")
        if not self.api_key and config_path:
            try:
                cfg = json.loads(config_path.read_text(encoding="utf-8"))
                self.api_key = cfg.get("jev_api_key")
            except Exception:
                pass
        self.base_url = base_url or DEFAULT_BASE_URL
        self.model = model or DEFAULT_MODEL
        self.timeout = timeout
        self.last_error: Dict = {}

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def _request(self, state, questions: Dict) -> Dict:
        req = urllib.request.Request(
            f"{self.base_url}/systemone",
            data=json.dumps({
                "model": self.model,
                "state": state,
                "questions": questions,
            }).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            body = json.loads(resp.read())
        self.last_error = {}
        return body.get("answers", {})

    # ── DecisionProvider contract ─────────────────────────────

    def route(self, query: str) -> Dict:
        """Jev Choice: which memory layer serves this query."""
        criteria = {l: f"Acces la couche memoire {l} pour cette requete"
                    for l in self.MEM_LAYERS}
        try:
            a = self._request(query, {
                "layer": {
                    "type": "choice",
                    "instructions": "Quelle couche memoire est la plus pertinente pour cette requete ?",
                    "criteria": criteria,
                },
            }).get("layer", {})
            choice = a.get("choice")
            if choice:
                probs = a.get("probabilities", {})
                return {"choice": choice, "distribution": probs,
                        "confidence": round(a.get("confidence", probs.get(choice, 0.0)), 3),
                        "provider": "jev-remote"}
            raise ValueError("reponse choice vide")
        except Exception as e:
            logger.warning("jev route fallback: %s", e)
            return {"choice": "semantic", "distribution": {}, "confidence": 0.3,
                    "provider": "rules", "reason": str(e)}

    def filter(self, memory: Dict, context: str, max_tokens: int = None) -> Dict:
        """Jev Noul: inject this memory NOW? (cost-aware caller keeps budget)."""
        state = {"memory": (memory.get("content") or "")[:2000],
                 "context": context[:2000]}
        try:
            a = self._request(state, {
                "inject": {"type": "noul",
                           "instructions": "Cette memoire est-elle pertinente a INJECTER dans ce contexte MAINTENANT ?"},
            }).get("inject", {})
            p = float(a.get("noul", 0.0))
            action = "inject" if p >= 0.75 else ("maybe" if p >= 0.45 else "ignore")
            return {"decision": action, "prob": p, "provider": "jev-remote"}
        except Exception as e:
            logger.warning("jev filter fallback: %s", e)
            return {"decision": "ignore", "prob": 0.0,
                    "provider": "rules", "reason": str(e)}

    def verify(self, claim: str, evidence_stats: Dict) -> Dict:
        state = {"claim": claim[:2000], "evidence": evidence_stats}
        try:
            a = self._request(state, {
                "supports": {"type": "noul",
                             "instructions": "Les preuves presentees supportent-elles ce claim ?"},
            }).get("supports", {})
            s = float(a.get("noul", 0.0))
            label = ("supports" if s >= 0.8 else
                     "contradicts" if s <= 0.2 else
                     "inconclusive")
            return {"supports": round(s, 3), "contradicts": round(1.0 - s, 3),
                    "unknown": 0.0, "label": label, "provider": "jev-remote"}
        except Exception as e:
            logger.warning("jev verify fallback: %s", e)
            return {"supports": 0.0, "contradicts": 0.0, "unknown": 1.0,
                    "label": "no_evidence", "provider": "rules", "reason": str(e)}

    def gate(self, action: str, destructive_threshold: float = 0.85) -> Dict:
        try:
            a = self._request({"proposed_action": action[:2000]}, {
                "destructive": {"type": "noul",
                                "instructions": "Cette action est-elle DESTRUCTIVE ou irreversible (suppression, flash, format) ?"},
                "allow": {"type": "noul",
                          "instructions": "Cette action est-elle sure a executer sans supervision humaine ?"},
            })
            d = float(a.get("destructive", {}).get("noul", 0.0))
            allow = float(a.get("allow", {}).get("noul", 0.0))
            if d >= 0.75:
                decision = "BLOCK"
            elif d >= 0.5:
                decision = "REVIEW"
            elif allow >= 0.8:
                decision = "ALLOW"
            else:
                decision = "REVIEW"
            return {"decision": decision, "destructive_prob": d, "allow_prob": allow,
                    "provider": "jev-remote"}
        except Exception as e:
            logger.warning("jev gate fallback: %s", e)
            fb = RuleBasedProvider().gate(action, destructive_threshold)
            fb["provider"] = "rules"
            fb["reason"] = str(e)
            return fb

    def score(self, grid: Dict) -> Dict:
        """Jev Score per criterion (0..4 legend), weighted average in code."""
        criteria = {k: v for k, v in grid.items()
                    if k != "_weights" and isinstance(v, (int, float))}
        if not criteria:
            return {"score": 0.0, "label": "low", "per_criterion": {}, "provider": "jev-remote"}
        legend = ["Tres faible", "Faible", "Moyen", "Bon", "Excellent"]
        questions = {f"rate_{k}": {
            "type": "score",
            "instructions": f"Note (0=catastrophe .. 4=excellent) la qualite sur: {k}",
            "criteria": legend,
        } for k in criteria}
        try:
            answers = self._request({"criteria": criteria}, questions)
            total, per = 0.0, {}
            for k in criteria:
                sv = answers.get(f"rate_{k}", {}).get("score")
                per[k] = round(float(sv if sv is not None else criteria[k]), 3)
                total += per[k]
            s = total / (len(criteria) * 4.0)
            label = ("high" if s >= 0.75 else "medium" if s >= 0.45 else "low")
            return {"score": round(s, 3), "label": label, "per_criterion": per,
                    "provider": "jev-remote"}
        except Exception as e:
            logger.warning("jev score fallback: %s", e)
            fb = RuleBasedProvider().score(dict(grid))
            fb["provider"] = "rules"
            fb["reason"] = str(e)
            return fb

    def decide(self, context: str, options: list) -> Dict:
        if not options:
            return {"choice": None, "distribution": {}, "confidence": 0.0,
                    "provider": "jev-remote"}
        try:
            a = self._request({"context": context[:4000]}, {
                "pick": {"type": "choice",
                         "instructions": "Quel est le meilleur choix pour le contexte donne ?",
                         "criteria": {opt: None for opt in options}},
            }).get("pick", {})
            return {"choice": a.get("choice", options[0]),
                    "distribution": a.get("probabilities", {}),
                    "confidence": a.get("confidence", 0.0),
                    "provider": "jev-remote"}
        except Exception as e:
            logger.warning("jev decide fallback: %s", e)
            return {"choice": options[0], "distribution": {}, "confidence": 0.0,
                    "provider": "rules", "reason": str(e)}
