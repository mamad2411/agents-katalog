---
name: qt-figma-token-extraction
version: 1.0.0
description: Extract design tokens from a Figma file via the REST API and map them into a Qt QML theme singleton.
author: matrixx0070
tags: [figma, qml, design-tokens, theming, qt6]
capabilities: []
---

## When to use

Use this when you have a Figma file and need its raw design decisions — colors, typography, spacing, radii, shadows — expressed as a typed, reusable Qt QML theme. Start here before you generate any component, because everything downstream should reference the tokens, not literal values.

**Not for:** turning Figma frames into actual QML component trees (see qt-figma-component-generation), or hand-designing a UI without a Figma source (see qt-ui-design).

## Method

1. Authenticate to the Figma REST API with a personal access token in the `X-Figma-Token` header. Confirm access with `GET /v1/files/:key` (the `:key` is the segment after `/file/` or `/design/` in the Figma URL).
2. Decide the token source. **Decision point:** if the file uses Figma **Variables** (Variables API / published variable collections) or **Styles**, prefer those as the token source of truth; if the design only has raw values baked into nodes, fall back to reading node properties directly via `GET /v1/files/:key/nodes?ids=...`.
3. Pull style metadata with `GET /v1/files/:key/styles` to list `FILL`, `TEXT`, and `EFFECT` styles with their names and `node_id`s. Resolve each style's actual paint/type/effect by requesting those node ids.
4. Extract colors. Figma paints give `color` as `{r,g,b}` floats in 0–1 plus a separate `opacity`. **Decision point:** if `opacity < 1` or the paint carries alpha, emit an 8-digit `#AARRGGBB` (Qt hex order) or `Qt.rgba(r,g,b,a)`; otherwise emit `#RRGGBB`.
5. Extract typography from `TEXT` styles: `fontFamily`, `fontSize`, `fontWeight`, `lineHeightPx`/`lineHeightPercent`, and `letterSpacing`. Map numeric weight to the Qt `Font` weight enum.
6. Extract spacing, radii, and shadows. Read auto-layout `itemSpacing`/`padding*` for spacing, `cornerRadius` (or `rectangleCornerRadii`) for radii, and `EFFECT` styles of type `DROP_SHADOW`/`INNER_SHADOW` for shadows.
7. Normalize names: slugify each Figma token name (e.g. `color/brand/primary`) into a valid QML property identifier (`colorBrandPrimary`). **Decision point:** if names collide after slugification, prefix by category to keep them unique.
8. Handle units. **Decision point:** if the design targets multiple densities, keep spacing/radii as logical pixels (Qt6 scales automatically by device pixel ratio) and document that px maps 1:1 to logical px at DPR 1; do not bake physical pixels.
9. Emit a `Theme.qml` singleton (`pragma Singleton`) grouped by category, and register it with `qt_add_qml_module`.

## Example

```qml
// Theme.qml
pragma Singleton
import QtQuick

QtObject {
    // colors  (Figma FILL styles → #AARRGGBB / Qt.rgba)
    readonly property color colorBrandPrimary:   "#FF2D6CDF"          // rgba(0.176,0.424,0.875,1)
    readonly property color colorSurface:        "#FFFFFFFF"
    readonly property color colorOverlay:        Qt.rgba(0, 0, 0, 0.5) // 50% scrim

    // spacing (logical px, from auto-layout itemSpacing/padding)
    readonly property int spacingXs: 4
    readonly property int spacingSm: 8
    readonly property int spacingMd: 16

    // radii (cornerRadius)
    readonly property int radiusSm: 6
    readonly property int radiusLg: 16

    // typography (TEXT styles)
    readonly property font titleLarge: Qt.font({
        family: "Inter",
        pixelSize: 22,
        weight: Font.DemiBold,   // Figma weight 600
        letterSpacing: 0
    })
}
```

```cmake
# CMakeLists.txt — register the singleton
qt_add_qml_module(app
    URI MyApp.Theme
    VERSION 1.0
    QML_FILES
    RESOURCES
    SOURCES
)
set_source_files_properties(Theme.qml PROPERTIES QT_QML_SINGLETON_TYPE TRUE)
```

## Pitfalls

- **Wrong hex order.** CSS uses `#RRGGBBAA`; Qt hex color strings are `#AARRGGBB`. Convert alpha to the leading pair or use `Qt.rgba(...)` to avoid ambiguity.
- **Float vs byte color.** Figma emits 0–1 floats; multiply by 255 and round for hex, or pass floats straight to `Qt.rgba`. Never truncate — rounding errors shift brand colors visibly.
- **Ignoring paint opacity.** The paint `color` has no alpha; alpha lives in the paint's `opacity`. Merge them or the token loses transparency.
- **Line-height mismatch.** Figma line height can be `lineHeightPx` or `lineHeightPercent`; QML `Text.lineHeight` is a multiplier (with `lineHeightMode`). Convert explicitly instead of copying the raw number.
- **Non-identifier names.** Slashes, spaces, and leading digits in Figma names are invalid QML identifiers. Always slugify before emitting properties.
- **Singleton not registered.** A `pragma Singleton` file without `QT_QML_SINGLETON_TYPE` (or a `qmldir` singleton line) fails to import at runtime.

## Output format

```
Theme.qml            # pragma Singleton QtObject with categorized readonly properties
tokens.json          # intermediate machine-readable dump of extracted tokens
qmldir / CMake       # singleton registration snippet
```

```json
{
  "colors":   { "brandPrimary": "#FF2D6CDF", "surface": "#FFFFFFFF" },
  "spacing":  { "xs": 4, "sm": 8, "md": 16 },
  "radii":    { "sm": 6, "lg": 16 },
  "typography": {
    "titleLarge": { "family": "Inter", "pixelSize": 22, "weight": 600, "letterSpacing": 0 }
  },
  "shadows":  { "elevation1": { "dx": 0, "dy": 1, "blur": 3, "color": "#33000000" } }
}
```

## Reference

- **Endpoints:** `GET /v1/files/:key` (full document tree), `GET /v1/files/:key/nodes?ids=1:2,3:4` (targeted subtrees; use this to resolve style node ids), `GET /v1/files/:key/styles` (published style metadata: `key`, `name`, `style_type` = `FILL`/`TEXT`/`EFFECT`/`GRID`, `node_id`). Auth header is `X-Figma-Token: <PAT>`.
- **Variables vs styles vs raw:** Variables (Variables REST API, `variableId` references) are the modern token source and support modes/aliasing; classic Styles cover fill/text/effect; raw node values are the last resort when nothing is published.
- **Color format:** Figma `SOLID` paint = `{ color: {r,g,b}, opacity }` with each channel a 0–1 float. Qt color string is `#AARRGGBB`; programmatic is `Qt.rgba(r, g, b, a)` (all 0–1) or `Qt.hsla(...)`. Effective alpha = paint `opacity` × node opacity.
- **Font weight mapping:** Figma numeric weight → `Font` enum: 100 `Font.Thin`, 200 `Font.ExtraLight`, 300 `Font.Light`, 400 `Font.Normal`, 500 `Font.Medium`, 600 `Font.DemiBold`, 700 `Font.Bold`, 800 `Font.ExtraBold`, 900 `Font.Black`. Prefer `pixelSize` over `pointSize` for pixel-precise Figma parity.
- **Singleton:** `pragma Singleton` at the top of `Theme.qml`; register via `qt_add_qml_module` plus `set_source_files_properties(... QT_QML_SINGLETON_TYPE TRUE)`, or a `singleton Theme 1.0 Theme.qml` line in `qmldir`. Import with the module URI, then reference `Theme.colorBrandPrimary`.
- **Units / DPI:** Qt 6 works in logical pixels and scales by the platform device pixel ratio automatically; treat Figma px as logical px at DPR 1. Use `int`/`real` tokens, not physical measurements.
- **Naming convention:** token path `category/group/name` → camelCase QML property `categoryGroupName`; keep `readonly property` typed (`color`, `int`, `real`, `font`) for tooling and completion.
