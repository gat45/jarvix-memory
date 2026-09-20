# Licences et Crédits · Licenses & Credits

JARVIX Memory est sous **MIT** (voir `LICENSE`). Ce fichier liste tout ce que le projet embarque ou dont il s'inspire, avec les licences correspondantes.

## 1. Dépendances logicielles (Runtime obligatoire)

| Paquet | Version testée | Licence | Rôle |
|---|---|---|---|
| [pydantic](https://github.com/pydantic/pydantic) | 2.12 | MIT | Modèles de données (Memory, schemas) |
| [mcp](https://github.com/modelcontextprotocol/python-sdk) | 1.27 | MIT | Serveur MCP (87 tools pour agents) |
| [sqlite](https://sqlite.org/) | (stdlib via Python) | **Domaine public** | Stockage, journal WAL, FTS via LIKE |

## 2. Dépendances optionnelles (vector + ui extras)

| Paquet | Version testée | Licence | Rôle |
|---|---|---|---|
| [flask](https://github.com/pallets/flask) | 3.1 | BSD-3-Clause | Interface web |
| [flask-cors](https://github.com/corydolphston/flask-cors) | 6.0 | MIT | CORS pour l'UI |
| [sentence-transformers](https://github.com/UKPLab/sentence-transformers) | 5.2 | Apache-2.0 | Embeddings (RAG vectoriel) |
| [transformers](https://github.com/huggingface/transformers) | 4.57 | Apache-2.0 | Backend des modèles d'embedding |
| [torch](https://github.com/pytorch/pytorch) | 2.14 | BSD-3-Clause | Backend d'inférence des embeddings |
| [numpy](https://github.com/numpy/numpy) | 2.4 | BSD-3-Clause | Calcul de similarité cosinus |
| [pytest](https://github.com/pytest-dev/pytest) | 9.0 | MIT | Suite de test |

Les dépendances BSD/MIT/Apache ne sont pas copiées dans ce dépôt — leurs textes sont dans les distributions originales.

## 3. Modèle d'embedding

| Modèle | Licence | Source |
|---|---|---|
| [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | Apache-2.0 | sentence-transformers (UKPLab) — 384 dims, ~80 MB |

Téléchargé automatiquement depuis Hugging Face Hub au premier usage ; fonctionne aussi hors-ligne une fois mis en cache.

## 4. Infrastructures externes (recommandé, non requis)

| Projet | Licence | Rôle dans ce projet |
|---|---|---|
| [llama.cpp / llama-server](https://github.com/ggml-org/llama.cpp) | MIT | Serveur LLM local optionnel (RAG, bilans, résumés) |
| [GitHub CLI (gh)](https://cli.github.com/) | MIT | Utilisé par l'autopilot pour `git push` |

## 5. Inspirations (idées, pas de code copié)

L'architecture de JARVIX doit explicitement ce qui suit à des projets publics que nous recommandons. Aucun code copié ; crédits conceptuels :

| Projet | Ce que nous en avons retenu |
|---|---|
| [apattichis/cognitive-memory-agent](https://github.com/apattichis/cognitive-memory-agent) | Séparation 4 mémoires + consolidation/sommeil |
| [Zijian-Ni/agent-memory](https://github.com/Zijian-Ni/agent-memory) | decay, répétition espacée, retrieval hybride |
| [MythologIQ-Labs/agent-memory](https://github.com/MythologIQ-Labs/agent-memory) | Questions de gouvernance mémoire (admission/mutation/oubli) |
| [agentclash/agentic-memory](https://github.com/agentclash/agentic-memory) | Learning ≠ Memory ; métacognition ; event bus |
| [ipiton/agent-memory-mcp](https://github.com/ipiton/agent-memory-mcp) | stewardship, supersession, provenance gate, valid_from/until |
| [Katra-Agentic-Memory](https://github.com/Katra-Agentic-Memory) | mémoire privée vs partagée multi-agents |
| [agentralabs/agentic-memory](https://github.com/agentralabs/agentic-memory) | stockage HOT/WARM/COLD, append-only, BLAKE3 |
| [Provem](https://github.com/RichLonelyAI/Provem) (gouvernance backend-agnostique) | Memory Gate indépendant du backend |
| [causal-memory](https://github.com/darwin-sim/causal-memory) | relations décision→résultat persistantes |
| [WorldMM](https://github.com/WorldMM-CVPR2026/WorldMM) | mémoire épisodique+visuelle pour raisonnement vidéo |
| AgentMem / travaux 2026 | l'agent est témoin non fiable : ancrer la mémoire sur fichiers/git réels |
| Meta AI 2026 (mémoire comme politique) | injection sélective silencieuse par défaut |
| [neoneye/agent-memory-atlas](https://github.com/neoneye/agent-memory-atlas) | benchmarks : deletion, contradiction, supersession, coût |

### Écosystème Jev / System One (alternatives + sources)

Le protocole typé `POST /v1/systemone` (noul/choice/score) provient de [TypeSafe AI](https://typesafe.ai) (jev, closed-weights). Alternatives open-weight que `JevRemoteProvider` supporte directement (même wire protocol) :

| Alternative | Modèle | Comment le brancher |
|---|---|---|
| TypeSafe direct ([[api.typesafe.ai](https://api.typesafe.ai)]) | jev-latest (jev-1.13.0) | `jev_base_url` + clé TypeSafe |
| [jev-agent.com](https://jev-agent.com) | jev-1.13.0 via proxy | `jev_base_url=https://jev-agent.com/api/v1` + clé `jv_live_` |
| [LitJev](https://github.com/zhengxuyu/litjev) | Qwen3.x local (pas d'entraînement) | `jev_local_url=http://127.0.0.1:8000`, `jev_provider=local` |
| [LocalJev](https://github.com/githubnext/localjev) | DiffusionGemma via oMLX | `jev_local_url=http://127.0.0.1:8080` |
| [simple-jev](https://github.com/featherless-ai/simple-jev) | Qwen3.5-0.8B (+ RFDT fine-tune) | `jev_local_url=http://127.0.0.1:8000` |
| [open-jev](https://github.com/daseinlabs/open-jev) | Gemma 3 4B (MLX/Apple) | `jev_local_url=<serveur>` |
| [OpenJEV](https://openjev.sh) (cloud open) | openjev | `jev_base_url=https://api.openjev.sh/v1` + clé |

Concrètement : `config.json` → `jev_provider: local` + `jev_local_url` route tous les jugements vers un moteur **entièrement local** (aucun token à la fin du mois, tout reste sur ta machine).

Les concepts retenus implémentés ici de manière originale : boucle fermée `observer → expérimenter → vérifier → mémoriser → apprendre → planifier → agir → mesurer → corriger`, mémoire négative `do_not_repeat`, environnements fingerprintés, value/cost retrieval, et couche décision JEV typée.

## 6. Conformité

- Tout le code tiers ci-dessus est utilisé selon ses termes ; aucun fichier de licence tierce n'est omis intentionnellement.
- Si une dépendance manque à l'appel : le Paquet se dégrade gracefully (recherche LIKE au lieu du vectoriel, UI sans Flask, etc.).
