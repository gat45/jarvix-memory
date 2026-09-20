import importlib.metadata as md

for pkg in ["pydantic", "mcp", "sentence-transformers", "torch", "numpy",
            "flask", "flask-cors", "transformers", "pytest"]:
    try:
        meta = md.metadata(pkg)
        lic = meta.get("License") or "n/a"
        print("|%s|%s|%s|" % (pkg, lic, meta.get("Version")))
    except Exception:
        print("|%s|NOT-INSTALLED||" % pkg)
