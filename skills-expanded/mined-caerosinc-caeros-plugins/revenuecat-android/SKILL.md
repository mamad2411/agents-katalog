---
name: revenuecat-android
description: Integrate RevenueCat on Android with Google Play Billing, configure the SDK, purchase flows, upgrades and downgrades with replacement modes, and billing recovery. Use when writing Kotlin purchase code for Play Store apps.
---

# RevenueCat on Android

Current SDK: `purchases-android` (Gradle: `com.revenuecat.purchases:purchases`).
It wraps Google Play Billing internally; you never call BillingClient
yourself. Requires the Play service-account credentials and Pub/Sub developer
notifications configured in the RevenueCat dashboard.

## Configure

```kotlin
// Application.onCreate
Purchases.logLevel = LogLevel.DEBUG   // development only
Purchases.configure(
    PurchasesConfiguration.Builder(this, "goog_XXXX").build()  // public key
)
```

Identity mirrors iOS: `Purchases.sharedInstance.logIn(userId)` /
`logOut()` so one backend account maps to one subscriber.

## Offerings and purchase

```kotlin
val offerings = Purchases.sharedInstance.awaitOfferings()
val packages = offerings.current?.availablePackages.orEmpty()

val result = Purchases.sharedInstance.awaitPurchase(
    PurchaseParams.Builder(activity, packages.first()).build()
)
if (result.customerInfo.entitlements["pro"]?.isActive == true) {
    // unlock
}
```

Handle `PurchasesException`: `userCancelled` is a normal outcome, not an
error path. Check entitlements, never Play SKU strings, in app code.

## Plan changes (upgrade / downgrade / crossgrade)

Google requires an explicit replacement mode when switching subscriptions.
Pass the old product and a `GoogleReplacementMode` on the purchase:

```kotlin
val params = PurchaseParams.Builder(activity, newPackage)
    .oldProductId("monthly_sub")
    .googleReplacementMode(GoogleReplacementMode.WITH_TIME_PRORATION)
    .build()
```

Common modes: `WITH_TIME_PRORATION` (default, credit remaining time),
`CHARGE_PRORATED_PRICE` (upgrade now, pay difference),
`CHARGE_FULL_PRICE` (immediate full charge), `DEFERRED` (switch at renewal,
typical for downgrades). Pick per direction of the change; Play rejects some
combinations, so test each path with license testers.

## Billing recovery and lifecycle

- Grace period and account hold are surfaced through entitlements and
  webhooks: during grace the entitlement stays active, during hold it goes
  inactive. Do not implement your own retry logic; Google retries payment.
- React to out-of-app events (renewals, recovery, refunds) by observing
  customer info updates, and server-side with `BILLING_ISSUE`, `RENEWAL`,
  `EXPIRATION` webhooks (see `revenuecat-webhooks-backend`).
- Prompt users in billing trouble to update payment via the Play
  subscription center deep link:
  `https://play.google.com/store/account/subscriptions`.

## Testing

- Upload at least one build to a closed track and add **license testers**;
  test subscriptions renew in minutes, so lifecycle paths are fast to verify.
- Verify the service account: if offerings are empty or purchases fail with
  store problem errors, check package name, product status (active), and
  that credentials finished propagating (can take up to ~36 hours initially).

## Pitfalls

- Missing developer notifications (Pub/Sub) delays server-side state changes;
  set them up, do not rely on app opens.
- Test on a device with a Play account that is a license tester; emulators
  need Play Store images.
- Amazon Appstore builds use a different store config and public API key.
