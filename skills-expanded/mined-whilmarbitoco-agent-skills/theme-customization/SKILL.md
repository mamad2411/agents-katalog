---
name: theme-customization
description: >
  Extends agent's knowledge of JavaFX CSS theming, custom properties, and
  palette management. Use when creating brand themes, implementing light/dark
  mode switches, or structuring CSS for maintainability.
compatibility: Java 21+
metadata:
  domain: ui-kickstartfx
  level: beginner
  stack: [java-21, javafx-21]
  version: "1.0.0"
---

# Theme Customization

JavaFX CSS uses custom looked-up colors and variables set on the scene graph.
All visual tokens live in CSS themes — controllers never call `setStyle()`.

## Concepts

- **Looked-up colors**: `-fx-primary`, `-fx-surface` — defined in root CSS, referenced everywhere
- **CSS variables**: `--spacing-unit: 8px;` — reused across rules
- **Theme files**: `light.css`, `dark.css`, `brand.css` — layered on `<scene>.getStylesheets()`
- **Programmatic switch**: `scene.getStylesheets().clear()` then re-add selected theme files

## Rules

1. Define all colors as looked-up colors in a `brand.css` base theme. Never hardcode hex in component rules.
2. Set theme stylesheets on the `Scene`, not on individual nodes.
3. Use `rem`-like spacing units via CSS variables — don't mix pixel values across rules.
4. Load theme files from external JAR or config dir so merchants can customize without recompiling.
5. Never use `node.setStyle("-fx-…")` in Java code — use pseudo-classes or toggle stylesheets instead.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- dark-mode-strategy — runtime theme switching
- responsive-desktop-layouts — layout tokens pair with theme spacing
