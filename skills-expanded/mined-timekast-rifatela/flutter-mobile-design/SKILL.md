---
name: flutter-mobile-design
description: Comprehensive reference for Flutter mobile app development and UI/UX design. Covers architecture, design patterns, component creation, animations, state management, Firebase integration, flavor configuration, localization, and deployment.
---

# Flutter Mobile Design Skill

> Universal reference for building premium Flutter mobile applications. Project-agnostic — use with any Flutter + Firebase project.

---

## 1. Recommended Project Structure

```
{project_root}/
├── lib/
│   ├── main.dart                    # App entry point
│   ├── main_{flavor}.dart           # Flavor-specific entry points (if flavors used)
│   ├── app.dart                     # MaterialApp / root widget
│   ├── core/
│   │   ├── config/
│   │   │   ├── app_config.dart      # Runtime config (env, URLs, feature flags)
│   │   │   ├── firebase_config.dart # Firebase initialization
│   │   │   └── flavor_config.dart   # Flavor enum, branding tokens
│   │   ├── theme/
│   │   │   ├── app_colors.dart      # Color tokens
│   │   │   ├── app_typography.dart  # Text styles
│   │   │   └── app_spacing.dart     # Spacing, radius, padding constants
│   │   ├── session/
│   │   │   └── session_initializer.dart
│   │   └── constants.dart           # App-wide constants
│   ├── models/                      # Data classes (fromJson/toJson)
│   ├── services/                    # API calls, Firebase ops, external integrations
│   ├── providers/                   # ChangeNotifier state management classes
│   ├── router/
│   │   └── app_router.dart          # GoRouter / Navigator 2.0 config
│   ├── screens/                     # Full-page views (one per screen)
│   ├── widgets/                     # Reusable UI components
│   ├── l10n/                        # ARB localization source files
│   │   ├── app_en.arb
│   │   └── app_es.arb
│   └── generated/                   # ⚠️ Auto-generated (NEVER edit manually)
│       └── l10n/
├── assets/
│   ├── images/
│   ├── videos/
│   └── animations/                  # Lottie JSON files
├── android/
│   └── app/src/{flavor}/            # Flavor-specific Android resources
├── ios/
│   ├── Runner/
│   └── config/{flavor}/             # Flavor-specific iOS configs
├── test/                            # Unit & widget tests
├── integration_test/                # E2E tests
├── pubspec.yaml
└── analysis_options.yaml
```

---

## 2. Layered Architecture

### 2.1 Layer Responsibilities

```
┌─────────────────────────────────────────────────────┐
│  SCREENS (Pages)                                     │
│  Full-page views. Compose widgets, consume providers.│
│  One file per screen. Never contains business logic. │
├─────────────────────────────────────────────────────┤
│  WIDGETS (Components)                                │
│  Reusable UI. Stateless preferred. Accept data via   │
│  constructor. No business logic, no service calls.   │
├─────────────────────────────────────────────────────┤
│  PROVIDERS (State / Business Logic)                  │
│  ChangeNotifier classes. Call services, expose state  │
│  to UI. Handle loading/error/data states.            │
├─────────────────────────────────────────────────────┤
│  SERVICES (Data Layer)                               │
│  Firebase, REST APIs, local storage. Return raw data.│
│  No UI awareness. Stateless static methods or        │
│  singleton instances.                                │
├─────────────────────────────────────────────────────┤
│  MODELS (Data Structures)                            │
│  Dart classes with fromJson/toJson/fromFirestore.    │
│  Immutable when possible. No logic beyond parsing.   │
├─────────────────────────────────────────────────────┤
│  CORE (Infrastructure)                               │
│  Config, theme, session, constants. Shared across    │
│  all layers.                                         │
└─────────────────────────────────────────────────────┘
```

### 2.2 Dependency Flow

```
Screens → Widgets
Screens → Providers (via Consumer/context.read)
Providers → Services
Services → Models
Core ← used by all layers
```

**Rules:**

- Screens NEVER call services directly
- Widgets NEVER access providers (receive data via constructor)
- Providers NEVER import UI classes
- Services NEVER import Flutter material

### 2.3 Clean Architecture — Gradual Refactor Levels

**Level 1 (Starting point):** Screens + Providers + Services + Models. Good enough for most apps < 20 screens.

**Level 2 (Moderate complexity):** Add a `repositories/` layer between providers and services for data source abstraction (local cache + remote).

```dart
// lib/repositories/investment_repository.dart
class InvestmentRepository {
  final InvestmentRemoteService _remote;
  final InvestmentCacheService _cache;

  Future<List<Investment>> getAll({bool forceRefresh = false}) async {
    if (!forceRefresh) {
      final cached = await _cache.getAll();
      if (cached.isNotEmpty) return cached;
    }
    final data = await _remote.fetchAll();
    await _cache.saveAll(data);
    return data;
  }
}
```

**Level 3 (Large apps, 30+ screens):** Add `use_cases/` (interactors) between providers and repositories to isolate business operations.

```dart
// lib/use_cases/calculate_returns.dart
class CalculateReturns {
  final InvestmentRepository _repo;

  Future<ReturnsSummary> execute(String investorId) async {
    final investments = await _repo.getByInvestor(investorId);
    // Business logic here
    return ReturnsSummary.fromInvestments(investments);
  }
}
```

---

## 3. State Management (Provider)

### 3.1 Provider Template

```dart
class FeatureProvider extends ChangeNotifier {
  List<Item> _items = [];
  bool _isLoading = false;
  String? _error;

  // Getters — never expose internal state directly
  List<Item> get items => List.unmodifiable(_items);
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get hasData => _items.isNotEmpty;

  Future<void> load() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _items = await FeatureService.getAll();
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void clear() {
    _items = [];
    _error = null;
    notifyListeners();
  }
}
```

### 3.2 Provider Registration

```dart
// In main.dart or app.dart
MultiProvider(
  providers: [
    ChangeNotifierProvider(create: (_) => AuthProvider()),
    ChangeNotifierProvider(create: (_) => InvestmentProvider()),
    // Add providers as features grow
  ],
  child: const MyApp(),
)
```

### 3.3 Consuming in UI

```dart
// ✅ Consumer — rebuilds only this subtree
Consumer<FeatureProvider>(
  builder: (context, provider, child) {
    if (provider.isLoading) return const LoadingSkeleton();
    if (provider.error != null) return ErrorState(message: provider.error!);
    if (!provider.hasData) return const EmptyState();
    return ItemList(items: provider.items);
  },
)

// ✅ context.read — for one-time actions (button taps)
ElevatedButton(
  onPressed: () => context.read<FeatureProvider>().load(),
  child: const Text('Refresh'),
)

// ❌ NEVER use context.watch in callbacks
// ❌ NEVER use setState for shared state
```

---

## 4. Flavor / Environment Configuration

### 4.1 Flavor Enum

```dart
// lib/core/config/flavor_config.dart
enum AppFlavor {
  development,
  staging,
  production;

  // Per-flavor values
  String get firebaseFunctionsBaseUrl => switch (this) {
    development => 'http://localhost:5001/{project_id}/us-central1',
    staging => 'https://us-central1-{staging_project_id}.cloudfunctions.net',
    production => 'https://us-central1-{prod_project_id}.cloudfunctions.net',
  };

  String get appName => switch (this) {
    development => '{App Name} DEV',
    staging => '{App Name} STG',
    production => '{App Name}',
  };
}
```

### 4.2 Client/Brand Flavor (Multi-tenant)

For apps serving multiple clients with different branding:

```dart
// lib/core/config/brand_config.dart
enum AppBrand {
  brandA,
  brandB;

  // These values change per client
  String get displayName => switch (this) {
    brandA => 'Brand A Name',
    brandB => 'Brand B Name',
  };

  Color get primaryColor => switch (this) {
    brandA => const Color(0xFF1A237E),
    brandB => const Color(0xFF004D40),
  };

  Color get accentColor => switch (this) {
    brandA => const Color(0xFFFFB300),
    brandB => const Color(0xFF00BFA5),
  };

  String get logoAsset => switch (this) {
    brandA => 'assets/images/logo_brand_a.png',
    brandB => 'assets/images/logo_brand_b.png',
  };

  String get firebaseProjectId => switch (this) {
    brandA => '{firebase_project_id_a}',
    brandB => '{firebase_project_id_b}',
  };
}
```

### 4.3 Runtime Configuration with --dart-define

```dart
// lib/core/config/app_config.dart
class AppConfig {
  static late final AppFlavor flavor;
  static late final AppBrand brand;

  static void initialize() {
    // Read from --dart-define at compile time
    const flavorStr = String.fromEnvironment('FLAVOR', defaultValue: 'development');
    const brandStr = String.fromEnvironment('BRAND', defaultValue: 'brandA');

    flavor = AppFlavor.values.firstWhere(
      (f) => f.name == flavorStr,
      orElse: () => AppFlavor.development,
    );

    brand = AppBrand.values.firstWhere(
      (b) => b.name == brandStr,
      orElse: () => AppBrand.brandA,
    );
  }

  static String get functionsBaseUrl => flavor.firebaseFunctionsBaseUrl;
  static String get appName => '${brand.displayName}${flavor != AppFlavor.production ? ' (${flavor.name.toUpperCase()})' : ''}';
}
```

### 4.4 Running with Flavors

```bash
# Development + Brand A
flutter run --dart-define=FLAVOR=development --dart-define=BRAND=brandA

# Production + Brand B
flutter run --release --dart-define=FLAVOR=production --dart-define=BRAND=brandB

# Build APK for specific flavor
flutter build apk --release \
  --dart-define=FLAVOR=production \
  --dart-define=BRAND=brandB
```

### 4.5 Flavor-Specific Entry Points (Alternative)

```dart
// lib/main_brand_a.dart
void main() {
  AppConfig.initializeWith(brand: AppBrand.brandA, flavor: AppFlavor.production);
  runApp(const MyApp());
}

// lib/main_brand_b.dart
void main() {
  AppConfig.initializeWith(brand: AppBrand.brandB, flavor: AppFlavor.production);
  runApp(const MyApp());
}
```

```bash
flutter run -t lib/main_brand_a.dart
flutter run -t lib/main_brand_b.dart
```

### 4.6 Firebase Per-Flavor Setup

Each brand/flavor needs its own Firebase project:

```
android/app/src/
├── brandA/
│   └── google-services.json       # Firebase project A
├── brandB/
│   └── google-services.json       # Firebase project B
└── main/
    └── AndroidManifest.xml

ios/config/
├── brandA/
│   └── GoogleService-Info.plist   # Firebase project A
└── brandB/
    └── GoogleService-Info.plist   # Firebase project B
```

In `firebase_options.dart`, switch based on brand:

```dart
class AppFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    final brand = AppConfig.brand;
    return switch (brand) {
      AppBrand.brandA => _brandAOptions,
      AppBrand.brandB => _brandBOptions,
    };
  }

  static const _brandAOptions = FirebaseOptions(
    apiKey: '{API_KEY_A}',
    appId: '{APP_ID_A}',
    messagingSenderId: '{SENDER_ID_A}',
    projectId: '{PROJECT_ID_A}',
    storageBucket: '{BUCKET_A}',
  );

  // ... _brandBOptions
}
```

---

## 5. Design System

### 5.1 Color Tokens

Define a centralized theme that can be overridden per flavor/brand:

```dart
// lib/core/theme/app_colors.dart
class AppColors {
  // Populated from brand config or static defaults
  final Color primary;
  final Color primaryLight;
  final Color primaryDark;
  final Color accent;
  final Color accentLight;

  // These are universal — same across brands
  static const Color backgroundDark = Color(0xFF0D1117);
  static const Color backgroundCard = Color(0xFF161B22);
  static const Color surface = Color(0xFF21262D);

  static const Color textPrimary = Color(0xFFE6EDF3);
  static const Color textSecondary = Color(0xFF8B949E);
  static const Color textMuted = Color(0xFF484F58);

  static const Color success = Color(0xFF3FB950);
  static const Color warning = Color(0xFFD29922);
  static const Color error = Color(0xFFF85149);
  static const Color info = Color(0xFF58A6FF);

  // Factory method from brand config
  factory AppColors.fromBrand(AppBrand brand) {
    return AppColors._(
      primary: brand.primaryColor,
      primaryLight: brand.primaryColor.withValues(alpha: 0.7),
      primaryDark: brand.primaryColor.withValues(alpha: 0.9),
      accent: brand.accentColor,
      accentLight: brand.accentColor.withValues(alpha: 0.7),
    );
  }

  const AppColors._({
    required this.primary,
    required this.primaryLight,
    required this.primaryDark,
    required this.accent,
    required this.accentLight,
  });
}
```

### 5.2 Typography

```dart
// lib/core/theme/app_typography.dart
class AppTypography {
  static const displayLarge = TextStyle(
    fontSize: 32, fontWeight: FontWeight.w700, letterSpacing: -0.5, height: 1.2,
  );
  static const headlineMedium = TextStyle(
    fontSize: 24, fontWeight: FontWeight.w600, letterSpacing: -0.3, height: 1.3,
  );
  static const titleLarge = TextStyle(
    fontSize: 20, fontWeight: FontWeight.w600, height: 1.4,
  );
  static const bodyLarge = TextStyle(
    fontSize: 16, fontWeight: FontWeight.w400, height: 1.5,
  );
  static const bodyMedium = TextStyle(
    fontSize: 14, fontWeight: FontWeight.w400, height: 1.5,
  );
  static const labelSmall = TextStyle(
    fontSize: 12, fontWeight: FontWeight.w500, letterSpacing: 0.5, height: 1.4,
  );
  static const caption = TextStyle(
    fontSize: 11, fontWeight: FontWeight.w400,
  );
}
```

### 5.3 Spacing & Layout

```dart
// lib/core/theme/app_spacing.dart
class AppSpacing {
  static const double xs = 4.0;
  static const double sm = 8.0;
  static const double md = 16.0;
  static const double lg = 24.0;
  static const double xl = 32.0;
  static const double xxl = 48.0;

  static const screenPadding = EdgeInsets.symmetric(horizontal: 20.0, vertical: 16.0);
  static const cardPadding = EdgeInsets.all(16.0);

  static const double radiusSm = 8.0;
  static const double radiusMd = 12.0;
  static const double radiusLg = 16.0;
  static const double radiusXl = 24.0;
  static const double radiusFull = 999.0;
}
```

### 5.4 Component Patterns

**Premium card with glassmorphism:**

```dart
Container(
  decoration: BoxDecoration(
    color: AppColors.backgroundCard.withValues(alpha: 0.8),
    borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
    border: Border.all(color: Colors.white.withValues(alpha: 0.08), width: 1),
    boxShadow: [
      BoxShadow(color: Colors.black.withValues(alpha: 0.2), blurRadius: 20, offset: const Offset(0, 8)),
    ],
  ),
  child: ClipRRect(
    borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
    child: BackdropFilter(
      filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
      child: Padding(padding: AppSpacing.cardPadding, child: content),
    ),
  ),
)
```

**Styled input field:**

```dart
TextField(
  decoration: InputDecoration(
    hintText: 'Placeholder',
    hintStyle: AppTypography.bodyMedium.copyWith(color: AppColors.textMuted),
    filled: true,
    fillColor: AppColors.surface,
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
      borderSide: BorderSide.none,
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
      borderSide: const BorderSide(color: AppColors.info, width: 1.5),
    ),
    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
  ),
)
```

---

## 6. Animation Guidelines

### 6.1 Principles

1. **Purpose over decoration** — Every animation must serve UX (feedback, transition, attention)
2. **Duration standards** — Micro: 150–300ms. Page transitions: 300–500ms. Sequences: max 800ms
3. **Easing** — `Curves.easeOutCubic` for enters, `Curves.easeInCubic` for exits. Never linear
4. **Performance** — Use `AnimatedBuilder`/`AnimatedWidget`, not `setState` in tick callbacks

### 6.2 Standard Reusable Animations

**Fade + slide in (for list items):**

```dart
class FadeSlideIn extends StatelessWidget {
  final Widget child;
  final int index;
  final Duration itemDelay;

  const FadeSlideIn({
    required this.child,
    this.index = 0,
    this.itemDelay = const Duration(milliseconds: 50),
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return TweenAnimationBuilder<double>(
      tween: Tween(begin: 0.0, end: 1.0),
      duration: Duration(milliseconds: 400 + (index * itemDelay.inMilliseconds)),
      curve: Curves.easeOutCubic,
      builder: (context, value, child) {
        return Opacity(
          opacity: value,
          child: Transform.translate(
            offset: Offset(0, 20 * (1 - value)),
            child: child,
          ),
        );
      },
      child: child,
    );
  }
}
```

**Scale bounce for interactive elements:**

```dart
class ScaleBounce extends StatefulWidget {
  final Widget child;
  final VoidCallback? onTap;
  const ScaleBounce({required this.child, this.onTap, super.key});

  @override
  State<ScaleBounce> createState() => _ScaleBounceState();
}

class _ScaleBounceState extends State<ScaleBounce>
    with SingleTickerProviderStateMixin {
  late final _ctrl = AnimationController(
    vsync: this, duration: const Duration(milliseconds: 150),
    lowerBound: 0.95, upperBound: 1.0, value: 1.0,
  );

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) => _ctrl.reverse(),
      onTapUp: (_) { _ctrl.forward(); widget.onTap?.call(); },
      onTapCancel: () => _ctrl.forward(),
      child: ScaleTransition(scale: _ctrl, child: widget.child),
    );
  }

  @override
  void dispose() { _ctrl.dispose(); super.dispose(); }
}
```

**Page transition (GoRouter):**

```dart
GoRoute(
  path: '/detail/:id',
  pageBuilder: (context, state) => CustomTransitionPage(
    child: DetailScreen(id: state.pathParameters['id']!),
    transitionsBuilder: (context, animation, _, child) {
      return FadeTransition(
        opacity: CurveTween(curve: Curves.easeOutCubic).animate(animation),
        child: SlideTransition(
          position: Tween<Offset>(begin: const Offset(0.05, 0), end: Offset.zero)
              .animate(CurveTween(curve: Curves.easeOutCubic).animate(animation)),
          child: child,
        ),
      );
    },
  ),
)
```

---

## 7. Firebase Integration Patterns

### 7.1 Firestore Reads

```dart
class DataService {
  static final _db = FirebaseFirestore.instance;

  /// One-time fetch
  static Future<List<Item>> getAll(String collectionPath) async {
    final snap = await _db.collection(collectionPath)
        .orderBy('createdAt', descending: true)
        .get();
    return snap.docs.map((d) => Item.fromFirestore(d)).toList();
  }

  /// Real-time stream
  static Stream<List<Item>> watchAll(String collectionPath) {
    return _db.collection(collectionPath)
        .snapshots()
        .map((snap) => snap.docs.map((d) => Item.fromFirestore(d)).toList());
  }
}
```

### 7.2 Model with Firestore Support

```dart
class Item {
  final String id;
  final String name;
  final DateTime createdAt;

  const Item({required this.id, required this.name, required this.createdAt});

  factory Item.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return Item(
      id: doc.id,
      name: data['name'] ?? '',
      createdAt: (data['createdAt'] as Timestamp?)?.toDate() ?? DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() => {
    'name': name,
    'createdAt': Timestamp.fromDate(createdAt),
  };
}
```

### 7.3 Cloud Functions Calls

```dart
class CloudFunctionService {
  static final _dio = Dio(BaseOptions(
    baseUrl: AppConfig.functionsBaseUrl,
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 30),
  ));

  static Future<Map<String, dynamic>> call(String functionName, {
    Map<String, dynamic>? body,
    String? authToken,
  }) async {
    final response = await _dio.post(
      '/$functionName',
      data: body,
      options: authToken != null
          ? Options(headers: {'Authorization': 'Bearer $authToken'})
          : null,
    );
    return response.data;
  }
}
```

### 7.4 Auth Guard Pattern

```dart
// In router config
GoRouter(
  redirect: (context, state) {
    final isLoggedIn = FirebaseAuth.instance.currentUser != null;
    final isAuthRoute = ['/login', '/signup', '/recover'].contains(state.fullPath);

    if (!isLoggedIn && !isAuthRoute) return '/login';
    if (isLoggedIn && isAuthRoute) return '/home';
    return null;
  },
  routes: [ /* ... */ ],
)
```

---

## 8. Localization (i18n)

### 8.1 Rules

1. **NEVER** hardcode user-facing strings
2. **ALWAYS** add to ALL supported `.arb` files simultaneously
3. **NEVER** edit `lib/generated/` — auto-generated
4. Run `flutter gen-l10n` after adding ARB entries

### 8.2 ARB Format

```json
{
  "screenTitle": "My Screen",
  "@screenTitle": { "description": "Title for the screen" },
  "itemCount": "{count} items",
  "@itemCount": {
    "placeholders": {
      "count": { "type": "int" }
    }
  },
  "greeting": "Hello, {name}!",
  "@greeting": {
    "placeholders": {
      "name": { "type": "String" }
    }
  }
}
```

### 8.3 Usage

```dart
final l10n = AppLocalizations.of(context)!;
Text(l10n.screenTitle);
Text(l10n.itemCount(42));
Text(l10n.greeting('Edmond'));
```

### 8.4 pubspec.yaml Config

```yaml
flutter:
  generate: true

flutter_l10n:
  arb-dir: lib/l10n
  template-arb-file: app_en.arb
  output-localization-file: app_localizations.dart
```

---

## 9. Screen Creation Checklist

When creating a new screen, follow this exact order:

1. **Model** — Create/update data model in `lib/models/`
2. **Service** — Create/update API/Firebase service in `lib/services/`
3. **Provider** — Create/update ChangeNotifier in `lib/providers/`
4. **Screen** — Create screen in `lib/screens/`
5. **Widgets** — Extract reusable components to `lib/widgets/`
6. **Router** — Add route in `lib/router/app_router.dart`
7. **Localization** — Add strings to all `.arb` files
8. **Test** — Write widget test in `test/`

### Screen Template

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class NewScreen extends StatefulWidget {
  const NewScreen({super.key});
  @override
  State<NewScreen> createState() => _NewScreenState();
}

class _NewScreenState extends State<NewScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<FeatureProvider>().load();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundDark,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Text(AppLocalizations.of(context)!.screenTitle),
      ),
      body: SafeArea(
        child: Consumer<FeatureProvider>(
          builder: (context, p, _) {
            if (p.isLoading) return const Center(child: CircularProgressIndicator());
            if (p.error != null) return _ErrorState(error: p.error!, onRetry: p.load);
            if (!p.hasData) return const _EmptyState();
            return _Content(items: p.items);
          },
        ),
      ),
    );
  }
}
```

> **Every screen MUST handle 4 states:** loading, error, empty, data.

---

## 10. Responsive Design

```dart
class Breakpoints {
  static bool isMobile(BuildContext c) => MediaQuery.of(c).size.width < 600;
  static bool isTablet(BuildContext c) =>
    MediaQuery.of(c).size.width >= 600 && MediaQuery.of(c).size.width < 1024;
  static bool isDesktop(BuildContext c) => MediaQuery.of(c).size.width >= 1024;
}
```

Rules:

1. ALWAYS wrap content in `SafeArea`
2. Account for notch, status bar, home indicator
3. Test on both small (iPhone SE) and large (iPad) screens
4. Use `LayoutBuilder` or `MediaQuery` for adaptive layouts

---

## 11. Performance Rules

1. Use `const` constructors wherever possible
2. Extract widgets instead of anonymous builders > 30 lines
3. `ListView.builder` for dynamic lists (never `ListView(children: [...])` for large lists)
4. Cache images with `cached_network_image`
5. Always `dispose()` controllers (Animation, Text, Scroll)
6. Never `setState` for shared state — use Provider
7. `RepaintBoundary` for complex static widgets
8. `compute()` for heavy synchronous work
9. Avoid rebuilding entire widget trees — use targeted `Consumer` or `Selector`

---

## 12. Testing

### Widget Test Pattern

```dart
void main() {
  testWidgets('Screen shows loading then data', (tester) async {
    final provider = MockFeatureProvider();
    when(provider.isLoading).thenReturn(true);

    await tester.pumpWidget(
      ChangeNotifierProvider<FeatureProvider>.value(
        value: provider,
        child: const MaterialApp(home: FeatureScreen()),
      ),
    );
    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });
}
```

### Commands

```bash
flutter test                                    # All tests
flutter test test/screens/my_screen_test.dart   # Specific test
flutter test --coverage                         # With coverage report
flutter analyze                                 # Static analysis
```

---

## 13. Build & Deploy

```bash
# Development
flutter pub get
flutter gen-l10n
flutter run --dart-define=FLAVOR=development --dart-define=BRAND={brand}

# Android APK
flutter build apk --release --dart-define=FLAVOR=production --dart-define=BRAND={brand}

# Android App Bundle (Play Store)
flutter build appbundle --release --dart-define=FLAVOR=production --dart-define=BRAND={brand}

# iOS
flutter build ios --release --dart-define=FLAVOR=production --dart-define=BRAND={brand}

# Web
flutter build web --release --dart-define=FLAVOR=production --dart-define=BRAND={brand}
```

### Version Format

```yaml
version: major.minor.patch+buildNumber # e.g. 1.2.0+42
```

- **major**: Breaking changes
- **minor**: New features
- **patch**: Bug fixes
- **buildNumber**: Always increment for store releases

---

## 14. File Naming Conventions

| Type         | Pattern                                  | Example                      |
| ------------ | ---------------------------------------- | ---------------------------- |
| Screens      | `{feature}_screen.dart`                  | `home_screen.dart`           |
| Widgets      | `{feature}_widget.dart` or `{name}.dart` | `custom_drawer.dart`         |
| Models       | `{entity}.dart`                          | `user.dart`                  |
| Providers    | `{feature}_provider.dart`                | `session_provider.dart`      |
| Services     | `{feature}_service.dart`                 | `auth_service.dart`          |
| Repositories | `{entity}_repository.dart`               | `investment_repository.dart` |
| Tests        | `{original_name}_test.dart`              | `home_screen_test.dart`      |

All file names use `snake_case`. All class names use `PascalCase`.

---

## 15. Recommended Dependencies

```yaml
# pubspec.yaml — commonly needed packages
dependencies:
  # State management
  provider: ^6.0.0

  # Navigation
  go_router: ^14.0.0

  # Firebase
  firebase_core: ^3.0.0
  firebase_auth: ^5.0.0
  cloud_firestore: ^5.0.0
  firebase_messaging: ^15.0.0

  # Networking
  dio: ^5.0.0

  # UI
  cached_network_image: ^3.0.0
  lottie: ^3.0.0
  shimmer: ^3.0.0

  # Utils
  intl: ^0.19.0
  flutter_localizations:
    sdk: flutter

dev_dependencies:
  flutter_lints: ^5.0.0
  mockito: ^5.0.0
  build_runner: ^2.0.0
```

> ⚠️ **Use exact versions from your project.** These are baseline suggestions — always check for latest compatible versions.

---

## 16. Common Rules

### ❌ DON'T

1. Don't use `setState` for shared state
2. Don't hardcode strings — use ARB localization
3. Don't use raw colors — use design tokens
4. Don't import `dart:io` in web-compatible code
5. Don't create screens without error/loading/empty states
6. Don't forget to dispose controllers
7. Don't use `print()` — use `debugPrint()` or a logger
8. Don't commit auto-generated files
9. Don't block main thread — use `compute()` for heavy work
10. Don't mix business logic in UI layers

### ✅ DO

1. Follow the layered architecture
2. Add localization in ALL supported languages
3. Handle loading, error, empty, and data states
4. Use `SafeArea` for screen layouts
5. Add meaningful transition animations
6. Test on both iOS and Android
7. Use `const` everywhere possible
8. Document non-obvious business logic
9. Use the design token system
10. Consider offline state and poor connectivity
