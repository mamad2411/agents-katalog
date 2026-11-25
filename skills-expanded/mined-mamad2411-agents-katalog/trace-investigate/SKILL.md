---
name: trace-investigate
description: Investigate a Honeycomb trace by trace.id — surface the offending span, its dependency chain, error context, and a candidate root-cause hypothesis.
---

# trace-investigate

> Given a trace ID, build the chain that explains the failure: which span errored, which span is the *cause* (not just the surface), and what bb.attributes characterize the failure.

> **MCP binding (read before any tool call):** resolve which server backs `honeycomb` from `${POLYMATH_PLUGIN_DATA:-$HOME/.polymath/data}/polymath-core/project-context.json` `mcpResolution.honeycomb` — when `source` is `host`, the CURRENT host agent's own `honeycomb` MCP server is ALREADY registered: use its tools (`toolPrefix` gives the naming) and do NOT register or start a polymath copy. A server registered in a DIFFERENT agent is never a substitute. When `source` is `plugin`, the plugin-shipped `.mcp.json` server backs this skill. When `none`, credentials are unconfigured: ask the user to configure them or degrade gracefully. See the `polymath-core:mcp-bridge` skill.

## When to use

- A log-search surfaced a recurring `trace.id` and you want the full trace context.
- An incident timeline points at a single request that failed; the trace is the proof.
- A latency regression is suspected and you want to see where the time went span-by-span.

## Inputs

- Trace ID (required) — 32-hex W3C trace ID.
- Dataset (optional) — fall back to `userConfig.honeycombDataset`.

## Procedure

1. **Fetch the trace.** Use the honeycomb MCP to run a query with `BREAKDOWN trace.span_id` filtered to `trace.id = <id>` over the relevant time window. Cap at 1000 spans (rare traces exceed this; if so, surface the cap and break by parent).
2. **Build the tree.** Sort spans by start time; resolve each span's parent via `trace.parent_id`. Identify the root span (no parent).
3. **Find the offending span.** Mark every span with `status_code != OK` or with `error = true`. The *first* error span in causal order is usually the cause; later errors may be propagated. Note: "first" is by ancestor walk, not by timestamp.
4. **Walk the dependency chain.** From the offending span, climb to the root: each parent shows the call site that invoked the failing span.
5. **Surface attributes.** For the offending span: `service.name`, `db.system`, `http.url`, `http.response.status_code`, `messaging.destination`, `error.type`, `error.message`, custom `bb.*` attributes the service set.
6. **Latency breakdown.** Group span self-time (`duration_ms` minus child time) by `service.name`. The dominant bucket points at where time went.
7. **Hypothesize root cause.** Use the offending span's attributes + chain + latency to suggest one of:
   - **upstream-timeout** — `error.type` indicates timeout; parent chain shows a long-running peer.
   - **database-error** — span has `db.system` + non-zero error; check the surrounding SQL.
   - **internal-bug** — span error in own service, no infra signal.
   - **rate-limit-or-circuit-breaker** — `error.type` includes `RateLimited`, `CircuitOpen`, etc.
   - **needs-more-data** — error message is opaque; surface a follow-up query suggestion.

## Output

```text
trace-investigate

Trace:       7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d  (dataset: refund-api)
Spans:       42 (within 1000 cap)
Span tree (collapsed)
  root: POST /refund/issue                                   [120ms]
    └─ refund-api: validate                                   [12ms]
    └─ refund-api: persist                                    [40ms]
         └─ refund-db: INSERT INTO refunds                    [38ms]
    └─ refund-api: queue                                      [60ms]
         └─ refund-worker: handle                             ⚠ ERROR
              └─ refund-worker: payments.charge.refund       ⚠ ERROR
                    └─ stripe-client: HTTP POST              ⚠ TIMEOUT (5s)

Offending span:
  service.name           = stripe-client
  http.url               = https://api.stripe.com/v1/refunds
  http.response.status   = (no response)
  error.type             = ConnectTimeoutError
  error.message          = "timeout=5000ms"
  duration_ms            = 5012

Self-time by service:
  stripe-client          5,012 ms (95%)   ← dominant
  refund-worker          120 ms
  refund-api             60 ms
  refund-db              38 ms

Hypothesis: upstream-timeout (Stripe API).
  Next: use the official Stripe MCP / dashboard to triage the
        affected charge IDs, and check Stripe status page for a
        platform-wide event during the trace window.
```

## Quality bar

- Span tree shown, not flat list. The shape is the diagnosis.
- "Offending span" identified by ancestor walk, not by timestamp.
- Latency breakdown by self-time, not total time (parent total is always 100%).
- Hypothesis cites the specific attribute / chain element that supports it.

## Anti-patterns to avoid

- Treating the *last* error span as the cause. Usually it's the *first* error in the chain — later errors are propagated.
- Showing total time per service. The root span's total is always 100%; self-time is the signal.
- Hypothesizing without citing evidence. "Looks like a Stripe issue" without naming the timeout span is unfalsifiable.
- Pulling the full 1000 spans into chat. Collapsed tree + offending-span detail is the right summary.

