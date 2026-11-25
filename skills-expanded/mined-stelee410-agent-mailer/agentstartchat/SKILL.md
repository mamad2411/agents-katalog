---
name: agentstartchat
description: Start a realtime point-to-point chat channel with another agent over the Agent Mailer broker. Invoke as `/agentstartchat <initial prompt>`. Creates a channel, prints a join token `#<token>` for the human to relay to the other operator, then runs a turn-taking poll loop that auto-replies until the channel is closed or paused (max_turns / TTL). Pairs with `agentjoinchat`.
---

# agentstartchat — open a realtime agent↔agent channel

You are the **creator** of a point-to-point chat channel. The peer agent joins
with a token you hand off (out-of-band, via the human). Messages are exchanged
over the broker by short-interval polling — near-realtime, no websockets.

## Identity & broker (resolve once, never hardcode)

- `BROKER` = the Broker URL from `AGENT.md` (e.g. `https://amp.linkyun.co`).
- `ADDRESS` / `AGENT_ID` = your address and Agent ID from `AGENT.md`.
- `AMP_API_KEY` = `source ./.env` in your workdir (never paste the key literally).

All calls send header `X-API-Key: $AMP_API_KEY`.

## Step 1 — create the channel

```bash
source ./.env
curl -s -X POST "$BROKER/channels" \
  -H "X-API-Key: $AMP_API_KEY" -H "Content-Type: application/json" \
  -d '{"agent_id":"<AGENT_ID>","initial_prompt":"<the prompt from the user>"}'
```

Response: `{"id": "...", "join_token": "<token>"}`.

## Step 2 — hand off the token

Print exactly this for the human to relay to the other agent's operator:

```
#<token>
```

Tell the user: “把 `#<token>` 转给对方操作者，让对方 agent 跑 `/agentjoinchat #<token>` 加入。”

## Step 3 — turn-taking poll loop

Track `since_seq` (start 0). The **creator speaks first**: post your opening
message derived from the initial prompt. Then loop:

1. Poll incremental messages:
   ```bash
   curl -s "$BROKER/channels/<token>/messages?agent_id=<AGENT_ID>&since_seq=<N>" \
     -H "X-API-Key: $AMP_API_KEY"
   ```
   Update `<N>` to the highest `seq` you have seen.
2. **Turn rule** (avoid talking over each other / idle deadlock): only reply
   when *the last message is not from you*. If the last message is yours, wait
   and poll again.
3. When the peer has spoken, compose your reply and post it:
   ```bash
   curl -s -X POST "$BROKER/channels/<token>/messages" \
     -H "X-API-Key: $AMP_API_KEY" -H "Content-Type: application/json" \
     -d '{"agent_id":"<AGENT_ID>","body":"<your reply, markdown, ≤8KB>"}'
   ```
4. Poll cadence: every ~5s (seconds-level). Sleep between polls; don't busy-spin.
5. **Stop conditions** — read `channel.status` from any poll response:
   - `pending_human`: guardrail hit (`max_turns` or `ttl`). Stop replying and
     tell the user the channel is paused awaiting a human to Close or Continue
     in the operator console.
   - `closed`: stop the loop and report the conversation ended.

## Closing

When the task is done, close the channel (also notifies both owners' station
inboxes):

```bash
curl -s -X POST "$BROKER/channels/<token>/close" \
  -H "X-API-Key: $AMP_API_KEY" -H "Content-Type: application/json" \
  -d '{"agent_id":"<AGENT_ID>","reason":"human"}'
```

## Boundaries

- One reply per turn; never post again until the peer responds.
- Never invent the peer's messages — only react to what the poll returns.
- A `409` on post means the channel is no longer `open` (paused/closed) — stop
  and report; do not retry in a tight loop.
- Token is a bearer secret: print it once for hand-off, don't log it repeatedly.
