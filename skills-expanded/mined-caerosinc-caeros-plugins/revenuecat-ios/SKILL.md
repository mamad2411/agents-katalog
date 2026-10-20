---
name: revenuecat-ios
description: Integrate RevenueCat on iOS with StoreKit 2, configure the SDK, fetch offerings, purchase packages, check entitlements, restore, and handle user identity. Use when writing Swift or SwiftUI purchase code.
---

# RevenueCat on iOS

Current SDK: `purchases-ios` v5+ (Swift Package Manager:
`https://github.com/RevenueCat/purchases-ios`). v5 uses **StoreKit 2 by
default**; RevenueCat validates transactions server-side, so you do not touch
receipts yourself. Requires an In-App Purchase key uploaded in the dashboard.

## Configure once, early

```swift
// App init (e.g. in App.init or AppDelegate)
Purchases.logLevel = .debug          // only during development
Purchases.configure(withAPIKey: "appl_XXXX")   // public SDK key, safe in app
```

If users log in, identify them so purchases follow the account:

```swift
try await Purchases.shared.logIn(myBackendUserID)   // aliases anonymous ID
try await Purchases.shared.logOut()
```

## Show a paywall from offerings

Never hardcode product IDs in the client; read the current offering:

```swift
let offerings = try await Purchases.shared.offerings()
let packages = offerings.current?.availablePackages ?? []
// package.storeProduct.localizedPriceString for display
```

## Purchase and unlock by entitlement

```swift
let result = try await Purchases.shared.purchase(package: package)
if result.customerInfo.entitlements["pro"]?.isActive == true {
    // unlock
}
// User cancels throw ErrorCode.purchaseCancelledError; treat as no-op.
```

Check access anywhere (cached, safe to call often):

```swift
let info = try await Purchases.shared.customerInfo()
let isPro = info.entitlements["pro"]?.isActive == true
```

Listen for changes (renewals, refunds, family sharing, web purchases):

```swift
for await info in Purchases.shared.customerInfoStream {
    updateAccess(from: info)
}
```

## Restore

Apple requires a visible restore control:

```swift
let info = try await Purchases.shared.restorePurchases()
```

## Testing

- **StoreKit configuration file** in Xcode: fastest loop, works in simulator;
  keep product IDs identical to App Store Connect.
- **Sandbox Apple ID** on device: exercises real Apple sandbox; subscriptions
  renew on compressed schedules.
- Sandbox purchases appear in the RevenueCat dashboard marked sandbox.

## Pitfalls

- Entitlement inactive after purchase: product not attached to the
  entitlement in the dashboard, or you checked a product ID instead of the
  entitlement identifier.
- Empty offerings: products not approved or missing in App Store Connect,
  bundle ID mismatch, or paid-apps agreement not signed.
- Do not gate the UI on a one-shot fetch at launch; use the customer info
  stream so renewals and refunds propagate while the app runs.
- Server is the source of truth for server-side gating: verify with the REST
  API or webhooks (see `revenuecat-webhooks-backend`), not client claims.
