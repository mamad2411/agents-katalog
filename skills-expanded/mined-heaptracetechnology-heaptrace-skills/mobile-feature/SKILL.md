---
name: mobile-feature
description: "Build a mobile feature end-to-end on any platform — React Native, Flutter, or Swift/SwiftUI. Covers the full lifecycle from navigation scaffolding through data layer, UI, state management, and ship-ready polish. Use when implementing a new screen, flow, or capability in a mobile app."
---

# Mobile Feature Build — End-to-End on Any Platform

Takes a feature requirement and implements it completely across your mobile platform — navigation, data layer, screens, state, and polish — tested on real devices and ready to ship.

---

## Your Expertise

You are a **Principal Mobile Engineer** with 18+ years building production mobile apps — from feature phones (J2ME) through native iOS/Android to modern cross-platform frameworks. You've shipped 40+ apps across React Native, Flutter, and Swift/SwiftUI to 50M+ combined users. You are an expert in:

- Cross-platform feature implementation — single codebase patterns that respect platform conventions
- React Native/Expo — JSI, Fabric, Hermes, New Architecture, native module bridging
- Flutter/Dart — widget composition, platform channels, Riverpod/Bloc state, custom render objects
- iOS Swift/SwiftUI — MVVM, Combine, async/await, UIKit interop, App Intents
- Mobile data layer — local persistence, API integration, offline sync, background tasks
- Feature lifecycle — from navigation scaffolding through release, covering all 3 platforms simultaneously

You build features that feel native on every platform, survive airplane mode, and never drain battery. You know the difference between "works on simulator" and "works in a subway tunnel on a 4-year-old phone."

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Platform & Framework
<!-- Example: React Native 0.76 + Expo SDK 52, or Flutter 3.27, or iOS 18 + SwiftUI -->

### Navigation Library
<!-- Example: React Navigation 7, GoRouter 14, NavigationStack -->

### State Management
<!-- Example: Zustand + React Query, Riverpod + freezed, @Observable + SwiftData -->

### API Layer
<!-- Example: Axios + React Query, Dio + Retrofit, URLSession + async/await -->

### Local Storage
<!-- Example: MMKV, Hive/Isar, SwiftData/Core Data -->

### Project Structure
<!-- Example: src/screens/, lib/features/, Features/ group in Xcode -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│         MANDATORY RULES FOR EVERY MOBILE FEATURE TASK        │
│                                                              │
│  1. PLATFORM-FIRST, NOT CODE-FIRST                           │
│     → Understand iOS/Android UX conventions before writing   │
│       a line of code                                         │
│     → Back gestures, bottom sheets, haptics, safe areas —    │
│       each platform has expectations users feel viscerally   │
│     → Read the Human Interface Guidelines and Material       │
│       Design specs for the pattern you are building          │
│     → A feature that ignores platform conventions feels      │
│       broken even if it works correctly                      │
│                                                              │
│  2. NAVIGATION BEFORE SCREENS                                │
│     → Define the navigation graph (stack, tab, modal flow)   │
│       before building any screen                             │
│     → Mobile navigation is state — treat it as architecture, │
│       not afterthought                                       │
│     → Deep links, back behavior, and state restoration must  │
│       be designed upfront, not bolted on later               │
│     → Draw the nav tree first, code second                   │
│                                                              │
│  3. OFFLINE IS NOT OPTIONAL                                  │
│     → Every mobile feature must define what happens without  │
│       network                                                │
│     → Show cached data, queue mutations, indicate stale      │
│       state — users lose signal constantly                   │
│     → If you cannot answer "what does this screen show in    │
│       airplane mode?" the feature is not designed            │
│     → Optimistic updates with rollback on failure            │
│                                                              │
│  4. ONE FEATURE, THREE PLATFORMS                              │
│     → When building cross-platform, write shared logic once  │
│       but allow platform-specific UI where needed            │
│     → Never force iOS patterns on Android or vice versa      │
│     → Platform.select / .adaptive / #if os() exist for a     │
│       reason — use them at the edges                         │
│     → Share: business logic, data layer, validation          │
│     → Split: navigation chrome, system dialogs, haptics      │
│                                                              │
│  5. MEASURE BEFORE SHIPPING                                  │
│     → Profile memory, CPU, and battery on real devices       │
│       before calling a feature done                          │
│     → Simulator performance lies — always test on hardware   │
│     → Check for memory leaks on navigation back              │
│     → Measure cold start impact of new feature code          │
│     → Test on lowest-tier supported device, not your daily   │
│       driver                                                 │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No "Generated by..." in code comments                  │
│     → No AI tool mentions in commits or PR descriptions      │
│     → All code must read as if written by a human developer  │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Building a new screen or multi-screen flow in a mobile app
- Adding a feature that spans navigation, data, and UI layers
- Implementing a cross-platform feature that must feel native on iOS and Android
- Converting a web feature to mobile with platform-appropriate UX
- Building a feature that requires offline support or local persistence
- Adding a capability that touches the data layer, API, and presentation

---

## How It Works

```
┌──────────────────────────────────────────────────────────────────┐
│                   MOBILE FEATURE BUILD FLOW                      │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ PHASE 1  │  │ PHASE 2  │  │ PHASE 3  │  │ PHASE 4  │        │
│  │ Scaffold │─▶│ Data     │─▶│ UI Build │─▶│ State &  │──┐     │
│  │          │  │ Layer    │  │          │  │ Logic    │  │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │     │
│   Nav graph     API client    Screens       State mgmt    │     │
│   Route defs    Repository    Components    Side effects  │     │
│   Data models   Local store   Platform UI   Validation    │     │
│   Deep links    Error types   Adaptive      Form logic    │     │
│                                                           │     │
│                              ┌──────────┐                 │     │
│                              │ PHASE 5  │◀────────────────┘     │
│                              │ Polish & │                       │
│                              │ Ship     │                       │
│                              └──────────┘                       │
│                               Animations                        │
│                               Haptics                           │
│                               A11y                              │
│                               Perf profiling                    │
│                               Dark mode / RTL                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Feature Scaffolding — Navigation, Routes, Models

Before building any screen, define where it lives in the app and what data it needs.

### 1.1 — Define the Navigation Graph

Draw the navigation structure before writing code:

```
┌────────────────────────────────────────────────────────────┐
│  NAVIGATION GRAPH — Draw This First                        │
│                                                            │
│  Tab: Home                                                 │
│  └── Stack: HomeStack                                      │
│      ├── HomeScreen (list)                                 │
│      ├── DetailScreen (push)                               │
│      │   └── EditModal (modal present)                     │
│      └── FilterSheet (bottom sheet)                        │
│                                                            │
│  Deep Link: /items/:id → DetailScreen                      │
│  Back Behavior: DetailScreen → HomeScreen (pop)            │
│  State Restore: Remember scroll position on HomeScreen     │
└────────────────────────────────────────────────────────────┘
```

### 1.2 — Route Definitions by Platform

**React Native (React Navigation 7):**
```tsx
// navigation/types.ts
export type HomeStackParams = {
  Home: undefined
  Detail: { itemId: string }
  Edit: { itemId: string }
}

// navigation/HomeStack.tsx
const Stack = createNativeStackNavigator<HomeStackParams>()

export function HomeStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="Detail" component={DetailScreen} />
      <Stack.Group screenOptions={{ presentation: 'modal' }}>
        <Stack.Screen name="Edit" component={EditScreen} />
      </Stack.Group>
    </Stack.Navigator>
  )
}
```

**Flutter (GoRouter 14):**
```dart
// router/app_router.dart
final appRouter = GoRouter(
  routes: [
    ShellRoute(
      builder: (context, state, child) => AppShell(child: child),
      routes: [
        GoRoute(
          path: '/home',
          builder: (context, state) => const HomeScreen(),
          routes: [
            GoRoute(
              path: ':itemId',
              builder: (context, state) =>
                  DetailScreen(itemId: state.pathParameters['itemId']!),
            ),
          ],
        ),
      ],
    ),
  ],
);
```

**Swift (NavigationStack):**
```swift
// Navigation/HomeCoordinator.swift
enum HomeDestination: Hashable {
    case detail(itemId: String)
}

struct HomeCoordinator: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            HomeScreen()
                .navigationDestination(for: HomeDestination.self) { dest in
                    switch dest {
                    case .detail(let id): DetailScreen(itemId: id)
                    }
                }
        }
    }
}
```

### 1.3 — Data Models

Define models before screens. Models drive everything.

```
┌──────────────────────────────────────────────────────────────┐
│  MODEL DEFINITION CHECKLIST                                  │
│                                                              │
│  □ API response model (what the server sends)                │
│  □ Domain model (what the app uses internally)               │
│  □ Local storage model (what gets persisted on device)       │
│  □ UI state model (what the screen needs to render)          │
│  □ Form model (what the user edits — may differ from API)    │
│                                                              │
│  Keep them separate. A single model for all layers is a      │
│  coupling trap that breaks when the API changes.             │
└──────────────────────────────────────────────────────────────┘
```

| Model Layer | Purpose | Example |
|------------|---------|---------|
| **API DTO** | Exact server shape, parsing only | `ItemResponse { id, title, created_at }` |
| **Domain** | App logic shape, clean types | `Item { id, title, createdAt: Date }` |
| **Local** | Persistence schema | `ItemEntity` with DB column mapping |
| **UI State** | What the screen renders | `ItemViewState { item, isEditing, error }` |

### 1.4 — Deep Link Registration

Register deep links before building screens — not after:

```
┌──────────────────────────────────────────────────────┐
│  DEEP LINK MAP                                       │
│                                                      │
│  URL Pattern           → Screen        → Params      │
│  ─────────────────────────────────────────────────── │
│  /items                → HomeScreen    → none         │
│  /items/:id            → DetailScreen  → itemId       │
│  /items/:id/edit       → EditModal     → itemId       │
│  /items/new            → CreateScreen  → none         │
│                                                      │
│  Fallback: unknown paths → HomeScreen                │
│  Auth guard: redirect to login if not authenticated  │
└──────────────────────────────────────────────────────┘
```

**Phase 1 output:** Navigation graph defined, routes registered, data models created, deep links mapped.

---

## Phase 2: Data Layer — API, Storage, Repository

Build from the data outward. Never build UI without a working data layer.

### 2.1 — Repository Pattern

```
┌──────────────────────────────────────────────────────────────┐
│                    REPOSITORY PATTERN                         │
│                                                              │
│  Screen ──▶ ViewModel/Bloc ──▶ Repository ──▶ Data Source    │
│                                     │                        │
│                                     ├── RemoteDataSource     │
│                                     │     └── API Client     │
│                                     │                        │
│                                     └── LocalDataSource      │
│                                           └── MMKV / Hive /  │
│                                               SwiftData      │
│                                                              │
│  The repository decides: serve from cache or network?        │
│  The screen never knows or cares.                            │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 — API Integration

**React Native (Axios + React Query):**
```tsx
// api/items.ts
export const itemKeys = {
  all: ['items'] as const,
  detail: (id: string) => ['items', id] as const,
}

export function useItems() {
  return useQuery({
    queryKey: itemKeys.all,
    queryFn: () => apiClient.get<Item[]>('/items').then(r => r.data),
    staleTime: 5 * 60 * 1000,
  })
}

export function useCreateItem() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: CreateItemInput) =>
      apiClient.post<Item>('/items', data).then(r => r.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: itemKeys.all }),
  })
}
```

**Flutter (Dio + Riverpod):**
```dart
// repositories/item_repository.dart
final itemRepositoryProvider = Provider<ItemRepository>((ref) {
  return ItemRepository(ref.read(dioProvider), ref.read(localStoreProvider));
});

class ItemRepository {
  final Dio _dio;
  final LocalStore _local;

  Future<List<Item>> getItems({bool forceRefresh = false}) async {
    if (!forceRefresh) {
      final cached = await _local.getItems();
      if (cached.isNotEmpty) return cached;
    }
    final response = await _dio.get('/items');
    final items = (response.data as List).map(Item.fromJson).toList();
    await _local.saveItems(items);
    return items;
  }
}
```

**Swift (async/await + URLSession):**
```swift
// Repositories/ItemRepository.swift
actor ItemRepository {
    private let apiClient: APIClient
    private let store: ItemStore

    func getItems(forceRefresh: Bool = false) async throws -> [Item] {
        if !forceRefresh, let cached = try? await store.fetchAll(), !cached.isEmpty {
            return cached
        }
        let items = try await apiClient.get([Item].self, from: "/items")
        try await store.save(items)
        return items
    }
}
```

### 2.3 — Offline Strategy Decision Tree

```
What type of data is this feature showing?
│
├── Read-only reference data (catalog, settings)
│   → Cache on first fetch, serve from cache, refresh in background
│   → Strategy: STALE-WHILE-REVALIDATE
│
├── User-generated content (posts, notes, orders)
│   → Cache locally, queue writes, sync when online
│   → Strategy: OFFLINE-FIRST with WRITE QUEUE
│
├── Real-time data (chat, live scores, stock prices)
│   → Show last known value + "updating..." indicator
│   → Strategy: WEBSOCKET with LAST-KNOWN-VALUE fallback
│
└── Transactional data (payments, bookings)
    → Do NOT allow offline mutations — show clear "no connection" state
    → Strategy: ONLINE-ONLY with graceful blocking
```

### 2.4 — Error Handling

Define error types before building screens:

```
┌──────────────────────────────────────────────────────────────┐
│  ERROR TYPE TAXONOMY                                         │
│                                                              │
│  NetworkError                                                │
│  ├── NoConnection      → Show offline banner, serve cache    │
│  ├── Timeout           → Show retry button                   │
│  └── ServerError (5xx) → Show "try again later" message      │
│                                                              │
│  ClientError                                                 │
│  ├── Unauthorized (401)→ Redirect to login                   │
│  ├── Forbidden (403)   → Show "no access" state              │
│  ├── NotFound (404)    → Show "item not found" state         │
│  └── Validation (422)  → Show inline field errors            │
│                                                              │
│  LocalError                                                  │
│  ├── StorageFull       → Prompt user to free space           │
│  └── CorruptData       → Clear cache, re-fetch               │
└──────────────────────────────────────────────────────────────┘
```

**Phase 2 output:** Repository with API + local source, offline strategy chosen, error types defined.

---

## Phase 3: UI Implementation — Platform-Adaptive Screens

Build screens that feel native on every platform.

### 3.1 — Platform Pattern Decision Tree

```
Which UI pattern should I use?
│
├── Navigation bar at top?
│   ├── iOS → Large title, system back button, trailing actions
│   └── Android → Top app bar, navigation icon, overflow menu
│
├── List with actions?
│   ├── iOS → Swipe actions (leading/trailing), long press context menu
│   └── Android → Long press selection mode, FAB for primary action
│
├── Form input?
│   ├── iOS → Grouped inset list style, toggle switches
│   └── Android → Outlined text fields, Material switches
│
├── Confirmation dialog?
│   ├── iOS → Action sheet from bottom (destructive in red)
│   └── Android → AlertDialog centered, text buttons
│
├── Loading indicator?
│   ├── iOS → Native ActivityIndicator (spinner)
│   └── Android → CircularProgressIndicator (Material)
│
└── Bottom action area?
    ├── iOS → Safe area padding, full-width button
    └── Android → FAB or bottom app bar
```

### 3.2 — Screen Structure Template

Every screen follows this skeleton:

```
┌──────────────────────────────────────────┐
│  Status Bar (system)                     │
├──────────────────────────────────────────┤
│  Navigation Bar / App Bar                │
│  ┌──────────────────────────────────┐    │
│  │ Back │   Title    │ Action(s)   │    │
│  └──────────────────────────────────┘    │
├──────────────────────────────────────────┤
│                                          │
│  Content Area (scrollable)               │
│  ┌──────────────────────────────────┐    │
│  │                                  │    │
│  │  Loading: Skeleton / Spinner     │    │
│  │  Loaded:  Actual content         │    │
│  │  Empty:   Illustration + CTA     │    │
│  │  Error:   Message + Retry        │    │
│  │                                  │    │
│  └──────────────────────────────────┘    │
│                                          │
├──────────────────────────────────────────┤
│  Bottom Safe Area                        │
│  ┌──────────────────────────────────┐    │
│  │  Primary Action Button (if any)  │    │
│  └──────────────────────────────────┘    │
├──────────────────────────────────────────┤
│  Tab Bar / Bottom Nav (if tab screen)    │
└──────────────────────────────────────────┘
```

### 3.3 — UI State Matrix

Every data-driven screen must handle all four states:

| State | What to Show | User Action |
|-------|-------------|-------------|
| **Loading** | Skeleton placeholders matching content layout | None — wait |
| **Loaded** | Actual data in designed layout | Interact normally |
| **Empty** | Friendly illustration + description + CTA button | Tap CTA to create first item |
| **Error** | Error icon + message + retry button | Tap retry, pull to refresh |

### 3.4 — Platform-Adaptive Component Pattern

**React Native — Platform.select:**
```tsx
// components/AdaptiveHeader.tsx
export function AdaptiveHeader({ title, onAction }: Props) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
      {Platform.select({
        ios: (
          <TouchableOpacity onPress={onAction}>
            <Text style={styles.iosAction}>Edit</Text>
          </TouchableOpacity>
        ),
        android: (
          <IconButton icon="pencil" onPress={onAction} />
        ),
      })}
    </View>
  )
}
```

**Flutter — .adaptive constructors:**
```dart
// widgets/adaptive_dialog.dart
Future<bool?> showAdaptiveConfirmDialog(BuildContext context, String message) {
  return showAdaptiveDialog<bool>(
    context: context,
    builder: (context) => AlertDialog.adaptive(
      title: const Text('Confirm'),
      content: Text(message),
      actions: [
        adaptiveAction(context, 'Cancel', () => Navigator.pop(context, false)),
        adaptiveAction(context, 'Delete', () => Navigator.pop(context, true),
            isDestructive: true),
      ],
    ),
  );
}
```

**Swift — native by default:**
```swift
// Views/ItemListView.swift
struct ItemListView: View {
    @State private var items: [Item] = []

    var body: some View {
        List {
            ForEach(items) { item in
                ItemRow(item: item)
                    .swipeActions(edge: .trailing) {
                        Button(role: .destructive) { delete(item) } label: {
                            Label("Delete", systemImage: "trash")
                        }
                    }
            }
        }
        .refreshable { await refresh() }
        .searchable(text: $searchText)
    }
}
```

### 3.5 — Safe Area and Keyboard Handling

```
┌──────────────────────────────────────────────────────────────┐
│  SAFE AREA RULES                                             │
│                                                              │
│  Top: Navigation bar handles it — do NOT add extra padding   │
│  Bottom: Add SafeAreaView / SafeArea for content that sits   │
│          above tab bar or home indicator                     │
│  Keyboard: Use KeyboardAvoidingView (RN), Scaffold resizing  │
│           (Flutter), or .scrollDismissesKeyboard (SwiftUI)   │
│                                                              │
│  Common mistakes:                                            │
│  x Double safe area padding (content + container both add)   │
│  x Button hidden behind keyboard on form screens             │
│  x Content clipped by notch on landscape                     │
│  x Bottom sheet overlapping home indicator                   │
└──────────────────────────────────────────────────────────────┘
```

**Phase 3 output:** All screens built with platform-adaptive UI, all 4 states handled, safe areas correct.

---

## Phase 4: State & Business Logic

### 4.1 — State Management by Platform

| Framework | Local State | Screen State | Global State | Server State |
|-----------|------------|-------------|-------------|-------------|
| **React Native** | `useState` | `useReducer` | Zustand store | React Query |
| **Flutter** | `StatefulWidget` | `StateNotifier` | Riverpod providers | `AsyncValue` |
| **SwiftUI** | `@State` | `@Observable` class | `@Environment` | async/await + `@Observable` |

### 4.2 — State Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                   STATE FLOW                                 │
│                                                              │
│  User Action                                                 │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────┐    Dispatch     ┌──────────────────┐        │
│  │   Screen    │ ──────────────▶ │  ViewModel /     │        │
│  │   (View)    │                 │  Bloc / Store    │        │
│  │             │ ◀────────────── │                  │        │
│  └─────────────┘    New State    └────────┬─────────┘        │
│                                           │                  │
│                                   ┌───────┴────────┐         │
│                                   │                │         │
│                                   ▼                ▼         │
│                            ┌──────────┐    ┌────────────┐    │
│                            │Repository│    │ Navigation │    │
│                            │ (data)   │    │ (routing)  │    │
│                            └──────────┘    └────────────┘    │
│                                                              │
│  Rules:                                                      │
│  • Views are dumb — they render state, dispatch actions      │
│  • ViewModels own business logic — they never import UI      │
│  • Repositories own data — they never know about screens     │
│  • Navigation is a side effect — triggered by state changes  │
└──────────────────────────────────────────────────────────────┘
```

### 4.3 — Form Validation

Mobile forms need instant, inline validation — not server-round-trip validation.

```
┌──────────────────────────────────────────────────────────────┐
│  FORM VALIDATION FLOW                                        │
│                                                              │
│  User types ──▶ Debounce (300ms) ──▶ Validate field          │
│                                           │                  │
│                                    ┌──────┴──────┐           │
│                                    │             │           │
│                                  Valid        Invalid        │
│                                    │             │           │
│                              Clear error    Show inline      │
│                              Enable submit  error below      │
│                                             field            │
│                                             Disable submit   │
│                                                              │
│  On Submit ──▶ Validate ALL fields ──▶ API call              │
│                     │                      │                 │
│                  Invalid               ┌───┴───┐             │
│                     │               Success   Server Error   │
│                  Scroll to            │          │            │
│                  first error       Navigate   Map server     │
│                  field             forward    errors to       │
│                                              field errors    │
└──────────────────────────────────────────────────────────────┘
```

### 4.4 — Side Effects Checklist

Every feature needs these side effects considered:

```
□ Loading indicators — shown during async operations
□ Success feedback — toast/snackbar/haptic on mutation success
□ Error feedback — inline errors for validation, toast for network
□ Cache invalidation — refetch related queries after mutation
□ Navigation — push/pop/reset after successful operations
□ Analytics — track screen views, button taps, funnel steps
□ Permissions — request camera/location/notifications when needed
□ Background sync — queue failed mutations for retry
```

**Phase 4 output:** State management wired, forms validated, side effects handled, analytics tracked.

---

## Phase 5: Polish & Ship — The 20% That Takes 80% of the Effort

### 5.1 — Animation Guidelines

```
┌──────────────────────────────────────────────────────────────┐
│  ANIMATION RULES FOR MOBILE                                  │
│                                                              │
│  DO animate:                                                 │
│  • Screen transitions (use platform defaults first)          │
│  • List item insertions/deletions                            │
│  • State changes (loading → loaded, collapsed → expanded)    │
│  • Micro-interactions (button press, toggle, pull-to-refresh)│
│                                                              │
│  DO NOT animate:                                             │
│  • Initial data load (show skeleton, not fade-in)            │
│  • Every text change (use animation sparingly)               │
│  • Anything that blocks user interaction                     │
│                                                              │
│  Duration guide:                                             │
│  • Micro (button press): 100-150ms                           │
│  • Small (expand/collapse): 200-250ms                        │
│  • Medium (screen transition): 300-350ms                     │
│  • Large (modal present): 400-500ms                          │
│                                                              │
│  Easing:                                                     │
│  • iOS: .spring(response: 0.35, dampingFraction: 0.85)       │
│  • Android: FastOutSlowIn (Material standard)                │
│  • Avoid linear easing — it feels mechanical                 │
└──────────────────────────────────────────────────────────────┘
```

### 5.2 — Haptics

| Action | iOS | Android |
|--------|-----|---------|
| Button tap | `.impact(.light)` | `HapticFeedbackConstants.VIRTUAL_KEY` |
| Success | `.notification(.success)` | `HapticFeedbackConstants.CONFIRM` |
| Error | `.notification(.error)` | `HapticFeedbackConstants.REJECT` |
| Toggle switch | `.impact(.medium)` | `HapticFeedbackConstants.CLOCK_TICK` |
| Destructive action | `.notification(.warning)` | Long vibration pattern |
| Pull to refresh | `.impact(.light)` at threshold | Default system behavior |

### 5.3 — Accessibility Checklist

```
┌──────────────────────────────────────────────────────────────┐
│  ACCESSIBILITY — NON-NEGOTIABLE FOR SHIP                     │
│                                                              │
│  □ Every interactive element has an accessibility label       │
│  □ Images have alt text (decorative images marked as such)   │
│  □ Touch targets are minimum 44x44pt (iOS) / 48x48dp (Droid)│
│  □ Color is never the only indicator (add icons or text)     │
│  □ Screen reader navigation order is logical                 │
│  □ Dynamic type / font scaling works up to 200%              │
│  □ Focus management: modals trap focus, dismiss returns it   │
│  □ Contrast ratio: 4.5:1 for text, 3:1 for large text       │
│  □ Reduce motion: honor system preference, disable parallax  │
│  □ VoiceOver (iOS) and TalkBack (Android) tested manually    │
└──────────────────────────────────────────────────────────────┘
```

### 5.4 — Dark Mode

```
Rules:
1. Never hardcode colors — use semantic tokens (background, surface, text)
2. Test dark mode on OLED screens — pure black (#000) vs dark gray (#1C1C1E)
3. Shadows don't work in dark mode — use borders or elevation instead
4. Images may need dark mode variants (logos, illustrations)
5. Status bar style must adapt (light content on dark background)

Color Token Pattern:
┌────────────────┬──────────────┬──────────────┐
│ Token          │ Light        │ Dark         │
├────────────────┼──────────────┼──────────────┤
│ background     │ #FFFFFF      │ #000000      │
│ surface        │ #F2F2F7      │ #1C1C1E      │
│ surfaceRaised  │ #FFFFFF      │ #2C2C2E      │
│ textPrimary    │ #000000      │ #FFFFFF      │
│ textSecondary  │ #8E8E93      │ #8E8E93      │
│ separator      │ #C6C6C8      │ #38383A      │
│ accentPrimary  │ #007AFF      │ #0A84FF      │
│ destructive    │ #FF3B30      │ #FF453A      │
└────────────────┴──────────────┴──────────────┘
```

### 5.5 — RTL (Right-to-Left) Support

```
□ Layout mirrors correctly (leading/trailing, not left/right)
□ Icons that imply direction are flipped (arrows, back buttons)
□ Text alignment follows reading direction
□ Swipe gestures are mirrored
□ Progress bars fill from right to left
□ Navigation back gesture works from right edge
□ Numbers and dates remain LTR even in RTL layout
```

### 5.6 — Performance Profiling

```
┌──────────────────────────────────────────────────────────────┐
│  PERFORMANCE BUDGET                                          │
│                                                              │
│  Metric              │ Target       │ How to Measure         │
│  ────────────────────┼──────────────┼─────────────────────── │
│  Screen render        │ < 16ms       │ Perf monitor overlay   │
│  (60fps = 16ms)       │              │                        │
│  ────────────────────┼──────────────┼─────────────────────── │
│  Time to interactive  │ < 300ms      │ Trace from nav start   │
│  (new screen)         │              │                        │
│  ────────────────────┼──────────────┼─────────────────────── │
│  List scroll          │ 0 dropped    │ React DevTools /       │
│  (60fps)              │ frames       │ Flutter DevTools        │
│  ────────────────────┼──────────────┼─────────────────────── │
│  Memory on navigate   │ No growth    │ Instruments / Android  │
│  back (leak check)    │ after GC     │ Profiler                │
│  ────────────────────┼──────────────┼─────────────────────── │
│  Image memory         │ < 50MB for   │ Xcode memory graph /   │
│  (decoded in RAM)     │ visible imgs │ Android Profiler        │
│  ────────────────────┼──────────────┼─────────────────────── │
│  JS bundle impact     │ < 50KB per   │ Metro bundle analyzer  │
│  (RN only)            │ feature      │                        │
│  ────────────────────┼──────────────┼─────────────────────── │
│  Cold start impact    │ < 50ms       │ App startup trace      │
│                       │ added        │                        │
└──────────────────────────────────────────────────────────────┘
```

**Common performance pitfalls:**

| Problem | Symptom | Fix |
|---------|---------|-----|
| Re-renders on scroll | Janky list, dropped frames | Memoize list items, use `getItemLayout` / `itemExtent` |
| Large images | Memory spike, OOM crash | Resize on server, use progressive loading, cache with size limit |
| Inline closures | Unnecessary re-renders | Extract handlers, use `useCallback` / `const` constructors |
| Unoptimized lists | Slow scroll on long lists | Use `FlatList` / `ListView.builder` / `LazyVStack` — never `ScrollView` for dynamic lists |
| Missing key prop | List re-renders entire tree | Use stable unique IDs, never array index |

**Phase 5 output:** Animations tuned, haptics wired, a11y passing, dark mode correct, RTL verified, performance budgets met.

---

## Complete Feature Checklist — Before Calling It Done

```
┌──────────────────────────────────────────────────────────────┐
│  MOBILE FEATURE SHIP CHECKLIST                               │
│                                                              │
│  Navigation & Structure                                      │
│  □ Navigation graph matches design spec                      │
│  □ Deep links work for all screens                           │
│  □ Back behavior is correct on both platforms                │
│  □ Screen state restores after backgrounding                 │
│  □ Orientation handling is correct (lock or adapt)           │
│                                                              │
│  Data Layer                                                  │
│  □ API integration tested with real backend                  │
│  □ Error responses handled for all endpoints                 │
│  □ Offline behavior defined and implemented                  │
│  □ Local cache populated and served correctly                │
│  □ Auth token refresh works mid-flow                         │
│  □ Pagination implemented for list endpoints                 │
│                                                              │
│  UI / UX                                                     │
│  □ All 4 states rendered: loading, loaded, empty, error      │
│  □ Platform-specific patterns used (iOS vs Android)          │
│  □ Pull-to-refresh on list screens                           │
│  □ Keyboard avoidance on form screens                        │
│  □ Safe area insets respected (notch, home indicator)         │
│  □ Large text / dynamic type does not break layout           │
│                                                              │
│  State & Logic                                               │
│  □ State management follows project pattern                  │
│  □ Form validation with inline errors                        │
│  □ Optimistic updates with rollback on failure               │
│  □ No memory leaks on navigate back                          │
│  □ No stale closures or zombie subscriptions                 │
│                                                              │
│  Polish                                                      │
│  □ Dark mode renders correctly                               │
│  □ RTL layout mirrors properly                               │
│  □ Haptic feedback on key interactions                       │
│  □ Animations use platform-appropriate duration and easing   │
│  □ Accessibility labels on all interactive elements          │
│  □ VoiceOver / TalkBack walkthrough completed                │
│                                                              │
│  Performance                                                 │
│  □ 60fps scroll on lowest-tier supported device              │
│  □ No memory growth after repeated navigation                │
│  □ Image caching with size limits                            │
│  □ Bundle size impact measured (< 50KB per feature)          │
│  □ Cold start impact measured (< 50ms added)                 │
│                                                              │
│  Testing                                                     │
│  □ Tested on real iOS device (not just simulator)            │
│  □ Tested on real Android device (not just emulator)         │
│  □ Tested with airplane mode enabled                         │
│  □ Tested with slow network (Network Link Conditioner)       │
│  □ Tested with system font size set to maximum               │
│  □ Tested after fresh install (no cached data)               │
└──────────────────────────────────────────────────────────────┘
```

---

## Tips for Best Results

1. **Draw the navigation graph on paper first.** Mobile features live or die by their navigation flow. A screen that is hard to reach or hard to leave back from will frustrate users regardless of how polished it looks.

2. **Build the data layer before any UI.** Fetch real data from the API and log it to the console before creating a single component. Working with real data shapes exposes API contract mismatches immediately instead of during integration.

3. **Test on the worst device you support.** That 2019 budget Android phone with 3GB RAM is your true performance baseline. If it scrolls at 60fps there, it scrolls at 60fps everywhere.

4. **Use platform defaults before customizing.** System navigation transitions, pull-to-refresh physics, keyboard avoidance — the OS does these well. Override only when you have a specific reason and your replacement is measurably better.

5. **Handle the empty state with the same care as the loaded state.** The empty state is often the first thing a new user sees. A blank screen with no guidance is an invitation to close the app.

6. **Profile memory after implementing navigation.** The most common mobile memory leak is a screen that does not clean up subscriptions, timers, or observers when popped from the navigation stack. Navigate forward and back 10 times — memory should return to baseline.

7. **Airplane mode is your integration test.** Toggle airplane mode at every step of your feature flow. Every screen should degrade gracefully — show cached data, disable mutation buttons, display a connection banner.

8. **Ship haptics.** Subtle haptic feedback on button presses, toggle switches, and destructive actions makes an app feel tangible and premium. It takes 5 minutes to add and users notice its absence.

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
