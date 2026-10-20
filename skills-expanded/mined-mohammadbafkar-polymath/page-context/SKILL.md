---
name: page-context
description: Fetch the full context for an active PagerDuty incident — log entries, oncall, related services, recent deploys — before responders join.
---

# page-context

> Front-load context for the on-call before they're fully awake. One incident in, one summary out.

> **MCP binding (read before any tool call):** resolve which server backs `pager` from `${POLYMATH_PLUGIN_DATA:-$HOME/.polymath/data}/polymath-core/project-context.json` `mcpResolution.pagerduty` — when `source` is `host`, the CURRENT host agent's own `pagerduty` MCP server is ALREADY registered: use its tools (`toolPrefix` gives the naming) and do NOT register or start a polymath copy. A server registered in a DIFFERENT agent is never a substitute. When `source` is `plugin`, the plugin-shipped `.mcp.json` server backs this skill. When `none`, credentials are unconfigured: ask the user to configure them or degrade gracefully. See the `polymath-core:mcp-bridge` skill.

## When to use

- A pager just fired and someone wants the situation at a glance.
- A workflow's first step after triage is "gather everything about the incident".

## Inputs

- Incident URL or ID.

## Procedure

1. **Fetch the incident** (`get_incident`) — status, urgency, title, created_at, assigned responder.
2. **Fetch log entries** (`list_log_entries`) — every trigger / ack / snooze / note in chronological order. This is the timeline so far.
3. **Fetch on-call** for the affected service (`get_oncall_for_service`) — who's currently up.
4. **Cross-link** any deploy / change records in the incident description or notes (parse for GitHub PR URLs, Jira keys, Datadog alert IDs — the other connectors handle those).
5. **Summarize** for the responder in this exact order:
   - **What** — one sentence, plain language.
   - **Since when** — start time + minutes elapsed.
   - **Who's on it** — assigned responder + escalation policy next-up.
   - **What we know** — from log entries / notes.
   - **What changed recently** — most recent deploys / config changes in the last 60 minutes (from cross-linked sources).
   - **First check** — the single highest-signal dashboard or metric to look at.

## Output

```text
PagerDuty: PT9X3HQ7 — Refund p99 latency above SLO

Status: triggered, urgency=high
Since:  2026-05-24 14:02 UTC (8 minutes ago)
Assigned: @payments-oncall (escalation in 12 min → @platform-oncall)

What we know:
  - 14:02 trigger from Datadog monitor "refund-p99-500ms"
  - 14:05 secondary trigger: refund 5xx rate > 1%
  - No human notes yet.

Recent change:
  - 13:50 GitHub: refund-service main → prod deploy (refund:0.5.1)
    https://github.com/example/refund-service/actions/runs/12345

First check:
  Grafana refund-service overview — confirm latency vs 5xx, both since 13:50.
```

## Quality bar

- Time elapsed since trigger is computed, not "recent".
- Assigned responder named explicitly, plus next-up.
- "Recent change" only includes the last 60 minutes; older context is noise during an incident.
- Single first-check recommendation, not a checklist of five.

## Anti-patterns to avoid

- Pasting the entire log_entries list. Summarize.
- Speculating about root cause from the title alone.
- Skipping the "what changed recently" step — fast cause-narrowing is the whole point.

