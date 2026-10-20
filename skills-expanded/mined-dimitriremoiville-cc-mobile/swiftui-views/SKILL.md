---
name: swiftui-views
description: Project-specific SwiftUI conventions — the RootView/View split, the `ViewState` shape, the `@Observable @MainActor` view-model contract, Figma-MCP-to-asset-catalog token translation, and the hard nos this project enforces. Load whenever writing or editing any `View` or view model in this codebase. Navigation destinations and route plumbing live in `navigation-stack` — load that one for any nav-graph or deep-link work.
---

# SwiftUI views (project delta)

For SwiftUI fundamentals — property wrappers, layout, `ViewBuilder`, `#Preview` mechanics, list performance, animation — read [Apple's SwiftUI documentation](https://developer.apple.com/documentation/swiftui) and the [Observation framework guide](https://developer.apple.com/documentation/observation). This file documents only where this project's conventions add to or override those defaults.

## When this applies

SwiftUI with the Observation framework (iOS 17+). On an existing app:

- **UIKit** (`UIViewController`, `.storyboard`, `.xib`, `UITableViewDataSource`) → don't push SwiftUI patterns. The RootView split, `@Observable`, and `#Preview` rules are SwiftUI-only.
- **Mixed UIKit + SwiftUI** (`UIHostingController`, `UIViewRepresentable`) → apply this skill to the SwiftUI half; let the UIKit half follow its own conventions.
- **`ObservableObject` + `@Published` codebase** (pre-Observation, or an iOS 16 deployment floor) → the "no `ObservableObject`" rule is for *new* code in an `@Observable` codebase. Don't propose a migration as a side effect of an unrelated change.
- **TCA** (`@Reducer`, `Store`, `WithViewStore`) → skip this skill entirely; TCA owns the view/state contract.

## Pulling design specs from Figma

The plugin declares Figma's official MCP server (`.mcp.json` → `figma`, `https://mcp.figma.com/mcp`, OAuth — no API key in the plugin). If the user supplies a Figma URL when asking for a screen or component, pull layout / typography / colour / spacing from the file before generating SwiftUI code. The first call triggers a browser OAuth prompt; nothing to configure beyond that.

**Translate the tokens; don't paste the values.** A Figma frame gives you fixed hex and pt numbers, and pasting them produces a screen that ignores dark mode and stops laying out at large Dynamic Type sizes:

- **Colour** → a named colour in the asset catalog (with a dark appearance), referenced as `Color("Surface")`, or a semantic system colour (`.primary`, `.secondary`). Never a `Color(hex:)` literal in a view body.
- **Type** → the nearest semantic text style (`.body`, `.headline`, `.caption`). If the design's scale genuinely differs, define it once with `Font.custom(_:size:relativeTo:)` so it still scales — a bare `.system(size:)` does not.
- **Spacing** → the project's spacing constants, or plain `padding` values. Don't reproduce a Figma auto-layout gap to the half-point.

Where the design and the platform disagree — a 32pt tap target, a fixed-height row holding scalable text, colour-only status — follow the platform and say so in your summary. See `ios-accessibility`.

## RootView + View split (project rule)

Every screen is **two views**: a stateful `<Feature>RootView` that owns the `@Observable` view model and knows about the world, and a stateless `<Feature>View` that takes values plus closures.

```swift
// ProfileRootView.swift — stateful container
struct ProfileRootView: View {
    @State private var model: ProfileViewModel
    let onSelectPost: (PostID) -> Void

    init(userID: UserID, container: CompositionRoot, onSelectPost: @escaping (PostID) -> Void) {
        _model = State(initialValue: container.makeProfileViewModel(userID: userID))
        self.onSelectPost = onSelectPost
    }

    var body: some View {
        ProfileView(
            state: model.state,
            onRefresh: { Task { await model.refresh() } },
            onSelectPost: onSelectPost
        )
        .task { await model.load() }
    }
}

// ProfileView.swift — pure UI, fully previewable, no container reference
struct ProfileView: View {
    let state: ProfileViewState
    let onRefresh: () -> Void
    let onSelectPost: (PostID) -> Void

    var body: some View { /* switch over state */ }
}
```

The stateless half is what `#Preview` and UI tests drive — no composition root, no network, no `@Observable` setup. The Root's job is wiring; the View's job is rendering.

**Never pass the view model itself into the presentation view.** Pass `model.state` and closures. A `View` that reads `model.something` in its body has erased the split.

## ViewState shape

An **enum** when the screen has distinct states — the default:

```swift
enum ProfileViewState: Equatable {
    case loading
    case loaded(Profile)
    case error(DomainError)
}
```

A **struct** when the screen is always populated and you need independent fields (forms, composers):

```swift
struct ComposeViewState: Equatable {
    var text: String = ""
    var isSending: Bool = false
    var errorMessage: String?
}
```

One-off effects — navigation, toasts, haptics — are **not** state. Surface them as a `ViewEvent` the Root consumes once, or as a closure the Root supplies.

## View model contract

```swift
@Observable @MainActor
final class ProfileViewModel {
    private(set) var state: ProfileViewState = .loading
    private let getProfile: GetProfileUseCase

    init(getProfile: GetProfileUseCase) { self.getProfile = getProfile }

    func load() async { /* ... */ }
    func refresh() async { await load() }
}
```

Non-negotiable in this codebase:

- `@Observable` + `@MainActor` + `final class`. All three.
- `private(set)` on every mutable property — the view reads, the model writes.
- Constructor injection, collaborators typed as protocols. Never the whole `CompositionRoot` (see `ios-di`).
- User actions are **discrete `async` methods** (`load()`, `refresh()`, `submit()`), and the View takes one closure per action. Escalate to a single `send(_ action:)` only when a screen has ≥5 distinct interactions — that's an MVI shape, and this project is MVVM by default.

## Previews

Every non-trivial view has previews for its **distinct states**, not just the happy one — the loading and error branches are the ones that rot:

```swift
#Preview("Loaded") { ProfileView(state: .loaded(.sample), onRefresh: {}, onSelectPost: { _ in }) }
#Preview("Error")  { ProfileView(state: .error(.notFound), onRefresh: {}, onSelectPost: { _ in }) }
```

Sample data only. A `#Preview` that needs real IO is a broken preview.

## Accessibility

The full checklist lives in `ios-accessibility`. The minimum the reviewer flags here: every non-decorative `Image` / custom control has an `accessibilityLabel`, decorative ones are `.accessibilityHidden(true)`, tap targets are ≥ 44×44pt, and text uses semantic styles (`.body`, `.headline`) rather than fixed sizes.

## Hard nos

- **No `ObservableObject` / `@Published` / `@StateObject`** in new code — `@Observable` + `@State`.
- **No `DispatchQueue.main.async`** — isolate the function `@MainActor`.
- **No network or database call in a `body` or in `onAppear`.** `.task { }` calling a view-model method, always.
- **No view model constructed inside a stateless view.** Only a `RootView` builds one, and only from the composition root.
- **No `#Preview` that requires real IO.**
- **No `AnyView`** without a written reason — it erases the type information the diffing engine needs.
- **No colour or font literals in a view body.** Asset-catalog colours and semantic text styles, always — see the Figma section above.
- **No `body` longer than ~40 lines.** Extract a subview when concerns mix or nesting passes three levels; readability is the rule, the line count is the smell.
