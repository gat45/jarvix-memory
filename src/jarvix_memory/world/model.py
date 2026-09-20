from ..core.database import Database
from ..core.models import Memory, MemoryType
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class WorldModel:
    """MEMORY -> WORLD STATE -> PREDICT -> OBSERVE -> COMPARE -> UPDATE"""

    def __init__(self, db: Database):
        self.db = db

    def get_state(self) -> Dict[str, Any]:
        states = self.db.search_by_type("world", limit=1)
        if not states:
            return {"initialized": False, "beliefs": {}}
        meta = json.loads(states[0].get("metadata", "{}"))
        return meta.get("state", {"initialized": False, "beliefs": {}})

    def update_state(self, key: str, value: Any, confidence: float = 0.8) -> Memory:
        state = self.get_state()
        state.setdefault("beliefs", {})[key] = {
            "value": value,
            "confidence": confidence,
            "updated_at": datetime.utcnow().isoformat(),
        }
        state["initialized"] = True
        memory = Memory(
            type=MemoryType.WORLD,
            content=f"World state update: {key} = {value}",
            confidence=confidence,
            metadata={"state": state, "update_key": key},
        )
        self.db.insert_memory(memory)
        return memory

    def predict(
        self,
        hypothesis: str,
        expected_result: Any = None,
        expected_cost: Dict[str, float] = None,
        expected_risk: float = 0.0,
    ) -> Memory:
        meta = {
            "hypothesis": hypothesis,
            "expected_result": expected_result,
            "expected_cost": expected_cost or {},
            "expected_risk": expected_risk,
            "status": "pending",
            "predictions": [],
        }
        memory = Memory(
            type=MemoryType.WORLD,
            content=f"Prediction: {hypothesis}",
            metadata=meta,
        )
        self.db.insert_memory(memory)
        return memory

    def observe(self, prediction_id: str, actual_result: Any, actual_cost: Dict[str, float] = None) -> Dict[str, Any]:
        mem = self.db.get_memory(prediction_id)
        if not mem:
            return {"error": "prediction not found"}

        meta = json.loads(mem.get("metadata", "{}"))
        expected = meta.get("expected_result")
        actual = {
            "result": actual_result,
            "cost": actual_cost or {},
            "observed_at": datetime.utcnow().isoformat(),
        }
        meta.setdefault("predictions", []).append(actual)
        meta["status"] = "observed"

        if expected is not None:
            meta["match"] = self._compare_values(expected, actual_result)
            meta["delta"] = self._compute_delta(expected, actual_result)
        else:
            meta["match"] = None

        self.db.update_memory(prediction_id, metadata=json.dumps(meta))
        return {
            "prediction_id": prediction_id,
            "expected": expected,
            "actual": actual_result,
            "match": meta.get("match"),
            "delta": meta.get("delta"),
        }

    def accuracy(self, limit: int = 50) -> Dict[str, Any]:
        rows = self.db.search_by_type("world", limit=limit * 2)
        predictions = []
        for r in rows:
            meta = json.loads(r.get("metadata", "{}"))
            if meta.get("status") == "observed" and "match" in meta:
                predictions.append(meta)
        if not predictions:
            return {"total": 0, "matches": 0, "accuracy": 0.0}
        matches = sum(1 for p in predictions if p.get("match"))
        return {
            "total": len(predictions),
            "matches": matches,
            "accuracy": matches / len(predictions),
        }

    def get_beliefs(self) -> Dict[str, Any]:
        state = self.get_state()
        return state.get("beliefs", {})

    def get_predictions(self, status: str = "pending", limit: int = 20) -> List[Dict]:
        all_world = self.db.search_by_type("world", limit=limit * 2)
        results = []
        for r in all_world:
            meta = json.loads(r.get("metadata", "{}"))
            if meta.get("status") == status and "hypothesis" in meta:
                results.append({"id": r["id"], "content": r["content"], **meta})
        return results[:limit]

    def _compute_delta(self, expected: Any, actual: Any) -> Any:
        if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            return actual - expected
        return None

    def _compare_values(self, expected: Any, actual: Any) -> bool:
        """Compare expected vs actual with numeric tolerance."""
        if expected == actual:
            return True
        # Try numeric comparison for strings like "+24%" vs "+24.2%"
        try:
            exp_num = float(str(expected).replace("%", "").replace("+", ""))
            act_num = float(str(actual).replace("%", "").replace("+", ""))
            return abs(exp_num - act_num) < 0.01
        except (ValueError, TypeError):
            return False
