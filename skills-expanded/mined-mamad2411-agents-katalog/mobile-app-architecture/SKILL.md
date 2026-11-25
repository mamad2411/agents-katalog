---
name: mobile-app-architecture
description: Cross-platform mobile architecture patterns covering layering, state management, offline-first sync, navigation, deep links, push, and modularization. Use when designing or reviewing the architecture of any mobile app (native or cross-platform) independent of framework choice.
source: self
---

# Mobile App Architecture

Framework-agnostic architecture guidance for mobile apps. Apply alongside the framework-specific skills (`mobile-android-native`, `mobile-ios-native`, `mobile-flutter`, `mobile-react-native`, `mobile-kotlin-multiplatform`).

## When to Use

- Starting a new mobile app and choosing a layering and state strategy
- Reviewing a mobile codebase for architectural drift, coupling, or testability issues
- Designing offline-first sync, conflict resolution, or background processing
- Defining navigation, deep linking, and push notification flows that survive cold start and process death
- Modularizing a growing mobile codebase

## Core Principles

1. **One source of truth per piece of state.** UI is derived; never duplicated across screens or layers.
2. **Unidirectional data flow.** State flows down, events flow up; side effects are explicit and testable.
3. **Layered, dependency-inverted.** UI → Domain → Data, with the Domain layer free of framework imports.
4. **Survive lifecycle hostility.** Process death, low memory kills, OS-driven backgrounding, and network loss are normal — design for them.
5. **Offline-first by default for user data.** The network is a cache update strategy, not a precondition for the UI to render.
6. **Native where it matters, shared where it pays.** Choose the platform mix based on UX risk, team shape, and product cadence — not hype.

## Layering

- **Presentation:** screens, components, view models / controllers. Holds UI state only.
- **Domain:** entities, value objects, use cases. Pure language types — no framework imports, no I/O.
- **Data:** repositories, remote sources (HTTP/gRPC/GraphQL), local sources (SQL/KV), mappers. Implements interfaces declared in the Domain.
- **Platform:** thin adapters for Keychain/Keystore, biometrics, push, location, camera, sensors.

Rules:
- Dependencies point inward. Data depends on Domain interfaces, never the reverse.
- DTOs live in Data; never let API shapes leak into UI.
- Use cases coordinate repositories and encode business rules — keep them small and composable.

## State Management

- Choose one primary pattern and apply it consistently: MVVM + UDF (Android/iOS), Riverpod/Bloc (Flutter), Redux/Zustand/MobX (RN). Avoid mixing.
- Model UI state as an immutable value (`UiState` sealed type) with explicit `loading`, `error`, `empty`, and `content` cases.
- Separate transient events (toasts, navigation, snackbars) from persistent state — use a one-shot event channel.
- Persist screen-level state (form input, scroll position) across process death using the platform's saved-state mechanism.

## Navigation & Deep Links

- Use a declarative, type-safe router (Navigation Compose, SwiftUI Navigation, `go_router`, React Navigation typed routes).
- Treat deep links as first-class entry points; every screen reachable via deep link must handle being the start destination.
- Validate and sanitize all deep link parameters; reject unknown hosts and paths.
- Authenticate deep links: if a target requires auth, route through a login flow that returns to the original destination.
- Handle universal/app links explicitly — fall back to a web URL when the app is not installed.

## Push Notifications

- Use a single notification service abstraction; map FCM/APNs payloads to a typed domain event.
- Always include a deep link or routing key in the payload — never hard-code navigation in the handler.
- Handle three states: foreground, background, and terminated. Test all three on real devices.
- Respect platform notification permissions and quiet hours; provide in-app preference UI.
- Token lifecycle: refresh on app start, on user change, and on token rotation; deregister on logout.

## Offline-First & Sync

- Read path: UI reads from the local store (SQL/KV) and observes changes; network refreshes the store, never the UI directly.
- Write path: write locally first with a "pending" flag; enqueue a sync job; reconcile on success/failure.
- Use a background scheduler (WorkManager on Android, BGTaskScheduler on iOS, Workmanager plugin in Flutter) for retries with exponential backoff.
- Conflict resolution: pick a strategy explicitly — last-write-wins, server-wins, CRDT, or domain-specific merge. Document it.
- Cache invalidation: combine TTL + ETag/`If-Modified-Since` + push-driven invalidation when available.
- Detect connectivity changes but never block UI on them; show clear "offline" affordances and queued-action counts.

## Background Work

- Distinguish deferrable (sync, analytics flush) from time-sensitive (location update, call) work — use the right primitive.
- Respect OS budgets: Doze, App Standby, low-power mode, iOS background time limits.
- Idempotent jobs only — assume any background task may run twice or be killed mid-flight.
- Coalesce work to save battery; avoid waking the device for trivial reasons.

## Modularization

- Start as a well-layered monolith. Extract modules when build times, ownership, or reuse demand it.
- Module shapes: feature modules (vertical slices), core modules (design system, network, storage, analytics), and app modules (entry points).
- Keep public APIs of modules small and stable; hide implementation details with `internal` (Kotlin/Swift) or package-private equivalents.
- Avoid cyclic dependencies; enforce with a build-time check or fitness function.

## Cross-Platform Choice (Decision Guide)

- **Native (Android + iOS separately):** highest UX fidelity, deepest platform integration, two teams or strong native skills available.
- **Kotlin Multiplatform:** share business logic, keep native UI; best when you have Android + iOS engineers and want native UX with shared correctness.
- **Flutter:** single team, design-driven UI, custom motion, shipping to multiple platforms quickly; accept Dart and a heavier runtime.
- **React Native / Expo:** strong web/JS team, lots of dynamic content, OTA updates important; accept JS bridge tradeoffs.
- **PWA:** simple content/forms, low install friction, no platform-API needs.

Choose based on: UX risk profile, team skills, hiring market, performance budget, native API needs, and time-to-first-release.

## Anti-Patterns

- "God" view models that own state for multiple unrelated screens
- UI reading directly from the network without going through a repository
- Storing app state in static singletons that don't survive process death
- Hard-coding navigation inside push notification or deep link handlers
- Treating the network as required for read paths
- Background work that is not idempotent or does not respect OS scheduling budgets
- Premature modularization that creates more interfaces than features
- Choosing a cross-platform framework based on hype rather than product/team fit

## Review Checklist

- [ ] Layers are clear and dependencies point inward; Domain has no framework imports
- [ ] One state-management pattern is applied consistently across the app
- [ ] All screens survive process death and configuration changes
- [ ] Deep links and push notifications route through a typed, validated entry point
- [ ] Read path is offline-first; write path is queued, retried, and idempotent
- [ ] Background work uses platform-native schedulers and respects OS budgets
- [ ] Module boundaries (if any) have small, stable public APIs and no cycles
- [ ] Cross-platform choice is documented with explicit tradeoffs
