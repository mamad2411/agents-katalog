---
name: android-in-app-purchases
description: |
  In-app purchase patterns for Android using Play Billing Library 6+ - BillingClient connection lifecycle, one-time products and subscriptions, purchase flow with PurchasesUpdatedListener, server-side verification, acknowledging and consuming purchases, pending purchase handling, and exposing entitlement state via a repository-backed Flow. Use this skill whenever implementing consumable items, one-time purchases, subscription flows, or purchase restoration. Trigger on phrases like "in-app purchase", "IAP", "Play Billing", "subscription", "BillingClient", "purchase flow", "entitlement", "consumable", or "one-time product".
---

# Android In-App Purchases

## Core Principles

- The BillingClient connection is a long-lived resource — manage it carefully and reconnect on disconnect.
- Never grant entitlement based on client-side purchase data alone. Always verify server-side.
- Acknowledge every non-consumable purchase within three days or Google will reverse it.
- Consume purchases only for consumable items (coins, credits, etc.) that can be re-purchased.
- Expose purchase/entitlement state as a `Flow` from a repository; the domain and presentation layers consume it without touching the Billing API directly.

---

## Dependencies

```kotlin
// build.gradle.kts
implementation(libs.android.billing)
implementation(libs.android.billing.ktx)
```

```toml
[libraries]
android-billing = { module = "com.android.billingclient:billing", version.ref = "billing" }
android-billing-ktx = { module = "com.android.billingclient:billing-ktx", version.ref = "billing" }

[versions]
billing = "6.2.1"
```

---

## BillingClient Setup and Connection

The `BillingClient` should live in the data layer, scoped to the application lifetime:

```kotlin
class BillingDataSource(
    private val context: Context,
    private val coroutineScope: CoroutineScope
) : PurchasesUpdatedListener {

    private val _purchaseUpdates = MutableSharedFlow<List<Purchase>>(
        extraBufferCapacity = 1,
        onBufferOverflow = BufferOverflow.DROP_OLDEST
    )
    val purchaseUpdates: SharedFlow<List<Purchase>> = _purchaseUpdates.asSharedFlow()

    val billingClient: BillingClient = BillingClient.newBuilder(context)
        .setListener(this)
        .enablePendingPurchases()
        .build()

    private var isConnected = false

    override fun onPurchasesUpdated(
        billingResult: BillingResult,
        purchases: List<Purchase>?
    ) {
        if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
            coroutineScope.launch {
                _purchaseUpdates.emit(purchases.orEmpty())
            }
        } else if (billingResult.responseCode != BillingClient.BillingResponseCode.USER_CANCELED) {
            // Log non-cancellation errors for monitoring
        }
    }

    suspend fun ensureConnected(): Boolean {
        if (isConnected && billingClient.isReady) return true
        return suspendCancellableCoroutine { cont ->
            billingClient.startConnection(object : BillingClientStateListener {
                override fun onBillingSetupFinished(result: BillingResult) {
                    isConnected = result.responseCode == BillingClient.BillingResponseCode.OK
                    cont.resume(isConnected)
                }
                override fun onBillingServiceDisconnected() {
                    isConnected = false
                    // Do not resume — let the caller retry
                }
            })
        }
    }

    fun disconnect() {
        billingClient.endConnection()
        isConnected = false
    }
}
```

Register `BillingDataSource` as a singleton in your DI module. Call `disconnect()` only when the app is shutting down.

---

## Querying Available Products

Query products before showing a paywall:

```kotlin
suspend fun queryProducts(
    productIds: List<String>,
    productType: String   // BillingClient.ProductType.INAPP or SUBS
): List<ProductDetails> {
    if (!ensureConnected()) return emptyList()

    val params = QueryProductDetailsParams.newBuilder()
        .setProductList(
            productIds.map { id ->
                QueryProductDetailsParams.Product.newBuilder()
                    .setProductId(id)
                    .setProductType(productType)
                    .build()
            }
        )
        .build()

    val result = billingClient.queryProductDetails(params)
    return if (result.billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
        result.productDetailsList.orEmpty()
    } else {
        emptyList()
    }
}
```

Cache `ProductDetails` results in memory for the session lifetime. Do not query on every recomposition.

---

## Launching the Purchase Flow

The purchase flow must be launched from an `Activity`:

```kotlin
fun launchBillingFlow(
    activity: Activity,
    productDetails: ProductDetails,
    offerToken: String? = null  // required for subscriptions
): BillingResult {
    val productDetailsParams = BillingFlowParams.ProductDetailsParams.newBuilder()
        .setProductDetails(productDetails)
        .apply { offerToken?.let { setOfferToken(it) } }
        .build()

    val params = BillingFlowParams.newBuilder()
        .setProductDetailsParamsList(listOf(productDetailsParams))
        .build()

    return billingClient.launchBillingFlow(activity, params)
}
```

For subscriptions, always pass an `offerToken` obtained from `ProductDetails.subscriptionOfferDetails`.

**Do not** launch billing flows from a `ViewModel` directly. The `Activity` reference must stay in the UI layer.

---

## Repository Layer

Wrap the billing data source behind a clean domain interface:

```kotlin
interface PurchaseRepository {
    fun observeEntitlements(): Flow<Set<Entitlement>>
    suspend fun getProductDetails(productId: String): ProductDetails?
    suspend fun acknowledgePurchase(purchaseToken: String): Boolean
    suspend fun consumePurchase(purchaseToken: String): Boolean
    suspend fun restorePurchases()
}

sealed interface Entitlement {
    data object PremiumMonthly : Entitlement
    data object PremiumAnnual : Entitlement
    data class CoinPack(val quantity: Int) : Entitlement
}
```

The domain and presentation layers depend only on `PurchaseRepository` — never on `BillingClient` directly.

---

## Acknowledging Purchases

Every non-consumable purchase **must** be acknowledged within 3 days, or Play will refund it automatically:

```kotlin
suspend fun acknowledgePurchase(purchase: Purchase): Boolean {
    if (purchase.isAcknowledged) return true
    val params = AcknowledgePurchaseParams.newBuilder()
        .setPurchaseToken(purchase.purchaseToken)
        .build()
    val result = billingClient.acknowledgePurchase(params)
    return result.responseCode == BillingClient.BillingResponseCode.OK
}
```

Acknowledge only after the server has verified and recorded the purchase.

---

## Consuming Purchases

Consume only items the user can re-purchase (coins, one-time consumables):

```kotlin
suspend fun consumePurchase(purchase: Purchase): Boolean {
    val params = ConsumeParams.newBuilder()
        .setPurchaseToken(purchase.purchaseToken)
        .build()
    val result = billingClient.consumePurchase(params)
    return result.billingResult.responseCode == BillingClient.BillingResponseCode.OK
}
```

Consuming a purchase removes it from the user's purchase history and makes the product available for re-purchase. Never consume subscriptions or permanent unlocks.

---

## Server-Side Verification

Client-side purchase data can be spoofed. The server must verify every purchase before granting entitlement:

```kotlin
// Data layer — send purchase token to your backend
suspend fun verifyWithServer(purchase: Purchase): VerificationResult {
    return try {
        val response = apiService.verifyPurchase(
            VerifyPurchaseRequest(
                purchaseToken = purchase.purchaseToken,
                productId = purchase.products.first(),
                packageName = BuildConfig.APPLICATION_ID
            )
        )
        if (response.isValid) {
            VerificationResult.Valid(entitlement = response.entitlement)
        } else {
            VerificationResult.Invalid
        }
    } catch (e: Exception) {
        VerificationResult.NetworkError
    }
}

sealed interface VerificationResult {
    data class Valid(val entitlement: Entitlement) : VerificationResult
    data object Invalid : VerificationResult
    data object NetworkError : VerificationResult
}
```

The server uses the Google Play Developer API to validate the token. The client should never trust its own `Purchase` object as ground truth.

---

## Handling Pending Purchases

Purchases can be in a `PENDING` state (cash payments, carrier billing). Never grant entitlement for pending purchases:

```kotlin
fun processPurchases(purchases: List<Purchase>) {
    purchases.forEach { purchase ->
        when (purchase.purchaseState) {
            Purchase.PurchaseState.PURCHASED -> handlePurchased(purchase)
            Purchase.PurchaseState.PENDING -> handlePending(purchase)
            Purchase.PurchaseState.UNSPECIFIED_STATE -> { /* ignore */ }
        }
    }
}

private fun handlePending(purchase: Purchase) {
    // Show a "payment pending" notice; do not grant access yet
    // Re-query purchases on next app open to check if it moved to PURCHASED
}
```

---

## Restoring Purchases

Always re-query active purchases on app startup and after a successful connection:

```kotlin
suspend fun restorePurchases() {
    if (!ensureConnected()) return

    // Query one-time purchases
    val inappResult = billingClient.queryPurchasesAsync(
        QueryPurchasesParams.newBuilder()
            .setProductType(BillingClient.ProductType.INAPP)
            .build()
    )

    // Query subscriptions
    val subsResult = billingClient.queryPurchasesAsync(
        QueryPurchasesParams.newBuilder()
            .setProductType(BillingClient.ProductType.SUBS)
            .build()
    )

    val allPurchases = inappResult.purchasesList + subsResult.purchasesList
    processPurchases(allPurchases)
}
```

Call this from your `Application.onCreate` or when the billing client reconnects.

---

## Exposing Entitlement State as a Flow

Use a `StateFlow` in the repository to make entitlement state observable:

```kotlin
class PurchaseRepositoryImpl(
    private val billingDataSource: BillingDataSource,
    private val apiService: PurchaseApiService,
    private val scope: CoroutineScope
) : PurchaseRepository {

    private val _entitlements = MutableStateFlow<Set<Entitlement>>(emptySet())

    override fun observeEntitlements(): Flow<Set<Entitlement>> = _entitlements.asStateFlow()

    init {
        scope.launch {
            billingDataSource.purchaseUpdates.collect { purchases ->
                val verified = purchases
                    .filter { it.purchaseState == Purchase.PurchaseState.PURCHASED }
                    .mapNotNull { verifyAndAcknowledge(it) }
                _entitlements.value = verified.toSet()
            }
        }
    }

    private suspend fun verifyAndAcknowledge(purchase: Purchase): Entitlement? {
        val result = verifyWithServer(purchase)
        return if (result is VerificationResult.Valid) {
            acknowledgePurchase(purchase)
            result.entitlement
        } else null
    }
}
```

The `ViewModel` observes `observeEntitlements()` and maps it to gated UI state:

```kotlin
class PaywallViewModel(
    private val purchaseRepository: PurchaseRepository
) : ViewModel() {

    val state: StateFlow<PaywallState> = purchaseRepository.observeEntitlements()
        .map { entitlements ->
            PaywallState(
                isPremium = Entitlement.PremiumMonthly in entitlements ||
                    Entitlement.PremiumAnnual in entitlements
            )
        }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), PaywallState())
}
```

---

## Graceful Offline Handling

When `ensureConnected()` returns false, show a non-blocking error rather than crashing:

```kotlin
val state: StateFlow<PaywallState> = flow {
    val available = billingDataSource.ensureConnected()
    emit(PaywallState(isBillingAvailable = available))
}.stateIn(viewModelScope, SharingStarted.Eagerly, PaywallState())
```

Cache the last known entitlement locally (e.g., in DataStore) so the user retains access when offline. See **android-datastore-preferences** for local persistence patterns.

---

## Anti-Patterns

- Granting entitlement immediately after `onPurchasesUpdated` without server verification — trivially spoofable.
- Forgetting to acknowledge purchases — Play reverses them after 72 hours.
- Consuming non-consumable purchases — permanently removes them from the user's account.
- Calling `queryProductDetails` on every screen entry — expensive; cache results for the session.
- Holding an `Activity` reference in the `ViewModel` to call `launchBillingFlow` — pass the Activity from the Root composable via a channel or event.
- Not handling `PENDING` purchase state — leaves users without access feedback for legitimate purchases.
- Reconnecting `BillingClient` on every `ViewModel` creation — it should be a singleton in the data layer.

---

## Testing Guidance

- Use the Play Billing Library's `BillingClient` test instruments or a fake `PurchaseRepository` in unit tests.
- Test `ViewModel` state changes for each entitlement scenario: empty, single product, subscription, expired.
- Use `FakePurchaseRepository` that emits controlled entitlement `Flow` states.
- For integration tests, use Google Play's License Testing accounts.

```kotlin
class FakePurchaseRepository : PurchaseRepository {
    private val entitlements = MutableStateFlow<Set<Entitlement>>(emptySet())
    override fun observeEntitlements(): Flow<Set<Entitlement>> = entitlements
    fun grant(entitlement: Entitlement) { entitlements.value = entitlements.value + entitlement }
    fun revoke(entitlement: Entitlement) { entitlements.value = entitlements.value - entitlement }
    override suspend fun restorePurchases() {}
    override suspend fun getProductDetails(productId: String): ProductDetails? = null
    override suspend fun acknowledgePurchase(purchaseToken: String): Boolean = true
    override suspend fun consumePurchase(purchaseToken: String): Boolean = true
}
```

---

## Checklist: Adding In-App Purchases

- [ ] Add billing dependency and declare products in Play Console before testing
- [ ] Keep `BillingClient` as an application-scoped singleton
- [ ] Query and restore purchases on every app start
- [ ] Verify every purchase server-side before granting entitlement
- [ ] Acknowledge all non-consumable purchases promptly
- [ ] Consume only genuinely consumable items
- [ ] Handle `PENDING` state without granting entitlement
- [ ] Expose entitlement as a `Flow` from a repository
- [ ] Cache entitlements locally for offline access
- [ ] Test with a `FakePurchaseRepository` that emits controlled state
