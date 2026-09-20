import sys, time
sys.path.insert(0, "src")
from jarvix_memory.router import MemoryRouter

r = MemoryRouter()
t0 = time.time(); r.db.search_hybrid("NPU profiling", limit=3); t1 = (time.time()-t0)*1000
t0 = time.time(); r2 = r.db.recall_cost_aware("MBUF 3500", limit=3); t2 = (time.time()-t0)*1000
t0 = time.time(); junk = r.db.recall_cost_aware("xyz123noexist bulldog", limit=1); t3 = (time.time()-t0)*1000
t0 = time.time(); bb = r.live.bundle("oneplus"); t4 = (time.time()-t0)*1000
j = r.jev.gate("flash le bootloader", log=False)
print(f"hybrid         : {t1:.0f} ms")
print(f"cost-aware     : {t2:.0f} ms | {len(r2)} results")
print(f"abstention junk: {junk[0].get('abstain')} | {t3:.0f} ms")
print(f"live bundle    : {len(bb['items'])} items | {t4:.0f} ms")
print(f"jev gate live  : {j['decision']} ({j.get('provider')})")
