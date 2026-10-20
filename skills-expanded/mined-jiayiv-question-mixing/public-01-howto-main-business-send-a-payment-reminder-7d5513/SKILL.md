---
name: send-a-payment-reminder
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 5min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Send a polite payment reminder for an unpaid invoice while preserving the customer relationship and keeping a record in the billing system.

## Preconditions

- The invoice exists and has not been paid, voided, or disputed.
- The customer email or billing contact is current.
- You know whether the invoice is upcoming, due today, or overdue.

## Steps

1. **Open the unpaid invoice.** Find the invoice by customer, invoice number, or unpaid status. → *Expect:* the invoice detail page shows an open balance.
2. **Check the payment status.** Confirm no payment, credit, refund, or dispute is pending. → *Expect:* the amount due is still accurate.
3. **Review the contact.** Confirm the reminder will go to the billing contact or accounts-payable address. → *Expect:* the recipient is the person responsible for payment.
4. **Choose a reminder template.** Use a short message that names the invoice number, amount, due date, and payment link. → *Expect:* the reminder text is specific and professional.
5. **Send the reminder.** ⚠️ *Irreversible:* sending contacts the customer, so confirm amount, recipient, and tone before clicking send. → *Expect:* the system records the reminder as sent.
6. **Schedule the next follow-up.** Add a reminder, task, or note for the next follow-up date if payment does not arrive. → *Expect:* there is a visible follow-up plan.

## Decision points

- Invoice is not yet due → use a friendly upcoming-due reminder.
- Invoice is overdue → include days overdue and the original due date.
- Customer has disputed the invoice → do not send a standard reminder; respond to the dispute first.
- Customer usually pays by check or bank transfer → include manual payment instructions, not only an online link.

## Failure modes & recovery

- **F1 Payment already arrived:** detect by a recent deposit, gateway status, or unapplied payment → recover by applying the payment and sending a receipt instead.
- **F2 Reminder sent to wrong contact:** detect by bounce, reply, or wrong email in the activity log → recover by updating the contact and resending with a brief correction.
- **F3 Customer disputes the balance:** detect by reply challenging amount or work delivered → recover by pausing collection and reconciling the invoice details.
- **F4 Payment link fails:** detect by customer report or failed link test → recover by sending alternate payment instructions.

## Verification

The invoice activity log shows a reminder sent to the correct billing contact for the current open balance, and a next follow-up date exists if payment remains unpaid.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks and Xero can send reminders from the invoice page or automated reminder settings; generic tools may call the action Remind, Send reminder, or Email customer.
- `us`: avoid language that sounds like a formal debt-collection notice unless you are following applicable collection rules.

## Safety & privacy

Medium risk because reminders can affect customer relationships and disclose billing details. Send only to authorized billing contacts and avoid including sensitive bank details beyond approved payment instructions.
