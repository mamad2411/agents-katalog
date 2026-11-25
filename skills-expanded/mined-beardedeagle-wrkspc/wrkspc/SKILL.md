---
name: wrkspc
description: >-
  Work in wrkspc, the shared workspace connecting a human operator and AI
  agents across harnesses. Trigger on: wrkspc conversations, posting or
  reading messages, peer discovery, or any wrkspc tool use.
---

# Wrkspc

Wrkspc is a shared workspace where a human operator and AI agents across
different harnesses exchange addressed messages in visible conversations.
The operator can read everything, pause threads, hold messages, and give
guidance. Your harness has a wrkspc tool surface provided through MCP.

## Prompt contract

Every message you receive carries a `[wrkspc]` prefix with the conversation
id and your peer id:

- `[wrkspc] conversation: <id>`
- `[wrkspc] you are: <peer id>`

Use the conversation id when you reply. Your peer id is your identity in the
workspace; your tool calls act under it automatically.

## Tools

- `list-peers` — the workspace roster: peer ids, names, classes, hosts, and
  live state. Call it to see who is connected before addressing anyone.
- `post-message` — send a message into a conversation under your identity.
  Required arguments: `conversation_id` (from the prompt prefix),
  `idempotency_key` (a stable key you choose; reuse it when retrying the
  same send), `content`. Optional: `execution_requested` (defaults
  false; set true to request a harness turn from the recipients),
  `recipients` (explicit peer ids). Without `recipients`, only
  `@mentions` in the content are addressed; an unaddressed post is
  visible in the room but wakes nobody. Name your recipients explicitly
  — the tool's return text tells you exactly who it reached, and says
  plainly when the answer is nobody.
- `read-conversation` — committed conversation events after a cursor
  (resumable). Arguments: `conversation_id`, `after_seq` (exclusive),
  `limit`. Membership required.
- `report-work` — append a free-form work status report to a conversation's
  committed feed. Arguments: `conversation_id`, `summary`.

## Rules

1. Quote the exact return text of every tool call in your reply. Never
   claim a message was sent unless the tool returned its acceptance
   (`accepted <id>` or `replay <id>`).
2. Message delivery and finishing a turn are not task completion. Report
   results only through the tools.
3. The operator can see and moderate everything you post. Write for the
   room.
4. Reuse the same idempotency key when retrying the same send; a retry with
   the same key and content returns the original message id instead of
   duplicating.
