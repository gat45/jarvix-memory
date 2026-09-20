"""Batches JEV réels — gate actions prioritaires, verify 10 faits sem, score 3 stratégies."""
import sys, os, tempfile
sys.path.insert(0, "src")
from jarvix_memory.router import MemoryRouter
from jarvix_memory.core.models import Memory
import json, time

r = MemoryRouter()
conn = r.db._connect()

QUOTA_START = None

# ── BATCH 1: GATE les 10 actions les plus prioritaires ──────────
acts = conn.execute(
    "SELECT id, content, metadata FROM memories "
    "WHERE type='action' AND status='provisional' "
    "AND created_at > datetime('now', '-7 days') "
    "ORDER BY created_at DESC LIMIT 10").fetchall()
gated, executed, blocked, review = 0, 0, 0, 0
for aid, content, meta_raw in acts:
    try:
        g = r.jev.gate(content, log=True)
        gated += 1
        provider = g.get("provider")
        if provider not in ("jev-remote", "rules"):
            continue
        d = g["decision"]
        if d == "ALLOW":
            r.action.approve(aid)
            r.action.execute(aid, result="auto-exec-après-gate-jev", success=True)
            executed += 1
        elif d == "BLOCK":
            r.action.skip(aid, reason="jev gate: BLOCK (destructive)")
            blocked += 1
        else:
            review += 1  # REVIEW: on laisse pour l'humain, mais loggé
        time.sleep(2.0)
        print(f"[GATE] {content[:50]:52s} -> {d} ({provider})")
    except Exception as e:
        print(f"[GATE ERR] {content[:40]}: {e}")
print(f"=> gate : {gated} jugées, {executed} executées, {blocked} bloquées, {review} à review")

# ── BATCH 2: VERIFY 10 faits sémantiques prioritaires ──────────
mems = conn.execute(
    "SELECT id, content FROM memories WHERE type='semantic' AND status='provisional' "
    "ORDER BY confidence DESC, created_at DESC LIMIT 10").fetchall()
verified, rejected = 0, 0
for sid, content in mems:
    try:
        claim = r.verification.claim(f"{content[:300]}", source="jev-batch-verify")
        vp = r.jev.verify(content[:300], {"total": 0, "passed": 0, "failed": 0})  # sans preuve: signal
        verdict = "verified" if vp.get("label") == "supports" else (
            "rejected" if vp.get("label") == "contradicts" else "inconclusive")
        r.verification.add_evidence(claim.id, "measurement",
                                   "jev-noul sans preuve delta", vp.get("supports", 0.0) >= 0.8,
                                   {"supports": vp.get("supports"),
                                    "provider": vp.get("provider")})
        result = r.verification.resolve(claim.id)
        if result["verdict"] == "verified":
            verified += 1
        elif result["verdict"] == "rejected":
            rejected += 1
        else:
            # inconclusive: on archive le claim de test, le original reste provisoire
            r.verification.add_evidence(claim.id, "manual", "inconclusif avec JEV alone", False)
        time.sleep(2.0)
        print(f"[VERIF] {content[:50]:52s} -> {result['verdict']} ({vp.get('provider')})")
    except Exception as e:
        print(f"[VERIF ERR] {content[:40]}: {e}")
print(f"=> verify: {verified} verified / {rejected} rejetés / {10-verified-rejected} inconclusif")

# ── BATCH 3: SCORE 3 stratégies actives (top leaderboard) ──────
lb = r.strategy.leaderboard(3)
for s in lb:
    sid, name = s.get("id"), s.get("name")
    viz = {"monstrant_validé": s.get("rate"), "cost": s.get("avg_cost")}
    grid = {"evidence_quality": s.get("rate", 0.5)}  # data réelle injectée
    try:
        sc = r.jev.score(grid, subject=name)
        time.sleep(2.0)
        print(f"[SCORE] {name:28s} -> {sc.get('score')} ({sc.get('label')}) ({sc.get('provider')})")
    except Exception as e:
        print(f"[SCORE ERR] {name}: {e}")
