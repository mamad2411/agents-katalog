---
name: payment-patterns
description: "StoreKit 2 subscription flow and renewal state, Google Play Billing Library integration, and RevenueCat cross-platform subscriptions. Use when implementing in-app purchases or subscriptions."
---

# Payment Patterns

## iOS StoreKit 2: Complete Subscription Flow

```swift
import StoreKit

class StoreService: ObservableObject {
    @Published var products: [Product] = []
    @Published var isPremium: Bool = false

    private var updateListenerTask: Task<Void, Error>? = nil

    init() {
        updateListenerTask = listenForTransactions()
        Task {
            await loadProducts()
            await checkEntitlements()
        }
    }

    deinit {
        updateListenerTask?.cancel()
    }

    // Listen for real-time transaction updates (renewals, revocations)
    private func listenForTransactions() -> Task<Void, Error> {
        Task.detached {
            for await result in Transaction.updates {
                if let transaction = try? result.payloadValue {
                    await self.handle(transaction: transaction)
                }
            }
        }
    }

    @MainActor
    func loadProducts() async {
        do {
            products = try await Product.products(for: ["com.myapp.premium.monthly",
                                                         "com.myapp.premium.annual"])
        } catch {
            print("Failed to load products: \(error)")
        }
    }

    @MainActor
    func purchase(_ product: Product) async throws {
        let result = try await product.purchase()

        switch result {
        case .success(let verificationResult):
            guard case .verified(let transaction) = verificationResult else { return }
            await handle(transaction: transaction)
        case .userCancelled:
            break
        case .pending:
            // Waiting for parental approval / SCA
            break
        @unknown default:
            break
        }
    }

    @MainActor
    func checkEntitlements() async {
        for await result in Transaction.currentEntitlements {
            if case .verified(let transaction) = result {
                if transaction.revocationDate == nil {
                    isPremium = true
                    return
                }
            }
        }
        isPremium = false
    }

    @MainActor
    private func handle(transaction: Transaction) async {
        // Deliver content
        if transaction.revocationDate == nil {
            isPremium = true
        } else {
            // Revoked — revoke access
            isPremium = false
        }
        // Always finish the transaction
        await transaction.finish()
    }

    func restore() async throws {
        try await AppStore.sync()
        await checkEntitlements()
    }
}
```

### StoreKit 2 Subscription Renewal State
```swift
func subscriptionStatus(for product: Product) async -> String {
    guard let subscription = product.subscription else { return "Not a subscription" }
    guard let status = try? await subscription.status.first else { return "Unknown" }

    return switch status.state {
    case .subscribed:         "Active"
    case .expired:            "Expired"
    case .inBillingRetryPeriod: "Payment issue — retrying"
    case .inGracePeriod:      "Grace period — update payment"
    case .revoked:            "Revoked"
    default:                  "Unknown"
    }
}
```

---

## Android: Google Play Billing Library

```kotlin
class BillingManager(private val context: Context) {
    private var billingClient: BillingClient? = null
    private var productDetails: List<ProductDetails> = emptyList()

    private val purchasesUpdatedListener = PurchasesUpdatedListener { billingResult, purchases ->
        if (billingResult.responseCode == BillingClient.BillingResponseCode.OK && purchases != null) {
            purchases.forEach { purchase ->
                lifecycleScope.launch { handlePurchase(purchase) }
            }
        }
    }

    fun initialize() {
        billingClient = BillingClient.newBuilder(context)
            .setListener(purchasesUpdatedListener)
            .enablePendingPurchases()
            .build()

        billingClient?.startConnection(object : BillingClientStateListener {
            override fun onBillingSetupFinished(result: BillingResult) {
                if (result.responseCode == BillingClient.BillingResponseCode.OK) {
                    lifecycleScope.launch { queryProducts() }
                    lifecycleScope.launch { checkExistingPurchases() }
                }
            }
            override fun onBillingServiceDisconnected() { /* retry connection */ }
        })
    }

    private suspend fun queryProducts() {
        val params = QueryProductDetailsParams.newBuilder()
            .setProductList(listOf(
                QueryProductDetailsParams.Product.newBuilder()
                    .setProductId("premium_monthly")
                    .setProductType(BillingClient.ProductType.SUBS)
                    .build()
            ))
            .build()

        val result = billingClient?.queryProductDetails(params)
        productDetails = result?.productDetailsList ?: emptyList()
    }

    fun launchPurchaseFlow(activity: Activity, productDetails: ProductDetails) {
        val offerToken = productDetails.subscriptionOfferDetails?.firstOrNull()?.offerToken ?: return

        val params = BillingFlowParams.newBuilder()
            .setProductDetailsParamsList(listOf(
                BillingFlowParams.ProductDetailsParams.newBuilder()
                    .setProductDetails(productDetails)
                    .setOfferToken(offerToken)
                    .build()
            ))
            .build()

        billingClient?.launchBillingFlow(activity, params)
    }

    private suspend fun handlePurchase(purchase: Purchase) {
        if (purchase.purchaseState != Purchase.PurchaseState.PURCHASED) return

        // Acknowledge REQUIRED within 3 days
        if (!purchase.isAcknowledged) {
            val params = AcknowledgePurchaseParams.newBuilder()
                .setPurchaseToken(purchase.purchaseToken)
                .build()

            billingClient?.acknowledgePurchase(params)
        }

        // Unlock premium access
        unlockPremium(purchase.purchaseToken)
    }

    private suspend fun checkExistingPurchases() {
        val params = QueryPurchasesParams.newBuilder()
            .setProductType(BillingClient.ProductType.SUBS)
            .build()

        val result = billingClient?.queryPurchasesAsync(params)
        val activePurchases = result?.purchasesList?.filter {
            it.purchaseState == Purchase.PurchaseState.PURCHASED
        }

        if (activePurchases?.isNotEmpty() == true) {
            unlockPremium(activePurchases.first().purchaseToken)
        }
    }
}
```

---

## RevenueCat: Cross-Platform Subscriptions

```swift
// iOS — initialize in AppDelegate
import RevenueCat

Purchases.configure(withAPIKey: "appl_XXXXXXXX")
Purchases.shared.delegate = self

// Check entitlement on app launch
func checkPremiumAccess() {
    Purchases.shared.getCustomerInfo { customerInfo, error in
        guard error == nil, let info = customerInfo else { return }
        let isPremium = info.entitlements["premium"]?.isActive == true
        // Update UI
    }
}

// Purchase
func purchasePackage(_ package: Package) {
    Purchases.shared.purchase(package: package) { transaction, info, error, userCancelled in
        guard !userCancelled, error == nil else { return }
        let isPremium = info?.entitlements["premium"]?.isActive == true
        // Update UI
    }
}
```

```kotlin
// Android
Purchases.configure(PurchasesConfiguration.Builder(context, "goog_XXXXXXXX").build())

Purchases.sharedInstance.getCustomerInfo(object : ReceiveCustomerInfoCallback {
    override fun onReceived(customerInfo: CustomerInfo) {
        val isPremium = customerInfo.entitlements["premium"]?.isActive == true
    }
    override fun onError(error: PurchasesError) { }
})
```
