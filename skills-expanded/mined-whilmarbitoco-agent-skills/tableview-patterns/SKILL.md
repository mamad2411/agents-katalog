---
name: tableview-patterns
description: >
  Build sortable, filterable, editable JavaFX TableViews with
  cell value factories, custom cell factories, and selection models.
  Use when displaying tabular data that requires inline editing or
  live filtering.
compatibility: Java 21+
metadata:
  domain: ui-javafx
  level: intermediate
  stack: [java-21, javafx-21]
  version: "1.0.0"
---

# TableView Patterns in JavaFX

Use `TableView` with `PropertyValueFactory` only for quick prototypes.
Prefer lambda-based `CellValueFactory` for type safety. Wrap the source
list in `FilteredList` and `SortedList` for live search and sort.

## Core rules
- Source list is `ObservableList`; wrap with `FilteredList` for search.
- Set `comparatorProperty()` on `SortedList` to drive column sort.
- Use `TextFieldTableCell.forTableColumn()` for inline editing.
- Use custom `TableCell` subclass for colored / icon cells (e.g., status).
- Set `setColumnResizePolicy(CONSTRAINED_RESIZE_POLICY_FLEX_LAST_COLUMN)` to fill width.

## Anti-patterns
- Using `PropertyValueFactory` with raw strings (refactoring breaks it silently).
- Replacing the `items` list on every search (resets selection and scroll).
- Inline business logic in a `CellValueFactory` lambda.
- Editing cells without `commitEdit` validation (accepts junk data).

## Related
observable-state • threading • css-theming • reusable-components
