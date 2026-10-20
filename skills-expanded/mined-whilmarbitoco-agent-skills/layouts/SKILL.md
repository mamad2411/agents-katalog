---
name: layouts
description: >
  Compose responsive JavaFX scene graphs with HBox, VBox, BorderPane,
  GridPane, and TilePane. Use when building forms, dashboards, or any
  multi-region container that must resize gracefully.
compatibility: Java 21+
metadata:
  domain: ui-javafx
  level: beginner
  stack: [java-21, javafx-21]
  version: "1.0.0"
---

# Layouts in JavaFX

Choose the right pane for the job. Nest simple panes rather than fighting
a single complex layout. Let `hgrow` / `vgrow` polices do the stretching;
avoid hardcoded `setPrefWidth()`.

## Core rules
- Use `BorderPane` for header-body-footer shells.
- Use `GridPane` for form layouts (label + input rows).
- Use `HBox` / `VBox` for linear toolbars and cards.
- Use `TilePane` for equal-width card grids.
- Set `hgrow = ALWAYS` on the column that should absorb extra width.
- Use `Priority.ALWAYS` on `RowConstraints` / `ColumnConstraints`.

## Anti-patterns
- Setting `minWidth`, `prefWidth`, `maxWidth` to the same value (prevents
  resize).
- Deeply nested `GridPane` inside `GridPane` — flatten with VBox/HBox.
- Using `AnchorPane` for responsive layouts (anchors are absolute).

## Related
css-theming • reusable-components • mvvm • observable-state
