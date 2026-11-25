---
name: slack-messaging
description: Search, read, and send Slack messages via mcporter CLI. Use for "find when I said X on slack", "any conversation about X", "message <person/team> about X", "send to #channel" (a leading # usually means a Slack channel), "respond to this thread <link>", or getting context from a Slack link.
only-on-hosts: ["jrose-04LCLG"]
---

# Slack via mcporter

`mcporter call slack.<tool> key=value ...` → JSON with a markdown `results` field. Every tool name is prefixed `slack_` (e.g. `slack.slack_search_public_and_private`).

| You want to… | Move |
|---|---|
| Find when **I** said X | `slack_search_public_and_private query="from:me X"` |
| **What's waiting on me** today | see [daily triage](references/searching.md#daily-triage) |
| Any conversation about X | `slack_search_public_and_private query="X"` |
| Context from a Slack **link** | parse link → `slack_read_thread channel_id=C… message_ts=…` (needs `message_ts`, **not** `thread_ts`; use the URL's `thread_ts` as `message_ts`) |
| Message a person/team | resolve ID → `slack_send_message_draft` |
| Send to **#channel** (leading # = channel name) | resolve channel ID → `slack_send_message_draft` |
| Reply to a thread **link** | parse link → `slack_send_message thread_ts=…` |
| Find a **channel ID** by name | `slack_search_channels query="name" response_format=concise` |

Details: [searching](references/searching.md) · [sending](references/sending.md) · [formatting](references/formatting.md) · [directory](references/directory.md).

## Token discipline (search is a hog)

- Scan with `response_format=concise include_context=false limit=20`; re-fetch full context only for real hits.
- Pipe big results to a file and grep, don't dump into context.
- Delegate broad searches to a subagent that returns only the answer + permalinks.

## Common IDs

Me (Jack): `U010S548P0F`. Ignore bot senders when triaging: Camper Portal Bot, Jira, Slackbot, agent-orchestrator (`U0B52APG03E`). Channels (private): #wol_devex `C02NUQ65U2C` · #team_hotel `C0B97KTKH25` · #team_agentic_engineering `C0BAJEK3HH8`. Shay `U09UM9ZC6NN` · Felicity `U0ADQP9DSNS` · Elliott `UFMU99PCG`. Others → [directory](references/directory.md).

Resolve a channel name → ID (needed before sending): `mcporter call slack.slack_search_channels query="learn_ai_agents" response_format=concise` → `#learn_ai_agents (C07318DS6MV)`. Add `channel_types=public_channel,private_channel` for private ones.

Send: `mcporter call slack.slack_send_message_draft channel_id=C… message="…"` (DM = user_id as channel_id). No Block Kit. Full tool list: `mcporter list slack`.
