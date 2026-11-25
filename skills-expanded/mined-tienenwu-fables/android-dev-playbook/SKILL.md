---
name: android-dev-playbook
description: Use when writing, refactoring, or debugging Android app code (Kotlin, Jetpack Compose, Gradle, ProGuard/R8) — before adding a feature, touching build config or proguard-rules, preparing a release/AAB, or when facing release-only crashes, ClassNotFoundException after minify, lifecycle leaks, ANR, or excessive recomposition.
---

> 🌐 [繁體中文（canonical）](https://github.com/tienenwu/fables/blob/main/android/SKILL.md) · English mirror

# Android Development Judgment Handbook

## Core Principles

1. **A green light on a debug build does not count**: R8, obfuscation, signing, and backend environment flags only take effect in release — changes on the release path must be verified with release-grade builds.
2. **State flows down, events flow up**: the UI layer makes no business decisions; a Composable holds no mutable business state.
3. **The lifecycle is the default enemy**: for any long-lived object holding a Context/View, first assume it will leak, then prove it won't.
4. **Reflection is R8's blind spot**: for every class constructed via reflection (Gson/Moshi/Retrofit models), change the keep rules in lockstep when the class changes — otherwise it's a release-only bomb.
5. **No IO on the main thread, no `GlobalScope` for coroutines** — there is no exceptional case worth discussing.

## Kickoff Routing

| Situation | Path | Read first |
|-----------|------|-----------|
| New screen/feature | Define the state owner and data flow first, then write the UI | references/architecture-state.md |
| UI jank, excessive recomposition | Don't touch the UI first — inspect the state design | references/compose-ui.md |
| Async, Flow, lifecycle issues | Check collect location and scope choice | references/coroutines-lifecycle.md |
| Add/change API model (Gson/Moshi/Retrofit) | Change implementation + keep rules together | references/release-checklist.md §R8 |
| Ship release / change build config | Run every item on the mandatory checklist | references/release-checklist.md |
| Crashes only in release, fine in debug | Assume minify/obfuscation/environment flags first, don't guess | references/release-checklist.md |

## Red Lines (Absolutely Forbidden)

- **Never declare release-related changes done after verifying only with a debug build** — minify, keep rules, and BuildConfig flags all have zero effect in debug.
- **Never `GlobalScope.launch`** — the lifecycle is uncontrolled; it keeps running after the screen is destroyed, causing both leaks and crashes.
- **Never make network/DB calls in the body of a Composable function** — it fires again on every recomposition; use `LaunchedEffect` or push it down into the ViewModel.
- **Never let a ViewModel hold a reference to an Activity/Fragment/View** — rotating the screen leaks it immediately; if you need a Context, use the Application-level one.
- **Never catch and only log without notifying the caller** — the user sees a spinner that never stops; errors must become UI state.
- **Never change test assertions to turn CI green** — two red runs in a row is a wrong-direction signal; back up to the previous decision point.

## Failure Signals (Back Up, Don't Retry)

| Symptom | Usually means | Back up to |
|---------|---------------|-----------|
| Fix recomposition in one place, another place janks | State placed at the wrong layer, granularity too coarse | Rethink the state-owner design |
| Piling on more `remember` / `derivedStateOf` just to stop flicker | Upstream is passing an unstable object as state | Check the stability of the incoming parameters |
| Fix one keep rule for a release crash and the next one pops | Patching class by class; keep the whole model directory instead | R8 rule layer |
| More and more null checks inside lifecycle callbacks | Holding a reference you shouldn't | Ownership design |
| Same ANR persists after three different rewrites | Hidden synchronous IO on the main thread | Find the real blocking point before touching anything |

## references Index

- `references/architecture-state.md` — layering criteria, which layer state belongs in, UDF positive/negative examples. Read before touching architecture or adding a feature.
- `references/compose-ui.md` — when to extract a Composable, stability and recomposition, side-effect API choice. Read before writing UI.
- `references/coroutines-lifecycle.md` — scope/Dispatcher choice, Flow collect location, typical leaks. Read whenever you touch async.
- `references/release-checklist.md` — R8/keep, build variant, signing, permissions, item-by-item sign-off before publishing. Mandatory before shipping a release.
- `references/test-scenarios.md` — the judgment test set, to verify whether the model taking over actually follows the playbook. Do not give it to a model that is executing.
