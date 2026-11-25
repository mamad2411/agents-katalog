---
name: views-to-compose
description: Expert guidance on migrating Android Views / XML layouts to Jetpack Compose incrementally, including AndroidView / ComposeView interop, Fragment hosting, and shared ViewModel strategies. Use this when modernizing a legacy codebase.
---

# Migrating Android Views to Jetpack Compose

## Instructions

Rewrites are rarely funded. Plan an **incremental** migration where Views and Compose coexist, then shrink the View surface over time.

### 1. Migration Ladder

1. **Host Compose inside existing XML** using `ComposeView`.
2. **Host Views inside Compose** using `AndroidView` / `AndroidViewBinding`.
3. **Migrate one screen at a time**, swapping the Activity/Fragment content view.
4. **Remove XML** + `data-binding`/`view-binding` once no consumers remain.

Do not attempt step 4 until the screen's ViewModel is already exposing a `StateFlow<UiState>` that Compose can consume.

### 2. Embedding Compose in an XML Layout

```xml
<!-- fragment_profile.xml -->
<androidx.compose.ui.platform.ComposeView
    android:id="@+id/profileHeader"
    android:layout_width="match_parent"
    android:layout_height="wrap_content" />
```

```kotlin
class ProfileFragment : Fragment(R.layout.fragment_profile) {
    private val vm: ProfileViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        val binding = FragmentProfileBinding.bind(view)
        binding.profileHeader.apply {
            setViewCompositionStrategy(ViewCompositionStrategy.DisposeOnViewTreeLifecycleDestroyed)
            setContent {
                AppTheme {
                    val state by vm.state.collectAsStateWithLifecycle()
                    ProfileHeader(state.user)
                }
            }
        }
    }
}
```

Always set an explicit `ViewCompositionStrategy` for Fragments — the default (`DisposeOnDetachedFromWindow`) leaks state on `FragmentManager` back-stack.

### 3. Embedding Views in Compose

```kotlin
@Composable
fun VideoSurface(uri: Uri, modifier: Modifier = Modifier) {
    AndroidView(
        modifier = modifier,
        factory = { ctx -> PlayerView(ctx).apply { useController = true } },
        update  = { view -> view.player?.setMediaItem(MediaItem.fromUri(uri)) },
        onRelease = { view -> view.player?.release() },
    )
}
```

For an existing `<include>`/custom View, wrap with `AndroidViewBinding`:

```kotlin
AndroidViewBinding(LegacyMapViewBinding::inflate) {
    mapView.onCreate(null)
    mapView.getMapAsync { it.moveCamera(CameraUpdateFactory.newLatLng(LatLng(0.0, 0.0))) }
}
```

Note: `AndroidView` is expensive to create — don't put it inside a `LazyColumn` item unless you need to; prefer a pure Compose alternative (e.g., Coil over `ImageView`).

### 4. Sharing State Between Views and Compose

Refactor to a `ViewModel` exposing `StateFlow<UiState>` first. Then Views observe via `repeatOnLifecycle` and Compose via `collectAsStateWithLifecycle()`:

```kotlin
viewLifecycleOwner.lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        vm.state.collect { state -> render(state) }
    }
}
```

Avoid bridging through `LiveData`. Use `.asLiveData()` only for legacy DataBinding expressions that you'll delete soon.

### 5. Navigation Strategy

If you use the **Navigation component** with Fragments, keep it. Each Fragment's `onCreateView` returns a `ComposeView`. Migrate individual fragments to Compose destinations (`composable<Route> { }`) when feasible. You can mix Fragment and Compose destinations in the same `NavHost` via the Navigation-Compose fragment integration, but the end-state is 100% Compose destinations.

### 6. Theming Parity

Derive a `MaterialTheme` from your existing `Theme.App.xml`:

```kotlin
@Composable
fun AppTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = lightColorScheme(
            primary = colorResource(R.color.brand_primary),
            onPrimary = colorResource(R.color.brand_on_primary),
            // ...
        ),
        typography = Typography( /* map res/values/styles.xml here */ ),
        content = content,
    )
}
```

Use `MdcTheme` from `com.google.accompanist:accompanist-themeadapter-material3` as a temporary bridge if you still rely on AppCompat themes.

### 7. Common Traps

- **Hybrid scroll**: do not nest a `RecyclerView` inside a Compose `Column` scroll — pick one owner of scroll. Fix by hoisting to `LazyColumn`.
- **Window insets**: enable `enableEdgeToEdge()` + `WindowCompat.setDecorFitsSystemWindows(window, false)`, then use `Modifier.windowInsetsPadding(...)` in Compose. Remove `fitsSystemWindows` from XML root views of migrated screens.
- **Fragment re-entry**: `ComposeView`s lose state unless you call `setViewCompositionStrategy(DisposeOnViewTreeLifecycleDestroyed)` and use `rememberSaveable`.
- **KAPT → KSP**: during migration, move Room/Hilt to KSP to avoid the KAPT tax slowing down every incremental build.

### 8. Definition of Done (per screen)

1. Screen's Activity/Fragment `setContent { AppTheme { ScreenRoute() } }` (no XML).
2. `ViewModel` exposes a single `StateFlow<UiState>`.
3. XML layout file for the screen is deleted.
4. Any `ViewBinding`/`DataBinding` references to that layout are removed.
5. UI tests are rewritten with `createAndroidComposeRule`.

## Checklist
- [ ] `ComposeView.setViewCompositionStrategy` is configured for every Fragment host.
- [ ] `AndroidView` is used only where a pure-Compose equivalent is unavailable.
- [ ] Shared state flows via a `ViewModel` using `StateFlow`, not `LiveData`.
- [ ] `MaterialTheme` mirrors the legacy XML theme's color and typography tokens.
- [ ] Edge-to-edge insets are handled in Compose, not XML.
- [ ] Each migrated screen deletes its XML and view-binding references.
