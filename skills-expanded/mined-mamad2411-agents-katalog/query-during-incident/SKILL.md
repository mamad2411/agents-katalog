---
name: query-during-incident
description: Run the right Datadog queries during an incident to narrow cause — error rates, latency percentiles, deploys, recent changes — and surface them concisely.
---

# query-during-incident

> Inside a live incident, run the focused queries that narrow root cause fastest. Output is a short situation summary, not a dashboard.

> **MCP binding (read before any tool call):** resolve which server backs `datadog` from `${POLYMATH_PLUGIN_DATA:-$HOME/.polymath/data}/polymath-core/project-context.json` `mcpResolution.datadog` — when `source` is `host`, the CURRENT host agent's own `datadog` MCP server is ALREADY registered: use its tools (`toolPrefix` gives the naming) and do NOT register or start a polymath copy. A server registered in a DIFFERENT agent is never a substitute. When `source` is `plugin`, the plugin-shipped `.mcp.json` server backs this skill. When `none`, credentials are unconfigured: ask the user to configure them or degrade gracefully. See the `polymath-core:mcp-bridge` skill.

## When to use

- A pager fired; the on-call wants Datadog signals without clicking through 8 dashboards.
- A workflow's incident-response step needs structured telemetry.

## Procedure

1. **Anchor on the alert that fired**. Note the metric, threshold, and exact time.
2. **Run these queries in order** via the MCP, comparing each result against pre-incident baseline (typically 24h ago, same time):
   - **Error rate** for the service: `5xx_rate{service:X}` over the last 30 min vs 24h ago same window.
   - **Latency** percentiles: `p50/p95/p99 latency{service:X}` over the last 30 min vs 24h ago.
   - **Saturation**: CPU / memory / queue depth on the service's pods or hosts.
   - **Upstream/downstream** errors: same `5xx_rate` for the service's main dependencies.
3. **Cross-reference recent changes**: events stream filtered to the last 60 min for `deploy:*`, `config_change:*`, `feature_flag:*`.
4. **Surface ONE finding** that's the highest-likelihood cause. List the second-most-likely so the on-call has a fallback if the first is wrong.
5. **Never speculate** beyond what the queries show. "Errors spiked after 13:50 deploy" is concrete; "the deploy probably broke X" is not.

## Output

```text
Datadog situation: refund-p99-500ms (triggered 14:02 UTC)

Vs 24h baseline:
  refund 5xx rate           14:02–14:10: 2.4%   (24h ago: 0.1%)
  refund p99 latency        14:02–14:10: 880ms  (24h ago: 320ms)
  refund pod CPU            steady ~45% (no signal)
  refund DB pool wait p99   140ms       (24h ago: 12ms)   ← bumped
  stripe-client 5xx rate    0.2%        (24h ago: 0.2%)   (no signal)

Recent change events (last 60 min):
  - 13:50 deploy_succeeded service:refund-service sha:abc123 v0.5.1
  - 13:50 feature_flag_change refund_async_writes=true

Most likely cause:
  Coincident with 13:50 deploy + flag flip. DB pool wait increased >10×;
  the new code path may hold connections longer.

Second-most-likely:
  Stripe-client error rate is flat — downstream looks unaffected. If the
  rollback doesn't help, suspect a slow DB query, not Stripe.
```

## Quality bar

- Every number compared to a stated baseline.
- One "most likely cause" + one fallback. Not a list of 5 maybes.
- Recent change events filtered to a tight window.
- No speculation past what the data shows.

## Anti-patterns to avoid

- Pasting raw query results without a baseline.
- "Could be X, could be Y, could be Z."
- Querying everything in the platform — focus.
- Skipping the events stream; deploys and flag flips usually explain incidents.

