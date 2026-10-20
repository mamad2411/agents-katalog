---
name: build-native-mobile-ui
description: Builds native mobile UI in SwiftUI (iOS) and Jetpack Compose (Android) — declarative layout (List/LazyVStack vs Scaffold/LazyColumn), unidirectional state with hoisting (@Observable vs ViewModel/StateFlow), typed navigation stacks with deep links, adaptive sizing (size classes/WindowSizeClass), light/dark theming via semantic tokens, lifecycle-correct side effects, recomposition control, and VoiceOver/TalkBack accessibility.
when_to_use: Implementing or reviewing a native iOS (SwiftUI) or Android (Jetpack Compose) screen/component — lists, forms, custom layouts, state hoisting, typed navigation, dark mode/Dynamic Type, adaptive phone/tablet/foldable, recomposition jank. Distinct from scaffold-cross-platform-app (React Native/Flutter, not native Swift/Kotlin), build-react-component (web/React), and audit-accessibility-wcag (web WCAG audit).
---

## When to Use

Reach for this skill when building or reviewing a **native** iOS/Android screen in a declarative UI framework (SwiftUI or Jetpack Compose, i.e. Swift/Kotlin — not React Native or Flutter):

- "Build a SwiftUI/Compose list-detail screen with pull-to-refresh"
- "Hoist this view state — the toggle should be controlled by the parent"
- "Add a NavigationStack / Compose Navigation route with a deep link"
- "Make this adapt to iPad / foldable / landscape (two-pane on wide)"
- "Support dark mode + Dynamic Type without truncation"
- "VoiceOver reads this button wrong / TalkBack skips the row"
- "This list janks / recomposes the whole screen on every keystroke"

NOT this skill:
- Cross-platform UI in React Native or Flutter (JSX/Dart, Expo Router, Riverpod/Bloc) → scaffold-cross-platform-app (this skill is native Swift/Kotlin only)
- Web/React components (JSX, hooks, DOM) → build-react-component
- CSS/Tailwind breakpoints and responsive web layout → style-responsive-tailwind
- Auditing a web page against WCAG success criteria → audit-accessibility-wcag
- Server cache, fetching, optimistic mutation, query invalidation → manage-client-server-state (this skill owns *UI* state, not network state)
- Architecting the token tiers/themes/multi-platform export pipeline → design-token-system (this skill *consumes* tokens in a screen, doesn't design the system)
- Converting a Figma/design spec into pixel-faithful code → implement-from-design (use this skill for the framework idioms once you have the spec)
- The server send path, payload schema, or token registration for push → implement-push-notifications (this skill owns the in-app deep-link router push taps land in)
- Code signing, build lanes, store upload, phased rollout → ship-mobile-app-store-release
- Profiling/fixing web load metrics (LCP/CLS) → optimize-core-web-vitals

## Steps

1. **Pick the container primitive by data shape — never default to a plain stack for collections.** Lazy containers virtualize; eager ones build every child up front and jank past ~50 rows.

   | Need | SwiftUI | Compose |
   |---|---|---|
   | Long/unbounded scrolling list | `List` (free separators, swipe, refresh) or `LazyVStack` in `ScrollView` | `LazyColumn` (with `key = { it.id }`) |
   | Small fixed group (≤ ~20, all visible) | `VStack`/`Form`/`Section` | `Column` |
   | Screen chrome (top bar, FAB, snackbar, insets) | `NavigationStack` + `.toolbar` | `Scaffold(topBar, floatingActionButton, snackbarHost)` |
   | Grid | `LazyVGrid(columns:)` | `LazyVerticalGrid(columns = GridCells.Adaptive(160.dp))` |
   | Overlap / z-stack | `ZStack` | `Box` |

   **Always set stable item identity** (`List(items, id: \.id)` / `items(list, key = { it.id })`) — without it, scroll position and animations break on reorder.

2. **One source of truth, hoisted up; flow data down, events up.** A child that owns the state it renders is unreusable and untestable. Make leaf views *stateless* (value + callback); keep state at the lowest common owner.

   SwiftUI — child takes `Binding`, owns nothing:
   ```swift
   struct ToggleRow: View {            // stateless leaf
       let title: String
       @Binding var isOn: Bool
       var body: some View { Toggle(title, isOn: $isOn) }
   }
   // parent owns it:
   @State private var pushEnabled = false
   ToggleRow(title: "Push", isOn: $pushEnabled)
   ```
   Compose — hoist with `value` + `onValueChange`, never an internal `remember` for controlled state:
   ```kotlin
   @Composable fun ToggleRow(title: String, checked: Boolean, onChecked: (Boolean) -> Unit) {
       Row { Text(title); Switch(checked = checked, onCheckedChange = onChecked) }   // stateless
   }
   ```

   | Concern | SwiftUI | Compose |
   |---|---|---|
   | Local ephemeral UI state | `@State` (private) | `var x by remember { mutableStateOf(...) }` |
   | Owned by parent | `@Binding` | `value` + `onValueChange` lambda |
   | Screen/business state, survives config change | `@Observable` class (`@State` at owner) | `ViewModel` + `StateFlow` → `collectAsStateWithLifecycle()` |
   | Survive process death | `@SceneStorage` / `@AppStorage` | `SavedStateHandle` / `rememberSaveable` |
   | DI'd cross-cutting | `@Environment` | `CompositionLocal` / hilt-injected VM |

   Default: screen state lives in `@Observable` (iOS 17+) / `ViewModel`; the view is a pure function of it. Expose **immutable** state out (`val uiState: StateFlow<UiState>`), accept intents in (`fun onIntent(...)`).

3. **Type your navigation — no stringly-typed routes for in-app pushes.** Drive the stack from a state-bound path so back/deep-link/restore are deterministic.

   SwiftUI:
   ```swift
   @State private var path = NavigationPath()
   NavigationStack(path: $path) {
       List(items) { NavigationLink("\($0.name)", value: $0) }   // value, not destination view
           .navigationDestination(for: Item.self) { ItemDetail(item: $0) }
   }
   // deep link: path.append(item)  — or .onOpenURL { url in route(url, &path) }
   ```
   Compose (type-safe routes, nav 2.8+ with `@Serializable` objects):
   ```kotlin
   @Serializable data class ItemDetail(val id: String)
   NavHost(nav, startDestination = ItemList) {
       composable<ItemList> { ItemListScreen(onOpen = { nav.navigate(ItemDetail(it.id)) }) }
       composable<ItemDetail>(deepLinks = listOf(navDeepLink<ItemDetail>(basePath = "app://item"))) {
           ItemDetailScreen(it.toRoute<ItemDetail>().id)
       }
   }
   ```
   Rules: each tab gets its **own** back stack; restore a saved stack on tab reselect (don't reset to root); a deep link must rebuild the parent stack so Back has somewhere to go.

4. **Layout for variable size from the start — respect insets, scale with the user's type setting, branch on width class.** Hardcoded heights and a single phone layout break on Dynamic Type / iPad / foldable.
   - **Safe area / insets:** never hardcode status-bar or notch padding. SwiftUI honors safe area by default — only push to edges with `.ignoresSafeArea()` deliberately and pad content back. Compose: `Scaffold` gives `innerPadding` — apply it; for keyboard use `Modifier.imePadding()` / `windowInsetsPadding(...)`.
   - **Dynamic Type / font scale:** use semantic styles (`.font(.body)` / `MaterialTheme.typography.bodyLarge`), not fixed `pt`/`sp`. Let text wrap; cap with `.lineLimit` + `.minimumScaleFactor(0.8)` only when a hard ceiling exists. Verify at the largest accessibility size.
   - **Adaptive width:** branch on the class, not a raw `375`-px guess. iPad/landscape and wide foldables → two-pane.

     | | iOS | Android |
     |---|---|---|
     | Read width class | `@Environment(\.horizontalSizeClass)` (`.compact`/`.regular`) | `calculateWindowSizeClass(activity).widthSizeClass` (`Compact`/`Medium`/`Expanded`) |
     | List+detail that adapts | `NavigationSplitView` | two-pane when `Expanded`, single `NavHost` when `Compact` |
     | Breakpoints | compact = phone portrait; regular = iPad/landscape | Compact <600dp · Medium 600–840dp · Expanded ≥840dp |

5. **Theme through tokens, not literals — and support dark by deriving, not duplicating.** Reference semantic roles so dark mode is automatic.
   - iOS: use system semantic colors (`Color(.systemBackground)`, `.primary`, `.secondary`, `Color("Brand")` from an Asset Catalog with a Dark variant) — they flip with `@Environment(\.colorScheme)`. Icons: SF Symbols (`Image(systemName: "trash")`) so they match weight/scale.
   - Android: define a `ColorScheme` via Material 3 `lightColorScheme()`/`darkColorScheme()` (or `dynamicColorScheme(context)` for Material You on API 31+), select by `isSystemInDarkTheme()`, expose through `MaterialTheme`. Never read `Color(0xFF...)` literals inside a composable.
   - Never gate logic on the literal color; gate on the token/role. One token table, two schemes derived from it.

6. **Accessibility is a build requirement, not a pass.** Every interactive element needs a label + role; targets ≥ 44pt (iOS HIG) / ≥ 48dp (Material). Decorative images get *no* label.
   - iOS: `.accessibilityLabel("Delete")`, `.accessibilityAddTraits(.isButton)`, `.accessibilityHidden(true)` for decoration, group a row with `.accessibilityElement(children: .combine)` so VoiceOver reads it as one unit.
   - Compose: `Modifier.semantics { contentDescription = "Delete" }` (or the param on `Icon`), `contentDescription = null` for decorative `Image`, `Modifier.clearAndSetSemantics {}` to merge a row, `Role.Button`/`Role.Checkbox` via `Modifier.semantics { role = ... }`.
   - Don't override the framework focus order unless reading order is genuinely wrong; tappable area must equal visible-or-larger, never smaller than the touch-target minimum.

7. **Lifecycle & side effects: run effects in the right hook, keyed correctly, and stop fighting recomposition.** A composable body / `body` runs *many* times — never do I/O, start timers, or mutate state there.
   - iOS: `.task { await load() }` (auto-cancels on disappear) for async load; `.onAppear`/`.onDisappear` for non-async; `.onChange(of: query) { … }` for reactions. Don't kick network off in `body`.
   - Compose: `LaunchedEffect(key)` for suspend work on enter / when `key` changes; `rememberCoroutineScope()` for event-triggered launches; `DisposableEffect` to register+`onDispose` cleanup; `derivedStateOf` to avoid recomposing on every upstream tick; `produceState` to bridge a callback into state. The **key** must include every input the effect depends on, or it goes stale.
   - Stop needless recomposition: read VM state with `collectAsStateWithLifecycle()`; pass stable/`@Immutable` types and lambdas; hoist heavy reads out of `items{}`; defer rapidly-changing reads (scroll offset) with a lambda (`Modifier.offset { … }`) so only the layout phase reruns. SwiftUI equivalent: split big views so a small `@State` change invalidates a small subtree, give `ForEach` stable ids, mark expensive subviews `Equatable`.

8. **Verify on a real simulator/emulator with previews + the accessibility inspectors** (see Verify) before declaring done — previews catch layout, the device catches lifecycle and gesture bugs previews can't.

## Common Errors

- **`VStack`/`Column` for a long list.** Builds every child eagerly → jank and memory blowup. Use `LazyVStack`/`List` / `LazyColumn`.
- **No stable item key.** `LazyColumn` without `key=` (or `List` keyed by index) reorders/animates wrong and loses scroll on insert. Key by a stable id.
- **State owned in the leaf you want to reuse.** Child `@State`/internal `remember` for what the parent should control → can't lift, can't test, drifts out of sync. Hoist: `Binding` / `value`+`onValueChange`.
- **`remember { mutableStateOf(...) }` for screen state.** Lost on rotation/process death; doesn't survive nav. Put it in a `ViewModel` (or `rememberSaveable` for trivial UI bits).
- **Collecting flow with `.collectAsState()`** instead of `collectAsStateWithLifecycle()` — keeps collecting in the background, wasting work and risking stale UI. Use the lifecycle-aware one.
- **Side effect in `body`/composable body.** Network or `mutableStateOf` write during composition → infinite recomposition or duplicate loads. Move to `.task`/`LaunchedEffect`.
- **Wrong/empty `LaunchedEffect` key.** `LaunchedEffect(Unit)` that reads `id` never reloads when `id` changes; over-keyed restarts constantly. Key on exactly the inputs the effect uses.
- **Stringly-typed nav routes** (`navigate("detail/$id")` with manual parsing) — typos compile, args lose types, deep links break silently. Use type-safe routes / `value:` + `navigationDestination(for:)`.
- **Single shared back stack across tabs.** Switching tabs nukes the other tab's history. Give each tab its own `NavHost`/stack and save/restore it.
- **Hardcoded padding for the notch/status bar / ignoring `innerPadding`.** Content slides under the bar or the keyboard. Honor safe area / apply `Scaffold` `innerPadding` + `imePadding()`.
- **Fixed font sizes / `.lineLimit(1)` everywhere.** Truncates at large Dynamic Type, fails accessibility. Semantic text styles; allow wrap; scale-factor only as a last resort.
- **Hardcoded hex colors in views.** Dark mode shows white-on-white. Use semantic colors / `MaterialTheme.colorScheme` tokens with light+dark schemes.
- **Touch target smaller than the icon's frame.** A 24pt icon with no padding is a 24pt target. Pad to ≥44pt/48dp.
- **`contentDescription`/label missing on icon buttons, or set on decorative images.** Screen reader says "button" with no name, or narrates clutter. Label actionable elements; `null`/`.accessibilityHidden(true)` decoration.
- **Reading rapidly-changing state (scroll offset, animation) at composition scope.** Recomposes the whole subtree every frame. Read it in a lambda (`Modifier.offset { … }`) / use `derivedStateOf`.

## Verify

1. **Builds & previews render:** `xcodebuild -scheme <S> -destination 'platform=iOS Simulator,name=iPhone 15' build` / `./gradlew assembleDebug`. SwiftUI `#Preview` and Compose `@Preview` show light **and** dark variants without crashing.
2. **List performance:** scroll a 500+ item list on device — no dropped frames; inserting/removing keeps scroll position. (Compose: Layout Inspector → recomposition counts stay flat per row while scrolling; a row recomposing on unrelated state changes is a fail.)
3. **State hoisting holds:** toggle the child's control, confirm the parent's single source of truth updates and no duplicate/stale copy exists; rotate the device (or trigger config change) — state survives (VM/`rememberSaveable`), is not reset.
4. **Navigation & deep link:** push → Back returns correctly; cold-launch the deep link (`xcrun simctl openurl booted app://item/42` / `adb shell am start -a android.intent.action.VIEW -d "app://item/42"`) lands on the right screen with a sane back stack; switch tabs and return — the other tab's stack is preserved.
5. **Adaptivity:** run iPhone portrait, iPhone landscape, and iPad / a foldable (or resizable emulator dragged across 600dp and 840dp) — layout switches single↔two-pane at the size-class boundary, nothing clips or overlaps.
6. **Dynamic Type / dark:** set the largest accessibility text size and dark mode (iOS Settings → Accessibility → Larger Text; emulator font scale 1.3+ / Dark theme) — no truncation, no white-on-white, all controls reachable.
7. **Screen reader:** enable VoiceOver (Accessibility Inspector → audit) / TalkBack — swipe through: every actionable element announces a name + role, decorative content is skipped, focus order is logical, and no target is below 44pt/48dp (Xcode Accessibility Inspector audit / Compose `testTagsAsResourceId` + Accessibility Scanner report zero issues).

Done = the screen builds, previews render light+dark, a 500+ row list scrolls without dropped frames and without per-row recomposition on unrelated changes, state is hoisted and survives a config change, typed navigation + cold deep link land correctly with per-tab back stacks preserved, layout adapts across the size-class boundaries, and the accessibility inspector/scanner reports zero issues at the largest Dynamic Type / font scale.
