---
name: ios-swiftui
description: >
  Expert SwiftUI development skill for building iOS apps. Covers layout system (VStack/HStack/ZStack/Grid/LazyStacks),
  state management (@State/@Binding/@Observable/@Environment), navigation (NavigationStack/NavigationSplitView),
  animations (springs/transitions/matchedGeometryEffect/PhaseAnimator/KeyframeAnimator), lists and scroll views,
  sheets/alerts/popovers, custom ViewModifiers and ViewBuilders, SwiftUI lifecycle, performance optimization,
  and UIKit interop. Use this skill whenever the user builds SwiftUI views, layouts, navigation, animations,
  or asks about SwiftUI state management, view lifecycle, or performance. Triggers on any SwiftUI-related work
  including: SwiftUI, View, @State, @Binding, @Observable, NavigationStack, List, ScrollView, sheet, alert,
  animation, transition, ViewModifier, @ViewBuilder, GeometryReader, LazyVStack, TabView, toolbar, searchable,
  AsyncImage, or any iOS UI development with Swift.
---

# iOS SwiftUI Expert Skill

## Core Rules

1. **Use @Observable (iOS 17+) over ObservableObject** — fine-grained property tracking, better performance, simpler syntax.
2. **Use @State to own @Observable instances**, NOT @StateObject. `@StateObject` is the pre-iOS 17 pattern.
3. **Use NavigationStack** (not NavigationView) with value-based `NavigationLink` + `.navigationDestination`.
4. **Never nest NavigationStack inside NavigationStack** — causes double navigation bars and broken behavior.
5. **Use LazyVStack/LazyHStack inside ScrollView** for large collections. Use `List` for very large datasets (cell reuse + prefetching).
6. **Keep `body` pure** — no data processing, network calls, or side effects. Use `.task` modifier for async work.
7. **Avoid `AnyView`** — it destroys view identity and kills diffing performance. Use `@ViewBuilder` or `Group` instead.
8. **Preserve view identity** — use ternary operators (`condition ? viewA : viewB`), not `if/else` that changes the view type in ways that break animations.
9. **Break large views into small subviews** — SwiftUI re-evaluates `body` often; smaller views = smaller re-evaluation scope.
10. **Use `.equatable()`** on expensive views to skip unnecessary re-renders.

---

## Decision Tables

### State Management — What to Use When

| Scenario | iOS 17+ | Pre-iOS 17 |
|---|---|---|
| Simple value owned by view | `@State` | `@State` |
| Pass value down for read/write | `@Binding` | `@Binding` |
| Reference-type model owned by view | `@State` + `@Observable` | `@StateObject` + `ObservableObject` |
| Reference-type model passed in | just pass it (auto-tracked) | `@ObservedObject` |
| Shared model via environment | `@Environment` + custom key | `@EnvironmentObject` |
| Create binding to @Observable property | `@Bindable` | N/A (use `@Published` + `$`) |
| System environment values | `@Environment(\.colorScheme)` | same |

**Key insight:** With `@Observable`, SwiftUI tracks which properties a view *actually reads* in `body`. With `ObservableObject`, ANY `@Published` change triggers ALL observing views to re-evaluate.

### Layout — What Container to Use

| Need | Use | Why |
|---|---|---|
| Small fixed list of items | `VStack` / `HStack` | All children measured upfront, correct sizing |
| Large scrollable list (100+) | `LazyVStack` in `ScrollView` | Creates views on demand |
| Very large list (1000+) with editing | `List` | Cell reuse, prefetching, swipe actions |
| 2D grid layout | `LazyVGrid` / `LazyHGrid` | Flexible column/row definitions |
| Aligned rows + columns (small data) | `Grid` + `GridRow` (iOS 16+) | Alignment across rows |
| Responsive layout | `ViewThatFits` (iOS 16+) | Picks first child that fits |

### Navigation — Which Pattern

| Need | Use |
|---|---|
| Linear drill-down (push/pop) | `NavigationStack` with path |
| Master-detail (iPad) | `NavigationSplitView` |
| Tab-based app | `TabView` (iOS 18: `Tab` items) |
| Modal presentation | `.sheet`, `.fullScreenCover` |
| Programmatic deep linking | `NavigationStack(path:)` + `NavigationPath` |

### Presentation — Sheets vs Alerts vs Popovers

| Need | Use |
|---|---|
| Complex form/detail | `.sheet` or `.fullScreenCover` |
| Simple yes/no question | `.alert` |
| Choose from options | `.confirmationDialog` |
| Contextual info (iPad) | `.popover` |
| Half-height sheet | `.sheet` + `.presentationDetents([.medium])` |
| Non-dismissable sheet | `.interactiveDismissDisabled(true)` |

---

## Quick Patterns

### Creating an @Observable Model (iOS 17+)

```swift
@Observable
class UserViewModel {
    var name = ""
    var email = ""
    var isLoading = false

    @ObservationIgnored  // not tracked
    var internalCache: [String: Any] = [:]

    func load() async {
        isLoading = true
        defer { isLoading = false }
        // fetch data...
    }
}

struct UserView: View {
    @State private var viewModel = UserViewModel()

    var body: some View {
        Form {
            TextField("Name", text: $viewModel.name)  // needs @Bindable or use @State
        }
        .task { await viewModel.load() }
    }
}
```

Note: To get `$viewModel.name` binding from `@State`, you can access it directly. If the model is passed as a parameter (not `@State`), wrap with `@Bindable`:

```swift
struct EditView: View {
    @Bindable var viewModel: UserViewModel

    var body: some View {
        TextField("Name", text: $viewModel.name)
    }
}
```

### Navigation Stack with Programmatic Navigation

```swift
struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List(items) { item in
                NavigationLink(value: item) {
                    Text(item.title)
                }
            }
            .navigationDestination(for: Item.self) { item in
                DetailView(item: item, path: $path)
            }
            .navigationTitle("Items")
        }
    }
}
```

### Custom ViewModifier

```swift
struct CardModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(.background, in: .rect(cornerRadius: 12))
            .shadow(color: .black.opacity(0.1), radius: 4, y: 2)
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardModifier())
    }
}
```

### Async Data Loading

```swift
struct PostListView: View {
    @State private var posts: [Post] = []
    @State private var error: Error?

    var body: some View {
        List(posts) { post in
            Text(post.title)
        }
        .overlay {
            if posts.isEmpty && error == nil {
                ProgressView()
            }
            if let error {
                ContentUnavailableView("Error", systemImage: "exclamationmark.triangle",
                    description: Text(error.localizedDescription))
            }
        }
        .task {
            do {
                posts = try await api.fetchPosts()
            } catch {
                self.error = error
            }
        }
    }
}
```

---

## Reference File Routing

Use this table to decide which reference file to read for a given task:

| Task / Question | Read |
|---|---|
| Building layouts, stacks, grids | `references/layout.md` |
| ScrollView, List, ForEach, lazy containers | `references/layout.md` |
| @State, @Binding, @Observable, @Environment | `references/state.md` |
| ObservableObject, @Published, migration to @Observable | `references/state.md` |
| NavigationStack, NavigationSplitView, deep linking | `references/navigation.md` |
| Sheets, alerts, popovers, modals | `references/navigation.md` |
| TabView, toolbar, searchable | `references/navigation.md` |
| Animations, transitions, springs | `references/animation.md` |
| matchedGeometryEffect, hero animations | `references/animation.md` |
| PhaseAnimator, KeyframeAnimator | `references/animation.md` |
| Symbol effects, haptics | `references/animation.md` |
| ViewModifier, @ViewBuilder, PreferenceKey | `references/patterns.md` |
| GeometryReader, coordinate spaces | `references/patterns.md` |
| App lifecycle, scenePhase, .task, .onAppear | `references/patterns.md` |
| UIKit interop, UIViewRepresentable | `references/patterns.md` |
| Performance optimization | `references/patterns.md` |
| AsyncImage, #Preview, ContentUnavailableView | `references/patterns.md` |

---

## Common Anti-Patterns to Avoid

1. **Using `@StateObject` with `@Observable`** — `@StateObject` is for `ObservableObject` only. Use `@State` with `@Observable`.

2. **Using `@ObservedObject` with `@Observable`** — just pass the object directly; observation is automatic.

3. **Nesting `NavigationStack`** inside another `NavigationStack` — causes double nav bars and broken navigation.

4. **Using `NavigationView`** — deprecated since iOS 16. Use `NavigationStack` or `NavigationSplitView`.

5. **Heavy work in `body`** — `body` is called frequently. Move computation to `.task`, `.onAppear`, or the model.

6. **Using `AnyView`** — type-erases the view, preventing SwiftUI from diffing efficiently. Use `@ViewBuilder` or `Group`.

7. **Using `GeometryReader` for simple layouts** — it proposes all available space to its child. Use proper stack alignment, `.frame()`, or `containerRelativeFrame` instead.

8. **Forgetting `.id()` on ForEach items** — causes incorrect diffing, wrong animations, and state bugs. Always use `Identifiable` or explicit `id:`.

9. **Using `.onAppear` for async work** — use `.task` instead; it auto-cancels when the view disappears.

10. **Creating `@State` from init parameters** — `@State` initializes once. If you need to react to parameter changes, use `.onChange(of:)` or derive state differently.

---

## iOS Version Feature Matrix

| Feature | Minimum iOS |
|---|---|
| `@Observable`, `@Bindable` | 17 |
| `NavigationStack`, `NavigationSplitView` | 16 |
| `Grid`, `GridRow` | 16 |
| `ViewThatFits` | 16 |
| `PhaseAnimator`, `KeyframeAnimator` | 17 |
| `sensoryFeedback` | 17 |
| `SymbolEffect` | 17 |
| `ContentUnavailableView` | 17 |
| `#Preview` macro | 17 |
| `containerRelativeFrame` | 17 |
| `scrollPosition`, `scrollTargetBehavior` | 17 |
| `withAnimation` completion | 17 |
| `navigationDestination(item:)` | 17 |
| `Tab` type in `TabView` | 18 |
| `@Entry` macro for Environment | 18 |
| `.presentationSizing` | 18 |
| `MeshGradient` | 18 |

---

## Project Structure Convention

```
MyApp/
├── MyAppApp.swift          // @main App struct
├── Models/                 // Data models, @Observable classes
├── Views/
│   ├── Components/         // Reusable small views
│   ├── Screens/            // Full-screen views
│   └── Modifiers/          // Custom ViewModifiers
├── Services/               // Network, persistence, etc.
├── Extensions/             // View+, Color+, etc.
└── Resources/              // Assets, Localizable
```

## Naming Conventions

- Views: noun or noun phrase (`ProfileView`, `SettingsScreen`, `UserRow`)
- ViewModels: `<Feature>ViewModel` with `@Observable`
- Modifiers: adjective or style name (`CardModifier`, `PrimaryButtonStyle`)
- Use `some View` return type, never concrete view types in public API
