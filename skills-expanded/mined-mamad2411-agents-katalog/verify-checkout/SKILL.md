---
name: verify-checkout
description: Implement, test, audit, debug, and harden Verify Checkout hosted-deposit flows in merchant backends, websites, and apps. Use for deposit creation, hosted checkout redirects, return pages, API-key auth, idempotency, signed webhooks, polling, reconciliation, exactly-once fulfillment, and production readiness for checkout.verify.et. Do not use for direct Verify.et bank-verification API integrations.
license: MIT
metadata:
  author: Verify.et
  version: "1.0.0"
  category: integration
  tags:
    - checkout
    - payments
    - webhooks
    - idempotency
---

# Verify Checkout

Act as an API integration specialist inside the merchant's existing architecture. Preserve its framework, conventions, domain model, persistence, queues, validation, logging, and test style unless a change materially improves safety or correctness.

Verify Checkout is non-custodial: customers pay a merchant-owned receiving account; the platform hosts checkout and verifies the reference; the merchant owns order, wallet, and entitlement. Integrate only through the documented public API; never copy platform server internals into a merchant repo.

## Outcome

When asked to integrate Verify Checkout, make the integration work in the merchant's repository; do not stop at generic instructions. Implement the server adapter, local attempt mapping, checkout initiation, return/status flow, chosen completion mechanism, exactly-once fulfillment, env placeholders, and focused tests that fit the existing project. Leave only dashboard/secret actions that require the merchant, and state those actions precisely without asking them to paste secrets into chat.

## Workflow

1. Inspect the merchant product before editing. Identify storefront vs API, customer auth, order/wallet/subscription/entitlement model, env validation, idempotency, webhook raw-body handling, queues, logs, and tests.
2. Read [references/merchant-setup.md](references/merchant-setup.md). Confirm dashboard prerequisites: active receiving account, API key with `deposits:create` and usually `deposits:read`, and an **active** return origin matching `return_url`. For the recommended webhook path, the merchant also registers its public HTTPS receiver at `/dashboard/developers/webhooks`, copies the one-time `whsec_...` secret into server secret storage, and completes the activation test.
3. Map this product to one fulfillment shape: order completion, wallet top-up, or subscription/entitlement. Map deposit statuses to merchant-owned customer copy. See [references/merchant-product-ux.md](references/merchant-product-ux.md).
4. Confirm the current contract before material work. Prefer the live OpenAPI document, then current public guides. Never copy internal platform code or operational secrets into a merchant integration.
5. Read only the references needed beyond the setup guide:
   - [references/api-contract.md](references/api-contract.md) for endpoints, headers, payloads, statuses, envelopes, expiry, and credits.
   - [references/merchant-code-quality.md](references/merchant-code-quality.md) for a suggested module shape and optional TypeScript skeleton. Improve structure when it is cheap; do not restructure the merchant project to match it.
   - [references/merchant-product-ux.md](references/merchant-product-ux.md) for pay CTA, redirect, return page, polling UX, mobile, and expiry.
   - [references/integration-architecture.md](references/integration-architecture.md) for env, persistence, hosted redirect, fulfillment, polling, and reconciliation.
   - [references/webhooks.md](references/webhooks.md) for signature verification, delivery semantics, and secret rotation.
   - [references/debugging-and-testing.md](references/debugging-and-testing.md) for error triage, tests, production checks, and the live smoke test.
6. Fit the merchant's existing layout. Keep Verify Checkout HTTP server-side. Prefer one small client/adapter if that fits; otherwise reuse the project's HTTP helpers. Put the API key and webhook secret in the merchant's secret-management path; use `.env` only for local development and ensure it is ignored. If credentials are already configured, check only their presence and server-only wiring—never read, print, or echo their values.
7. Create a deposit with a stable `Idempotency-Key` minted once per local attempt. Prefer an opaque local payment-attempt ID or UUID (`checkout_<attempt-id>`); the contract accepts 1–256 characters. Persist the key before the remote call, persist `data.id` before redirecting, and return `data.checkout_url` only to a trusted client that navigates there. Do not rebuild the hosted payment form, collect the transfer reference in merchant UI, parse the checkout token, or infer payment from the return redirect.
8. Recommend signed webhooks plus polling/reconciliation for production. Webhooks update backend truth when the browser closes; client polling of the merchant backend keeps the return page responsive; reconciliation repairs gaps. If the merchant explicitly chooses polling-only, do not require a webhook secret, but implement bounded server-side polling/reconciliation and explain the latency/outage tradeoff. Use `GET /v1/deposits/{deposit_id}` as the authoritative remote lookup.
9. Fulfill only from authoritative `status: "succeeded"`. Make fulfillment exactly-once using the Verify Checkout deposit `id` as a unique key. Hold `review_required`; never credit `failed`, `expired`, or `cancelled`.
10. If the project already has tests, add focused coverage at the merchant boundary (request construction, idempotent retry, webhook signature, exactly-once fulfillment). Do not add a new test stack or a large suite the merchant did not ask for.
11. Finish with the smallest safe end-to-end check. Run [scripts/verify_checkout_smoke_test.mjs](scripts/verify_checkout_smoke_test.mjs) only after the user authorizes creating a real deposit and supplies safe test configuration through environment variables. Never invent, request in chat, print, or commit a secret. Report automated checks, untested live behavior, and the exact remaining dashboard/deployment steps.

## Preferred improvements

Improve structure when it is easy and matches the repo. Do not block integration on a refactor, new layers, or extra files. Details: [references/merchant-code-quality.md](references/merchant-code-quality.md).

- One server-side Verify Checkout helper instead of duplicated `fetch`, if that fits.
- Validate secrets at startup when the project already validates env.
- Keep money as decimal strings or the merchant's existing money type; avoid new float math.
- Unique `deposit_id` / idempotency / fulfillment keys when the database style already uses constraints.
- Map `error.code` to customer-safe copy rather than showing raw API `message`.
- No `NEXT_PUBLIC_`, `VITE_`, or other client-exposed prefixes for secrets.

## Non-negotiable invariants

- Never expose `vchk_...` or `whsec_...` values in browser/mobile code, public environment variables, URLs, logs, screenshots, fixtures, commits, or assistant output.
- Send `Authorization: Bearer ...`, pin `VerifyCheckout-Version: 2026-06-01`, and send an `Idempotency-Key` that is 1–256 characters and unique to the local attempt.
- On timeout or ambiguous create failure, retry the identical request with that same stored key. Mint a new key only for a genuinely new attempt (new pay after expiry, new order).
- Treat create `201` and idempotent replay `200` as success. Branch on stable `error.code`, respect `error.retryable`, and honor `Retry-After`.
- Before buffering a webhook, require `POST`, require `application/json`, and enforce a conservative request-body limit (256 KiB unless the public contract documents a larger payload). Then verify HMAC over the exact raw bytes before JSON parsing, enforce timestamp tolerance and constant-time comparison, and deduplicate by event ID rather than delivery attempt ID.
- Webhooks are at least once and may arrive out of order. Persist/accept quickly, process asynchronously when possible, and retrieve current deposit state when ordering matters.
- Do not let browser return parameters, webhook delivery order, `verification_status` alone, or `notification_status` determine fulfillment.
- Redact authorization headers, secrets, checkout tokens, full transaction references, and sensitive customer data. Log deposit ID, request ID, event ID, status, and stable error code.

## Source discipline

Current public sources:

- `https://checkoutapi.verify.et/openapi/public-api.json` — contract source of truth
- `https://checkout.verify.et/docs` — task-oriented guides
- `https://checkout.verify.et/docs/webhooks` — webhook setup and signing

If current sources disagree with this skill, follow the current OpenAPI/runtime contract and update the integration narrowly. Call out any incompatibility instead of guessing. Prefer OpenAPI over narrative docs when examples omit `error.type`/`retryable` or show `data: null` on errors.
