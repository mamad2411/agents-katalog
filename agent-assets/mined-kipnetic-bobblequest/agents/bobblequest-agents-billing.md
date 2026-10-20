# packages/billing — AGENTS.md

Package: `@t/billing`

## What this owns

The server-side billing **port** and its concrete implementations. This package defines the
abstract `BillingRepository` contract and ships the infrastructure adapters (RevenueCat,
Stripe, Composite) that fulfill it. No app imports a provider SDK directly — all billing
calls go through the port.

## Layout

```
src/
├── index.ts
├── dependency-injection/
│   ├── index.ts
│   └── registerBillingDI.ts       ← composition root call
├── entities/
│   ├── ports/
│   │   └── BillingRepository.ts   ← abstract port (only symbol apps touch)
│   ├── schemas/
│   │   ├── CustomerSchema.ts
│   │   ├── EntitlementSchema.ts
│   │   ├── SubscriptionSchema.ts
│   │   └── WebhookEventSchema.ts
│   └── types/
│       └── BillingSource.ts       ← "stripe" | "revenuecat"
├── infrastructure/
│   ├── RevenueCatBillingImpl.ts   ← primary impl (REST via fetch)
│   ├── StripeBillingImpl.ts       ← web-rail impl (scaffold, retire to RC-only)
│   ├── CompositeBillingImpl.ts    ← routes by BillingSource; collapses once RC-primary
│   ├── errors.ts                  ← BillingWebhookSignatureError, BillingProviderError
│   └── webhookVerifier.ts         ← verifyStripeWebhook, verifyRevenueCatWebhook
└── ports/
    └── BillingTracker.ts
tests/
├── fixtures/                      ← RevenueCat JSON fixtures
├── infrastructure/                ← 4 test files
└── schemas/                       ← 3 test files
```

## DI registrar

File: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\packages\billing\src\dependency-injection\registerBillingDI.ts

Call `registerBillingDI(container)` in `apps/api/src/index.ts` after `config` + `logging`
are registered. Binds `CompositeBillingImpl` under
`dependencyKeys.global.BILLING_REPOSITORY` (re-exported as `BILLING_REPOSITORY_DEPENDENCY_KEY`
from `@t/billing`).

## Consumers

| Consumer       | Usage                                                                   |
| -------------- | ----------------------------------------------------------------------- |
| `apps/api`     | Webhook handler + tRPC billing router; calls port, never provider SDK   |
| `apps/web`     | tRPC `billing.entitlements.get` for server-side feature-gate RSCs       |
| `apps/desktop` | Same tRPC call as web; no Stripe Checkout, no `shell.openExternal`      |
| `apps/mobile`  | tRPC `billing.entitlements.get` after RevenueCat on-device purchase     |
| `apps/website` | No billing (marketing only)                                             |

## Conventions

**RevenueCat is the primary billing layer across every app (web, mobile, desktop).** All
purchase UI, subscription state, and entitlement checks route through RevenueCat SDKs on the
client; RevenueCat webhooks are the server-side source of truth.

- Stripe is the **web payment processor behind RevenueCat only** — configured inside the
  RevenueCat dashboard, never surfaced to app code. No `@stripe/stripe-js`, no Stripe Checkout,
  no Stripe Customer Portal in any app.
- The port always returns **RevenueCat-shaped `Entitlement[]`**. Stripe-specific fields are
  translated inside `StripeBillingImpl` before they reach the port boundary.
- **Never expose Stripe IDs (customer, payment-intent, subscription) to any client.** They are
  internal to RevenueCat's web-rail configuration.
- `StripeBillingImpl` and `CompositeBillingImpl` are scaffold artifacts pending retirement once
  RevenueCat-primary is fully wired. All consumers already bind to the single
  `BILLING_REPOSITORY` DI key — the impl collapse is transparent to them.
- Webhook routes require raw-body access for signature verification; keep them outside the tRPC
  router.
- No `any`, no `@ts-ignore`, no type casts. Branded types for IDs. Domain errors use typed
  classes from `errors.ts`.

## Links

- C:\Users\jager\OneDrive\Documents\GitHub\template-repo\docs\architecture\platform\billing.md
