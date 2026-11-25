---
name: jetpack-compose
description: Expert guidance on writing idiomatic Jetpack Compose UI with correct recomposition behavior, stable parameters, Material 3 theming, and reusable patterns. Use this for any composable authoring task.
---

# Jetpack Compose — Composable Patterns & Material 3

## Instructions

### 1. Composable Naming and Shape

- `PascalCase` for composables, `Unit` return type.
- First parameter: data. Then `modifier: Modifier = Modifier`. Then callbacks. Optional styling last.
- Extract anything longer than ~30 lines into a named composable.

```kotlin
@Composable
fun ArticleCard(
    article: Article,
    modifier: Modifier = Modifier,
    onClick: (Article) -> Unit = {},
) {
    Card(
        onClick = { onClick(article) },
        modifier = modifier.fillMaxWidth().padding(horizontal = 16.dp),
    ) {
        Column(Modifier.padding(16.dp)) {
            Text(article.title, style = MaterialTheme.typography.titleMedium)
            Spacer(Modifier.height(4.dp))
            Text(article.summary, style = MaterialTheme.typography.bodyMedium, maxLines = 3, overflow = TextOverflow.Ellipsis)
        }
    }
}
```

### 2. Stability Rules (Skippable Composables)

Compose skips a composable when all parameters are **stable** and unchanged. Ensure:

- Use `data class` for state models.
- Annotate genuinely-immutable types with `@Immutable`.
- Use `ImmutableList` / `PersistentList` (kotlinx.collections.immutable), not `List<T>` from code that mutates.
- Avoid `lambda` references that capture unstable values; hoist them to `remember { { ... } }` only when profiling shows a problem.

Verify with the Compose Compiler metrics:

```kotlin
kotlinOptions.freeCompilerArgs += listOf(
    "-P", "plugin:androidx.compose.compiler.plugins.kotlin:reportsDestination=${layout.buildDirectory.get()}/compose-reports",
    "-P", "plugin:androidx.compose.compiler.plugins.kotlin:metricsDestination=${layout.buildDirectory.get()}/compose-metrics",
)
```

Look at the generated `*-classes.txt` — classes should be marked `stable`, composables `skippable` and `restartable`.

### 3. Modifier Discipline

- Always accept `modifier: Modifier = Modifier` and apply it **once**, first.
- Order matters: `Modifier.padding(8.dp).background(Color.Red)` differs from the reverse.
- Extract reusable modifier chains into extension functions: `Modifier.cardSurface()`.

### 4. Lists

```kotlin
LazyColumn(
    contentPadding = PaddingValues(vertical = 8.dp),
    verticalArrangement = Arrangement.spacedBy(8.dp),
) {
    items(items = articles, key = { it.id }, contentType = { "article" }) { a ->
        ArticleCard(a, onClick = onOpen)
    }
}
```

Always supply `key =` for non-trivial lists — it's how Compose preserves state and animations across data changes.

### 5. Material 3 Theming

```kotlin
@Composable
fun AppTheme(darkTheme: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
    val ctx = LocalContext.current
    val dynamic = Build.VERSION.SDK_INT >= Build.VERSION_CODES.S
    val colors = when {
        dynamic && darkTheme -> dynamicDarkColorScheme(ctx)
        dynamic              -> dynamicLightColorScheme(ctx)
        darkTheme            -> DarkColors
        else                 -> LightColors
    }
    MaterialTheme(colorScheme = colors, typography = AppTypography, shapes = AppShapes, content = content)
}

private val LightColors = lightColorScheme(primary = Color(0xFF006D3B), onPrimary = Color.White, /* ... */)
private val DarkColors  = darkColorScheme(primary = Color(0xFF6DDB9A), onPrimary = Color(0xFF003919), /* ... */)
```

### 6. Side Effects

| API | When to use |
|---|---|
| `LaunchedEffect(key)` | Run a coroutine tied to composition lifetime for `key`. |
| `DisposableEffect(key)` | Subscribe on enter, clean up on leave. |
| `SideEffect` | Publish Compose state to non-Compose code after every recomposition. |
| `rememberUpdatedState(value)` | Access latest value inside a long-lived effect without restarting it. |

```kotlin
LaunchedEffect(userId) {
    presenceRepo.start(userId)
}
DisposableEffect(lifecycleOwner) {
    val obs = LifecycleEventObserver { _, e -> if (e == Lifecycle.Event.ON_RESUME) vm.refresh() }
    lifecycleOwner.lifecycle.addObserver(obs)
    onDispose { lifecycleOwner.lifecycle.removeObserver(obs) }
}
```

### 7. Previews

```kotlin
@Preview(name = "Light"); @Preview(name = "Dark", uiMode = UI_MODE_NIGHT_YES)
@Composable private fun ArticleCardPreview() = AppTheme {
    ArticleCard(Article(id = "1", title = "Hello", summary = "Kotlin on Android", /*...*/))
}
```

Use `@PreviewParameter` with a `PreviewParameterProvider` to cover multiple states (loading / error / empty / loaded).

## Checklist
- [ ] Every composable takes `modifier: Modifier = Modifier` as its first non-data parameter.
- [ ] All list `items` calls pass a stable `key`.
- [ ] Compose compiler reports show all screen composables as `skippable` and `restartable`.
- [ ] `MaterialTheme` is applied at the root through an `AppTheme` wrapper.
- [ ] No business logic lives inside composable bodies — only state, layout, and event wiring.
- [ ] Each screen has light + dark previews.
