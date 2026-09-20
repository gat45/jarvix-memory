"""Flask UI for JARVIX Memory — dashboard + search + chat."""

import json
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from jarvix_memory.router import MemoryRouter
from jarvix_memory.core.vector_store import VectorStore
from jarvix_memory.core.migration import run_migrations, get_version
from jarvix_memory.llm.reasoner import LLMReasoner

app = Flask(__name__, template_folder="templates")
CORS(app)

# Init components
DB_PATH = str(Path(__file__).resolve().parent.parent.parent.parent / "jarvix_memory.db")
router = MemoryRouter(db_path=DB_PATH)
vector_store = VectorStore(router.db)
llm = LLMReasoner(router.db, vector_store=vector_store)


@app.route("/")
def index():
    stats = router.stats()
    vec_stats = vector_store.stats()
    llm_health = llm.health()
    db_version = get_version(router.db._connect())
    return render_template("index.html", stats=stats, vec_stats=vec_stats,
                           llm_health=llm_health, db_version=db_version)


@app.route("/api/search", methods=["POST"])
def api_search():
    data = request.json or {}
    query = data.get("query", "")
    mode = data.get("mode", "hybrid")  # text, vector, hybrid
    limit = data.get("limit", 10)

    results = []
    if mode == "vector":
        results = vector_store.search(query, limit=limit)
    elif mode == "text":
        results = router.db.search_fts(query, limit=limit)
    else:  # hybrid
        vec_results = vector_store.search(query, limit=limit)
        text_results = router.db.search_fts(query, limit=limit)
        # Merge and deduplicate
        seen = set()
        for r in vec_results + text_results:
            mid = r.get("id")
            if mid not in seen:
                seen.add(mid)
                results.append(r)
        results = results[:limit]

    return jsonify({"results": results, "count": len(results)})


@app.route("/api/reason", methods=["POST"])
def api_reason():
    data = request.json or {}
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "query required"}), 400

    result = llm.reason(query)
    return jsonify(result)


@app.route("/api/memories", methods=["GET"])
def api_memories():
    mem_type = request.args.get("type")
    limit = int(request.args.get("limit", 50))
    if mem_type:
        results = router.db.search_by_type(mem_type, limit=limit)
    else:
        results = router.db.list_all(limit=limit)
    return jsonify({"memories": results, "count": len(results)})


@app.route("/api/memories", methods=["POST"])
def api_add_memory():
    data = request.json or {}
    content = data.get("content", "")
    mem_type = data.get("type", "semantic")
    confidence = data.get("confidence", 1.0)
    source = data.get("source")

    if not content:
        return jsonify({"error": "content required"}), 400

    from jarvix_memory.core.models import Memory
    mem = Memory(type=mem_type, content=content, confidence=confidence, source=source)
    router.db.insert_memory(mem)

    # Auto-embed
    try:
        vector_store.embed_and_store(mem.id, content)
    except Exception as e:
        app.logger.warning("Embedding failed: %s", e)

    return jsonify({"id": mem.id, "type": mem_type, "status": "created"})


@app.route("/api/memories/<memory_id>", methods=["GET"])
def api_get_memory(memory_id):
    mem = router.db.get_memory(memory_id)
    if not mem:
        return jsonify({"error": "not found"}), 404
    return jsonify(mem)


@app.route("/api/memories/<memory_id>", methods=["DELETE"])
def api_delete_memory(memory_id):
    ok = router.db.delete_memory(memory_id)
    return jsonify({"deleted": ok})


@app.route("/api/connections/<memory_id>", methods=["GET"])
def api_connections(memory_id):
    result = llm.find_connections(memory_id)
    return jsonify(result)


@app.route("/api/health", methods=["GET"])
def api_health():
    return jsonify({
        "status": "ok",
        "memories": router.stats(),
        "vector_store": vector_store.stats(),
        "llm": llm.health(),
        "db_version": get_version(router.db._connect()),
    })


@app.route("/api/rebuild-embeddings", methods=["POST"])
def api_rebuild_embeddings():
    count = vector_store.rebuild()
    return jsonify({"embedded": count})


def run_ui(host="127.0.0.1", port=5000, debug=False):
    app.run(host=host, port=port, debug=debug)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="JARVIX Memory UI")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    print(f"JARVIX Memory UI -> http://{args.host}:{args.port}")
    run_ui(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
