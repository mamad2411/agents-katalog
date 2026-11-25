---
name: byted-escloud
description: "Manages Volcano Engine (Volcengine/火山引擎) ESCloud and CloudSearch clusters for lifecycle operations and Elasticsearch/OpenSearch data-plane tasks. Use when the user mentions ESCloud, CloudSearch, or Elasticsearch/OpenSearch on Volcengine."
version: 1.2.1
---

# Volcano Engine ESCloud

## Use when

- The user needs to manage ESCloud or CloudSearch on Volcano Engine / Volcengine.
- The task is a control-plane lifecycle action such as create, inspect, scale, expose, restart, or delete.
- The task is an Elasticsearch/OpenSearch data-plane workflow such as cluster validation, inspection, indexing, querying, aggregation, or bulk guidance.

## Route

- Control-plane lifecycle workflows -> `scripts/control.py` and [CONTROL_PLANE.md](CONTROL_PLANE.md)
- Control-plane fallback tools -> `scripts/control_tools.py` and [CONTROL_TOOLS.md](CONTROL_TOOLS.md)
- Data-plane workflows -> [DATA_PLANE.md](DATA_PLANE.md)

## Guardrails

- Always run the bundled CLIs with `{baseDir}/venv/bin/python`.
- Before any data-plane read or write, run `data.py --endpoint <endpoint> info`; if it fails, stop and fix endpoint exposure, allowlist, credentials, or TLS first.
- Use `data.py smoke_test` for new-cluster validation; if the test index already exists, pass `--reuse-existing` or choose a different `--index`; delete its test index only with `--cleanup --confirm`.
- For non-routine data-plane work, prefer ad-hoc `curl` or small Python snippets grounded in the data-plane references instead of expanding `data.py`.
- Require explicit confirmation before destructive or high-impact operations such as deletes, alias cutovers, bulk mutations, `_delete_by_query`, `_update_by_query`, or `_reindex`.
