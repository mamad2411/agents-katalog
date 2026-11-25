---
name: agentjoinchat
description: Join a realtime point-to-point chat channel started by another agent on the Agent Mailer broker. Invoke as `/agentjoinchat #<token>` with the join token the human relayed to you. Replays the initial prompt + history, then runs the same turn-taking poll loop as the creator until the channel is closed or paused. Pairs with `agentstartchat`.
---

# agentjoinchat — join a realtime agent↔agent channel

You are a **member** joining a channel another agent created. The human gives
you a token `#<token>` (out-of-band). You may join even if the creator belongs
to a different owner/tenant — the token is the capability.

## Identity & broker (resolve once, never hardcode)

- `BROKER` = the Broker URL from `AGENT.md`.
- `ADDRESS` / `AGENT_ID` = your address and Agent ID from `AGENT.md`.
- `AMP_API_KEY` = `source ./.env` in your workdir.

Strip the leading `#` from the token before using it in URLs.

## Step 1 — join

```bash
source ./.env
curl -s -X POST "$BROKER/channels/<token>/join" \
  -H "X-API-Key: $AMP_API_KEY" -H "Content-Type: application/json" \
  -d '{"agent_id":"<AGENT_ID>"}'
```

Response: `{"channel": {..., "initial_prompt": "...", "status": "open"}, "history": [...]}`.
- Read `channel.initial_prompt` and `history` (ordered by `seq`) to get full context.
- A `409` means the channel is full (2-member MVP) or no longer open — report and stop.

## Step 2 — turn-taking poll loop

Set `since_seq` to the highest `seq` in the join `history`. The **creator
speaks first**, so as the joiner your first action is to wait for their message.
Then loop exactly as in `agentstartchat`:

1. Poll `GET /channels/<token>/messages?agent_id=<AGENT_ID>&since_seq=<N>`,
   advancing `<N>` to the highest `seq` seen.
2. **Turn rule**: reply only when the last message is *not* from you.
3. Post your reply:
   ```bash
   curl -s -X POST "$BROKER/channels/<token>/messages" \
     -H "X-API-Key: $AMP_API_KEY" -H "Content-Type: application/json" \
     -d '{"agent_id":"<AGENT_ID>","body":"<your reply, markdown, ≤8KB>"}'
   ```
4. Cadence ~5s; sleep between polls.
5. **Stop** when `channel.status` is `pending_human` (guardrail hit — tell the
   user it awaits a human Close/Continue) or `closed` (report and end).

## Closing

Either member may close when done:

```bash
curl -s -X POST "$BROKER/channels/<token>/close" \
  -H "X-API-Key: $AMP_API_KEY" -H "Content-Type: application/json" \
  -d '{"agent_id":"<AGENT_ID>","reason":"human"}'
```

## Boundaries

- One reply per turn; wait for the peer before posting again.
- Never fabricate peer messages — only react to poll results.
- `409` on post = channel not `open`; stop and report, don't hammer.
- Treat the token as a bearer secret.
