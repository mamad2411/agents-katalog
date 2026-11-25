---
name: triage-error
description: Triage a Sentry issue — group context, frequency trend, recent-deploy correlation, blast radius, suggested next action (fix / ignore / re-prioritize).
---

# triage-error

> Take one Sentry issue and classify it for action. Output is a triage record with frequency + reach + recent-change correlation + the next move.

> **MCP binding (read before any tool call):** resolve which server backs `sentry` from `${POLYMATH_PLUGIN_DATA:-$HOME/.polymath/data}/polymath-core/project-context.json` `mcpResolution.sentry` — when `source` is `host`, the CURRENT host agent's own `sentry` MCP server is ALREADY registered: use its tools (`toolPrefix` gives the naming) and do NOT register or start a polymath copy. A server registered in a DIFFERENT agent is never a substitute. When `source` is `plugin`, the plugin-shipped `.mcp.json` server backs this skill. When `none`, credentials are unconfigured: ask the user to configure them or degrade gracefully. See the `polymath-core:mcp-bridge` skill.

## When to use

- A Sentry issue URL or short-ID lands in the prompt.
- A workflow's bug-triage step has a Sentry signal as the trigger.
- A regular Sentry-cleanup pass.

## Inputs

- Sentry issue URL or `(org, project, issue_id)`.

## Procedure

1. **Fetch the issue** via the sentry MCP (`get_issue`). Pull title, culprit, first-seen, last-seen, event count, user count, environment.
2. **Fetch recent events** (`list_events` or `get_event`). Look at:
   - Stack trace frames in *our* code (not vendor).
   - Breadcrumbs leading to the error.
   - The most-recent event's release tag.
3. **Frequency trend**: events per hour over the last 24h vs the trailing 24h before that. Spike, flat, or fading?
4. **Recent-change correlation**: first-seen timestamp vs deploy timeline. If first-seen lines up within minutes of a deploy, name that deploy.
5. **Blast radius**: distinct users affected, environments touched, whether it's customer-facing.
6. **Action classification** — choose ONE:
   - **Fix now** — high frequency or customer-facing or revenue-impacting.
   - **Fix this sprint** — moderate frequency, not blocking but persistent.
   - **Investigate** — unfamiliar; needs reproduction before classification.
   - **Ignore + suppress** — known third-party noise; suppress with a `.sentryclirc` rule + tracking ticket so we can revisit. Never ignore without a suppression rule.
   - **Re-prioritize** — was open; the trend shifted; bump priority.

## Output

```text
Sentry triage: <issue url>

Title:          RefundServiceException: Stripe timeout
Culprit:        api/refunds.py:create_refund
First seen:     2026-05-24 13:52 UTC (3 minutes after the 13:50 deploy of v0.5.1)
Event count:    1,420 in last 24h (0 the prior 24h — new error)
Users affected: 240 distinct, all envs: production

Trend:          SPIKE (1,420 / 24h vs 0 / prior 24h).
Recent deploy:  v0.5.1 (refund-service) deployed 2026-05-24 13:50 UTC. Correlation: yes.
Blast radius:   customer-facing; revenue path.

Action: FIX NOW.
  - Rollback v0.5.1 → v0.4.7 while investigating; this is sev2 incident
    territory (consider escalating via polymath-incident:incident-triage).
  - Open a tracking ticket for the post-rollback investigation.
  - Suppress new event burst from the polymath-vuln-scan Stop hook
    if it picks the same project up (avoid double-paging).
```

## Quality bar

- Trend computed against a baseline (24h-vs-prior-24h, or 7d-vs-prior-7d).
- Recent-change correlation either confirmed with a named deploy/config-change, or explicitly "no correlation in the last 60 min".
- Action is ONE of the five — not "investigate and fix and maybe ignore".
- IGNORE always pairs with a suppression rule + a tracking ticket. No silent ignores.

## Anti-patterns to avoid

- Marking high-frequency errors as "investigate" because they're scary. Investigate IS an action; pair it with a timebox.
- Ignoring without suppression. The same error keeps showing up next pass.
- Correlating with a deploy by gut, without checking timestamps. The 13:50 deploy didn't necessarily cause the 14:02 trigger — verify.
- Treating user count as proxy for impact when the issue is in a low-volume path used by paying customers. Cite revenue / journey impact directly.

