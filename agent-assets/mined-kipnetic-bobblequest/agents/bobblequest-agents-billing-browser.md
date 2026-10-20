# packages/billing-browser — AGENTS.md

Package: `@t/billing-browser`

## What this owns

The **browser-side billing implementation** of the `@t/billing` port. Wraps
`@revenuecat/purchases-js` to provide purchase UI, entitlement reads, and offering
resolution in web and desktop renderer contexts. No Stripe SDK, no Stripe Checkout — the
RevenueCat Web SDK is the only client-side billing surface.

## Layout

```
src/
├── index.ts
├── dependency-injection/
│   └── registerBillingBrowserDI.ts   ← composition root call
├── infrastructure/
│   ├── RevenueCatBrowserBilling.ts   ← primary impl (purchases-js ^1.36.0)
│   ├── NoOpBillingTracker.ts         ← safe stub for SSR / server components
│   └── init.ts                       ← Purchases.configure helper
└── react/
    └── index.ts                      ← React hooks / context (peer: react ^18||^19)
```

## DI registrar

File: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\packages\billing-browser\src\dependency-injection\registerBillingBrowserDI.ts

Call `registerBillingBrowserDI(container)` in the browser composition root (e.g., the
Next.js layout or Electron renderer entry point) before any component tree mounts. Binds
`RevenueCatBrowserBilling` under the same `BILLING_REPOSITORY` key defined in `@t/billing`
so consumers are provider-agnostic.

## Consumers

| Consumer       | Usage                                                                          |
| -------------- | ------------------------------------------------------------------------------ |
| `apps/web`     | RevenueCat Web SDK paywalls + purchase UI; `billing.entitlements.get` via tRPC |
| `apps/desktop` | RevenueCat Web Billing in the renderer; no separate Stripe flow                |

`apps/mobile` uses the RevenueCat React Native SDK — it does **not** import this package.
`apps/api` and `apps/website` have no browser billing surface.

## Conventions

**RevenueCat is the primary billing layer.** This package is the browser implementation of
that contract; it wraps `@revenuecat/purchases-js` and nothing else for purchase UI.

- Stripe is the **web payment processor behind RevenueCat only** — configured inside the
  RevenueCat dashboard. This package imports no Stripe SDK and exposes no Stripe surface.
- **Never expose Stripe IDs (customer, payment-intent, subscription) to the client.** The
  port returns RevenueCat-shaped `Entitlement[]` exclusively.
- RevenueCat's SDK handles the full purchase UX (paywalls, offerings, checkout). Do not
  build custom checkout flows backed by Stripe Checkout or any other processor.
- `NoOpBillingTracker` is the safe default for SSR paths and server components where
  `window` is unavailable — swap it for `RevenueCatBrowserBilling` only in client-side
  context.
- No `any`, no `@ts-ignore`, no type casts. No side-effects at module level (`sideEffects:
  false` in package.json) — keep the bundle tree-shakeable.
- React peer dependency is `^18 || ^19`; never import from `react` in non-`/react` exports.

## Links

- C:\Users\jager\OneDrive\Documents\GitHub\template-repo\docs\architecture\platform\billing.md
