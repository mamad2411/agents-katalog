---
name: smb-handle-complaint
version: 1.0.0
description: Handle a single customer complaint end-to-end — context, root cause, an owner-approved remedy, a drafted response, and an operational fix.
author: matrixx0070
tags: [small-business, complaints, customer-service, retention, service-recovery, operations]
capabilities: []
---

# Handle a Complaint

## When to use
Use this when a customer raises a complaint and the owner wants to respond well, keep the relationship, and stop the same problem recurring — not just fire off an apology.

**Not for:** aggregating many complaints into themes (use smb-customer-pulse) or drafting reusable templates across issues (use smb-customer-pulse-check). This handles one case, deeply.

## Method
1. **Capture the complaint.** State what the customer said, the channel, the order/account, and the outcome they want.
2. **Pull context.** Note the customer's history — tenure, spend, prior issues — and what actually happened on your side.
3. **Diagnose root cause.** Separate the symptom from the underlying cause (process gap, product defect, miscommunication, one-off).
4. **Decide the remedy.** Propose the resolution — apology, fix, refund, replacement, credit, or goodwill gesture. Decision point: size it to both the severity and the customer's lifetime value; a loyal high-spender warrants more than a first-time buyer with a minor gripe.
5. **Draft the response.** Write a message that acknowledges, takes responsibility where due, states the remedy and timeline, and stays warm and specific.
6. **Prescribe the operational fix.** Recommend the change that prevents recurrence, with an owner.

Any refund, credit, compensation, or customer-facing reply requires owner approval before it goes out or money moves — present them as proposals.

## Example
Complaint (email): "My monthly delivery arrived broken again." Context: 3-year customer, ~$1,200/yr, second breakage in two months. Root cause: new packaging insert too thin. Proposed remedy: replace free + one month credit ($40) — pending approval. Draft response opens: "You've been with us three years and this is twice now — that's on us." Operational fix: revert to the thicker insert; owner = ops lead.

## Pitfalls
- **Apology without a fix.** "Sorry for the inconvenience" with no remedy or root cause loses the customer anyway.
- **One-size remedy.** Over-compensating a minor issue trains bad behavior; under-compensating a loyal customer loses them.
- **Sending before approval.** Every reply and any money movement waits for the owner's yes.
- **Skipping prevention.** If you don't name the operational fix, the same complaint returns.

## Output format
```
Complaint: <what> | channel <..> | desired outcome <..>
Customer context: tenure, value, history
Root cause: ___
Proposed remedy: <action> — cost/credit $__ (pending owner approval)
Draft response: "<ready to send on approval>"
Operational fix: <change> — owner <who> — prevents <what>
```

## Reference

### Severity × loyalty remedy matrix
Size the remedy to two axes: how badly the customer was hurt (severity) and how much the relationship is worth (tenure + annual spend + margin). Use this as a starting grid, then let the owner adjust.

| Severity | New / low-value customer | Established / mid-value | Loyal / high-value (top 20%) |
|----------|--------------------------|--------------------------|------------------------------|
| Minor (cosmetic, small delay, easily reversed) | Sincere apology; fix it | Apology + small goodwill ($ or 5-10% credit) | Apology + goodwill + proactive check-in |
| Moderate (defect, repeated delay, billing error) | Apology + full fix/replacement | Fix + partial credit (10-20%) or one free period | Fix + credit + a call from the owner |
| Severe (safety, data, total service failure, second occurrence) | Full refund or replacement + apology | Refund/replacement + meaningful credit (25%+) | Refund + credit + retention offer + owner ownership of the fix |

Rule of thumb: a goodwill gesture should cost less than one month of that customer's margin for minor/moderate cases. Anything above that, or any cash refund, is an owner decision. Second occurrence of the *same* issue jumps one severity row — repeat failure is itself the injury.

### Response template by complaint type
Every draft follows the same spine — **Acknowledge → Own → Remedy + timeline → Prevent → Warm close** — but the emphasis shifts:

- **Product defect / breakage.** Lead with the fix, not the apology. "You shouldn't have received a broken {item} — a replacement ships {date}, and I've credited {amount}. We've also changed {root cause} so it stops here."
- **Billing / double-charge.** Money back first, explanation second. "You were charged twice; the duplicate ${amount} is refunded and will clear in {2-5 days}. Here's exactly what happened and the guardrail we added."
- **Late / missed delivery.** Concrete new commitment, no vague "soon." "Your order is now {status}, arriving {date/time}. For the delay, {remedy}."
- **Rude / poor service.** Own the behavior without blaming the staffer publicly. "That's not how we treat customers, and I'm sorry. I've spoken with the team and {change}."
- **Expectation gap (worked as designed but felt wrong).** Validate the feeling, clarify gently, offer a bridge. Don't over-refund a non-error, but don't win the argument and lose the customer.

### Escalation ladder
1. **Frontline resolve** — within remedy authority, same day. Target first-response < 4 business hours, resolution < 24-48 hours.
2. **Owner review** — any refund, credit above the goodwill threshold, public reply, or legally/safety-sensitive issue. Always for top-20% customers.
3. **Formal / external** — threats of legal action, regulator/chargeback, or media/viral review. Stop drafting casual replies; loop in the owner (and counsel if named) before any response.

### Tone and timing rules
- Respond fast even before you can resolve — a same-day "I've got this, here's when you'll hear back" beats a perfect reply two days late.
- Never use "policy," "unfortunately," or "as per" in a recovery message; they read as defensive.
- Match the channel: public review → brief, warm public reply + a private channel to make it right (never negotiate money in public).
- One remedy, stated once. Re-negotiating erodes trust and invites gaming.

### Metrics worth tracking
Recovery rate (retained / total complained), repeat-complaint rate on the same root cause (should trend to zero after the fix), average first-response and resolution time, and goodwill cost as a % of complaint value. A rising repeat-complaint rate means the operational fix didn't stick — reopen it.
