---
name: responsive-desktop-layouts
description: >
  Extends agent's knowledge of responsive layout techniques for JavaFX desktop
  apps. Use when adapting the UI to different screen sizes, implementing
  breakpoint-like behavior, or ensuring the app works on both laptop and
  dual-monitor setups.
compatibility: Java 21+
metadata:
  domain: ui-kickstartfx
  level: intermediate
  stack: [java-21, javafx-21]
  version: "1.0.0"
---

# Responsive Desktop Layouts

JavaFX has no built-in media queries. Responsiveness comes from binding `Pane`
dimensions to observable window properties and toggling pseudo-classes or layout
strategies at thresholds.

## Concepts

- **Binding-based sizing**: `prefWidthProperty().bind(scene.widthProperty().multiply(0.3))`
- **Breakpoint detection**: listen to `widthProperty()` and set a `PseudoClass` when crossing thresholds
- **FlowPane / TilePane**: auto-wrapping containers that respond to container width without manual logic
- **Side panel pinning**: toggle between overlay (small screen) and docked modes (large screen)

## Rules

1. Prefer binding dimensions over hard-coded `prefWidth = 300` values.
2. Use `FlowPane` or `TilePane` for card grids — they auto-wrap without explicit resize logic.
3. Define three breakpoints: `< 1024px` (compact), `< 1440px` (medium), `≥ 1440px` (expanded).
4. Collapse the sidebar to icon-only below the compact breakpoint using a `PseudoClass` toggle.
5. Never use `Platform.runLater` for layout — use bindings or `InvalidationListener`.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- sidebar-shell-architecture — shell adapts sidebar visibility
- theme-customization — CSS pseudo-classes drive responsive style changes
