"""Jev LOGITS provider — local scoring via llama.cpp (Simple-Jev/LitJev style).

No JSON generation, no cloud: the prompt constrains the next token to the
allowed candidate letters (choice) or OUI/NON (noul), and we read their
token logprobs from the OpenAI-compatible completion endpoint (llama.cpp
/v1/completions logprobs). One prefill per decision, argmax over allowed
tokens, normalized distribution — the Simple-Jev mechanic on any GGUF
model you already have on disk (Qwen/Gemma), CPU or GPU.
"""

import json
import os
import math
import logging
import urllib.request
import urllib.error
from typing import Dict, List, Optional
from .jev import DecisionProvider, RuleBasedProvider

logger = logging.getLogger(__name__)


class JevLogitsProvider(DecisionProvider):
    """DecisionProvider backed by any local llama.cpp server (logprobs)."""

    def __init__(self, db, base_url: str = None, model: str = None,
                 timeout: float = 30.0, config_path=None):
        self.db = db
        self.base_url = base_url or os.environ.get("JARVIX_JEV_LLAMA_URL") \
            or "http://127.0.0.1:8080"
        self.timeout = timeout
        self._model_id: Optional[str] = None
        # temperature/seed tuned for stable ranking, not creativity

    @property
    def available(self) -> bool:
        try:
            req = urllib.request.Request(f"{self.base_url}/v1/models", method="GET")
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read())
                models = data.get("data", [])
                if models:
                    self._model_id = models[0].get("id", "local")
                return True
        except Exception:
            return False

    def _score_tokens(self, prompt: str, candidates: List[str]) -> Dict[str, float]:
        """One completion with logprobs; match candidate tokens (single letters
        AND full words, with/without leading space) in top-logprobs."""
        # keep full candidate words when given (OUI, NON, digits, letters)
        base = [c.strip().upper() for c in candidates]
        tail = "Answer strictly with one single token: "
        full_prompt = f"{prompt}\n{tail}"
        payload = json.dumps({
            "prompt": full_prompt,
            "max_tokens": 1,
            "temperature": 0.0,
            "logprobs": 10,
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/completion",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            body = json.loads(resp.read())
        probs = body.get("completion_probabilities") or []
        tops: list = []
        if isinstance(probs, list) and probs:
            item = probs[0]
            tops = item.get("top_logprobs") or []
        out = {c.strip().upper(): -20.0 for c in base}
        matched = 0
        for entry in tops:
            if not isinstance(entry, dict):
                continue
            tok = str(entry.get("token", "")).strip().upper()
            lp = entry.get("logprob")
            if lp is None:
                continue
            # exact: ' O' -> O / ' OUI' -> OUI
            if tok in out:
                out[tok] = max(out[tok], float(lp))
                matched += 1
                continue
            # prefix: a first letter ' O' counts for 'OUI' candidate
            for cand in out:
                if (len(tok) == 2 and tok[-1] == cand[0]) or \
                   (len(tok) > 2 and tok.lstrip() in cand[:len(tok.lstrip())]):
                    out[cand] = max(out[cand], float(lp))
                    matched += 1
                    break
        if not matched or all(v == -20.0 for v in out.values()):
            return {}  # pas de logits exploitables -> l'appelant retombe sur rules
        return out

    def _softmax(self, logprobs: Dict[str, float], temp: float = 1.0) -> Dict[str, float]:
        # mask candidates never observed in top-k (they stay at -20 => ~0 weight)
        real = {k: v for k, v in logprobs.items() if v > -19.0}
        if not real:
            return {}
        mx = max(real.values())
        exps = {k: math.exp((v - mx) / temp) for k, v in real.items()}
        s = sum(exps.values()) or 1.0
        return {k: round(v / s, 3) for k, v in exps.items()}

    # ── DecisionProvider contract ─────────────────────────────

    def route(self, query: str) -> Dict:
        keys = ["E", "S", "P", "D", "H", "G", "R"]
        names = {"E": "episodic", "S": "semantic", "P": "procedural", "D": "decision",
                 "H": "hypothesis", "G": "graph", "R": "recovery"}
        try:
            lp = self._score_tokens(
                f"Question agent: {query}\n"
                "CHOIX de couche memoire la plus utile: e=episodic(events), "
                "s=semantic facts, p=procedural(how-to), d=decision rationale, "
                "h=hypothesis a tester, g=graphe relations, r=recovery echec.",
                keys)
            probs = self._softmax(lp)
            if not probs:
                raise ValueError("no logprobs")
            win = max(probs, key=probs.get)
            return {"choice": names[win], "distribution":
                    {names[k]: v for k, v in probs.items()},
                    "confidence": probs[win], "provider": "jev-logits"}
        except Exception as e:
            logger.warning("jev-logits route fallback: %s", e)
            fb = RuleBasedProvider().route(query)
            fb["provider"] = "rules"
            return fb

    def filter(self, memory: Dict, context: str, max_tokens: int = None) -> Dict:
        try:
            lp = self._score_tokens(
                f"CONTEXTE: {context[:1500]}\n"
                f"MEMOIRE: {(memory.get('content') or '')[:1500]}\n"
                "Faut-il injecter cette memoire dans le contexte MAINTENANT ?"
                 "Reponds par UN mot (OUI ou NON). Reponse:"
                ["OUI", "NON"])  
            p = self._softmax(lp)
            yes = p.get("OUI", 0.5)
            action = "inject" if yes >= 0.75 else ("maybe" if yes >= 0.45 else "ignore")
            return {"decision": action, "prob": round(yes, 3), "provider": "jev-logits"}
        except Exception as e:
            logger.warning("jev-logits filter fallback: %s", e)
            return {"decision": "ignore", "prob": 0.0, "provider": "rules"}

    def verify(self, claim: str, evidence_stats: Dict) -> Dict:
        ev = evidence_stats.get("evidence", [])
        passed = sum(1 for e in ev if isinstance(e, dict) and e.get("passed"))
        failed = sum(1 for e in ev if isinstance(e, dict) and e.get("passed") is False)
        try:
            lp = self._score_tokens(
                f"CLAIM: {claim[:1200]}\nPREUVES: {passed} passent, {failed} echouent "
                f"({', '.join(sorted({e.get('type', '') for e in ev if hasattr(e, 'get')}))}\n"
                "Les preuves supportent-elles le claim ?"
                "Reponds par UN mot (OUI ou NON). Reponse:",
                ["OUI", "NON"])
            s_raw = self._softmax(lp)
            if not s_raw:
                raise ValueError("no logprobs")
            s = s_raw.get("OUI", 0.5)
            label = ("supports" if s >= 0.8 else "contradicts" if s <= 0.2 else "inconclusive")
            return {"supports": round(s, 3), "contradicts": round(1.0 - s, 3),
                    "unknown": 0.0, "label": label, "provider": "jev-logits"}
        except Exception as e:
            logger.warning("jev-logits verify fallback: %s", e)
            return {"supports": 0.0, "contradicts": 0.0, "unknown": 1.0,
                    "label": "no_evidence", "provider": "rules"}

    def gate(self, action: str, destructive_threshold: float = 0.85) -> Dict:
        try:
            lp = self._score_tokens(
                f"ACTION PROPOSEE: {action[:2000]}\n"
                "Cette action est-elle DESTRUCTIVE/irreversible ?"
                "Reponds par UN mot (OUI ou NON). Reponse:",
                ["OUI", "NON"])
            d_raw = self._softmax(lp)
            if not d_raw:
                raise ValueError("no logprobs")
            d = d_raw.get("OUI", 0.5)
            if d >= 0.75:
                decision = "BLOCK"
            elif d >= 0.5:
                decision = "REVIEW"
            else:
                decision = "ALLOW"
            return {"decision": decision, "destructive_prob": d, "provider": "jev-logits"}
        except Exception as e:
            logger.warning("jev-logits gate fallback: %s", e)
            fb = RuleBasedProvider().gate(action, destructive_threshold)
            fb["provider"] = "rules"
            return fb

    def score(self, grid: Dict) -> Dict:
        """Score each criterion 0-4 via next-token distribution over digits."""
        criteria = {k: v for k, v in grid.items()
                    if k != "_weights" and isinstance(v, (int, float))}
        if not criteria:
            return {"score": 0.0, "label": "low", "per_criterion": {}, "provider": "jev-logits"}
        per, total = {}, 0.0
        try:
            for k, provided in criteria.items():
                lp = self._score_tokens(
                    f"Critere {k} (0=catastrophe .. 4=excellent). "
                    "Note le chiffre unique: 0 1 2 3 4",
                    [str(i) for i in range(5)])
                p = self._softmax(lp)
                if not p:
                    raise ValueError("no logprobs")
                v = sum(int(d) * p[d] for d in p)
                per[k] = round(v / 4.0, 3)
                total += per[k]
            out = total / len(criteria)
            label = ("high" if out >= 0.75 else "medium" if out >= 0.45 else "low")
            return {"score": round(out, 3), "label": label, "per_criterion": per,
                    "provider": "jev-logits"}
        except Exception as e:
            logger.warning("jev-logits score fallback: %s", e)
            fb = RuleBasedProvider().score(dict(grid))
            fb["provider"] = "rules"
            return fb

    def decide(self, context: str, options: list) -> Dict:
        if not options:
            return {"choice": None, "distribution": {}, "confidence": 0.0,
                    "provider": "jev-logits"}
        letters = [chr(ord("A") + i) for i in range(len(options))]
        try:
            menu = "\n".join(f"{l}. {o}" for l, o in zip(letters, options))
            lp = self._score_tokens(
                f"CONTEXTE: {context[:2000]}\nChoix:\n{menu}\nMeilleure lettre ?",
                letters)
            probs = self._softmax(lp)
            if not probs:
                raise ValueError("no logprobs")
            win = max(probs, key=probs.get)
            return {"choice": options[letters.index(win)], "distribution": probs,
                    "confidence": probs[win], "provider": "jev-logits"}
        except Exception as e:
            logger.warning("jev-logits decide fallback: %s", e)
            return {"choice": options[0], "distribution": {}, "confidence": 0.0,
                    "provider": "rules", "reason": str(e)}
