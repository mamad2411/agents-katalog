---
name: android-feature
version: 3.0.0
license: Apache-2.0
description: >
  Production-ready, step-by-step skill for implementing a new feature in any modern
  Android application (Kotlin, Jetpack Compose, Hilt, MVI, offline-first). Encodes
  module/package layout, file-by-file templates, naming conventions, and quality bars
  derived from the Now in Android (android/nowinandroid) reference architecture.
  Covers feature module scaffolding (single module AND api/impl split), Clean Architecture
  layers (Presentation → Domain → Data), MVI contract (Screen, View, ViewModel, UiState,
  Intent, Event, ViewMapper), Hilt DI, type-safe Compose Navigation, offline-first
  repository pattern with Room + Ktor, build flavours, Compose preview/test conventions.
  Includes embedded references for software design principles (SOLID/KISS/DRY/YAGNI) and
  quality gates verification (Detekt, Lint, coverage, scoring). Use standalone for
  complete feature building workflow from generation through quality verification.
---

# Android Feature Development

> This skill is a bundle. The `SKILL.md` you are reading is a **router** — it points to the
> deep-dive references, copyable templates, evaluation rubrics, and scripts that together
> form the full guidance. Do not try to memorise everything at once. When you are working
> on a feature, open the file relevant to the layer you are touching.

---

## When to use this skill

Activate this skill when you are:
- Creating a new feature module (any screen / flow new to the app).
- Restructuring an existing screen to follow the canonical layered MVI shape.
- Implementing the core layer scaffold, business logic, and presentation for a feature.
- Verifying code quality before opening a PR.

**This skill includes:**
- **Software design principles** — `references/software-design.md` (SOLID, KISS, DRY, YAGNI engineering foundation).
- **Quality gates & verification** — `references/quality-gates.md` (Detekt, Lint, coverage, scoring rubric).
- **Feature architecture** — 19 references covering domain, data, presentation, UI, navigation, DI, performance, and security.
- **Testing patterns** — `references/testing.md` (unit, integration, screenshot tests).

**Out of scope** (handle with your own process): git/PR workflow, peer code-review process,
cross-feature microfrontend contracts, and KMP/multiplatform targets. This skill stays
focused on building one Android feature well, from generation through quality verification.

---

## Standards alignment (validated against Now in Android)

This skill is validated against the official [Now in Android](https://github.com/android/nowinandroid)
reference app and the [Android architecture guide](https://developer.android.com/topic/architecture).

**Matches NiA / official guidance exactly:**
- Reactive **Unidirectional Data Flow** (events down, data up) via Kotlin Flows.
- **Offline-first** data layer as the single source of truth; data exposed as streams, never snapshots.
- **Repository pattern** as the public data API; each repository owns its models.
- **Hilt** for dependency injection throughout.
- **Type-safe Jetpack Navigation** for Compose.
- **Room** for local persistence; **sealed** UiState modelling (`Loading`/`Success`/`Error`).
- ViewModels as state holders exposing `StateFlow`.

**Deliberate, documented divergences (all defensible — pick what fits your project):**

| Topic | This skill | Now in Android | Why |
|-------|-----------|----------------|-----|
| Repository interface location | **Domain layer** (Clean-Architecture style) | Data layer (`:core:data`) | Both are valid ([NiA discussion #1273](https://github.com/android/nowinandroid/discussions/1273)). Domain-owned interfaces keep the dependency rule pointing inward. If you prefer NiA's exact model, move the interface to `data/`. |
| Networking | **Ktor** + kotlinx.serialization | Retrofit + OkHttp | Ktor is KMP-ready, easing a future multiplatform migration. Swap to Retrofit if you're Android-only and prefer NiA's stack. |
| Presentation pattern | Formal **MVI** (Intent / Event / ViewMapper) | Plainer UDF ViewModels + event callbacks | MVI adds explicit, testable contracts. NiA's lighter approach is also fine; drop Intent/Event if you want less ceremony. |
| Build flavors | Flavorless `debug`/`release` in examples | `demo`/`prod` | Generic default. Substitute your project's flavors in Gradle commands. |
| "Clean Architecture" framing | Used as organizing vocabulary | NiA explicitly is **not** Clean Architecture | The layering is compatible; the term is just a convenient label here. |

> The official Android architecture note is explicit: *"The official Android architecture is
> different from other architectures, such as Clean Architecture. Concepts from other
> architectures may not apply here, or be applied in different ways."* This skill blends NiA's
> layering with a Clean-Architecture-style domain layer — a common, well-supported hybrid.

---



For every new feature `<Feature>` (e.g. `Transactions`, `CardManagement`, `Profile`):

1. **Scaffold** — `:feature:<feature>` (single module) or `:feature:<feature>:api` + `:feature:<feature>:impl` if other features must navigate to it. See `references/modularization.md`.
2. **Domain** — model → repository interface → use case → mapper. Pure Kotlin. See `references/domain-layer.md`.
3. **Data** — DTO + Entity + RemoteDataSource + LocalDataSource + RepositoryImpl. Offline-first. See `references/data-layer.md`.
4. **Presentation MVI** — `<Feature>UiState`, `<Feature>Intent`, `<Feature>Event`, `<Feature>ViewModel`, `<Feature>ViewMapper`. See `references/mvi-contract.md` and `references/presentation-layer.md`.
5. **UI** — `<Feature>Screen` (stateful) + `<Feature>View` (stateless, previewable). See `references/presentation-layer.md`.
6. **DI + Navigation** — Hilt module binding interfaces; type-safe `@Serializable` routes. See `references/dependency-injection.md` and `references/navigation.md`.

---

## File map of this skill bundle

```
android-feature/
├── SKILL.md                         ← You are here (complete feature-building router)
│
├── references/                      ← Deep-dive guidance (optimized for feature development)
│   ├── software-design.md           ← SOLID, KISS, DRY, YAGNI, naming conventions (CORE)
│   ├── quality-gates.md             ← Detekt, Lint, coverage, scoring, verification (CORE)
│   ├── architecture.md              ← Layered architecture, UDF, offline-first overview
│   ├── modularization.md            ← Single module vs api/impl, convention plugins
│   ├── package-layout.md            ← Authoritative package + folder structure
│   ├── domain-layer.md              ← Models, repository interfaces, use cases, mappers
│   ├── data-layer.md                ← DTOs, Entities (Room), DataSources, RepositoryImpl
│   ├── presentation-layer.md        ← ViewModel, StateFlow, stateIn(WhileSubscribed)
│   ├── mvi-contract.md              ← UiState / Intent / Event / ViewMapper rules
│   ├── ui-compose.md                ← Screen vs View split, previews, accessibility
│   ├── navigation.md                ← Type-safe Compose Navigation, routes, deep links
│   ├── dependency-injection.md      ← Hilt modules, scopes, @Binds vs @Provides
│   ├── security.md                  ← Mobile security baseline (storage, network, logging)
│   ├── performance.md               ← Cold start, baseline profiles, Compose recompositions
│   ├── testing.md                   ← Use case / VM / repo test patterns
│   ├── screenshot-testing.md        ← Roborazzi setup, snapshot conventions
│   ├── benchmarking.md              ← Macrobenchmark + Microbenchmark + baseline profiles
│   └── anti-patterns.md             ← Rejection table for code review
│
├── templates/                       ← Copy-pasteable file skeletons
│   ├── domain/
│   │   ├── Model.kt.template
│   │   ├── Repository.kt.template
│   │   └── UseCase.kt.template
│   ├── data/
│   │   ├── Dto.kt.template
│   │   ├── DtoMapper.kt.template
│   │   ├── Entity.kt.template            ← Room @Entity
│   │   ├── EntityMapper.kt.template
│   │   ├── Dao.kt.template               ← Room @Dao
│   │   ├── RemoteDataSource.kt.template  ← Ktor
│   │   ├── LocalDataSource.kt.template   ← Wraps Room Dao
│   │   ├── OfflineFirstRepository.kt.template
│   │   └── HttpClientFactory.kt.template ← Ktor + OkHttp engine
│   ├── presentation/
│   │   ├── UiState.kt.template
│   │   ├── Intent.kt.template
│   │   ├── Event.kt.template
│   │   ├── ViewMapper.kt.template
│   │   └── ViewModel.kt.template
│   ├── ui/
│   │   ├── Screen.kt.template
│   │   └── View.kt.template
│   ├── test/
│   │   └── ScreenshotTest.kt.template    ← Roborazzi (androidUnitTest)
│   ├── benchmark/
│   │   ├── Microbenchmark.kt.template
│   │   ├── Macrobenchmark.kt.template
│   │   └── BaselineProfile.kt.template
│   ├── navigation/
│   │   └── Navigation.kt.template
│   └── di/
│       └── Module.kt.template            ← Hilt + Ktor + Room + Kermit + dispatchers
│
├── eval/                            ← How to evaluate a feature against this skill
│   ├── checklist.md                 ← Pre-PR boolean checklist
│   ├── architecture-fitness.md      ← Qualitative architecture review questions
│   └── quality-rubric.md            ← Scored rubric (0–4) across 12 axes (max 48)
│
├── config/                          ← Plug-and-play starters (zero authoring needed)
│   ├── detekt/detekt.yml            ← Detekt config matching the quality-gates rules
│   └── libs.versions.toml           ← Exact dependency set for the templates' stack
│
├── scripts/
│   ├── run-quality-gates.sh         ← Runs build + detekt + lint + tests + coverage
│   └── scaffold-feature.sh          ← Generates the empty file skeleton
│
├── README.md                        ← Adoption guide + measured token usage + LICENSE (Apache-2.0)
```

**Legend:**
- CORE = Loaded with feature generation, always available
- Other = Reference on-demand during development

---

## Authoritative package layout (summary)

For a feature `transactions` in a module `:feature:transactions`, package
`com.<org>.feature.transactions`:

```
presentation/
├── screen/      ← <Feature>Screen.kt (stateful) + <Feature>View.kt (stateless)
├── viewmodel/   ← <Feature>ViewModel.kt
├── state/       ← <Feature>UiState.kt (sealed)
├── intent/      ← <Feature>Intent.kt (sealed)
├── event/       ← <Feature>Event.kt (sealed, one-shot)
└── viewmapper/  ← <Feature>ViewMapper.kt

domain/
├── model/       ← Pure Kotlin data classes / sealed interfaces
├── repository/  ← interfaces only
├── usecase/     ← one operation per class, operator fun invoke
└── mapper/      ← cross-domain mappers (rare)

data/
├── repository/  ← OfflineFirst<Feature>Repository.kt
└── datasource/
    ├── network/  ← <Feature>RemoteDataSource + Api + dto/
    └── local/    ← <Feature>LocalDataSource + Dao + entity/

di/              ← <Feature>Module.kt (Hilt @Module)
navigation/      ← <Feature>Navigation.kt (typed routes)
```

Full per-folder rules in `references/package-layout.md`.

---

## Feature Development Workflow

### Build (Steps 1–6)
Generate the complete feature end-to-end using the TL;DR recipe above.

### Verify (Built-in Guidance)

**Step 7: Quality Verification** — See `references/quality-gates.md` for:
- Automated checks (Detekt, Lint, tests, coverage)
- Manual verification checklist
- Architecture fitness evaluation
- Quality scoring (0–40 rubric)

**Step 8: Design Review** — See `references/software-design.md` for:
- SOLID principles validation
- KISS, DRY, YAGNI compliance
- Naming conventions alignment
- Pre-commit quality checklist

**Step 9: Cross-Feature Concerns** (if applicable):
- For PRs/release workflow → follow your team's git and PR process.
- For peer code review → use `eval/checklist.md` and `eval/architecture-fitness.md` as the review rubric.
- For multi-module / cross-feature navigation → see the api/impl split in `references/modularization.md`.

---

## Quick rules — never violate

These are the non-negotiable rules. Detailed reasoning lives in `references/`.

- **Domain has zero Android imports.** Pure Kotlin only.
- **DTOs and Entities are `internal`.** Domain models are `public`.
- **Mappers are extension functions**, never methods inside the DTO/Entity.
- **Repository is `@Singleton`**, offline-first (Flow from local, sync writes to local).
- **`@Dispatcher(IO)` injected** — never hardcoded `Dispatchers.IO`.
- **ViewModel exposes only `StateFlow<UiState>`** built with `stateIn(viewModelScope, WhileSubscribed(5_000), Loading)`.
- **State / Intent / Event are sealed.** `when` is exhaustive.
- **Events via `Channel(Channel.BUFFERED).receiveAsFlow()`** for one-shot effects.
- **Screen uses `collectAsStateWithLifecycle()`.** Never `collectAsState()`.
- **View is stateless** with `@PreviewLightDark` for every meaningful state.
- **Hilt binds interfaces**, never concrete classes.
- **Navigation routes are `@Serializable`.** Features expose `NavGraphBuilder.<feature>Screen(...)`.
- **No `LiveData` anywhere.** `StateFlow` always.
- **Run quality gates** before opening a PR.

Full rationale per rule in the relevant `references/` file. Anti-pattern table in
`references/anti-patterns.md`.

---

## References

- Now in Android — Architecture Learning Journey
  <https://github.com/android/nowinandroid/blob/main/docs/ArchitectureLearningJourney.md>
- Now in Android — Modularization Learning Journey
  <https://github.com/android/nowinandroid/blob/main/docs/ModularizationLearningJourney.md>
- Official Android architecture guide
  <https://developer.android.com/topic/architecture>
- WhileSubscribed(5000) deep-dive
  <https://blog.p-y.wtf/whilesubscribed5000>
