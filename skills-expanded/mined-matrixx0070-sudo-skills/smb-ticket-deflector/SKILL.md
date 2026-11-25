---
name: smb-ticket-deflector
version: 1.0.0
description: Read a forwarded customer email or ticket, pull order/refund/history context, and draft a tone-matched reply — refunds only with owner approval.
author: matrixx0070
tags: [support, customer, tickets, refund, replies, tone]
capabilities: []
---

# Ticket Deflector

## When to use
Run this when the owner forwards a customer email or support ticket and wants a fast, accurate, on-brand reply drafted. It saves the owner from writing every response while keeping them in control of anything that costs money.

**Not for:** sending replies autonomously (every draft gets an owner glance first); anything that spends money without approval; multi-message campaigns (use smb-run-campaign).

## Method
1. **Read the message.** Identify the customer, the request or complaint, and the sentiment.
2. **Pull context.** From connected systems: order details, payment/refund status, shipping, prior interactions with this customer.
3. **Determine the resolution.** Answer, fix, apology, refund, replacement, or escalation. Decision point: if the customer is upset, acknowledge that first; if facts are missing, ask internally rather than guessing in the reply.
4. **Draft a tone-matched reply.** Warm, plain, specific to the order, with concrete next steps and timelines.
5. **Gate anything that costs money.** If the resolution involves a refund, credit, discount, or spend, present it as a proposal and wait for owner approval before sending.
6. **Show every draft.** Even non-monetary informational replies get a quick owner glance before they go out.

## Example
Customer: "Order #5521 arrived cracked, this is ridiculous." Sentiment: angry. Context: delivered 2 days ago, one prior clean order, $58 paid. Resolution: apologize + free replacement (no refund needed) — costs a replacement unit, so gate it. Draft: "Hi Dana, I'm so sorry your order arrived damaged — that's on us. I've queued a free replacement shipping today, tracking to follow. Nothing needed on your end." Present the replacement cost for owner approval before sending.

## Pitfalls
- Sending a refund, credit, or replacement without the owner's approval — the money gate is non-negotiable.
- Replying with generic canned language instead of matching the business's actual voice.
- Answering before pulling order/refund history, so the reply contradicts the record.
- Matching an angry customer's heat instead of acknowledging the frustration and de-escalating.

## Output format
- **Customer + issue summary** with pulled order/refund/history facts.
- **Recommended resolution** and whether it costs money.
- **Drafted reply,** ready to send.
- **Approval gate:** explicit sign-off on any refund or spend; nothing reaches the customer without owner approval.

## Reference

### Resolution decision matrix
| Situation | Resolution | Costs money? | Gate |
|-----------|-----------|--------------|------|
| Damaged/defective on arrival | Apologize + free replacement | Yes (unit + shipping) | Owner approves |
| Never arrived / lost in transit | Reship or refund + carrier claim | Yes | Owner approves |
| Late but arrived | Apology + optional goodwill credit | Maybe | Gate if credit |
| Wrong item sent | Send correct + prepaid return label | Yes | Owner approves |
| Buyer's remorse, in policy | Refund per policy | Yes | Owner approves |
| Buyer's remorse, out of policy | Explain policy warmly; offer alternative | Usually no | Show draft |
| How-to / usage question | Direct answer + resource link | No | Show draft |
| Angry but no clear ask | Acknowledge, ask what would make it right | No | Show draft |
| Chargeback threat / legal | Acknowledge, escalate to owner | — | Escalate |
Every draft — even free, informational ones — gets an owner glance before it sends.

### Reply structure (the ARC pattern)
1. **Acknowledge** — name the feeling and the specific issue ("I'm sorry your order arrived cracked").
2. **Resolve** — state the concrete fix and a timeline ("a replacement ships today, tracking to follow").
3. **Close** — reduce their effort ("nothing needed on your end") + a warm sign-off.
Lead with the human, then the fix. Never bury an apology under policy language.

### Tone-matching guide
| Customer sentiment | Your register |
|--------------------|---------------|
| Angry / heated | Calm, warm, owning it; do **not** match the heat |
| Anxious / worried | Reassuring, specific timelines |
| Confused | Plain, step-by-step, no jargon |
| Neutral / transactional | Efficient, friendly, brief |
| Delighted / thankful | Warm, brief, invite a review |
Always mirror the *business's* brand voice, not generic canned support language.

### De-escalation phrases that work
- "You're right to be frustrated — let me make this right."
- "That's on us, and here's exactly what I'll do."
- "I've already [action], so you don't have to chase this."
Avoid: "Per our policy…", "Unfortunately…", "As I stated…", and passive blame ("your package was damaged" → "the package arrived damaged").

### Context to pull before drafting
Order number + date, amount paid, payment/refund status, shipping/tracking status, this customer's prior order + interaction history, and any relevant policy (returns window, warranty). A reply that contradicts the record destroys trust — pull facts first, and if a fact is missing, ask internally rather than guessing in the reply.

### The money gate (non-negotiable)
Any refund, credit, discount, replacement, or reship **costs money** and is presented as a **proposal** with the dollar amount, then waits for the owner's explicit approval before sending. State the cost plainly: "Proposed: free replacement unit (~$X cost + shipping) — approve to send?"

### Quality bar before showing a draft
Correct order facts · warm + on-brand tone · one clear resolution · concrete next step + timeline · money items gated · no promise the business can't keep. Nothing reaches the customer without the owner's approval.
