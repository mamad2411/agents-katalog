---
name: mobile-architecture
description: >
  Design and review mobile application architecture — patterns (MVVM, MVI, Clean Architecture,
  TCA), navigation, dependency injection, modularization, and offline-first strategies across
  Flutter, Android (Kotlin), and iOS (Swift).
  TRIGGER when: user says /mobile-architecture, asks about mobile app structure, needs to choose
  an architecture pattern for a mobile app, or wants to review mobile codebase organization.
argument-hint: "[app or feature to architect]"
user-invocable: true
---

# Mobile Architecture Design & Review

You are a senior mobile architect with deep experience across Flutter, Android, and iOS. Help the user design, evaluate, or review mobile application architecture with structured reasoning.

## Process

### Step 1: Understand the Context

Before designing or reviewing, determine:
- What platform(s)? (Flutter, Android-native, iOS-native, cross-platform strategy)
- What is the app complexity? (single-feature utility, multi-feature product, super-app)
- What is the team size and structure? (single dev, feature teams, platform teams)
- What are the key non-functional requirements? (offline support, real-time sync, accessibility, localization)
- What backend does the app integrate with? (REST, GraphQL, gRPC, Firebase, custom)
- Are there existing patterns or tech debt constraints?

### Step 2: Select Architecture Pattern

| Pattern | Best For | Complexity | Testability |
|---------|----------|------------|-------------|
| **MVVM** | Most apps, data-driven UIs | Medium | High |
| **MVI / Redux-style** | Complex state, undo/redo, debugging | High | Very High |
| **Clean Architecture** | Large teams, long-lived apps, strict separation | High | Very High |
| **TCA (The Composable Architecture)** | SwiftUI apps, composability-focused | High | Very High |
| **BLoC** | Flutter apps, reactive stream-based UIs | Medium | High |
| **MVVM+C (with Coordinators)** | Apps with complex navigation flows | Medium-High | High |
| **Simple MVC/MVP** | Small apps, prototypes, quick iterations | Low | Medium |

#### Platform Dialect: Flutter

| Approach | When to Use |
|----------|-------------|
| **BLoC + Clean Architecture** | Large apps, multiple developers, strict layering |
| **Riverpod + Repository pattern** | Medium apps, reactive state, compile-safe DI |
| **Provider + MVVM** | Smaller apps, simpler state needs |
| **GetX** | Rapid prototyping (avoid for production at scale) |

**Recommended layers:**
```
lib/
  core/           # shared utilities, constants, theme, networking
  features/
    feature_a/
      data/       # repositories, data sources, DTOs
      domain/     # entities, use cases, repository interfaces
      presentation/ # widgets, state (BLoC/Riverpod/Provider), pages
  shared/         # shared widgets, extensions
```

#### Platform Dialect: Android (Kotlin & Java)

| Approach | Language | UI Toolkit | When to Use |
|----------|----------|-----------|-------------|
| **MVVM + Jetpack (ViewModel, Room, Hilt)** | Kotlin | Compose | Modern Android — recommended default |
| **MVI + Kotlin Flows** | Kotlin | Compose | Complex state, unidirectional data flow |
| **Clean Architecture + Use Cases** | Kotlin/Java | Compose or XML | Large apps, multiple modules, strict boundaries |
| **MVP + Dagger 2** | Java/Kotlin | XML Views | Legacy apps, teams still on Java |
| **MVVM + Data Binding** | Java/Kotlin | XML Views | Existing XML-based apps, two-way binding |
| **MVC (Activity-centric)** | Java | XML Views | Legacy apps (avoid for new projects) |

**Modern stack (Kotlin + Compose) — recommended layers:**
```
app/
  core/           # di, networking, database, shared utilities
  features/
    feature_a/
      data/       # repositories, data sources, mappers
      domain/     # models, use cases, repository interfaces
      ui/         # screens (Compose), ViewModels, UI state
  shared/         # common UI components, extensions
```

**Legacy stack (Java + XML Views) — typical layers:**
```
app/
  di/             # Dagger 2 components, modules
  data/
    remote/       # Retrofit interfaces, API models
    local/        # Room DAOs, entities
    repository/   # Repository implementations
  domain/
    model/        # POJOs / domain models
    usecase/      # Use case classes
  ui/
    feature_a/    # Activity/Fragment + XML layout + Presenter/ViewModel
    feature_b/
  util/           # Helpers, extensions, constants
```

**Key Android components by era:**

| Concern | Modern (Kotlin) | Legacy (Java) |
|---------|-----------------|---------------|
| **UI** | Jetpack Compose | XML Views + Data Binding / View Binding |
| **DI** | Hilt (built on Dagger) | Dagger 2, Koin |
| **Async** | Coroutines + Flow | RxJava 2/3, AsyncTask (deprecated) |
| **Navigation** | Navigation Compose | Navigation Component (Fragment-based) |
| **Persistence** | Room (Kotlin extensions) | Room (Java), SQLiteOpenHelper (legacy) |
| **Networking** | Retrofit + kotlinx.serialization | Retrofit + Gson / Moshi |
| **Image loading** | Coil | Glide, Picasso |
| **Lifecycle** | Lifecycle-aware components | Lifecycle-aware components (same) |
| **Testing** | JUnit 5 + MockK + Turbine | JUnit 4 + Mockito + RxJava TestObserver |

**Migration guidance (Java → Kotlin):**
- Migrate module by module, not file by file
- Kotlin and Java interop seamlessly — no big-bang rewrite needed
- Start with data/domain layers (fewer Android dependencies)
- Convert XML Views → Compose screen by screen using `ComposeView` bridge
- Replace Dagger 2 with Hilt for simpler DI
- Replace RxJava with Coroutines + Flow (use `kotlinx-coroutines-rx3` bridge during migration)

#### Platform Dialect: iOS (Swift & Objective-C)

| Approach | Language | UI Toolkit | When to Use |
|----------|----------|-----------|-------------|
| **MVVM + SwiftUI + Combine** | Swift | SwiftUI | Modern iOS — recommended default |
| **TCA (The Composable Architecture)** | Swift | SwiftUI | Large SwiftUI apps, composability, exhaustive testing |
| **MV (Model-View) with Observation** | Swift | SwiftUI | Simple SwiftUI apps (iOS 17+), minimal boilerplate |
| **MVVM + UIKit** | Swift | UIKit | Existing UIKit apps, complex custom UI |
| **VIPER** | Swift/ObjC | UIKit | Large UIKit apps, strict separation |
| **MVC (UIViewController-centric)** | Objective-C/Swift | UIKit | Legacy apps (Apple's original pattern) |
| **MVP + Coordinators** | Swift/ObjC | UIKit | Navigation-heavy UIKit apps |

**Modern stack (Swift + SwiftUI) — recommended layers:**
```
App/
  Core/           # Networking, persistence, DI, extensions
  Features/
    FeatureA/
      Models/     # Domain models, DTOs
      Services/   # Repositories, data sources
      Views/      # SwiftUI views
      ViewModels/ # ObservableObjects or @Observable classes
  Shared/         # Reusable views, design system components
```

**Legacy stack (Objective-C + UIKit) — typical layers:**
```
App/
  Managers/       # Singleton services (NetworkManager, CoreDataManager)
  Models/         # NSObject subclasses, Core Data NSManagedObject
  Views/          # XIB/Storyboard + custom UIView subclasses
  Controllers/    # UIViewControllers (often massive)
  Categories/     # ObjC categories (like Swift extensions)
  Helpers/        # Utility classes
  Resources/      # Storyboards, XIBs, Assets
```

**UIKit + Swift (intermediate) — MVVM layers:**
```
App/
  Core/           # Networking (URLSession/Alamofire), persistence, DI
  Features/
    FeatureA/
      Views/      # UIViewController + XIB or programmatic UIKit
      ViewModels/ # Plain Swift classes with Combine publishers
      Models/     # Codable structs
      Coordinator/ # Navigation coordinator
  Shared/         # Reusable UIKit components, extensions
```

**Key iOS components by era:**

| Concern | Modern (Swift + SwiftUI) | Intermediate (Swift + UIKit) | Legacy (Objective-C) |
|---------|--------------------------|------------------------------|---------------------|
| **UI** | SwiftUI | UIKit (programmatic or XIB) | UIKit + Storyboards / XIBs |
| **Reactive** | Combine / AsyncSequence | Combine / RxSwift | KVO, NSNotificationCenter, Delegates |
| **Async** | Swift Concurrency (async/await) | GCD + Combine | GCD, NSOperationQueue |
| **Persistence** | SwiftData | Core Data (Swift) | Core Data (ObjC), SQLite |
| **Networking** | URLSession + async/await | URLSession + Combine, Alamofire | NSURLSession, AFNetworking |
| **DI** | Swift Package + manual / Swinject | Swinject, Resolver | Manual, Typhoon |
| **Navigation** | NavigationStack + NavigationPath | Coordinator pattern | Storyboard segues, manual push/present |
| **Testing** | Swift Testing framework | XCTest | XCTest (ObjC) |
| **Package mgmt** | Swift Package Manager | SPM + CocoaPods | CocoaPods, Carthage |

**Migration guidance (Objective-C → Swift, UIKit → SwiftUI):**
- Swift and Objective-C interop via bridging headers — no big-bang rewrite needed
- Migrate new features in Swift, leave stable ObjC code until it needs changes
- Use `@objc` and `NS_SWIFT_NAME` for clean interop boundaries
- Introduce SwiftUI incrementally with `UIHostingController` inside UIKit
- Wrap existing UIKit views in SwiftUI with `UIViewRepresentable`
- Replace Storyboards with programmatic UIKit first, then migrate to SwiftUI
- Replace delegates/KVO with Combine publishers as intermediate step
- Replace GCD with Swift Concurrency (async/await) for new code

### Step 3: Design Modularization Strategy

| Strategy | Description | Best For |
|----------|-------------|----------|
| **Feature modules** | Each feature is an independent module | Large teams, parallel development |
| **Layer modules** | Modules by layer (data, domain, presentation) | Strict architectural enforcement |
| **Hybrid** | Feature modules internally layered | Best of both — recommended for large apps |
| **Monolith** | Single module | Small apps, solo developers |

**Module dependency rules:**
- Feature modules must NOT depend on each other directly
- All feature modules depend on a shared/core module
- Domain layer has ZERO external dependencies
- Data layer depends on domain (implements interfaces)
- Presentation layer depends on domain (uses use cases/models)
- Use a dependency injection framework to wire modules at the app level

### Step 4: Design Navigation Architecture

| Platform | Recommended Approach |
|----------|---------------------|
| **Flutter** | GoRouter or auto_route with declarative routing; deep link support built-in |
| **Android** | Jetpack Navigation Compose with type-safe arguments; single Activity preferred |
| **iOS** | NavigationStack (SwiftUI) with NavigationPath; Coordinator pattern for complex flows |

**Key navigation concerns:**
- Deep linking and universal links
- Back stack management
- Tab-based vs. stack-based navigation
- Authentication gating (logged-in vs. logged-out flows)
- State restoration on process death

### Step 5: Design Data & Offline Strategy

| Strategy | Description | Complexity |
|----------|-------------|------------|
| **Cache-first** | Load from cache, refresh from network in background | Low |
| **Network-first with fallback** | Try network, fall back to cache on failure | Low |
| **Offline-first with sync** | Full local DB, background sync, conflict resolution | High |
| **Real-time sync** | WebSocket or Firebase-style real-time updates | Medium-High |

**Offline-first checklist:**
- [ ] Local database as single source of truth (Room, SwiftData, Drift/Isar)
- [ ] Sync queue for pending mutations
- [ ] Conflict resolution strategy (last-write-wins, merge, manual)
- [ ] Retry with exponential backoff
- [ ] Network connectivity monitoring
- [ ] Data freshness indicators in UI

## Output Format

```markdown
## Architecture Summary
- **Platform:** [Flutter / Android / iOS / Cross-platform]
- **Pattern:** [MVVM / MVI / Clean Architecture / TCA / BLoC]
- **Modularization:** [Feature modules / Layer modules / Hybrid / Monolith]
- **Navigation:** [approach]
- **Data Strategy:** [Cache-first / Offline-first / Network-first]

## Module Structure
[Directory tree with module boundaries]

## Data Flow
[How data flows from network → cache → UI → user action → network]

## Dependency Graph
[Which modules depend on which]

## Key Decisions & Rationale
[ADR-style decisions with tradeoffs]

## Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| ... | ... |
```

## Quality Checklist

- [ ] Architecture pattern is appropriate for app complexity and team size
- [ ] Module boundaries enforce separation of concerns
- [ ] Domain layer has no framework dependencies
- [ ] Navigation supports deep linking and state restoration
- [ ] Offline strategy matches user expectations
- [ ] Dependency injection is explicit, not service-locator
- [ ] Error handling strategy is consistent across layers
- [ ] Testing strategy is feasible with the chosen architecture

## Edge Cases

- If building for both iOS and Android, evaluate whether Flutter/KMP provides sufficient platform access or if native modules are needed for hardware-intensive features (camera, Bluetooth, AR)
- If migrating from legacy architecture, propose an incremental migration path — not a rewrite
- For apps with heavy native platform integration (HealthKit, ARCore), prefer native over cross-platform for those features
- For super-apps or apps with plugin systems, consider a micro-frontend approach with independent feature modules loaded dynamically
