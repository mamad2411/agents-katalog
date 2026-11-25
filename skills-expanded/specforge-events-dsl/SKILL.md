---
name: specforge-events-dsl
description: "Write event blocks in .spec files (the event kind is declared by the builtin @specforge/software extension). Each event declares something that happened, with a snake_case ID, a payload type reference, a channel name, verify obligations (with @specforge/testing) and sync/protocol/process links (with @specforge/formal). Use when making a system's reactive behavior explicit and traceable."
---

# SpecForge Events DSL

> **Declared by `@specforge/software`**, a builtin extension. The `event` kind exists only in a project that loads it:
> run `specforge extensions` first, and if it is not listed, do not write `event` blocks (add it with
> `specforge add @specforge/software`, or write the kinds the project's own extensions declare). `verify` needs
> `@specforge/testing`; `sync`, `follows_protocol` and `participates_in` need `@specforge/formal`.
> `specforge infer-guide event` prints the fields.

Events make reactive behavior explicit: a behavior emits an event (`produces`), other behaviors react to it
(`consumes`).

Typed edit: `specforge new event <id> "<title>" --in spec/<file>.spec --payload <Type> --channel "…"`.

## Block Syntax

```spec
event user_created "User Created" {
  channel  "users.created"
  payload  UserCreatedPayload
  category domain

  verify integration "the event is emitted after user creation"
}
```

## Fields Reference

| Field | Type | Declared by | Description |
|-------|------|-------------|-------------|
| `payload` | reference -> type | software | The type describing the event's data. |
| `channel` | string | software | Logical channel, topic or queue name. |
| `channel_type` | identifier | software | Transport, e.g. `queue`, `topic`, `stream`. |
| `category` | identifier | software | Classification, e.g. `domain`, `integration`, `system`. |
| `contract` | string | software | Delivery or ordering guarantees. |
| `description` | string | software | Human-readable summary. |
| `refs` | string list | software | Declared `ref` IDs. |
| `sync` | block | formal | Synchronization bound: barrier, timeout or delivery. |
| `follows_protocol` | reference list -> protocol | formal | Protocols this event follows. |
| `participates_in` | reference list -> process | formal | Processes this event takes part in. |

### Sync block (formal)

```spec
event analysis_complete "Analysis Complete" {
  payload AnalysisReport

  sync {
    barrier [detect_deadlocks, detect_channel_mismatch]
    timeout 30s "all sub-analyses must complete within 30 seconds"
  }
}
```

### Verify kinds

With `@specforge/testing`: `integration`, `unit`, `deadlock_free`, `liveness` (another kind is W009).

## Relationships

An event lists no behaviors: the behaviors that emit or react to it name it (writing `trigger` or `consumers` on an
event is E079), and `specforge trace <event>` lists them.

| Field | Edge | Target |
|-------|------|--------|
| `payload` | `EventCarriesPayloadType` | type |
| behavior's `produces` | `BehaviorProducesEvent` | this event |
| behavior's `consumes` | `BehaviorConsumesEvent` | this event |

## Writing Rules

1. **Past tense names** -- `user_created`, `order_placed`: events describe what happened.
2. **Write the relation on the behavior** -- `produces` / `consumes` live on behaviors.
3. **Payload is a type reference** -- define the shape as a `type` block, then `payload ThatType`.
4. **An event no behavior produces is fine while drafting** -- W007 reminds you.
5. **Add `verify`** -- or W004 fires (with `@specforge/testing`).

## Validation Rules

| Code | Owner | Rule |
|------|-------|------|
| E002 | core | Two events share an ID. |
| E003 / E022 | core | `payload` names nothing, or names an entity that is not a `type`. |
| W007 | software | No behavior produces the event. |
| W004 | testing | No `verify` obligation. |
| W029 | formal | Produced but never consumed. |
| W034 | formal | Produced, with no `sync` bound (reported by `specforge analyze`). |
| E034 | formal | Unmitigated event cycle (reported by `specforge analyze`). |

## Examples

### Event Without Consumers

```spec
event user_email_changed "User Email Changed" {
  channel "users.email-changed"
  payload EmailChangedPayload

  // No behavior consumes it yet -- fine during early development.

  verify integration "the event is emitted after an email update"
}
```

### Cross-Service Event

```spec
event order_placed "Order Placed" {
  channel      "orders.placed"
  channel_type topic
  payload      OrderPlacedPayload
  contract     "Delivered at least once, in order per customer."

  verify integration "the event carries the order details"
  verify liveness    "every consumer eventually processes the event"
}
```

## What NOT to Do

- Do not name events as commands (`send_welcome_email` is a behavior)
- Do not write `trigger` or `consumers` on an event (E079): behaviors list it in `produces` and `consumes`
- Do not define payload fields inline -- reference a `type`
