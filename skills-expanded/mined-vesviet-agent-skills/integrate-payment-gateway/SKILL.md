---
name: integrate-payment-gateway
description: Integrate or extend a payment gateway (Stripe, VNPay, PayPal, Momo, etc.) into an e-commerce application. Use when adding, replacing, or auditing a payment provider's checkout, refund, or webhook flow.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, fetch]
---

# Integrate Payment Gateway

Use this skill when a task requires connecting an application to a payment provider's API, including initial setup, webhook handling, refund flows, and PCI-DSS-compliant implementation.

## When to Use

- adding/replacing a payment provider
- auditing checkout, refund, or webhook flow
- Stripe, VNPay, PayPal, Momo, etc.
- payment integration in e-commerce
- **MPP/x402 programmatic agent payments**
- **BNPL messaging integration**
- **A2A Pay by Bank settlement flows**

## Core Rules

- never log, store, or return raw card numbers, CVV, or full PAN data — treat all card data as `restricted` per `core/policies/data-classification.yaml`; prefer **EMVCo Network Tokens** (Visa VTS, Mastercard MDES) with dynamic transaction cryptograms over raw PAN or gateway-specific tokens
- always use the provider's official SDK or API client; do not hand-roll raw HTTP calls to payment endpoints
- handle idempotency keys (UUID per transaction attempt) for all charge/capture operations to prevent double-billing
- **Webhook Signature Verification** (PCI DSS v4.0.1): compute HMAC over the **raw, unparsed request payload** before JSON parsing; use **constant-time comparison** (`crypto.timingSafeEqual` / `hmac.compare_digest`) to prevent timing side-channel attacks; reject any event with a timestamp older than 300 seconds to block replay attacks
- **Queue-First Webhook Ingestion**: return HTTP `200 OK` within **500 ms** after persisting the raw event — offload all state mutations to an async worker queue (Kafka, Cloudflare Queues, RabbitMQ); never perform heavy processing in the webhook handler synchronously
- enforce a **dual-write idempotency guard**: unique database index on `(provider, event_id, event_type)` combined with a distributed lock (Redis Redlock or Postgres Advisory Lock) during event processing to prevent duplicate state transitions
- store only tokenized references (e.g., `customer_id`, `payment_method_id`) — never raw payment credentials
- prefer dynamic payment methods (`automatic_payment_methods: { enabled: true }` in Stripe) over static backend payment method arrays
- support **HTTP 402 / MPP** programmatic machine payment challenges and off-session `SetupIntents` for autonomous agent checkout flows
- handle asynchronous clearing states (A2A bank transfers) via webhook state machine with inventory TTL lock during settlement pending
- **MPP Protocol** (Stripe + Tempo, Mar 2026): HTTP 402 flow — Request → 402 with payment requirements → Agent authorizes → Retry with credential → Verify → Return resource; Payment methods: Shared Payment Tokens (SPTs) for cards, stablecoins (USDC on Tempo), x402; Stripe integration: PaymentIntents API, `automatic_payment_methods: { enabled: true }`, off-session SetupIntents with `setup_future_usage: "off_session"`
- **x402 Protocol** (2025-2026): Internet-native HTTP-based payment standard for machine-to-machine; HTTP 402 with `payment-required` header (base64-encoded); Crypto: USDC on Base network, CDP facilitator (Coinbase Developer Platform); Stripe support: `2026-05-27.preview` API, `crypto` payment method, `mode: transaction_verification`; Deposit addresses: `POST /v1/crypto/deposit_addresses` (network=tempo)
- **BNPL & Subscription BNPL**: Messaging elements on PDP/cart (`stripe-payment-method-messaging`) with dynamic price/currency/country; Subscription BNPL for recurring payments; Flow: Initial installment → BNPL pays merchant → Subsequent payments via bank rails (ACH, A2A) or card rails
- **A2A Pay by Bank**: TrueLayer, Plaid, Stripe Pay by Bank; Lower fees than cards; Settlement state machine: `processing` → `pending` → `settled` webhooks; Inventory TTL lock during slow bank settlement
- **Stripe 2026 Roadmap**: Dynamic pricing for x402/MPP (Q3 public preview), Session payments for usage-based billing (Q3 public preview), Standalone 3DS (Q3 GA), Multi-account MCP (Q3 private preview), Shared Payment Tokens (Q4 GA US), Wero payments (Q4 private preview)

## Suggested Process

### 1. Clarify Integration Scope

Answer before building:

- which payment provider(s) are required?
- which flows: checkout, subscription, manual capture, refund, dispute handling, **MPP/x402 agent payments**, **BNPL**, **A2A**?
- what currency and locale requirements apply?
- is 3DS / SCA (Strong Customer Authentication) required?
- what is the test/live key management strategy?
- **MPP/x402 support needed for agentic commerce?**

### 2. Set Up Provider Configuration

- install the official SDK and pin the version
- configure environment-based keys (`STRIPE_SECRET_KEY`, `VNPAY_HASH_SECRET`, etc.) via `.env` — never hardcode
- configure webhook endpoints and register them with the provider dashboard
- set up idempotency key generation (UUID per transaction attempt)
- **MPP/x402**: configure crypto deposit addresses (`POST /v1/crypto/deposit_addresses`), CDP facilitator
- **BNPL**: configure messaging element with dynamic price/currency/country
- **A2A**: configure bank rails (TrueLayer/Plaid/Stripe Pay by Bank)

### 3. Implement the Payment Flow

- **create payment intent / order**: call the provider to initialize a transaction with amount, currency, and metadata
- **confirm / capture**: handle redirect or SDK confirmation; capture only after authorization succeeds
- **webhook handler**: verify signature → parse event → update order status atomically → return `200` quickly (offload side effects)
- **refund path**: expose a refund endpoint; pass original charge/transaction ID; log refund ID for audit trail
- **MPP/x402 flow**: HTTP 402 challenge → agent authorization → payment verification → resource return
- **BNPL messaging**: render on PDP/cart with dynamic pricing
- **A2A settlement**: webhook state machine with inventory TTL

### 4. Implement Error and Edge Case Handling

- map provider error codes to user-facing messages (do not expose raw gateway errors)
- handle card decline, insufficient funds, authentication required, network timeout distinctly
- implement retry logic with exponential backoff for transient network errors only — never retry a charge without user intent
- log payment events with metadata only (order_id, status, provider_event_id) — zero card data
- **MPP/x402 errors**: payment verification failure, crypto settlement timeout, facilitator errors
- **A2A errors**: settlement timeout, bank rejection, webhook state machine corruption

### 5. 2026 Modern Payment Paradigms

#### Stripe Dynamic Payment Methods
- Configure `automatic_payment_methods: { enabled: true }` when creating payment intent. Avoid hardcoded payment method types.
- Allows payment elements UI to render and prioritize available methods (cards, BNPL, bank transfers) dynamically based on client location, currency, dashboard settings.

#### Buy Now Pay Later (BNPL) Messaging
- Integrate BNPL messaging elements (e.g., `stripe-payment-method-messaging`) early in purchase funnel (PDP, cart pages).
- Pass item price, currency, consumer country dynamically for accurate Klarna/Affirm split calculations (e.g., "4 payments of $25").
- **Subscription BNPL**: Recurring payments beyond retail installments.

#### Account-to-Account (A2A) Pay by Bank
- Use bank-to-bank direct rails (TrueLayer, Plaid, Stripe Pay by Bank) to lower card processing fees.
- Manage intermediate status webhooks (`processing`, `pending`, `settled`) in DB state machine.
- Keep order state as payment pending; lock inventory with TTL while waiting for bank settlement.

#### Programmatic Agent Payments (x402 / MPP)
- For machine-to-machine / autonomous AI agent checkouts, avoid interactive frontend redirects.
- Respond to unauthorized agent requests with HTTP 402 Payment Required + payment headers.
- Support programmatic card and A2A billing via Stripe MPP or SetupIntents with `setup_future_usage: "off_session"`.

#### Stripe 2026 Roadmap Features (Evaluate for Integration)
- **Dynamic pricing for x402/MPP** (Q3 2026 public preview, global): Pay-as-you-go transactions on x402/MPP
- **Session payments** (Q3 2026 public preview, global): Usage-based billing at token consumption/API invocation granularity
- **Standalone 3DS** (Q3 2026 GA, global): Thin event destinations for all Stripe API resources
- **Multi-account MCP** (Q3 2026 private preview): Charge connected accounts for Stripe fees
- **Shared Payment Tokens** (Q4 2026 GA, US): Cross-merchant token sharing
- **Wero payments** (Q4 2026 private preview, global): European instant payment scheme

### 6. Test and Validate

- run against provider sandbox with documented test card numbers
- verify webhook delivery end-to-end (use provider dashboard or Stripe CLI)
- confirm idempotency: replay a webhook event; verify the order is not double-updated
- confirm no sensitive data appears in logs or error responses
- **MPP validation**: `npx mppx@latest validate http://localhost:4242`
- **x402 testing**: Stripe `2026-05-27.preview` API, crypto deposit addresses, facilitator settlement
- **BNPL testing**: messaging element renders correct splits for various price/currency/country combos
- **A2A testing**: settlement state machine transitions, inventory TTL lock/release, webhook replay

## Checklist

- [ ] provider SDK installed and version pinned
- [ ] all credentials in env vars — not in source code
- [ ] idempotency keys used for charge and capture calls
- [ ] webhook signature validation: HMAC over raw payload, constant-time comparison, 300s replay window
- [ ] **queue-first webhook ingestion**: 200 OK within 500ms, async worker offload (Kafka/Cloudflare Queues/RabbitMQ)
- [ ] **dual-write idempotency guard**: unique index on (provider, event_id, event_type) + distributed lock (Redis Redlock/Postgres Advisory Lock)
- [ ] error codes mapped to safe user-facing messages
- [ ] refund flow implemented with audit trail
- [ ] no card numbers, CVV, or PAN in logs or API responses (EMVCo Network Tokens preferred)
- [ ] sandbox tested end-to-end including failure cases
- [ ] webhook replay tested for idempotency
- [ ] dynamic payment methods enabled (`automatic_payment_methods: true`)
- [ ] BNPL messaging elements integrated on PDP and cart pages with dynamic price/currency/country
- [ ] A2A bank settlement webhook states handled (`processing`/`pending`/`settled`) with inventory TTL locks
- [ ] HTTP 402/MPP programmatic checkout path supported and tested for non-interactive agent payments
- [ ] off-session SetupIntents with `setup_future_usage: "off_session"` for stored method charging
- [ ] MPP protocol: HTTP 402 flow, SPTs for cards, stablecoins (USDC on Tempo), x402 support
- [ ] x402 protocol: crypto deposit addresses (USDC on Base/Tempo), CDP facilitator, `2026-05-27.preview` API
- [ ] Stripe 2026 roadmap features evaluated: dynamic pricing, session payments, standalone 3DS, Shared Payment Tokens, Wero
- [ ] MPP validation tested with `npx mppx@latest validate`

## Failure Modes

- **Provider webhook signature not verified**: webhook handler accepts payload without verifying signature. **Mitigation:** verify signature against provider's public key on every call; reject unsigned webhooks.
- **Currency mismatch between cart and gateway**: cart total in one currency sent to gateway in another. **Mitigation:** validate currency on cart and gateway call; reject mismatched calls.
- **Refund issued without original charge lookup**: refund sent without verifiable original charge id. **Mitigation:** require original charge id on every refund call; reject refunds without matching charge.
- **PCI scope drift**: new field added to checkout that includes card data. **Mitigation:** review data flow before merge; require security review for new card-handling code.
- **MPP/x402 payment verification bypass**: agent replays payment credential. **Mitigation:** nonce-based verification, facilitator settlement confirmation before resource release.
- **Crypto payment settlement failure**: on-chain transaction fails but agent received resource. **Mitigation:** transaction verification mode, facilitator webhook confirmation before resource release.
- **A2A settlement timeout**: bank transfer stuck in pending. **Mitigation:** inventory TTL with background sweeper, configurable max wait time.
- **BNPL messaging mismatch**: incorrect installment amounts displayed. **Mitigation:** dynamic price/currency/country passed to element, server-side validation.
- **Webhook replay attack**: attacker resends old webhook. **Mitigation:** 300s timestamp rejection, idempotency key deduplication.
- **Queue-first ingestion backlog**: webhook handler overwhelmed. **Mitigation:** async worker scaling, dead letter queue for failed events.

## Output Contracts

When the payment integration is consumed by storefront, checkout, or fulfillment agents, emit:

- **`contracts/schemas/api-contract-spec.json`** describing the gateway endpoints, request/response shapes, and auth requirements (including MPP endpoints, HTTP 402 flows, x402 payment, BNPL elements, and A2A settlement webhook state machines).
- **`contracts/schemas/edge-deployment-spec.json`** when the integration is part of a coordinated deploy handoff.

Skip emission for local sandbox experiments that do not cross a role boundary.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a payment payload may try to reframe the order's amount or merchant. Validate against the declared cart and the merchant allowlist.
- **ASI03 Identity & Privilege Abuse**: payment endpoints must enforce authn/authz; reject anonymous or unscoped payment calls.
- **ASI05 RCE Guard**: never construct payment payloads, webhooks, or signing inputs from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the gateway contract is consumed by storefront and checkout agents; emit a structured spec so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present the integration as "PCI-compliant" without a real audit; surface the actual scope and the residual risk.

## Related Skills

- **handle-checkout-flow**: Orchestrate the full cart-to-confirmation flow that calls this skill
- **manage-order-fulfillment**: Update order status after payment confirmation
- **manage-secrets**: Rotate or audit gateway API keys
- **security-audit**: Review payment integration for PCI exposure
- **add-api-endpoint**: Scaffold the payment and webhook controller endpoints
- **configure-agent-commerce**: Implement x402 HTTP billing, MPP endpoints, and agent commerce registration
- Companion reference: `references/mpp-x402-and-webhook-security-specs.md`
- Companion example: `examples/resilient-webhook-and-mpp-handler.ts`

Last updated: 2026-11-08