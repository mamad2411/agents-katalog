---
name: solid-principles
description: >
  Apply and evaluate SOLID principles in mobile and backend codebases — Single Responsibility,
  Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion with
  platform-specific examples across Flutter (Dart), Android (Kotlin/Java), iOS (Swift/ObjC),
  and backend (Spring/Node/Python/Go).
  TRIGGER when: user says /solid-principles, asks about SOLID, needs to evaluate
  code against design principles, or wants to refactor for better design.
argument-hint: "[code or design to evaluate against SOLID]"
user-invocable: true
---

# SOLID Principles

You are a senior software engineer. Help the user understand, apply, and evaluate SOLID principles with concrete, platform-specific examples and refactoring guidance.

## The Five Principles

### S — Single Responsibility Principle (SRP)

> A class should have only one reason to change.

**Violation signs:** Class handles networking AND parsing AND caching. ViewModel does API calls AND navigation AND analytics. Activity/Controller manages UI AND business logic.

#### Bad (Android — Java)
```java
// This class does EVERYTHING — networking, caching, UI logic
public class ProductManager {
    public List<Product> fetchFromApi() { /* HTTP call */ }
    public void saveToDatabase(List<Product> products) { /* Room insert */ }
    public void trackAnalytics(String event) { /* Firebase call */ }
    public String formatPrice(double price) { /* currency formatting */ }
    public boolean isProductAvailable(Product p) { /* business logic */ }
}
```

#### Good (Android — Kotlin)
```kotlin
class ProductRepository(private val api: ProductApi, private val dao: ProductDao) {
    suspend fun getProducts(): List<Product> { /* fetch + cache */ }
}
class PriceFormatter(private val locale: Locale) {
    fun format(price: Double): String { /* currency formatting */ }
}
class AvailabilityChecker {
    fun isAvailable(product: Product): Boolean { /* business rule */ }
}
class AnalyticsTracker(private val firebase: FirebaseAnalytics) {
    fun track(event: String) { /* tracking */ }
}
```

#### Bad (iOS — Objective-C)
```objc
// Massive View Controller
@implementation ProductViewController
- (void)viewDidLoad {
    [self fetchProductsFromAPI];      // networking
    [self setupTableView];             // UI
    [self configureAnalytics];         // analytics
    [self checkUserPermissions];       // auth
    [self validateProductData];        // business logic
}
@end
```

#### Good (iOS — Swift)
```swift
// Each concern is a separate type
class ProductListViewModel { /* presentation logic only */ }
class ProductRepository { /* data access only */ }
class ProductValidator { /* business rules only */ }
class AnalyticsService { /* tracking only */ }
```

#### Flutter (Dart)
```dart
// Bad: Widget does fetching, formatting, and navigation
class ProductPage extends StatefulWidget { /* 500 lines of everything */ }

// Good: Separate concerns
class ProductRepository { /* data access */ }
class ProductBloc extends Bloc<ProductEvent, ProductState> { /* state logic */ }
class PriceFormatter { /* formatting */ }
class ProductPage extends StatelessWidget { /* UI only, delegates to BLoC */ }
```

---

### O — Open/Closed Principle (OCP)

> Software entities should be open for extension but closed for modification.

**Violation signs:** Adding a new feature requires modifying existing classes with if/else chains. Switch statements that grow with every new type.

#### Bad (Java)
```java
// Adding a new payment method requires modifying this class
public class PaymentProcessor {
    public void process(Payment payment) {
        if (payment.type.equals("credit_card")) {
            // process credit card
        } else if (payment.type.equals("paypal")) {
            // process paypal
        } else if (payment.type.equals("crypto")) {
            // process crypto — had to modify existing class!
        }
    }
}
```

#### Good (Kotlin)
```kotlin
// New payment methods are extensions, not modifications
interface PaymentStrategy {
    fun process(payment: Payment): Result<Receipt>
}

class CreditCardPayment : PaymentStrategy { override fun process(payment: Payment) = /* ... */ }
class PayPalPayment : PaymentStrategy { override fun process(payment: Payment) = /* ... */ }
class CryptoPayment : PaymentStrategy { override fun process(payment: Payment) = /* ... */ }
// Adding ApplePayPayment doesn't touch any existing code

class PaymentProcessor(private val strategies: Map<PaymentType, PaymentStrategy>) {
    fun process(payment: Payment): Result<Receipt> =
        strategies[payment.type]?.process(payment) ?: Result.failure(UnsupportedPaymentException())
}
```

#### Swift
```swift
protocol PaymentStrategy {
    func process(_ payment: Payment) async throws -> Receipt
}

struct CreditCardPayment: PaymentStrategy { func process(_ payment: Payment) async throws -> Receipt { /* ... */ } }
struct PayPalPayment: PaymentStrategy { func process(_ payment: Payment) async throws -> Receipt { /* ... */ } }
// Extend by adding new conformances, not modifying existing code
```

#### Dart (Flutter)
```dart
abstract class PaymentStrategy {
  Future<Receipt> process(Payment payment);
}

class CreditCardPayment implements PaymentStrategy { /* ... */ }
class PayPalPayment implements PaymentStrategy { /* ... */ }
// Register new strategies without modifying PaymentProcessor
```

---

### L — Liskov Substitution Principle (LSP)

> Subtypes must be substitutable for their base types without altering program correctness.

**Violation signs:** Subclass throws exceptions for methods the parent supports. Overriding a method to do nothing. Checking `instanceof` / `is` to handle subtypes differently.

#### Bad (Java)
```java
class Bird {
    public void fly() { /* fly logic */ }
}
class Penguin extends Bird {
    @Override
    public void fly() {
        throw new UnsupportedOperationException("Penguins can't fly!");
        // Violates LSP — callers of Bird.fly() don't expect exceptions
    }
}
```

#### Good (Kotlin)
```kotlin
interface Bird { fun move() }
interface FlyingBird : Bird { fun fly() }

class Sparrow : FlyingBird {
    override fun move() { fly() }
    override fun fly() { /* fly logic */ }
}
class Penguin : Bird {
    override fun move() { /* waddle logic */ }
    // No fly() — penguins aren't FlyingBirds
}
```

#### Practical mobile example — Swift
```swift
// Bad: ReadOnlyRepository extends MutableRepository but disallows writes
protocol Repository {
    func getAll() async -> [Product]
    func save(_ product: Product) async
    func delete(_ id: String) async
}

class CachedRepository: Repository {
    func save(_ product: Product) async {
        fatalError("Cache is read-only!") // LSP violation
    }
}

// Good: Separate read and write protocols
protocol ReadableRepository {
    func getAll() async -> [Product]
}
protocol WritableRepository: ReadableRepository {
    func save(_ product: Product) async
    func delete(_ id: String) async
}
```

---

### I — Interface Segregation Principle (ISP)

> Clients should not be forced to depend on interfaces they do not use.

**Violation signs:** A class implements an interface but leaves half the methods empty or throwing. A "God interface" with 20+ methods.

#### Bad (Java)
```java
interface UserService {
    User getUser(String id);
    List<User> searchUsers(String query);
    void createUser(User user);
    void deleteUser(String id);
    void sendEmail(String userId, String message);    // Why is email in UserService?
    void exportToCSV(List<User> users);               // Why is export here?
    boolean validatePassword(String password);          // Why is validation here?
}
```

#### Good (Kotlin)
```kotlin
interface UserReader {
    suspend fun getUser(id: String): User
    suspend fun searchUsers(query: String): List<User>
}
interface UserWriter {
    suspend fun createUser(user: User)
    suspend fun deleteUser(id: String)
}
interface UserExporter {
    suspend fun exportToCSV(users: List<User>): ByteArray
}
// Classes implement only what they need
```

#### Dart (Flutter)
```dart
// Bad: One massive repository interface
abstract class Repository<T> {
  Future<T> getById(String id);
  Future<List<T>> getAll();
  Future<void> create(T item);
  Future<void> update(T item);
  Future<void> delete(String id);
  Stream<List<T>> watchAll();           // Not all repos need streams
  Future<void> syncWithServer();        // Not all repos sync
  Future<int> count();                  // Not all repos need count
}

// Good: Compose small interfaces
abstract class Readable<T> { Future<T> getById(String id); }
abstract class Listable<T> { Future<List<T>> getAll(); }
abstract class Writable<T> { Future<void> save(T item); }
abstract class Watchable<T> { Stream<List<T>> watchAll(); }

class ProductRepository implements Readable<Product>, Listable<Product>, Watchable<Product> {
  // Only implements what it needs
}
```

---

### D — Dependency Inversion Principle (DIP)

> High-level modules should not depend on low-level modules. Both should depend on abstractions.

**Violation signs:** ViewModel directly instantiates Retrofit/URLSession. Business logic imports database framework. Constructor creates its own dependencies with `new`.

#### Bad (Java)
```java
// ViewModel depends directly on concrete implementation
class ProductViewModel extends ViewModel {
    // Tightly coupled — can't test without real API and database
    private final RetrofitProductApi api = new RetrofitProductApi();
    private final RoomProductDao dao = AppDatabase.getInstance().productDao();
}
```

#### Good (Kotlin — with Hilt)
```kotlin
// ViewModel depends on abstraction
class ProductViewModel @Inject constructor(
    private val repository: ProductRepository  // Interface, not impl
) : ViewModel()

// DI module wires the concrete implementation
@Module
@InstallIn(SingletonComponent::class)
abstract class DataModule {
    @Binds
    abstract fun bindProductRepo(impl: ProductRepositoryImpl): ProductRepository
}
```

#### Good (Swift — manual DI)
```swift
// Protocol (abstraction)
protocol ProductRepository {
    func getAll() async throws -> [Product]
}

// ViewModel depends on protocol, not concrete class
@Observable
class ProductListViewModel {
    private let repo: ProductRepository
    init(repo: ProductRepository) { self.repo = repo }
}

// In production: ViewModel(repo: APIProductRepository())
// In tests:      ViewModel(repo: MockProductRepository())
```

#### Good (Dart — Riverpod)
```dart
// Abstract repository
abstract class ProductRepository {
  Future<List<Product>> getAll();
}

// Concrete implementation
class ApiProductRepository implements ProductRepository {
  final Dio _dio;
  ApiProductRepository(this._dio);
  @override
  Future<List<Product>> getAll() async { /* API call */ }
}

// DI via Riverpod
final productRepoProvider = Provider<ProductRepository>((ref) {
  return ApiProductRepository(ref.read(dioProvider));
});

// Override in tests
final container = ProviderContainer(overrides: [
  productRepoProvider.overrideWithValue(MockProductRepository()),
]);
```

#### DI Framework Reference

| Platform | Modern | Legacy |
|----------|--------|--------|
| **Android** | Hilt (recommended), Koin | Dagger 2, manual |
| **iOS** | Swinject, Resolver, Factory, manual | Typhoon (ObjC), manual |
| **Flutter** | Riverpod, get_it + injectable | Provider, manual |
| **Spring** | Spring IoC (constructor injection) | — |
| **Node** | NestJS DI, tsyringe, awilix | manual |

---

## Applying SOLID in Practice

### When to Enforce Strictly

- Domain / business logic layer
- Shared libraries used across features
- Code with high test coverage requirements

### When to Be Pragmatic

- Simple CRUD screens (don't over-abstract)
- Prototypes and throwaway code
- Private implementation details unlikely to change

### SOLID vs. YAGNI Balance

| Scenario | Apply SOLID? |
|----------|-------------|
| 3+ implementations exist or are likely | Yes — create abstraction |
| Only 1 implementation, no tests needed | No — direct dependency is fine |
| Crossing module/layer boundary | Yes — always use interfaces |
| Internal helper within a single class | No — keep it simple |

## Output Format

```markdown
## SOLID Assessment
- **Code/Module:** [what was evaluated]
- **Violations found:** [list with principle and location]

## Recommendations
| Principle | Violation | Refactoring |
|-----------|-----------|-------------|
| SRP | ... | ... |

## Refactored Code
[Before/after examples]
```

## Quality Checklist

- [ ] Each class has a single, clear responsibility
- [ ] New features can be added by extension, not modification of existing classes
- [ ] Subtypes are fully substitutable for their base types
- [ ] Interfaces are small and focused
- [ ] High-level modules depend on abstractions, not concrete implementations
- [ ] DI is used at module boundaries; direct instantiation is fine internally
- [ ] SOLID is applied pragmatically, not dogmatically

## Edge Cases

- Over-applying SRP leads to "class explosion" — dozens of tiny classes that are harder to follow than one medium class. Use judgment.
- In Flutter, widget composition naturally enforces SRP — prefer composing small widgets over creating service classes for UI concerns
- Kotlin's extension functions and Swift's protocol extensions can satisfy OCP without inheritance
- SOLID was designed for OOP. For functional-heavy code (Go, functional Kotlin/Swift), prefer composition and small functions over interface hierarchies
