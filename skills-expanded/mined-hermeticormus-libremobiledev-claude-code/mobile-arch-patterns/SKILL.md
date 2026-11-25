---
name: mobile-arch-patterns
description: "Architecture code: a Clean Architecture domain and data layer, the iOS Coordinator pattern, an MVI reducer, and Android Navigation with Safe Args. Use when structuring layers, navigation, or state flow in a mobile app."
---

# Mobile Architecture Patterns

## Clean Architecture: Domain Layer (Shared Interface)

```kotlin
// Domain — pure Kotlin, no Android/iOS imports

// Entity
data class Product(
    val id: String,
    val name: String,
    val price: Double,
    val stockCount: Int,
)

// Repository interface (in domain, implemented in data)
interface ProductRepository {
    fun observeProducts(): Flow<List<Product>>
    suspend fun getProduct(id: String): Result<Product>
    suspend fun refresh(): Result<Unit>
}

// UseCase — single responsibility, depends on interface not implementation
class GetProductsUseCase @Inject constructor(
    private val repository: ProductRepository
) {
    operator fun invoke(): Flow<List<Product>> =
        repository.observeProducts()
}

class GetProductDetailUseCase @Inject constructor(
    private val repository: ProductRepository
) {
    suspend operator fun invoke(id: String): Result<Product> =
        repository.getProduct(id)
}
```

### Data Layer Implementation
```kotlin
// data module — implements domain interfaces
class ProductRepositoryImpl @Inject constructor(
    private val remote: ProductRemoteDataSource,
    private val local: ProductLocalDataSource,
) : ProductRepository {

    override fun observeProducts(): Flow<List<Product>> =
        local.observeAll()
            .map { entities -> entities.map { it.toDomain() } }
            .flowOn(Dispatchers.IO)

    override suspend fun getProduct(id: String): Result<Product> =
        runCatching {
            local.getById(id)?.toDomain()
                ?: remote.fetchProduct(id).also { local.insert(it.toEntity()) }.toDomain()
        }

    override suspend fun refresh(): Result<Unit> = runCatching {
        val products = remote.fetchAll()
        local.replaceAll(products.map { it.toEntity() })
    }
}
```

---

## iOS: Coordinator Pattern

```swift
protocol Coordinator: AnyObject {
    var childCoordinators: [Coordinator] { get set }
    var navigationController: UINavigationController { get }
    func start()
}

// App-level coordinator
class AppCoordinator: Coordinator {
    var childCoordinators: [Coordinator] = []
    let navigationController: UINavigationController
    private let authService: AuthService

    init(navigationController: UINavigationController, authService: AuthService) {
        self.navigationController = navigationController
        self.authService = authService
    }

    func start() {
        if authService.isLoggedIn {
            showHome()
        } else {
            showLogin()
        }
    }

    private func showLogin() {
        let coordinator = LoginCoordinator(navigationController: navigationController)
        coordinator.delegate = self
        childCoordinators.append(coordinator)
        coordinator.start()
    }

    private func showHome() {
        let coordinator = HomeCoordinator(navigationController: navigationController)
        childCoordinators.append(coordinator)
        coordinator.start()
    }
}

extension AppCoordinator: LoginCoordinatorDelegate {
    func loginDidComplete(_ coordinator: LoginCoordinator) {
        childCoordinators.removeAll { $0 === coordinator }
        showHome()
    }
}

// Feature coordinator
class LoginCoordinator: Coordinator {
    var childCoordinators: [Coordinator] = []
    let navigationController: UINavigationController
    weak var delegate: LoginCoordinatorDelegate?

    init(navigationController: UINavigationController) {
        self.navigationController = navigationController
    }

    func start() {
        let vm = LoginViewModel(authService: AuthService.shared)
        let vc = LoginViewController(viewModel: vm)
        vm.coordinator = self
        navigationController.setViewControllers([vc], animated: false)
    }

    func showForgotPassword() {
        let vc = ForgotPasswordViewController()
        navigationController.pushViewController(vc, animated: true)
    }

    func loginCompleted() {
        delegate?.loginDidComplete(self)
    }
}

protocol LoginCoordinatorDelegate: AnyObject {
    func loginDidComplete(_ coordinator: LoginCoordinator)
}
```

---

## MVI: Reducer Pattern

```kotlin
// MVI with pure reducer
data class CheckoutUiState(
    val items: List<CartItem> = emptyList(),
    val isLoading: Boolean = false,
    val errorMessage: String? = null,
    val orderConfirmed: Boolean = false,
)

sealed class CheckoutIntent {
    object LoadCart : CheckoutIntent()
    data class RemoveItem(val itemId: String) : CheckoutIntent()
    object PlaceOrder : CheckoutIntent()
    object DismissError : CheckoutIntent()
}

sealed class CheckoutEffect {
    object NavigateToConfirmation : CheckoutEffect()
    data class ShowError(val message: String) : CheckoutEffect()
}

class CheckoutViewModel @Inject constructor(
    private val getCartUseCase: GetCartUseCase,
    private val placeOrderUseCase: PlaceOrderUseCase
) : ViewModel() {

    private val _state = MutableStateFlow(CheckoutUiState())
    val state = _state.asStateFlow()

    private val _effects = Channel<CheckoutEffect>()
    val effects = _effects.receiveAsFlow()

    fun processIntent(intent: CheckoutIntent) {
        when (intent) {
            is CheckoutIntent.LoadCart -> loadCart()
            is CheckoutIntent.RemoveItem -> removeItem(intent.itemId)
            is CheckoutIntent.PlaceOrder -> placeOrder()
            is CheckoutIntent.DismissError -> _state.update { it.copy(errorMessage = null) }
        }
    }

    private fun loadCart() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            getCartUseCase().collect { items ->
                _state.update { it.copy(items = items, isLoading = false) }
            }
        }
    }

    private fun placeOrder() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            placeOrderUseCase(_state.value.items)
                .onSuccess {
                    _state.update { it.copy(isLoading = false, orderConfirmed = true) }
                    _effects.send(CheckoutEffect.NavigateToConfirmation)
                }
                .onFailure { error ->
                    _state.update { it.copy(isLoading = false, errorMessage = error.message) }
                }
        }
    }
}
```

---

## Android Navigation: SafeArgs

```kotlin
// NavGraph (nav_graph.xml)
// <fragment android:id="@+id/productListFragment" ...>
//   <action android:id="@+id/action_list_to_detail"
//           app:destination="@id/productDetailFragment" />
// </fragment>
// <fragment android:id="@+id/productDetailFragment">
//   <argument android:name="productId" app:argType="string" />
// </fragment>

// Navigate with SafeArgs (type-safe)
val action = ProductListFragmentDirections
    .actionListToDetail(productId = "SKU-123")
findNavController().navigate(action)

// Receive in destination
val args: ProductDetailFragmentArgs by navArgs()
val productId = args.productId
```
