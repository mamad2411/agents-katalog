---
name: langgraph-api-dockerfile-with-healthcheck
description: Production Dockerfile for a LangGraph agent that uses the official langchain/langgraph-api base image, installs the package against API constraints.txt, points LANGSERVE_GRAPHS at the build_graph factory, and includes a HEALTHCHECK using only stdlib urllib.
category: build
version: 1.0.0
version_origin: extracted
tags: [docker, langgraph, healthcheck, deployment]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: Dockerfile
imported_at: 2026-04-18T00:00:00Z
---

# LangGraph API Dockerfile with Stdlib Healthcheck

## When to use
You're deploying a LangGraph-based agent to a self-hosted Railway/EC2/ECS environment (not LangSmith Deployments). You need a slim Dockerfile that uses the official LangGraph API server, installs your agent's deps under the API's pinned constraints, and supports a Docker HEALTHCHECK without curl in the base image.

## How it works
- `FROM langchain/langgraph-api:3.11` provides the API server, port 2024, and `/ok` health endpoint.
- `pip install --no-cache-dir -c /api/constraints.txt /deps/agent` pins all transitive deps to versions tested by the LangGraph maintainers.
- `LANGSERVE_GRAPHS` env wires your agent factory by file:symbol path.
- HEALTHCHECK uses `python -c "import urllib.request; urllib.request.urlopen('http://localhost:2024/ok', timeout=5)"` — no curl/wget required in the image.

## Example
```dockerfile
FROM langchain/langgraph-api:3.11

ADD . /deps/agent

RUN PYTHONDONTWRITEBYTECODE=1 \
    pip install --no-cache-dir -c /api/constraints.txt /deps/agent

# Intentionally omit custom auth here; self-hosted LangGraph does not
# support enterprise-only custom auth.
ENV LANGSERVE_GRAPHS='{"agent":"/deps/agent/app/graph_pipeline.py:build_graph"}'

WORKDIR /deps/agent
EXPOSE 2024

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:2024/ok', timeout=5)" || exit 1
```

## Gotchas
- `--start-period=60s` is critical — LangGraph's first-time DB migration can take 30+ seconds and the container would otherwise be marked unhealthy and recycled.
- Pin against `/api/constraints.txt` so a newer pydantic/langchain release doesn't break the API server in your image.
- `PYTHONDONTWRITEBYTECODE=1` shaves layer size by ~30% — no `__pycache__` directories.
- Bind your `LANGSERVE_GRAPHS` path to a stable shim module (see `langgraph-compat-shim-import-path-preserved`) so internal refactors don't require rebuilding the image config.
