---
name: event-versioning-compatibility
description: >
  Version domain events for owned event-driven systems: schema evolution,
  additive changes, compatibility modes, dual-publish, and consumer contract
  tests. Use when event schema version, Avro/JSON Schema/Protobuf evolution,
  breaking consumer changes, or outbox payload compatibility.
---

# Event Versioning Compatibility

## Scope And Authorization

- **In scope:** Event buses/topics and producers/consumers you operate.
- **Out of scope:** Poisoning external partners’ topics without agreement.
- Breaking events can cascade outages—use staged rollouts.
- Redact PII in example payloads and schema registries.
- Pair with `code-quality-standards` and schema skills (`json-schema-design` if applicable).

## When To Use

- Adding fields or changing meaning of domain events.
- Choosing compatibility mode in a schema registry (FORWARD/BACKWARD/FULL).
- Migrating event type names or partitions.
- Multiple consumer teams on different release cadences.
- Fixing poison messages from incompatible payloads.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| HTTP ETag concurrency | `etag-optimistic-concurrency` |
| Protobuf/gRPC RE | `protobuf-grpc-reverse-engineering` |
| Feature flags for release | `feature-flag-patterns` |
| Implementation quality baseline | `code-quality-standards` |
| Secrets in events | `secrets-management-hygiene` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Compatibility | Prefer additive optional fields |
| Version | Explicit `event_version` or schema id |
| Names | Stable type names; avoid reuse with new meaning |
| Consumers | Tolerate unknown fields; ignore carefully |
| Dual write | Temporary v1+v2 during migration |
| Tests | Consumer-driven contract / schema tests in CI |

## Workflow

### 1. Confirm scope and success criteria

1. Event types, producers, consumers, retention.
2. Success: deploy producer change without forcing all consumers same day; no DLQ storm.

### 2. Inventory events

```bash
rg -n "event_version|schema_id|EventType|CloudEvent" --glob '!node_modules' | head
# List topics / registry subjects in your platform
```

1. Document owners per event type.
2. Note serialization format (JSON, Avro, Proto).

### 3. Classify change

| Change | Compatibility |
| --- | --- |
| Add optional field | Usually backward compatible for consumers |
| Remove field | Breaking for consumers that require it |
| Change type/meaning | Breaking—new version or new type name |
| Rename field | Breaking unless alias period |
| Enum new value | Consumers must default unknown |

### 4. Apply versioning strategy

```json
{
  "event_type": "order.completed",
  "event_version": 2,
  "occurred_at": "2026-07-12T00:00:00Z",
  "data": {
    "order_id": "o_1",
    "total_cents": 1200,
    "currency": "USD"
  }
}
```

1. **In-place additive:** bump minor version; old consumers ignore new fields.
2. **Breaking:** `event_type` + version  or `order.completed.v3`; dual-publish until lag consumers upgrade.
3. Schema registry: set BACKWARD (producer evolves carefully) or FULL as org standard—document choice.
4. Never silently change units (cents vs dollars) without version bump.

### 5. Consumer rules

1. Ignore unknown properties by default (JSON).
2. Unknown enum → safe fallback + metric, not crash loops if possible.
3. Idempotency keys stable across versions when business entity same.
4. Poison pipeline: DLQ + replay after fix.

### 6. Verify with evidence

```bash
# Contract tests: old consumer library parses new sample fixtures
# New consumer parses golden historical events from fixtures/
```

1. CI matrix: producer schemas vs N consumer versions.
2. Stage dual-publish; watch error rates and lag.
3. Rollback plan: stop v2 publish; keep v1.

### 7. Hand off

1. Changelog of event types (like public API).
2. Deprecation window policy (e.g. 90 days).
3. Owners on-call for DLQ of their events.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Evolution | Additive fields | Reuse field for new meaning |
| Version | Explicit version/schema id | Guess from presence of keys |
| Migration | Dual-publish + metrics | Big-bang all services |
| Consumers | Tolerate unknown | Crash on extra fields |
| Docs | Event catalog | Oral tradition only |

## Output Checklist

- [ ] Event catalog with owners
- [ ] Compatibility mode chosen
- [ ] Change classified additive vs breaking
- [ ] Version field/schema id present
- [ ] Consumer tolerance rules implemented
- [ ] CI contract tests for fixtures
- [ ] Migration/deprecation plan
- [ ] Residual risk noted

## Rules

- Treat events as public contracts inside the company.
- Prefer additive evolution; version breaking changes.
- Test old consumers against new payloads before prod.
- Redact sensitive payload examples.
- HTTP resource concurrency → `etag-optimistic-concurrency`.
