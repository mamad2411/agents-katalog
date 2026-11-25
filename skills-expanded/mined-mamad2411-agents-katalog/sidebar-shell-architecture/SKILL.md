---
name: sidebar-shell-architecture
description: >
  Extends agent's knowledge of the sidebar shell pattern for desktop JavaFX
  apps. Use when building the main application frame, implementing collapsible
  navigation drawers, or structuring a persistent topbar + sidebar layout.
compatibility: Java 21+
metadata:
  domain: ui-kickstartfx
  level: intermediate
  stack: [java-21, javafx-21]
  version: "1.0.0"
---

# Sidebar Shell Architecture

The shell is the persistent frame: topbar (brand, search, user menu) + sidebar
(navigation items) + a center content area that swaps views. The shell never
reloads — only the center `StackPane` content changes.

## Concepts

- **Shell control**: custom `Region` with its own FXML — `ShellView.fxml`
- **Sidebar**: `VBox` of icon+label `ToggleButton`s styled as nav items
- **Content area**: `StackPane` in `BorderPane.CENTER` — navigation service replaces its children
- **Collapsible mode**: sidebar toggles between icon-only (collapsed) and icon+label (expanded)
- **Notification badge**: `Label` overlay on sidebar items showing pending counts

## Rules

1. Shell loads once at startup — navigation changes only the center content pane.
2. Track active route via an `ObjectProperty<Route>` bound to sidebar `ToggleButton` selection.
3. Collapse/expand sidebar with a smooth `TranslateX` animation, not by removing nodes.
4. Topbar remains static — search and user menu are included inside the shell FXML.
5. Content views must not know they live in a shell — inject navigation service via constructor.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- navigation-patterns — drives center content swaps
- responsive-desktop-layouts — shell adapts to window size
