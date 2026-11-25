---
name: revenuecat-setup
description: Set up a RevenueCat project from scratch, projects, apps, API keys, products, entitlements, offerings, and the official MCP server connection. Use when the user is configuring RevenueCat for a new or existing app.
---

# RevenueCat Project Setup

Order of operations: project, apps, keys, products, entitlements, offerings.
Dashboard: https://app.revenuecat.com

## Project and apps

One RevenueCat **project** per product; add one **app** per platform inside it
(App Store, Play Store, Amazon, Stripe, Web Billing, Roku). Each app needs its
store credentials:

- **iOS**: App Store Connect API key (In-App Purchase key) so RevenueCat can
  validate transactions and receive App Store Server Notifications.
- **Android**: Play service-account JSON with financial-data access, plus
  Play Developer Notifications routed to RevenueCat via Pub/Sub.

## API keys (know which kind you need)

- **Public SDK keys** (per app, prefixed like `appl_`, `goog_`): safe to ship
  in the client, used in `Purchases.configure`.
- **Secret v1 keys** (`sk_`): server-side REST v1 calls; never in a client.
- **API v2 secret keys**: project-scoped, used for the REST v2 API and the
  MCP server. Create read-only vs write-enabled variants deliberately.

Store secrets in your secret manager or environment, never in code or chat.

## Products, entitlements, offerings

Model access in three layers so store SKUs stay swappable:

1. **Products**: mirror the store SKUs (create the SKUs in App Store
   Connect / Play Console; attach them in RevenueCat).
2. **Entitlements**: what the user unlocks (for example `pro`). Attach every
   product that should unlock it, across all platforms. Client code checks
   entitlements only, never product IDs.
3. **Offerings and packages**: what the paywall displays. Keep a `default`
   offering (`$rc_monthly`, `$rc_annual` package types); switch offerings
   remotely for experiments without an app release.

## Official MCP server

This plugin ships RevenueCat's hosted MCP server: `https://mcp.revenuecat.ai/mcp`
(Streamable HTTP). Auth is OAuth (sign in when prompted) or a Bearer header
with an **API v2 secret key**. It manages project config in natural language:
apps, products, entitlements, offerings, packages, paywalls. Limits: it edits
RevenueCat configuration only; it does not create SKUs inside App Store
Connect or Play Console. Use a read-only v2 key if you only want inspection.

## Sandbox testing

- iOS: sandbox Apple ID or StoreKit configuration file; sandbox purchases
  show in the dashboard flagged as sandbox.
- Android: license testers on the Play track; test cards renew on
  accelerated schedules.
- Webhooks can be scoped to sandbox, production, or both; keep a separate
  endpoint or flag for sandbox events while developing.

## Checklist before shipping

- Entitlement attached to every product on every platform.
- Store server notifications (Apple and Google) connected, not just receipts.
- Public key in the app, secret keys only on servers.
- A `default` offering exists and the paywall reads packages from it.
