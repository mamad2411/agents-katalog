---
name: author-monitor
description: Author a Datadog monitor — query, threshold, evaluation window, no-data behavior, notification routing; pair with polymath-sre:slo-design for SLO burn-rate monitors.
---

# author-monitor

> Write one Datadog monitor and create it via the MCP server. Output is the monitor JSON + the rationale.

> **MCP binding (read before any tool call):** resolve which server backs `datadog` from `${POLYMATH_PLUGIN_DATA:-$HOME/.polymath/data}/polymath-core/project-context.json` `mcpResolution.datadog` — when `source` is `host`, the CURRENT host agent's own `datadog` MCP server is ALREADY registered: use its tools (`toolPrefix` gives the naming) and do NOT register or start a polymath copy. A server registered in a DIFFERENT agent is never a substitute. When `source` is `plugin`, the plugin-shipped `.mcp.json` server backs this skill. When `none`, credentials are unconfigured: ask the user to configure them or degrade gracefully. See the `polymath-core:mcp-bridge` skill.

## When to use

- A new service needs alerting before going live.
- An existing alert is too noisy or too quiet; we want to tune it.

## Inputs

- The metric or log query.
- The SLO target (if pair with `polymath-sre:slo-design`).
- The destination (Slack channel, PagerDuty service, email list).

## Procedure

1. **Decide the monitor type**:
   - **metric alert** — Prometheus/Datadog metric exceeds a threshold.
   - **anomaly** — significant deviation from history. Use only when threshold-based is genuinely impossible.
   - **log alert** — count of matching log lines.
   - **service check** — uptime / synthetic.
   - **composite** — `(monitorA && monitorB) || monitorC`.
2. **Query** — write the metric or log query. Validate it in Datadog's UI before automating; the MCP creates monitors but it doesn't validate semantics.
3. **Threshold** — derive from the SLO or from a documented baseline. **Never** "pick a round number that looks right".
4. **Evaluation window** — match the response expectation:
   - Page (sev2): 5-15 min window with a short critical threshold.
   - Ticket: 6h+ window.
5. **No-data behavior** — explicit. For revenue-impacting paths: `notify_no_data: true`, `no_data_timeframe: 10`. For things that legitimately go quiet (low traffic at night): `notify_no_data: false` with a comment explaining why.
6. **Notification message** — Markdown, with sections: what's broken, why it matters, link to runbook, link to dashboard. Use `{{value}}` and `{{#is_alert}}` Datadog template syntax.
7. **Routing** — `@pagerduty-<service>` for pages; `@slack-<channel>` for tickets. Tag the team owner.
8. **Tags** — `team:`, `service:`, `severity:`, `slo:` so monitors can be filtered.

## Output

```text
Monitor: refund-p99-500ms

Type: metric alert
Query: avg(last_5m):p99:trace.http.request{service:refund-service} > 0.5

Thresholds:
  critical: 0.5     (500ms, matches SLO threshold)
  warning:  0.4

Evaluation window: 5 minutes (we page on sev2 burn).

No-data: notify_no_data=true, no_data_timeframe=10 (refund is a hot path).

Message:
  @pagerduty-payments
  ## Refund p99 latency above SLO
  p99 latency on refund-service is {{value}}s (threshold 0.5s).
  This is a fast-burn signal on the 99.5% / 28d SLO.

  Runbook: <link>
  Dashboard: <link>

Tags: team:payments, service:refund-service, severity:sev2, slo:refund-latency
```

## Quality bar

- Threshold derived from an SLO or a baseline number, with the source named.
- `notify_no_data` explicitly set, not defaulted.
- Notification routes via `@pagerduty-<service>` (not a person), tagged with team owner.
- Runbook + dashboard links in the message.

## Anti-patterns to avoid

- Anomaly monitors as the first alert — usually too noisy without a strong baseline.
- "Composite" monitors that fan out across teams. Pick a clear owner.
- Notification messages that contain the threshold as a literal but no link to context.

