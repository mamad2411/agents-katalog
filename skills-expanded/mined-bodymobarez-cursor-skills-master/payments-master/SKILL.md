---
name: payments-master
description: >-
  Master hub for Payments — accept money worldwide and across Africa at staff/principal depth.
  Build PCI-SAQ-A checkout and integrate every gateway/wallet behind one provider-agnostic adapter:
  global PSPs (Stripe, Adyen, PayPal, Checkout.com, Braintree, Razorpay, Mollie, Klarna, Paddle MoR),
  African gateways (Paystack, Flutterwave, Paymob, Fawry, Geidea, Interswitch, Ozow, Yoco, Wave,
  CinetPay), and mobile money/wallets (Apple/Google Pay, M-Pesa Daraja, MTN MoMo, Airtel/Orange
  Money), plus orchestration/failover, 3DS2/SCA, fraud, webhooks + idempotency, and double-entry
  reconciliation. Bundles 8 specialized skills (in skills/<name>/GUIDE.md). Use for any payments task.
---

# Payments — Master Hub

Build payment pages and integrate **gateways, wallets, and mobile money worldwide and across Africa**
— cards, wallets, bank transfers, vouchers, and mobile money — securely (PCI SAQ-A), reliably
(multi-gateway, idempotent, reconciled), and with high conversion.

## Non-negotiables (every payments task)

- **Money = integer minor units + currency**, always. Convert to each provider's wire format only
  inside its adapter (XOF/XAF are zero-decimal; Flutterwave/PayPal want major units; M-Pesa whole shillings).
- **Server is the source of truth for the amount** — never trust a client-sent price.
- **Idempotency keys** on every create/capture/refund; **dedupe webhooks** by provider event id.
- **Webhooks are the source of truth** (verify signature on raw body, ack fast, reduce idempotently) —
  not the client redirect.
- **Stay PCI SAQ-A**: PAN/CVV never touch your servers (hosted fields / redirect / tokenization).
- **Reconcile daily**: provider settlement ↔ payments ↔ double-entry ledger.

## How to use this hub

This single skill bundles **all 8 payments skills**; each one's full instructions live in
`skills/<name>/GUIDE.md`. Read on demand.

**Workflow:** 1) **payments-architecture** for the adapter layer, canonical model, Money, and state
machine. → 2) Pick gateways/wallets by market (global / africa / ewallets). → 3) Build the page with
**checkout-and-payment-pages**. → 4) Harden with **payment-orchestration-and-security**,
**payment-webhooks-and-idempotency**, and **reconciliation-and-ledger**.

## Route to the right skill

| You need to… | Skill |
|--------------|-------|
| Design the provider-agnostic layer, money, states, idempotency | **payments-architecture** ⭐ |
| Integrate Stripe/Adyen/PayPal/Checkout.com/Razorpay/Mollie/MoR | **global-payment-gateways** |
| Integrate Paystack/Flutterwave/Paymob/Fawry/Geidea/Ozow/Wave | **africa-payment-gateways** |
| Apple/Google Pay, M-Pesa STK, MTN MoMo, Airtel/Orange | **ewallets-and-mobile-money** |
| Build the checkout/pay page, 3DS2, saved cards, conversion | **checkout-and-payment-pages** |
| Routing/failover, retries/dunning, fraud, SCA, subs, disputes | **payment-orchestration-and-security** |
| Verify/dedupe/replay webhooks; request vs event idempotency | **payment-webhooks-and-idempotency** |
| Double-entry ledger + daily settlement reconciliation | **reconciliation-and-ledger** |

## Bundled skills

- **payments-architecture** ⭐ — Foundation: provider-agnostic adapter interface, canonical Payment
  model + state machine, integer minor-units Money with per-provider formatting, idempotency-key
  derivation, webhooks-as-truth, and PCI scope. → `skills/payments-architecture/GUIDE.md`
- **global-payment-gateways** — Worldwide PSPs with copy-paste code: Stripe PaymentIntents + Elements +
  webhook signing, Adyen `/payments` + HMAC, PayPal Orders v2 (decimal strings), Checkout.com,
  Braintree, Razorpay, Mollie, Klarna, merchant-of-record. → `skills/global-payment-gateways/GUIDE.md`
- **africa-payment-gateways** — Per-country PSPs: Paystack (HMAC-SHA512 + verify), Flutterwave (⚠ major
  units), Paymob (Intention API + HMAC), Fawry (signed + voucher), Geidea/Interswitch/Ozow/Yoco/Wave,
  with minor-unit & verification gotchas. → `skills/africa-payment-gateways/GUIDE.md`
- **ewallets-and-mobile-money** — Global wallets via your gateway + African mobile money: M-Pesa Daraja
  STK Push (full code + STK Query), MTN MoMo RequestToPay, Airtel/Orange/Wave, async PIN UX.
  → `skills/ewallets-and-mobile-money/GUIDE.md`
- **checkout-and-payment-pages** — High-converting, PCI-SAQ-A pages: hosted vs embedded (Stripe Payment
  Element/Adyen Drop-in), 3DS2/SCA, tokenization, localized methods, and the PCI v4.0.1 script rules.
  → `skills/checkout-and-payment-pages/GUIDE.md`
- **payment-orchestration-and-security** — Reliability + safety: multi-gateway routing/failover, decline
  classification + smart retries/dunning, fraud (3DS2/Radar/velocity), subscriptions/off-session MIT,
  refunds/disputes/chargebacks + ratio monitoring. → `skills/payment-orchestration-and-security/GUIDE.md`
- **payment-webhooks-and-idempotency** — The webhook backbone: per-provider signature verification, raw
  body, ack-fast, event-id dedupe, out-of-order/replay/dead-letter, request-key vs event dedupe.
  → `skills/payment-webhooks-and-idempotency/GUIDE.md`
- **reconciliation-and-ledger** — Money accuracy: append-only double-entry ledger (minor units),
  lifecycle posting rules, daily settlement reconciliation, break detection, marketplace payouts.
  → `skills/reconciliation-and-ledger/GUIDE.md`

## Pairs well with
`backend-api-master` (adding-stripe, stripe-best-practices; auth/MFA; integrations-pro webhooks),
`business-master` (accounting-finance ledger/GAAP), `marketplace-master` (split payments/payouts),
`ui-master` / `tailwind-master` (checkout UI).

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are
`GUIDE.md`, not `SKILL.md`) so only this master appears in the skills list. Read the relevant
`GUIDE.md` on demand.
