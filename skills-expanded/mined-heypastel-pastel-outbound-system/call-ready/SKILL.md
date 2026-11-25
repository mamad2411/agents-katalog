---
name: call-ready
description: Screener — decides whether a hot conversation is ready for a call by checking three things (pain, power, priority), then writes either the booking message or the one question that closes the gap. Use on hot replies, demo requests, or "is this worth a call".
---

# Call ready — Screener

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

`fit-check` already judged the account. Here, only the conversation counts: what the person actually wrote.

## Three checks

| Check | The question | Evidence |
|---|---|---|
| **Pain** | Did they describe, in their words, a problem we solve? | their sentence, quoted |
| **Power** | Can they decide, or bring in whoever does? | what they said about their role or team |
| **Priority** | Is there a reason to act soon — a deadline, a target, an event? | the date or event they mentioned |

- **3 of 3 → Book.** Propose a call the way `outbound-brief.md` prefers, with its booking link if it has one.
- **2 of 3 → Ask.** One question aimed at the missing check.
- **0–1 → Keep talking.** Answer what they asked, and ask about their situation; the call comes later.

## Steps

1. Read the whole conversation with `pastel_get_conversation`.
2. Fill the three checks with evidence.
3. Write the next message; run `human-voice`.
4. Once a call is booked, prepare `mark_lead_status` → `PROCESSED`.

## Output

```
# Call ready? — [Person]
Decision: book | ask | not yet
Pain: "…"
Power:
Priority:
Next message:
> …
Booking link: [link] | [missing]
```
