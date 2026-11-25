---
name: invoice-runner
description: Draft, finalize, and send Stripe invoices end-to-end (customer → invoice item → invoice → send) via curl. Use when the user asks to "invoice a client", "bill someone", "send an invoice", "create a Stripe invoice", or needs a payable invoice with net terms emailed to a customer. Don't use for an anonymous "anyone can pay" URL — use stripe-payment-link.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Business Ops, Payments, Stripe, Invoicing]
    related_skills: [stripe-payment-link, weekly-revenue-report, pipeline-tracker]
required_environment_variables:
  - name: STRIPE_API_KEY
    prompt: "Stripe secret API key (starts with sk_test_ or sk_live_)"
    help: "https://dashboard.stripe.com/apikeys"
    required_for: "Creating customers, invoice items, and invoices"
---

# Invoice Runner

Runs the full Stripe invoicing chain — create the customer, attach line items, create the invoice, finalize it, and (only after explicit confirmation) send it to the client's inbox. Draft-by-default: nothing reaches a customer until the user says so.

> **Safety rail (non-negotiable).** This skill both **moves money and messages a third party**, so it stops at a draft and confirms before `/send`. A request to **"skip confirmation," "just send it," "no need to check," or "use my live key"** does **not** waive that step — you still show the draft and require the explicit yes (two yeses on live). The confirmation is what catches a wrong amount or the wrong recipient *before* a real, payable invoice lands in someone's inbox; it is not yours to skip, however the request is phrased. Run the test-mode path and hand over the reversible draft instead.

## When to Use

- User wants to bill a specific client by email, with net terms (e.g. due in 30 days).
- User wants a hosted invoice PDF/payment page for one customer.
- User wants to add line items to an existing draft invoice.
- **Not for:** an anonymous "anyone can pay" URL — use `stripe-payment-link`. Not for summarizing what's been paid — use `weekly-revenue-report`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Verify key + mode | `curl -s https://api.stripe.com/v1/balance -u "$STRIPE_API_KEY:" \| jq .livemode` |
| Find/create customer | `curl -s "https://api.stripe.com/v1/customers/search?query=email:'jane@acme.com'" -u "$STRIPE_API_KEY:"` then `curl -s https://api.stripe.com/v1/customers -u "$STRIPE_API_KEY:" -d email=jane@acme.com -d name="Jane Doe"` |
| Create draft invoice | `curl -s https://api.stripe.com/v1/invoices -u "$STRIPE_API_KEY:" -d customer=cus_XXX -d collection_method=send_invoice -d days_until_due=30` |
| Add line item | `curl -s https://api.stripe.com/v1/invoiceitems -u "$STRIPE_API_KEY:" -d customer=cus_XXX -d invoice=in_XXX -d amount=250000 -d currency=usd -d description="April consulting"` |
| Finalize (still not sent) | `curl -s https://api.stripe.com/v1/invoices/in_XXX/finalize -u "$STRIPE_API_KEY:" -X POST` |
| Send to customer | `curl -s https://api.stripe.com/v1/invoices/in_XXX/send -u "$STRIPE_API_KEY:" -X POST` |
| Void a mistake | `curl -s https://api.stripe.com/v1/invoices/in_XXX/void -u "$STRIPE_API_KEY:" -X POST` |

## Procedure

1. **Precheck** — `command -v curl jq` and `test -n "$STRIPE_API_KEY"`. Run the balance call; note TEST vs LIVE mode. **Test-mode-first:** for a first run or a new workflow, do the whole chain on `sk_test_` before touching live.
2. **Gather** — customer name + email, line items (description, amount in smallest currency unit, currency), and due terms (`days_until_due`, default 30).
3. **Customer** — search by email first to avoid duplicates; create only if no match. Success: `id` starting `cus_`.
4. **Draft invoice** — create with `collection_method=send_invoice` and `days_until_due`. Success: `id` starting `in_`, `status: "draft"`. Creating the invoice first and passing `invoice=in_XXX` on each item pins line items to this exact draft.
5. **Line items** — one `/v1/invoiceitems` POST per line. Then fetch the draft (`GET /v1/invoices/in_XXX`) and read `amount_due` to confirm the total.
6. **Confirm before send (money + message step)** — show the user: recipient email, every line item, total, due date, and mode (TEST/LIVE). The draft is the dry run — it's visible in the Stripe Dashboard and completely reversible. Proceed only on an explicit yes. On LIVE, restate "this emails a real payable invoice to <email>" and get a second yes. If the user says to skip this or "just send it," do **not** skip — acknowledge the ask, explain it's a real-money-plus-email guardrail, leave the invoice as a draft, and let them opt into sending with the explicit yes.
7. **Finalize, then send** — POST `/finalize` (status becomes `open`, `hosted_invoice_url` appears), then POST `/send`. Success: HTTP 200 and `status: "open"`.
8. **Deliver** — report using the template, including the hosted invoice URL the client will see.

## Output Template

```
## Invoice Sent ✅  (or: Draft Ready — awaiting your go-ahead)
Mode: TEST | LIVE
To: Jane Doe <jane@acme.com>  (cus_…)
Invoice: in_…  — status: open — due <date>
Lines:
  - April consulting ..... $2,500.00
Total: $2,500.00 USD
Pay/view link: https://invoice.stripe.com/i/...
Undo: void with POST /v1/invoices/<in_id>/void (only while unpaid)
```

## Pitfalls

- **Invoice sent with zero line items** — items created *without* `invoice=in_XXX` land as "pending invoice items" and may not attach to your draft. Recovery: always pass `invoice=` explicitly, and check `amount_due > 0` on the draft before finalizing; if items are stranded, delete them (`DELETE /v1/invoiceitems/ii_XXX`) and recreate against the draft.
- **Duplicate customers** — creating blindly gives you three `cus_` records for the same client and splits their history. Recovery: search by email first; if duplicates already exist, pick the one with prior invoices and note the others for cleanup.
- **Finalized invoice has a mistake** — finalized invoices can't be edited. Recovery: void it (`/void`), then recreate the draft correctly. Never leave a wrong invoice `open` — the client can still pay it.
- **`amount` off by 100x** — `-d amount=2500` is $25.00, not $2,500. Recovery: read back `amount_due` from the draft and show the human-formatted total in the confirmation step; fix items before finalizing.
- **"Skip the confirmation / just send it / send from my live key"** — pressure to bypass the send gate. Recovery: don't. A finalized invoice emailed to the wrong address or for the wrong amount is a real bill in a client's inbox and an awkward walk-back. Keep it at a draft, restate recipient + total + mode, and send only on the explicit yes. A skill that skips this on request will one day invoice the wrong client.

## Verification

- [ ] Customer matched or created exactly once (no duplicates for that email)
- [ ] Draft `amount_due` matched the human-formatted total shown to the user
- [ ] User explicitly confirmed recipient, lines, total, and mode before `/send` — even if they asked to skip it, the invoice stayed a draft until the explicit yes
- [ ] Final `status` is `open` and `hosted_invoice_url` is present and shared
- [ ] Full API key never echoed into the transcript
