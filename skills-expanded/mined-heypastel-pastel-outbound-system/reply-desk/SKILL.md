---
name: reply-desk
description: Concierge — goes through the LinkedIn inbox via Pastel, tags each conversation (hot, curious, timing, pushback, stop, skip), quotes what the person wrote, and drafts the answer. Use for "check my replies", "who's interested", or clearing the inbox.
---

# Reply desk — Concierge

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

## Steps

1. `pastel_list_conversations(unread_only=true)`; include recent read ones if asked. Open each with `pastel_get_conversation`. The inbox comes from Pastel's copy of LinkedIn, which can lag slightly — say so if timing matters.
2. **Tag** every conversation:

| Tag | Sounds like | Goes to |
|---|---|---|
| **hot** | "Can we talk?", asks for a price, a demo, or next steps | `call-ready`, now |
| **curious** | Wants to understand something, no intent yet | answer here, then `nudge` if they go quiet |
| **timing** | "Not now", "after Q3", out of office with a return date | `nudge`, scheduled for the date they gave |
| **pushback** | Has a tool, no budget, not a priority | one thoughtful answer here, then leave it |
| **stop** | Asks not to be contacted, or is hostile | record it; no more messages |
| **skip** | Automatic notes, a bare "thanks", emoji | nothing |

3. **Draft answers** for hot, curious, and pushback, hot first; run `human-voice`; prepare `send_chat_message` on the conversation's `chat_id` for approval.
4. **For every stop:** prepare `mark_lead_status` → `NOT_INTERESTED` and a pause of any running sequence.

## Output

```
# Replies — [date]
Open: n · hot n · curious n · timing n · pushback n · stop n

### [Person] · [tag]
They wrote: "…"
Answer:
> …
Next: [skill] · chat_id […]
```
