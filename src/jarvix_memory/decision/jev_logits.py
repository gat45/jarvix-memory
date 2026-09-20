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
        """One completion with logprobs=5; extract logprob of each candidate
        token for the NEXT token. Works with llama.cpp server."""
        from urllib.parse import urlparse
        from pathlib import Path as _Path
        candidates = [c.upper()[:1] if len(c) == 1 else c.upper() for c in candidates]
        # nouns may need a leading space depending on tokenizer; try both joins
        tail = "Answer strictly with single choice: "
        full_prompt = f"{prompt}\n{tail}"
        payload = json.dumps({
            "prompt": full_prompt,
            "max_tokens": 1,
            "temperature": 0.0,
            "logprobs": 10,
            "echo": False,
            "top_k": 50,
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/completion",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            body = json.loads(resp.read())
        # llama.cpp /completion returns tokens/probs list; logits view:
        content = body.get("content", "")
        probs = body.get("completion_probabilities") or \
            (body.get("choices") or [{}])[0].get("logprobs", {}) or {}
        # top_logprobs list of dicts
        top = []
        if isinstance(probs, dict) and probs.get("content"):
            for item in probs["content"][:1]:
                top = item.get("top_logprobs") or item.get("logprobs", []) or []
        elif isinstance(probs, list):
            top = probs[:1]
        out = {c: -20.0 for c in candidates}
        if not top:
            # no raw logprobs: fallback, mustn't pretend
            return {}
        for entry in top:
            if not isinstance(entry, dict):
                continue
            lp = entry.get("logprob")
            tok = (entry.get("token") or "").strip().upper()
            if lp is not None and tok in out:
                out[tok] = max(out[tok], float(lp))
        # check: content token maps if in candidates
        if content.strip().upper()[:1] in out and out[content.strip().upper()] == -20.0:
            pass  # keep logprobs-anchored result only
        return out

    def _softmax(self, logprobs: Dict[str, float], temp: float = 1.0) -> Dict[str, float]:
        mx = max(logprobs.values())
        exps = {k: math.exp((v - mx) / temp) for k, v in logprobs.items()}
        s = sum(exps.values()) or 1.0
        return {k: round(v / s, 3) for k, v in exps.items()}

    # ── DecisionProvider contract ─────────────────────────────

    def route(self, query: str) -> Dict:
        layers = ["e", "s", "p", "d", "h", "g", "r"]  # episodic,semantic,procedural,decision,hypothesis,graph,recovery
        names = {"e": "episodic", "s": "semantic", "p": "procedural", "d": "decision",
                 "h": "hypothesis", "g": "graph", "r": "recovery"}
        try:
            lp = self._score_tokens(
                f"Question agent: {query}\n"
                "CHOIX de couche memoire la plus utile: e=episodic(events), "
                "s=semantic facts, p=procedural(how-to), d=decision rarionale, "
                "h=hypothesis a tester, g=graphe relations, r=recovery echec.",
                layers)
            probs = self._softmax(lp)
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
                "Faut-il injecter cette memoire dans le contexte MAINTENANT ? OUI ou NON.",
                ["O", "N"])  # first letters
            p = self._softmax(lp)
            yes = p.get("O", 0.5)
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
                f"({', '.join(sorted({e.get('type', '') for e in ev if hasattr(e, 'get')}))}.\n"
                "Les preuves supportent-elles le claim ? OUI ou NON.",
                ["O", "N"])
            s = self._softmax(lp).get("O", 0.5)
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
                "Cette action est-elle DESTRUCTIVE/irreversible ? OUI ou NON.",
                ["O", "N"])
            d = self._softmax(lp).get("O", 0.5)
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
            win = max(probs, key=probs.get)
            return {"choice": options[letters.index(win)], "distribution": probs,
                    "confidence": probs[win], "provider": "jev-logits"}
        except Exception as e:
            logger.warning("jev-logits decide fallback: %s", e)
            return {"choice": options[0], "distribution": {}, "confidence": 0.0,
                    "provider": "rules", "reason": str(e)}
