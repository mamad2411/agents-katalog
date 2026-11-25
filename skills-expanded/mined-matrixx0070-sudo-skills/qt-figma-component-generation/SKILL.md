---
name: qt-figma-component-generation
version: 1.0.0
description: Generate reusable Qt Quick QML components from Figma frames and components using extracted design tokens.
author: matrixx0070
tags: [figma, qml, codegen, qt-quick, components]
capabilities: []
---

## When to use

Use this when you have Figma frames or components and want them turned into structured Qt Quick QML components — layouts, rectangles, text, and images — that reference a theme singleton instead of literal values. Run token extraction first so generated components stay themeable.

**Not for:** extracting colors/typography/spacing into a theme (see qt-figma-token-extraction), or designing a UI from scratch without a Figma source (see qt-ui-design).

## Method

1. Fetch the target subtree with `GET /v1/files/:key/nodes?ids=...` and traverse the node tree depth-first, reading each node's `type`, `name`, `absoluteBoundingBox`, `layoutMode`, `constraints`, `fills`, `strokes`, `cornerRadius`, and `characters`.
2. Choose the container. **Decision point:** if a frame has `layoutMode` of `HORIZONTAL` map it to `RowLayout`, `VERTICAL` map it to `ColumnLayout`; if `layoutMode` is `NONE`, keep a plain `Item`/`Rectangle` and position children with anchors from their `constraints`.
3. Map auto-layout spacing and padding: frame `itemSpacing` → layout `spacing`; `paddingLeft/Right/Top/Bottom` → `Layout.margins` on children or an outer `Item` with anchored margins.
4. Map constraints to anchors when not using a layout: `LEFT`/`RIGHT`/`CENTER`/`SCALE`/`TOP`/`BOTTOM` → `anchors.left/right/horizontalCenter/fill/top/bottom`. **Decision point:** never place a child under both a `*Layout` (via `Layout.*`) and manual `anchors` on the same item — pick one per item.
5. Map visual leaf nodes. `RECTANGLE`/`FRAME` fills → `Rectangle.color`; `strokes` + `strokeWeight` → `border.color`/`border.width`; `cornerRadius` (or `rectangleCornerRadii` for per-corner) → `radius`.
6. Map text. `TEXT` nodes → `Text` (or `Label` from Controls) with `text: node.characters`, and `font` sourced from the theme singleton typography token that matches the node's text style.
7. Decide component boundaries. **Decision point:** if a Figma node is a `COMPONENT`/`INSTANCE` or repeats, emit a separate reusable `.qml` file with `property` inputs (text, colors, callbacks) and set `implicitWidth`/`implicitHeight`; otherwise inline it.
8. Handle images/vectors. **Decision point:** if the node is a `VECTOR`/boolean/star shape, export SVG and use it via an `Image` (or `IconImage`); if it is a raster fill (`IMAGE` paint), export a PNG/@2x and reference it with `Image { source }` and a `fillMode`.
9. Replace every literal with a token reference (`Theme.colorSurface`, `Theme.spacingMd`, `Theme.radiusLg`) resolved from the extraction step; leave a `TODO` only when no matching token exists.
10. Set sizing from content: give components `implicitWidth`/`implicitHeight` so parents and layouts can size them, rather than hardcoding `width`/`height`.

## Example

```qml
// PrimaryButton.qml  (from a Figma COMPONENT with auto-layout)
import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import MyApp.Theme

Rectangle {
    id: root
    property alias text: label.text
    signal clicked()

    implicitWidth: content.implicitWidth + Theme.spacingMd * 2
    implicitHeight: content.implicitHeight + Theme.spacingSm * 2
    radius: Theme.radiusSm
    color: mouse.pressed ? Theme.colorBrandPressed : Theme.colorBrandPrimary
    border.width: 1
    border.color: Theme.colorBrandPrimary

    RowLayout {          // Figma layoutMode: HORIZONTAL
        id: content
        anchors.centerIn: parent
        spacing: Theme.spacingXs

        Image {          // exported SVG vector
            source: "qrc:/icons/plus.svg"
            sourceSize: Qt.size(16, 16)
        }
        Label {          // Figma TEXT node
            id: label
            font: Theme.titleLarge
            color: Theme.colorOnBrand
        }
    }

    MouseArea { id: mouse; anchors.fill: parent; onClicked: root.clicked() }
}
```

## Pitfalls

- **Anchors and Layout on one item.** Mixing `anchors.*` with `Layout.*` on the same child yields undefined geometry and console warnings. One positioning system per item.
- **Hardcoded width/height.** Copying Figma `absoluteBoundingBox` as fixed `width`/`height` breaks inside layouts and on resize. Prefer `implicitWidth`/`implicitHeight` plus `Layout.fillWidth`.
- **Baking literal colors.** Emitting raw hex instead of `Theme.*` defeats the token pipeline; every fill/stroke should resolve to a token.
- **Per-corner radius lost.** `cornerRadius` is a single value; Figma per-corner radii (`rectangleCornerRadii`) need Qt's per-corner `topLeftRadius`/etc. (Qt 6.7+) or a shape, not one `radius`.
- **Text elision and wrapping dropped.** Figma text boxes clip/auto-resize; set `Text.wrapMode`/`elide`/`maximumLineCount` deliberately or long strings overflow.
- **Vector as font glyph.** Don't approximate Figma vectors with characters; export SVG and render via `Image`/`IconImage` for fidelity and crisp scaling.

## Output format

```
components/
  PrimaryButton.qml     # reusable COMPONENT → property-driven .qml
  Card.qml
  <Frame>.qml           # one file per Figma component/instance
assets/
  icons/*.svg           # exported vectors
  images/*@2x.png       # exported rasters
qmldir                  # module registration for generated components
```

```qml
// each generated component follows this skeleton
import QtQuick
import QtQuick.Layouts
import MyApp.Theme

Item {
    // public API: property aliases + signals
    // layout: Row/Column/GridLayout OR anchored Item
    // leaves: Rectangle (fill/border/radius), Text/Label (theme font), Image (svg/png)
    // sizing: implicitWidth / implicitHeight
}
```

## Reference

- **Node traversal:** `GET /v1/files/:key/nodes?ids=...` returns `document` subtrees; recurse `children`. Relevant fields: `type` (`FRAME`, `COMPONENT`, `INSTANCE`, `RECTANGLE`, `TEXT`, `VECTOR`, `GROUP`), `layoutMode`, `itemSpacing`, `padding*`, `constraints`, `fills`, `strokes`, `strokeWeight`, `cornerRadius`/`rectangleCornerRadii`, `characters`, `style`.
- **Auto-layout → Qt Quick Layouts:** `HORIZONTAL`→`RowLayout`, `VERTICAL`→`ColumnLayout`; wrap grids in `GridLayout`. `itemSpacing`→`spacing`; use `Layout.fillWidth`/`Layout.fillHeight`/`Layout.preferredWidth`/`Layout.alignment` on children (`import QtQuick.Layouts`).
- **Constraints → anchors:** `MIN`→`left`/`top`, `MAX`→`right`/`bottom`, `CENTER`→`horizontalCenter`/`verticalCenter`, `STRETCH`/`SCALE`→`anchors.fill` or left+right anchors. Anchors and Layouts are mutually exclusive per item.
- **Fills/strokes/radius:** solid `fills[0]` → `Rectangle.color` (convert Figma 0–1 RGBA per qt-figma-token-extraction); `strokes[0]` + `strokeWeight` → `border.color`/`border.width`; `cornerRadius` → `radius` (per-corner via `topLeftRadius` etc. in Qt 6.7+).
- **Text:** `TEXT` → `Text` (bare) or `Label` (Controls, theme-aware). Set `text`, `font` (from theme typography token), `color`, and explicit `wrapMode`/`elide`.
- **Controls vs custom:** use Qt Quick Controls (`Button`, `Label`, `TextField`, `Slider`) for interactive/accessible widgets and style via a theme; build custom `Rectangle`+`MouseArea` only for bespoke visuals not covered by Controls.
- **Images/SVG:** `Image { source; fillMode: Image.PreserveAspectFit; sourceSize }`; SVG is supported by the built-in svg image provider; prefer `sourceSize` to rasterize crisply. Bundle assets via the Qt resource system (`qrc:/`).
- **Reusable components:** a component is any `.qml` file whose name is Capitalized; expose inputs with `property`/`property alias` and outputs with `signal`; set `implicitWidth`/`implicitHeight` so it composes inside layouts. Register generated files with `qt_add_qml_module`/`qmldir`.
