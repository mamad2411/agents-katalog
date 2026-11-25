---
name: immutable-action-event-log
description: Model state transitions as `(state, action) → (newState, List<Event>)` where the event list is an append-only, serializable log. Enables deterministic replay, audit trails, cheat detection, and UI choreography without coupling engine to presentation.
category: arch
tags:
  - event-sourcing
  - immutable-state
  - action-log
  - deterministic
  - replay
  - audit
triggers:
  - action result log
  - state transition events
  - replay log
  - deterministic engine
  - audit trail events
source_project: veda-chronicles
version: 0.1.0-draft
---
