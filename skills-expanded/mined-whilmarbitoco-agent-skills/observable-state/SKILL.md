---
name: observable-state
description: >
  Build reactive UI state with JavaFX ObservableValue, Property, and
  Binding primitives. Use when connecting domain models to live scene
  graph nodes without manual synchronization.
compatibility: Java 21+
metadata:
  domain: ui-javafx
  level: beginner
  stack: [java-21, javafx-21]
  version: "1.0.0"
---

# Observable State in JavaFX

Wrap every piece of mutable UI state in a JavaFX `Property` or
`ObservableValue`. Compose them with `Bindings` helpers so the scene
graph updates itself — never call `setText()` / `setItems()` by hand.

## Core rules
- Use `SimpleStringProperty`, `SimpleDoubleProperty`, etc. for view-model
  fields.
- Use `IntegerStringConverter`, `BigDecimalStringConverter` (custom) for
  bidirectional binds.
- Prefer `Bindings.createObjectBinding()` over manual `ChangeListener`
  when the derived value is a function of other observables.
- Use `ObservableList` + `FilteredList` / `SortedList` for dynamic tables.
- Never mirror observable state in a plain field — binds instantly stale.

## Anti-patterns
- Calling `textField.setText(...)` when a `textProperty()` bind exists.
- Creating new `ObservableList` on every refresh instead of mutating in
  place.
- Forgetting to dispose bindings (memory leak in long-lived views).

## Related
layouts • mvvm • reusable-components • threading
