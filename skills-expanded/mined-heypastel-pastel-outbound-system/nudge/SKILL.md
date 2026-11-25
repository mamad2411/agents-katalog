---
name: nudge
description: Concierge — keeps conversations moving by alternating a public touch (a comment on their latest post) with a private one (a DM that brings something new), follows up on the dates people gave, and unblocks stuck Pastel sequence runs. Use for "follow up", silence after connecting, curious / timing / pushback conversations, or runs needing attention.
---

# Nudge — Concierge

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

Each follow-up adds something to the conversation: a thought on their latest post, an example from a similar company, a number they'd find useful.

## In scope

- `curious`, `timing`, and `pushback` conversations from `reply-desk`.
- Connected, opening message sent, no answer yet.
- Pastel runs with `status="needs_attention"`.

## The rhythm: public, then private

| Touch | When | Where |
|---|---|---|
| 1 | — | The opening message (from `campaign-launch`) |
| 2 | 3 business days of silence | **Public:** a comment on their latest post through `social-warmup`, if they posted in the last two weeks. If not, a DM with something useful attached to the conversation. |
| 3 | 8 business days after touch 2 | **Private:** a short DM that leaves the door open, with a reason to come back to it later. |

That's the whole rhythm. `timing` conversations skip it: one message, on the date they gave.

## Steps

1. Gather the conversations and runs in scope.
2. **Stuck runs:** read the failing step in `pastel_get_sequence_run` and prepare `resolve_sequence_step` with `resolve` or `resend`. `confirmed_resend` only if the user accepts a possible duplicate.
3. **Write** the touch, then `human-voice`.
4. Prepare `send_chat_message` on the `chat_id`, or the comment through `social-warmup`, for approval.

## Output

Same layout as `message-writer`, plus `chat_id`, touch number, channel, and the `not before` date.
