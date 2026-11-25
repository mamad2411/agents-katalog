---
name: payment-reconciliation
description: Matches Stripe charges and payouts against a local invoices CSV, flagging mismatched amounts, unexpected fees, refunds, and orphan payments — strictly read-only on Stripe. Use when the user says "reconcile payments", "does Stripe match my invoices", "where's the missing money", "check my payouts", or before bookkeeping/tax prep. Don't use for creating payment links — use stripe-payment-link — or for issuing invoices — use invoice-runner.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Business Ops, Payments, Stripe, Reconciliation]
    related_skills: [stripe-payment-link, invoice-runner, weekly-revenue-report]
required_environment_variables:
  - name: STRIPE_API_KEY
    prompt: "Stripe secret API key (starts with sk_test_ or sk_live_)"
    help: "https://dashboard.stripe.com/apikeys"
    required_for: "Read-only listing of charges, refunds, and payouts"
---

# Payment Reconciliation

Answers the question every operator eventually asks at midnight: "does the money in Stripe actually match what I invoiced?" Pulls charges and payouts from Stripe with **GET requests only — this skill never creates, modifies, or refunds anything** — and matches them against a local `invoices.csv` with python3. Output: matched, mismatched, refunded, and orphaned, with fee totals made visible.

## When to Use

- Monthly close, tax prep, or "my bank deposit doesn't match my revenue" confusion.
- User asks to reconcile, audit payments, or find an unpaid/double-paid invoice.
- **Not for:** collecting money (`stripe-payment-link`), issuing invoices (`invoice-runner`), or trend reporting (`weekly-revenue-report`). Never for issuing refunds — that's a human action in the Stripe dashboard.

## Quick Reference

| Action | Command / Call |
|---|---|
| Verify key (read-only) | `curl -s https://api.stripe.com/v1/balance -u "$STRIPE_API_KEY:" \| jq .livemode` |
| List charges (paginate) | `curl -s -G https://api.stripe.com/v1/charges -u "$STRIPE_API_KEY:" -d limit=100 -d "created[gte]=$(date -v-30d +%s 2>/dev/null \|\| date -d '30 days ago' +%s)" > charges.json` |
| List payouts | `curl -s -G https://api.stripe.com/v1/payouts -u "$STRIPE_API_KEY:" -d limit=100 > payouts.json` |
| Fee per charge | `balance_transactions` object: `curl -s https://api.stripe.com/v1/balance_transactions/txn_XXX -u "$STRIPE_API_KEY:" \| jq '.fee'` |
| Expected invoices header | `invoice_id,client,amount,currency,date,status` |
| Match script | python3 stdlib (Procedure step 4) |

## Procedure

1. **Precheck** — confirm `STRIPE_API_KEY` is set and `curl`, `jq`, `python3` exist. Run the balance call; note `livemode`. Confirm `invoices.csv` exists with the expected header (`head -2 invoices.csv`). Missing either input: report and stop.
2. **Read-only rail** — state it before pulling data: every Stripe call in this run is a GET/list. If any step seems to need a POST to Stripe (refund, update, capture), that is out of scope — flag it for the human instead.
3. **Pull Stripe data** — fetch charges for the reconciliation window (default 30 days; ask if unclear) into `charges.json`, and payouts into `payouts.json`. If `has_more: true`, paginate with `-d starting_after=<last_id>` until complete — a partial pull produces false "missing payment" flags.
4. **Match** — run:

   ```bash
   python3 - <<'EOF'
   import csv, json
   charges = [c for c in json.load(open('charges.json'))['data'] if c['paid']]
   invoices = list(csv.DictReader(open('invoices.csv')))
   used = set()
   for inv in invoices:
       amt = round(float(inv['amount']) * 100)
       hit = next((c for c in charges if c['id'] not in used
                   and c['amount'] == amt and c['currency'] == inv['currency'].lower()), None)
       if hit:
           used.add(hit['id'])
           tag = 'REFUNDED' if hit.get('amount_refunded', 0) > 0 else 'MATCHED'
           print(f"{tag}\t{inv['invoice_id']}\t{inv['client']}\t{inv['amount']}\t{hit['id']}")
       else:
           print(f"UNPAID?\t{inv['invoice_id']}\t{inv['client']}\t{inv['amount']}\t-")
   for c in charges:
       if c['id'] not in used:
           print(f"ORPHAN\t-\t{c.get('billing_details',{}).get('name','?')}\t{c['amount']/100}\t{c['id']}")
   EOF
   ```

   Success: every invoice and every charge appears in exactly one line. Amount matching is exact by design — near-misses surface as UNPAID? + ORPHAN pairs for human judgment.
5. **Fees + payouts** — sum `fee` from balance transactions for matched charges; compare gross − fees against payout totals in `payouts.json`. The classic mystery — "Stripe says $2,000, bank got $1,941" — is usually just fees; show the arithmetic.
6. **Deliver** — fill the template. Every UNPAID?, ORPHAN, and REFUNDED line gets a suggested next action for the human (chase, match manually, or verify the refund was intended). The agent suggests; the human acts.

## Output Template

```
# Payment Reconciliation — {window} ({TEST|LIVE} mode)

Invoices: {n} · Matched: {n} · Refunded: {n} · Unpaid?: {n} · Orphan charges: {n}

## ✅ Matched ({n}) — gross ${x} · fees ${y} · net ${z}
| Invoice | Client | Amount | Charge |
## 🔻 Refunded — verify intended
## ❓ Unpaid? — invoice with no matching charge → chase or match manually
## 👻 Orphans — charge with no invoice → who paid you, and for what?

## Payout check
Gross ${x} − fees ${y} = ${z} expected · payouts listed: ${w} · {reconciles ✅ / gap ${d} ⚠️}

All Stripe access this run: read-only. No refunds, no changes.
```

## Pitfalls

- **Cents vs. dollars mismatch** — Stripe amounts are in the smallest unit; a $150 invoice must compare against `15000`. Recovery: the script multiplies invoice amounts by 100 — but zero-decimal currencies (JPY, KRW) must NOT be multiplied; check currency before trusting an UNPAID? flag.
- **Pagination skipped** — `limit=100` with `has_more: true` silently drops older charges, generating phantom unpaid invoices. Recovery: loop `starting_after` until `has_more: false`; verify `jq '.data | length'` totals look plausible for the window.
- **Same amount, two clients** — two $500 invoices and the greedy matcher pairs them to the wrong charges. Recovery: cross-check `billing_details.name`/receipt email on matched pairs; flag ambiguous same-amount matches for human confirmation rather than asserting them.
- **Timezone edge charges** — a charge at 23:50 UTC lands outside the local-date window. Recovery: pad the `created[gte]` window by one day each side and de-duplicate against the previous reconciliation.
- **Key echoed in output** — never print `$STRIPE_API_KEY`; if debugging auth, show only the first 8 chars.

## Verification

- [ ] Every Stripe call in the transcript is a GET/list — zero write calls
- [ ] Invoice count + orphan count equals lines in the match output; nothing dropped
- [ ] Pagination completed (`has_more: false` on final pages)
- [ ] Fee arithmetic shown; payout gap either reconciles or is flagged with the exact delta
- [ ] Full API key never appears in the transcript
