---
name: event-driven-ui
description: >
  Extends agent's knowledge of event-driven UI architecture in JavaFX.
  Use when multiple views or components need to communicate without direct
  references, using a lightweight event bus for decoupled updates.
compatibility: Java 21+
metadata:
  domain: architecture
  level: intermediate
  stack: [java-21, javafx-21, slf4j]
  version: "1.0.0"
---

# Event-Driven UI

Decouple UI components with a typed event bus. Publishers fire events; subscribers react — no direct references needed.

## Event Bus Design

- **Event** — `record` carrying payload data. Immutable.
- **Bus** — Central registry mapping event type → list of handlers.
- **Publisher** — Calls `bus.publish(event)`.
- **Subscriber** — Registers `handler` for a specific event type.

## Rules

- Events are `record` — no mutable event objects.
- Bus dispatches on FX Application Thread for UI subscribers.
- Weak references for subscribers to prevent memory leaks.
- One bus per module; avoid a single global god-bus.
- Events carry data, not commands — "what happened", not "do this".
- Unregister handlers on view disposal (`onClose`, `dispose()`).

## When to use

- Cross-module communication (e.g., invoice list ↔ payment panel).
- Decoupling background sync from UI updates.
- Replacing deep callback chains.

## When NOT to use

- Parent-child component communication → use direct binding.
- Simple CRUD forms → overkill.

## See also

- mvvm-javafx — events complement property bindings
- offline-first-design — sync events drive UI updates
