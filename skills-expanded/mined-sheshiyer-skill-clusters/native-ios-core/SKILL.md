---
name: native-ios-core
description: "Shared reference for the native-iOS cluster: the iOS 26 / Swift 6.2 / Xcode 26 baseline, availability-gating discipline for the new frameworks, the data-race-safety (actor isolation + Sendable) model, and shared SwiftUI conventions. USE WHEN adopting Swift 6.2 concurrency, gating an iOS 26-only API, or choosing a state/persistence pattern — the rules every native-iOS spoke shares."
cluster: native-ios
version: 1.0.0
---

# Native iOS Core

Shared model for the `native-ios` cluster. The concurrency, SwiftUI, persistence, AI, and design
spokes all depend on the same baseline and the same safety rules — keep them consistent here so no
spoke contradicts another.

## 1. The baseline (this cluster's defining decision)

Everything is written for **one toolchain line**:

```
Xcode 26 ──compiles──> Swift 6.2 ──targets──> iOS 26 / macOS 26 (with graceful fallback below)
```

The flagship capabilities the cluster exists to teach — **Approachable Concurrency**, **Liquid
Glass**, and **on-device FoundationModels** — only exist on this line. So the first question for
any task is *"what's the deployment target, and is this API available there?"* — not *"how do I
call it?"*. Get the baseline right and the spokes compose; get it wrong and they conflict.

## 2. Availability gating (non-negotiable)

A higher SDK does **not** mean every device can run the API. Gate, don't assume:

- **Compile-time / OS gate** — wrap iOS 26-only UI (Liquid Glass, newest SwiftUI) in `if #available(iOS 26, *)` with a real pre-26 branch. → `liquid-glass-design`
- **Runtime capability gate** — on-device AI is gated by hardware + user settings, not just OS. Always switch on `SystemLanguageModel.default.availability` (`.available` / `.unavailable(...)`) before opening a session. → `foundation-models-on-device`

**Rule:** never raise the whole app's minimum deployment target just to use one new affordance — gate the affordance and keep a fallback.

## 3. Data-race safety model (Swift 6.2)

Concurrency is **isolated-by-default**; you opt *into* parallelism, not out of it.

- Async code **stays on the calling actor** by default (no implicit background hop). Offload explicitly with `@concurrent`. → `swift-concurrency-6-2`
- **MainActor** is the default isolation for UI types; non-isolated protocols are satisfied via **isolated conformances**.
- Cross-isolation values must be **`Sendable`**; the compiler enforces it.
- **Actors** serialize access to shared mutable state — use them for persistence/caches instead of locks or `DispatchQueue`. → `swift-actor-persistence`
- Abstract I/O (file system, network, iCloud) behind small **`Sendable` protocols** so it's mockable and the isolation stays clean. → `swift-protocol-di-testing`

## 4. Shared SwiftUI & architecture conventions

- State: **`@Observable`** (Observation framework) over `ObservableObject`/`@Published` — property-level change tracking, fewer re-renders. → `swiftui-patterns`
- Pick the **narrowest** property wrapper that fits (`@State` → `@Binding` → `@Bindable` → `@Environment`).
- Inject dependencies via protocols (not concretes) so views are previewable and testable. → `swift-protocol-di-testing`
- Structured AI output uses **`@Generable`** types, not hand-parsed strings. → `foundation-models-on-device`
- Icons ship as **asset-catalog imagesets** (1x/2x/3x), generated to match existing project style. → `ios-icon-gen`

## 5. Version / tooling matrix

| Concern | Target | Spoke | Notes |
|---|---|---|---|
| Toolchain | Xcode 26 | (all) | required for Swift 6.2 + iOS 26 SDK |
| Language / concurrency | Swift 6.2 | `swift-concurrency-6-2` | Approachable Concurrency build setting on |
| UI framework | SwiftUI (Observation) | `swiftui-patterns` | `@Observable`, `NavigationStack` |
| Persistence | Swift 5.5+ actors | `swift-actor-persistence` | works back to 5.5; written for 6.2 isolation |
| Testing | Swift Testing | `swift-protocol-di-testing` | `@Test`/`#expect`, protocol mocks |
| On-device AI | iOS 26+ FoundationModels | `foundation-models-on-device` | availability-gated, hardware-dependent |
| Design system | iOS 26+ Liquid Glass | `liquid-glass-design` | SwiftUI / UIKit / WidgetKit |
| Assets | Xcode asset catalog | `ios-icon-gen` | SF Symbols (macOS) or Iconify (network) |

## 6. Shared guardrails

- **Baseline first**: confirm deployment target before reaching for an iOS 26 API.
- **Gate every new API**: `if #available` for OS features, `.availability` for on-device AI — always with a fallback.
- **Don't widen the deployment target silently** to use one affordance.
- **Isolated-by-default**: keep data-race safety; offload with `@concurrent`, share via `Sendable`, serialize state with actors — never ad-hoc background dispatch.
- **`@Observable` over `ObservableObject`**; narrowest property wrapper that works.
- **Protocol-seam I/O**: external dependencies behind `Sendable` protocols so tests stay deterministic.
- Native Swift vs cross-platform: pick this cluster for the newest first-party frameworks (Liquid Glass, on-device AI) and full platform fidelity; if the app must also ship Android/web from one codebase, weigh a cross-platform stack instead.
