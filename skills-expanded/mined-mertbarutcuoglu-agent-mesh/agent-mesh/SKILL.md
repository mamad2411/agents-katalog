---
name: agent-mesh
description: Cross-session expert queries between local AI coding agents over a transactional SQLite-backed mesh. Use when you need information about a different project than the one you are working in, when you ask a peer agent a question with mesh ask, when you reply to an inbox message with mesh reply, when you join or leave a mesh, or when you handle a broadcast notification from another peer.
---

# Agent Mesh

You are part of a local mesh of AI coding agents. Each agent is the deepest expert on its own project's recent state. When you need information about a project other than the one you are working in, prefer asking the responsible peer over exploring the foreign codebase yourself — that peer has live context you do not.

## Command reference

Quote every argument that contains spaces (questions, answers, roles, topics, messages, context). Required flags are marked.

| Task | Command |
|------|---------|
| Join a mesh | `mesh join <mesh-name> --project <name> --agent <agent> [--mode responder] [--role "<expertise>"] [--topics "<a,b,c>"]` |
| List peers (routing) | `mesh peers --json` — inspect `delivery_mode` and `reachable` |
| Ask a peer | `mesh ask "<question>" --to <project-or-node-id> --context "<why>"` |
| Reply to a query | `mesh reply <msg-id> "<answer>"` |
| Announce to all peers | `mesh broadcast "<message>" --context "<why>"` |
| Show/update your contract | `mesh contract --show` / `mesh contract --role "<expertise>" --topics "<a,b,c>"` |
| Show status and mode | `mesh status` |
| Read inbox manually | `mesh inbox` |
| Wait for one message | `mesh inbox --wait [--wait-timeout <duration>] [--responder-only]` |
| Leave the mesh | `mesh leave` |

`mesh inbox` inspects pending messages without waiting. `mesh inbox --wait` is a manual one-shot wait: it defaults to 55 seconds, emits at most one complete notification, and exits. Set `--wait-timeout <duration>` to change the bound (`0` waits until cancelled), or add `--responder-only` to no-op outside responder mode. Run it again to receive another message.

`mesh join` **requires** `--project`. `mesh ask` **requires** `--to`. Omitting a required flag fails with exit code 2. Never invent a `--to` value — resolve the real target from `mesh peers --json` first (see Routing).

## Routing — finding the right peer

Before asking, decide who to ask:

- If the user named a peer or project ("ask the backend", "check payments-api"), use that target directly.
- Otherwise run `mesh peers --json` and inspect the output:
  - Skip peers where `is_self: true`.
  - Use `reachable` plus `delivery_mode` to set synchronous expectations. `reachable: true` means a live `active_session` or `unattended` adapter can receive now. `reachable: false` means the default ask will queue rather than wait; `next_turn`, `manual`, and an empty delivery mode all fall into this category.
  - Treat `stale` as a compatibility freshness diagnostic, not as the gate for routing or waiting.
  - Match your question against each peer's `contract.role` and `contract.topics`; pick the best fit.
  - If several fit equally, pick the most specific or ask the user briefly.
  - If no peer covers the question, say so — do not pick a poor match.

The CLI does not auto-route; you are the router. Use the exact `project` (or `node_id`) from the JSON as your `--to` value.

## Asking

```
mesh ask "<question>" --to <project-or-node-id> --context "<why>"
```

Queries have a 24-hour default TTL. If the selected peer reports `reachable: true`, the CLI waits up to 60 seconds by default and prints the reply. If `reachable: false`, the default command durably queues the query, prints its ID, and returns immediately. Supplying `--timeout <seconds>` explicitly forces a wait even for an unreachable peer; `--timeout 0` always queues without waiting. Retrieve later replies with `mesh inbox`. `--context` is optional but strongly recommended, and a `node_id` disambiguates duplicate project names.

## Joining

```
mesh join <mesh-name> --project <name> --agent <agent> [--mode responder] [--role "<expertise>" --topics "<a,b,c>"]
```

`--project` is required. On Pi pass `--agent pi`. Add `--role` and `--topics` so peers can route to you — you can change them later with `mesh contract`. Add `--mode responder` for a node that only answers and never asks.

## Responding to incoming queries

When an `=== AGENT MESH ===` block appears at the top of your turn, you have incoming messages. For each query:

1. Read it. Decide if it is within your project's expertise.
2. If yes: answer concisely from your live context. Cite commits or files. State confidence ("I'm sure" vs "I think — verify with X").
3. If no: reply `I don't have expertise on this. Try asking <peer> instead.` Don't hallucinate.
4. Always send the answer with `mesh reply <msg-id> "<answer>"`. Never leave a peer waiting.

For multiline or quote-heavy answers, read the reply from a file or stdin:

```
mesh reply <msg-id> --file <path>
mesh reply <msg-id> --file -
```

`--file -` reads the complete answer from stdin. Provide exactly one answer source: either the positional `"<answer>"` or `--file`.

## Broadcasts

**Receiving:** a `broadcast (FYI, no reply expected)` line is a notification, not a question. Read it, note anything that affects your project, and fold it into your next steps. Do not `mesh reply` to it. `mesh gc` cleans up expired broadcasts.

**Sending:** to announce something to every active peer (a breaking change, a coordination signal), use:

```
mesh broadcast "<message>" --context "<why>"
```

Broadcasts expect no reply.

## Updating your contract

When your responsibilities change, update what peers see when routing:

```
mesh contract --role "<expertise>" --topics "<a,b,c>"
```

Run `mesh contract --show` to print the current contract.

## Responder mode

If `mesh status` shows `mode=responder`, you answer queries only — you cannot initiate `mesh ask` or `mesh broadcast`.

## Receiving messages

The Pi package extension runs `mesh inbox --hook` on Pi's `before_agent_start` event and surfaces pending messages as an `=== AGENT MESH ===` block before each turn. Because delivery only fires when Pi starts a turn, it advertises `delivery_mode: next_turn` with `reachable: false`, not unattended delivery. Check `mesh inbox` manually when running as a responder without new turns.

Only run `mesh inbox --wait --monitor` under a facility that surfaces each stdout line as an event. Under exit-notification backgrounding, use `mesh inbox --wait --responder-only --wait-timeout 0`, verify its process and `mesh status`, and re-arm it after each message. An unread monitor claims messages before another path can surface them: queries remain leased, while one-way messages may be completed without reaching the agent.

## Etiquette

- Be concise. Peers pay tokens for your answer.
- Quote, don't paraphrase, when accuracy matters.
- Don't run long commands during a reply unless asked.
- If you don't know, say so. Don't bluff.

## Exit codes

- `0` — success
- `2` — user error (bad flags, missing required flag, mode violation, ambiguous `--to`)
- `3` — not joined to a mesh; run `mesh join <mesh-name> --project <name>`
- `4` — mesh state issue (missing msg-id or unavailable mesh database)
- `5` — `mesh ask` timed out
