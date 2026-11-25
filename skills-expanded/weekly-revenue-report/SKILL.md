---
name: weekly-revenue-report
description: Scheduled Monday-morning revenue digest — pulls Stripe balance and the last 7 days of charges via curl, aggregates with jq, and delivers a plain-language weekly report. Use when the user asks for a "revenue report", "how much did we make this week", "Monday digest", "weekly Stripe summary", or wants revenue reporting automated on a schedule. Don't use for creating charges or links (stripe-payment-link), sending invoices (invoice-runner), or forecasting open deals (pipeline-tracker).
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Business Ops, Payments, Stripe, Reporting, Automation]
    related_skills: [stripe-payment-link, invoice-runner, pipeline-tracker]
    blueprint:
      schedule: "0 9 * * 1"
      prompt: "Compile the weekly revenue report"
required_environment_variables:
  - name: STRIPE_API_KEY
    prompt: "Stripe secret API key (starts with sk_test_ or sk_live_)"
    help: "https://dashboard.stripe.com/apikeys"
    required_for: "Reading balance and charge history"
---

# Weekly Revenue Report

A blueprint skill: every Monday at 09:00 it compiles a one-screen revenue digest — current Stripe balance, last week's gross/refunds/net, charge count, top payments, and failures worth chasing. Strictly read-only: it only ever GETs from Stripe, never creates or mutates anything, so it's safe to run unattended.

## When to Use

- The Monday scheduled run (automatic via the blueprint above).
- User asks ad-hoc: "run the revenue report", "how did last week go?"
- **Not for:** creating charges or links (`stripe-payment-link`), sending invoices (`invoice-runner`), or forecasting open deals (`pipeline-tracker` covers pipeline, this covers cash that actually moved).

## Quick Reference

| Action | Command / Call |
|---|---|
| Balance | `curl -s https://api.stripe.com/v1/balance -u "$STRIPE_API_KEY:"` |
| Week window (epoch) | `SINCE=$(python3 -c "import time; print(int(time.time())-7*86400)")` |
| Charges (last 7d) | `curl -s -G https://api.stripe.com/v1/charges -u "$STRIPE_API_KEY:" -d limit=100 -d "created[gte]=$SINCE"` |
| Next page | append `-d starting_after=<last charge id>` while `.has_more == true` |
| Aggregate | `jq '[.data[] \| select(.paid and .status=="succeeded")] \| {count: length, gross: (map(.amount) \| add // 0), refunded: (map(.amount_refunded) \| add // 0)}'` |
| Failures | `jq '[.data[] \| select(.status=="failed")] \| length'` |

## Procedure

1. **Precheck** — `command -v curl jq python3`; `test -n "$STRIPE_API_KEY"`. Hit `/v1/balance`; note `livemode` (a `sk_test_` key means the report covers test data — say so in the header). If the key is missing or rejected, deliver a short failure note instead of an empty report.
2. **Balance snapshot** — from the balance response, capture `available` and `pending` amounts per currency. These are in the smallest currency unit; divide by 100 for display (except zero-decimal currencies like JPY).
3. **Pull the week's charges** — compute `SINCE`, fetch `/v1/charges` with `created[gte]=$SINCE`, `limit=100`. If `has_more` is true, paginate with `starting_after` until false, concatenating `.data` arrays (`jq -s '[.[].data[]] '` across saved pages).
4. **Aggregate** — with jq compute: succeeded count, gross volume, total refunded, net (gross − refunded), failed count, and the top 3 charges by amount (`sort_by(-.amount) | .[:3] | map({amount, description, receipt_email})`).
5. **Compare** — if last week's report figures are available in memory/notes, compute week-over-week deltas; otherwise mark WoW as "first run — no baseline".
6. **Deliver** — fill the template and send it through the run's normal delivery channel. Read-only means no confirmation gate is needed — but if this skill is ever edited to write to Stripe, it must gain a confirm step per the authoring standard.

## Output Template

```
# Weekly Revenue Report — week ending <date>
Mode: LIVE | TEST (test data — not real revenue)

## Cash position
Available: $X,XXX.XX | Pending: $X,XXX.XX  (per currency if multiple)

## Last 7 days
Gross: $X,XXX.XX across N charges
Refunds: -$XXX.XX | Net: $X,XXX.XX
Failed charges: N  <- follow up if > 0
WoW: net +/-X% (or "first run — no baseline")

## Top payments
1. $XXX — <description> — <customer email>

## Action items
- <e.g., 3 failed charges to retry; refund spike worth a look; nothing — clean week>
```

## Pitfalls

- **Only the first 100 charges counted** — a good week overflows one page and the report silently under-reports. Recovery: always loop on `has_more`/`starting_after`; sanity-check that reported count isn't exactly 100 (a strong pagination-bug smell).
- **Cents vs dollars** — Stripe amounts are in the smallest unit; `amount: 15000` is $150.00. Recovery: divide by 100 at display time only (keep math in integer cents), and skip the division for zero-decimal currencies.
- **Refunds double-counted or missed** — refunded charges still appear with `status=="succeeded"`; their `amount_refunded` field carries the refund. Recovery: sum `amount` for gross and `amount_refunded` separately, report net = gross − refunded; don't filter refunded charges out.
- **Test key masquerading as revenue** — a `sk_test_` key produces a confident report of fake money. Recovery: the `livemode` check in step 1 is mandatory; stamp TEST prominently in the header when false.
- **Scheduled run fails silently** — expired key or network error yields no Monday report and nobody notices. Recovery: on any API failure, still deliver a message ("report failed: <reason>, fix: rotate key at dashboard.stripe.com/apikeys") so absence is never ambiguous.

## Verification

- [ ] Pagination exhausted (`has_more: false` on the final page)
- [ ] Net = gross − refunds; totals spot-checked against 2 raw charge objects
- [ ] All displayed amounts converted from cents correctly (currency-aware)
- [ ] LIVE/TEST mode stated in the report header
- [ ] Report delivered even on failure (with the reason), never silently skipped
- [ ] No API key or full customer card data echoed anywhere
