---
name: threading
description: >
  Run background work off the JavaFX Application Thread and safely
  marshal results back to the UI. Use when binding async tasks,
  progress indicators, or long-running I/O to live scenes.
compatibility: Java 21+
metadata:
  domain: ui-javafx
  level: intermediate
  stack: [java-21, javafx-21]
  version: "1.0.0"
---

# Threading in JavaFX

Never block the FX Application Thread. Offload I/O and CPU-bound work
to background threads; update live nodes only via `Platform.runLater()`,
`Task`, or `Service`.

## Core rules
- Use `Task<V>` for one-shot background work with progress callbacks.
- Use `Service<V>` for reusable, restartable background operations.
- Bind `progressProperty()` and `messageProperty()` to UI controls — never
  call `Platform.runLater()` manually when a property binding exists.
- Use Java 21 virtual threads (`Thread.ofVirtual()`) for I/O-bound tasks
  inside `Task.call()`.
- Guard all shared mutable state with `synchronized`, `Atomic*`, or
  immutable records.

## Anti-patterns
- Calling `Thread.sleep()` on the FX thread (freezes the UI).
- Updating `ObservableList` from a background thread (throws
  `IllegalStateException`).
- Catching `InterruptedException` and swallowing it.

## Related
observable-state • async-ui-patterns • layouts
