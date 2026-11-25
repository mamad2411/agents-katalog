---
name: payment-systems
description: >
  Design payment and fintech systems. Use for payment flows, authorization and
  settlement, cards/Visa, ACH, SWIFT, UPI, QR and scan-to-pay, wallets, Apple
  Pay/Google Pay, money movement, reconciliation, avoiding double payment,
  idempotency and resiliency in payments, hotspots, FX, and e-commerce flows.
  Triggers: "payment system", "checkout", "reconciliation", "double payment",
  "settlement", "wallet", "UPI", "SWIFT", "fintech".
---

# Payment Systems

Correctness, idempotency, and auditability matter more than latency.

## When to use
- Designing checkout, payments, payouts, or wallet flows.
- Integrating a PSP or card network.
- Preventing duplicate/incorrect charges.
- Reconciliation and settlement design.

## Lifecycle of a card payment
1. **Authorization** (issuer approves, funds held).
2. **Capture** (merchant claims).
3. **Clearing / settlement** (net funds move between banks).
4. **Reconciliation** (records match across systems).
Visa/card networks sit between acquirer (merchant side) and issuer (bank).
Source: `...\how-does-visa-work-when-we-swipe-a-credit-card-at-a-merchant's-shop.md`.

## Core design rules
- **Idempotency keys** on every write → retries cannot double-charge.
- **Exactly-once effect** via idempotent state machine + dedup store.
- Immutable **ledger** (double-entry) as source of truth; never mutate balances
  in place without an audit trail.
- **State machine** for payment status (initiated → authorized → captured →
  settled → refunded/failed); reject invalid transitions.
- Timeouts + reconciliation jobs to resolve "unknown" states.
- Asynchronous settlement where possible; strongly consistent ledger.

## Rails & methods
| Method | Notes |
|---|---|
| Card (Visa/Mastercard) | Global; auth + capture + settlement |
| ACH | Bank transfers, US, batch, reversible |
| SWIFT | Cross-border messaging, not settlement itself |
| UPI / QR / scan-to-pay | Real-time account-to-account, high volume |
| Wallets (Apple/Google Pay) | Tokenized card credentials |
| Blockchain | Settlement/asset, new failure modes |

## Reliability & operations
- Retries with idempotency; circuit breakers around PSPs.
- Reconciliation (internal ledger vs PSP/bank) daily + real-time.
- Handle **hotspot accounts** (high-traffic merchant/account).
- Handle FX (rates, rounding, currency precision).
- PCI scope: never store PAN; tokenize; encrypt; audit.

## Checklist
- [ ] Idempotency for all payment writes.
- [ ] Double-entry ledger, immutable, auditable.
- [ ] Explicit state machine + invalid-transition guards.
- [ ] Timeout + reconciliation for unknown states.
- [ ] Retries safe; no duplicate charges.
- [ ] PCI scope minimized (tokenization).
- [ ] FX + rounding + currency handling defined.
- [ ] Daily reconciliation with PSP/bank.
- [ ] DR/backup for ledger; RPO near zero.

## Common pitfalls
- Retrying a charge without idempotency → double payment.
- Mutable balances without an audit trail.
- Ignoring "unknown" states after timeouts.
- Assuming the payment is final at authorization.
- Floating point for money (use integer minor units / decimal).

## References
- `...\payment-system.md`, `...\money-movement.md`, `...\the-payments-ecosystem.md`
- `...\how-does-visa-work-when-we-swipe-a-credit-card-at-a-merchant's-shop.md`, `...\how-does-visa-make-money.md`
- `...\how-does-ach-payment-work.md`, `...\swift-payment-messaging-system.md`, `...\unified-payments-interface-upi-in-india.md`
- `...\how-does-scan-to-pay-work.md`, `...\4-ways-of-qr-code-payment.md`
- `...\how-applegoogle-pay-works.md`, `...\digital-wallet-in-traditional-banks-vs-wallet-in-blockchain.md`
- `...\reconciliation-in-payment.md`, `...\how-to-avoid-double-payment.md`, `...\handling-hotspot-accounts.md`
- `...\foreign-exchange-payments.md`, `...\10-principles-for-building-resilient-payment-systems-by-shopify.md`
- `...\e-commerce-workflow.md`, `...\how-to-learn-payments.md`
Base: `D:\Agent-Assets\system-design-101\data\guides\`

## Related skills
`high-availability-and-resilience`, `distributed-systems`, `database-design`,
`messaging-and-streaming`.
