---
name: post-incident-comms
description: Post an incident-comms update to the right Slack channel + thread; pairs with polymath-incident:comms-update for the body and respondToIncident for context.
---

# post-incident-comms

> Take a comms-update draft (or write one) and post it to the right Slack channel + thread. Output is the posted ts so the next update can thread under it.

> **MCP binding (read before any tool call):** resolve which server backs `incident_comms` from `${POLYMATH_PLUGIN_DATA:-$HOME/.polymath/data}/polymath-core/project-context.json` `mcpResolution.slack` — when `source` is `host`, the CURRENT host agent's own `slack` MCP server is ALREADY registered: use its tools (`toolPrefix` gives the naming) and do NOT register or start a polymath copy. A server registered in a DIFFERENT agent is never a substitute. When `source` is `plugin`, the plugin-shipped `.mcp.json` server backs this skill. When `none`, credentials are unconfigured: ask the user to configure them or degrade gracefully. See the `polymath-core:mcp-bridge` skill.

## When to use

- An incident comms update was drafted by `polymath-incident:comms-update` and needs to go out.
- A `respondToIncident` workflow step needs to broadcast progress.
- A status-page-style update is going to the internal channel.

## Inputs

- Update body (required) — or invoke `polymath-incident:comms-update` first to draft one.
- Incident ID (required) — used to derive the channel name + locate the thread.
- Channel — explicit (`#inc-2026-09`) or computed from the incident ID. Fall back to `userConfig.defaultIncidentChannel` when neither is supplied.
- Parent thread `ts` (optional) — when set, the post threads under it. When absent, this update opens a new thread and the returned `ts` becomes the thread root for follow-ups.

## Procedure

1. **Resolve the channel.** Prefer explicit channel input; fall back to `inc-<incident-id-slug>`; fall back to `userConfig.defaultIncidentChannel`. If none resolves, surface and stop.
2. **Look up the channel ID** via the slack MCP's `conversations_list` (or `channels.list`). Slack APIs take channel IDs, not names.
3. **Format the body** — `polymath-incident:comms-update` already produces a status / impact / next-update structure. Don't re-wrap; post as-is into a Slack code block or as Markdown if the channel renders it.
4. **Post** via the slack MCP's `chat_postMessage` with:
   - `channel`: resolved ID.
   - `thread_ts`: if a parent was supplied.
   - `text`: a short fallback summary (Slack uses it for push notifications and screen-readers).
   - `blocks`: rich layout with the structured fields.
5. **Return the posted message's `ts`** so the next update can thread under it. Save it as a step artifact (e.g. `docs/incidents/<id>-slack-thread.ts`).
6. **Status-page channel mirror** — for sev1/sev2, also post a one-line summary to the status-page channel (separate channel from the incident channel). The summary points back to the incident channel for thread continuation.

## Output

```text
post-incident-comms

Resolved channel: #inc-2026-09 (id C0XXXXXX)
Parent thread ts: 1716572400.000200
Posted ts:        1716572734.000300
Mirrored to:      #status-page (one-line summary)

Saved thread root: docs/incidents/2026-09/slack-thread.ts
```

## Quality bar

- Channel ID resolved before posting (not the name).
- Thread root saved as a step artifact so subsequent updates thread correctly.
- Status-page channel mirror for sev1/sev2 (one line, no body duplication).
- No PII in the fallback `text` field — it appears in push notifications.

## Anti-patterns to avoid

- Calling `chat_postMessage` with the channel name. Some Slack APIs accept it; some don't. Resolve to ID.
- Re-posting the full update to two channels — duplicate noise. Mirror is one line + a back-pointer.
- Posting without a thread when one exists. Splits the conversation.
- Logging the body to plain logs (PII risk). The slack MCP holds it; we don't.

