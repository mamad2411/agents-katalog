---
name: ticket-deflector
description: >
  Reads a forwarded customer email or ticket, pulls order/refund status from
  Stripe and account history from Clarify, drafts a tone-matched reply in the
  owner's writing voice, and can issue a Stripe refund with explicit owner
  approval. Use when the user says "draft a response," "answer this customer,"
  "where's my order," or "I want a refund."
compatibility: "Requires Stripe, Clarify, Mail. Optional: Intercom."
---

# Ticket Deflector

## Quick start

Forward or paste a customer email — Claude pulls order status from Stripe, looks up the customer in Clarify, and drafts a reply in the owner's voice. If a refund is needed, it stages the details and waits for explicit approval before issuing anything.

```
User: "answer this customer" [forwards email]
→ Extract customer email + issue from thread
→ Pull Stripe transaction status
→ Pull Clarify contact history
→ Draft reply in owner's voice
→ Owner approves draft → send or stage
→ If refund needed: approval prompt → owner confirms → issue
```

## Workflow

1. **Read the customer message.** Accept a forwarded Gmail thread or pasted text. Extract: customer email address, name, order or transaction ID (if present), and the core issue — refund request, order status question, or general complaint. If multiple issues are present, address them in the order they appear.

2. **Pull order status from Stripe.** Search Stripe transactions by customer email or transaction ID. Capture: amount, date, status, and whether a refund has already been issued. If Stripe is not connected, note it in the draft and continue. If no transaction matches, flag it — do not guess at a match.
   - **Stripe rate limit:** If the customer provided a transaction ID, use it — single-record lookups avoid throttling entirely. If searching by email, use a 7-day window (not 30 days). Stripe's transaction list endpoint throttles aggressively on wide date-range queries; back-to-back tickets in the same session will hit this limit if the window is too broad.
   - If Intercom is connected, check for open support tickets from this customer.
   - If Stripe is connected, check Stripe transaction history as a secondary source.
   - If multiple transactions match, surface all of them and ask the owner which one applies before drafting.

3. **Pull customer history from Clarify.** Search contacts by email address. Pull: lifecycle stage, notes, open deals, and recent activity. If no contact exists, note it and offer to create one after the reply is sent — do not create during the response workflow.

4. **Draft the reply.** Write in the owner's writing voice. Adjust tone to fit the issue type:
   - Refund request → empathetic, clear, action-oriented
   - Order status question → factual, reassuring
   - General complaint → acknowledge, explain, offer resolution
   Flag any data gaps inline in the draft with a bracketed note (e.g., *[Note: No Stripe transaction found — verify order ID before sending]*) so the owner sees the gap before sending. For a worked example, see [reference/examples/respond-refund-request.md](reference/examples/respond-refund-request.md). For common pitfalls, see [reference/gotchas.md](reference/gotchas.md).

5. **Approval gate — owner reviews the draft.** Present the full draft. Do not send or stage it until the owner approves. The owner may edit freely before approving.

6. **Approval gate — refund issuance.** If a refund is warranted, surface a dedicated confirmation prompt after the owner approves the draft:

   > *"Issue refund of $[amount] to [customer name] ([email]) for transaction [ID]? Reply Y to proceed."*

   Wait for explicit confirmation. If the owner's reply is anything other than a clear yes, stop and ask what they'd like to do instead.

7. **Send or stage the reply.** After draft approval, ask the owner: send via Gmail now, or save as a draft? Execute their choice. Then log the interaction as a note on the Clarify contact timeline.

8. **Report.** One short paragraph: reply sent or staged, refund issued or not, Clarify note logged.

## Approval gates

- **Never issue a Stripe refund without explicit owner confirmation** — always show amount, customer name, email, and transaction ID before executing.

**Release Owner gate (high-stakes).** Before issuing the Stripe refund, present the exact content and the recipient or amount, then stop. Do not proceed until one named human approves with their initials and the date. Record the decision to the shared gate log: run `python3 "Taskade/_Shared Files/_gate-log/record_decision.py" --skill frontier-founder-smb:ticket-deflector --tier high-stakes --action "<summary>" --target "<recipient/amount/target>" --decision signed|stopped|overridden|edited --approver "<named human>" --requested-at <ISO-8601>` (one row per decision; never edit past rows). Roll up override rate and response time anytime with `override_report.py`. Never auto-approve, and never sign on the owner's behalf. Watch the override rate over time; a low override rate signals rubber-stamping.

- **Never send the reply without owner review.** Always present the full draft first.
- **Never create a Clarify contact during the response flow.** Offer it afterward.
- **Never auto-select a Stripe transaction.** If multiple match, surface them all and let the owner choose.
- **Never fabricate order details.** If Stripe has no record, say so inline in the draft — do not invent a status.

## Reference

- [reference/gotchas.md](reference/gotchas.md) — Good / Bad patterns for tone, Stripe lookup, and ambiguous refund scenarios
- [reference/examples/respond-refund-request.md](reference/examples/respond-refund-request.md) — worked example: refund request with Stripe transaction found
