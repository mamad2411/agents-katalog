---
name: "integrating-revenuecat"
description: "Integrates RevenueCat in-app purchases and subscriptions into Flutter apps using `purchases_flutter` (v11.x). Use when implementing paywalls, checking entitlements via `CustomerInfo`, configuring `PurchasesConfiguration` for iOS or Android, displaying paywalls with `purchases_ui_flutter`, handling purchase errors via `PurchasesErrorHelper`, restoring purchases, integrating RevenueCat with Riverpod or Bloc, presenting the Customer Center, handling web purchase redemption, or calling `Purchases.logIn` for cross-device purchase sync."
metadata:
  last_modified: "2026-04-27 17:41:00 (GMT+8)"
---

# RevenueCat (Flutter) Latest Version Best Practices Guide (v11.x)

## Goal
RevenueCat is the industry-standard solution for handling In-App Purchases (IAP) and subscriptions in mobile applications. In Flutter, the official package is `purchases_flutter` (paired with `purchases_ui_flutter` for pre-built paywall UI).

## Instructions

### 1. Core Concept: Entitlements > Products
In traditional IAP development, developers often focus on "which Product ID the user purchased."
**RevenueCat's best practice is: Always check the user's Entitlements.**

*   **Products**: The actual items configured in Apple/Google consoles (e.g., `monthly_sub_199`).
*   **Offerings**: RevenueCat packages multiple Products into a display offering (e.g., a default offering contains "Monthly" and "Annual" subscriptions). This makes A/B testing extremely easy, allowing you to swap products without changing the APP code.
*   **Entitlements**: The ultimate goal unlocked after a user purchases (e.g., `pro_access`).

👉 **Your APP logic should ALWAYS only check if `pro_access` is active. Do not care about which offering the user bought to get it.**

### 2. Dependencies and Initialization Setup

#### 2.1 Install Packages
```yaml
dependencies:
  purchases_flutter: ^11.0.1  # v11: Android Kotlin 2.1+, compileSdk 35, Play Billing Library 9
  # 🌟 Highly Recommended: Use the official native UI checkout templates (Paywalls) to reduce the pain of building your own UI
  purchases_ui_flutter: ^11.0.1 
```

#### 2.2 Platform Specific Configurations (Extremely Important)
*   **Android (`AndroidManifest.xml`)**: Be sure to set the main Activity's `launchMode` to `singleTask` or `singleTop`. Otherwise, unexpected behaviors like canceled purchases might occur when the user switches back from the Google Play payment screen.
*   **iOS**: Ensure Xcode 14.0+, and the deployment target is generally recommended to be iOS 13.0+.

#### 2.3 Initialization (On App Startup)
Complete the initialization as early as possible, either in `main()` or before the App UI renders.

```dart
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:purchases_flutter/purchases_flutter.dart';

Future<void> initPlatformState() async {
  await Purchases.setLogLevel(kDebugMode ? LogLevel.debug : LogLevel.info);

  PurchasesConfiguration? configuration;
  if (Platform.isAndroid) {
    // Android natively uses a Builder underneath; just provide the API Key in Flutter
    configuration = PurchasesConfiguration('goog_api_key_here');
  } else if (Platform.isIOS) {
    configuration = PurchasesConfiguration('appl_api_key_here')
      // 🌟 v7+ Best Practice: Explicitly define StoreKit version (defaults to auto-select, but StoreKit 2 requires In-App Purchase Key configurations in your RevenueCat Dashboard)
      ..storeKitVersion = StoreKitVersion.storeKit2; 
  }
  
  if (configuration != null) {
    // 🌟 Best Practice: Pass your own user ID here to help RevenueCat sync across devices.
    // configuration.appUserID = "my_app_user_id";

    // ⚠️ Deprecation Notice: "Observer Mode" is now legacy. If your App fundamentally completes its own transactions (instead of RevenueCat), deploy:
    // configuration.purchasesAreCompletedBy = PurchasesAreCompletedByMyApp(storeKitVersion: StoreKitVersion.storeKit2);

    await Purchases.configure(configuration);
  }
}
```

> [!WARNING]
> **v10.0 Breaking Change — Min Android SDK 21 → 23**: purchases_flutter v10 updates to Billing Library 8.3.0, raising the minimum Android SDK from API 21 to API 23 (Android 6). Update your `android/app/build.gradle`:
> ```gradle
> defaultConfig {
>     minSdkVersion 23  // was 21 in v9
> }
> ```
> 
> **CRITICAL**: If your App offers "Lifetime Unlock" products without a backend account system, you **MUST** strictly configure them as **Non-consumable** inside the RevenueCat dashboard. If labeled as consumable, RevenueCat consumes them instantly, and users will permanently lose the ability to `restorePurchases`! This workaround (available in v9) is **completely removed** in v10.

### 3. Checking Entitlements and State Management (Best Practices)
Integrate RevenueCat's state into your state management (like Riverpod / Bloc) to drive UI unlocking.

```dart
// Using Riverpod as an example
final customerInfoProvider = FutureProvider<CustomerInfo>((ref) async {
  // Get the latest state
  return await Purchases.getCustomerInfo();
});

final isProUserProvider = Provider<bool>((ref) {
  final customerInfo = ref.watch(customerInfoProvider).valueOrNull;
  if (customerInfo == null) return false;
  
  // 🌟 Best Practice: Only verify if the entitlement is active
  return customerInfo.entitlements.all['pro_access']?.isActive == true;
});
```

Besides the initial fetch, it's recommended to listen for customer info changes (e.g., successful background renewals):
```dart
Purchases.addCustomerInfoUpdateListener((customerInfo) {
  // Update your global state (e.g., notify Bloc or invalidate Riverpod provider)
  // ref.invalidate(customerInfoProvider);
});
```

### 4. Checkout and Displaying the Paywall
RevenueCat's strength lies in its ability to let you remotely control what to sell.

#### 4.1 Using the Official Paywall (Fastest, Most Stable)
Through `purchases_ui_flutter`, you can directly summon the paywall designed in the RevenueCat console, saving you the time of building the UI.

```dart
import 'package:purchases_ui_flutter/purchases_ui_flutter.dart';

Future<void> showPaywall(BuildContext context) async {
  // Presents a full-screen Paywall meticulously designed in the RevenueCat Dashboard
  final paywallResult = await RevenueCatUI.presentPaywall();
  
  if (paywallResult == PaywallResult.purchased) {
    // Purchase successful, update state and close the wall
  }
}
```

#### 4.2 Customer Center (v9+ New Feature)
RevenueCatUI now encompasses a full-fledged robust **Customer Center** interface natively empowering users to manage subscriptions, cancel, or seek refunds autonomously without developers coding management screens.

```dart
// Launch the autonomous subscription management center directly 
await RevenueCatUI.presentCustomerCenter();
```

#### 4.3 Custom Paywall
If you need complete customization, fetch the `Offerings` and manually call the purchase method:

```dart
Future<void> purchasePackage(Package package) async {
  try {
    // Execute purchase. ⚠️ v9 Breaking Change: Now returns `PurchaseResult` encapsulating `customerInfo` and `storeTransaction` instead of exposing `CustomerInfo` directly.
    PurchaseResult result = await Purchases.purchasePackage(package);
    
    // 🌟 Principle: Still check the Entitlement after purchase leveraging the extracted customerInfo!
    final isPro = result.customerInfo.entitlements.all['pro_access']?.isActive == true;
    if (isPro) {
      // Successfully unlocked!
    }
  } on PlatformException catch (e) {
    // 🌟 Officially endorsed error interception approach
    var errorCode = PurchasesErrorHelper.getErrorCode(e);
    if (errorCode != PurchasesErrorCode.purchaseCancelledError) {
      // Show error to the user
    }
  }
}
```

#### 4.4 Web Redemption (Flutter Web)
RevenueCat v9 integrates Web Billing smoothly. You must parse `WebPurchaseRedemptionResult` exhaustively through `switch`:
```dart
  switch (result) {
    case WebPurchaseRedemptionSuccess(:final customerInfo):
      // Redeemed successfully
      break;
    case WebPurchaseRedemptionError(:final error):
      // Redemption failed
      break;
    case WebPurchaseRedemptionPurchaseBelongsToOtherUser():
      // Already tied to another user
      break;
    case WebPurchaseRedemptionInvalidToken():
    case WebPurchaseRedemptionExpired(:final obfuscatedEmail):
      // Validation failures
      break;
  };
```

### 5. Restore Purchases
Apple mandates that Apps must provide a "Restore Purchases" button.

```dart
try {
  CustomerInfo customerInfo = await Purchases.restorePurchases();
  // Check entitlements as usual
  if (customerInfo.entitlements.all['pro_access']?.isActive == true) {
     // Restore successful
  }
} catch (e) {
  // Handle error
}
```

### 6. Summary
1.  **Abandon local receipt validation**: Hand this over 100% to RevenueCat.
2.  **Decouple logic from products**: In your code, only check `entitlements` through `CustomerInfo`. Do not hardcode any product IDs.
3.  **Login Integration**: If your App has its own account system, remember to call `Purchases.logIn(userId)` after login to ensure cross-device purchase history can be bound to your account.

## Constraints
* Always check `entitlements.all['your_entitlement']?.isActive` instead of checking the presence of active subscriptions or product IDs.
* Ensure you configure the `Purchases` singleton before making any other RevenueCat calls.
* **v10+ Android**: `minSdkVersion` must be 23 or higher. Apps still targeting API 21/22 must remain on v9.

## Old Patterns (pre-v10)

```yaml
# Pre-v10 line (v9.x, latest 9.16.2). Supports Android API 21+; use only if you cannot raise minSdk to 23.
dependencies:
  purchases_flutter: ^9.16.2
  purchases_ui_flutter: ^9.16.2
```

In v9, a workaround allowed restoring consumed one-time products on Android. This workaround is removed in v10. If you relied on it, configure those products as non-consumable in the RevenueCat dashboard before upgrading.
