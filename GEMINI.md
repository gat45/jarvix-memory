# JARVIX Memory - Project Instructions

## Conventions
- **Language**: Python 3.10+
- **Architecture**: Modular memory layers (Episodic, Semantic, Procedural, etc.)
- **Storage**: SQLite + FTS5 as the primary engine.
- **Modularity**: Each layer should be independent and accessible via the `MemoryRouter`.

## Workflows
- **New Layer**: Inherit from `MemoryLayer` in `core/layer.py`.
- **Database Changes**: Update `Database` class in `core/database.py` and ensure FTS5 tables are synchronized.
- **Consolidation**: Tasks that require background processing should be added to `ConsolidationService`.

## Vision
JARVIX Memory aims to be more than a vector DB; it's a cognitive architecture that tracks provenance, confidence, and contradictions to provide a reliable long-term memory for AI agents.
