---
name: backend-testing
description: Test backend services end-to-end. Use when the user wants to drive HTTP/gRPC/GraphQL/WebSocket endpoints against a real server, correlate requests with server logs (file/Docker/Kubernetes), verify database side-effects with snapshot/diff or watch-changes, replay captured curl/HAR requests, or seed and roll back fixtures inside a writable transaction.
allowed-tools: Bash(ironbee-backend-devtools-cli:*)
---

# Backend Testing Skill

End-to-end backend verification with the IronBee Backend DevTools CLI. Drive requests, watch logs, and assert on database state — all in one session.

See the full CLI reference at [`ironbee-backend-devtools-cli`](../ironbee-backend-devtools-cli/SKILL.md). Domain-level docs: [request](../ironbee-backend-devtools-cli/references/request.md), [log](../ironbee-backend-devtools-cli/references/log.md), [db](../ironbee-backend-devtools-cli/references/db.md), [o11y](../ironbee-backend-devtools-cli/references/o11y.md).

## When to Use

This skill activates when:
- User wants to test backend APIs over HTTP/1.1, HTTP/2, gRPC, GraphQL, or WebSocket
- User needs to assert on log lines that a request produced (file, Docker, or Kubernetes logs)
- User needs to verify that a request changed exactly the right database rows
- User wants to replay a captured `curl` command or HAR entry
- User needs to seed test fixtures and roll them back automatically
- User wants to correlate a request chain with a single W3C trace id

## Core principle: correlate by trace id

Pin a trace id once on the session and every request automatically carries it. Then read your server logs filtered by that trace id — that's the cleanest agent-driven verification loop.

```bash
SESSION="--session-id e2e"
TRACE=$(ironbee-backend-devtools-cli $SESSION --json o11y new-trace-id | jq -r .traceId)
ironbee-backend-devtools-cli $SESSION request http --url "https://api.example.com/orders" --method POST --body '{"kind":"json","value":{"sku":"ABC"}}'
ironbee-backend-devtools-cli $SESSION --json log read --source app --pattern "$TRACE" --parse-json --select '["timestamp","level","msg","span_id"]'

# Same id, read back as spans from the IronBee platform (needs SERVICE_OAUTH_TOKEN or SERVICE_API_KEY)
ironbee-backend-devtools-cli $SESSION --json o11y get-trace --wait-ms 10000 --status error
```

## Capabilities

### HTTP / GraphQL / gRPC / WebSocket requests
```bash
# HTTP with JSON body
ironbee-backend-devtools-cli --json request http \
  --url "https://api.example.com/orders" \
  --method POST \
  --body '{"kind":"json","value":{"sku":"ABC","qty":2}}'

# GraphQL
ironbee-backend-devtools-cli --json request graphql \
  --url "https://api.example.com/graphql" \
  --query 'mutation($s:String!){createOrder(sku:$s){id}}' \
  --variables '{"s":"ABC"}'

# gRPC unary via .proto file
ironbee-backend-devtools-cli --json request grpc \
  --target "api.example.com:443" \
  --service "orders.v1.OrderService" \
  --method "GetOrder" \
  --proto-source '{"kind":"protoFile","path":"./protos/orders.proto"}' \
  --request '{"orderId":"abc-123"}'

# WebSocket — multi-step (open / send / receive / close)
CONN=$(ironbee-backend-devtools-cli --json request websocket-open --url "wss://api.example.com/stream" | jq -r .connectionId)
ironbee-backend-devtools-cli request websocket-send --connection-id "$CONN" --data '{"kind":"json","value":{"subscribe":"orders"}}'
ironbee-backend-devtools-cli --json request websocket-receive --connection-id "$CONN" --max-count 50 --timeout-ms 5000
ironbee-backend-devtools-cli request websocket-close --connection-id "$CONN"
```

### Session state: cookies, default headers, default gRPC metadata
```bash
# Pin auth on every call to api.example.com for this session
ironbee-backend-devtools-cli request set-default-headers \
  --host "api.example.com" \
  --headers '{"Authorization":"Bearer $TOKEN"}'

# Pin gRPC metadata for a specific target
ironbee-backend-devtools-cli request set-default-metadata \
  --target "api.example.com:443" \
  --metadata '{"x-tenant-id":"acme"}'

# Inspect / clear when needed
ironbee-backend-devtools-cli request list-default-headers
ironbee-backend-devtools-cli request list-cookies
ironbee-backend-devtools-cli request clear-cookies --domain "api.example.com"
```

### Replay captured calls (curl or HAR)
```bash
ironbee-backend-devtools-cli --json request replay \
  --source '{"kind":"curl","value":"curl -X POST https://api.example.com/orders -d ..."}' \
  --overrides '{"headers":{"Authorization":"Bearer NEW"}}' \
  --new-trace-id
```

### Log capture: register → read or follow
```bash
# Point-in-time read with JSON filters
ironbee-backend-devtools-cli log register-source --name app --type file --path /var/log/app.log
ironbee-backend-devtools-cli --json log read --source app --tail 200 \
  --level ERROR --parse-json --json-filter '{"span.kind":"server"}'

# Multi-line stack coalescing
ironbee-backend-devtools-cli --json log read --source app --pattern "TypeError" --coalesce true \
  --context-before 2 --context-after 10

# Live follow during a request (drain after)
FOLLOW=$(ironbee-backend-devtools-cli --json log follow --source app --max-buffer-lines 1000 | jq -r .followId)
ironbee-backend-devtools-cli request http --url "https://api.example.com/orders" --method POST --body '{"kind":"json","value":{}}'
ironbee-backend-devtools-cli --json log get-followed --follow-id "$FOLLOW" --drain --pattern "trace_id="
ironbee-backend-devtools-cli log stop-follow --follow-id "$FOLLOW"

# Read across multiple sources (file + docker), interleaved by timestamp
ironbee-backend-devtools-cli log register-source --name api --type docker --container my-api
ironbee-backend-devtools-cli log register-source --name worker --type kubernetes --pod worker-0 --namespace prod
ironbee-backend-devtools-cli --json log read-multi --sources '["app","api","worker"]' --tail 500 --pattern "$TRACE"
```

### Database verification: snapshot → request → snapshot → diff
```bash
# Prefer connection-string-env so the credential never enters the agent's context
ironbee-backend-devtools-cli db connect --name main --type postgres --connection-string-env DATABASE_URL

BEFORE=$(ironbee-backend-devtools-cli --json db snapshot \
  --connection main --table orders --where "customer_id = $1" --params '["cust-1"]' | jq -r .snapshotId)

ironbee-backend-devtools-cli request http --url "https://api.example.com/orders" --method POST --body '{"kind":"json","value":{"customer_id":"cust-1"}}'

AFTER=$(ironbee-backend-devtools-cli --json db snapshot \
  --connection main --table orders --where "customer_id = $1" --params '["cust-1"]' | jq -r .snapshotId)

ironbee-backend-devtools-cli --json db diff --from "$BEFORE" --to "$AFTER"
```

### Database watch-changes (async writes)
```bash
WATCH=$(ironbee-backend-devtools-cli --json db watch-changes \
  --connection main --table outbox --poll-interval-ms 500 | jq -r .watchId)

ironbee-backend-devtools-cli request http --url "https://api.example.com/orders" --method POST --body '{"kind":"json","value":{}}'

# Pull the latest diffs (each event = one poll cycle's added/removed/changed)
ironbee-backend-devtools-cli --json db get-changes --watch-id "$WATCH" --drain
```

### Writable transactions: fixtures with auto-rollback
```bash
ironbee-backend-devtools-cli db connect --name main --type postgres --connection-string-env TEST_DATABASE_URL --allow-writes

ironbee-backend-devtools-cli db transaction-begin --connection main --writable
ironbee-backend-devtools-cli db seed --connection main --table users \
  --rows '[{"id":"u1","email":"a@example.com"},{"id":"u2","email":"b@example.com"}]'
# ... run requests, take snapshots, assert ...
ironbee-backend-devtools-cli db transaction-rollback --connection main
```

### Readonly probes: list-tables / describe-table / query
```bash
ironbee-backend-devtools-cli --json db list-tables --connection main
ironbee-backend-devtools-cli --json db describe-table --connection main --table orders
ironbee-backend-devtools-cli --json db query --connection main \
  --sql "SELECT id, status FROM orders WHERE customer_id = \$1" --params '["cust-1"]'
```

## Canonical flows

### A. Log-correlated request → assertion

```bash
SESSION="--session-id flow-a"

# Pin trace id, register log source, start follower
TRACE=$(ironbee-backend-devtools-cli $SESSION --json o11y new-trace-id | jq -r .traceId)
ironbee-backend-devtools-cli $SESSION log register-source --name app --type file --path /var/log/app.log
FOLLOW=$(ironbee-backend-devtools-cli $SESSION --json log follow --source app --max-buffer-lines 2000 | jq -r .followId)

# Trigger the operation
ironbee-backend-devtools-cli $SESSION request http \
  --url "https://api.example.com/orders" --method POST \
  --body '{"kind":"json","value":{"sku":"ABC"}}'

# Drain just the lines tagged with our trace id
ironbee-backend-devtools-cli $SESSION --json log get-followed \
  --follow-id "$FOLLOW" --drain --pattern "$TRACE" \
  --parse-json --select '["timestamp","level","msg","error"]'

ironbee-backend-devtools-cli $SESSION log stop-follow --follow-id "$FOLLOW"
```

### B. Database-correlated request → diff

```bash
SESSION="--session-id flow-b"

ironbee-backend-devtools-cli $SESSION db connect --name main --type postgres --connection-string-env DATABASE_URL

BEFORE=$(ironbee-backend-devtools-cli $SESSION --json db snapshot --connection main --table orders | jq -r .snapshotId)

ironbee-backend-devtools-cli $SESSION request http \
  --url "https://api.example.com/orders" --method POST \
  --body '{"kind":"json","value":{"sku":"ABC"}}'

AFTER=$(ironbee-backend-devtools-cli $SESSION --json db snapshot --connection main --table orders | jq -r .snapshotId)

ironbee-backend-devtools-cli $SESSION --json db diff --from "$BEFORE" --to "$AFTER"
```

### C. Sandboxed fixture write inside a transaction

```bash
SESSION="--session-id flow-c"

ironbee-backend-devtools-cli $SESSION db connect --name test --type postgres \
  --connection-string-env TEST_DATABASE_URL --allow-writes

ironbee-backend-devtools-cli $SESSION db transaction-begin --connection test --writable
ironbee-backend-devtools-cli $SESSION db seed --connection test --table customers \
  --rows '[{"id":"cust-1","email":"a@example.com"}]'

# ... run requests / verifications that depend on the seeded row ...

# Always rollback unless you explicitly want to keep the rows
ironbee-backend-devtools-cli $SESSION db transaction-rollback --connection test
```

## Best Practices

1. **Pin a trace id at the start of a flow** — `o11y new-trace-id` once, then correlate logs / spans / db audit rows by it.
2. **Treat 4xx / 5xx and non-OK gRPC as data, not errors.** Only transport-level failures (DNS, TLS, timeout, abort, blocked) populate the `error` field. A `BLOCKED` code means the target is outside `BACKEND_ALLOWED_DOMAINS` — that decision is permanent (no retries), and loopback is not implicitly allowed, so list `localhost` when testing locally.
3. **Prefer `--connection-string-env`** over inline credentials — the value stays in `process.env` and never enters the agent's context.
4. **Default to readonly db access.** Open with `--allow-writes` only when you need fixtures, and always wrap writes in a transaction you roll back.
5. **Use the cookie jar for login flows.** It's on by default — set credentials once and every subsequent request inherits the session.
6. **Pin host-scoped default headers** (`request set-default-headers`) for auth tokens instead of passing `--headers` on every call.
7. **Set up log followers BEFORE the request** so the buffer captures lines emitted during the call. `log get-followed` and `db get-changes` drain by default; passing `--drain` is a no-op but harmless. To peek without clearing, call via MCP / `run execute` with `drain: false`.
8. **Snapshot just the affected rows** with a tight `--where` clause — full-table snapshots are slow and noisy in the diff.
9. **Compose flows in a scenario** when you'll reuse them — see [scenario reference](../ironbee-backend-devtools-cli/references/scenario.md). Scenarios are platform-agnostic and work on the backend CLI too. Prefer the step-based form (`--body`) with `setup` / `teardown` sections so fixtures come up and come down with the run, and let an `llm-action` step carry the part that still needs judgement.
10. **SQLite needs no driver** — it runs on Node's built-in `node:sqlite` (Node >= 22.16.0). Only Postgres (`pg`) and MySQL (`mysql2`) need an install.
