---
name: payment-platform
description: Use when designing or modifying payment, billing, checkout, subscription, refund, dispute, invoice, wallet, payout, payment-webhook, PCI, or provider integration flows such as Stripe, PayPal, Square, Adyen, bank transfer, Apple Pay, Google Pay, or marketplace payment routing.
category: payments
---

# Payment Platform

Use this local skill as the mandatory safety layer for all payment work. Provider-specific skills such as stripe-best-practices, stripe-integration, upgrade-stripe, paypal-integration, and payment-integration can be attached in addition to this skill.

## Activation evidence

Apply this skill when task or code mentions payment, billing, checkout, subscription, invoice, refund, dispute, chargeback, payout, wallet, payment method, card, PCI, Stripe, PayPal, Square, Adyen, Apple Pay, Google Pay, webhook payment events, customer portal, metered billing, pricing plan, tax, or marketplace fee.

## Operating rules

- Never log card data, CVV, raw payment method details, provider secrets, webhook signing secrets, or full tokens.
- Use provider-hosted or tokenized payment collection unless the project explicitly owns PCI scope.
- Treat webhook processing as the source of truth for irreversible state changes.
- Make payment webhooks idempotent using provider event id, domain id, and atomic state transition rules.
- Separate user-facing redirect success from backend payment confirmation.
- Handle duplicate webhook delivery, out-of-order delivery, retries, partial failure, network timeout, and provider API timeout.
- Use decimal-safe money representation. Do not use floating point for money.
- Persist currency, amount, provider, provider object ids, status, idempotency key, and audit trail.
- Refund, dispute, cancellation, proration, renewal, failed payment, and trial-ending flows must have explicit state transitions.
- Do not change production payment API versions without an upgrade plan, rollback strategy, and webhook compatibility review.

## Required coder output

Coder agents using this skill must document:

- Provider and product scope: checkout, billing, subscription, refund, payout, invoice, marketplace, or tax.
- Payment state machine before and after the change.
- Webhook events handled and idempotency strategy.
- Data model changes and migration/backfill impact.
- Security controls: secret handling, logging, PCI boundary, webhook signature validation.
- Dev verification evidence and unresolved provider sandbox limitations.

## Skill composition

- Attach stripe-best-practices and stripe-integration for Stripe implementation.
- Attach upgrade-stripe for Stripe API or SDK version upgrades.
- Attach paypal-integration for PayPal checkout, subscription, IPN, refund, or dispute work.
- Attach payment-integration for generic gateway work or multi-provider payment design.
- Attach customer-billing-ops or finance-billing-ops for operational billing workflows.
- Attach cost-optimization when cloud or provider cost is part of the payment/billing task.
- Attach notification-delivery when payment events trigger email, SMS, push, in-app, or webhook notifications.
