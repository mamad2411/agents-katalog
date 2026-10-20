---
name: langgraph-compat-shim-import-path-preserved
description: Keep a one-line import-shim module at an old path (e.g. app/graph_pipeline.py) that re-exports build_graph from the new location, so deployed langgraph.json configs that hard-code the old path keep working through internal refactors.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [refactor, compatibility, langgraph, deployment]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/graph_pipeline.py
imported_at: 2026-04-18T00:00:00Z
---

# LangGraph Build-Graph Compatibility Shim

## When to use
You moved `build_graph` from `app/graph_pipeline.py` to `app/pipeline/graph.py` but your `langgraph.json`, hosted deployment env, or third-party MCP/CI configs still reference the old path. Renaming everything atomically is impossible.

## How it works
A 5-line module at the old path re-exports the new symbol. `__all__` documents the public surface so static analyzers don't flag the unused import.

## Example
```python
"""Compatibility shim for deployed LangGraph entrypoints.

Production deployment config and older internal docs still reference
``app.graph_pipeline:build_graph``. The actual implementation now lives in
``app.pipeline.graph``, so this module preserves that import path.
"""

from __future__ import annotations

from app.pipeline.graph import build_graph

__all__ = ["build_graph"]
```

Deployment config keeps working unchanged:
```dockerfile
ENV LANGSERVE_GRAPHS='{"agent":"/deps/agent/app/graph_pipeline.py:build_graph"}'
```

## Gotchas
- Document why the shim exists in the module docstring; otherwise a future cleanup PR will delete it and break prod silently.
- For LangGraph specifically, both `langgraph.json` and the Dockerfile `LANGSERVE_GRAPHS` env are common pinning points — grep for both.
- Once a deprecation window passes (track in CHANGELOG), update both internal and documentation references then delete the shim.
