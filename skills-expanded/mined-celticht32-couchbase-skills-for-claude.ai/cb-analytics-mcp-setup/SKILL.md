---
name: cb-analytics-mcp-setup
description: |
  Use this skill when the user is setting up cb-analytics-mcp from scratch
  or troubleshooting an existing install — generating secrets, configuring
  .env, running --check, picking single- vs multi-cluster mode, tuning
  rate limits, configuring audit rotation, or using the CLI. Trigger when
  the user mentions "install", "configure", "first run", "MCP_API_KEY",
  "GUI_PASSWORD", "clusters.json", "cb-analytics-mcp --check",
  "MAX_QUERY_ROWS", "RATE_LIMIT_", "AUDIT_ROTATE", "tools call", or
  "tools list".
license: MIT
---

# cb-analytics-mcp setup

You're helping the user bring up or tune a cb-analytics-mcp installation.
This skill covers configuration, validation, and the operator CLI.

## Required env vars (server refuses to start without these)

- `MCP_API_KEY` — bearer token for Claude. **Min 32 chars.**
  Generate: `python -c "import secrets; print(secrets.token_urlsafe(48))"`
- At least one of:
  - **Single cluster**: `CB_ANALYTICS_HOST` and `CB_ANALYTICS_PASSWORD`
  - **Multi cluster**: `CB_ANALYTICS_CLUSTERS_FILE` pointing at a JSON array
- If GUI is enabled (default): `GUI_SESSION_SECRET` (≥32 chars) and a
  non-default `GUI_PASSWORD`.

## Validation flow

Always recommend `cb-analytics-mcp --check` before `make run`. It returns:

- exit 0 + a `config_valid` log line on success
- exit 2 + a list of human-readable errors on failure

`--check` doesn't try to reach the cluster. To verify network reachability
too, use the **dashboard's Test Connection button** after starting the
server (or `cb-analytics-mcp tools call ping_cluster --offline`, see CLI
section below).

## Single vs multi-cluster decision

- **One Couchbase cluster.** Use env vars only. Simpler.
- **More than one cluster** (prod, stage, dev), or **one cluster with
  separate credentials per tenant.** Use `CB_ANALYTICS_CLUSTERS_FILE`.
  The file is a JSON array; each entry has `name`, `host`, `username`,
  `password`, and optional `tls`, `mgmt_port`, `analytics_port`,
  `verify_ssl`, `timeout_seconds`, `max_retries`. See
  `config/clusters.example.json`.

## Tunable safety limits (sensible defaults; tune only if needed)

| Env var | Default | What it controls |
|---|---|---|
| `MAX_QUERY_ROWS` | `1000` | Soft cap on `execute_query` / `execute_query_readonly`. Responses include `truncated: true` and `full_row_count` when the cap kicks in. `0` disables. |
| `RATE_LIMIT_QUERY_PER_SEC` | `10` | Token-bucket rate for all query tools (per API key). |
| `RATE_LIMIT_READ_PER_SEC` | `60` | Token-bucket rate for read-only tools (list/get/ping/…). |
| `RATE_LIMIT_WRITE_PER_SEC` | `1` | Token-bucket rate for mutating tools (upsert/delete user, links, restart, capella mutations, …). Intentionally conservative. |
| `AUDIT_ROTATE_BYTES` | `10485760` (10 MB) | Rotate audit log when it exceeds this. `0` disables rotation. |
| `AUDIT_ROTATE_KEEP` | `5` | How many rotated generations to keep (`audit.log.1`…`.5`). |

These defaults are deliberate. Before raising any limit, ask: "is the
right answer actually a different architecture (caching layer, batched
query, smarter pagination), not a higher rate limit?" Raising the write
limit in particular is rarely the answer — a misbehaving client can
easily cause real harm at 10 writes/sec.

When a rate limit fires, the tool response is:

```json
{ "ok": false, "error": "RateLimitExceeded",
  "message": "Rate limit exceeded for category 'write' (limit 1/sec). Retry in 0.83s.",
  "category": "write", "rate_per_sec": 1, "retry_after_sec": 0.83 }
```

This is by design — the rate limits ARE the recommended behavior. They
are also recorded in the audit log as `success: false` so you can spot
abusive clients.

## The operator CLI (`cb-analytics-mcp tools …`)

For testing config or scripting workflows without going through Claude:

```bash
# Enumerate every registered tool
cb-analytics-mcp tools list

# Filter by rate-limit category
cb-analytics-mcp tools list --category write

# Offline mode: instantiates the pool in-process. No running server needed.
# Uses the same env config the server would.
cb-analytics-mcp tools call list_dataverses --offline

# Pass args. Values are JSON-parsed when possible, otherwise treated as
# strings. Nested JSON works:
cb-analytics-mcp tools call execute_query_readonly \
    --arg statement='SELECT * FROM Default.Books LIMIT 5' \
    --arg cluster=prod \
    --offline

# Against a running server (uses MCP_API_KEY as bearer):
cb-analytics-mcp tools call list_users \
    --remote http://localhost:8000/mcp
```

Both modes pretty-print the JSON result and exit non-zero on tool-level
errors, so the CLI works in shell pipelines. Use it for:

- Smoke-testing config after editing `.env`
- Verifying a specific cluster is reachable (`tools call ping_cluster
  --arg cluster=NAME --offline`)
- Pre-flighting a query before wiring it into automation
- Debugging in CI

## Common gotchas

- `MCP_API_KEY` under 32 chars → ValueError at startup. Pad it.
- `GUI_PASSWORD=changeme` is rejected in strict mode (`--check` flags it).
- TLS to Couchbase: set `CB_ANALYTICS_TLS=true` **and** the correct
  TLS-port numbers (`18091`/`18095` are common).
- Capella tools require **both** `CB_CAPELLA_API_KEY_SECRET` and a
  working outbound HTTPS path to `cloudapi.cloud.couchbase.com`.
- The audit log writer creates its parent directory on first record. If
  the path is on a read-only mount, set `AUDIT_LOG_ENABLED=false` or pick
  a writable location.
- Audit rotation creates `audit.log.1`, `audit.log.2`, etc. alongside
  the active file. If your `AUDIT_LOG_FILE` is in a directory you only
  intend for the live log, the backups will end up there too. Pick a
  dedicated directory.
- Setting `MAX_QUERY_ROWS=0` to "see everything" is rarely the right call.
  The cap exists to keep wire payloads sane. If you need the full result,
  use `execute_query_paginated` instead.
- The GUI's WebSocket log streamer reads from `LOG_FILE`. If you haven't
  set `LOG_FILE`, the `/logs` page falls back to a note explaining that
  there's nothing to tail.

## What to do after a successful --check

1. `make run` to start both servers.
2. Browse to `http://localhost:8080` to confirm the GUI.
3. Click **Test** on each cluster row in the dashboard to confirm
   reachability end-to-end (or use the CLI: `cb-analytics-mcp tools call
   ping_cluster --offline`).
4. From the GUI, run `SELECT 1` in the query editor to round-trip the
   full request path.
5. Point Claude at `http://<host>:8000/mcp` with the bearer token from
   step 1 (see `connecting-claude-ai.md` in the project docs).
6. Visit `/admin` and confirm the audit log is recording your test calls.
   Use the date / tool / failures filters to verify they work.

## Troubleshooting decision tree

- **Server won't start** → run `--check`. Address every reported error.
- **Server starts but cluster shows "Unreachable"** → click Test on the
  cluster row; the inline message tells you whether it's DNS, port, TLS,
  or credentials.
- **Tools return `AnalyticsAuthError`** → credentials wrong, role missing,
  or wrong cluster. Cross-check with `tools call who_am_i --offline`.
- **Tools return `RateLimitExceeded`** → expected behavior, not a bug.
  Check the audit log to identify the noisy client; consider raising
  `RATE_LIMIT_*_PER_SEC` if the traffic is legitimate.
- **Audit log file grows without bound** → confirm `AUDIT_ROTATE_BYTES`
  is non-zero. The default 10 MB cap should keep ~50 MB on disk.
- **WebSocket `/logs/ws` errors out** → almost always a reverse-proxy not
  upgrading; the page auto-falls back to HTMX polling, which still works.

## Related skills

- `cb-analytics-security` — creating the Couchbase service account the MCP server uses to authenticate
- `cb-analytics-cluster` — `ping_cluster` and `who_am_i` to verify connectivity after setup
