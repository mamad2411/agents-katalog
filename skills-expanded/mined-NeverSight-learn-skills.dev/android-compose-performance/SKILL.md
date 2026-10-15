---
name: "android-compose-performance"
description: "Profile and improve Compose recomposition, layout, scrolling, startup, and rendering performance in Android apps."
metadata:
  version: "0.1.0"
  category: "ui"
  tags: ["android", "compose", "performance", "profiling"]
  triggers:
    include: ["compose performance issue", "recomposition too much android", "slow lazycolumn compose", "compose startup jank", "measure compose rendering", "compose recomposition storm", "unstable lazycolumn keys android"]
    exclude: ["play release notes only", "room migration only", "permission denied ui only", "coil image loading only", "rxjava migration only"]
  owners: ["@android-agent-skills/maintainers"]
  test_targets: ["examples/orbittasks-compose", "examples/orbittasks-xml", "benchmarks/triggers.jsonl"]
---
# Android Compose Performance

## When To Use
- Use this skill when the request is about: compose performance issue, recomposition too much android, slow lazycolumn compose.
- Primary outcome: Profile and improve Compose recomposition, layout, scrolling, startup, and rendering performance in Android apps.
- Handoff skills when the scope expands:
- `android-performance-observability`
- `android-testing-ui`

## Workflow
1. Identify whether the target surface is Compose, View system, or a mixed interoperability screen.
2. Select the lowest-friction UI pattern that satisfies responsiveness, accessibility, and performance needs.
3. Build the UI around stable state, explicit side effects, and reusable design tokens.
4. Exercise edge cases such as long text, font scaling, RTL, and narrow devices in the fixture apps.
5. Validate with unit, UI, and screenshot-friendly checks before handing off.

## Guardrails
- Optimize for stable state and predictable rendering before adding animation or abstraction.
- Respect accessibility semantics, contrast, focus order, and touch target guidance by default.
- Do not mix Compose and View system ownership without an explicit interoperability boundary.
- Prefer measured performance work over premature micro-optimizations.

## Anti-Patterns
- Embedding navigation or business logic directly in leaf UI components.
- Using fixed dimensions that break on localization or dynamic text.
- Ignoring semantics and announcing only visual changes.
- Porting XML patterns directly into Compose without adapting the mental model.

## Remediation Examples
### Stabilize list identity
```kotlin
LazyColumn {
    items(tasks, key = { it.id }) { task ->
        TaskRow(task)
    }
}
```

### Move heavy work out of composition
```kotlin
@Composable
fun TaskBoard(tasks: List<TaskUiModel>) {
    val visibleTasks = remember(tasks) { tasks.sortedBy { it.title } }
    LazyColumn { items(visibleTasks, key = { it.title }) { TaskRow(it) } }
}
```

### Avoid broad scroll-driven recomposition
```kotlin
Box(
    modifier = Modifier.offset {
        IntOffset(0, scrollState.value)
    }
)
```

## Examples
### Happy path
- Scenario: Profile the Compose task list for unnecessary recomposition hotspots.
- Command: `cd examples/orbittasks-compose && ./gradlew :app:testDebugUnitTest`

### Edge case
- Scenario: Evaluate long lists, filter chips, and snackbar churn under repeated state changes.
- Command: `cd examples/orbittasks-compose && ./gradlew :app:assembleDebug`

### Failure recovery
- Scenario: Separate performance requests from generic Compose or observability prompts.
- Command: `python3 scripts/eval_triggers.py --skill android-compose-performance`

## Done Checklist
- The implementation path is explicit, minimal, and tied to the right Android surface.
- Relevant example commands and benchmark prompts have been exercised or updated.
- Handoffs to adjacent skills are documented when the request crosses boundaries.
- Official references cover the chosen pattern and the main migration or troubleshooting path.

## Official References
- [https://developer.android.com/develop/ui/compose/performance](https://developer.android.com/develop/ui/compose/performance)
- [https://developer.android.com/topic/performance/benchmarking/macrobenchmark-overview](https://developer.android.com/topic/performance/benchmarking/macrobenchmark-overview)
- [https://developer.android.com/topic/performance/baselineprofiles/overview](https://developer.android.com/topic/performance/baselineprofiles/overview)
- [https://developer.android.com/studio/profile/overview](https://developer.android.com/studio/profile/overview)
