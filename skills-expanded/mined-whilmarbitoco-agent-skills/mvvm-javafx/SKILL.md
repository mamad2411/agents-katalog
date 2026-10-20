---
name: mvvm-javafx
description: >
  Extends agent's knowledge of MVVM pattern with JavaFX 21.
  Use when building reactive desktop UIs with clean separation between
  view definition (FXML), binding logic (ViewModel), and domain state (Model).
compatibility: Java 21+
metadata:
  domain: architecture
  level: intermediate
  stack: [java-21, javafx-21, slf4j]
  version: "1.0.0"
---

# MVVM with JavaFX

MVVM keeps the View passive and the ViewModel stateless in behavior. Bindings carry updates; they are not event spaghetti.

## Roles

- **Model** — Domain entities, records, value objects. No UI knowledge.
- **ViewModel** — Observable state (`ObjectProperty`, `StringProperty`),
  commands, and formatters. Holds no `Node` references.
- **View** — FXML file + controller. Binds to ViewModel via `Bindings API`.
  Minimal code-behind; no business logic.

## Rules

- Controller injects ViewModel via constructor; ViewModel never imports `javafx.scene.*`.
- Use `SimpleObjectProperty`, `SimpleListProperty` — not raw fields with getters/setters.
- Formatting (dates, currency) belongs in ViewModel, not in FXML.
- ViewModels are testable with plain JUnit — no FX toolkit needed.
- Prefer FXML for layout; use `fx:controller` with factory that injects the ViewModel.

## Thread safety

- All bound properties must be mutated on FX Application Thread.
- Background work via `Task` / `Service` pattern; ViewModel exposes `ObjectProperty<Task>`.

## See also

- event-driven-ui — event bus complements MVVM binding
- layered-architecture — Model layer guidance
