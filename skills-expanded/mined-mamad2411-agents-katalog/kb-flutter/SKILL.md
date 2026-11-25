---
name: kb-flutter
description: Portable reference for Flutter mobile development (Dart + Provider + GoRouter + Firebase + Material 3) — not grounded in this repo. Invoke when a derived Flutter project needs layered architecture, design tokens, the 4-state screen checklist (loading/error/empty/data), iOS vs Android conventions, or Provider performance rules.
last-verified: 2026-04-23
---

# Flutter — Mobile App Development

> **Stack:** Dart + Flutter 3.x + Provider + GoRouter + Firebase + ARB localization + Material 3.
> **Not grounded in this repo.** TimeKast Factory is Next.js — this skill activates in Flutter projects that inherit the kit.
> For visual direction → `doc-visual-direction`. For token discipline → `kb-design-system`.

> **Registry anchors** — esta skill es **portable**: no hay registry kit-shipped en este repo (no aplican `project/reference/HOOKS.md` ni `INVENTORY.md`, que son convenciones del stack Next.js). La verdad canónica para APIs de widgets, paquetes `pub.dev` y conventions Material vive en [flutter.dev/docs](https://flutter.dev/docs) y [api.flutter.dev](https://api.flutter.dev). Esta skill enseña **patterns de arquitectura y disciplina** (layered split, 4-state checklist, Provider vs Selector); los nombres exactos de APIs se leen de la doc oficial, no se enumeran aquí.

---

## 1. When to use

**Use for:**

- Writing Flutter widgets, screens, providers
- Firebase integration (Auth / Firestore / Messaging / Storage)
- Flavor / branding configuration (multi-tenant)
- ARB localization (i18n)
- State management with Provider / ChangeNotifier
- Mobile-specific UX/performance decisions

**Don't use for:**

- React Native → not covered here
- Native iOS (Swift) / native Android (Kotlin) → out of scope
- Backend API design → see `kb-api` (Next.js) or `kb-python` (FastAPI)

---

## 2. Project structure

```
lib/
├── main.dart                         # Default entry
├── main_{flavor}.dart                # Flavor-specific entries
├── app.dart                          # Root MaterialApp
├── core/
│   ├── config/
│   │   ├── app_config.dart           # Env, URLs, feature flags
│   │   ├── firebase_config.dart      # Firebase init
│   │   └── flavor_config.dart        # Flavor enum + brand tokens
│   ├── theme/
│   │   ├── app_colors.dart
│   │   ├── app_typography.dart
│   │   └── app_spacing.dart
│   └── session/
├── models/                           # Data classes (fromJson/toJson)
├── services/                         # API/Firebase — no UI
├── providers/                        # ChangeNotifier classes
├── router/app_router.dart            # GoRouter config
├── screens/                          # One file per screen
├── widgets/                          # Reusable UI
├── l10n/                             # ARB sources (app_en.arb, app_es.arb)
└── generated/                        # NEVER edit manually
```

All files `snake_case`. All classes `PascalCase`.

---

## 3. Layered architecture

```
Screens ─────► Widgets           (compose UI)
   │
   └─► Providers (via Consumer/context.read)
           │
           └─► Services
                   │
                   └─► Models
Core ←───────── used by all layers
```

**Rules (non-negotiable):**

- Screens **never** call services directly
- Widgets **never** access providers (receive data via constructor)
- Providers **never** import UI classes (no `material.dart` in providers)
- Services **never** import Flutter Material

**Gradual refactor levels:**

| Level | Structure                                  | Scale             |
| ----- | ------------------------------------------ | ----------------- |
| 1     | Screens + Widgets + Providers + Services   | < 20 screens      |
| 2     | Add `repositories/` (cache + remote split) | Medium complexity |
| 3     | Add `use_cases/` (interactors)             | 30+ screens       |

Start at Level 1. Don't over-engineer.

---

## 4. State management — Provider

```dart
class FeatureProvider extends ChangeNotifier {
  List<Item> _items = [];
  bool _isLoading = false;
  String? _error;

  List<Item> get items => _items;
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get hasData => _items.isNotEmpty;

  Future<void> load() async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    try {
      _items = await _service.fetchAll();
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}
```

**Consumption in UI:**

- `Consumer<FeatureProvider>` — rebuilds when provider calls `notifyListeners`
- `Selector<FeatureProvider, T>` — rebuilds only when selected slice changes (prefer for hot paths)
- `context.read<FeatureProvider>()` — one-shot access (no rebuild), e.g. in `initState`
- `context.watch<FeatureProvider>()` — subscribes in `build`, rebuilds on change

---

## 5. Design tokens

Centralized tokens, overridable per flavor/brand.

**Colors** (`lib/core/theme/app_colors.dart`):

```dart
class AppColors {
  final Color primary;
  final Color accent;

  // Universal (same across brands)
  static const backgroundDark = Color(0xFF0D1117);
  static const backgroundCard = Color(0xFF161B22);
  static const textPrimary    = Color(0xFFE6EDF3);
  static const textSecondary  = Color(0xFF8B949E);
  static const success        = Color(0xFF3FB950);
  static const warning        = Color(0xFFD29922);
  static const error          = Color(0xFFF85149);

  factory AppColors.fromBrand(AppBrand b) =>
      AppColors._(primary: b.primaryColor, accent: b.accentColor);
}
```

**Typography** — Material 3 scale (displayLarge / headlineMedium / titleLarge / bodyLarge / bodyMedium / labelSmall).

**Spacing** — 4/8/16/24/32/48 scale (`xs` → `xxl`). Radius scale: 8/12/16/24 + `full: 999`.

**Rule:** never raw hex / pixel literals in widgets — always reference the token class.

---

## 6. Screen creation checklist

Order is mandatory:

1. **Model** — `lib/models/`
2. **Service** — `lib/services/`
3. **Provider** — `lib/providers/`
4. **Screen** — `lib/screens/`
5. **Widgets** — extract to `lib/widgets/` if reused
6. **Router** — register in `lib/router/app_router.dart`
7. **Localization** — add strings to **all** `.arb` files
8. **Test** — widget test in `test/`

**Every screen MUST handle 4 states:**

```dart
Consumer<FeatureProvider>(
  builder: (ctx, p, _) {
    if (p.isLoading) return const Center(child: CircularProgressIndicator());
    if (p.error != null) return _ErrorState(error: p.error!, onRetry: p.load);
    if (!p.hasData) return const _EmptyState();
    return _Content(items: p.items);
  },
)
```

Wrap every screen body in `SafeArea`. Load data in `initState` via `WidgetsBinding.instance.addPostFrameCallback`.

---

## 7. Platform conventions (iOS vs Android)

| Element          | iOS                  | Android               |
| ---------------- | -------------------- | --------------------- |
| Primary font     | SF Pro / SF Compact  | Roboto                |
| Min touch target | 44pt × 44pt          | 48dp × 48dp           |
| Back navigation  | Edge swipe left      | System back button    |
| Bottom tab icons | SF Symbols           | Material Symbols      |
| Action sheet     | UIActionSheet bottom | Bottom Sheet / Dialog |
| Pull to refresh  | UIRefreshControl     | SwipeRefreshLayout    |

**Unify vs diverge:**

- **Always unify:** business logic, data layer, core features
- **Always diverge:** navigation, gestures, date pickers, modals/sheets, typography, alerts

**Thumb zone:** primary CTAs in the bottom third (natural thumb arc). Destructive actions away from easy reach.

---

## 8. Performance rules

1. `const` constructors everywhere possible — prevents rebuilds
2. Extract widgets instead of inline builders > 30 lines
3. `ListView.builder` for dynamic lists (never `ListView(children: [...])` for large lists)
4. `cached_network_image` for remote images
5. **Always `dispose()`** controllers (Animation, Text, Scroll)
6. Never `setState` for shared state — Provider
7. `RepaintBoundary` for complex static widgets
8. `compute()` for heavy synchronous work (off main thread)
9. Prefer `Selector` over `Consumer` on hot paths (targeted rebuilds)

**Animation performance:**

| GPU-accelerated (fast) | CPU-bound (avoid)           |
| ---------------------- | --------------------------- |
| `transform`, `opacity` | `width`, `height`, `margin` |

Duration: micro 150–300ms, page transitions 300–500ms, sequences max 800ms. Easing: `easeOutCubic` for enters, `easeInCubic` for exits. Never linear.

---

## 9. Firebase integration (minimal)

Initialize in `main_{flavor}.dart`:

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: FirebaseConfig.forFlavor(Flavor.development));
  runApp(const MyApp());
}
```

**Services wrap Firebase:**

- `firebase_auth` → `AuthService` (sign-in / sign-out / user stream)
- `cloud_firestore` → per-entity service (returns `Stream<List<Model>>` or `Future`)
- `firebase_messaging` → `PushService` (request perms, token, foreground handler)
- `firebase_storage` → `StorageService` (upload/download with progress)

**Rule:** providers consume services; services consume Firebase SDK. Screens never touch Firebase.

---

## 10. Flavors + i18n (setup pointers)

**Flavors:** configure via `--dart-define=FLAVOR=development --dart-define=BRAND=acme` and read with `const String.fromEnvironment`. Android: per-flavor `android/app/src/{flavor}/`. iOS: per-flavor config in `ios/config/{flavor}/`.

**i18n:** `flutter gen-l10n` generates `AppLocalizations` from `lib/l10n/app_*.arb`. Consume in UI: `AppLocalizations.of(context)!.key`. Never hardcode user-visible strings.

---

## 11. Build & deploy

```bash
flutter pub get && flutter gen-l10n
flutter run --dart-define=FLAVOR=development --dart-define=BRAND=acme

flutter build apk       --release --dart-define=FLAVOR=production --dart-define=BRAND=acme
flutter build appbundle --release --dart-define=FLAVOR=production --dart-define=BRAND=acme
flutter build ios       --release --dart-define=FLAVOR=production --dart-define=BRAND=acme
flutter build web       --release --dart-define=FLAVOR=production --dart-define=BRAND=acme
```

Version format: `major.minor.patch+build` (e.g. `1.2.0+42`). Increment `+build` for every store release.

---

## 12. Anti-patterns

| ❌ Don't                                  | ✅ Do                                     |
| ----------------------------------------- | ----------------------------------------- |
| `setState` for shared state               | Provider / ChangeNotifier                 |
| Hardcoded strings in UI                   | ARB localization                          |
| Raw hex / pixel literals                  | Design tokens (`AppColors`, `AppSpacing`) |
| Screen without error/loading/empty states | 4-state pattern (Consumer builder)        |
| Forget `dispose()` on controllers         | Always dispose in `dispose()`             |
| `print()` for logs                        | `debugPrint()` or logger                  |
| Inline widget trees > 30 lines            | Extract to reusable widget                |
| `import 'dart:io'` in web-compatible code | Platform check or conditional imports     |
| Services importing `material.dart`        | Services stay UI-agnostic                 |
| Widget accessing provider directly        | Receive data via constructor              |

---

_Cross-reference: `doc-visual-direction` for visual language upstream. `kb-design-system` for token discipline. The `flutter-mobile` subagent loads this skill when invoked._
