---
name: message-writer
description: Ghostwriter — writes the LinkedIn invitation note, the opening message once connected, and a variant B, built on each lead's why-now sentence, then runs human-voice on them. Use for "write the messages", drafts for a batch of leads, or fixing a message that sounds automated.
---

# Message writer — Ghostwriter

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md)

Write from the **why now** sentence and the proof in the lead card, in the voice set by `outbound-brief.md`. Use the lead's language if Pastel shows it; if not, the user's.

## Three drafts per lead

| Draft | Length | Job |
|---|---|---|
| **Invitation note** | ≤ 180 characters, counted | Get the connection accepted. The why-now point and a light question. No pitch, and no product or company name of ours. |
| **Opening message** | ≤ 50 words | Sent once connected: the why-now point, what it means for them, one question they can answer in a line. |
| **Variant B** | same limits | Same facts, different entry point, so the user can pick or A/B test. |

The Buying Committee seat changes the angle: deciders hear outcomes and cost, users hear about their day, champions hear back what they already said.

## Rules

- Open with the topic, not the surveillance: talk about what the post they engaged with was about ("teams juggling five outbound tools…"), never "I saw your comment" or "you commented DEMO".
- The ask is small: something they can answer from their phone in one line.
- The Buying Committee seat, if any, decides the angle (see above).
- When `why-now` is `thin`, write shorter rather than padding it.

## Steps

1. Read the lead card: why now, proof, seat, quality.
2. Write the three drafts.
3. Run `human-voice` on all of them.
4. Return them as drafts; `campaign-launch` handles sending after approval.

## Output

```
# Drafts — [date]

### [Person] · [Company] · priority [n]
Why now: …
Invitation note ([n]/180):
> …
Opening message:
> …
Variant B:
> …
```
