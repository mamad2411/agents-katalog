---
name: agent-message-broker
description: Subscribe running coding-agent sessions to real-world event topics (GitHub, Jira, Google Workspace, polled URLs, webhooks) via the amb CLI, and react to events the broker delivers mid-session. Use when an amb event arrives in this session, or when the user asks to wire an event source or topic to an agent session.
---

# agent-message-broker (amb)

amb is a local pub/sub broker that routes external events into running coding-agent sessions. Event sources publish to **topics**; **subscriptions** bind a topic to a live agent session and render each event with a template. Everything is available over the `amb` CLI — you can wire sources and subscribe yourself without any UI.

## Prerequisites

- Node >= 22.5. The CLI is `amb` (or `npx agent-message-broker …`).
- The broker must be running locally at `http://127.0.0.1:4733`. Check with:

```bash
amb doctor          # broker health + registered agent kinds
```

If it is not running, tell the user; start it only if asked (`npx agent-message-broker`).

- CLI auth is automatic: the broker's bearer token lives at
  `~/.config/agent-message-broker/token` (mode 0600) and the CLI picks it up.
  Never print or exfiltrate this token.

## When an event arrives in this session

Events are delivered as rendered text from the subscription's template — `{{kind}}` is the event type, `{{payload}}` its JSON. The frame may be mid-conversation (steered into your active turn). React in the current conversation:

1. Parse the intent from `kind` and `payload` (do not ask the user to re-paste it).
2. If you need more history, inspect the topic: `amb events list --topic <name> --limit 20`.
3. Act on the event (the event usually names a concrete artifact: a PR, ticket, doc, URL).
4. Keep going; do not stop and wait unless the event is genuinely ambiguous.

## Discovering state

```bash
amb topics list                       # existing topics + retention
amb sources list                      # wired sources per topic
amb sources running                   # which feeds are actively polling
amb sessions                          # live agent sessions visible to the broker
amb events list --topic <idOrName>    # recent retained events (replay window)
amb deliveries [eventId]              # audit delivery attempts per event
```

Events persist per-topic up to `retainN` even with zero subscribers, so a new subscription can replay the recent window — you never need to ask the user "what did I miss" if it is within retention.

## Subscribing this session to a topic

If a topic already exists, one command suffices (get your session id from `amb sessions` or ask the user):

```bash
amb subscriptions create --topic <idOrName> --agent pi|claude|codex --session <sessionId> \
  --template "PR event {{kind}}: {{payload}}"
```

To create the whole wiring from scratch:

```bash
amb topics create <name> --retain 100
amb sources create --topic <name> --kind <kind> --options '{…}'
amb sources start <sourceId>          # sources start stopped; this begins polling
```

Source kinds and their `--options` JSON: see [references/sources.md](references/sources.md).
Delivery mechanisms per agent kind and the delivery audit model: see [references/delivery.md](references/delivery.md).

## Credentials for event sources

Vendors are polled with the developer's own credentials, scaffolded once:

```bash
amb config init --kind github   # then fill ~/.amb/github/credentials.json
amb config init --kind jira     # → ~/.amb/jira/credentials.json (email, apiToken, domain)
amb config init --kind google   # service-account JSON, or `amb google login` for OAuth
```

If a source fails auth, point the user at the relevant `~/.amb/<kind>/credentials.json` — do not attempt to create vendor credentials yourself.

## Design rules to respect

- Prefer an existing topic/source over creating a duplicate; list first.
- Choose `intervalMs` conservatively (60s+ for most feeds) — this is a local machine.
- Use `--template` to make delivered frames self-describing; the payload is raw JSON.
- Webhook delivery is an opt-in tier (requires a tunnel); polling is the default and needs nothing internet-reachable.
