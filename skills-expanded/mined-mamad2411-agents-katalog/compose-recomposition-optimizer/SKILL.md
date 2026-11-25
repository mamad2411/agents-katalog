---
name: compose-recomposition-optimizer
description: Diagnose and fix unnecessary recompositions in Jetpack Compose — unstable parameters, missing @Stable/@Immutable, lambdas captured into composables, over-broad state reads, and missing deferred reads. Use whenever the user mentions Compose performance, jank, dropped frames in Compose UIs, "this screen feels slow", "why is this recomposing", or wants to run the Compose compiler metrics. Also use when reviewing a Composable that's complex enough that recomposition cost matters.
---

# Compose Recomposition Optimizer

Recomposition is supposed to be cheap. When it isn't, it's almost always one of a small number of root causes. This skill walks through them in priority order.

## When to use

Triggers: "compose perf", "recomposing too much", "this screen is janky", "compiler metrics", "@Stable", "@Immutable", "strong skipping", "Layout Inspector recomposition counts".

Don't reach for this on plain MVP screens that scroll fine. Use it when there's evidence of a problem (frame drops, visible jank, recomposition counts in Layout Inspector, profiler data).

## Process

### Phase 1: Confirm there's a real problem

Before optimizing, measure. Ask the dev for one of:

- Layout Inspector recomposition counts on the suspect Composable.
- A Macrobenchmark frame timing run.
- The Compose compiler metrics report.

If they don't have any of these yet, point them to **Phase 6** to set up metrics first, then come back. Don't optimize blindly — Compose perf intuition is often wrong, and you'll waste an afternoon.

### Phase 2: Generate compiler metrics

If the project doesn't already emit them, add to the relevant module's `build.gradle.kts`:

```kotlin
composeCompiler {
    metricsDestination = layout.buildDirectory.dir("compose_metrics")
    reportsDestination = layout.buildDirectory.dir("compose_reports")
}
```

Then `./gradlew assembleRelease` and read `*-classes.txt` and `*-composables.txt` from the output.

In the reports:
- `unstable class Foo` → fix Phase 3.
- `restartable skippable fun Bar` is good.
- `restartable fun Bar` (not skippable) means a parameter is unstable.

### Phase 3: Fix unstable parameters

Most recomposition problems come from unstable types passed as parameters. Common offenders and fixes:

| Symptom | Fix |
|---|---|
| `List<Foo>` parameter | Use `ImmutableList<Foo>` (kotlinx.collections.immutable) or wrap in `@Immutable data class FooList(val items: List<Foo>)`. |
| `data class` with `var` properties | Make them `val`, or annotate the class `@Immutable` if you guarantee immutability another way. |
| `data class` referencing an unstable type | Annotate `@Stable` only if you guarantee equality reflects state changes; otherwise refactor the field. |
| Class from another module (e.g. domain) | Add `@Immutable` to the source, or wrap it locally with an `@Immutable` UI model. |
| `Flow<T>` or `StateFlow<T>` parameter | Collect at the boundary (`collectAsStateWithLifecycle`) and pass `T` down. |

With **Strong Skipping Mode** (Kotlin 2.0+), many unstable types skip automatically based on equality — but only when the Composable also doesn't capture unstable lambdas. Confirm Strong Skipping is enabled in the compiler options.

### Phase 4: Fix lambdas and captures

Lambdas are stable when:

- They don't capture anything, or
- They only capture stable values, or
- They're `remember`ed.

Patterns:

- `onClick = { viewModel.doThing() }` — captures `viewModel`. If `viewModel` is stable (it usually is), fine. If not, `remember(viewModel) { { viewModel.doThing() } }`.
- Passing the same lambda to many list items? `remember` it once at the parent, don't recreate per item.
- Method references (`onClick = viewModel::doThing`) are stable and cheap — prefer them when they read well.

### Phase 5: Fix state reads

Recomposition scope is per function. Read state as late as possible.

- **Defer reads with lambdas**: instead of `MyComposable(scrollOffset = state.offset)`, pass `MyComposable(scrollOffset = { state.offset })`. Only the part that actually uses the value recomposes.
- **Don't read state in parent if only child needs it**: pull the `viewModel.state.collectAsStateWithLifecycle()` down into the child that uses it.
- **Avoid `derivedStateOf` for simple transforms** — use it only when the input changes more often than the output (e.g. `derivedStateOf { listState.firstVisibleItemIndex > 0 }`).
- **Lazy lists**: provide stable `key`s. Without them, every item recomposes when the list changes.

### Phase 6: Set up ongoing measurement

So the dev catches regressions next time:

- Compiler metrics in CI (compare stable/unstable counts across PRs).
- A Macrobenchmark `FrameTimingMetric` test on the critical screen.
- Layout Inspector recomposition counts during local development.

## Output

A report listing:

- What the dev measured (or needs to measure first).
- Each root cause found, with the file/line and the specific fix.
- Whether Strong Skipping is enabled, and the impact if not.
- Recommended ongoing checks.

Don't apply fixes without confirmation if the project is large — group them by "definitely safe" (annotations on UI models) vs. "needs review" (changing parameter types across boundaries).

## Common pitfalls

- **Annotating with `@Stable` without justification.** It's a promise to the compiler. If equality doesn't actually reflect state changes, you'll get stale UI.
- **Adding `remember` everywhere.** It costs memory. Only `remember` lambdas you can prove are recreated unnecessarily.
- **Optimizing without measuring.** Compose perf intuition is wrong more often than right. Get the data first.
- **Ignoring keys in `LazyColumn`.** This is the single most common cause of janky lists.
