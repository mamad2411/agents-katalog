---
name: mobile-flutter-core
description: "Shared reference for the mobile-flutter cluster: the state-management decision (which solution, and the immutable-state contract it implies), the layered-architecture rule, the async/lifecycle safety rules, and the Dart/Flutter/KMP version & tooling matrix. USE WHEN choosing a state solution, designing the data/domain boundary, or aligning Flutter/Android/KMP tooling — the decisions every spoke shares."
cluster: mobile-flutter
version: 1.0.0
---

# Mobile Flutter Core

Shared model for the `mobile-flutter` cluster. The pattern, review, and architecture spokes all
depend on these decisions — keep them consistent here so no spoke contradicts another.

## 1. The decision this cluster turns on: state management

Everything else (immutability, testing, rebuild discipline, DI) follows from **which state
solution you pick**. Pick **one per app** and stay consistent. The two families:

- **Immutable-state** (BLoC/Cubit, Riverpod, Redux) — state is replaced, never mutated; new
  instances via `copyWith`/constructors; `==`/`hashCode` over all fields. UI rebuilds when a new
  value is emitted.
- **Reactive-mutation** (MobX, GetX, Signals) — state is mutated through a tracked API
  (`@action`, `.value`, `.obs`); derived values use the computed mechanism; reactions/disposers
  must be cleaned up.

| Concern | BLoC/Cubit | Riverpod | Provider | GetX | MobX | Signals |
|---|---|---|---|---|---|---|
| Container | `Bloc`/`Cubit` | `Notifier`/`AsyncNotifier` | `ChangeNotifier` | `GetxController` | `Store` | `signal()` |
| UI consumer | `BlocBuilder` | `ConsumerWidget` | `Consumer` | `Obx`/`GetBuilder` | `Observer` | `Watch` |
| Selector | `buildWhen`/`BlocSelector` | `ref.watch(p.select)` | `Selector` | — | `computed` | `computed()` |
| Disposal | auto via `BlocProvider` | `.autoDispose` | auto via `Provider` | `onClose()` | `ReactionDisposer` | manual |
| Testing | `blocTest()` | `ProviderContainer` | directly | `Get.put` | store directly | signal directly |

**Default recommendation:** Riverpod or BLoC for non-trivial apps (immutable, testable,
explicit async states). Implementation patterns → `dart-flutter-patterns`; review rules per
solution → `flutter-dart-code-review` (§4).

## 2. Immutable-state contract (the rule the decision implies)

- Model mutually-exclusive states as **sealed types / union variants** (or the solution's async
  type like Riverpod `AsyncValue`) — never boolean flags (`isLoading` + `hasError` is an
  impossible-state generator).
- Every async op models **loading / success / error** as distinct states; error states carry the
  error, loading states don't carry stale data.
- Collections inside state are exposed as **unmodifiable views**, not raw `List`/`Map`.
- Handle every variant exhaustively in the UI (Dart 3 `switch` expression enforces this).

## 3. Layered architecture (shared across Flutter & native/KMP)

Business logic lives **outside the widget/UI layer**, behind injected dependencies, with a
repository abstracting data sources. Dependency direction points inward:

```
presentation ──> domain <── data
       │            ▲         │
       └── design ──┘         └── DB / network
domain depends on nothing framework-specific (pure Dart / pure Kotlin).
```

- Flutter UI structure (widget decomposition, clean layering) → `dart-flutter-patterns`.
- Native Android / Kotlin-Multiplatform modules, UseCases, Repositories, mappers, DI → `android-clean-architecture`.
- **Rule:** never expose DB entities/DTOs to the UI — map to domain models; keep `domain` import-pure.

## 4. Async & lifecycle safety (cross-cutting, non-negotiable)

- After **any `await`** in a `StatefulWidget`, check `mounted` (or `context.mounted`, Flutter
  3.7+) before touching `BuildContext` — navigation, dialogs, `ScaffoldMessenger`.
- Cancel every manual subscription (`.listen()`), close stream controllers, cancel timers in
  `dispose()`/`close()`. Prefer declarative builders over manual subscriptions.
- Never store `BuildContext` in singletons, controllers, or static fields.
- Run futures concurrently (`Future.wait` / record `.wait`) instead of awaiting sequentially.

## 5. Version / tooling matrix

| Layer | Target | Notes |
|---|---|---|
| Language | **Dart 3+** | sealed classes, records, patterns, exhaustive `switch` are assumed |
| Flutter | 3.7+ | `context.mounted` guard; current widget/perf APIs |
| Codegen | `freezed` + `*.g.dart` | generated files current or git-ignored |
| Routing | GoRouter (declarative) | one routing approach per app — no mixing imperative + declarative |
| Networking | Dio (interceptors, one-time refresh-retry guard) | secure storage for tokens |
| Native / KMP | Kotlin + Room *(Android)* / SQLDelight + Ktor *(KMP)* | DI via Koin (KMP) or Hilt (Android) |
| Lint | strict `analysis_options.yaml` | `strict-casts/inference/raw-types`; `very_good_analysis` or `flutter_lints` |

## 6. Shared guardrails

- **One** state-management solution and **one** routing approach per app; stay consistent.
- Business logic out of widgets; dependencies injected, never constructed in-place.
- Sealed/union states over boolean flags; exhaustive handling in UI.
- `mounted`-check `BuildContext` after every `await`; dispose every subscription.
- Keep `domain` framework-pure; map entities/DTOs → domain models at the boundary.
- Secrets via `--dart-define`/secure storage — never hardcoded in Dart, never logged.
- Run `flutter analyze` + the test suite in CI; failures block merges → `flutter-dart-code-review`.
- Flutter vs native/KMP: pick Flutter for a single cross-platform UI codebase; reach for
  `android-clean-architecture` (KMP) when you need shared business logic with fully native UI.
