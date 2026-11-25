---
name: payments-and-money
description: Engineering money movement — payment integration, ledgers, reconciliation, refunds, billing, and the discipline that prevents losing or double-charging money. Use when integrating a payment gateway (Razorpay, Stripe, PayU, …), recording payments/credits/balances, building billing or subscriptions, handling refunds and disputes, or when the user says "payments", "billing", "checkout", "refund", "reconciliation", "ledger", or "wallet".
---

# Payments and Money

Money code has a property no other code has: its bugs convert directly into rupees, disputes, and audits — and they're discovered by customers and accountants, not by monitoring. The discipline is total paranoia dressed as engineering: **assume every network call fails after succeeding, every webhook arrives twice or never, and every balance you compute will one day be checked against someone else's records.**

## The invariants (violating any of these is an incident)

1. **Exact decimals only** — `NUMERIC`/integer-minor-units end to end: DB, API (string or integer, never JSON float), UI. One float sneaking into the pipeline poisons everything downstream (database-design).
2. **The server computes every amount.** Client-submitted prices, totals, or discounts are display hints to be re-derived and verified, never inputs to be charged. The classic exploit is editing the amount in the request.
3. **Append-only truth.** Every money movement is a new immutable record; corrections are compensating entries (refund, credit note, adjustment with reason), never UPDATEs to history. If the question "what did we believe on March 31?" can't be answered, the model is wrong.
4. **Balances are derived, not stored** — or if cached for speed, recomputable from the movement log and audited for drift on a schedule. A stored balance with no recomputation path is a rumor.
5. **One transaction per money operation**: invoice + line items + stock + ledger entries + payment record commit atomically or not at all — and no external API calls inside that DB transaction (system-design).

## Idempotency — the heart of payment correctness

The network failing *after* the charge succeeded is not an edge case; at volume it's a Tuesday.

- Every money-moving operation (charge, refund, payout, credit) carries a **client-generated idempotency key**, stored with a unique constraint: the retry returns the original result instead of moving money twice (api-contract-design).
- Same rule internally: the "record payment" service function must be safe against double-click, double-webhook, and job-retry — enforce with the constraint, not with a check-then-insert race (database-design concurrency rules).
- Every payment gets a **state machine** with legal transitions written down: `created → pending → succeeded | failed → (refund_pending → refunded)`. Illegal transitions rejected loudly. "It's in a weird state" means the state machine has undocumented states — fix the model.

## Gateway integration rules

- **The gateway is the source of truth for gateway events; your ledger is the source of truth for your business.** Never mark a payment succeeded from the client's redirect/callback alone (users close tabs; attackers forge redirects) — confirm server-side via signed webhook + verification API call.
- **Webhooks**: verify the signature, respond fast (enqueue, don't process inline), process idempotently (event IDs stored unique), tolerate out-of-order delivery (a `refunded` may arrive before you saw `succeeded` — reconcile against the API, don't assume sequence).
- **Reconciliation is not optional**: a scheduled job compares your records against the gateway's (their API/settlement reports) — every payment you have vs they have, amounts, statuses. Discrepancies alert a human. Webhooks WILL be missed; reconciliation is how you find out this week instead of at year-end audit. This single job is the difference between professional and amateur money handling.
- Store the gateway's IDs on your records (and your ID in their metadata) so every dispute/support case can be traced both directions in seconds.

## Refunds, partials, and disputes

- Refunds are new transactions referencing the original — with their own state machine, idempotency, and webhook handling. Partial refunds must be capped at (original − already refunded), enforced at the database level, under concurrency.
- Overpayment, underpayment, and payment-against-multiple-invoices are business decisions to spec explicitly (requirements-to-spec) — the allocation logic is where wholesaler/B2B systems earn their keep. Record allocations as first-class rows, not as mutated invoice fields.
- Disputes/chargebacks arrive months later: your records retention, evidence (what was delivered, when, agreed by whom), and audit trail are your defense. This is why append-only wasn't optional.

## Billing & subscriptions (if you charge for your own SaaS)

- Bill from your ledger of usage/entitlements, not from scattered flags. Trial, grace period, suspension, and cancellation are a tenant-lifecycle state machine (saas-multi-tenancy) — decide *in the spec* what happens to data and access at each stage.
- Proration, upgrades mid-cycle, and failed-renewal retries (dunning) are the edge cases that eat billing systems: spec them before building, and prefer the gateway's subscription engine over rebuilding it unless you have a real reason.
- Tax (GST etc.) correctness is a legal matter: rates and rounding rules verified by someone qualified, and stored per-line at transaction time (rates change; history must not).

## Testing money code (testing-strategy, doubled)

- Exhaustive units on the math: rounding at every boundary, zero, negative-guards, max values, allocation splits that don't sum, currency formatting.
- Integration tests against the gateway **sandbox** for the golden path, plus simulated chaos your code must survive: duplicate webhook, out-of-order webhook, timeout-after-success, and the two-tabs double-submit.
- Before launch: one end-to-end real-money transaction (smallest amount) through production, refunded — verified in your ledger, the gateway dashboard, AND the reconciliation job (release-readiness).
