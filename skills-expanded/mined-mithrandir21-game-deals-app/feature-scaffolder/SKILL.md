---
name: feature-scaffolder
description: Scaffold a new Android or KMP feature module that matches the project's existing conventions — layering, DI, navigation, and tests. Use whenever the user asks to "add a feature", "start a new screen", "create a module for X", "set up the skeleton for Y", or "wire up a new feature end-to-end". Especially valuable in modularized codebases where consistency with existing patterns matters more than picking ideal patterns from scratch.
---

# Feature Scaffolder

Spin up a new feature module that looks like it was written by whoever already works on this codebase. The point is to match conventions, not to introduce them.

## When to use

Trigger phrases: "scaffold", "skeleton", "new feature", "new module", "wire up", "add a screen for…", "create the module structure for…".

Do **not** use this for a one-off Composable inside an existing feature — that's just normal editing.

## Process

### Phase 1: Read the conventions

Before generating anything, inspect the repo. The goal is to copy patterns, not invent them.

Look at one or two existing feature modules and note:

- Module layout: single module per feature, or `:feature:foo:api` / `:feature:foo:impl` split? Domain/data extracted or co-located?
- Gradle setup: convention plugins (`buildSrc` / `build-logic`)? Version catalog name?
- DI: Hilt or Koin? Where bindings live (`*Module.kt`, `di/`, top-level)?
- Navigation: Compose Navigation type-safe routes, Voyager, Decompose, Jetpack Nav with strings?
- State: ViewModel + StateFlow? MVI? Molecule?
- Tests: Where unit tests live, what dispatcher/turbine setup, what assertion lib.

Confirm the inventory with the user in a few lines before scaffolding. Surprises cost more than a 30-second confirmation.

### Phase 2: Propose the structure

Present the file tree you intend to create. Don't generate yet. Example:

```
:feature:onboarding
├── build.gradle.kts
└── src/
    ├── main/kotlin/com/app/onboarding/
    │   ├── OnboardingRoute.kt           ← public nav entry
    │   ├── ui/OnboardingScreen.kt
    │   ├── ui/OnboardingViewModel.kt
    │   ├── ui/OnboardingUiState.kt
    │   ├── domain/StartOnboardingUseCase.kt
    │   ├── data/OnboardingRepository.kt
    │   └── di/OnboardingModule.kt
    └── test/kotlin/.../OnboardingViewModelTest.kt
```

Flag anything ambiguous (e.g. "your other features use a separate `:domain` module — should this one too?") and let the dev decide.

### Phase 3: Generate

Create files in this order so each compiles against what came before:

1. `build.gradle.kts` — apply the convention plugin used by sibling modules; reuse versions from the catalog.
2. Settings include — add `include(":feature:foo")` to `settings.gradle.kts`.
3. Data layer — repository interface + a stub impl returning hardcoded data so the rest can compile.
4. Domain — use cases that wrap the repo (skip if the project doesn't use a domain layer).
5. ViewModel + UiState — `StateFlow<UiState>` exposed, events handled via a single `onEvent(Event)` or named functions, whichever the project uses.
6. Screen — Composable that takes `(state, onEvent)` and a stateful wrapper that hoists from the ViewModel.
7. Route/nav entry — registers the destination in the project's nav graph.
8. DI module — provides the repo and (if needed) ViewModel.
9. App wiring — add the route to the main NavHost or app graph.
10. Test skeleton — one ViewModel test that exercises the happy path with `runTest` + `Turbine`/equivalent.

### Phase 4: Verify

Don't claim "done" until:

- `./gradlew :feature:foo:assembleDebug` (or KMP equivalent) succeeds.
- The new screen is reachable from the app — point the dev at the exact deep link or nav action to try.
- The one test runs green.

## KMP variant

If the project is KMP and the feature has shared logic:

- Put repository + use cases in `commonMain` of a shared module (`:shared:feature:foo` if the project uses that naming, else inside the existing `:shared`).
- Android-specific UI stays in the Android feature module and depends on the shared module.
- For iOS, expose only the ViewModel-equivalent (e.g. a `Store` or `Presenter`) — don't leak Flows directly unless the project already uses SKIE / KMP-NativeCoroutines.

## Output

A working, navigable, testable feature skeleton with no business logic — just the wiring. The dev fills in the actual behavior. Hand off with: which files were created, what command verifies it builds, and where to put the first real logic.

## Common pitfalls

- **Inventing patterns.** If existing modules use Koin, don't introduce Hilt. Match what's there even if it's not your preference.
- **Over-scaffolding.** Don't generate domain + data layers if the project keeps things flat in a single layer. Match the depth that's already there.
- **Skipping the build check.** A skeleton that doesn't compile is worse than no skeleton — the dev now has to debug your code before writing theirs.
