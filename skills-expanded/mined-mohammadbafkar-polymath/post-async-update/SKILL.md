---
name: post-async-update
description: Post an async standup / status update to a Slack channel — short, structured (yesterday / today / blockers), threaded under a daily anchor.
---

# post-async-update

> Replace the daily-standup meeting with a structured Slack post. Output is the message ts + a pointer to the daily-anchor thread.

> **MCP binding (read before any tool call):** resolve which server backs `incident_comms` from `${POLYMATH_PLUGIN_DATA:-$HOME/.polymath/data}/polymath-core/project-context.json` `mcpResolution.slack` — when `source` is `host`, the CURRENT host agent's own `slack` MCP server is ALREADY registered: use its tools (`toolPrefix` gives the naming) and do NOT register or start a polymath copy. A server registered in a DIFFERENT agent is never a substitute. When `source` is `plugin`, the plugin-shipped `.mcp.json` server backs this skill. When `none`, credentials are unconfigured: ask the user to configure them or degrade gracefully. See the `polymath-core:mcp-bridge` skill.

## When to use

- The user has a daily / weekly status update to share.
- A workflow's reporting step needs to surface progress to the team async.

## Inputs

- The update body (or invoke `polymath-communication:meeting-notes` to draft one first).
- The channel (e.g. `#team-payments-standup`).
- Daily-anchor strategy:
  - **anchor-per-day** (default): a single bot-posted "Standup — YYYY-MM-DD" message at 09:00 user-local; everyone threads their update under it.
  - **flat**: each person posts at the top level. Use only when the team is small (< 5).

## Procedure

1. **Resolve channel ID** via the slack MCP.
2. **Find or create the daily anchor** (anchor-per-day mode): search the channel for today's "Standup — YYYY-MM-DD" message in the last 24h. Create one if absent.
3. **Format the update** in the standard structure:
   - **Yesterday** — what shipped or moved.
   - **Today** — what's planned.
   - **Blockers** — what's stuck and who can unblock.
   Each section ≤ 3 bullets. No prose paragraphs.
4. **Post threaded** under the daily anchor. Return the posted `ts`.

## Output

```text
post-async-update

Channel:        #team-payments-standup (id C0XXXXXX)
Daily anchor:   1716566400.000100 ("Standup — 2026-05-24")
Posted ts:      1716566700.000700

Update:
  Yesterday: shipped rate-limit middleware (PR-1234); reviewed lodash bump.
  Today:    SLO design for refund-create; pair with @bob on idempotency tests.
  Blockers: waiting on platform team for the new Redis cluster.
```

## Quality bar

- 3 sections, ≤ 3 bullets each. No prose body.
- Blockers section names a person who can unblock (or "none").
- Posted threaded under the daily anchor (or explicitly flat if that's the team's convention).

## Anti-patterns to avoid

- Pasting a stream-of-consciousness without the 3 sections. Defeats the point.
- "No blockers" when there are blockers but you don't want to call them out. Surface them; that's the whole value.
- Posting to the wrong channel because anchors aren't searched. Verify the anchor message exists.

