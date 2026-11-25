---
name: android-foldables-adaptive-ui
description: |
  Adaptive UI and foldable support patterns for Android/Compose - WindowSizeClass for layout decisions, ListDetailPaneScaffold for two-pane layouts, NavigationSuiteScaffold for adaptive navigation, FoldingFeature detection for hinge and table-top postures, and resizable emulator testing. Use this skill whenever building tablet, foldable, or large-screen layouts, or adapting navigation patterns based on available space. Trigger on phrases like "foldable", "tablet layout", "adaptive UI", "WindowSizeClass", "two-pane", "ListDetailPaneScaffold", "NavigationSuiteScaffold", "navigation rail", or "large screen".
---

# Android Foldables and Adaptive UI

## Core Principles

- Never use hardcoded dp breakpoints. Always use `WindowSizeClass` for layout decisions.
- Navigation chrome (bottom bar, rail, drawer) should adapt to width, not device type.
- Two-pane layouts should degrade gracefully to single-pane on compact screens.
- Foldable postures (table-top, book mode) are additive — they adjust an existing adaptive layout.
- Test on resizable emulator, not just specific device profiles.

---

## Dependencies

```kotlin
// build.gradle.kts (app or feature module)
implementation(libs.androidx.adaptive)
implementation(libs.androidx.adaptive.layout)
implementation(libs.androidx.adaptive.navigation)
implementation(libs.androidx.window)
implementation(libs.androidx.navigation.compose)
```

Version catalog entries:

```toml
[libraries]
androidx-adaptive = { module = "androidx.compose.material3.adaptive:adaptive", version.ref = "adaptiveLayout" }
androidx-adaptive-layout = { module = "androidx.compose.material3.adaptive:adaptive-layout", version.ref = "adaptiveLayout" }
androidx-adaptive-navigation = { module = "androidx.compose.material3.adaptive:adaptive-navigation", version.ref = "adaptiveLayout" }
androidx-window = { module = "androidx.window:window", version.ref = "androidxWindow" }
```

---

## WindowSizeClass

### Obtaining the Class

Obtain `WindowSizeClass` once at the Activity level and propagate it down via `CompositionLocal` or pass it explicitly:

```kotlin
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val windowSizeClass = calculateWindowSizeClass(this)
            AppTheme {
                AppRoot(windowSizeClass = windowSizeClass)
            }
        }
    }
}
```

### The Three Widths

| `WindowWidthSizeClass` | Typical screen | Typical layout |
|---|---|---|
| `Compact` | Phone portrait | Single pane, bottom nav |
| `Medium` | Phone landscape, small tablet, open foldable | Transitional; nav rail |
| `Expanded` | Tablet, large foldable unfolded | Two-pane, nav drawer |

Make all layout decisions relative to the window size class, not raw dp values.

---

## Adaptive Navigation with NavigationSuiteScaffold

`NavigationSuiteScaffold` from the Material3 adaptive library automatically switches between bottom bar, navigation rail, and navigation drawer based on `WindowAdaptiveInfo`:

```kotlin
@Composable
fun AppRoot(windowSizeClass: WindowSizeClass) {
    val navController = rememberNavController()
    val currentDestination by navController
        .currentBackStackEntryAsState()

    NavigationSuiteScaffold(
        navigationSuiteItems = {
            TopLevelDestination.entries.forEach { destination ->
                item(
                    selected = currentDestination?.destination?.route == destination.route,
                    onClick = { navController.navigateTo(destination) },
                    icon = { Icon(destination.icon, contentDescription = destination.label) },
                    label = { Text(destination.label) }
                )
            }
        }
    ) {
        AppNavHost(navController = navController, windowSizeClass = windowSizeClass)
    }
}
```

`NavigationSuiteScaffold` internally reads `WindowAdaptiveInfo` from the local composition. Do not override its layout decisions with manual size checks.

---

## Two-Pane Layout with ListDetailPaneScaffold

Use `ListDetailPaneScaffold` for list-detail navigation patterns:

```kotlin
@Composable
fun NotesListDetailScreen(windowSizeClass: WindowSizeClass) {
    val navigator = rememberListDetailPaneScaffoldNavigator<String>()

    BackHandler(navigator.canNavigateBack()) {
        navigator.navigateBack()
    }

    ListDetailPaneScaffold(
        directive = navigator.scaffoldDirective,
        value = navigator.scaffoldValue,
        listPane = {
            AnimatedPane {
                NoteListPane(
                    onNoteSelected = { noteId ->
                        navigator.navigateTo(ListDetailPaneScaffoldRole.Detail, noteId)
                    }
                )
            }
        },
        detailPane = {
            AnimatedPane {
                val noteId = navigator.currentDestination?.content
                if (noteId != null) {
                    NoteDetailPane(noteId = noteId)
                } else {
                    NoteEmptyDetail()
                }
            }
        }
    )
}
```

On `Compact` screens the scaffold shows one pane at a time with back-stack navigation. On `Expanded` screens both panes are visible simultaneously. This behavior is handled by the scaffold — do not manually toggle pane visibility with `if (isExpanded)` checks.

---

## Handling Foldable Postures with FoldingFeature

`FoldingFeature` describes the physical hinge or fold state. Obtain it from `WindowInfoTracker`:

```kotlin
@Composable
fun rememberFoldingFeature(): FoldingFeature? {
    val context = LocalContext.current
    return WindowInfoTracker.getOrCreate(context)
        .windowLayoutInfo(context as Activity)
        .collectAsStateWithLifecycle(initialValue = null)
        .value
        ?.displayFeatures
        ?.filterIsInstance<FoldingFeature>()
        ?.firstOrNull()
}
```

### Table-Top Mode

Table-top mode is when the fold is horizontal and the device is resting flat:

```kotlin
@Composable
fun CameraScreen() {
    val fold = rememberFoldingFeature()
    val isTableTop = fold != null &&
        fold.state == FoldingFeature.State.HALF_OPENED &&
        fold.orientation == FoldingFeature.Orientation.HORIZONTAL

    if (isTableTop) {
        TableTopCameraLayout()  // viewfinder above fold, controls below fold
    } else {
        StandardCameraLayout()
    }
}
```

### Book Mode

Book mode is when the fold is vertical and the device is held open like a book:

```kotlin
val isBookMode = fold != null &&
    fold.state == FoldingFeature.State.HALF_OPENED &&
    fold.orientation == FoldingFeature.Orientation.VERTICAL
```

### Hinge Bounds

When content must avoid the hinge, use `FoldingFeature.bounds` to calculate safe drawing areas. Do not hardcode hinge width values — they vary by device.

---

## Passing WindowSizeClass Through the Nav Graph

Pass `windowSizeClass` into composables that need it or provide it via `CompositionLocal`:

```kotlin
val LocalWindowSizeClass = compositionLocalOf<WindowSizeClass> {
    error("No WindowSizeClass provided")
}

// In AppRoot:
CompositionLocalProvider(LocalWindowSizeClass provides windowSizeClass) {
    AppNavHost(navController = navController)
}

// In a composable anywhere in the tree:
val windowSizeClass = LocalWindowSizeClass.current
val isCompact = windowSizeClass.widthSizeClass == WindowWidthSizeClass.Compact
```

---

## Responsive Compose Layout Patterns

Use width-class-aware layout switching:

```kotlin
@Composable
fun ProfileScreen(windowSizeClass: WindowSizeClass) {
    when (windowSizeClass.widthSizeClass) {
        WindowWidthSizeClass.Compact -> ProfileSingleColumnLayout()
        WindowWidthSizeClass.Medium -> ProfileTwoColumnLayout()
        WindowWidthSizeClass.Expanded -> ProfileSideBySideLayout()
        else -> ProfileSingleColumnLayout()
    }
}
```

Avoid mixing `BoxWithConstraints` pixel comparisons with `WindowSizeClass` checks for the same decision — pick one source of truth.

---

## Anti-Patterns

- Hardcoding `if (screenWidth > 600.dp)` — brittle, ignores system bar insets, and diverges from system semantics.
- Creating custom NavigationRail/BottomNavigation visibility logic by hand — `NavigationSuiteScaffold` handles this correctly.
- Calling `calculateWindowSizeClass` inside a composable deeper than the Activity root — create it once at the top.
- Showing two panes manually with `Row { if (isTablet) DetailPane() }` instead of `ListDetailPaneScaffold` — loses correct back-stack behavior.
- Ignoring `Medium` — many foldables and landscape phones land here; treat it as a real layout target.

---

## Testing Adaptive UIs

### Resizable Emulator

Use the resizable emulator (API 34+) and resize the window to exercise all three `WindowSizeClass` states without a physical device.

### Compose Preview with WindowSizeClass

```kotlin
@Preview(name = "Compact", widthDp = 360, heightDp = 800)
@Preview(name = "Medium", widthDp = 700, heightDp = 800)
@Preview(name = "Expanded", widthDp = 1200, heightDp = 800)
@Composable
private fun NotesListDetailPreview() {
    AppTheme {
        NotesListDetailScreen(
            windowSizeClass = WindowSizeClass.calculateFromSize(DpSize(360.dp, 800.dp))
        )
    }
}
```

### Robolectric WindowSizeClass Tests

```kotlin
@Test
fun `compact width shows single pane`() {
    val windowSizeClass = WindowSizeClass.calculateFromSize(DpSize(360.dp, 800.dp))
    composeTestRule.setContent {
        NotesListDetailScreen(windowSizeClass = windowSizeClass)
    }
    composeTestRule.onNodeWithTag("detail_pane").assertDoesNotExist()
}

@Test
fun `expanded width shows both panes`() {
    val windowSizeClass = WindowSizeClass.calculateFromSize(DpSize(1200.dp, 800.dp))
    composeTestRule.setContent {
        NotesListDetailScreen(windowSizeClass = windowSizeClass)
    }
    composeTestRule.onNodeWithTag("list_pane").assertIsDisplayed()
    composeTestRule.onNodeWithTag("detail_pane").assertIsDisplayed()
}
```

---

## Checklist: Adaptive UI Feature

- [ ] Obtain `WindowSizeClass` once at Activity root
- [ ] Never use hardcoded dp breakpoints for layout decisions
- [ ] Use `NavigationSuiteScaffold` for adaptive nav chrome
- [ ] Use `ListDetailPaneScaffold` for two-pane list/detail flows
- [ ] Handle `Medium` as a real target, not a fallback
- [ ] Check `FoldingFeature` for hinge-aware layouts where relevant
- [ ] Add multi-size `@Preview` annotations for adaptive composables
- [ ] Test with resizable emulator across all three width classes
