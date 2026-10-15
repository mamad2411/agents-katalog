---
name: kibana-esql
description: >
  Runs ES|QL queries against Elastic Cloud / Kibana by reusing the user's
  authenticated browser session via the claude-in-chrome MCP, without
  requiring an API key. Use when the user mentions Kibana, ES|QL,
  Elasticsearch, Elastic Cloud, asks to query logs or indices, or wants
  to explore data in their cluster and only has SSO access.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

# Kibana ES|QL (browser-session proxy)

## When to Use

- User wants to run ES|QL queries and only has SSO access to Kibana (no API key permissions)
- User has Kibana open in Chrome with an active SSO session
- User asks questions that require querying indices, logs, or data in their Elastic Cloud cluster
- User references an Elastic Cloud hostname (`*.found.io`, `*.cloud.es.io`, `*.kb.<region>.aws.elastic-cloud.com`)

Do NOT use this skill when:

- User has an API key available — use the Elastic MCP (`@elastic/mcp-server-elasticsearch`) instead
- User is on self-hosted Elasticsearch reachable over the network — use direct HTTP + basic auth
- User wants dashboard/visualization authoring — use `kibana-dashboards`, `kibana-vega`

## Critical Patterns

### The endpoint and the headers that matter

```
POST /internal/search/esql_async

Headers:
  Content-Type: application/json
  kbn-xsrf: true
  Elastic-Api-Version: 1
  x-elastic-internal-origin: Kibana      ← REQUIRED. Without it: 400.

Credentials: include
Body: { "params": { "query": "<ES|QL>" } }
```

`x-elastic-internal-origin: Kibana` is the gate for `/internal/*` endpoints in Kibana 8.11+. If missing, Kibana returns 400 `"uri ... exists but is not available with the current configuration"` — misleading, but it IS a header problem, not a permissions problem.

### Response shape

Small/fast queries complete inline:

```json
{
  "rawResponse": {
    "columns": [{"name": "greeting", "type": "keyword"}, {"name": "n", "type": "integer"}],
    "values": [["hello", 42]],
    "took": 15,
    "is_running": false,
    "is_partial": false
  },
  "isRunning": false,
  "warning": "299 Elasticsearch ... \"No limit defined, adding default limit of [1000]\""
}
```

Slow queries return `{ id, isRunning: true }` and must be polled at `POST /internal/search/ese/<id>` with the same four headers until `isRunning: false`.

### Transport rule

NEVER extract session cookies into the conversation context. Keep every API call inside the browser tab via `mcp__claude-in-chrome__javascript_tool`. The cookie is `HttpOnly` anyway — cookies stay in the Chrome process, the agent receives only JSON results.

## Workflow

1. **Find or create the tab**
   - Call `mcp__claude-in-chrome__tabs_context_mcp` (with `createIfEmpty: true` if no group exists)
   - Look for a tab whose URL is on the user's Kibana host
   - If none, navigate an existing tab to the Kibana root

2. **Verify authentication**
   - Evaluate `window.location.pathname` via `javascript_tool`
   - If it starts with `/app/` (e.g. `/app/discover`) → authenticated, proceed
   - If it contains `/login` or redirects to `amazon.com` / `identitycenter` → ask user to complete SSO in that window and wait for confirmation

3. **Run the query**
   - Use `assets/run-esql.js` pattern: single `fetch` with the four headers
   - Pass the ES|QL string as `params.query`
   - Read `rawResponse.columns` and `rawResponse.values` for the result

4. **Handle async**
   - If `isRunning: true` in the first response, extract `id` and use `assets/poll-async.js`
   - Poll with backoff (start 250ms, cap 2s) until `isRunning: false`
   - Always `DELETE /internal/search/<id>` when done to release cluster resources

5. **Render for the user**
   - Small results (<20 rows, <8 cols) → markdown table
   - Larger → summary stats + first/last 5 rows + a one-line description of what each column contains based on types
   - Always echo the ES|QL query you ran so the user can reproduce it
   - Mention `took` ms and warnings (default LIMIT 1000 is the common one)

## Code Examples

Minimum viable query (sync path):

```javascript
const r = await fetch('/internal/search/esql_async', {
  method: 'POST',
  credentials: 'include',
  headers: {
    'Content-Type': 'application/json',
    'kbn-xsrf': 'true',
    'Elastic-Api-Version': '1',
    'x-elastic-internal-origin': 'Kibana'
  },
  body: JSON.stringify({ params: { query: 'FROM logs-* | LIMIT 5' } })
});
const j = await r.json();
// j.rawResponse.columns, j.rawResponse.values, j.rawResponse.took
```

Full self-contained snippet lives in `assets/run-esql.js` and handles both sync and async completions. For polling-only, see `assets/poll-async.js`.

## Common Errors

| HTTP | Body contains | Cause | Fix |
|------|---------------|-------|-----|
| 400  | `not available with the current configuration` | Missing `x-elastic-internal-origin: Kibana` | Add the header |
| 400  | `Please specify a version via Elastic-Api-Version header` | Missing version header | Add `Elastic-Api-Version: 1` |
| 401  | `security_exception` or redirect to login | Session expired | Ask user to re-login via SSO in the tab |
| 403  | `security_exception` with index name | User's role lacks read on that index | Try a different index or `FROM <other-index>` |
| 404  | `Not Found` on `/internal/search/esql_async` | Kibana version < 8.11 — endpoint did not exist | Fall back to `/api/console/proxy?path=_query&method=POST` if console is enabled, otherwise unsupported |
| 400  | `parsing_exception` with line/col | ES|QL syntax error | Show the parser message to the user — it's precise |

Deep debugging: see `references/troubleshooting.md`.

## Discovering Endpoints in an Unknown Cluster

If endpoints in this skill stop working (Kibana upgrade, different cluster topology), use the **interceptor discovery** approach rather than guessing:

1. Inject `assets/install-interceptor.js` via `javascript_tool`
2. Ask the user to run one real ES|QL query in Discover
3. Read `window.__cap` to see the exact URL, method, and body Kibana used
4. Update this skill with the new endpoint

This is faster and more reliable than reading Kibana source or trying documented endpoints.

## Resources

- **Snippets**: See [assets/](assets/) for ready-to-inject JavaScript
  - `run-esql.js` — run one ES|QL query, handles sync + async
  - `poll-async.js` — poll an async search id until complete
  - `probe-auth.js` — check whether the tab has a live Kibana session
  - `install-interceptor.js` — capture Kibana's internal API calls for endpoint discovery
  - `list-indices.js` — enumerate available indices via autocomplete
- **Endpoint details**: See [references/endpoints.md](references/endpoints.md) for full request/response shapes
- **Session setup**: See [references/session-setup.md](references/session-setup.md) for the tab/login flow
- **Troubleshooting**: See [references/troubleshooting.md](references/troubleshooting.md) for edge cases beyond the table above
