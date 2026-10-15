---
name: apple-storekit
description: "Implement in-app purchases, subscriptions, and entitlements on Apple platforms with StoreKit 2 (and the SwiftUI StoreKit views). Covers product loading (Product, Products.for), the purchase flow (purchase(), PurchaseResult, options), transaction verification (VerificationResult, Transaction.updates, currentEntitlements, finish()), entitlement/unlock gating, subscriptions (auto-renewable, SubscriptionInfo, RenewalState, status, grace period, billing retry), offers (intro/promo/win-back, offer codes), restoring purchases (AppStore.sync), refunds (beginRefundRequest), the SwiftUI views (StoreView, SubscriptionStoreView, ProductView, .storeProductsTask), App Store Server Notifications V2 / Server API and signed JWS transactions, and StoreKit testing (.storekit config files, StoreKitTest, sandbox). Use when building a paywall, unlocking premium features, adding a subscription tier, restoring purchases, validating receipts/transactions server-side, or testing IAP. Does NOT cover SwiftUI layout (use swiftui-expert-skill), notifications/App Intents (use apple-notifications-appintents), or general backend infra."
---

# Apple StoreKit (In-App Purchase & Subscriptions)

Guide for selling and unlocking content with **StoreKit 2** on iOS, iPadOS,
macOS, tvOS, watchOS, and visionOS. StoreKit 2 is Swift-native, async/await
based, and replaces the legacy `SKPaymentQueue` API for all new work.

## Contents

- [StoreKit 2 vs Legacy (Use 2)](#storekit-2-vs-legacy-use-2)
- [Product Types Router](#product-types-router)
- [The Five Things Every IAP App Must Do](#the-five-things-every-iap-app-must-do)
- [Loading Products](#loading-products)
- [Purchasing](#purchasing)
- [Verification (Never Trust Unverified)](#verification-never-trust-unverified)
- [Entitlements & Gating](#entitlements--gating)
- [Transaction Updates Listener (Required)](#transaction-updates-listener-required)
- [Subscriptions](#subscriptions)
- [Restoring Purchases](#restoring-purchases)
- [SwiftUI StoreKit Views](#swiftui-storekit-views)
- [Server-Side Validation](#server-side-validation)
- [Testing](#testing)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## StoreKit 2 vs Legacy (Use 2)

**Use StoreKit 2** (`Product`, `Transaction`, async/await) for everything new. It
gives you cryptographically signed, already-verified transactions (JWS), simple
entitlement queries, and no manual receipt parsing.

Only touch the legacy `SKPaymentQueue` / `SKProduct` API when maintaining code
that must run on iOS 14 or earlier. Do not mix the two transaction systems for
the same product.

This skill is StoreKit 2 throughout.

## Product Types Router

| You want to sell... | Product type | Key trait |
|---|---|---|
| A permanent unlock (remove ads, "pro" forever) | **Non-consumable** | Bought once, restorable forever |
| Currency/credits/lives that get used up | **Consumable** | Not restorable; you track balance |
| A recurring subscription that auto-renews | **Auto-renewable subscription** | Renewal state, grace period, offers |
| A fixed-duration pass that does **not** auto-renew | **Non-renewing subscription** | You manage expiry yourself |

Rules:
- Non-consumables and auto-renewable subs appear in `Transaction.currentEntitlements`.
- Consumables do **not** stay in entitlements - finish them and credit the user's
  balance in your own storage (ideally server-validated).
- Non-renewing subscriptions have no system-tracked expiry; you persist it.

## The Five Things Every IAP App Must Do

1. **Load products** from the App Store (`Product.products(for:)`).
2. **Start a `Transaction.updates` listener at launch** - before any UI - so you
   never miss Ask-to-Buy approvals, renewals, refunds, or cross-device purchases.
3. **Verify** every transaction (`VerificationResult` -> `.verified`).
4. **Grant entitlement** from `Transaction.currentEntitlements` (source of truth),
   not from the purchase return value alone.
5. **`finish()`** every verified transaction after delivering the content.

Miss any of these and you get the classic bugs: stuck "pending" purchases,
purchases that don't restore, double-charges, or content that never unlocks.

## Loading Products

```swift
import StoreKit

let ids: Set<String> = ["com.example.pro.lifetime", "com.example.pro.yearly"]
let products = try await Product.products(for: ids)   // network call; can throw

for product in products {
    print(product.id, product.displayName, product.displayPrice)  // localized price string
}
```

Rules:
- Product IDs must match App Store Connect exactly. An unknown/unapproved ID is
  silently omitted from the result (not an error) - check for missing ones.
- Use `product.displayPrice` (already localized + currency-formatted). Never
  build your own price string from `product.price` + a hardcoded symbol.
- Cache the loaded `Product` objects; you need them to call `purchase()`.
- Loading can fail (offline, App Store down) - show a retry, not a dead paywall.

## Purchasing

```swift
func buy(_ product: Product) async throws -> Bool {
    let result = try await product.purchase()
    switch result {
    case .success(let verification):
        let transaction = try checkVerified(verification)   // see Verification
        await grantEntitlement(for: transaction)
        await transaction.finish()
        return true
    case .pending:
        // Ask-to-Buy / SCA / parental approval. Do NOT show success.
        // The updates listener delivers it later.
        return false
    case .userCancelled:
        return false
    @unknown default:
        return false
    }
}
```

Rules:
- Handle **all four** cases. `.pending` is not failure - it resolves later via the
  listener, so never show a success state for it.
- On macOS/visionOS pass `purchaseOptions` as needed; on visionOS/SwiftUI you can
  also drive purchases through the StoreKit views.
- Pass `Product.PurchaseOption` for app account tokens (`appAccountToken`),
  quantity (consumables), promotional offers, or simulating Ask-to-Buy in tests.

## Verification (Never Trust Unverified)

Every transaction and renewal info comes wrapped in `VerificationResult`. The
payload is a signed JWS the system checks for you - but you must still branch on
the result and reject `.unverified`.

```swift
enum StoreError: Error { case failedVerification }

func checkVerified<T>(_ result: VerificationResult<T>) throws -> T {
    switch result {
    case .unverified:
        throw StoreError.failedVerification   // tampered / failed signature
    case .verified(let safe):
        return safe
    }
}
```

Never grant entitlement from an `.unverified` result.

## Entitlements & Gating

`Transaction.currentEntitlements` is the **source of truth** for what the user
currently owns (active subs + non-consumables). Recompute from it at launch and
after every transaction - don't rely solely on a cached bool from a past purchase.

```swift
@MainActor @Observable
final class Store {
    private(set) var ownedProductIDs: Set<String> = []

    func refreshEntitlements() async {
        var owned: Set<String> = []
        for await result in Transaction.currentEntitlements {
            guard case .verified(let tx) = result else { continue }
            if tx.revocationDate == nil {     // not refunded/revoked
                owned.insert(tx.productID)
            }
        }
        ownedProductIDs = owned
    }

    var hasPro: Bool { ownedProductIDs.contains("com.example.pro.lifetime") }
}
```

Rules:
- Check `revocationDate == nil` (refunds/family-sharing revocation) and, for subs,
  `expirationDate` / renewal status.
- Gate features off the recomputed entitlement set, ideally on `@MainActor` so the
  UI updates reactively (`@Observable`).
- Persisting a local "isPro" flag is fine as a cache, but always reconcile it
  against `currentEntitlements` on launch.

## Transaction Updates Listener (Required)

Start this **at app launch, before UI**, and keep it for the app's lifetime. It
delivers renewals, Ask-to-Buy approvals, refunds, revocations, and purchases made
on other devices.

```swift
init() {
    // Start the listener FIRST so nothing is missed during async setup.
    updates = Task.detached { [weak self] in
        for await result in Transaction.updates {
            guard case .verified(let tx) = result else { continue }
            await self?.refreshEntitlements()
            await tx.finish()
        }
    }
    Task { await refreshEntitlements() }
}

deinit { updates?.cancel() }
```

Rules:
- One listener for the whole app. Starting it late = missed transactions.
- Always `finish()` verified transactions, or the system re-delivers them forever.

## Subscriptions

Auto-renewable subscriptions add renewal state, billing retry, grace periods, and
offers on top of the basics.

```swift
// Status for a subscription group (use the product's subscription group).
guard let sub = product.subscription else { return }
let statuses = try await sub.status            // [Product.SubscriptionInfo.Status]

for status in statuses {
    let renewal = try checkVerified(status.renewalInfo)
    switch status.state {
    case .subscribed:        // active
    case .inGracePeriod:     // still entitled; billing retry in progress
    case .inBillingRetryPeriod:  // may or may not be entitled per your policy
    case .expired:           // no longer entitled
    case .revoked:           // refunded / removed
    default: break
    }
    _ = renewal.willAutoRenew
    _ = renewal.autoRenewPreference   // product id it will renew into (up/downgrade)
}
```

Key concepts:
- A **subscription group** holds tiers; a user has at most one active sub per
  group. Up/downgrade moves within the group.
- **Grace period** and **billing retry** keep users entitled (per your policy)
  through payment hiccups - check `state`, not just `expirationDate`.
- **Offers**: introductory (one per user/group), promotional (target existing/
  lapsed users), win-back, and offer codes. Eligibility for intro offers comes
  from `product.subscription?.isEligibleForIntroOffer`.

See [references/subscriptions.md](references/subscriptions.md) for status
handling, offer eligibility, and group/tier design.

## Restoring Purchases

`currentEntitlements` already restores non-consumables and active subs on a fresh
install once the user is signed into the same Apple ID. Provide an explicit
**Restore Purchases** button (App Review requires it) that calls `AppStore.sync()`.

```swift
func restore() async throws {
    try await AppStore.sync()        // forces a refresh against the App Store
    await refreshEntitlements()
}
```

Rules:
- `AppStore.sync()` may prompt for App Store authentication - only call it from an
  explicit user action, not automatically on launch.
- For normal launches, just read `currentEntitlements`; don't sync every time.

## SwiftUI StoreKit Views

For many apps the StoreKit SwiftUI views are the fastest correct path - they load
products, render localized pricing, and run the purchase flow for you.

```swift
import StoreKit

// A merchandising view for a set of products / a subscription group.
StoreView(ids: productIDs)

SubscriptionStoreView(groupID: "ABCD1234") {
    MyMarketingContent()
}
.subscriptionStoreButtonLabel(.multiline)
.storeButton(.visible, for: .restorePurchases)

// Single product:
ProductView(id: "com.example.pro.lifetime")
```

Handle results with `.onInAppPurchaseCompletion` and react to entitlement changes
with `.currentEntitlementTask(for:)` / `.subscriptionStatusTask(for:)`.

See [references/swiftui-storekit-views.md](references/swiftui-storekit-views.md)
for customization, purchase-completion handling, and policy/redemption modifiers.

## Server-Side Validation

If you have a backend, validate entitlements server-to-server rather than trusting
the client - especially for consumables and cross-platform accounts.

- **App Store Server API** - fetch transaction/subscription status with a signed
  JWT (issued from an App Store Connect key). Endpoints: `Get Transaction Info`,
  `Get All Subscription Statuses`, `Get Transaction History`.
- **App Store Server Notifications V2** - the App Store POSTs signed JWS events
  (`SUBSCRIBED`, `DID_RENEW`, `DID_FAIL_TO_RENEW`, `REFUND`, `EXPIRED`, etc.) to
  your endpoint. Use these to keep server state current without polling.
- **Signed transactions (JWS)** - both the client and these APIs hand you JWS you
  verify against Apple's x5c certificate chain (root: Apple Root CA - G3). Use
  Apple's open-source `app-store-server-library` (Swift/Java/Python/Node) to
  verify and decode rather than hand-rolling JWS parsing.

See [references/server-validation.md](references/server-validation.md) for the
JWT auth, notification payloads, and JWS verification flow.

## Testing

Three layers, fastest to most realistic:

1. **`.storekit` configuration file** (in Xcode) - define products locally; test
   purchases with no network and no App Store Connect setup. Set it as the scheme's
   StoreKit configuration.
2. **`StoreKitTest`** framework - `SKTestSession` to drive purchases, refunds,
   renewals, Ask-to-Buy, and time-accelerated subscription renewals in unit/UI
   tests.
3. **Sandbox** - real App Store Connect products with a Sandbox Apple ID; required
   before release. Subscriptions renew on an accelerated sandbox clock.

```swift
import StoreKitTest

let session = try SKTestSession(configurationFileNamed: "Products")
session.clearTransactions()
session.disableDialogs = true
// drive purchases / renewals / refunds programmatically
```

See [references/testing.md](references/testing.md) for the config file, `SKTestSession`,
and sandbox setup.

## Common Mistakes

- Starting the `Transaction.updates` listener late (or per-screen) -> missed
  renewals/Ask-to-Buy/refunds.
- Granting entitlement from the `purchase()` return value but never reconciling
  with `currentEntitlements` -> wrong state after reinstall or on a new device.
- Treating `.pending` as failure or success instead of "resolves later."
- Not handling `.unverified` -> trusting tampered transactions.
- Forgetting `transaction.finish()` -> transactions re-delivered endlessly.
- No **Restore Purchases** button -> App Review rejection.
- Building price strings manually instead of `displayPrice` -> wrong currency/locale.
- Calling `AppStore.sync()` automatically on launch -> needless auth prompts.
- Putting consumables in entitlement checks (they aren't there) instead of
  crediting a balance.
- Checking only `expirationDate` for subs and ignoring grace/billing-retry states.
- Trusting the client for consumables/high-value unlocks without server validation.

## Review Checklist

- [ ] StoreKit 2 (`Product`/`Transaction`), not legacy `SKPaymentQueue`, for new code.
- [ ] `Transaction.updates` listener started at launch, before UI, lives app-long.
- [ ] Every transaction/renewal info goes through `VerificationResult`; `.unverified` rejected.
- [ ] Entitlements recomputed from `currentEntitlements` at launch and after updates.
- [ ] `revocationDate` (and sub `state`/`expirationDate`) checked before granting.
- [ ] All four `PurchaseResult` cases handled; `.pending` not shown as success.
- [ ] Every verified transaction `finish()`-ed after delivery.
- [ ] Explicit Restore Purchases action calling `AppStore.sync()`.
- [ ] Prices shown via `displayPrice`; missing product IDs handled.
- [ ] Consumables credited (ideally server-validated), not put in entitlement checks.
- [ ] Tested with a `.storekit` config and `SKTestSession`, then sandbox before release.
- [ ] Server validation (Server API / Notifications V2) for backend-backed accounts.

## References

- [references/purchase-flow.md](references/purchase-flow.md) -- full Store model, product loading, purchase, verification, finishing, app account tokens.
- [references/subscriptions.md](references/subscriptions.md) -- groups/tiers, status & renewal state, grace/billing retry, intro/promo/win-back offers, offer codes.
- [references/swiftui-storekit-views.md](references/swiftui-storekit-views.md) -- StoreView, SubscriptionStoreView, ProductView, completion/entitlement modifiers.
- [references/server-validation.md](references/server-validation.md) -- App Store Server API JWT, Server Notifications V2, JWS verification, app-store-server-library.
- [references/testing.md](references/testing.md) -- .storekit config files, StoreKitTest / SKTestSession, sandbox.

Apple documentation:
- [StoreKit](https://developer.apple.com/documentation/storekit)
- [In-App Purchase](https://developer.apple.com/documentation/storekit/in-app_purchase)
- [App Store Server API](https://developer.apple.com/documentation/appstoreserverapi)
- [App Store Server Notifications](https://developer.apple.com/documentation/appstoreservernotifications)
- [StoreKitTest](https://developer.apple.com/documentation/storekittest)
