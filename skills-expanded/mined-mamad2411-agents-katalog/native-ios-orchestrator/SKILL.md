---
name: native-ios-orchestrator
description: "Route a native Apple-platform task to the right skill among the iOS specialists — Swift 6.2 concurrency, SwiftUI architecture, actor persistence, protocol-based DI/testing, on-device FoundationModels, Liquid Glass design, and icon assets. USE WHEN a user is building, modernizing, or shipping a native iOS/macOS app in Swift but hasn't named the specific concern."
cluster: native-ios
version: 1.0.0
---

# Native iOS Orchestrator

The single entry skill for native Apple-platform (Swift / SwiftUI) work. It locates the task on
the **layer × concern** map and delegates to one of 7 specialist spokes. The cross-cutting fact
every spoke shares — the **iOS 26 / Swift 6.2 / Xcode 26 baseline**, its availability-gating
discipline, and the data-race-safety model — lives in `native-ios-core`; read it before adopting
the new concurrency mode or any of the iOS 26 frameworks.

## Cluster map (spoke → role)

- `swift-concurrency-6-2` — the **language model**: Swift 6.2 Approachable Concurrency, single-threaded by default, `@concurrent` for explicit offloading, isolated conformances.
- `swiftui-patterns` — the **UI architecture**: `@Observable` state, view composition, `NavigationStack`, list/render performance.
- `swift-actor-persistence` — the **storage layer**: actor-backed in-memory cache + file persistence, data races eliminated by the compiler.
- `swift-protocol-di-testing` — the **testability seam**: small focused protocols for file system / network / external APIs, mocked under Swift Testing.
- `foundation-models-on-device` — the **on-device AI**: Apple FoundationModels LLM, `@Generable` guided generation, tool calling, snapshot streaming.
- `liquid-glass-design` — the **design system**: iOS 26 Liquid Glass material for SwiftUI, UIKit, WidgetKit.
- `ios-icon-gen` — the **asset pipeline**: PNG icon imagesets for Xcode asset catalogs from SF Symbols or Iconify.

See also **## Folded spokes** below for the watchOS and HIG-design spokes.

## Routing rules by intent

**Set the foundation**
- "Data races / async errors / migrate to Swift 6.2 / MainActor architecture" → `swift-concurrency-6-2`  *(baseline in `native-ios-core`)*
- "How do I structure views / state / navigation?" → `swiftui-patterns`

**Build the app body**
- Local/offline storage, caching, thread-safe shared state → `swift-actor-persistence`
- Make it testable, mock I/O, deterministic tests → `swift-protocol-di-testing`
- On-device text generation, structured extraction, AI tool calls → `foundation-models-on-device`

**Make it look native**
- Glass buttons/cards/toolbars, morphing, iOS 26 material → `liquid-glass-design`
- HIG-conformant UI, SF Symbols, Dynamic Type, adaptive iPhone/iPad layout, Dark Mode, accessibility → `mobile-ios-design`
- App/feature icons, asset-catalog imagesets → `ios-icon-gen`

**Ship to the wrist**
- watchOS app/extension, Watch Connectivity sync, complications, watch workouts/HealthKit, Smart Stack widgets → `watchos`

**Fix / audit / refactor / ship (picked-up workflow spokes)**
- A specific Swift 6.2 data-race / `Sendable` / actor-isolation *compiler diagnostic* to fix → `swift-concurrency-expert`
- Concrete navigation / sheet / async-`.task` / deep-link / reusable-screen pattern → `swiftui-ui-patterns`
- An existing SwiftUI view is too large / mixes logic with layout / needs splitting → `swiftui-view-refactor`
- Janky scrolling, dropped frames, high CPU, hangs, excessive view updates → `swiftui-performance-audit`
- Review/implement Liquid Glass against a checklist (availability, modifier order, containers) → `swiftui-liquid-glass`
- Run/inspect/debug the app on a booted simulator, capture logs, drive UI → `ios-debugger-agent`
- Generate App Store "What's New" / release notes from git history → `app-store-changelog`
- macOS menu-bar (LSUIElement) app built with Tuist → `macos-menubar-tuist-app`
- Build/sign/notarize/package a SwiftPM macOS app into a `.app` (no Xcode project) → `macos-spm-app-packaging`

## Folded spokes

These spokes were folded into this cluster from overlapping standalone skills. They share the
`native-ios` baseline (`native-ios-core`) and the SwiftUI architecture in `swiftui-patterns`; route
to them like any other spoke above.

- `mobile-ios-design` — the **HIG layer**: Apple Human Interface Guidelines made concrete in SwiftUI — layout/grids, navigation patterns, SF Symbols, Dynamic Type, semantic color/materials, and iPhone/iPad adaptivity. Pairs with `swiftui-patterns` (architecture) and `liquid-glass-design` (iOS 26 material).
- `watchos` — the **wrist platform**: watchOS apps and Watch extensions — Watch Connectivity (iPhone <-> Watch sync), complications (ClockKit and WidgetKit), HealthKit workout sessions, and Smart Stack widgets. Reuses the cluster's concurrency and SwiftUI conventions on the watch form factor.

## Picked-up spokes

These spokes were picked up from the **antigravity-awesome-skills** library (upstream: Dimillian/Skills,
MIT). They are **task/workflow** spokes — review, fix, refactor, audit, debug, package, ship — that sit on
top of the architecture spokes above (`swift-concurrency-6-2`, `swiftui-patterns`, `liquid-glass-design`).
Where two spokes overlap, the rule is **architecture spoke = how to design it; picked-up spoke = how to
fix/audit/ship it**. Route to them on demand like any other spoke.

- `swift-concurrency-expert` — the **concurrency fix workflow**: triage a concrete Swift 6.2 data-race / `Sendable` / actor-isolation *diagnostic* and apply the smallest behavior-preserving edit, then verify. Pairs with `swift-concurrency-6-2` (which is the language *model*; this one fixes specific compiler errors).
- `swiftui-ui-patterns` — the **pattern catalog**: NavigationStack routing, enum-driven sheets, `.task` async state, deep links, previews, reusable screens, with a component-reference index. Pairs with `swiftui-patterns` (architecture) as the concrete how-to layer.
- `swiftui-view-refactor` — the **refactor workflow**: split oversized views into small dedicated subview types, MV-first data flow, stable view trees, side effects out of `body`. Use after `swiftui-patterns`/`swiftui-ui-patterns` when an existing view has grown too large.
- `swiftui-performance-audit` — the **performance diagnostic**: code-first audit of invalidation storms, unstable `ForEach` identity, layout thrash, and main-thread image decode, escalating to Instruments profiling. Route here for janky scrolling, dropped frames, hangs, or excessive view updates.
- `swiftui-liquid-glass` — the **Liquid Glass audit/impl**: correct `glassEffect` / `GlassEffectContainer` / glass button-style usage, modifier order, `#available(iOS 26)` gating, and morphing. Overlaps `liquid-glass-design`; prefer this one for review/checklist-driven adoption.
- `ios-debugger-agent` — the **simulator debug loop**: build/run/inspect the current app on a booted simulator via XcodeBuildMCP — UI taps, screenshots, view inspection, runtime log capture. Route here to reproduce a bug or drive a flow at runtime.
- `app-store-changelog` — the **release-notes generator**: turn git history since the last tag into user-facing App Store "What's New" bullets (New/Improved/Fixed), dropping internal-only commits. The ship-time spoke.
- `macos-menubar-tuist-app` — the **macOS menubar (Tuist) workflow**: `LSUIElement` menu-bar utilities with a Tuist-first manifest/run-script flow and strict model/client/store/view boundaries. The macOS sibling of the iOS architecture spokes.
- `macos-spm-app-packaging` — the **macOS packaging/release pipeline**: scaffold, build, codesign, notarize, staple, and package a SwiftPM macOS app into a `.app` (plus Sparkle appcast) with no Xcode project. The macOS ship-time spoke.

## Standard flow

1. Locate the task: which layer (language → architecture → storage/test/AI → design → assets) and which concern.
2. If it touches **concurrency isolation, `Sendable`, availability gating, or any iOS 26-only API**, pull the baseline from `native-ios-core` first — these interlock across spokes (a `@MainActor` decision in concurrency changes how SwiftUI, actors, and DI are written).
3. Delegate to the spoke(s). Multi-step asks fan out in layer order (e.g. "build an AI feature with a glass UI" → `swift-concurrency-6-2` isolation → `foundation-models-on-device` → `liquid-glass-design`).
4. Return: chosen spoke(s), the deployment-target / availability implications, and the next action.

## Guardrails

See `native-ios-core`. In short: target **Swift 6.2 + Xcode 26**, and treat every iOS 26-only API
(Liquid Glass, FoundationModels, the newest SwiftUI affordances) as **availability-gated** — wrap
it in `if #available` / `SystemLanguageModel.availability` with a real fallback rather than raising
the whole app's deployment target silently. Prefer `@Observable` over `ObservableObject`, actors
over manual locks, and isolated-by-default concurrency over ad-hoc background dispatch. Don't widen
a deployment target or weaken data-race safety without saying so explicitly.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
