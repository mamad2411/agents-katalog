---
name: observability
description: Monitor and debug web, Node.js, and Python applications using OpenTelemetry, console logs, network requests, outbound (egress) HTTP capture, distributed tracing, and reading recorded traces back from the IronBee platform. Use when the user asks about distributed tracing, correlating frontend/backend requests, inspecting the spans a trace recorded, seeing which downstream services a backend process calls, OpenTelemetry, Jaeger, or monitoring application behavior.
allowed-tools: Bash(ironbee-browser-devtools-cli:*), Bash(ironbee-node-devtools-cli:*), Bash(ironbee-python-devtools-cli:*), Bash(ironbee-backend-devtools-cli:*)
---

# Observability Skill

Monitor and debug web, Node.js, and Python applications using OpenTelemetry, console logs, network requests, outbound (egress) HTTP capture, and distributed tracing.

## When to Use

This skill activates when:
- User asks about distributed tracing
- User wants to correlate frontend and backend requests
- User mentions OpenTelemetry, Jaeger, Zipkin, or tracing
- User needs to debug request flow across services
- User wants to see which downstream services a Node.js/Python process calls (egress)
- User wants to monitor application behavior

## Capabilities

### Distributed Tracing
```bash
# Pin / inspect the session trace context
ironbee-browser-devtools-cli o11y get-trace-context
ironbee-browser-devtools-cli o11y new-trace-id
ironbee-browser-devtools-cli o11y set-trace-context --trace-id "abc123def456..."

# Read the spans back from the IronBee platform
ironbee-browser-devtools-cli --json o11y get-trace --wait-ms 10000
ironbee-browser-devtools-cli --json o11y get-session-traces --status error
```

### Console Monitoring
```bash
ironbee-browser-devtools-cli o11y get-console-messages
ironbee-browser-devtools-cli --json o11y get-console-messages --type warning
ironbee-browser-devtools-cli --json o11y get-console-messages --search "error"
```

### Network Observability
```bash
ironbee-browser-devtools-cli --json o11y get-http-requests
ironbee-browser-devtools-cli --json o11y get-http-requests --resource-type fetch
ironbee-browser-devtools-cli --json o11y get-http-requests --status '{"min":400}'
```

### Performance Metrics
```bash
ironbee-browser-devtools-cli --json o11y get-web-vitals
ironbee-browser-devtools-cli --json o11y get-web-vitals --wait-ms 3000
ironbee-browser-devtools-cli --json o11y get-web-vitals --include-debug
```

## OpenTelemetry Integration

### Trace Context
Browser DevTools MCP can inject and extract W3C Trace Context headers:
- `traceparent`: Contains trace-id, span-id, and trace flags
- `tracestate`: Vendor-specific trace information

### Correlation Flow
```
Browser Session
    │
    ├─► trace-id: abc123
    │
    ▼
Frontend Request
    │
    ├─► Header: traceparent: 00-abc123-def456-01
    │
    ▼
Backend Service
    │
    ├─► Logs with trace-id: abc123
    │
    ▼
Observability Platform
    │
    └─► Full trace visualization
```

### Backend Observability (ironbee-node-devtools-cli)

When correlating frontend traces with backend behavior, use `ironbee-node-devtools-cli` to inspect Node.js processes:

```bash
# Connect to backend
ironbee-node-devtools-cli --session-id backend debug connect --pid 12345

# Get console logs from Node process (can correlate with trace ID in logs)
ironbee-node-devtools-cli --session-id backend --json debug get-logs
ironbee-node-devtools-cli --session-id backend --json debug get-logs --search "trace"

# Optional: set tracepoints on backend handlers to capture call context
ironbee-node-devtools-cli --session-id backend debug put-tracepoint \
  --url-pattern "routes/api.ts" \
  --line-number 25
```

### Egress Capture and Trace Injection (node / python)

The node and python CLIs capture the **outbound** HTTP requests the connected process makes (its egress) via an in-process agent — no proxy, no CA — and inject the session-pinned trace id as `traceparent` on every hooked outbound request. Capture is forward-looking (first call installs the agent) and requires `debug connect` first.

```bash
# Node.js process egress
ironbee-node-devtools-cli --session-id backend debug connect --process-name "server.js"
ironbee-node-devtools-cli --session-id backend --json o11y new-trace-id          # pin + inject on egress
ironbee-node-devtools-cli --session-id backend --json o11y get-http-requests     # start capture
# ... trigger the flow ...
ironbee-node-devtools-cli --session-id backend --json o11y get-http-requests --url-pattern "*/api/*" --include-headers

# Python process egress (same surface; requires debugpy in the target)
ironbee-python-devtools-cli --session-id pyapp debug connect --host 127.0.0.1 --debugpy-port 5678
ironbee-python-devtools-cli --session-id pyapp --json o11y new-trace-id
ironbee-python-devtools-cli --session-id pyapp --json o11y get-http-requests
```

This closes the loop end-to-end: pin one trace id in the browser session (frontend → backend requests) AND in the backend process (backend → downstream egress), then search your observability platform by that id.

### Reading traces back (`o11y get-trace` / `get-session-traces`)

Instead of leaving the CLI to search a UI, read the spans back from the IronBee platform. Both tools exist on **all six** platform CLIs (terminal included — they query the platform API, not the platform session) and need a credential: `SERVICE_OAUTH_TOKEN` (personal access token) or `SERVICE_API_KEY` (shared account key).

```bash
# Pin, drive the app, then read every span recorded under that trace
ironbee-browser-devtools-cli --session-id trace-session --json o11y new-trace-id
ironbee-browser-devtools-cli --session-id trace-session navigation go-to --url "https://app.example.com/checkout"
ironbee-browser-devtools-cli --session-id trace-session --json o11y get-trace --wait-ms 10000

# Narrow to what failed, with span attributes
ironbee-browser-devtools-cli --json o11y get-trace --status error --detail attributes

# Slow spans of one service only
ironbee-backend-devtools-cli --json o11y get-trace --service-name payments --min-duration-ms 250

# Everything recorded under one IronBee session (the id is implicit only when an
# orchestrator injects _metadata; pass it explicitly from a plain CLI)
ironbee-backend-devtools-cli --json o11y get-session-traces --session-id 8a1f…
```

`get-trace` defaults to the trace the call is already correlated to, then to the session pin, so the usual call takes no arguments. Spans are ingested asynchronously — use `--wait-ms` right after an action instead of retrying by hand. Results are a **flat**, start-time-ordered page: rebuild the waterfall from `parentSpanId`, page with `--limit` / the returned `nextOffset`, and read `services[]` / `errorCount` for the summary.

## Debugging Workflow

```bash
SESSION="--session-id trace-session"

# 1. Generate new trace ID
ironbee-browser-devtools-cli $SESSION o11y new-trace-id

# 2. Navigate (requests will carry trace ID)
ironbee-browser-devtools-cli $SESSION navigation go-to --url "https://app.example.com"
ironbee-browser-devtools-cli $SESSION sync wait-for-network-idle

# 3. Perform actions
ironbee-browser-devtools-cli $SESSION interaction click --selector "#submit"
ironbee-browser-devtools-cli $SESSION sync wait-for-network-idle

# 4. Get trace ID for backend correlation
ironbee-browser-devtools-cli $SESSION o11y get-trace-context

# 5. Check console errors
ironbee-browser-devtools-cli $SESSION --json o11y get-console-messages --type error

# 6. Check network requests
ironbee-browser-devtools-cli $SESSION --json o11y get-http-requests

# 7. Cleanup
ironbee-browser-devtools-cli session delete trace-session
```

## Use Existing Trace ID

```bash
SESSION="--session-id trace-session"

# Set trace ID from backend
ironbee-browser-devtools-cli $SESSION o11y set-trace-context --trace-id "abc123def456789..."

# Navigate (requests will use this trace ID)
ironbee-browser-devtools-cli $SESSION navigation go-to --url "https://app.example.com"

# All subsequent requests carry the trace ID
ironbee-browser-devtools-cli $SESSION interaction click --selector "#api-call"
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OTEL_ENABLE` | Enable OpenTelemetry | `false` |
| `OTEL_SERVICE_NAME` | Service identifier | `frontend` |
| `OTEL_EXPORTER_TYPE` | Export destination | `none` |
| `OTEL_EXPORTER_HTTP_URL` | Collector endpoint | - |
| `OTEL_EXPORTER_HTTP_HEADERS` | Auth headers | - |

### Exporter Types

| Type | Description |
|------|-------------|
| `none` | Disabled |
| `console` | Log to console |
| `otlp/http` | Send to OTLP collector |

## Common Platforms

### Jaeger
```bash
OTEL_EXPORTER_HTTP_URL=http://localhost:4318
```

### Grafana Tempo
```bash
OTEL_EXPORTER_HTTP_URL=http://tempo:4318
```

### Honeycomb
```bash
OTEL_EXPORTER_HTTP_URL=https://api.honeycomb.io
OTEL_EXPORTER_HTTP_HEADERS=x-honeycomb-team=YOUR_API_KEY
```

### Datadog
```bash
OTEL_EXPORTER_HTTP_URL=http://localhost:4318
```

## Best Practices

1. **Generate new trace IDs** for each test scenario
2. **Document trace IDs** in bug reports
3. **Check console first** for JavaScript errors
4. **Filter network requests** to relevant endpoints
5. **Correlate timestamps** between frontend and backend
6. **Use structured logging** with trace context
7. **Set up OTEL exporter** for full trace visibility
