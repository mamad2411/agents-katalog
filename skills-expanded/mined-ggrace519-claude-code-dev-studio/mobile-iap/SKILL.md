---
name: mobile-iap
description: Mobile in-app purchase specialist. Owns App Store / Play billing integration, receipts, server-side validation, restore, refund handling, subscription lifecycle, and family sharing. Auto-invoked for any IAP, subscription, or store-billing code.
---

# Mobile In-App Purchase

IAP failures are revenue holes that drain silently. Receipt validation, restore,
and the subscription state machine differ per store and punish shortcuts.

## When to reach for this

- Integrating StoreKit 2 (iOS) or Play Billing (Android) purchase flows
- Building server-side validation and entitlement grants from store transactions
- Handling App Store Server Notifications V2 or Play RTDN (real-time developer
  notifications) for subscription lifecycle
- Dealing with restore, refunds, family sharing, intro/promotional offers

## Principles

1. **Server-side validation, always.** Never trust client-reported receipts.
   StoreKit 2 transactions are JWS-signed — verify the signature chain server-side
   (or via the App Store Server API); on Android, verify purchases with the Play
   Developer API before granting anything.
2. **Entitlement state lives on the server.** Compute it from store
   notifications (ASSN V2 / RTDN) plus on-demand store lookups; the client only
   *displays* entitlement, never decides it.
3. **Idempotent grant.** Key grants on the original transaction ID — the same
   transaction delivered twice (retry, restore, notification + client race)
   grants exactly once.
4. **Restore is mandatory, not optional.** App Review rejects restorable
   purchases without a restore path; restore must map back to the original
   transaction and re-grant idempotently.
5. **Acknowledge / finish only after the grant is durable.** Play purchases not
   acknowledged within 3 days are auto-refunded; finishing a StoreKit
   transaction before the server grant persists loses the sale on a crash.
6. **Model the full lifecycle.** Trial → active → grace period → billing retry
   (account hold) → expired → refunded/revoked. Grace and billing-retry keep
   access; expiry and revocation remove it — get those two edges wrong and you
   either leak entitlement or punish paying users.
7. **Reconcile on a schedule.** Notifications get missed. A daily job comparing
   store subscription status against your entitlement DB catches drift before
   users (or finance) do.

## Lifecycle event → entitlement action

| Store signal | Entitlement action |
|---|---|
| purchase / `SUBSCRIBED` / initial transaction | grant by original transaction ID (idempotent) |
| `DID_RENEW` / `SUBSCRIPTION_RENEWED` | extend expiry; clear any retry state |
| grace period entered | keep access; surface fix-payment prompt |
| billing retry / account hold | per policy — typically revoke at hold, keep through grace |
| `EXPIRED` / `SUBSCRIPTION_EXPIRED` | revoke at expiry timestamp, not at notification arrival |
| `REFUND` / `SUBSCRIPTION_REVOKED` | revoke immediately; flag for abuse review if repeated |
| restore | look up original transaction; re-grant (no duplicate) |

A worked server-side flow (signed-transaction verification, idempotent grant,
notification handler, reconciliation job) is in
[`references/server-validation.md`](references/server-validation.md).

## Pitfalls

- Granting on the client purchase callback alone — refunds and family-sharing
  revocations never reach that code path
- Treating the sandbox/test environment as proof: test renewal compression,
  billing-retry, and refund flows explicitly per store
- Missing the unacknowledged-purchase auto-refund window on Play (3 days)
- Mapping entitlements off product ID alone and breaking when an upgraded /
  crossgraded subscription changes mid-period
- No handling for deferred (ask-to-buy) and pending purchase states — they
  arrive minutes-to-days after the buy button

---
*Related: `mobile-release` (store review, IAP rejection handling), `mobile-crash`
(purchase-flow stability) · domain agent: `mobile-architect` · output/ADR
format: `playbook-conventions`*
