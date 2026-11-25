---
name: dark-mode-strategy
description: >
  Extends agent's knowledge of runtime dark/light mode toggling in JavaFX apps.
  Use when implementing a theme switcher, persisting user appearance preference,
  or structuring CSS to support dual palettes without duplication.
compatibility: Java 21+
metadata:
  domain: ui-kickstartfx
  level: intermediate
  stack: [java-21, javafx-21]
  version: "1.0.0"
---

# Dark Mode Strategy

Support runtime switching between light and dark palettes by layering CSS
files: a base `brand.css` (typography, spacing, radii) and a palette file
(`light.css` or `dark.css`) that only redefines looked-up colors.

## Concepts

- **Layered stylesheets**: `brand.css` (always loaded) + `palette.css` (swapped at runtime)
- **CSS file generation**: generate `palette-dark.css` from a template or store both in resources
- **Preference persistence**: save choice in `Preferences.userNodeForPackage(App.class)` or a JSON file
- **Initial load**: read persisted preference before `Stage.show()` to avoid a flash of wrong palette

## Rules

1. Separate palette CSS from structural CSS — never mix color tokens with layout rules.
2. Swap palettes by replacing the stylesheet list on the `Scene`, not individual nodes.
3. Persist theme choice in `Preferences` under key `ui.theme` with values `"light"` or `"dark"`.
4. Load persisted palette in `Application.init()`, before the stage is shown.
5. Use `looks-up color` tokens everywhere — switching files changes all tokens in one pass.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- theme-customization — base theming conventions
- responsive-desktop-layouts — shell structure affects how palette is set
