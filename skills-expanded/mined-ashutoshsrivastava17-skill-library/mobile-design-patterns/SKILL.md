---
name: mobile-design-patterns
description: >
  Understand, compare, and implement mobile design patterns — MVC, MVP, MVVM, MVI,
  Clean Architecture, VIPER, TCA, and BLoC. Covers rationale, data flow, testability,
  and platform-specific implementations across Flutter, Android (Java/Kotlin), and iOS (ObjC/Swift).
  TRIGGER when: user says /mobile-design-patterns, asks about MVC vs MVVM vs MVI,
  needs to understand or choose a mobile architecture pattern, or wants to migrate between patterns.
argument-hint: "[pattern to understand or compare, or codebase to evaluate]"
user-invocable: true
---

# Mobile Design Patterns

You are a senior mobile architect. Help the user understand, compare, choose, or implement mobile design patterns with clear examples and tradeoff analysis.

## Process

### Step 1: Understand the Need

| Question | Why It Matters |
|----------|---------------|
| Are you choosing for a new project or understanding existing code? | Greenfield vs. migration |
| What platform? (Flutter, Android, iOS, or all) | Platform idioms differ |
| What is the app complexity? | Simple apps don't need complex patterns |
| What is the team size? | More developers = more need for strict boundaries |
| What is the team's experience? | Familiar patterns ship faster |
| What are the testing requirements? | Some patterns are far more testable |

### Step 2: Pattern Overview & Comparison

| Pattern | Separation | Testability | Complexity | Learning Curve | Best For |
|---------|-----------|-------------|------------|---------------|----------|
| **MVC** | Low | Low | Low | Easy | Small apps, prototypes, legacy |
| **MVP** | Medium | Medium-High | Medium | Moderate | UIKit/XML apps needing testable presenters |
| **MVVM** | High | High | Medium | Moderate | Most apps — the modern default |
| **MVI** | Very High | Very High | High | Steep | Complex state, undo/redo, time-travel debugging |
| **Clean Architecture** | Very High | Very High | High | Steep | Large apps, long-lived codebases, multiple teams |
| **VIPER** | Very High | Very High | Very High | Steep | Large UIKit apps (less relevant for SwiftUI) |
| **TCA** | Very High | Very High | High | Steep | SwiftUI apps, composability, exhaustive testing |
| **BLoC** | High | Very High | Medium-High | Moderate | Flutter apps, event-driven, stream-based |

---

## Pattern Deep Dives

### MVC (Model-View-Controller)

**Data flow:**
```
User Action → Controller → updates Model
                        → updates View
Model change → Controller → updates View
```

**Roles:**
| Component | Responsibility |
|-----------|---------------|
| **Model** | Data and business logic |
| **View** | Display UI, receive user input |
| **Controller** | Mediates between Model and View, handles user actions |

**The problem:** In mobile, the Controller (Activity/UIViewController) often becomes the View AND Controller — the "Massive View Controller" anti-pattern. Business logic, navigation, networking, and UI all end up in one class.

#### Android (Java) — MVC
```java
// Activity acts as both View and Controller (typical MVC issue)
public class ProductListActivity extends AppCompatActivity {
    private ProductRepository repo;
    private RecyclerView recyclerView;
    private ProductAdapter adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_product_list);

        recyclerView = findViewById(R.id.recycler_view);
        adapter = new ProductAdapter();
        recyclerView.setAdapter(adapter);

        // Controller logic mixed with View
        repo.getProducts(new Callback<List<Product>>() {
            @Override
            public void onSuccess(List<Product> products) {
                adapter.setProducts(products); // View update
            }
            @Override
            public void onError(Exception e) {
                Toast.makeText(ProductListActivity.this, e.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}
```

#### iOS (Objective-C) — MVC
```objc
// UIViewController acts as both View and Controller
@implementation ProductListViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    [self.tableView registerClass:[UITableViewCell class] forCellReuseIdentifier:@"Cell"];

    // Controller logic mixed with View
    [self.repository getProductsWithCompletion:^(NSArray<Product *> *products, NSError *error) {
        dispatch_async(dispatch_get_main_queue(), ^{
            if (error) {
                [self showAlert:error.localizedDescription];
            } else {
                self.products = products;
                [self.tableView reloadData];
            }
        });
    }];
}

// Also acts as data source (more Controller+View mixing)
- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:@"Cell" forIndexPath:indexPath];
    cell.textLabel.text = self.products[indexPath.row].name;
    return cell;
}
@end
```

**When to use:** Prototypes, very simple apps, learning. Avoid for production apps with more than a few screens.

---

### MVP (Model-View-Presenter)

**Data flow:**
```
User Action → View → Presenter → Model
                                    ↓
              View ← Presenter ← Model (result)
```

**Roles:**
| Component | Responsibility |
|-----------|---------------|
| **Model** | Data and business logic |
| **View** | Display UI, delegates all actions to Presenter (passive) |
| **Presenter** | All presentation logic, updates View through interface |

**Key difference from MVC:** The View is passive (implements an interface). The Presenter holds no reference to Android/iOS framework classes, making it unit-testable.

#### Android (Java) — MVP
```java
// View interface
public interface ProductListView {
    void showProducts(List<Product> products);
    void showError(String message);
    void showLoading();
}

// Presenter — fully testable, no Android imports
public class ProductListPresenter {
    private final ProductListView view;
    private final ProductRepository repo;

    public ProductListPresenter(ProductListView view, ProductRepository repo) {
        this.view = view;
        this.repo = repo;
    }

    public void loadProducts() {
        view.showLoading();
        repo.getProducts(new Callback<List<Product>>() {
            @Override
            public void onSuccess(List<Product> products) {
                view.showProducts(products);
            }
            @Override
            public void onError(Exception e) {
                view.showError(e.getMessage());
            }
        });
    }
}

// Activity implements the View interface
public class ProductListActivity extends AppCompatActivity implements ProductListView {
    private ProductListPresenter presenter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        presenter = new ProductListPresenter(this, new ProductRepository());
        presenter.loadProducts();
    }

    @Override
    public void showProducts(List<Product> products) {
        adapter.setProducts(products);
    }

    @Override
    public void showError(String message) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
    }

    @Override
    public void showLoading() { /* show spinner */ }
}
```

#### iOS (Swift) — MVP with UIKit
```swift
// View protocol
protocol ProductListViewProtocol: AnyObject {
    func showProducts(_ products: [Product])
    func showError(_ message: String)
    func showLoading()
}

// Presenter — no UIKit imports
class ProductListPresenter {
    weak var view: ProductListViewProtocol?
    private let repo: ProductRepository

    init(repo: ProductRepository) {
        self.repo = repo
    }

    func loadProducts() {
        view?.showLoading()
        repo.getProducts { [weak self] result in
            switch result {
            case .success(let products):
                self?.view?.showProducts(products)
            case .failure(let error):
                self?.view?.showError(error.localizedDescription)
            }
        }
    }
}

// ViewController implements View protocol
class ProductListViewController: UIViewController, ProductListViewProtocol {
    private let presenter: ProductListPresenter

    func showProducts(_ products: [Product]) {
        self.products = products
        tableView.reloadData()
    }
    // ...
}
```

**When to use:** UIKit or XML-based apps where you need testable presentation logic. Less relevant for Compose/SwiftUI where MVVM is more natural.

---

### MVVM (Model-View-ViewModel)

**Data flow:**
```
User Action → View → ViewModel → Model / Repository
                                        ↓
              View ← (observes) ← ViewModel ← Model (result)
```

**Roles:**
| Component | Responsibility |
|-----------|---------------|
| **Model** | Data, business logic, repository |
| **View** | Display UI, bind to ViewModel observables |
| **ViewModel** | Expose state as observable streams, handle user intents |

**Key difference from MVP:** The View observes the ViewModel reactively (data binding) rather than the Presenter calling View methods imperatively. The ViewModel does NOT hold a reference to the View.

#### Flutter — MVVM with Riverpod
```dart
// ViewModel (Riverpod notifier)
@riverpod
class ProductListViewModel extends _$ProductListViewModel {
  @override
  Future<List<Product>> build() async {
    return ref.read(productRepoProvider).getAll();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(
      () => ref.read(productRepoProvider).getAll(),
    );
  }
}

// View — observes ViewModel reactively
class ProductListScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(productListViewModelProvider);
    return state.when(
      loading: () => const CircularProgressIndicator(),
      error: (e, _) => Text('Error: $e'),
      data: (products) => ListView.builder(
        itemCount: products.length,
        itemBuilder: (_, i) => ProductTile(product: products[i]),
      ),
    );
  }
}
```

#### Android (Kotlin + Compose) — MVVM
```kotlin
// ViewModel — exposes state as StateFlow
class ProductListViewModel(
    private val repo: ProductRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow<UiState<List<Product>>>(UiState.Loading)
    val uiState: StateFlow<UiState<List<Product>>> = _uiState.asStateFlow()

    init { loadProducts() }

    fun loadProducts() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            _uiState.value = try {
                UiState.Success(repo.getAll())
            } catch (e: Exception) {
                UiState.Error(e.message ?: "Unknown error")
            }
        }
    }
}

// View — observes ViewModel
@Composable
fun ProductListScreen(viewModel: ProductListViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    when (val state = uiState) {
        is UiState.Loading -> CircularProgressIndicator()
        is UiState.Error -> Text("Error: ${state.message}")
        is UiState.Success -> LazyColumn {
            items(state.data) { product -> ProductCard(product) }
        }
    }
}
```

#### Android (Java + XML) — MVVM with LiveData
```java
// ViewModel — exposes state as LiveData
public class ProductListViewModel extends ViewModel {
    private final MutableLiveData<List<Product>> products = new MutableLiveData<>();
    private final MutableLiveData<Boolean> loading = new MutableLiveData<>(false);
    private final ProductRepository repo;

    public LiveData<List<Product>> getProducts() { return products; }
    public LiveData<Boolean> isLoading() { return loading; }

    public void loadProducts() {
        loading.setValue(true);
        repo.getAll(result -> {
            loading.postValue(false);
            products.postValue(result);
        });
    }
}

// Activity — observes LiveData
public class ProductListActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ProductListViewModel vm = new ViewModelProvider(this).get(ProductListViewModel.class);

        vm.getProducts().observe(this, products -> {
            adapter.submitList(products);
        });
        vm.isLoading().observe(this, loading -> {
            progressBar.setVisibility(loading ? View.VISIBLE : View.GONE);
        });
        vm.loadProducts();
    }
}
```

#### iOS (Swift + SwiftUI) — MVVM
```swift
// ViewModel — observable state
@Observable  // iOS 17+
class ProductListViewModel {
    var products: [Product] = []
    var isLoading = false
    var errorMessage: String?

    private let repo: ProductRepository

    func loadProducts() async {
        isLoading = true
        defer { isLoading = false }
        do {
            products = try await repo.getAll()
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}

// View — automatic observation
struct ProductListView: View {
    @State private var viewModel = ProductListViewModel(repo: .live)

    var body: some View {
        Group {
            if viewModel.isLoading {
                ProgressView()
            } else {
                List(viewModel.products) { product in
                    ProductRow(product: product)
                }
            }
        }
        .task { await viewModel.loadProducts() }
    }
}
```

#### iOS (Swift + UIKit) — MVVM with Combine
```swift
class ProductListViewModel {
    @Published private(set) var products: [Product] = []
    @Published private(set) var isLoading = false
    private var cancellables = Set<AnyCancellable>()

    func loadProducts() {
        isLoading = true
        repo.getAll()
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { [weak self] _ in self?.isLoading = false },
                receiveValue: { [weak self] in self?.products = $0 }
            )
            .store(in: &cancellables)
    }
}

// UIViewController binds via Combine
class ProductListVC: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        viewModel.$products
            .sink { [weak self] _ in self?.tableView.reloadData() }
            .store(in: &cancellables)
    }
}
```

**When to use:** The default choice for most modern mobile apps. Works naturally with reactive frameworks (Compose, SwiftUI, Flutter).

---

### MVI (Model-View-Intent)

**Data flow:**
```
User Action → Intent (Event) → Reducer → New State → View renders
                                  ↕
                            Side Effects
```

**Roles:**
| Component | Responsibility |
|-----------|---------------|
| **Model** | Immutable state object representing the entire screen |
| **View** | Renders state, emits user Intents (events) |
| **Intent** | User actions as explicit events (sealed class/enum) |
| **Reducer** | Pure function: (State, Intent) → State |
| **Side Effects** | Async operations triggered by Intents |

**Key difference from MVVM:** State is a single immutable object. All changes go through a reducer. This makes state transitions predictable, debuggable, and testable.

#### Flutter — MVI with BLoC
```dart
// State — single immutable object
@freezed
class ProductListState with _$ProductListState {
  const factory ProductListState({
    @Default([]) List<Product> products,
    @Default(false) bool isLoading,
    String? error,
    @Default('') String searchQuery,
  }) = _ProductListState;
}

// Events (Intents)
@freezed
class ProductListEvent with _$ProductListEvent {
  const factory ProductListEvent.loadRequested() = _LoadRequested;
  const factory ProductListEvent.searchChanged(String query) = _SearchChanged;
  const factory ProductListEvent.productDeleted(String id) = _ProductDeleted;
}

// BLoC — reducer + side effects
class ProductListBloc extends Bloc<ProductListEvent, ProductListState> {
  ProductListBloc(this._repo) : super(const ProductListState()) {
    on<_LoadRequested>(_onLoadRequested);
    on<_SearchChanged>(_onSearchChanged, transformer: debounce(300.ms));
  }

  Future<void> _onLoadRequested(event, emit) async {
    emit(state.copyWith(isLoading: true, error: null));
    try {
      final products = await _repo.getAll();
      emit(state.copyWith(isLoading: false, products: products));
    } catch (e) {
      emit(state.copyWith(isLoading: false, error: e.toString()));
    }
  }
}
```

#### Android (Kotlin) — MVI
```kotlin
// State
data class ProductListState(
    val products: List<Product> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val searchQuery: String = ""
)

// Intent (Event)
sealed interface ProductListIntent {
    data object LoadRequested : ProductListIntent
    data class SearchChanged(val query: String) : ProductListIntent
    data class ProductDeleted(val id: String) : ProductListIntent
}

// ViewModel as state machine
class ProductListViewModel(private val repo: ProductRepository) : ViewModel() {
    private val _state = MutableStateFlow(ProductListState())
    val state: StateFlow<ProductListState> = _state.asStateFlow()

    fun onIntent(intent: ProductListIntent) {
        when (intent) {
            is ProductListIntent.LoadRequested -> loadProducts()
            is ProductListIntent.SearchChanged -> search(intent.query)
            is ProductListIntent.ProductDeleted -> delete(intent.id)
        }
    }

    private fun loadProducts() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true, error = null) }
            try {
                val products = repo.getAll()
                _state.update { it.copy(isLoading = false, products = products) }
            } catch (e: Exception) {
                _state.update { it.copy(isLoading = false, error = e.message) }
            }
        }
    }
}
```

#### iOS (Swift) — MVI with TCA
```swift
@Reducer
struct ProductListFeature {
    @ObservableState
    struct State: Equatable {
        var products: [Product] = []
        var isLoading = false
        var searchQuery = ""
        @Presents var alert: AlertState<Action.Alert>?
    }

    enum Action {
        case loadRequested
        case productsLoaded(Result<[Product], Error>)
        case searchChanged(String)
        case alert(PresentationAction<Alert>)
        enum Alert: Equatable {}
    }

    @Dependency(\.productClient) var productClient

    var body: some ReducerOf<Self> {
        Reduce { state, action in
            switch action {
            case .loadRequested:
                state.isLoading = true
                return .run { send in
                    await send(.productsLoaded(Result {
                        try await productClient.getAll()
                    }))
                }
            case .productsLoaded(.success(let products)):
                state.isLoading = false
                state.products = products
                return .none
            case .productsLoaded(.failure(let error)):
                state.isLoading = false
                state.alert = AlertState { TextState(error.localizedDescription) }
                return .none
            case .searchChanged(let query):
                state.searchQuery = query
                return .none
            case .alert:
                return .none
            }
        }
    }
}
```

**When to use:** Complex screens with many interacting state fields, undo/redo, time-travel debugging, or when state predictability is critical.

---

### Clean Architecture

**Layer structure:**
```
┌─────────────────────┐
│    Presentation     │  ← UI, ViewModels, Widgets
├─────────────────────┤
│      Domain         │  ← Use Cases, Entities, Repository Interfaces
├─────────────────────┤
│       Data          │  ← Repository Impls, APIs, Database, DTOs
└─────────────────────┘

Dependency rule: outer layers depend on inner layers, NEVER the reverse.
Domain layer has ZERO external dependencies.
```

**Roles:**
| Layer | Contains | Depends On |
|-------|----------|-----------|
| **Domain** | Entities, Use Cases, Repository interfaces | Nothing (pure language) |
| **Data** | Repository impls, API clients, DB, DTOs, mappers | Domain (implements interfaces) |
| **Presentation** | UI, ViewModels/BLoCs, navigation | Domain (uses Use Cases) |

**Clean Architecture applies ON TOP of any presentation pattern (MVVM, MVI, BLoC).**

#### Flutter — Clean Architecture + BLoC
```
lib/
  features/
    products/
      domain/
        entities/product.dart           # Pure Dart class
        repositories/product_repo.dart  # Abstract class (interface)
        usecases/get_products.dart      # Single-purpose use case
      data/
        models/product_model.dart       # DTO with fromJson/toJson
        datasources/product_api.dart    # HTTP client
        datasources/product_local.dart  # Local DB
        repositories/product_repo_impl.dart  # Implements domain interface
      presentation/
        bloc/product_list_bloc.dart     # BLoC using use cases
        pages/product_list_page.dart    # Widget
        widgets/product_card.dart       # Reusable widget
```

#### Android — Clean Architecture + MVVM
```
app/
  features/
    products/
      domain/
        model/Product.kt               # Domain entity (no annotations)
        repository/ProductRepository.kt # Interface
        usecase/GetProductsUseCase.kt   # Single-purpose use case
      data/
        model/ProductDto.kt            # API/DB model with annotations
        mapper/ProductMapper.kt        # DTO ↔ Domain mapping
        remote/ProductApi.kt           # Retrofit interface
        local/ProductDao.kt            # Room DAO
        repository/ProductRepositoryImpl.kt
      presentation/
        ProductListViewModel.kt        # Uses use cases, exposes StateFlow
        ProductListScreen.kt           # Compose UI
```

#### iOS — Clean Architecture + MVVM
```
App/
  Features/
    Products/
      Domain/
        Entities/Product.swift          # Plain Swift struct
        Repositories/ProductRepository.swift  # Protocol
        UseCases/GetProductsUseCase.swift
      Data/
        DTOs/ProductDTO.swift           # Codable struct
        DataSources/ProductAPI.swift    # URLSession/Alamofire
        DataSources/ProductLocalDB.swift
        Repositories/ProductRepositoryImpl.swift
      Presentation/
        ProductListViewModel.swift      # @Observable, uses use cases
        ProductListView.swift           # SwiftUI view
```

**When to use:** Large apps with multiple developers, long-lived codebases, or when strict testability and separation are required. Overkill for small apps.

---

### VIPER

**Components:**
| Component | Responsibility |
|-----------|---------------|
| **View** | Display UI (passive, like MVP) |
| **Interactor** | Business logic (like Use Case) |
| **Presenter** | Presentation logic, mediates View ↔ Interactor |
| **Entity** | Data models |
| **Router** | Navigation logic |

**When to use:** Large UIKit apps. Largely superseded by Clean Architecture + MVVM for modern development. Avoid for SwiftUI/Compose (too many abstractions for declarative UI).

---

## Step 3: Decision Guide

```
Is the app small (< 5 screens)?
  → MVVM (simple ViewModel per screen)

Is the app medium (5-20 screens)?
  → MVVM with Repository pattern

Is the app large (20+ screens, multiple devs)?
  → Clean Architecture + MVVM or MVI

Does state management need strict predictability?
  → MVI (BLoC for Flutter, TCA for iOS)

Is this a legacy UIKit/XML app?
  → MVP (if refactoring from MVC) or MVVM with UIKit binding

Is this a legacy Objective-C/Java app?
  → MVC (existing) → migrate to MVP → then MVVM as you modernize
```

## Step 4: Migration Paths

| From | To | Strategy |
|------|-----|---------|
| **MVC → MVP** | Extract Presenter from Controller, define View interface | Screen by screen |
| **MVC → MVVM** | Extract ViewModel, add reactive bindings | Screen by screen |
| **MVP → MVVM** | Replace View interface with reactive observation | Replace Presenter with ViewModel |
| **MVVM → MVI** | Unify state into single object, add event/intent layer | Feature by feature |
| **Any → Clean Architecture** | Add domain layer (entities + use cases + interfaces), then refactor data layer | Layer by layer, domain first |

**Rule:** Never rewrite. Always migrate incrementally — one screen or one feature at a time.

## Output Format

```markdown
## Pattern Recommendation
- **Pattern:** [MVVM / MVI / Clean Architecture + MVVM / etc.]
- **Platform:** [Flutter / Android / iOS]
- **Rationale:** [Why this pattern for this context]

## Architecture Diagram
[Layer diagram with data flow arrows]

## Example Implementation
[Key classes and their relationships]

## Testing Strategy
[What is testable and how]

## Migration Plan (if applicable)
[Step-by-step migration from current pattern]
```

## Quality Checklist

- [ ] Pattern complexity matches app complexity (no over-engineering)
- [ ] Business logic is testable without UI framework
- [ ] Data flow direction is consistent and documented
- [ ] Team understands the pattern (not just the architect)
- [ ] Navigation is handled explicitly (not scattered across views)
- [ ] Pattern is applied consistently across features

## Edge Cases

- Mixing patterns within one app is fine during migration — enforce consistency per feature, not globally
- For Kotlin Multiplatform, the domain and data layers can be shared; only the presentation layer is platform-specific
- SwiftUI's opinionated state management (@State, @Environment) can conflict with external patterns — embrace it for local state, use ViewModel/TCA for feature state
- BLoC is Flutter-specific. If sharing concepts across Flutter and native, consider aligning on MVI terminology instead
- VIPER generates many files per feature — use code generation templates (Xcode templates, Android Studio templates) if you adopt it
