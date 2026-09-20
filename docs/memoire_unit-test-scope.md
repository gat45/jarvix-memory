# Mémoire exportée — 2026-09-20 15:52

Projet : `unit-test-scope` · 472 souvenirs · générée par JARVIX autopilot

## action (46)

- [provisional|conf=1.0] Test mmap configuration
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal
- [provisional|conf=1.0] Test MBUF=4000
- [provisional|conf=1.0] Investigate OOM
- [provisional|conf=1.0] Check thermal

## decision (22)

- [provisional|conf=1.0] Decision: profiler-v3 copie interne profiler-v3-work (original gele)
Reasoning: ExpertEvent/ExpertState/DecisionEvent + exactly-once + registre expert 3D + benefit/loss marginale ; tests 20/20 ; registre valide sur marcoV2 (19488 experts, 4.03 GiB) ; Q4_1 mixte ffn_down confirme
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=0.9] Decision: abandonner ngl=40 (T3b) comme config par defaut. Reasoning: le gain etait un artefact thermique, indistinguable de ngl=60+MBUF3500 a froid, et chauffe a 78,7 degC. Alternatives: A/B apparie complet (6 runs ~30 min) si preuve contraire voulue.
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=1.0] Decision: Corriger le deadlock MCP upia par stdin=subprocess.DEVNULL dans _run()
Reasoning: Le CLI upia enfant héritait du stdin du serveur (pipe MCP sans EOF) et se bloquait à la première lecture ; le subprocess standalone passait en 0,55s, prouvant que le blocage venait de l'héritage de flux et non du CLI ni du store. Alternative rejetée : réécrire le CLI upia (trop invasif) ou passer par un tra…
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=1.0] Decision: Serveur LLM upia fixé sur llama-upstream b10837 + IQ4NL, ctx 16384
Reasoning: Diagnostic en 3 étapes : (1) curl direct sur lamaturbot b1-30d6881 = tokens '?' → le serveur est en cause, pas upia ; (2) header GGUF (tools/gguf_arch.py) : arch qwen35 sur les 2 GGUF → bug décodage du build TurboQuant+ ; (3) b10837 vanilla lit le même arch correctement. ctx 2048→16384 car le prompt de synthèse…
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=0.7] JEV score: ui-test -> high
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=0.7] JEV score: ui-test -> high
- [provisional|conf=1.0] Decision: Use MBUF=3500
Reasoning: +24% throughput, no quality loss
- [provisional|conf=0.7] JEV score: ui-test -> high

## environment (13)

- [provisional|conf=1.0] ENVIRONMENT env_c9db3d27f513: {"bench_device": "ci-pc", "git_commit": "e60d01f3b9f3", "machine": "AMD64", "os": "Windows", "os_release": "11", "python": "3.14.2"}
- [provisional|conf=1.0] ENVIRONMENT env_cf672303bfaa: {"bench_device": "ci-phone", "git_commit": "e60d01f3b9f3", "machine": "AMD64", "os": "Windows", "os_release": "11", "python": "3.14.2"}
- [provisional|conf=1.0] ENVIRONMENT env_db69c12ff877: {"bench_device": "debug-pc", "git_commit": "e60d01f3b9f3", "machine": "AMD64", "os": "Windows", "os_release": "11", "python": "3.14.2"}
- [provisional|conf=1.0] ENVIRONMENT env_ff72242a6384: {"bench_device": "x-pc", "git_commit": "e60d01f3b9f3", "machine": "AMD64", "os": "Windows", "os_release": "11", "python": "3.14.2"}
- [provisional|conf=1.0] ENVIRONMENT env_269f878f43f4: {"bench_device": "y-phone", "git_commit": "e60d01f3b9f3", "machine": "AMD64", "os": "Windows", "os_release": "11", "python": "3.14.2"}
- [provisional|conf=1.0] ENVIRONMENT env_042bfe5d3c45: {"bench_device": "z-pc", "git_commit": "e60d01f3b9f3", "machine": "AMD64", "os": "Windows", "os_release": "11", "python": "3.14.2"}
- [provisional|conf=1.0] ENVIRONMENT env_b56201b4aca0: {"bench_device": "z-phone", "git_commit": "e60d01f3b9f3", "machine": "AMD64", "os": "Windows", "os_release": "11", "python": "3.14.2"}
- [provisional|conf=1.0] ENVIRONMENT env_25dea354beec: {"bench_device": "ci-pc", "git_commit": "f2d47dcd0cec", "machine": "AMD64", "os": "Windows", "os_release": "11", "python": "3.14.2"}
- [provisional|conf=1.0] ENVIRONMENT env_134ad6fcea1b: {"bench_device": "ci-phone", "git_commit": "f2d47dcd0cec", "machine": "AMD64", "os": "Windows", "os_release": "11", "python": "3.14.2"}
- [provisional|conf=1.0] ENVIRONMENT env_1d0320677ce7: {"bench_device": "ci-pc", "git_commit": "7290a1f8ecc2", "machine": "AMD64", "os": "Windows", "os_release": "11", "python": "3.14.2"}
- [provisional|conf=1.0] ENVIRONMENT env_371988d097d6: {"bench_device": "ci-phone", "git_commit": "7290a1f8ecc2", "machine": "AMD64", "os": "Windows", "os_release": "11", "python": "3.14.2"}
- [provisional|conf=1.0] ENVIRONMENT env_73674cc3171e: {"bench_device": "ci-pc", "git_commit": "766efe855c75", "machine": "AMD64", "os": "Windows", "os_release": "11", "python": "3.14.2"}
- [provisional|conf=1.0] ENVIRONMENT env_5b65378b8ab0: {"bench_device": "ci-phone", "git_commit": "766efe855c75", "machine": "AMD64", "os": "Windows", "os_release": "11", "python": "3.14.2"}

## episodic (45)

- [provisional|conf=1.0] Action: Tested Qwen3.5-9B
Result: Success on SM8850
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=1.0] Action: Full directory inventory scan of D:\oneplus
Result: 33,760 key files (filtered from 59,486 total), 5,504 directories. 34.1 GB total. Report written to D:\oneplus\INVENTORY.txt
- [provisional|conf=1.0] Action: rapport pipeline (RAG+UPIA+JARVIX)
Result: RAPPORT_SESSION_MCP_UPIA_2026-09-20.md ingere
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=1.0] FTS test after LIKE fix
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=1.0] Action: Test des 7 outils MCP upia (tools/test_upia_mcp.py)
Result: 7/7 OK après fix stdin deadlock ; upia_update a ingéré les commits 2026-09-18 (events 1233+, claims 1061, entités 5576) ; consigné en 3 souvenirs semantic.
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=1.0] Action: upia_update complet + upia_ask avec synthèse LLM sur 18181
Result: update OK (entités 6024) ; ask OK 13,3s « LLM: oui » synthèse cohérente. Chemin validé : b10837 + IQ4NL + ctx 16384 ; lamaturbot b1-30d6881 inutilisable (garbage '?' sur arch qwen35).
- [provisional|conf=1.0] Action: rapport pipeline (RAG+UPIA+JARVIX)
Result: RAPPORT_SESSION_MCP_UPIA_LLM_2026-09-20.md ingere
- [provisional|conf=1.0] Action: Fixes de durabilité LLM upia (bat ctx 16384 + _fail() dans llm.py)
Result: Validés 2 chemins (dead URL / 18181) ; addendum au rapport 20/09 ré-ingéré RAG ; ingestion UPIA D:\oneplus confirmée finie (4180 entités).
- [provisional|conf=1.0] Action: Clôture session 20/09 (test Cyber sur b10837 + health-check LLM)
Result: Cyber Q4_K_M OK sur b10837 → coupable = build b1-30d6881 ; health-check 2 s validé (URL morte 3 s au lieu de 3,5 min) ; serveur 18181 restauré IQ4NL+ctx16384 ; consolidation lancée.
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=1.0] Action: Commit dca4d24 (parent) : MCP upia + LLM 18181 + test non-regression
Result: 11 fichiers, 744 insertions (tools/, rapport, .gitignore). start_cyber.bat reoriente b10837+ctx16384. test_upia_mcp.py smoke promu dans AGENTS.md (ligne non commitee : +38 lignes preexistantes d une autre session). memoire/ = repo embarque, fix stats() deja dans f2d47dc.
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=1.0] Action: Commits de cloture : 3dfcd0c (parent, AGENTS.md) + 335f0b8 (harness, llm.py)
Result: AGENTS.md : 39 insertions (smoke line recorregee dans le fence + reflexes N4/N5 preexistants). Harness (branche codex/profiler-v5-formats) : llm.py seul, 73+/3- ( _fail + health-check), autres mods non touchés.
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=0.8] OBSERVATION [C:\Users\videl\AppData\Local\Temp\ui_test_signals.log]: SIGSEGV 0xc0 in htp | note: ui-test
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=0.8] OBSERVATION [C:\Users\videl\AppData\Local\Temp\ui_test_signals.log]: SIGSEGV 0xc0 in htp | note: ui-test
- [provisional|conf=1.0] Action: Commit 33bad96 : untrack clones vendored (graft 73, local-dream-master 147, snapdragon-npu-llm-main 14)
Result: 320940 lignes sorties de l index, disque intact, .gitignore aligne sur la politique AGENTS.md. Tri tools/ : aucun doublon byte-identique, tout conserve. memoire/ clean : P0 commit par la session parallele (5ea7878).
- [provisional|conf=1.0] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [provisional|conf=0.8] OBSERVATION [C:\Users\videl\AppData\Local\Temp\ui_test_signals.log]: SIGSEGV 0xc0 in htp | note: ui-test

## evidence (42)

- [verified|conf=1.0] Fixed crash in build.cpp
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] pyproject exists
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] pyproject exists
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] pyproject exists
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] pyproject exists
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] pyproject exists
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] pyproject exists
- [provisional|conf=1.0] ARTIFACT C:\Users\videl\AppData\Local\Temp\ui_test_signals.log sha256=18bd932e9265c296acf748ba71d115642323a2b646488e69e233e5987509e302
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] pyproject exists
- [provisional|conf=1.0] ARTIFACT C:\Users\videl\AppData\Local\Temp\ui_test_signals.log sha256=18bd932e9265c296acf748ba71d115642323a2b646488e69e233e5987509e302
- [verified|conf=1.0] Fixed EACCES in exp_launch.sh
- [invalid|conf=1.0] Will fix thermal
- [verified|conf=1.0] pyproject exists
- [provisional|conf=1.0] ARTIFACT C:\Users\videl\AppData\Local\Temp\ui_test_signals.log sha256=18bd932e9265c296acf748ba71d115642323a2b646488e69e233e5987509e302

## experiment (12)

- [provisional|conf=1.0] [t1] no effect (ENV env_c9db3d27f513)
- [provisional|conf=1.0] [t2] bad (ENV env_c9db3d27f513)
- [provisional|conf=1.0] [t1] no effect (ENV env_25dea354beec)
- [provisional|conf=1.0] [t2] bad (ENV env_25dea354beec)
- [provisional|conf=1.0] [t1] no effect (ENV env_25dea354beec)
- [provisional|conf=1.0] [t2] bad (ENV env_25dea354beec)
- [provisional|conf=1.0] [t1] no effect (ENV env_1d0320677ce7)
- [provisional|conf=1.0] [t2] bad (ENV env_1d0320677ce7)
- [provisional|conf=1.0] [t1] no effect (ENV env_1d0320677ce7)
- [provisional|conf=1.0] [t2] bad (ENV env_1d0320677ce7)
- [provisional|conf=1.0] [t1] no effect (ENV env_73674cc3171e)
- [provisional|conf=1.0] [t2] bad (ENV env_73674cc3171e)

## graph (31)

- [provisional|conf=1.0] Qwen3.5-9B --[uses]--> Q4_K_M
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81
- [provisional|conf=1.0] Qwen3.5-9B --[quantized_with]--> Q4_K_M
- [provisional|conf=1.0] Q4_K_M --[runs_on]--> HTP v81

## hypothesis (6)

- [provisional|conf=1.0] guard test: mmap causes reboot
- [provisional|conf=1.0] guard test: mmap causes reboot
- [provisional|conf=1.0] guard test: mmap causes reboot
- [provisional|conf=1.0] guard test: mmap causes reboot
- [provisional|conf=1.0] guard test: mmap causes reboot
- [provisional|conf=1.0] guard test: mmap causes reboot

## learning (16)

- [provisional|conf=0.9] Learning from bf962e6c-5a92-415a-b468-a913f6d9fe3a: Always check mmap before modifying backend
- [provisional|conf=0.92] Learning from 576463fc-a7a6-49b9-a13a-b440a983df01: Always check mmap before modifying HTP backend
- [provisional|conf=0.92] Learning from 5f076520-24ab-401a-9f9e-ff97a016c3a7: Always check mmap before modifying HTP backend
- [provisional|conf=0.92] Learning from 973af0b5-ead4-4b42-b2e7-3e4148947bf1: Always check mmap before modifying HTP backend
- [provisional|conf=0.92] Learning from 9a25d541-c348-4e73-8344-0814f944a8af: Always check mmap before modifying HTP backend
- [provisional|conf=0.92] Learning from 3e2811db-57d5-4e17-bd84-5d0da277df69: Always check mmap before modifying HTP backend
- [provisional|conf=0.92] Learning from 5dec286b-49f5-4670-95ee-d2fc51e913d0: Always check mmap before modifying HTP backend
- [provisional|conf=0.92] Learning from 1ea4e875-52d6-405c-b72b-521152318891: Always check mmap before modifying HTP backend
- [provisional|conf=0.92] Learning from ca5aafa9-2945-4560-8c96-d96ea4eed7ba: Always check mmap before modifying HTP backend
- [provisional|conf=0.92] Learning from 3bc147ef-5d2a-4c23-a60a-569b4f925491: Always check mmap before modifying HTP backend
- [provisional|conf=0.92] Learning from 6189c185-d9c6-4f89-b979-4cc3bcbc1252: Always check mmap before modifying HTP backend
- [provisional|conf=0.92] Learning from af612165-06fd-4042-ad3e-95db953f921e: Always check mmap before modifying HTP backend
- [provisional|conf=0.92] Learning from 1aed37d2-2f02-42c0-b792-89aba006e36c: Always check mmap before modifying HTP backend
- [provisional|conf=0.92] Learning from d81b99b7-8549-4d45-923b-95d5dd7bc0c2: Always check mmap before modifying HTP backend
- [provisional|conf=0.92] Learning from 189c16a2-f589-4909-b4cc-3de976e1ab7b: Always check mmap before modifying HTP backend
- [provisional|conf=0.92] Learning from 8b079e59-f287-4786-8d63-ca415c985680: Always check mmap before modifying HTP backend

## procedural (17)

- [provisional|conf=1.0] gradle assembleDebug --no-daemon
- [provisional|conf=0.9] Bench governor P4 : python governor/p4_loop.py --model <path> --nodes <A..L> ; depart device < 45 degC obligatoire, seed 42, garde thermique 80/65/70 degC, cost model + trace JSON. Config gagnante : ngl=60 + GGML_HEXAGON_MBUF=3500.
- [provisional|conf=1.0] gradle assembleDebug --no-daemon
- [provisional|conf=1.0] gradle assembleDebug --no-daemon
- [provisional|conf=1.0] gradle assembleDebug --no-daemon
- [provisional|conf=1.0] gradle assembleDebug --no-daemon
- [provisional|conf=1.0] gradle assembleDebug --no-daemon
- [provisional|conf=1.0] PROBLÈME : serveur MCP (FastMCP/python mcp SDK, Windows) dont les tools/call
hangent indéfiniment alors que initialize + tools/list répondent ; process
python orphelins qui s'accumulent.

CAUSE : un tool qui lance subprocess.run() SANS stdin explicite → le processus
enfant hérite du stdin du serveur MCP (= pipe JSON-RPC du client, ouvert sans
EOF). Toute lecture stdin de l'enfant bloque → subproce…
- [provisional|conf=1.0] gradle assembleDebug --no-daemon
- [provisional|conf=1.0] gradle assembleDebug --no-daemon
- [provisional|conf=1.0] gradle assembleDebug --no-daemon
- [provisional|conf=1.0] gradle assembleDebug --no-daemon
- [provisional|conf=1.0] gradle assembleDebug --no-daemon
- [provisional|conf=1.0] gradle assembleDebug --no-daemon
- [provisional|conf=1.0] gradle assembleDebug --no-daemon
- [provisional|conf=1.0] gradle assembleDebug --no-daemon
- [provisional|conf=1.0] gradle assembleDebug --no-daemon

## recovery (31)

- [provisional|conf=1.0] Failure in test_001: OOM during HTP load
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM
- [provisional|conf=1.0] Failure in exp_001: SIGSEGV at 0xc
- [provisional|conf=1.0] Failure in exp_002: OOM

## semantic (110)

- [provisional|conf=0.95] Qwen3.5-9B works on SM8850
- [provisional|conf=1.0] GGML_TYPE_IDS canoniques: Q4_0=2 Q8_0=8 Q4_K=12 IQ4_NL=20 (verifies gguf-py)
- [provisional|conf=1.0] test retour add_fact
- [provisional|conf=1.0] GGML_TYPE_IDS canoniques: Q4_0=2 Q8_0=8 Q4_K=12 IQ4_NL=20 (verifies gguf-py officiel)
- [provisional|conf=1.0] P0-H extended_udma OP15: patch ab-wt commit 98173ab6 - has_extended_map (probe EXTENDED_MAP_SUPPORT) etait jamis consomme; ajoute rpc_mmap_extended + rpc_mempool_mib (env GGML_HEXAGON_RPC_MMAP_EXTENDED / GGML_HEXAGON_MEMPOOL_MIB), flags FASTRPC_MAP_FD[_DELAYED]_EXTENDED gate probe, downgrade one-shot si kernel rejette, cible mempool override (4600 MiB possible). Build ab-build-xudma (PREBUILT_LIB_…
- [provisional|conf=1.0] P0-H extension complete (commits ab-wt 98173ab6 + bed734ad): (1) decouverte CMake - GGML_HEXAGON_USE_MEMPOOL=ON build fastrpc.cpp+htp-drv.cpp, ggml-hexagon.cpp = variante dspqueue -> patch couvre les 2 variantes; (2) cross-TU accesseur ggml_hexagon_get_rpc_mmap_cfg: strong (cfg+env) dans fastrpc.cpp, weak env-only dans ggml-hexagon.cpp; (3) buffers tenseurs ggml_hexagon_shared_buffer::mmap honoren…
- [provisional|conf=1.0] SM8850 has Hexagon HTP v81
- [provisional|conf=0.95] Qwen3.5-9B runs at 7.15 tok/s on MBUF=3500
- [provisional|conf=0.95] T3b (ngl=40) 'gain' = artefact de protocole thermique : a froid, ngl=60+MBUF3500 atteint 9,379 tok/s ~ T3b froid 9,414 tok/s. ngl=40 a abandonner sauf preuve contraire d'un A/B apparie complet.
- [provisional|conf=0.97] Lecon de methode OP15 : toute comparaison de configs doit apparier le cycle thermique (depart < 45 degC, 1 run par cycle) - ecart froid/chaud ~ +31 % sur le debit.
- [provisional|conf=0.9] Requant Gemma3n E4B : variante A3 recommandee = Q4_0 + token_embd F16 + per_layer_token_embd Q8_0 -> 5,41 GiB poids, ~6,2 GiB RAM total. Quantification EN ATTENTE de lancement, puis gate PPL delta < 2 % vs F16 (wiki.test.raw).
- [provisional|conf=0.9] Couverture HTP fork ab-wt (ggml-hexagon.cpp l.1012-1031) : Q4_0/Q4_1/Q8_0/IQ4_NL supportes ; Q6_K/Q2_K/Q4_K/Q5_1/Q5_K NON -> repli CPU par token sur ces formats.
- [provisional|conf=0.9] Menage git en attente : renommage xdna2-forensics -> op15-forensics vu comme 271 suppressions + 155 fichiers non trackes ; ~2500 lignes modifiees non commitrees dans app/.
- [provisional|conf=0.9] Device OP15 CPH2747 (2026-09-19) : migre 204->400, bootloader deverrouille, root Magisk 30.7, Android 16, kernel 6.12.23 ; RAM libre ~2 Go (purge standard -> 6-7 Go), swap 4,47 GiB.
- [provisional|conf=0.95] MCP jarvix-memory branche dans opencode.json racine (python312 + memoire/mcp_server.py, stdio). Reflexe N4 AGENTS.md : memory_search avant toute re-lecture de rapport ; conclusions -> semantic_add, decisions -> decision_log, procedures -> procedural_skill.
- [provisional|conf=0.95] Outils harness E:/oneplus/geniex_harness branches (2026-09-20) : upia (memoire temporelle projet, py -3.12, store governor_state/upia/E_oneplus_geniex_harness : 1233 events, 106 commits, 687 docs) + unified_rag (py -3.14, CLI search --mode bm25|vector|hybrid, corpus rapports harness). Routage grave dans AGENTS.md table protocole. upia init/update/ask/status/events/graph/unknown/research/watch.
- [provisional|conf=0.9] UPIA = Universal Project Intelligence Agent : modele temporel revisable de projet (DISCOVERY -> INGESTION -> MEMORY -> ANSWER avec provenance). Garanties epistemiques : OBSERVED/INFERRED/ASSUMED/CONFIRMED/REJECTED/SUPERSEDED ; registre des inconnus ; LLM local optionnel (UPIA_LLM_URL), sinon reponse deterministe BM25 + intentions canoniques.
- [provisional|conf=0.95] MCP upia branche dans opencode.json racine (D:/oneplus/tools/upia_mcp_server.py, python312) : 7 outils upia_ask/status/events/graph/unknown/update/research deleguant au CLI governor.upia.upia.cli (cwd E:/oneplus/geniex_harness). Store vivant = ~/.upia/store/E_oneplus_geniex_harness (Sep 8, 1233 events) > governor_state/upia (Sep 6, plus ancien).
- [provisional|conf=0.9] upia + llama.cpp local : env persistante UPIA_LLM_URL=http://127.0.0.1:8080/v1, UPIA_LLM_KEY=none (setx HKCU). Patch applique E:/oneplus/geniex_harness/governor/upia/upia/llm.py : chat_template_kwargs enable_thinking=false par defaut (env UPIA_LLM_THINK=1 pour reactiver) car Bonsai-27B est un modele reasoning -> content vide sinon. LIMITE : Bonsai-27B-Q1_0 (quant 1-bit) trop faible pour la synthes…
- [provisional|conf=0.9] Rapport de session — 2026-09-20 — Branchement mémoire & outils (JARVIX + UPIA + RAG)
## Verdicts clés
- **JARVIX Memory branché en MCP natif opencode** : `opencode.json` racine expose
- **UPIA identifié et branché** : Universal Project Intelligence Agent
- **Serveur MCP upia créé** : `tools/upia_mcp_server.py` — 7 outils
- **Stores upia synchronisés** : `governor_state/upia/E_oneplus_geniex_harnes…
- [provisional|conf=0.95] ANGLE MORT: 6 scripts de patch timeout identiques (patch_timeout_jz.py, tools/patch_timeout.py, tools/patch_timeout_v050.py, tools/patch_timeout_final.py, tools/patch_dspqueue_timeout.py, tools/patch_geniex_timeout.py) — meme logique, offsets differents. A consolider en 1 script parametre.
- [provisional|conf=0.95] ANGLE MORT: 8 fichiers .so orphelins racine (~42 MB) non references par aucun script: libggml-hexagon-patched-final.so, patched-v2.so, patched-npu.so, verify.so, 3gib.so, device.so, coherent.so, librpcmem_dmabuf.so. A supprimer.
- [provisional|conf=0.95] ANGLE MORT: 50+ fichiers .log stale dans jz_work snapdragon/vm/ — disk bloat massif. Logs gouverneur (matrix_run*.log, t3b_cold.log) aussi stale. .gitignore ignore *.log mais restent sur disque.
- [provisional|conf=0.95] ANGLE MORT: 3 parsers GGUF copies dans profile_q5_layer_detail.py, profile_q5_mixed_precision.py, profile_q5_precision_analysis.py — read_gguf() + DTYPE_MAP identiques. A extraire dans tools/gguf_utils.py.
- [provisional|conf=0.95] ANGLE MORT: 4 variants de sweep OPBATCH (opbatch_sweep.sh, opbatch_sweep2.sh, run_opbatch_sweep.sh, sweep_opbatch.sh) + 2 variants RTT (sweep_rtt.sh, rtt_sweep.sh). A consolider.
- [provisional|conf=0.95] ANGLE MORT: check_symbols2.py reference repertoire inexistant ./ab-build-otfix/. Script casse.
- [provisional|conf=0.95] ANGLE MORT: 6x def log(msg) identiques dans apk_pipeline.py, d2_htp_profiler.py, htp_l2_traffic_probe.py, htp_make_calibration.py, sm8850_quant_matrix.py, governor/p4_watch.py. A extraire dans tools/log.py.
- [provisional|conf=0.95] ANGLE MORT: 20+ scripts reverse_npu et jz_work snapdragon/vm avec chemins hardcodes C:\Users\videl\Desktop\oneplus\... — casse si deplacement. A relativeiser.
- [provisional|conf=0.95] ANGLE MORT: Aucun test pour d2_htp_profiler.py (804 lignes), sm8850_quant_matrix.py (561 lignes), apk_pipeline.py, governor/*.py, tools/parse_fastrpc_*.py, tools/patch_*.py.
- [provisional|conf=0.95] ANGLE MORT: htp_l2_traffic_probe.py a 7 TODO(user) non resolus — tags v81, patterns, categories atrace, compteurs DMA, perfetto, chemins reverse. Script a moitie implemente.
- [provisional|conf=0.95] ANGLE MORT: 6 scripts de patch timeout identiques (patch_timeout_jz.py + 5 dans tools/) - meme logique, offsets differents. A consolider en 1 script parametre.
- [provisional|conf=0.95] ANGLE MORT: 8 .so orphelins racine (~42 MB) non references: libggml-hexagon-patched-final/v2/npu/verify/3gib/device/coherent.so + librpcmem_dmabuf.so. A supprimer.
- [provisional|conf=0.95] ANGLE MORT: 50+ logs stale dans jz_work/vm/ + governor/*.log - disk bloat. .gitignore ignore *.log mais restent sur disque.
- [provisional|conf=0.95] ANGLE MORT: 3 parsers GGUF copies (profile_q5_*.py) - read_gguf() + DTYPE_MAP x3. A extraire dans tools/gguf_utils.py.
- [provisional|conf=0.95] ANGLE MORT: 4 variants OPBATCH sweep + 2 variants RTT sweep - doublons. A consolider.
- [provisional|conf=0.95] ANGLE MORT: check_symbols2.py reference ./ab-build-otfix/ inexistant. Script casse.
- [provisional|conf=0.95] ANGLE MORT: 6x def log() identiques dans 6 scripts. A extraire dans tools/log.py.
- [provisional|conf=0.95] ANGLE MORT: 20+ scripts avec chemins hardcodes C:\Users\videl\Desktop\oneplus - casse si deplacement. A relativeiser.
- [provisional|conf=0.95] ANGLE MORT: 0 test pour d2_htp_profiler.py (804l), sm8850_quant_matrix.py (561l), apk_pipeline.py, governor/*.py, tools/parse_*.py, tools/patch_*.py.
- [provisional|conf=0.95] ANGLE MORT: htp_l2_traffic_probe.py a 7 TODO(user) non resolus - tags, patterns, atrace, DMA, perfetto, chemins reverse. Script a moitie implemente.
- [provisional|conf=1.0] CRITIQUE: memoire.py:113 r.strategy.best() n existe pas. Devrait etre best_for_situation(). CLI strategy-best casse.
- [provisional|conf=1.0] CRITIQUE: FTS5 sans content=memories - sync manuel. consolidation/decay/archive ne sync PAS le FTS, index stale.
- [provisional|conf=1.0] CRITIQUE: FTS5 query pas d echappement double-quote - requete cassee si query contient guillemet.
- [provisional|conf=0.95] HIGH: MemoryModel.embedding jamais utilise - code mort dans models.py:70.
- [provisional|conf=0.95] HIGH: Version mismatch - pyproject=0.3.0, init=0.2.0, main=0.2.0.
- [provisional|conf=0.95] HIGH: proactive/rules in-memory uniquement, perdu au restart. Pas d outil MCP pour rules.
- [provisional|conf=0.95] HIGH: N+1 queries dans 6 layers - charge tout en Python, pas en SQL. LENT.
- [provisional|conf=0.9] MEDIUM: bilan.py os.chdir() side effect global - change CWD MCP server.
- [provisional|conf=0.9] MEDIUM: 0 test pour MultimodalEngine, ConsolidationService, bilan.py, CLI. test_all_tools utilise DB production.
- [provisional|conf=0.9] MEDIUM: MCP tools sans try/except - traceback brut envoye au client si layer throw.
- [provisional|conf=0.9] MEDIUM: Pas de migration DB - CREATE TABLE IF NOT EXISTS. Schema change = intervention manuelle.
- [provisional|conf=0.85] LOW: graph pas de traversee inverse. Procedural get_skill charge 100 lignes pour trouver 1.
- [provisional|conf=0.85] LOW: world prediction match = string exacte (+24 pourcent != +24.2 pourcent). Accuracy inutile numerique.
- [provisional|conf=1.0] SM8850 has Hexagon HTP v81
- [provisional|conf=0.95] Qwen3.5-9B runs at 7.15 tok/s on MBUF=3500
- [provisional|conf=1.0] SM8850 has Hexagon HTP v81
- [provisional|conf=0.95] Qwen3.5-9B runs at 7.15 tok/s on MBUF=3500
- [verified|conf=0.8] Action: QNN crash happened
Result: SIGSEGV at 0xc
- [verified|conf=0.8] Action: compiled APK
Result: build OK, 151 MB
- [provisional|conf=1.0] SM8850 has Hexagon HTP v81
- [provisional|conf=0.95] Qwen3.5-9B runs at 7.15 tok/s on MBUF=3500
- [provisional|conf=0.95] Session 2026-09-20: FTS5 supprime (LIKE search), @safe_tool sur 35 outils MCP, bilan.py --analyze corrige (strip think tags), tests 29/29 + 55/56. Rapport: reports/RAPPORT_SESSION_2026-09-20.md
- [provisional|conf=1.0] Test 2026-09-20 : les 7 outils MCP upia (tools/upia_mcp_server.py) passent 7/7 via client stdio — upia_status 0,4s · upia_events 0,2s · upia_graph 0,2s · upia_unknown 0,2s · upia_ask 4,4s (recherche déterministe, LLM non sollicité) · upia_update 21,1s (5576 entités, commits 2026-09-18 ingérés) · upia_research 1,0s (8 résultats GitHub).
- [provisional|conf=1.0] Bug deadlock corrigé dans tools/upia_mcp_server.py : le CLI upia lancé par subprocess.run héritait du stdin du serveur MCP (pipe client sans EOF) et bloquait tout tools/call (>60s, process orphelins) → fix stdin=subprocess.DEVNULL — status passe de hang à 0,4s. Toute nouvelle écriture subprocess dans un serveur MCP FastMCP doit rediriger stdin.
- [provisional|conf=1.0] Le UnicodeEncodeError 'charmap' lors des tests upia venait du print() du client de test (stdout Windows cp1252), PAS du serveur MCP ; serveur reconfiguré UTF-8 (sys.stdout.reconfigure) par précaution. Diagnostic : positions d'erreur identiques (394-395) sur deux runs = symptôme client, pas serveur.
- [provisional|conf=1.0] SM8850 has Hexagon HTP v81
- [provisional|conf=0.95] Qwen3.5-9B runs at 7.15 tok/s on MBUF=3500
- [provisional|conf=0.95] Session 2026-09-20 (2): 4 features implementees. VectorStore all-MiniLM-L6-v2 (384d, 158 embeds, 0.0075s/recherche, auto-embed + fallback LIKE). Schema DB v4 via migration.py. LLMReasoner (RAG /v1/chat/completions + summarize + connections, deg graceful si llama down). UI Flask :127.0.0.1:5000 (jarvix-ui). 8 nouveaux MCP tools = 64 total. torch 2.14.0+cpu reinstalle (ancien torch_cuda.dll corrompu…
- [provisional|conf=1.0] SM8850 has Hexagon HTP v81
- [provisional|conf=0.95] Qwen3.5-9B runs at 7.15 tok/s on MBUF=3500
- [provisional|conf=1.0] upia_update complet via MCP : OK en 12,4s (events 432 re-scannés, claims 1099, entités 6024, 120 commits vérifiés) — « aucun nouvel événement détecté » après l'update initial : store à jour au 2026-09-20.
- [provisional|conf=1.0] Garbage « ? » résolu : le build lamaturbot TurboQuant+ b1-30d6881 décode MAL l'arch qwen35 (les 2 GGUF Qwen3.8-9B — Cyber Q4_K_M et IQ4NL mtpQ2 — ont general.architecture=qwen35) et produit uniquement des tokens '?' dans reasoning_content. Le build vanilla llama-upstream b10837 lit le même GGUF IQ4NL correctement (32,5 tok/s, texte cohérent). Règle : pour les GGUF qwen35, utiliser llama-upstream b…
- [provisional|conf=1.0] Synthèse LLM upia_ask fonctionnelle sur 18181 : OK 13,3s, « LLM: oui », synthèse française cohérente avec citations [n], think vide (patch enable_thinking:false efficace). CONDITION CRITIQUE : ctx-size 16384 — avec le ctx 2048 du start_upstream.bat, le prompt upia (~7k tokens : 18 blocs × 1200 chars) dépasse le contexte → HTTP 400 avalé par le « except: return None » de synthesize()/gap_analysis()…
- [provisional|conf=1.0] Serveur 18181 au 2026-09-20 : llama-upstream b10837 + D:/qwen9b_IQ4NL_owIQ4NL_mtpQ2.gguf, ngl 999, ctx 16384, KV q4_0, reasoning-format deepseek (log: tools/llama_server_upstream16k.log). start_upstream.bat actuel a ctx 2048 → à mettre à jour sinon régression silencieuse au prochain redémarrage.
- [provisional|conf=1.0] Inconnu ouvert : le GGUF Cyber Q4_K_M (V3_Merged, arch qwen35) n'est correct sur AUCUN build testé — b1-30d6881 = garbage '?', b10837 non testé avec ce GGUF.
- [provisional|conf=1.0] Procédure enregistrée « mcp_subprocess_stdin_deadlock » (JARVIX procedural) : tout tool MCP qui spawn un process doit passer stdin=subprocess.DEVNULL — sinon l'enfant hérite du pipe JSON-RPC sans EOF et hang le tools/call. Diagnostic : test standalone rapide + log CallToolRequest sans réponse + process orphelins. Client de test réutilisable : tools/test_upia_mcp.py.
- [provisional|conf=0.9] Rapport de session — 2026-09-20 (2) — Outils MCP upia, LLM 18181 & pipeline mémoires
## Verdicts clés
- **7/7 outils MCP upia testés OK** le 2026-09-20 via client stdio (`tools/test_upia_mcp.py`) :
- **Fix 1 (critique) — deadlock stdin** dans `D:\oneplus\tools\upia_mcp_server.py` : le CLI
- **Fix 2 (défensif) — UTF-8** : stdout/stderr du serveur reconfigurés utf-8 ; le vrai
- **`upia_update` compl…
- [provisional|conf=1.0] start_upstream.bat corrigé le 2026-09-20 : ctx-size 2048 → 16384 — le fix LLM upia survit aux redémarrages manuels. Rappel : ctx 2048 = prompt upia (~7k tokens) rejeté HTTP 400 → fallback « LLM: non » silencieux.
- [provisional|conf=1.0] governor/upia/upia/llm.py : synthesize() et gap_analysis() loggent leurs échecs sur stderr via helper _fail() (format « [upia-llm] ERREUR ...: Type: détail -> fallback deterministe » ; HTTPError → 300 octets de body). Contrat None inchangé. Validé 2026-09-20 : URL morte → message + « LLM: non » ; 18181 → « LLM: oui » réponse cohérente citation [12].
- [provisional|conf=1.0] Quirk Windows : une URL LLM morte en localhost (port 9) HANG jusqu'au timeout (90 s gap_analysis + 120 s synthesize ≈ 3,5 min par ask) au lieu d'un refus instantané — amélioration possible : health-check rapide dans llm_available().

## strategy (31)

- [provisional|conf=1.0] Strategy: QNN debug
Situation: QNN crash on memory allocation
Steps: check allocation -> measure RSS -> verify mmap
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling
- [provisional|conf=1.0] Strategy: NPU debug
Situation: QNN crash on HTP
Steps: check alloc -> check mmap -> check skel
- [provisional|conf=1.0] Strategy: Thermal debug
Situation: device overheats
Steps: check LMh -> check cooling

## world (50)

- [provisional|conf=0.8] World state update: device_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=3500 improves throughput
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=1.0] Predicting [bench_tok_s] in [30..40] ENV env_ui
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=1.0] Predicting [bench_tok_s] in [30..40] ENV env_ui
- [provisional|conf=0.9] World state update: npu_temp = 65.0
- [provisional|conf=1.0] Prediction: MBUF=5000 gives +40%
- [provisional|conf=1.0] Prediction: ngl=60 is optimal
- [provisional|conf=1.0] Predicting [bench_tok_s] in [30..40] ENV env_ui
