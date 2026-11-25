---
name: mobile-flutter-orchestrator
description: "Route a Flutter/Dart (and Android/KMP) task to the right specialist — idiomatic patterns, the state-management decision, navigation/networking/codegen wiring, clean-architecture module boundaries, and the review/ship checklist. USE WHEN building, structuring, reviewing, or hardening a Flutter or Kotlin-Multiplatform mobile app but the specific concern hasn't been named."
cluster: mobile-flutter
version: 1.0.0
---

# Mobile Flutter Orchestrator

The single entry skill for Flutter/Dart (and Android/KMP) work. It locates the task on the
**layer × phase** map — UI / state / data / build, then write → review — and delegates to one
of the specialist spokes. The cross-cutting decision every app turns on (which state-management
solution, and the immutable-state contract it implies) plus the shared conventions live in
`mobile-flutter-core`; read it before picking a state library or wiring the data layer.

## Cluster map (spoke → role)

- **`dart-flutter-patterns`** — copy-paste-ready Dart 3 / Flutter patterns: null safety, sealed/immutable state, async composition, widget architecture, BLoC + Riverpod, GoRouter, Dio, Freezed, testing. The "how do I write this" reference.
- **`flutter-dart-code-review`** — library-agnostic review checklist across 15 axes (widgets, state, performance, a11y, security, l10n, DI, static analysis). The "is this code right" gate.
- **`android-clean-architecture`** — module boundaries and dependency rules for Android/KMP (domain → data → presentation), UseCases, Repositories, Room/SQLDelight/Ktor, Koin/Hilt. The "how is the project structured" reference for native + multiplatform.
- **`mobile-flutter-core`** *(shared model)* — the state-management decision matrix, immutable-state contract, layering rule, and version/tooling matrix all spokes share.

## Routing rules by intent

**Write / implement a feature**
- Idiomatic Dart/Flutter code (state, nav, networking, codegen) → `dart-flutter-patterns`
- Choosing/contrasting state solutions before you start → `mobile-flutter-core` (decision matrix), then `dart-flutter-patterns`
- Native Android or Kotlin-Multiplatform module/data layer → `android-clean-architecture`

**Structure / architect**
- Where does this code live? Module + dependency direction → `android-clean-architecture` (native/KMP) or the clean-architecture + widget-architecture sections of `dart-flutter-patterns` (Flutter UI)
- The layering rule that applies to both → `mobile-flutter-core`

**Review / harden**
- PR review, audit, "find what's wrong" → `flutter-dart-code-review`
- Security/perf/a11y pass before ship → `flutter-dart-code-review` (sections 5, 7, 9)

**Cross-cutting decision**
- "Which state library / what's the immutable contract / what versions" → `mobile-flutter-core`

## Standard flow

1. Locate the task: which **layer** (UI → state → data → build) and which **phase** (write vs review).
2. If it touches **state management or the data/domain boundary**, pull the decision from `mobile-flutter-core` first — the state choice constrains immutability, testing, and rebuild discipline downstream.
3. Delegate to the spoke(s). Multi-step asks fan out in layer order (e.g. "build this feature properly" → `mobile-flutter-core` decision → `android-clean-architecture` / `dart-flutter-patterns` to implement → `flutter-dart-code-review` to verify).
4. Return: chosen spoke(s), the state/architecture decision implied, target platform (Flutter / Android / KMP), and the next action.

## Guardrails

See `mobile-flutter-core`. In short: **business logic never lives in widgets** — it sits in a
state container behind injected dependencies, with a repository abstracting data sources. Model
mutually-exclusive states as sealed/union types, not boolean flags. Keep `domain` pure (no
framework imports). Always `mounted`-check a `BuildContext` after an `await`. Pick **one**
state-management solution and one routing approach per app and stay consistent — the cluster's
value is a coherent architecture, not a mix of every pattern at once.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
