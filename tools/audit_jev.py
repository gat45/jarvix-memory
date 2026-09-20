"""Audit complet du projet sur toute la mémoire + plan d'actions spécifique JEV."""
import sys
sys.path.insert(0, "src")
from jarvix_memory.router import MemoryRouter
import json

r = MemoryRouter()
conn = r.db._connect()
print("=" * 64)
print("AUDIT COMPLET SUR TOUTE LA MÉMOIRE")
print("=" * 64)
st = r.stats()
total = st.pop("total_memories")
print(f"Total: {total} souvenirs")
for k, v in sorted(st.items(), key=lambda x: -x[1]):
    if v:
        print(f"  {k:12s}: {v}")

# état de la boucle cognitive
n_verified = conn.execute("SELECT COUNT(*) FROM memories WHERE type='evidence' AND status='verified'").fetchone()[0]
n_invalid = conn.execute("SELECT COUNT(*) FROM memories WHERE type='evidence' AND status='invalid'").fetchone()[0]
n_hyp_refuted = conn.execute("SELECT COUNT(*) FROM memories WHERE type='hypothesis' AND metadata LIKE '%REFUTED%'").fetchone()[0]
n_hyp_pend = len(r.experiment.pending_hypotheses(limit=100))
n_actions_pend = len(r.action.pending())
n_dnr = conn.execute("SELECT COUNT(*) FROM memories WHERE type='hypothesis' AND metadata LIKE '%do_not_repeat\": true%'").fetchone()[0]
n_unverified_sem = conn.execute("SELECT COUNT(*) FROM memories WHERE type='semantic' AND status='provisional'").fetchone()[0]
n_sem_verified = conn.execute("SELECT COUNT(*) FROM memories WHERE type='semantic' AND status='verified'").fetchone()[0]
n_decisions_logged = conn.execute("SELECT COUNT(*) FROM memories WHERE content LIKE 'JEV %'").fetchone()[0]
print(f"claims: {n_verified} vérifiés / {n_invalid} rejetés | hypothèses: {n_hyp_refuted} réfutées, {n_hyp_pend} en attente | do_not_repeat: {n_dnr}")
print(f"actions pending: {n_actions_pend} | sémantique: {n_sem_verified} vérifiés vs {n_unverified_sem} provisoires | décisions JEV loggées: {n_decisions_logged}")

# ce que JEV devrait juger
print()
print("CE QUE JEV PEUT FAIRE MAINTENANT")
print(f"  [GATE] {n_actions_pend} actions proposees -> gate avant approve/execute")
print(f"  [VERIFY] {n_unverified_sem} facts sem provisoires sans preuve -> verify_auto avant promotion")
print(f"  [ROUTE] chaque chat -> choisir la couche (meme si rules suffisent offline)")
pend = r.experiment.pending_hypotheses(limit=5)
if pend:
    print("  [DECIDE] prochains tests a orienter:")
    for h in pend[:3]:
        print(f"     - {h['content'][:60]} ({h['attempts']} essay)")
lb = r.strategy.leaderboard(3)
if lb:
    print(f"  [SCORE] {len(lb)} strategies a evaluer avec jev score (factuel, pas sa teinte)")
quit()
