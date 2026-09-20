# JARVIX Memory

Persistent, multi-layered cognitive memory system for AI agents.

## Architecture

JARVIX Memory is organized into specialized modules, each handling a specific aspect of the agent's cognition.

### Core Modules
- **memory-core**: Common contracts, base schemas, and SQLite/FTS5 storage engine.
- **memory-router**: Orchestration and query routing between memory layers.

### Memory Layers
- **memory-episodic**: Log of events, tool calls, and observations (Raw history).
- **memory-semantic**: Extracted facts and persistent knowledge.
- **memory-procedural**: Skills, "how-to" guides, and verified workflows.
- **memory-working**: Short-term context and active task state.
- **memory-graph**: Temporal and semantic relations between entities.

### Meta-Memory & Analysis
- **memory-provenance**: Source tracking and evidence for claims.
- **memory-confidence**: Reliability scoring and contradiction management.
- **memory-hypothesis**: Tracking experimental paths and scientific hypotheses.
- **memory-error**: Specialized debugging memory and failure signatures.
- **memory-decision**: Log of architectural and logic decisions (The "Why").

### Lifecycle
- **memory-consolidation**: "Sleep" cycles for merging, pruning, and promoting memories.

## Usage

```python
from jarvix_memory.router import MemoryRouter

router = MemoryRouter()

# Log an event (Episodic)
router.episodic.log_event("Tested model", "Success")

# Store a fact (Semantic)
router.semantic.add_fact("The sky is blue", confidence=0.99)

# Define a relation (Graph)
router.graph.add_relation("Sky", "has_color", "Blue")

# Search across all layers
results = router.query("Sky")
for res in results:
    print(f"[{res['type']}] {res['content']}")
```

## Structure
- `core/`: Base abstractions and database.
- `layers/`: Specialized memory implementations.
- `router.py`: Orchestration and entry point.
- `consolidation/`: Background processing service.

## CLI agent (Buffy / terminal)

```bash
python D:\oneplus\memoire\memoire.py add "<contenu>" --type semantic --source "<src>"
python D:\oneplus\memoire\memoire.py search "<terms>"   # AND implicite, fallback OR
python D:\oneplus\memoire\memoire.py stats | list | get <id>
python D:\oneplus\memoire\memoire.py decision "<quoi>" "<pourquoi>"
python D:\oneplus\memoire\memoire.py episodic "<action>" "<resultat>"
python D:\oneplus\memoire\memoire.py graph "<sujet>" "<predicat>" "<objet>"
```

Notes d'intégration :
- DB ancrée au paquet (`D:\oneplus\memoire\jarvix_memory.db`) — appelable depuis n'importe quel CWD.
- Le FTS du core matche en phrase exacte ; la CLI contourne en requêtes pré-quotées (AND implicite → fallback OR).
- Le MCP server (`mcp_server.py`) reste le chemin canonique pour opencode (`pip install -e .` requis pour l'import `jarvix_memory`).
- Répartition : RAG `op15-forensics` = preuves pipeline BM25 ; JARVIX = mémoire cognitive agent (décisions, stratégies, épisodique).
