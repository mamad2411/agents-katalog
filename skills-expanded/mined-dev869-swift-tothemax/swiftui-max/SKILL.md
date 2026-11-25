---
name: swiftui-max
description: Expert SwiftUI guidance for building UI on iOS, iPadOS, macOS, watchOS, tvOS, and visionOS. Use whenever writing, reviewing, refactoring, or debugging ANY SwiftUI code — views, view modifiers, layout, navigation (NavigationStack/SplitView, deep links), lists and scrolling, animation and transitions, state management (@State, @Binding, @Observable, Observation, environment), Liquid Glass adoption, toolbars, sheets and presentations, widgets/Live Activities, UIKit/AppKit interop, or SwiftUI performance problems (slow lists, hitches, excessive view updates). ALSO use it when building common UI components (bottom sheets, tab bars, onboarding, infinite scroll, skeletons, charts, forms, toasts), choosing or adding UI libraries (Pow, Lottie, Nuke, Kingfisher, snapshot testing, Inject hot reload, TCA), building a design system (tokens, themes, component packages), or iterating visually (simulator screenshots, previews, snapshot tests). Trigger on mentions of SwiftUI, "build a screen/view", "make it look good", @Observable, ObservableObject migration, NavigationView, glassEffect, WidgetKit, or any *View struct with a body. For pure Swift language/concurrency questions, the sibling swift-language skill applies instead.
---

# SwiftUI to the Max

Write SwiftUI the way a senior Apple-platforms engineer writes it in mid-2026: Observation-first, value-typed, identity-aware, and Liquid Glass-native. Prefer deleting code to adding it; most SwiftUI bugs are self-inflicted state or identity problems.

**Scope split**: This skill owns UI. Swift language, strict concurrency, actors/Sendable, macros, SwiftPM, and Swift Testing belong to the sibling **swift-language** skill — route there instead of answering language questions here (e.g. "is this Sendable", Swift 6 migration, `@concurrent`). SwiftUI code that *contains* concurrency needs both.

## Give yourself eyes (mandatory for UI work)

UI built blind is the single biggest quality gap in agent-written SwiftUI. Never declare UI work done without having rendered and *looked at* it. The loop:

1. Build for the simulator (`xcodebuild -scheme App -destination 'platform=iOS Simulator,name=iPhone 17' build`) or, for isolated components, render with `ImageRenderer` from a scratch target.
2. Screenshot: `xcrun simctl io booted screenshot /tmp/screen.png` — then **read the image** and critique it against `apple-hig-ux` standards (spacing, hierarchy, Dynamic Type, dark mode).
3. Repeat across the matrix that matters: light/dark, small/large Dynamic Type, smallest + largest supported device.
4. Lock in what's right with snapshot tests so regressions are caught without eyes.

Full workflow (simulator CLI, PreviewHost pattern, hot reload with Inject, snapshot testing, accessibility audits): `references/visual-iteration-workflow.md`.

## Build vs. recipe vs. library

Before hand-rolling any common component, check `references/component-recipes.md` (canonical implementations of the 12 hardest-to-get-right components) and `references/ecosystem-libraries.md` (curated, maintenance-verified third-party catalog: effects, images, markdown, dev tooling, architecture). Default order: native API → recipe from this skill → library from the vetted list. Never re-implement what Pow/Nuke/Lottie already do well; never import a library for what native does in 20 lines. For app-wide consistency (tokens, themes, reusable components), follow `references/design-system-kit.md` and consume tokens instead of magic numbers.

## Version landscape (July 2026)

| Release | Status | Headline UI features |
|---|---|---|
| iOS 17 / macOS 14 | old floor | Observation (`@Observable`), `@Entry`-era environment patterns, scrollTargetBehavior/scrollPosition, keyframe/phase animators, `#Preview` |
| iOS 18 / macOS 15 | common floor | `@Entry` macro, zoom navigation transitions, scroll geometry/visibility callbacks, mesh gradients, floating tab bar/`TabSection` |
| iOS 26 / macOS 26 "Tahoe" | **current shipping** (unified "26" version number across platforms) | **Liquid Glass** design system (`glassEffect`, `GlassEffectContainer`), `@Animatable` macro, rich-text `TextEditor` (AttributedString), `WebView`, scroll edge effects, `tabBarMinimizeBehavior`, Instruments SwiftUI template |
| iOS 27 / macOS 27 "Golden Gate" (WWDC26) | **beta** — mark all usage as beta | `@State` becomes a macro (lazy class init), reorderable containers, `swipeActions` in any ScrollView, `ToolbarOverflowMenu`/`visibilityPriority`, `WritableDocument`/`ReadableDocument`, `AsyncImage` HTTP caching, `ContentBuilder` (build-time wins), item-binding `alert`/`confirmationDialog`, resizable iPhone apps |

Gate anything above the deployment target with `#available` and provide a real fallback, not a blank view.

## Modern defaults (non-negotiable unless the target forces otherwise)

1. **Observation over Combine-era state.** New model types are `@Observable` classes (or plain structs held in `@State`). `ObservableObject`/`@Published`/`@StateObject` are legacy — use only below iOS 17. Why: Observation tracks per-property reads, so views update only when a property they actually read changes.
2. **`NavigationStack` / `NavigationSplitView`, never `NavigationView`.** Drive navigation with a `path` value (`NavigationPath` or a typed array) so deep links and state restoration are data, not view spelunking.
3. **`@Entry` for environment keys.** One line replaces the `EnvironmentKey` + extension boilerplate:
   ```swift
   extension EnvironmentValues {
       @Entry var audioMixer = AudioMixer()   // iOS 18+; hand-rolled key below that
   }
   ```
4. **Composition over `AnyView`.** Return `some View`, split subviews, use `@ViewBuilder` properties/functions and generics. `AnyView` erases identity and blocks diffing — reach for it only at true dynamic boundaries (e.g. heterogeneous routing tables).
5. **Stable identity.** `ForEach` over `Identifiable` data with ids that survive edits (never `id: \.self` on mutable strings, never array indices for reorderable data). Remember: `if/else` creates *different* identities (transition + state reset); modifying one view (`opacity`, `disabled`) preserves identity.
6. **Value flows down, actions flow up.** Pass the smallest thing that works: `let` for display, `@Binding` for mutation, closures for events. Don't pass a whole store into a leaf view that reads one field.
7. **`body` is pure.** No side effects, no object allocation per evaluation, no `DateFormatter()` inline, no sorting/filtering big arrays. Compute in the model, or memoize; kick effects off with `.task`/`.onChange`.
8. **Semantic styling.** System colors/materials, `Font.TextStyle` (Dynamic Type), `foregroundStyle` over `foregroundColor`, button/label/list *styles* over hand-built lookalikes. Accessibility is part of "done": labels on image-only buttons, `accessibilityElement(children: .combine)` for composite rows.

## Legacy → modern translation table

| Legacy (flag on sight) | Modern replacement | Since |
|---|---|---|
| `NavigationView` | `NavigationStack(path:)` / `NavigationSplitView` | iOS 16 |
| `NavigationLink(destination:)` (eager) | `NavigationLink(value:)` + `navigationDestination(for:)` | iOS 16 |
| `ObservableObject` + `@Published` | `@Observable` class | iOS 17 |
| `@StateObject` / `@ObservedObject` | `@State` (owner) / plain `let` (non-owner) | iOS 17 |
| `@EnvironmentObject` | `@Environment(MyModel.self)` + `.environment(model)` | iOS 17 |
| `EnvironmentKey` struct + extension | `@Entry` | iOS 18 |
| `foregroundColor` | `foregroundStyle` | iOS 15 |
| `.animation(.spring)` (no value) | `.animation(.spring, value: x)` or `withAnimation` | iOS 15 |
| `onChange(of:) { newValue in }` (1-param) | `onChange(of:) { old, new in }` / zero-param | iOS 17 |
| `DispatchQueue.main.async` / `onAppear` for async work | `.task { }` / `.task(id:)` (auto-cancelling) | iOS 15 |
| `UIScreen.main.bounds` sizing | `GeometryReader` (sparingly) / `containerRelativeFrame` | iOS 17 |
| `AnimatableModifier` / manual `animatableData` | `@Animatable` macro | iOS 26 |
| Hand-built blur "glass" (`.ultraThinMaterial` chrome) | `glassEffect` + `GlassEffectContainer` | iOS 26 |
| `cornerRadius(_:)` | `clipShape(.rect(cornerRadius:))` / concentric shapes | iOS 16/26 |
| `MasterDetailView`-style bool spaghetti for alerts | `alert(item:)` / `confirmationDialog(item:)` | iOS 27 beta (sheet-style item binding) |
| `@State private var model = BigModel()` eager init | unchanged code, now lazy — but drop default values when assigning in `init` | iOS 27 beta (`@State` macro) |

`FetchRequest`/Core Data ↔ SwiftData `@Query`: see references/state-and-data-flow.md.

## Performance rules of thumb

- **Measure before rewriting**: Instruments 26 → SwiftUI template ("Long View Body Updates" lane), or `Self._printChanges()` in body while reproducing. Guessing wastes time; the tooling names the guilty view.
- Keep bodies cheap and small — extraction into child views is free and *narrows invalidation scope*.
- Big value types diff slowly; conform hot views to `Equatable` (or restructure so inputs are small) to skip subtree updates.
- `LazyVStack`/`LazyHStack`/`List` for anything unbounded; but lazy containers never *release* built views — keep row views trivial. Stable, cheap `id`s; no per-row `GeometryReader`.
- `.task(id:)` over `.onChange` + manual `Task` — you get cancellation of the stale work for free.
- Animate leaf modifiers, not layout of giant hierarchies; prefer `scrollTargetBehavior`/`scrollTransition` to hand-rolled offset math.
- Full playbook: references/performance-and-debugging.md.

## Liquid Glass (iOS 26+; refined in 27 beta)

Adopting the system design is mostly free: rebuild with Xcode 26+ and standard bars, tabs, sheets, and controls pick up Liquid Glass automatically. On the 2027-era OSes (beta), glass tint additionally follows the user's system-level Liquid Glass appearance slider with no code changes. Rules for custom surfaces:

```swift
// One floating control
Image(systemName: "plus")
    .frame(width: 52, height: 52)
    .glassEffect(.regular.interactive(), in: .circle)

// Multiple glass shapes that sit near each other MUST share a container,
// so they blend/morph instead of stacking blur on blur.
GlassEffectContainer(spacing: 24) {
    ForEach(tools) { tool in
        ToolIcon(tool)
            .glassEffect()
            .glassEffectID(tool.id, in: namespace)   // enables morph transitions
    }
}
```

- `glassEffect(_:in:)` with `.regular` / `.clear`, `.tint(_:)`, `.interactive()`; `buttonStyle(.glass)` and `.glassProminent` for buttons.
- Glass is **chrome, not content**: use it for the floating control layer above scrolling content, never for list rows or whole backgrounds. One glass layer — don't nest.
- Let content flow under bars: `backgroundExtensionEffect()` for hero images, `scrollEdgeEffectStyle(_:for:)` to manage edge legibility, `tabBarMinimizeBehavior(.onScrollDown)` on TabView.
- Custom-styled controls: audit tinted/rounded hand-rolled buttons — replace with glass button styles rather than approximating.
- Escape hatch while migrating: `UIDesignRequiresCompatibility` Info.plist key (temporary; Apple has said it is going away — treat as tech debt).
- iOS 27 beta refinements: respect the `appearsActive` environment value for glass emphasis; toolbar items get `visibilityPriority`, `ToolbarOverflowMenu`, and pinned-trailing placement — see references/platform-integration.md and layout ref.

## Routing table

| Question smells like… | Go to |
|---|---|
| @Observable vs @State vs @Binding, environment DI, ObservableObject migration, SwiftData in views | `references/state-and-data-flow.md` |
| Custom layout, Grid, ViewThatFits, adaptive UI, transitions, matchedGeometry, phase/keyframe animation, scroll APIs, reordering | `references/layout-and-animation.md` |
| Slow lists, hitches, spinning bodies, Instruments traces, identity bugs, "why did this view update" | `references/performance-and-debugging.md` |
| UIKit/AppKit interop, hosting, representables, widgets, Live Activities, App Intents, multiplatform targets | `references/platform-integration.md` |
| Building a specific component: bottom sheet, custom tab bar, parallax header, infinite scroll, skeleton, search, forms, image grids, onboarding, charts, toasts, list state machines | `references/component-recipes.md` |
| Should I use a library? Which one? Pow, Lottie, Nuke vs Kingfisher, markdown, TCA vs vanilla, snapshot testing, hot reload, DI | `references/ecosystem-libraries.md` |
| Design tokens, theming, custom fonts with Dynamic Type, reusable component package, brand consistency, style protocols | `references/design-system-kit.md` |
| Rendering/screenshotting what I built, simulator CLI, previews at scale, snapshot tests, hot reload setup, visual QA matrix | `references/visual-iteration-workflow.md` |
| async/await, actors, Sendable, MainActor isolation, Swift 6 errors, testing | sibling skill **swift-language** |

When reviewing code: run the translation table first (deprecated API sweep), then identity/state checks, then performance only if there's a reported symptom.

## Companions & orchestration

Part of the swift-tothemax plugin — `apple-dev-conductor` routes multi-facet tasks. Siblings: `swift-language` owns concurrency/data/performance below the view layer (route non-UI Swift there); `apple-hig-ux` owns design judgment — consult it BEFORE building a screen, not after.
Ecosystem companions (delegate if installed): `swiftui-expert-skill` / `swiftui-pro` for deep SwiftUI code review; `swiftui-performance-audit` for hitch investigations with Instruments. Prefer their workflows for those sub-tasks; keep this skill's WWDC26-current API facts when they disagree on versions.
After substantial UI work, run a `ui-crawler-max` sweep (sibling skill) to exercise every screen and harvest errors, crashes, and unlabeled controls — then fix its findings here.
