---
name: riskmodels-api-discovery
description: >-
  Discover RiskModels API endpoints, schemas, and billing before building clients.
  Use when adding or editing SDK methods, HTTP examples, CLI, MCP tools, or any
  code that calls riskmodels.app. Requires RiskModels MCP when available; falls
  back to OPENAPI_SPEC.yaml and mcp/data/openapi.json.
---

# RiskModels API discovery

## When to use this skill

Apply **before** implementing or refactoring:

- New Python/TypeScript/CLI calls to `https://riskmodels.app/api`
- SDK methods in `sdk/riskmodels/client.py`
- Example scripts under `examples/python/` or `packages/riskmodels/examples/`
- Anything that embeds paths, JSON bodies, or query params for the public API

**Do not use this skill to answer a stock or portfolio question.** The catalog resources (`riskmodels:///capabilities`, `riskmodels:///schemas/{path}`, `riskmodels:///openapi`) are for wiring a client. Live numbers come from the MCP tools (`riskmodels_get_stock_snapshot`, `riskmodels_decompose`, `riskmodels_compare`, `riskmodels_get_returns`, …) or the matching REST routes. After an MCP OAuth connect, call a data tool first — reading the catalog does not count as activation.

## Discovery order (mandatory for client work)

### 1. MCP resources (if connected)

Since `@riskmodels/mcp` 2.0.0 the catalog is served as **MCP resources**, not tools (the tool list is in `mcp/README.md`):

| Step | Resource | Purpose |
|------|----------|--------|
| 1 | **`riskmodels:///capabilities`** | Latest index of capabilities: ids, HTTP method, path, parameters, pricing, examples. Read this first so you are not working from an outdated mental model. |
| 2 | **`riskmodels:///schemas/list`** / **`riskmodels:///schemas/{path}`** | JSON response schema for an endpoint (e.g. `ticker-returns-v2.json`). |
| 3 | **`riskmodels:///openapi`** | Full OpenAPI 3 spec. |

Treat these resources as the **provisioning schema** for what the API exposes and how it bills—prefer them over remembered URLs when the server is available. Without MCP, read `mcp/data/capabilities.json` directly.

### 2. Repo sources (always)

Regardless of MCP:

- **`OPENAPI_SPEC.yaml`** — canonical REST contract at repo root.
- **`mcp/data/openapi.json`** — JSON mirror used by the MCP server; good for grep and CI.
- **`lib/api/schemas.ts`** — Zod validation for Next.js routes (must stay aligned with OpenAPI).
- **`SEMANTIC_ALIASES.md`** — field names for user-facing tables and the Python SDK.

### 3. CLI / ad-hoc data exploration

The `cli-query` capability (`POST /api/cli/query`) allows SELECT-only SQL queries against Supabase tables (`security_history_latest`, `symbols`, `security_master`, `macro_factors`; `security_history` is frozen at 2026-04-14 — do not query; `ticker_metadata` is frozen at 2026-01-21 — do not query). Use it as a fallback when you need to explore raw data that isn't exposed through a dedicated endpoint — e.g., checking available date ranges, confirming column names, or sampling rows before building a client.

```python
resp = requests.post(
    "https://riskmodels.app/api/cli/query",
    headers={"Authorization": f"Bearer {api_key}"},
    json={"sql": "SELECT s.ticker, l.teo, l.l3_mkt_er, l.l3_res_er FROM security_history_latest l JOIN symbols s USING (symbol) WHERE s.ticker = 'AAPL' AND l.periodicity = 'daily'"}
)
```

Cost: $0.003/request. Rate-limited to 60/min. SELECT only — no writes.

### 4. Human / portal

- **Auth and keys:** [AUTHENTICATION_GUIDE.md](../../AUTHENTICATION_GUIDE.md), [riskmodels.app/get-key](https://riskmodels.app/get-key). Agents cannot mint keys without user login; document env vars (`RISKMODELS_API_KEY`, `RISKMODELS_BASE_URL`).

## After discovery

- Implement against the **discovered** path and body (e.g. `title` not `name` on `POST /portfolio/risk-snapshot`).
- Update **OpenAPI + MCP data** when the server contract changes (see `.agents/skills/repo-sync/` and maintainer rules).
- Add or extend tests (`tests/*.test.ts`, `sdk/tests/`) for new client surfaces.

## Cursor: Nightly channel

To reduce stale-tool issues when MCP registers many tools or updates often, use Cursor **Settings → Beta → Update channel → Nightly**. This is a **local user setting**; document it for the team but do not assume it is on in every session.

## Related docs in this repo

- [mcp/README.md](../../mcp/README.md) — MCP tool list and design.
- [docs/portfolio-risk-snapshot-runbook.md](../../docs/portfolio-risk-snapshot-runbook.md) — example discovery → minimal PDF client.
- [SKILL.md](../../SKILL.md) (repo root) — research assistant + graphing; defers to this skill for contract discovery.
