---
name: figma-android-xml
description: Generate high-fidelity Android XML layouts from Figma MCP by extracting tokens/resources first, mapping components, then implementing ConstraintLayout and screenshot-diff fixes.
argument-hint: "[figma-frame-url-or-frame-name] [target-layout-or-screen]"
---

# Figma → Android XML High-Fidelity Implementation

Use this skill when the user asks to implement, restore, convert, review, or refine Android **XML View-system** UI from a Figma design, especially when they care about high visual fidelity.

This skill is not a one-shot Figma-to-code generator. It enforces this workflow:

1. Read and normalize the Figma design.
2. Extract Android resources and component mappings.
3. Generate resources first.
4. Generate XML layout second.
5. Add only the minimal Kotlin/ViewBinding code needed.
6. Validate with build/lint when possible.
7. Iterate using screenshot differences.

Do not switch to Jetpack Compose unless the user explicitly asks.

## Core Principles

- Treat Figma as a design specification, not as absolute-positioned code.
- Prefer Android resource references over hardcoded values.
- Prefer `ConstraintLayout` for complex screens and shallow hierarchy.
- Preserve spacing, typography, corner radius, image scale type, component states, and system-bar assumptions.
- Never hide uncertainty. If Figma data, assets, fonts, or states are missing, state the gap and choose the least risky implementation.
- Do not generate a giant final layout before producing the design specification and resource plan.

## Required First Step

Before editing files, inspect the project and the Figma input.

### Project inspection

Check, as available:

- Gradle modules and Android plugin setup.
- Whether the screen uses Activity, Fragment, ViewBinding, DataBinding, or legacy manual binding.
- Existing `res/values/colors.xml`, `dimens.xml`, `styles.xml`, `themes.xml`, `strings.xml`.
- Existing custom widgets, base layouts, adapters, drawable naming conventions, and typography resources.
- ConstraintLayout, RecyclerView, AppCompat, and Material Components availability.
- minSdk, targetSdk, and whether edge-to-edge / WindowInsets handling is already present.

### Figma inspection

Use configured Figma MCP tools when available. Read, if possible:

- design context
- metadata
- variables / styles
- component names and variants
- selected frame screenshot
- asset export information

If Figma MCP is unavailable or incomplete, use any provided screenshot/specs and mark missing values as assumptions. Do not invent exact colors, fonts, or dimensions when they are not available.

## Output Gate 1: Design Spec Report

Before writing code, output a concise implementation report with these sections:

1. **Target screen**
   - Frame name and size
   - Android baseline width assumption, for example 360dp, 375dp, 390dp, 393dp, or project-defined width
   - Whether the Figma frame includes status bar / navigation bar
   - Scroll behavior

2. **Resource tokens**
   - Colors → proposed `@color/...` names
   - Spacing → proposed `@dimen/space_*` names
   - Sizes → heights, widths, icon sizes, image sizes
   - Radius → proposed `@dimen/radius_*` names
   - Typography → text appearances, font family, size, weight, line height, letter spacing
   - Elevation / shadow approximation

3. **Layout structure**
   - Root layout choice
   - Major sections
   - Reusable item layouts
   - RecyclerView / ScrollView / NestedScrollView decisions

4. **Component mapping**
   - Figma Button/Input/Card/TopBar/ListItem/etc. → Android view or custom component
   - States: default, pressed, disabled, selected, error, loading

5. **Assets**
   - Images to export
   - Icons to convert to VectorDrawable
   - Image scale type: `centerCrop`, `fitCenter`, `centerInside`, etc.

6. **Risks / assumptions**
   - Missing fonts
   - Unknown system bars
   - Unknown responsive behavior
   - Missing states
   - Ambiguous image crop or shadow

Only after this report should implementation begin.

## Implementation Order

### Phase 1: Resources first

Create or update resources before page XML:

- `res/values/colors.xml`
- `res/values/dimens.xml`
- `res/values/styles.xml`
- `res/values/strings.xml` when static strings are needed
- `res/drawable/bg_*.xml` shape drawables
- `res/drawable/selector_*.xml` state selectors
- `res/drawable/ic_*.xml` vector drawables when icons are available

Rules:

- All colors must be referenced through `@color/...`.
- All layout dimensions, margins, paddings, icon sizes, corner radii, and text sizes must be referenced through `@dimen/...`, unless the project convention intentionally keeps common values inline.
- Use clear token names, not Figma layer names.
- Reuse existing resources if semantically equivalent.
- Do not duplicate near-identical colors or dimens without explaining why.

Recommended naming:

```xml
<color name="color_bg_page">#FFFFFF</color>
<color name="color_text_primary">#111827</color>
<color name="color_text_secondary">#6B7280</color>
<color name="color_brand_primary">#2563EB</color>
```

```xml
<dimen name="space_4">4dp</dimen>
<dimen name="space_8">8dp</dimen>
<dimen name="space_12">12dp</dimen>
<dimen name="space_16">16dp</dimen>
<dimen name="radius_12">12dp</dimen>
<dimen name="height_button_48">48dp</dimen>
<dimen name="text_size_16">16sp</dimen>
<dimen name="line_height_24">24sp</dimen>
```

### Phase 2: Text styles

Define reusable text styles in `styles.xml` when the project has no better convention.

Use `TextAppearance.App.*` for reusable text appearances and `Widget.App.*` for widgets/components.

Text fidelity rules:

- Set `android:includeFontPadding="false"` unless the project convention or design requires default font padding.
- Preserve `fontFamily`, `textSize`, `lineHeight`, `textColor`, `textStyle`, and `letterSpacing` when available.
- If exact font files are missing, use the closest available font and explicitly report the gap.
- For multi-line text, preserve line height and max lines when specified.

Example:

```xml
<style name="TextAppearance.App.Title20">
    <item name="android:fontFamily">@font/inter_semibold</item>
    <item name="android:textSize">@dimen/text_size_20</item>
    <item name="android:textColor">@color/color_text_primary</item>
    <item name="android:includeFontPadding">false</item>
</style>
```

### Phase 3: Drawable and selector resources

For Figma fills, strokes, and corners, create shape drawables:

```xml
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/color_bg_card" />
    <corners android:radius="@dimen/radius_16" />
    <stroke
        android:width="@dimen/stroke_1"
        android:color="@color/color_border_default" />
</shape>
```

For buttons and stateful components, use selectors rather than runtime hacks:

- `selector_button_primary.xml`
- `selector_input_border.xml`
- `selector_card_background.xml`

Approximate Figma shadows carefully. XML View shadows are limited; use elevation for Material-like shadows, drawable layers for simple shadows, or document that an exact shadow requires a custom drawable/view.

### Phase 4: Layout XML

Use `ConstraintLayout` as the default root for complex screens.

Layout rules:

- Root screen: usually `android:layout_width="match_parent"` and `android:layout_height="match_parent"`.
- Inside `ConstraintLayout`, use `0dp` for dimensions that should stretch between constraints. Do not use child `match_parent` inside `ConstraintLayout` unless there is a project-specific reason.
- Use `wrap_content` for text height unless fixed height is explicitly required.
- Avoid translating Figma absolute x/y positions into a pile of fixed margins.
- Avoid excessive nested `LinearLayout` hierarchies.
- Use `LinearLayout` only for simple vertical/horizontal groups where it improves clarity.
- Use `FrameLayout` for overlays, badges, scrims, or stacked content.
- Use `RecyclerView` for repeating content and create separate `item_*.xml` files.
- Use `NestedScrollView` only when the whole page scrolls and there is no large/repeating list.
- Add `tools:` preview attributes for design-time content, not runtime behavior.
- Keep IDs meaningful: `titleText`, `primaryButton`, `bannerImage`, `contentRecyclerView`.

Constraint rules:

- Anchor sections to sibling or parent constraints, not arbitrary coordinates.
- Use `app:layout_constraintDimensionRatio` for fixed-ratio images/cards.
- Use chains for evenly distributed horizontal or vertical items.
- Use barriers when long dynamic text affects alignment.
- Use guidelines only when the design genuinely uses a fixed percentage or shared alignment rail.

### Phase 5: Figma-to-XML conversion rules

Use these mappings unless project conventions override them:

| Figma concept | Android XML implementation |
|---|---|
| Vertical Auto Layout | `LinearLayout vertical` for simple groups; `ConstraintLayout` for complex groups |
| Horizontal Auto Layout | `LinearLayout horizontal` for simple groups; `ConstraintLayout` for adaptive alignment |
| Fill container | `0dp` + constraints, or root `match_parent` |
| Hug contents | `wrap_content` |
| Fixed size | named `@dimen/...` |
| Gap | margin or parent padding from `@dimen/...` |
| Padding | parent `android:padding*` from `@dimen/...` |
| Overlay / badge | `FrameLayout` or constrained overlay |
| Figma image Fill | `ImageView android:scaleType="centerCrop"` |
| Figma image Fit | `ImageView android:scaleType="fitCenter"` |
| Icon SVG | Convert to VectorDrawable XML |
| Button variants | style + background selector + text color selector |
| Input variants | background/border selector + helper/error text |

### Phase 6: System bars and insets

Always decide whether the Figma frame includes status bar and navigation bar.

- If the Figma frame includes system bars, do not duplicate their space in XML.
- If the Figma frame excludes system bars, ensure the Activity/Fragment handles WindowInsets or existing project edge-to-edge conventions.
- If targetSdk is 35 or higher, explicitly check whether edge-to-edge behavior affects the screen.
- Do not silently add top/bottom padding without explaining whether it corresponds to system bars, toolbar height, or content spacing.

### Phase 7: Kotlin / ViewBinding

Only add Kotlin when needed for:

- wiring ViewBinding
- setting adapters
- loading images
- applying WindowInsets
- binding sample/static data
- handling simple states requested by the user

Do not put visual dimensions, colors, or spacing in Kotlin unless unavoidable. Keep UI styling in XML resources.

If the screen has a list:

- Create `item_*.xml`.
- Create or update adapter only if required.
- Keep item spacing faithful to Figma.
- Use stable, simple placeholder data if the user has not supplied real data.

## Validation

After implementation, validate in this order where possible:

1. XML resource syntax and duplicate names.
2. Gradle build or at least module resource merge:
   - `./gradlew assembleDebug`
   - or the narrowest relevant Gradle task available.
3. Lint or Android Studio warnings when available.
4. Manual layout review against the Figma spec.
5. Screenshot comparison, if screenshots are available.

If running Gradle is not practical, report that validation was limited and perform static XML review.

## Screenshot Difference Workflow

When the user provides both Figma and app screenshots, or when screenshots can be generated:

1. Compare layout first: root padding, top/bottom offsets, section positions, scroll area.
2. Compare typography: font weight, text size, line height, baseline, text color.
3. Compare spacing: margins, inner padding, list gaps, icon-text gaps.
4. Compare components: radius, stroke, background, selector states.
5. Compare imagery: crop, aspect ratio, alignment, clipping.
6. Compare system bars/insets.

Output a prioritized diff list before making changes. Fix only necessary differences. Do not rewrite the whole screen unless the structure is fundamentally wrong.

## Final Response Format

When finishing an implementation, summarize:

- Files changed.
- Resources added or reused.
- Layout/component structure.
- Known deviations from Figma.
- Validation performed and result.
- Next screenshot-diff steps, if needed.

## Real-World Pitfalls (battle-tested gotchas)

These are non-obvious failures that have caused multiple debug rounds. Check each one BEFORE the user asks "why is X broken".

### Asset format pitfalls

#### 1. SVG-as-PNG trap (most common)
- **Symptom**: Downloaded `.png` files are present at sane sizes (700B-2KB) but `ImageView` renders blank, no error.
- **Cause**: Figma exports vector nodes (Group with paths/rects/circles) as **raw SVG content** even when the asset URL looks like it returns a PNG. The file extension is `.png` but the bytes start with `<svg ...>`. Android's `BitmapFactory` cannot decode SVG → silent blank.
- **Detection**: After every batch download, check PNG magic bytes:
  ```python
  with open(path, 'rb') as f:
      ok = f.read(8) == b'\x89PNG\r\n\x1a\n'
  ```
  Or `file path.png` should report `PNG image data`, not `SVG Scalable Vector Graphics image`.
- **Fix**: Convert each SVG to Android `VectorDrawable` XML (handles `<rect>`/`<line>`/`<circle>`/`<path>` with `fillColor`/`strokeColor`/`strokeWidth`). Save as `.xml` in `drawable/`, **delete the broken `.png`** (Android resource system: `@drawable/foo` matches either `.png` or `.xml` — having both causes duplicate-resource error).
- **Quick rule**: anything that appears as a `<g id="...">` group with shape primitives in Figma → expect SVG export → expect to convert.

#### 2. SVG `<filter>` (drop shadow / inner shadow / blur) doesn't translate
- **Symptom**: Converted VectorDrawable shows the shape but missing the shadow/glow that was visible in Figma.
- **Cause**: VectorDrawable does not support `feGaussianBlur` / `feDropShadow` / `feColorMatrix`. SVG `<filter>` blocks are silently dropped during conversion.
- **Fix**: Approximate shadows with Android `android:elevation` (Material drop shadow), or for non-rectangular cards use `CardView` + `cardElevation`. Inner shadows generally cannot be reproduced without a full bitmap render.

#### 3. SVG `linearGradient` → use Android shape `<gradient>`
- **Symptom**: VectorDrawable shows solid color where Figma had a gradient fill.
- **Cause**: `<linearGradient>` referenced via `fill="url(#paint0_linear...)"` requires either inline `<aapt:attr name="android:fillColor">` (API 24+) inside the `<path>`, or rewriting the whole asset as a `shape` drawable with `<gradient>`.
- **Fix**: For simple gradients on rect/oval, **prefer hand-authored `shape` drawable** with `<gradient android:angle="270" startColor="..." endColor="..." />` — it's cleaner than fighting VectorDrawable inline gradients.

#### 4. SVG `mask group` (alpha mask / clip path) cannot run in XML View system
- **Symptom**: Figma hero illustration cropped to a specific shape — Android shows the un-cropped photo.
- **Cause**: Figma's mask group uses alpha masking on raster images. The View system has no built-in alpha mask. Compose has it. `BitmapShader` + custom View can do it.
- **Fix**: Use the source photo asset directly without mask (90-95% visual match), or write a small custom `MaskedImageView` if pixel-perfect is required. Document the deviation.

#### 5. Asset filename ↔ content mapping is unreliable
- **Symptom**: Tab a/b state PNGs render but selected tab shows the wrong icon (e.g., clicking "device" makes "mine" turn blue).
- **Cause**: When pre-downloaded by an earlier script, naming conventions (`_a` for active, `_b` for inactive) may have been applied inconsistently — one tab's `_a` is blue while another's `_a` is gray.
- **Fix**: For state-pair assets, **read each PNG once** to verify content matches the name. Then either rename files on disk OR adjust selectors/Java to match actual content. Don't fix it twice.

#### 6. Figma asset URLs are short-lived (7-day TTL)
- **Symptom**: `curl <figma-mcp-asset-url>` succeeds but downloads 0 bytes or HTML error.
- **Cause**: URLs returned by `get_design_context` expire ~7 days after the call. Asset URLs cached from earlier sessions may be dead.
- **Fix**: Re-call `get_design_context` for fresh URLs immediately before downloading. Do not store/reuse URLs across sessions.

### Layout / inset pitfalls

#### 7. `match_parent` + `weight=1` collision in LinearLayout
- **Symptom**: Sibling views (tab bar, footer) get pushed off-screen when a weighted child is present.
- **Cause**: Setting `layout_height="match_parent"` on a child with `layout_weight="1"` causes some Android versions to allocate the child the full parent height before applying weight, eating space meant for fixed-size siblings.
- **Fix**: Use `layout_height="0dp"` + `layout_weight="1"` (the canonical LinearLayout weight pattern). Same for horizontal: `layout_width="0dp"` + `layout_weight`.

#### 8. Edge-to-edge enforced on `targetSdk` 35+
- **Symptom**: Top of screen (back button, title) hidden behind the system status bar.
- **Cause**: Android 15 (`targetSdk=35`) makes app windows fullscreen by default, regardless of theme settings. Activities must explicitly handle insets.
- **Fix**: Add `android:fitsSystemWindows="true"` to the **Activity root layout** (not just individual fragments). For multi-fragment Activities, putting it on the Activity root means all fragments inherit padded content. ImmersionBar alone does not pad content.

#### 9. Figma absolute Y positions assume "0 = below status bar"
- **Symptom**: Content positioned with Figma's Y values appears too low on Android.
- **Cause**: Figma 375×812 frames assume 50dp iPhone status bar at top. Figma `y=110` means "60dp below status bar" — but on Android, `marginTop=110dp` would be 110dp from screen top, including any Android status bar.
- **Fix**: Subtract Figma status bar height (50dp) when mapping to Android marginTop after `fitsSystemWindows="true"` consumes the inset. Or use a 48dp Android toolbar and measure from below it.

#### 10. PingFang SC font is iOS-only
- **Symptom**: Chinese characters look subtly wrong on Android compared to Figma.
- **Cause**: Figma uses PingFang SC (iOS system Chinese font). Android falls back to Noto Sans CJK / 鸿蒙 Sans / OEM-specific fonts.
- **Fix**: Either bundle PingFang or close-equivalent font (`+5-10MB APK`), or accept system fallback. For special display fonts (FZHanZhenGuangBiao etc.) → bundle is unavoidable for fidelity.

### State management pitfalls

#### 11. `duplicateParentState=true` + state-list selectors are fragile on MIUI/EMUI
- **Symptom**: Tab/button state changes work on some devices but not others. Icon doesn't swap, text doesn't recolor, despite `setSelected(true)` being called on parent.
- **Cause**: Relying on `View.setSelected` cascading through `dispatchSetSelected` to children, which then read parent state via `duplicateParentState`, then state-list selector resolves the right drawable/color. Multiple framework hops, each one varies by ROM.
- **Fix**: For tab bars and similar, **explicit Java helper** is more reliable:
  ```kotlin
  fun selectTab(index: Int) {
      tab1.setSelected(index == 0)
      iv1.setImageResource(if (index == 0) R.drawable.tab_a else R.drawable.tab_b)
      tv1.setTextColor(if (index == 0) selectedColor else unselectedColor)
      // ... repeat per tab
  }
  ```
  Single source of truth. Selectors and `duplicateParentState` become unnecessary for these cases.

#### 12. Text-color flicker on touch-down with multi-state ColorStateList
- **Symptom**: Tapping a tab briefly turns text blue (or other "selected" color) before reverting.
- **Cause**: ColorStateList with `state_pressed` matches first → selected color shows during touch-down, even before click handler sets the actual selected state.
- **Fix**: Either remove the `state_pressed` entry or accept the flicker. For tab bars, prefer single color + explicit Java state changes (see #11).

### Figma access pitfalls

#### 13. File access ≠ node access
- **Symptom**: `get_metadata` / `get_design_context` returns "This figma file could not be accessed" (`could not be accessed`).
- **Cause**: The MCP-authenticated account doesn't have view permission on this file.
- **Fix**: User must (a) invite the auth account email as Viewer, (b) change sharing to "Anyone with the link — can view", or (c) re-auth Figma MCP under the file owner's account. **Always run `whoami` first** when access fails.

#### 14. Sections vs Frames in Figma
- **Symptom**: `get_design_context` on a node returns "You currently have nothing selected" even with valid `nodeId`.
- **Cause**: The node is a Figma **Section** (a container, not a Frame). Sections don't support `get_design_context` (no rendered code).
- **Fix**: Use `get_screenshot(<sectionId>)` to identify what's inside, then ask user for individual **frame** URLs to call `get_design_context` on. Frames have `node-id=NN-MM` format too but represent a discrete screen.

#### 15. `get_metadata(0:1)` truncates large files
- **Symptom**: Searching the metadata XML for a known node ID returns nothing, even though the node exists.
- **Cause**: Metadata response for a large file caps around 89K-100K chars. Deeper sub-frames fall off the end.
- **Fix**: Don't rely on file-root metadata to enumerate everything. Pull specific node IDs directly via `get_design_context` or `get_screenshot`. Ask user for URLs.

#### 16. Copying a Figma file may renumber node IDs
- **Symptom**: User shares a URL with `node-id=34-335` from the original, but the same node-id doesn't exist in their Copy file.
- **Cause**: Figma duplicate-file behavior is inconsistent — sometimes preserves IDs, sometimes regenerates.
- **Fix**: When working from a Copy, always re-pull `get_design_context` to verify the node still exists at the expected ID. If not, ask user to re-export the URL from the Copy file directly.

### Build pitfalls

#### 17. Multi-channel build is slow; iterate on a single flavor
- **Cause**: Projects with multiple market flavors (Xiaomi, Huawei, Oppo, Vivo, Yingyongbao etc.) running `./gradlew assembleDebug` builds every flavor. 5+ minute builds kill iteration speed.
- **Fix**: Build just one flavor for iteration: `./gradlew assembleXiaomiDebug` (or whatever's installed on the test device). Run the full multi-channel build only at the end.

#### 18. `dimens.xml` `dp_NN` token sequence has gaps
- **Symptom**: Build fails with `error: resource dimen/dp_378 not found` after referencing what looks like a standard Figma value.
- **Cause**: Existing project's `dimens.xml` has `dp_1`..`dp_360`, then jumps `dp_365`, `dp_370`, `dp_400`, `dp_410`, `dp_472`, `dp_500`, etc. — common values like 378, 395, 486 are missing.
- **Fix**: Add missing entries to `dimens.xml` as needed. Don't assume the dp_NN sequence is dense.

### Custom view pitfalls

#### 19. Custom-canvas widgets can't match gradient-rich Figma PNGs
- **Symptom**: A `View` subclass that draws a dial / indicator via `Canvas.drawCircle/drawArc/drawText` looks "flat" compared to Figma's layered gradient design.
- **Cause**: Hand-coded Paint flat fills don't replicate the multi-stop gradients + soft shadows + blur layers that Figma renders.
- **Fix**: Layer the Figma drawable (PNG or VectorDrawable) **behind** the custom view, then use the custom view as a transparent **touch-only overlay** (empty `onDraw`, keep `onTouchEvent`). Caller composition: `FrameLayout` { dial_bg + arrow_overlays + center_text + custom_dpad_view }.

#### 20. ColorStateList resource location convention
- **Note**: `<selector>` files with `<item android:color>` (not `android:drawable`) conventionally go in `res/color/` not `res/drawable/`. Both work for `android:textColor="@drawable/foo"` references, but `res/color/` is the idiomatic location and avoids confusion.

### Workflow & verification pitfalls

#### 21. Don't `Read` many drawables in one turn after batch download — it hard-errors the API
- **Symptom (real, observed)**: After downloading ~13+ image assets and `Read`-ing each one in sequence to "verify content", the Anthropic API returns:
  ```
  API Error: 400 {"type":"error","error":{"type":"invalid_request_error","message":"Could not process image"}}
  ```
  The turn is **blocked** — you can't continue, must roll back. This is not a context-budget warning, it's an upstream image-processing failure.
- **Cause**: Anthropic's image processing has per-turn limits (count and/or cumulative size). Batch-`Read`-ing many PNGs (especially photos in the 100KB+ range) blows past it. SVG-as-PNG files at ~700B-2KB don't decode as images either, which can also tip the error mode.
- **Fix**: After batch download, **use `ls -lhS`** to verify file sizes are reasonable:
  - Small icons: expect ≥1KB for a colored raster, ≥500B for a vector
  - Photos / illustrations: expect ≥50KB
  - Anything <300B is suspicious (likely a fragment or HTML error page)
  
  Then **`Read` at most 1–2 images per turn**, and only when you specifically need visual disambiguation (e.g., which of `tab_a/b` is selected blue vs unselected gray). Never sweep through the whole download with `Read`.
- **Concrete budget**: If you need to compare 6+ state-pair images, do it across multiple turns (3 per turn max with photos in the mix), or skip visual verification and trust the build to fail loud.

#### 22. `MD5 compare` doesn't help when source format is wrong
- **Cause**: User suggests "re-download and MD5 compare to verify". But if Figma is exporting the wrong format (SVG instead of PNG), the bytes will be identical to existing broken files — MD5 matches.
- **Fix**: Before MD5, run a **format check** (PNG header magic bytes). If format is wrong, MD5 is moot — the asset itself needs a different export approach (manual VectorDrawable conversion, or different Figma node, or hand-authored Android shape).

## Anti-patterns to Avoid

- Starting with the page XML before extracting resources.
- Hardcoding `#RRGGBB`, `16dp`, or `14sp` throughout the layout.
- Using `match_parent` inside `ConstraintLayout` children where `0dp` constraints are needed.
- Converting Figma absolute positions directly into fixed margins.
- Deeply nesting `LinearLayout` for a complex page.
- Ignoring `includeFontPadding`, line height, font weight, or letter spacing.
- Leaving `ImageView` without an explicit `scaleType`.
- Using Material default button/text-field/card styling without overriding padding, shape, colors, and states to match Figma.
- Mixing runtime placeholder text with design-time preview text.
- Silently assuming system bars are included or excluded.
- **Trusting `.png` extension without checking magic bytes after Figma download** (see Pitfall #1).
- **Layout `match_parent` + `weight=1` together in LinearLayout** (see Pitfall #7).
- **Relying on `duplicateParentState` for tab/button state changes** (see Pitfall #11).
- **Reading every drawable after batch download to "verify"** (see Pitfall #21).

## Invocation Examples

```text
/figma-android-xml https://www.figma.com/design/... Login screen activity_login.xml
```

```text
/figma-android-xml 请根据当前 Figma Frame 实现 res/layout/fragment_product_detail.xml，XML + ViewBinding，不要用 Compose。
```

```text
/figma-android-xml 对比 figma.png 和 actual.png，只列出 XML 还原差异并修复必要资源和布局。
```
