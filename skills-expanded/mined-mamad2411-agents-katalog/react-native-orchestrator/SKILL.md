---
name: react-native-orchestrator
description: "Route a React Native craft task to the right spoke — styling/navigation/Reanimated animation, touch/gesture/haptics, data fetching, full screen/app visual design, or integrated product-flow UI/UX audits. USE WHEN building or reviewing React Native UI and interaction (toolchain-agnostic). For the Expo toolchain (EAS, dev client, Expo Router, native modules) hand off to the expo cluster; for native SwiftUI/iOS, the native-ios cluster."
cluster: react-native
version: 1.0.1
---

# React Native Orchestrator

Entry skill for **React Native UI and interaction craft** — independent of how the app is
built or shipped. It routes by what you're crafting (layout, motion, touch, data, screens)
or reviewing (whole-product UI/UX flow, source-of-truth gaps, route/state/API continuity).
The runtime model (New Architecture, Reanimated, navigation, performance) lives in
`react-native-core`. Toolchain/build/ship belongs to the **expo** cluster.

## Cluster map (routing targets)

- `react-native-core` — RN runtime model: New Architecture (Fabric/TurboModules/JSI), styling approaches, navigation options, the Reanimated + Gesture Handler stack, platform differences, performance, and integrated product-flow audits.
- `react-native-design` — styling, navigation, and **Reanimated** animations; the day-to-day RN UI craft.
- `mobile-touch` — gestures, haptic feedback, touch interactions, native-feel micro-animations.
- `sleek-design-mobile-apps` — high-level screen/app **design** ("design a mobile app", build screens) incl. Sleek projects.
- `native-data-fetching` — *(shared with expo)* network requests, React Query/SWR, caching, offline, error handling.

## Routing Rules by Intent

- **Styling / layout / navigation / animation** → `react-native-design` (+ `react-native-core` for the Reanimated/nav model).
- **Gestures, haptics, touch feel** → `mobile-touch`.
- **Design a screen / whole app visually** → `sleek-design-mobile-apps`.
- **Whole-product / integrated UI/UX flow audit** → `react-native-core` integrated-flow reference + `react-native-design`; add `native-data-fetching` for API/cache/offline gaps and the **expo cluster** for Expo Router/toolchain evidence.
- **Fetch / cache / sync data** → `native-data-fetching`.
- **Toolchain** (EAS build/submit/update, dev client, Expo Router, native modules, SDK upgrade) → **expo cluster** (`expo-orchestrator`).
- **Native iOS** (SwiftUI, UIKit, HIG) → **native-ios cluster** (`mobile-ios-design`).

## Standard Operating Flow

1. Identify the craft: layout/motion, touch, screen design, data, or whole-flow review.
2. For whole-flow review, read the product contract first: actors, role gates, success states, safety/consent, revenue or token rules, and live-vs-demo boundaries.
3. Pull the relevant model from `react-native-core` (e.g. Reanimated worklets, list performance, Platform splits, integrated-flow audit checklist).
4. Delegate to the spoke(s). If the request implies Expo Router, build, ship, or native module evidence, redirect that part to `expo-orchestrator`.
5. Return: chosen spoke(s), runtime concerns in play (UI-thread vs JS-thread, New Arch), implementation gaps, verification path, and next action.

## Guardrails

See `react-native-core`. In short: run animations/gestures on the **UI thread** (Reanimated
worklets + Gesture Handler) — never block the JS thread; animate transforms, not layout, for
60fps; respect `prefers-reduced-motion` / reduce-motion settings; use `Platform`/platform-file
splits instead of runtime OS branching where it matters; and virtualize long lists
(FlatList/FlashList) rather than mapping arrays.

For integrated-flow audits, do not start with screen polish. Trace the flow contract from
source of truth to route graph, state authority, API/cache, persistence, recovery states, and
verification evidence. Fixture or mock fallbacks are acceptable only when they are explicitly
labeled as simulator/demo paths and cannot masquerade as production proof.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
