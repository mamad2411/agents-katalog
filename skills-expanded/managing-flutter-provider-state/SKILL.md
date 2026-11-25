---
name: "managing-flutter-provider-state"
description: "Provider (v6.x) state management for Flutter using ChangeNotifier and InheritedWidget with MVVM architecture pattern. Use this skill when implementing Provider-based state management, using Consumer/Consumer2 widgets for targeted rebuilds, accessing state with context.read/context.watch/context.select, setting up ChangeNotifierProvider or StateNotifierProvider, configuring MultiProvider for multiple providers, implementing ProxyProvider for dependent state, using Selector for optimized rebuilds, migrating from StatefulWidget to reactive state, maintaining legacy Provider codebases, debugging provider not found errors, preventing memory leaks with proper ChangeNotifier disposal, fixing context access issues in initState, or resolving .value constructor anti-patterns. Essential for apps with shared state across widgets (shopping carts, authentication, global settings, form state, theme management), when teaching state management fundamentals, or when debugging memory leaks and resource cleanup in Provider-based applications."
metadata:
  last_modified: "2026-04-01 14:35:00 (GMT+8)"
---

# Provider State Management Guide (v6.x)

## Goal
Implement state management and dependency injection using the `provider` package in Flutter applications. Provider is built on Flutter's native `InheritedWidget` and remains the foundation for many production apps worldwide. This guide enforces MVVM (Model-View-ViewModel) architecture patterns and eliminates unnecessary widget rebuilds through targeted state consumption.

## Process

### Phase 1: Understand State Scope

Before implementing Provider, determine if the state truly needs to be shared:

- **Ephemeral State** (local): Use `StatefulWidget` + `setState()` for UI state confined to a single widget (e.g., form input, animation progress, current tab index).
- **App State** (shared): Use Provider when multiple unrelated widgets need access to the same data (e.g., user auth, shopping cart, app settings).

If uncertain about the scope, ask the user to clarify the intended lifecycle and accessibility requirements.

### Phase 2: Install Dependencies

```yaml
dependencies:
  provider: ^6.1.5
```

### Phase 3: Implement MVVM Architecture

#### A. Create the Model Layer (Data / Repository)
Handle low-level data operations (HTTP requests, database queries, caching):

```dart
class UserRepository {
  Future<User> fetchUser(String id) async {
    // API call or database query
    return User(id: id, name: 'John Doe');
  }
}
```

**Constraints**: Models MUST NOT reference `ChangeNotifier`, `BuildContext`, or any UI code.

#### B. Create the ViewModel Layer
Extend `ChangeNotifier` to hold UI state and expose commands:

```dart
class UserViewModel extends ChangeNotifier {
  final UserRepository _repository;
  
  UserViewModel(this._repository);

  User? _user;
  User? get user => _user;

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  String? _errorMessage;
  String? get errorMessage => _errorMessage;

  // Command invoked by View
  Future<void> loadUser(String id) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners(); // Trigger loading UI

    try {
      _user = await _repository.fetchUser(id);
    } catch (e) {
      _errorMessage = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners(); // Trigger success/error UI
    }
  }
}
```

**Critical**: Always call `notifyListeners()` after state mutations to trigger widget rebuilds.

#### C. Provide State to Widget Tree
Use `MultiProvider` to inject dependencies at the root or page level:

```dart
void main() {
  runApp(
    MultiProvider(
      providers: [
        Provider(create: (_) => UserRepository()),
        ChangeNotifierProvider(
          create: (context) => UserViewModel(
            context.read<UserRepository>(),
          ),
        ),
      ],
      child: const MyApp(),
    ),
  );
}
```

**Best Practice**: Provide state as close to its usage point as possible. Avoid putting every provider at the app root if only used in specific screens.

#### D. Consume State in View Layer

**For reading state in `build()` method**:

Use `Consumer` or `Selector` to minimize rebuild scope:

```dart
class UserProfileView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Profile')),
      body: Consumer<UserViewModel>(
        builder: (context, viewModel, child) {
          if (viewModel.isLoading) {
            return Center(child: CircularProgressIndicator());
          }
          
          if (viewModel.errorMessage != null) {
            return Center(child: Text('Error: ${viewModel.errorMessage}'));
          }
          
          if (viewModel.user != null) {
            return Center(child: Text('Hello, ${viewModel.user!.name}'));
          }
          
          return Center(child: Text('No user loaded'));
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => context.read<UserViewModel>().loadUser('123'),
        child: Icon(Icons.refresh),
      ),
    );
  }
}
```

**For executing commands** (event handlers, callbacks):

Use `context.read<T>()` with `listen: false`:

```dart
// ✅ CORRECT: No rebuild triggered on button widget
onPressed: () => context.read<CartModel>().addItem(item),

// ❌ WRONG: Causes infinite rebuild loops
onPressed: () => Provider.of<CartModel>(context).addItem(item),
```

### Phase 4: Memory Management & Resource Cleanup

#### ⚠️ CRITICAL: .value vs create Constructor

**This is the #1 cause of memory leaks in Provider 6.x applications.**

Provider offers two constructors for providing objects. Understanding when to use each is essential:

**Rule:**
- ✅ Use `create` for objects **YOU create and manage** (Provider will call `dispose()` automatically)
- ❌ Use `.value` **ONLY** for pre-existing instances you manage elsewhere (Provider will NOT call `dispose()`)

**Anti-pattern (Memory Leak):**

```dart
// ❌ WRONG: Creates a new instance but .value won't dispose it!
ChangeNotifierProvider.value(
  value: MyNotifier(), // MEMORY LEAK - never disposed!
  child: MyWidget(),
)
```

**Why it leaks**: The `.value` constructor assumes you're passing in an instance that already exists and will be disposed elsewhere. Creating a new instance here means it will never be cleaned up.

**Correct Pattern:**

```dart
// ✅ CORRECT: create constructor manages lifecycle
ChangeNotifierProvider(
  create: (_) => MyNotifier(),
  child: MyWidget(),
)
```

**When to actually use `.value`:**

```dart
// ✅ CORRECT: Reusing an existing instance from parent scope
final existingNotifier = context.watch<MyNotifier>();

return ChangeNotifierProvider.value(
  value: existingNotifier, // Pre-existing instance
  child: ChildWidget(),
)
```

#### ChangeNotifier Disposal Checklist

Every `ChangeNotifier` subclass **MUST** implement `dispose()` and clean up all resources:

```dart
class MyViewModel extends ChangeNotifier {
  StreamSubscription? _subscription;
  Timer? _timer;
  TextEditingController? _controller;
  
  MyViewModel() {
    _subscription = someStream.listen(_onData);
    _timer = Timer.periodic(Duration(seconds: 1), _onTick);
    _controller = TextEditingController();
  }
  
  @override
  void dispose() {
    // Cancel ALL subscriptions
    _subscription?.cancel();
    
    // Cancel ALL timers
    _timer?.cancel();
    
    // Dispose ALL controllers
    _controller?.dispose();
    
    // Close ALL streams you own
    // _myStreamController?.close();
    
    // ALWAYS call super.dispose() last
    super.dispose();
  }
}
```

**Checklist** - Before shipping, verify each `ChangeNotifier` cleans up:
- [ ] StreamSubscriptions (`.cancel()`)
- [ ] Timers (`.cancel()`)
- [ ] TextEditingControllers (`.dispose()`)
- [ ] AnimationControllers (`.dispose()`)
- [ ] FocusNodes (`.dispose()`)
- [ ] ScrollControllers (`.dispose()`)
- [ ] StreamControllers you own (`.close()`)
- [ ] Any platform resources (camera, location services, etc.)

**Testing for leaks**: Use Flutter DevTools Memory tab to verify instances are released when navigating away from screens.

#### Context Access Patterns & Solutions

**Problem**: "Provider not found" or "Bad state" errors when accessing providers in `initState`.

```dart
// ❌ WRONG: Context not ready during initState
@override
void initState() {
  super.initState();
  final provider = context.watch<MyProvider>(); // Error!
}
```

**Solution 1**: Access providers in `build()` method

```dart
@override
Widget build(BuildContext context) {
  final provider = context.watch<MyProvider>(); // ✅ Works
  return ...;
}
```

**Solution 2**: Use `didChangeDependencies` lifecycle method

```dart
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  // Context is ready here
  final provider = context.read<MyProvider>();
  provider.loadInitialData();
}
```

**Solution 3**: Use `context.read` for one-time initialization

```dart
@override
void initState() {
  super.initState();
  // Schedule for after first frame
  WidgetsBinding.instance.addPostFrameCallback((_) {
    context.read<MyProvider>().initialize();
  });
}
```

**Critical Distinction**:
- `context.watch<T>()` - Subscribes to changes, triggers rebuilds (use in `build()`)
- `context.read<T>()` - One-time access, no subscription (use in callbacks/lifecycle methods)
- `context.select<T, R>()` - Subscribes to specific property (use in `build()` for granular rebuilds)

### Phase 5: Advanced Patterns

#### Using Selector for Granular Rebuilds

When a widget only needs a small part of a large model:

```dart
Selector<UserModel, String>(
  selector: (context, user) => user.name,
  builder: (context, name, child) {
    // Only rebuilds when user.name changes
    return Text('Hello, $name');
  },
)
```

#### Using ProxyProvider for Dependent Services

When a ViewModel depends on another Provider:

```dart
MultiProvider(
  providers: [
    ChangeNotifierProvider(create: (_) => AuthProvider()),
    ProxyProvider<AuthProvider, CartService>(
      update: (context, auth, previous) => CartService(auth.userId),
    ),
  ],
  child: MyApp(),
)
```

---

## Reference Documentation

For detailed implementation guides:

- [Provider Best Practices (v6.x)](./references/provider.md) - Complete implementation guide with advanced patterns
- [State Management Overview](./references/state-management-overview.md) - Fundamental concepts and decision logic

---

## Constraints

* **No Business Logic in Views**: StatelessWidget and StatefulWidget MUST only contain UI and layout logic. All data transformation belongs in ViewModels.
* **Strict UDF**: Data flows down (Repository → ViewModel → View). Events flow up (View → ViewModel → Repository). Views NEVER mutate Repository data directly.
* **Targeted Rebuilds**: Never use `Provider.of<T>(context)` with `listen: true` at the root of large build methods. Use `Consumer<T>` or `Selector<T, R>` to scope rebuilds.
* **Command Invocation**: When calling ViewModel methods from event handlers, MUST use `context.read<T>()` or `Provider.of<T>(context, listen: false)`.
* **No context.watch in initState**: Prohibited from using `watch` inside `initState()`. Use `context.read` instead or `didChangeDependencies()`.
* **ChangeNotifier Separation**: ViewModels MUST NOT contain UI elements, rendering code, or BuildContext references. This ensures testability.
* **Mandatory Disposal**: Every `ChangeNotifier` MUST implement `dispose()` and clean up all subscriptions, timers, controllers, and resources. Use `create` constructor (not `.value`) when creating new instances.
* **Memory Leak Prevention**: NEVER use `ChangeNotifierProvider.value(value: NewInstance())`. Always use `ChangeNotifierProvider(create: (_) => NewInstance())` for proper lifecycle management.
