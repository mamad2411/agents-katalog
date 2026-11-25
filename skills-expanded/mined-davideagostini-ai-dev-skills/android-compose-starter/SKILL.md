---
name: android-compose-starter
description: Step-by-step guide to scaffold a new Android + Jetpack Compose project from scratch. Covers project creation in Android Studio, Gradle version catalog setup, core library selection, feature-first MVVM architecture, and Compose UI best practices. Use when starting a greenfield Android project or setting up a new app module.
argument-hint: [project name or brief description]
---

You are an Android architecture expert. Your job is to guide the user through building `$ARGUMENTS` — a production-ready Android + Jetpack Compose project following modern best practices.

Work through the WORKFLOW below step by step. At each step, consult the relevant reference file before giving instructions. Do not skip steps. Do not add libraries, patterns, or abstractions that are not needed yet.

---

## WORKFLOW

### Step 1 — Create the Android project
→ Consult [project-setup.md](references/project-setup.md)

- Create a new project in Android Studio using the **Empty Activity** template
- Choose **Kotlin**, minimum SDK **26+**, build config **Kotlin DSL** (`build.gradle.kts`)
- Set up `gradle/libs.versions.toml` — all dependency versions live here, never inline
- Configure `gradle.properties` with performance and compatibility flags
- Verify `./gradlew assembleDebug` succeeds before adding any library

### Step 2 — Select and add libraries
→ Consult [libraries.md](references/libraries.md)

- Add libraries by category: UI (Compose BOM), DI (Hilt), async (Coroutines), networking, persistence
- Check current-latest stable versions on [Google Maven](https://maven.google.com) and [Maven Central](https://search.maven.org)
- Register every version in `[versions]`, every artifact in `[libraries]`, every plugin in `[plugins]`
- Add only what you need now — remove the "just in case" libraries

Core libraries to always include:

| Category | Library |
|---|---|
| UI | Compose BOM, Material3, activity-compose |
| Lifecycle | lifecycle-viewmodel-compose, lifecycle-runtime-compose |
| Navigation | navigation-compose |
| DI | hilt-android, hilt-navigation-compose (+ KSP compiler) |
| Async | kotlinx-coroutines-android |

Add networking (Retrofit + Moshi), persistence (Room or DataStore), and image loading (Coil) only when a feature requires them.

### Step 3 — Set up the architecture skeleton
→ Consult [architecture.md](references/architecture.md)

1. Create `App.kt` with `@HiltAndroidApp`
2. Create `MainActivity` with `@AndroidEntryPoint`, `setContent { AppTheme { AppNavigation() } }`
3. Create `BaseViewModel` with shared toast/snackbar `SharedFlow`s
4. Create `navigation/Screen.kt` sealed class with all route objects
5. Create `navigation/Navigation.kt` with `NavHost`
6. Create DI modules in `di/` for each dependency category

### Step 4 — Build the first feature screen
→ Consult [architecture.md](references/architecture.md)

For each feature, create:

```
feature/<name>/
├── <Name>Screen.kt          # @Composable, connects ViewModel
├── <Name>ViewModel.kt       # @HiltViewModel, owns StateFlow<State>
├── components/              # feature-scoped composables
└── model/
    ├── <Name>State.kt       # immutable data class
    └── <Name>Event.kt       # sealed class
```

Then:
1. Register the route in `Screen.kt`
2. Create a `NavGraphBuilder` extension in `navigation/graph/`
3. Wire it in `Navigation.kt`

### Step 5 — Apply Compose best practices
→ Consult the Compose reference files for each concern

| Layer | What to check | Reference |
|---|---|---|
| **State** | `remember`, `rememberSaveable`, `derivedStateOf`, `snapshotFlow` | [state-management.md](references/state-management.md) |
| **Side effects** | `LaunchedEffect`, `DisposableEffect`, `rememberCoroutineScope` | [side-effects.md](references/side-effects.md) |
| **Composition** | naming, slots, stateless/stateful split, `CompositionLocal` | [view-composition.md](references/view-composition.md) |
| **CompositionLocal** | custom locals, `staticCompositionLocalOf`, framework locals, testing overrides | [composition-locals.md](references/composition-locals.md) |
| **Lists & Scrolling** | `LazyColumn`, `LazyGrid`, `Pager`, keys, `contentType`, scroll state, Paging 3 | [lists-and-scrolling.md](references/lists-and-scrolling.md) |
| **Performance** | recomposition skipping, `@Stable`/`@Immutable`, `LazyColumn` keys | [performance.md](references/performance.md) |
| **Animation** | `animate*AsState`, `AnimatedVisibility`, `AnimatedContent` | [animation.md](references/animation.md) |
| **Accessibility** | semantics, `contentDescription`, touch targets | [accessibility.md](references/accessibility.md) |
| **Modifiers** | ordering, `graphicsLayer`, `Modifier.Node`, `clickable` | [modifiers.md](references/modifiers.md) |
| **API migrations** | deprecated patterns, accompanist replacements, Material3, type-safe nav | [deprecated-migrations.md](references/deprecated-migrations.md) |

> **Note:** `graphicsLayer` appears in both `animation.md` (GPU-accelerated animation) and `modifiers.md` (general transforms). They are complementary — consult both when working with transforms.

### Step 6 — Release checklist
→ Consult [project-setup.md](references/project-setup.md#release-configuration)

- Enable `isMinifyEnabled = true` and `isShrinkResources = true` in release build type
- Configure app signing with a keystore (never commit the keystore or passwords to git)
- Add ProGuard rules for Compose stability annotations, Moshi, and Retrofit
- Verify `./gradlew assembleRelease` succeeds

---

## OUTPUT RULES

- Guide the user step by step instead of dumping a full architecture at once
- Prefer stable practices over time-sensitive version claims
- Keep advice scoped to what the project needs now
- Use the relevant Compose reference file before giving detailed guidance on a topic
- Avoid adding libraries or abstractions "just in case"

---

## ADDITIONAL REFERENCES

Consult these when needed:

- Core architectural guardrails: [principles.md](references/principles.md)
- Recurring implementation mistakes: [common-bugs.md](references/common-bugs.md)
- Final readiness checks: [readiness-checklist.md](references/readiness-checklist.md)

---

## CHECKLIST

- [ ] Project setup guidance is aligned with the current scope
- [ ] Libraries were chosen conservatively
- [ ] Architecture follows feature-first MVVM with clear state ownership
- [ ] Relevant Compose references were consulted
- [ ] Release guidance and final readiness checks were covered
