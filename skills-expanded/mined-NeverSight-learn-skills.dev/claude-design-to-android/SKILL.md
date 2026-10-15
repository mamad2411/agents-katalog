---
name: claude-design-to-android
description: >
  Convert Claude Code Design handoff bundles (zip files containing JSX/HTML/CSS prototypes)
  into pixel-accurate Android Kotlin + Jetpack Compose code. Use this skill whenever the user
  uploads a zip file from Claude Design (claude.ai/design), a "handoff bundle", or any
  design prototype exported from Claude's design tool that they want implemented as an
  Android app. Also triggers when the user says "convert this design to Android",
  "implement this design in Kotlin", "build this app from the design", "make this into
  a Compose app", "turn this mockup into Android code", or references a design zip and
  wants Kotlin/Android output. This skill handles the full pipeline: unzipping, discovering
  design tokens and component hierarchies from ANY JSX/HTML/CSS source structure, mapping
  them to Compose equivalents, and generating a complete Android project structure with
  screens, navigation, theme, and reusable components — matching the original design as
  closely as Compose allows. Works with any Claude Design export regardless of file naming,
  folder structure, or token format.
trigger:
  keywords: ["design bundle", ".zip", "handoff bundle", "JSX", "tokens.css", ".design-canvas", "Figma export", "claude.ai/design", "design zip"]
  when: A ZIP file from Claude Design or a JSX/HTML/CSS design bundle is attached and needs to be converted to Kotlin Compose screens
---

# Claude Design → Android Converter

Converts a Claude Code Design handoff bundle into Android/Kotlin + Jetpack Compose code that closely matches the original HTML/CSS/JSX prototypes.

This skill is designed to be **universal** — it does not hard-code file names, folder structures, or token formats. Every bundle is different, so the workflow is to *discover* what's in the bundle and adapt.

> **Why "closely matches" rather than "pixel-perfect"?** Web and Android have genuine rendering differences — system fonts differ, shadows render differently, web `box-shadow` has no exact Compose equivalent, and Android system insets affect layout. The goal is faithful translation, not impossible parity. Be honest with the user about what carries over exactly and what's an approximation.

---

## Phase 0 — Extract & Discover

### Step 1: Extract

Don't hard-code the zip filename — discover it. The lookup chain handles both GitHub Actions CI and the Claude.ai sandbox:

```bash
ZIP_FILE=""
# 1. CI / GitHub Actions — workflow pre-extracts into $DESIGN_BUNDLE_DIR
if [ -d "${DESIGN_BUNDLE_DIR:-/tmp/issue-attachments}" ]; then
  ZIP_FILE=$(ls "${DESIGN_BUNDLE_DIR:-/tmp/issue-attachments}"/*.zip 2>/dev/null | head -1)
fi
# 2. Claude.ai sandbox (legacy)
if [ -z "$ZIP_FILE" ]; then
  ZIP_FILE=$(ls /mnt/user-data/uploads/*.zip 2>/dev/null | head -1)
fi
if [ -z "$ZIP_FILE" ]; then
  echo "No design zip found. Looked in \$DESIGN_BUNDLE_DIR, /tmp/issue-attachments, /mnt/user-data/uploads."
  exit 1
fi

# Skip extraction if the workflow already unzipped it
STEM="$(basename "$ZIP_FILE" .zip)"
if [ -n "${DESIGN_BUNDLE_DIR:-}" ] && [ -d "$DESIGN_BUNDLE_DIR/$STEM" ]; then
  BUNDLE_DIR="$DESIGN_BUNDLE_DIR/$STEM"
else
  BUNDLE_DIR=/tmp/design-bundle
  mkdir -p "$BUNDLE_DIR"
  unzip -o "$ZIP_FILE" -d "$BUNDLE_DIR"
fi
echo "Bundle dir: $BUNDLE_DIR"
```

### Step 2: Survey the structure

```bash
find "$BUNDLE_DIR" -type f | head -50
```

Claude Design bundles vary widely. They may have nested folders or be flat. Files may be named anything. The reliable signal is that the design lives in `.jsx`, `.html`, and/or `.css` files.

### Step 3: Classify every file

Scan each file and classify it. The categories below are guidance, not rigid rules — if a file mixes roles (e.g. tokens + components), treat it as both.

| Role | How to identify | What to extract |
|---|---|---|
| **Design tokens** | Color/spacing definitions — look for: `const T = {`, `const COLORS =`, `:root {`, CSS custom properties (`--var-name:`), or any object/file with bulk color/spacing/shadow values | Colors, typography, shadows, radii, spacing, gradients |
| **Shared components** | Reusable UI functions used across screens — icon systems (`const ICONS =`, inline SVGs), button components, navigation bars, cards, input fields, list items | Reusable Composables |
| **Screen files** | Functions that render a full phone-sized frame — usually named like `S01Name`, `NameScreen`, `NameView`, `NamePage`, with navigation callbacks | One Composable per screen function |
| **App/Router** | Navigation/routing logic — screen switching via state, route definitions, tab configuration, `initialScreen`, conditional rendering | Navigation graph structure |
| **Design canvas** | `design-canvas.jsx` or similar — the Figma-like canvas wrapper | Skip — it's just the preview wrapper |
| **State file** | `.design-canvas.state.json` — screen labels and sections | Screen groupings for folder organization |
| **README / chats** | `README.md`, `chats/` directory | User intent and design decisions |
| **Device frame** | Phone chrome (status bar, nav bar as device decoration) | Skip — Android system handles this |
| **Referenced assets** ⭐ | Image files actually used inside the design — usually in folders named `assets/`, `images/`, `media/`, `public/`, or referenced from JSX via `src="…"`, `backgroundImage: url(…)`, or `<img>` tags. Includes logos, photos, illustrations, splash images, custom icons that aren't inline SVG | Copy into the Android project's `res/drawable/` — see Phase 1.5 |
| **State screenshots** | PNG/JPG files in folders named `screenshots/`, `previews/`, or `states/`, OR named after screens (`s01-welcome.png`, `home-light.png`) and **not referenced** from any JSX file | Skip — these are visual cross-checks only |
| **Standalone HTML** | Large `.html` files (often 1MB+) with "Standalone" in name | Skip — these are self-contained previews; the source is in the JSX |

> **The screenshot vs asset distinction matters.** Older versions of this skill treated every `.png`/`.jpg` as "visual reference only" and skipped them all — which silently dropped real logos and photos that the design depended on. The way to tell them apart is *whether the JSX actually references the file*. Run `grep -r "filename.png" /home/claude/design-bundle/` for a few candidate files to find out. Files referenced from JSX → ship them to Android. Files only sitting in `screenshots/` or named after a state with no JSX reference → preview captures, skip them.

### Step 4: Read files in priority order

1. **Design tokens first** — understand the color/type system before reading screens, otherwise you'll be guessing what `T.primary` resolves to.
2. **Shared components** — understand the building blocks before reading screens that compose them.
3. **All screen files** — read every one, completely. Inline styles often contain values that aren't in the token file.
4. **App/Router** — for navigation structure.
5. **State file / README** — for context on grouping and intent.

> **Read source code, not screenshots.** Every dimension, color, font, spacing, radius, and shadow is in the code. Screenshots are pixel-quantized and lossy — the JSX has the canonical values. The screenshots are useful only as visual cross-checks at the end.

---

## Phase 1 — Extract Design System

After reading the token file(s), build a complete design system. See `references/design-token-mapping.md` for full conversion tables.

### 1.1 Color Tokens

Find all color definitions in the bundle. They appear in many forms:

```
'rgb(37,100,207)'           → Color(0xFF2564CF)
'rgba(15,15,26,0.06)'       → Color(0xFF0F0F1A).copy(alpha = 0.06f)
'#0066FF'                   → Color(0xFF0066FF)
'#131111'                   → Color(0xFF131111)
rgba(255,255,255,0.10)      → Color.White.copy(alpha = 0.10f)
var(--brand-blue)           → reference to BrandBlue constant
```

For deterministic conversion of long color lists, run the bundled helper:

```bash
python3 .claude/skills/claude-design-to-android/scripts/convert_colors.py "$BUNDLE_DIR"
```

It scans the bundle for color literals, deduplicates them, and emits a draft `Color.kt`. Review the names — auto-generated names can be ugly — but the hex values will be correct.

Output: `Color.kt` with every color from the design. Use the original token names from the design (camelCase).

### 1.2 Typography

Scan screens for all unique `fontSize` + `fontWeight` + `letterSpacing` combinations. Also look for CSS classes (`.gx-h1`, `.gx-body`) or JS objects defining typography styles.

Output: `Type.kt` with named `TextStyle` constants.

### 1.3 Shadows, Shapes, Spacing

- Map each unique `boxShadow` → Compose `elevation` or `shadow()` modifier (CSS shadows don't map exactly — see the reference for guidance on choosing elevation values that approximate the visual weight).
- Map each unique `borderRadius` → `RoundedCornerShape(N.dp)`.
- Extract recurring `padding`, `gap`, `margin` values → spacing constants.
- Look for CSS spacing scales (`--space-1: 2px`, etc.) or JS spacing objects.

Output: `Shape.kt`, `Spacing.kt`.

### 1.4 Gradients

Find all `linear-gradient`, `radial-gradient` definitions → `Brush` objects. Look for CSS variables (`--grad-premium: linear-gradient(...)`) and inline gradient styles.

Output: include in `Color.kt` or a separate `Gradient.kt`.

### 1.5 Dark mode

If the design has a `dark` prop on screens or a `darkMode` toggle, the design system needs **two color sets**, not just one. Structure tokens as:

```kotlin
private val LightColors = lightColorScheme(primary = Primary, background = White, ...)
private val DarkColors  = darkColorScheme(primary = Primary, background = Ink, ...)

@Composable
fun AppTheme(darkTheme: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
    val colors = if (darkTheme) DarkColors else LightColors
    MaterialTheme(colorScheme = colors, typography = AppTypography, content = content)
}
```

For inline conditionals like `dark ? "#fff" : "#0F1115"` in the design, lift these into the color scheme rather than scattering ternaries through the Composables.

---

## Phase 1.5 — Extract Assets

Claude Design's handoff bundle ships referenced assets alongside the JSX/CSS — logos, photos, illustrations, splash images, and any custom icons that aren't inline SVG. They need to be copied into the Android project's `res/drawable*/` folders and made accessible to Compose. This phase is what older versions of the skill missed: every `.png`/`.jpg` was being silently skipped.

See `references/asset-mapping.md` for the detailed rules on naming, folder choice, SVG conversion, and Compose usage. The summary:

### Step 1: Run the asset extraction script

```bash
# Resolve the output res dir: in CI write directly into the repo; in sandbox use the staging area
if [ "${GITHUB_ACTIONS:-}" = "true" ]; then
  OUTPUT_RES="app/src/main/res"
else
  OUTPUT_RES="/home/claude/android-output/res"
fi
python3 .claude/skills/claude-design-to-android/scripts/extract_assets.py "$BUNDLE_DIR" \
    --output-dir "$OUTPUT_RES"
```

The script:
- Walks the bundle for image files
- Greps every JSX/HTML/CSS file for image references
- Cross-references the two: assets that are referenced get copied; orphans are reported but not copied (run with `--include-unreferenced` to override)
- Skips anything in folders named `screenshots/`, `previews/`, `states/`, `captures/` — those are Claude Design's own preview captures, not real assets
- Renames each file to a valid Android resource name (lowercase, `[a-z0-9_]`, can't start with digit, no `@2x` density markers)
- Routes bitmaps to `res/drawable-nodpi/` (so Android doesn't auto-rescale them) and SVGs to `res/drawable/`
- Generates `assets-manifest.md` with origin → destination mapping and Compose usage snippets for every asset

If you want to preview without copying, pass `--check` first.

### Step 2: Convert SVGs (manual step)

The script copies SVGs as `.svg` files but flags them — Android doesn't render SVG natively at the resource level. Two options:

- **Tell the user** to import each one via Android Studio's *File → New → Vector Asset → Local file*. This is the most reliable path.
- **For simple SVGs** (single path, basic colors, no filters/masks), convert manually to vector drawable XML. See `references/asset-mapping.md` for the translation pattern.

The Compose code references the eventual `.xml` filename, so the user just needs to drop the converted XML into `res/drawable/` with the same stem name.

### Step 3: Wire the manifest into Phase 3

When generating screen Composables in Phase 3, use the manifest's "Compose usage" column verbatim — it has the exact `painterResource(R.drawable.foo)` calls already formed. Look for places in the source JSX where assets are referenced (`<img src="…"/>`, `style={{ background: 'url(…)' }}`) and substitute the corresponding Compose snippet.

### Step 4: Handle placeholder/remote images

Some designs use Lorem-Picsum-style URLs or named placeholders (`profile-photo`, `user-avatar`) that aren't shipped as real assets — they represent backend content. Don't try to bundle these. Generate a placeholder `Box` in Compose and tell the user to wire Coil's `AsyncImage` later. See `references/asset-mapping.md` for the pattern.

---

## Phase 2 — Map Components

Scan files for reusable functions — any function called by multiple screens.

### Component vs screen

- **Component**: called inside other functions. Renders a UI fragment (button, card, row, bar, icon).
- **Screen**: top-level. Renders a full phone frame. Has navigation callbacks (`onClose`, `onBack`, `onNav`).

### Universal Layout Translation

| Web Pattern | Compose |
|---|---|
| `display: 'flex', flexDirection: 'column'` | `Column` |
| `display: 'flex'` (row) | `Row` |
| `position: 'absolute'` | `Box` + `Modifier.offset()` or `Modifier.align()` |
| `gap: N` | `Arrangement.spacedBy(N.dp)` |
| `padding: '0 16px'` | `Modifier.padding(horizontal = 16.dp)` |
| `overflow: 'hidden'` | `Modifier.clip(shape)` |
| `gridTemplateColumns: 'repeat(N, 1fr)'` | `LazyVerticalGrid(GridCells.Fixed(N))` |
| `flex: 1` | `Modifier.weight(1f)` |
| `width: '100%'` | `Modifier.fillMaxWidth()` |
| `inset: 0` | `Modifier.fillMaxSize()` |
| `cursor: 'pointer'` | `Modifier.clickable { }` |
| `transform: 'rotate(Ndeg)'` | `Modifier.rotate(N.f)` |
| `transform: 'scale(N)'` | `Modifier.scale(N.f)` |
| `transform: 'translateX(-50%)'` | `Modifier.offset { IntOffset(-size.width/2, 0) }` |
| `display: '-webkit-box', WebkitLineClamp: N` | `maxLines = N, overflow = TextOverflow.Ellipsis` |
| `zIndex: N` | `Modifier.zIndex(N.f)` |
| `background: 'transparent'` | `Color.Transparent` |
| `minWidth: 0` | `Modifier.widthIn(min = 0.dp)` |

### Universal Component Mapping

| Design Pattern | Compose Equivalent |
|---|---|
| Phone frame wrapper | `Scaffold` or root `Box(Modifier.fillMaxSize())` |
| System status bar (fake) | Skip — handle with edge-to-edge (see below) |
| Home indicator / gesture bar (fake) | Skip — Android system handles this |
| Keyboard (fake) | Skip — Android system handles this |
| Bottom tab bar | `NavigationBar` + `NavigationBarItem` |
| Top app bar | `TopAppBar` or custom `Row` |
| Floating action button | `FloatingActionButton` |
| Primary filled button | Custom `Button` with design colors |
| Ghost/outline button | `OutlinedButton` |
| Bottom sheet overlay | `ModalBottomSheet` |
| Text input | `OutlinedTextField` or custom `Box` |
| Toggle/switch | `Switch` with custom colors |
| Scrim/overlay backdrop | `Box(Modifier.fillMaxSize().background(scrimColor))` |
| Scrollable content | `LazyColumn` or `Column(Modifier.verticalScroll(...))` |
| Horizontal scroll | `LazyRow` or `Row(Modifier.horizontalScroll(...))` |
| Progress bar | `LinearProgressIndicator` with custom colors |
| Slider | `Slider` with custom colors |
| Chip/pill/tag | Custom `Box` or `SuggestionChip` |
| Avatar/initial circle | `Box(CircleShape)` with text or image |
| Badge/dot | `Box(Modifier.size(N).background(color, CircleShape))` |

### Status bar / edge-to-edge (current API)

Older skill versions used Accompanist's `rememberSystemUiController` — that library is **deprecated**. Use the modern AndroidX edge-to-edge API in `MainActivity`:

```kotlin
// In MainActivity.onCreate, before setContent:
enableEdgeToEdge(
    statusBarStyle = SystemBarStyle.light(
        scrim = android.graphics.Color.TRANSPARENT,
        darkScrim = android.graphics.Color.TRANSPARENT
    )
)
```

Imports: `androidx.activity.enableEdgeToEdge`, `androidx.activity.SystemBarStyle`. This requires `androidx.activity:activity-compose:1.8.0+`.

### Icon Systems

Designs use icons in various formats. Detect whatever is present:

1. **Inline SVG elements** — `<svg>` with paths inline in JSX
2. **Path-data object** — `const ICONS = { name: "M3 6h18..." }`
3. **Icon wrapper component** — `function Icon({ name })` wrapping SVGs
4. **Individual icon functions** — `Ic.menu = (c) => <svg...>`
5. **Any other pattern** — extract the SVG path data however it's stored

For each icon: first check if a Material Icon matches (see `references/icon-mapping.md`). If not, build a custom `ImageVector`. Preserve exact `strokeWidth`, `strokeLinecap`, `strokeLinejoin`.

> **Use `Icons.AutoMirrored.Filled.ArrowBack`, not `Icons.Default.ArrowBack`.** The `Default.ArrowBack` family is deprecated in current Compose Material — it doesn't mirror in RTL locales. The same applies to other directional icons (`ArrowForward`, `Send`, `List`, `KeyboardArrowLeft/Right`).

See `references/component-mapping.md` for detailed Compose code patterns.

---

## Phase 3 — Generate Screens

Each screen function in the bundle becomes one `@Composable` function. Don't skip screens — even ads, paywalls, and placeholders are part of the design and the user expects them implemented.

Screen functions may be named in any convention. The identifying trait: they render a full-screen UI (usually wrapped in a frame component) and have navigation-related callbacks.

### Screen Translation Rules

1. **Read the function thoroughly** — every inline style property matters.
2. **Translate top-down**: outermost container first, then children.
3. **Use the exact values from the source.** `fontSize: 13` → `13.sp`. `padding: 16` → `16.dp`. `borderRadius: 14` → `RoundedCornerShape(14.dp)`. Rounding to "nearest 4dp" or substituting "Material defaults that look similar" is the most common cause of pixel drift complaints — designers chose those values deliberately.
4. **Use the exact colors.** Reference your `Color.kt` constants. Substituting `MaterialTheme.colorScheme.primary` for a brand color named `Primary` will silently break the design when Material's defaults differ.
5. **Font weights**: `400`=Normal, `500`=Medium, `600`=SemiBold, `700`=Bold, `800`=ExtraBold.
6. **Opacity**: `opacity: 0.45` → `.alpha(0.45f)` or `color.copy(alpha = 0.45f)`.
7. **Borders**: `border: '1px solid color'` → `Modifier.border(1.dp, color, shape)`.
8. **Gradients**: `linear-gradient(180deg, A, B)` → `Brush.verticalGradient(listOf(A, B))`.
9. **Text overflow**: `textOverflow: 'ellipsis'` → `maxLines = 1, overflow = TextOverflow.Ellipsis`.
10. **Text transform**: `.toUpperCase()` → `.uppercase()`.
11. **Text decoration**: `textDecoration: 'line-through'` → `textDecoration = TextDecoration.LineThrough`.

### Frame dimensions are reference, not target

The design's `390×844` frame represents iPhone-ish dimensions. Don't hard-code these on Android — Android phones range from ~360dp to 480dp wide, plus tablets and foldables. Use `fillMaxSize()` and let relative spacing (paddings, weights, `Arrangement.spacedBy`) carry the layout. Hard-coded heights are fine for individual elements (buttons, top bars) but not for screen-level containers.

### Handling Dynamic UI Patterns

| JSX Pattern | Compose Translation |
|---|---|
| `dark` prop / parameter | Theme toggle → `isSystemInDarkTheme()` or ViewModel state |
| `React.useState(value)` | `remember { mutableStateOf(value) }` |
| `condition && <Component/>` | `if (condition) { Component() }` |
| `condition ? <A/> : <B/>` | `if (condition) A() else B()` |
| `items.map((item, i) => ...)` | `LazyColumn { items(list) { item -> ... } }` |
| `Array.from({length: N}).map(...)` | `repeat(N) { i -> ... }` |
| `new Set()` / selection tracking | `remember { mutableStateListOf<T>() }` |
| `onClick` handler | `Modifier.clickable { }` or `onClick` parameter |
| Inline ternary colors `dark ? "#fff" : "#000"` | Theme-aware color (push to color scheme, don't ternary inline) |

### Screen Grouping

Group screens into folders based on what's in the bundle:
1. Check `.design-canvas.state.json` for section groupings
2. Check source file names for logical groupings (`screens-main`, `screens-tools`, etc.)
3. Check navigation/router for feature areas
4. Fall back to grouping by user flow: onboarding → main → detail → settings

---

## Phase 4 — Navigation & Architecture

### Discover Navigation

Don't assume any pattern — look for navigation logic in the bundle. Check:
1. Any app/router file — screen switching state, callbacks, conditional rendering
2. Screen callback props — `onNav`, `onBack`, `onClose`, `onOpenX`, `onFab`
3. Tab bar active state — which tab each screen belongs to
4. Sheet/overlay patterns — bottom sheets, modals, scrims

Build `NavGraph.kt` from what you discover, using Jetpack Navigation Compose:

```kotlin
NavHost(navController = navController, startDestination = Routes.Home) {
    composable(Routes.Home) { HomeScreen(onOpenDetail = { id -> navController.navigate("detail/$id") }) }
    composable("detail/{id}") { backStackEntry ->
        DetailScreen(id = backStackEntry.arguments?.getString("id"))
    }
}
```

### ViewModel

Create ViewModels for feature areas with stateful screens. One ViewModel per logical feature group, not per screen.

```kotlin
data class ScreenUiState(
    val isLoading: Boolean = false,
    val data: DataType = defaultValue,
    val error: String? = null
)
```

---

## Phase 5 — Output Structure

### Output target (CI vs sandbox)

**When running under GitHub Actions (`GITHUB_ACTIONS=true`)** — write Compose source DIRECTLY into the repo working tree:

```
app/src/main/java/<package>/ui/theme/
  Color.kt        ← every color from the design
  Type.kt         ← typography styles
  Shape.kt        ← shape definitions
  Spacing.kt      ← spacing/sizing constants
  Theme.kt        ← MaterialTheme wrapper (light + dark)

app/src/main/java/<package>/ui/components/
  [ComponentName].kt   ← one file per reusable component

app/src/main/java/<package>/ui/<feature>/
  [ScreenName].kt      ← one Composable per screen function
  [Feature]ViewModel.kt

app/src/main/java/<package>/navigation/
  Routes.kt
  NavGraph.kt

app/src/main/java/<package>/ui/icons/
  AppIcons.kt          ← custom ImageVector icons (non-Material only)

app/src/main/res/
  drawable/            ← vector drawables (XML)
  drawable-nodpi/      ← bitmap assets at design resolution
```

Derive `<package>` from `app/build.gradle.kts` (`applicationId`). If not found, use `com.example.galleryapp` (this project's existing package).

**When running in the Claude.ai sandbox** — stage to `/home/claude/android-output/` and copy to `/mnt/user-data/outputs/` as before. Structure mirrors the CI tree above but under `android-output/kotlin/` (for `.kt` files) and `android-output/res/`.

### Regardless of target — also produce

```
assets-manifest.md   ← origin → destination mapping for every imported asset
README.md            ← setup notes, dependency list, find-replace package instruction
```
        └── *.png, *.jpg, *.webp ← Logos, photos, illustrations
```

The split into `kotlin/` and `res/` matches Android's source layout. The user copies `kotlin/` into `app/src/main/java/com/yourpkg/` and `res/` into `app/src/main/res/`. The `assets-manifest.md` makes the asset import auditable in one place.

### Package declarations

Use a placeholder package at the top of every file:

```kotlin
package com.example.designapp.theme
```

In the README, tell the user:

> *"All files use `package com.example.designapp.*`. Find-and-replace `com.example.designapp` with your own package name (e.g. `com.acme.taskmaster`). If you have an existing project, also adjust the subfolder structure to match — typically `app/src/main/java/com/yourorg/yourapp/...`."*

If the user provides a `build.gradle` or specifies their package, use that instead.

---

## Phase 6 — Quality Check & Verification

### 6.1 Automated checks (Claude can verify these)

Run these as scripts or counts, not eyeballed:

- [ ] **Color count**: every unique color literal in the bundle has a constant in `Color.kt`. Diff the source colors against `Color.kt` to confirm.
- [ ] **Screen count**: number of `@Composable` screen functions == number of screen functions in the bundle. List both side-by-side.
- [ ] **Icon coverage**: every icon used in the bundle is either a Material Icon import or a custom `ImageVector` in `AppIcons.kt`.
- [ ] **Asset coverage**: every image referenced from JSX/CSS exists in `res/drawable*/` with a valid Android resource name. Run `extract_assets.py` in `--check` mode against the output to verify nothing was dropped.
- [ ] **No deprecated APIs**: grep output for `Icons.Default.ArrowBack`, `rememberSystemUiController`, `Accompanist` — there should be zero matches.
- [ ] **Resource name validity**: every file in `res/drawable*/` matches `^[a-z][a-z0-9_]*\.(xml|png|jpg|jpeg|webp|gif)$`. Capital letters or hyphens will cause Android build errors.
- [ ] **Compilation**: if the user provides an Android project, drop the files in and run `./gradlew compileDebugKotlin`. Surface any errors back to the user immediately. If no project is provided, mention this verification step in the README so the user can do it themselves.

### 6.2 User-review checks (subjective, the user decides)

- Shadows look about right (CSS box-shadow doesn't map exactly to Compose elevation)
- Gradients have correct colors, direction, stops
- Bottom sheets, FAB, tab bar look like the design
- Dark mode reads correctly (if the design has dark mode)
- Interactive states (selection, toggles) feel right

Tell the user: *"I've translated all screens and verified colors/screens/icons match the source. Shadow weight and gradient stops are eyeballed approximations — please flip through and let me know what to adjust."*

---

## How to think about edge cases

- **A token defined but never used.** Include it in `Color.kt` anyway — the user added it for a reason and may need it later.
- **A color used inline that isn't in the token file.** Add it to `Color.kt` with a usage-based name (`ScrimBackground`, `DividerColor`).
- **A screen with no clear feature group.** Put it in `screens/misc/` and ask the user where it belongs.
- **An icon with no Material match and complex paths.** Build the `ImageVector` faithfully; preserve stroke caps/joins. Document any simplifications in a comment.
- **A CSS feature with no Compose equivalent** (e.g. `backdrop-filter: blur()`). Approximate with a translucent overlay and call out the approximation in the README.

---

## Critical translations to get right

These are the failure modes that come up most often. They're framed as guidance because the *why* matters more than the rule.

1. **Every screen function = one Composable.** Skipping screens (even paywalls, onboarding, placeholders) breaks the user's flow expectations. The design includes them on purpose.
2. **Don't substitute Material3 defaults for design tokens.** `Primary` looks "close enough" to `MaterialTheme.colorScheme.primary` until the user puts the app next to the prototype and the brand color is wrong.
3. **Translate absolute positioning carefully.** `position: absolute` with `top/left/right/bottom` maps to `Box` + `Modifier.offset()` or `.align()`. Dropping it and hoping for the best produces stacked layouts that don't match.
4. **Frame dimensions (390×844) are reference, not target.** Use `fillMaxSize()` so the app works on every Android screen size.
5. **Preserve icon stroke widths.** A 1.75dp stroke and a 2dp stroke look noticeably different at icon scale.
6. **Skip system chrome.** Status bar, home indicator, keyboard, device frame in the design are decorative — Android handles all of these via system UI.
7. **Photo/video placeholders should be swappable.** Use a `Box` with the placeholder background that can be replaced with `AsyncImage` later, not a hardcoded gradient.
