from ..core.database import Database
from ..core.models import Memory
import sqlite3
import json
import uuid
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ConsolidationService:
    def __init__(self, db: Database):
        self.db = db

    def run_sleep_cycle(self):
        logger.info("Starting consolidation sleep cycle")
        self.decay_importance()
        self.merge_episodic_to_semantic()
        self.archive_old_provisional()
        logger.info("Consolidation complete")

    def decay_importance(self, decay_factor: float = 0.95, min_importance: float = 0.1):
        conn = self.db._connect()
        conn.execute("""
            UPDATE memories
            SET importance = MAX(importance * ?, ?)
            WHERE importance > ?
        """, (decay_factor, min_importance, min_importance))
        conn.commit()

    def merge_episodic_to_semantic(self, min_repeat: int = 3):
        conn = self.db._connect()
        conn.row_factory = sqlite3.Row
        episodic = conn.execute(
            "SELECT content, COUNT(*) as cnt FROM memories "
            "WHERE type = 'episodic' GROUP BY content HAVING cnt >= ?",
            (min_repeat,)
        ).fetchall()
        merged = 0
        for row in episodic:
            existing = conn.execute(
                "SELECT id FROM memories WHERE type = 'semantic' AND content = ?",
                (row["content"],)
            ).fetchone()
            if not existing:
                mem = Memory(
                    type="semantic",
                    content=row["content"],
                    status="verified",
                    confidence=0.8,
                    importance=0.7,
                    source="consolidation",
                    metadata={"merged_from": "episodic", "repeat_count": row["cnt"]},
                )
                self.db.insert_memory(mem)
                merged += 1
        if merged:
            logger.info("Merged %d episodic memories into semantic", merged)

    def archive_old_provisional(self, max_age_days: int = 30):
        conn = self.db._connect()
        conn.execute("SAVEPOINT sp_archive")
        try:
            rows = conn.execute(
                "SELECT id FROM memories WHERE status = 'provisional' "
                "AND created_at < datetime('now', ? || ' days')",
                (f'-{max_age_days}',)
            ).fetchall()
            for row in rows:
                conn.execute(
                    "UPDATE memories SET status = 'archived' WHERE id = ?",
                    (row[0],)
                )
                self._fts_sync_status(conn, row[0], "archived")
            conn.execute("RELEASE sp_archive")
            if rows:
                logger.info("Archived %d old provisional memories", len(rows))
        except Exception:
            conn.execute("ROLLBACK TO sp_archive")
            raise

    def _fts_sync_status(self, conn: sqlite3.Connection, memory_id: str, new_status: str):
        try:
            conn.execute("DELETE FROM memories_fts WHERE id = ?", (memory_id,))
            row = conn.execute(
                "SELECT content, type FROM memories WHERE id = ?", (memory_id,)
            ).fetchone()
            if row:
                conn.execute(
                    "INSERT INTO memories_fts(id, content, type, status) VALUES (?, ?, ?, ?)",
                    (memory_id, row[0], row[1], new_status),
                )
        except Exception as e:
            logger.warning("FTS status sync failed for %s: %s", memory_id, e)

    def stats(self) -> dict:
        conn = self.db._connect()
        rows = conn.execute(
            "SELECT type, status, COUNT(*) as cnt FROM memories GROUP BY type, status"
        ).fetchall()
        # clés stringifiées : json.dumps (MCP) refuse les clés tuple
        return {f"{r[0]}/{r[1]}": r[2] for r in rows}
