---
name: mobile-state-management
description: >
  Choose, design, and review state management in mobile apps — local vs. global state,
  reactive patterns, state persistence, and platform-specific solutions across
  Flutter (BLoC, Riverpod, Provider), Android (ViewModel, StateFlow), and iOS (SwiftUI Observation, Combine).
  TRIGGER when: user says /mobile-state-management, asks about managing state in a mobile app,
  needs to choose a state management approach, or wants to debug state-related issues.
argument-hint: "[app or feature with state management needs]"
user-invocable: true
---

# Mobile State Management

You are a senior mobile engineer. Help the user choose, design, or review state management patterns that are predictable, testable, and scalable.

## Process

### Step 1: Understand State Requirements

| Question | Why It Matters |
|----------|---------------|
| What kind of state? (UI, app, server, form) | Determines scope and persistence |
| How many screens share this state? | Local vs. global state boundary |
| Does state need to survive process death? | Persistence and restoration strategy |
| How frequently does state change? | Performance and rebuild optimization |
| Is there optimistic UI or offline mutation? | Sync and conflict resolution needs |
| What is the team's familiarity with reactive patterns? | Pragmatic solution selection |

### Step 2: Classify State Types

| Type | Scope | Examples | Persistence |
|------|-------|---------|-------------|
| **UI State** | Single widget/screen | Text field value, scroll position, animation | None or SavedState |
| **Feature State** | Single feature/flow | Form data, step in a wizard, filter selection | Session or SavedState |
| **App State** | Entire app | Auth status, user profile, theme, locale | Persistent storage |
| **Server State** | Cache of remote data | API responses, paginated lists, real-time feeds | Cache with TTL |

**Rule of thumb:** Keep state as local as possible. Only lift state when two or more independent components need it.

### Step 3: Select Approach by Platform

#### Flutter

| Solution | State Scope | Complexity | Best For |
|----------|-------------|------------|----------|
| **setState / ValueNotifier** | Local (single widget) | Low | Simple UI state, prototypes |
| **Provider** | Local to global | Low-Medium | Small-medium apps, simple DI |
| **Riverpod** | Local to global | Medium | Medium-large apps, compile-safe, testable |
| **BLoC / Cubit** | Feature to global | Medium-High | Large apps, event-driven, strict separation |
| **GetX** | Global | Low | Rapid prototyping only |
| **Signals (flutter_signals)** | Local to global | Low-Medium | Fine-grained reactivity, minimal rebuilds |

**Recommended patterns:**
```dart
// Riverpod — feature state with async data
@riverpod
class ProductList extends _$ProductList {
  @override
  Future<List<Product>> build() => ref.read(productRepoProvider).getAll();

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(
      () => ref.read(productRepoProvider).getAll(),
    );
  }
}

// BLoC — event-driven state
class CartBloc extends Bloc<CartEvent, CartState> {
  CartBloc(this._repo) : super(const CartState.initial()) {
    on<AddToCart>(_onAddToCart);
    on<RemoveFromCart>(_onRemoveFromCart);
  }
}
```

#### Android (Kotlin & Java)

| Solution | Language | State Scope | Complexity | Best For |
|----------|----------|-------------|------------|----------|
| **Compose remember / mutableStateOf** | Kotlin | Local (single composable) | Low | UI state within a composable |
| **ViewModel + StateFlow** | Kotlin | Feature (screen-level) | Medium | Standard modern approach — recommended default |
| **ViewModel + MVI (sealed class events)** | Kotlin | Feature | Medium-High | Complex screens, predictable state |
| **ViewModel + LiveData** | Kotlin/Java | Feature (screen-level) | Medium | UIKit/XML Views apps, Java compatibility |
| **RxJava + ViewModel** | Java/Kotlin | Feature to global | Medium-High | Legacy reactive apps |
| **DataStore / Room + Flow** | Kotlin | App-wide / persistent | Medium | Preferences, cached data |
| **SharedPreferences + LiveData** | Java | App-wide / persistent | Low | Legacy persistent state |
| **Redux-style (Mobius, Workflow)** | Kotlin | App-wide | High | Very complex state, strict unidirectional flow |
| **EventBus** | Java | Global (broadcast) | Low | Legacy apps (avoid — hard to debug) |

**Modern (Kotlin + Compose):**
```kotlin
// ViewModel + StateFlow — standard approach
class ProductListViewModel(
    private val repo: ProductRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow<ProductListUiState>(Loading)
    val uiState: StateFlow<ProductListUiState> = _uiState.asStateFlow()

    fun loadProducts() {
        viewModelScope.launch {
            _uiState.value = try {
                Success(repo.getAll())
            } catch (e: Exception) {
                Error(e.message)
            }
        }
    }
}

// MVI — sealed events + reduce
sealed interface ProductListEvent {
    data object LoadRequested : ProductListEvent
    data class FilterChanged(val filter: Filter) : ProductListEvent
}
```

**Legacy (Java + XML Views):**
```java
// ViewModel + LiveData — Java approach
public class ProductListViewModel extends ViewModel {
    private final MutableLiveData<UiState> uiState = new MutableLiveData<>(new Loading());
    private final ProductRepository repo;

    public LiveData<UiState> getUiState() { return uiState; }

    public void loadProducts() {
        uiState.setValue(new Loading());
        repo.getAll(new Callback<List<Product>>() {
            @Override
            public void onSuccess(List<Product> products) {
                uiState.postValue(new Success(products));
            }
            @Override
            public void onError(Exception e) {
                uiState.postValue(new Error(e.getMessage()));
            }
        });
    }
}

// RxJava approach
public class ProductListViewModel extends ViewModel {
    private final CompositeDisposable disposables = new CompositeDisposable();

    public void loadProducts() {
        disposables.add(repo.getAll()
            .subscribeOn(Schedulers.io())
            .observeOn(AndroidSchedulers.mainThread())
            .subscribe(
                products -> uiState.setValue(new Success(products)),
                error -> uiState.setValue(new Error(error.getMessage()))
            ));
    }
}
```

**Migration path:** LiveData → StateFlow, RxJava → Coroutines + Flow, EventBus → SharedFlow
```

#### iOS (Swift & Objective-C)

| Solution | Language | UI Toolkit | State Scope | Complexity | Best For |
|----------|----------|-----------|-------------|------------|----------|
| **@State / @Binding** | Swift | SwiftUI | Local (single view) | Low | Simple UI state within a view |
| **@Observable class (iOS 17+)** | Swift | SwiftUI | Feature | Low-Medium | Modern SwiftUI — recommended default |
| **ObservableObject + @Published** | Swift | SwiftUI | Feature | Medium | iOS 15-16 compatible |
| **TCA (ComposableArchitecture)** | Swift | SwiftUI | Feature to app-wide | High | Large apps, exhaustive testing |
| **Combine pipelines** | Swift | Both | Feature to app-wide | Medium-High | Reactive chains, complex async |
| **ViewModel + Delegates** | Swift | UIKit | Feature | Medium | UIKit MVVM without reactive |
| **RxSwift + RxCocoa** | Swift/ObjC | UIKit | Feature to global | Medium-High | Reactive UIKit apps |
| **KVO (Key-Value Observing)** | ObjC/Swift | UIKit | Property-level | Medium | Legacy Objective-C observation |
| **NSNotificationCenter** | ObjC/Swift | Both | Global broadcast | Low | Legacy cross-component events |
| **Delegation pattern** | ObjC/Swift | UIKit | 1-to-1 communication | Low | Classic UIKit pattern |

**Modern (Swift + SwiftUI):**
```swift
// @Observable (iOS 17+) — modern approach
@Observable
class ProductListViewModel {
    var products: [Product] = []
    var isLoading = false
    var error: String?

    private let repo: ProductRepository

    func loadProducts() async {
        isLoading = true
        defer { isLoading = false }
        do {
            products = try await repo.getAll()
        } catch {
            self.error = error.localizedDescription
        }
    }
}

// TCA — composable, testable
@Reducer
struct ProductListFeature {
    @ObservableState
    struct State: Equatable {
        var products: [Product] = []
        var isLoading = false
    }
    enum Action {
        case loadProducts
        case productsLoaded(Result<[Product], Error>)
    }
    var body: some ReducerOf<Self> { ... }
}
```

**UIKit + Swift (MVVM with Combine):**
```swift
// ViewModel with Combine publishers for UIKit binding
class ProductListViewModel {
    @Published private(set) var products: [Product] = []
    @Published private(set) var isLoading = false

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

// In UIViewController
viewModel.$products
    .receive(on: DispatchQueue.main)
    .sink { [weak self] products in
        self?.tableView.reloadData()
    }
    .store(in: &cancellables)
```

**Legacy (Objective-C):**
```objc
// KVO-based observation
[self.viewModel addObserver:self
                 forKeyPath:@"products"
                    options:NSKeyValueObservingOptionNew
                    context:nil];

// Delegate pattern
@protocol ProductListViewModelDelegate <NSObject>
- (void)viewModelDidUpdateProducts:(NSArray<Product *> *)products;
- (void)viewModelDidFailWithError:(NSError *)error;
@end

// NSNotificationCenter broadcast
[[NSNotificationCenter defaultCenter]
    postNotificationName:@"ProductsDidUpdate"
    object:self
    userInfo:@{@"products": products}];
```

**Migration path:** KVO/Delegates → Combine → @Observable, RxSwift → Combine, NSNotificationCenter → @Published/SharedFlow
```

### Step 4: Design State Flow

Define how state moves through the system:

```
User Action → Event/Intent → State Logic (BLoC/ViewModel/Reducer) → New State → UI Rebuild
                                    ↕
                            Side Effects (API calls, DB writes, analytics)
```

**Key principles:**
- State flows in one direction (unidirectional data flow)
- UI reads state, never mutates it directly
- Side effects are explicit and managed (not scattered in UI code)
- State transitions are deterministic (same input → same output)

### Step 5: Handle Common Patterns

| Pattern | How to Handle |
|---------|--------------|
| **Loading / Error / Success** | Use sealed classes or union types (AsyncValue in Riverpod, sealed class in Kotlin, enum in Swift) |
| **Pagination** | Append-only list state with page cursor, loading-more flag, and end-of-list detection |
| **Optimistic updates** | Apply change immediately to UI state, queue mutation, rollback on failure |
| **Form state** | Local state per field with validation; lift to feature state on submit |
| **Process death** | Save critical state to SavedStateHandle (Android), @SceneStorage (iOS), or hydrated_bloc (Flutter) |
| **Debounced search** | Debounce user input events before triggering API call; cancel in-flight requests |

## Output Format

```markdown
## State Management Summary
- **Platform:** [Flutter / Android / iOS]
- **Approach:** [BLoC / Riverpod / ViewModel+StateFlow / @Observable / TCA]
- **State Types:** [What state exists and its classification]

## State Diagram
[State types, their scope, and how they flow]

## Implementation Outline
[Key classes/files and their responsibilities]

## Testing Strategy
[How to unit test state logic in isolation]

## Risks
| Risk | Mitigation |
|------|------------|
| ... | ... |
```

## Quality Checklist

- [ ] State is classified by scope (UI, feature, app, server)
- [ ] No business logic in UI layer — all in state holder (ViewModel/BLoC/Reducer)
- [ ] State transitions are testable in isolation without UI framework
- [ ] Loading, error, and empty states are explicitly modeled
- [ ] Side effects are managed and cancellable
- [ ] No unnecessary global state — state is as local as possible
- [ ] Process death and state restoration are handled for critical flows

## Edge Cases

- If migrating state management libraries (e.g., Provider → Riverpod), migrate feature by feature, not all at once
- For shared state across Flutter and native (in add-to-app scenarios), use platform channels or Pigeon for state synchronization
- For real-time collaborative features, consider CRDTs or operational transforms rather than simple last-write-wins
- If state logic is identical across platforms (KMP), consider sharing the domain/state layer via Kotlin Multiplatform
