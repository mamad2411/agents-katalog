# Mobile Development Standards

**Version**: 2.7.0  
**Applies to**: iOS, Android, React Native, Flutter  
**Last Updated**: 2026-04-09

---

## 🎯 Core Principles

Mobile development requires unique constraints: limited battery, memory, network conditions, screen sizes, touch interaction, and platform-specific APIs. This standard covers native mobile (iOS/Android) and cross-platform frameworks (React Native, Flutter).

---

## 📱 Platform-Specific Standards

### iOS (Swift)

**Project Structure**
```
MyApp/
├── App/
│   ├── AppDelegate.swift
│   ├── SceneDelegate.swift
│   └── Main.storyboard
├── Scenes/
│   ├── Home/
│   │   ├── HomeViewController.swift
│   │   ├── HomeViewModel.swift
│   │   └── HomeView.swift
│   └── Detail/
├── Services/
│   ├── APIClient.swift
│   ├── DatabaseService.swift
│   └── LocationService.swift
├── Models/
├── Utils/
└── Resources/
    ├── Localizable.strings
    ├── Assets.xcassets
    └── Fonts/
```

**Swift Code Standards**
- Use Swift 5.9+ features (async/await, actors for thread safety)
- Prefer SwiftUI over UIKit for new screens
- MVVM architecture: ViewController → ViewModel → Model
- View Models use `@Published` properties with `@StateObject` binding
- Network calls: use `URLSession` with async/await, never synchronous
- Thread safety: `@MainActor` for UI updates, `nonisolated` for background work
- Memory: weak self in closures, use value types (struct) over reference types (class)
- Optionals: favor `guard let` over force unwrap, use `??` for defaults
- Error handling: custom `Error` enum with `LocalizedError` conformance
- No hardcoded strings: use `NSLocalizedString()` or Localizable.strings

**Example: Network Service**
```swift
@MainActor
final class UserAPIClient {
    static let shared = UserAPIClient()
    
    private let session: URLSession
    
    func fetchUsers() async throws -> [User] {
        let url = URL(string: "https://api.example.com/users")!
        let (data, response) = try await session.data(from: url)
        
        guard (response as? HTTPURLResponse)?.statusCode == 200 else {
            throw APIError.invalidResponse
        }
        
        return try JSONDecoder().decode([User].self, from: data)
    }
}

final class UserViewModel: ObservableObject {
    @Published var users: [User] = []
    @Published var isLoading = false
    @Published var error: APIError?
    
    func loadUsers() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            users = try await UserAPIClient.shared.fetchUsers()
        } catch let error as APIError {
            self.error = error
        }
    }
}
```

**Testing**
- Unit tests: XCTest with mocked dependencies
- UI tests: XCUITest for critical user flows
- Performance: measure with `XCTestMetrics`

---

### Android (Kotlin)

**Project Structure**
```
MyApp/
├── java/com/example/myapp/
│   ├── MainActivity.kt
│   ├── ui/
│   │   ├── home/
│   │   │   ├── HomeFragment.kt
│   │   │   ├── HomeViewModel.kt
│   │   │   └── HomeActivity.kt
│   │   └── detail/
│   ├── data/
│   │   ├── api/
│   │   │   └── ApiService.kt
│   │   ├── db/
│   │   │   └── AppDatabase.kt
│   │   └── repository/
│   │       └── UserRepository.kt
│   ├── domain/
│   │   └── model/
│   │       └── User.kt
│   └── di/
│       └── AppModule.kt
├── res/
│   ├── layout/
│   ├── drawable/
│   ├── values/
│   │   ├── strings.xml
│   │   └── colors.xml
│   └── anim/
└── AndroidManifest.xml
```

**Kotlin Code Standards**
- Kotlin 1.9+, use coroutines for async (never Thread.sleep or blocking calls)
- Architecture: MVVM with Jetpack libraries (ViewModel, LiveData/StateFlow, Room, Hilt)
- Fragment-based UI: single Activity + multiple Fragments with Navigation Component
- State management: `ViewModel` + `StateFlow` for reactive updates
- Dependency injection: Hilt with `@Module`, `@Provides`, `@Singleton`
- Network: Retrofit with OkHttp, coroutine adapters
- Database: Room with typed DAOs, migrations, live updates
- Lifecycle awareness: use `lifecycleScope` for coroutines, avoid memory leaks
- Permissions: use Jetpack Security library, request at runtime
- No hardcoded strings: use `@StringRes` or strings.xml
- Build types: debug (with logging), release (proguard enabled)

**Example: Network + ViewModel**
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {
    
    private val _users = MutableStateFlow<List<User>>(emptyList())
    val users: StateFlow<List<User>> = _users.asStateFlow()
    
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()
    
    fun loadUsers() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                _users.value = userRepository.getUsers()
            } finally {
                _isLoading.value = false
            }
        }
    }
}

@Dao
interface UserDao {
    @Query("SELECT * FROM users WHERE isDeleted = 0 ORDER BY name ASC")
    fun getAllUsers(): Flow<List<User>>
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUsers(users: List<User>)
}
```

**Testing**
- Unit tests: JUnit + Mockito
- Instrumentation tests: AndroidX Test + Espresso for UI
- Test database: in-memory Room instance

---

## 🚀 React Native Standards

**Project Structure**
```
MyApp/
├── src/
│   ├── screens/
│   │   ├── HomeScreen.tsx
│   │   ├── DetailScreen.tsx
│   │   └── index.ts
│   ├── components/
│   │   ├── UserCard.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── index.ts
│   ├── hooks/
│   │   ├── useUserAPI.ts
│   │   └── useAsync.ts
│   ├── services/
│   │   ├── api.ts
│   │   └── storage.ts
│   ├── types/
│   │   └── index.ts
│   ├── navigation/
│   │   └── RootNavigator.tsx
│   ├── App.tsx
│   └── index.ts
├── app.json
├── tsconfig.json
└── package.json
```

**TypeScript Standards**
- React Native 0.73+, TypeScript 5+
- Use Expo for easier setup, or bare React Native for full native access
- Navigation: React Navigation v6+ with TypeScript-typed routes
- State management: Redux Toolkit or Zustand (never Context alone for complex state)
- API calls: Axios with typed responses, error boundaries
- Storage: React Native AsyncStorage or encrypted with MMKV
- Testing: Jest + React Native Testing Library
- No direct platform checks (Platform.OS): use abstraction layer

**Example: Hook for API**
```typescript
// hooks/useUserAPI.ts
export const useUserAPI = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<User[]>('/users');
      setUsers(response.data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  return { users, loading, error, refetch: fetchUsers };
};
```

**Performance**
- Flatten view hierarchies: avoid deep nesting
- Use `FlatList` with `keyExtractor` and `renderItem` callback
- Memoize components: `React.memo()` for expensive renders
- Use `useCallback` for event handlers passed to memoized children
- Lazy load screens: code splitting with dynamic imports
- Monitor: use React Native Debugger for performance profiling

---

## 📦 Flutter Standards

**Project Structure**
```
my_app/
├── lib/
│   ├── main.dart
│   ├── screens/
│   │   ├── home_screen.dart
│   │   └── detail_screen.dart
│   ├── widgets/
│   │   ├── user_card.dart
│   │   └── loading_spinner.dart
│   ├── providers/
│   │   └── user_provider.dart
│   ├── services/
│   │   ├── api_client.dart
│   │   └── storage_service.dart
│   ├── models/
│   │   └── user.dart
│   └── theme/
│       └── app_theme.dart
├── pubspec.yaml
└── test/
    └── widget_test.dart
```

**Dart Code Standards**
- Flutter 3.13+, Dart 3+
- Use Provider or Riverpod for state management (not Provider alone)
- MVVM: UI Widget → ViewModel/Provider → Service/Repository
- Naming: `snake_case` for files, `PascalCase` for classes
- Null safety: never use `!` operator, use `??` and `?.` safely
- Async: use async/await with try-catch, never blocking operations
- No hardcoded strings: use Localizations delegate or constants file
- Performance: use `const` constructors, ListWheelScrollView for lists, avoid rebuilds

**Example: Provider + API**
```dart
// providers/user_provider.dart
final usersProvider = FutureProvider<List<User>>((ref) async {
  final apiClient = ref.watch(apiClientProvider);
  return apiClient.fetchUsers();
});

// screens/home_screen.dart
class HomeScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(usersProvider);

    return usersAsync.when(
      data: (users) => ListView(
        children: users.map((user) => UserCard(user: user)).toList(),
      ),
      loading: () => Center(child: CircularProgressIndicator()),
      error: (err, st) => Center(child: Text('Error: $err')),
    );
  }
}
```

**Testing**
- Widget tests: `testWidgets()` with finders
- Integration tests: `IntegrationTestWidgetsFlutterBinding`

---

## 🔋 Performance & Battery Optimization

### Common Issues

**1. Battery Drain**
- GPS polling: use background location with permission, coarse updates when possible
- Network: batch requests, use WiFi when available, implement exponential backoff
- Background tasks: use native background processing, not wake locks
- Sensors: limit accelerometer/gyro polling frequency, unsubscribe when not needed
- Animations: use GPU-accelerated paths, avoid expensive repaints

**2. Memory Leaks**
- Swift: avoid retain cycles with `weak self` in closures
- Kotlin: use lifecycle-aware components, clear listeners in `onDestroy()`
- React Native: clean up subscriptions in useEffect cleanup
- Flutter: dispose controllers and providers properly
- All: remove event listeners on screen exit

**3. Slow Startup**
- Defer non-critical initialization (analytics, crash reporting)
- Lazy load feature modules
- Use lazy initialization patterns
- Cache critical data locally
- Measure with profilers: XCProfiler (iOS), Android Profiler, React Native Debugger, DevTools (Flutter)

### Best Practices
```swift
// iOS: Defer non-critical work
DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
    // Initialize analytics after UI is ready
}

// Kotlin: Lazy initialization
private val apiClient: ApiClient by lazy {
    Retrofit.Builder().build().create(ApiClient::class.java)
}

// React Native: Lazy screen loading
const HomeScreen = lazy(() => import('./screens/HomeScreen'));

// Flutter: Lazy initialization
final apiClient = FutureProvider<ApiClient>((ref) async {
    return ApiClient();
});
```

---

## 🧪 Testing Standards

### iOS
- Unit tests with `XCTest`, mock with `OCMock` or custom fakes
- UI tests with `XCUITest` for critical flows
- Always test async code with `XCTestExpectation`

### Android
- Unit tests with JUnit + Mockito
- Instrumentation with AndroidX Test + Espresso
- Test database: in-memory Room

### React Native
- Jest for unit + snapshot tests
- React Native Testing Library for component tests
- Detox for E2E tests

### Flutter
- `test` package for unit tests
- `flutter_test` for widget tests
- `integration_test` for E2E

---

## 🔒 Security Standards

**Never:**
- Store passwords/tokens in UserDefaults (iOS), SharedPreferences (Android), AsyncStorage (React Native), SharedPreferences (Flutter)
- Send plain HTTP (always HTTPS)
- Log sensitive data (PII, tokens, passwords)
- Hardcode API keys or secrets

**Always:**
- Use secure storage: Keychain (iOS), KeyStore (Android), encrypted MMKV (React Native), flutter_secure_storage (Flutter)
- Validate SSL certificates
- Implement certificate pinning for sensitive APIs
- Use OAuth 2.0 + PKCE for authentication
- Sanitize user inputs
- Implement rate limiting on API calls
- Expire tokens after 1 hour, refresh with refresh tokens

---

## 📋 Localization Standards

- Never hardcode strings: use platform-native localization (NSLocalizedString, strings.xml, i18n)
- Support RTL languages: test with Arabic/Hebrew
- Use timezone-aware date formatting, never hardcoded offsets
- Currency formatting: use platform APIs, not string interpolation

**Example:**
```swift
// iOS: Localizable.strings
"user.greeting" = "Hello, %@";

// Code
let name = "Alice"
let greeting = String(format: NSLocalizedString("user.greeting", comment: ""), name)
```

---

## ✅ Checklist for Mobile Features

- [ ] Code runs on 2+ devices/simulators
- [ ] Handles offline scenario (no network)
- [ ] Handles slow network (3G simulated)
- [ ] Memory: profiler shows < 100MB base usage
- [ ] Battery: background tasks optimized
- [ ] Crash logs: none from app code (system errors ok)
- [ ] Localization: works in English + 1 other language
- [ ] Accessibility: VoiceOver (iOS) or TalkBack (Android) works
- [ ] Security: no hardcoded secrets, HTTPS only
- [ ] Testing: 80%+ coverage on business logic
- [ ] Documentation: API integration, custom components documented

---

**Version**: 2.7.0  
**Last Updated**: 2026-04-09  
**Author**: SmartWorkz Dev
