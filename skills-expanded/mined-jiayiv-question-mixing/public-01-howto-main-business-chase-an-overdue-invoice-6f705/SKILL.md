---
name: chase-an-overdue-invoice
domain: business
locale: [generic]
interface: mixed
difficulty: intermediate
est_time: 20min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Follow up on an overdue invoice with a structured escalation path that seeks payment, resolves blockers, and preserves evidence.

## Preconditions

- The invoice is overdue, unpaid, and not voided.
- You have the invoice, contract or quote, delivery evidence, reminder history, and customer contact details.
- You know who can approve payment on the customer side.

## Steps

1. **Review the account.** Open the customer record and confirm invoice number, amount due, due date, prior reminders, and payment history. → *Expect:* you know the exact overdue balance and timeline.
2. **Check for blockers.** Look for disputes, missing purchase order, wrong billing contact, failed payment link, or unapplied payment. → *Expect:* any nonpayment reason is identified or ruled out.
3. **Send a firm written follow-up.** State invoice number, amount, days overdue, payment link, and a specific response deadline. → *Expect:* the customer receives a clear request with next action.
4. **Call or message the right contact.** If no response, contact accounts payable or the buyer and ask what is needed to release payment. → *Expect:* you get a payment date, blocker, or escalation contact.
5. **Record every contact.** Log dates, names, promises to pay, disputes, and documents sent. → *Expect:* the customer record has a complete collection trail.
6. **Offer a controlled resolution.** [BRANCH: pay now | payment plan | dispute resolution] accept immediate payment, document a payment plan, or pause collection while resolving a valid dispute. → *Expect:* there is a concrete next step and owner.
7. **Escalate if needed.** Send final notice, suspend service if contract allows, or refer to owner, attorney, or collection agency after approval. ⚠️ *Irreversible:* formal escalation can damage the relationship and may create legal duties, so confirm approval and documentation first. → *Expect:* escalation status and approval are recorded.

## Decision points

- Customer says invoice was never received → resend and confirm the correct billing contact.
- Customer disputes the work → switch to dispute resolution and stop standard reminders.
- Customer promises payment by a date → calendar the date and follow up immediately if missed.
- Amount is small or customer is insolvent → consider write-off after approval.

## Failure modes & recovery

- **F1 Chasing wrong contact:** detect by no response or referral to accounts payable → recover by updating billing contact and resending.
- **F2 Payment already received:** detect by bank deposit, gateway status, or unapplied cash → recover by applying payment and apologizing for the reminder.
- **F3 Escalation without documentation:** detect by missing reminder and delivery history → recover by gathering evidence before final notice or collections.
- **F4 Relationship damage:** detect by angry response or buyer escalation → recover by acknowledging facts, pausing pressure, and resolving the blocker.

## Verification

The overdue invoice has a current collection note showing contact history, blocker status, next action date, responsible contact, and payment, payment plan, dispute path, escalation, or write-off recommendation.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks and Xero track invoice notes and reminders; generic tools may require CRM tasks or manual notes.
- `us`: third-party debt collection, late fees, and service suspension may be subject to contract and state rules.

## Safety & privacy

Medium risk because collection activity affects money, customer trust, and legal exposure. Keep tone factual, contact only appropriate business recipients, and avoid threats not supported by contract or law.
