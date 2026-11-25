---
name: avro-compat-rules
description: >
  Apache Avro schema compatibility rules (BACKWARD, FORWARD, FULL, and TRANSITIVE
  variants) for owned event pipelines and Schema Registry: field defaults, evolution
  patterns, and CI checks. Use when evolving Avro contracts safely across producers
  and consumers — not for corrupting third-party schemas or brokers.
---

# Avro Compat Rules

## Scope And Authorization

- **In scope:** Avro schemas and registries for systems you own (Kafka, Pulsar, files, RPC).
- **Out of scope:** Unauthorized modification of others’ schema registries.
- Incompatible evolution causes production consumer outages — treat schema PRs as production changes.
- Prefer registry-enforced compatibility over honor-system wiki rules.
- Pair with `asyncapi-specs-basics` for channel docs; `code-quality-standards` for codegen.

## When To Use

- Adding/removing/renaming fields in Avro records.
- Choosing BACKWARD vs FORWARD vs FULL (and transitive modes) for a subject.
- Configuring Confluent/Apicurio/Glue-compatible registries.
- Debugging `Schema being registered is incompatible` errors.
- Planning multi-version consumer rollout order.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| AsyncAPI channel layout | `asyncapi-specs-basics` |
| Protobuf evolution | Protobuf/gRPC skills |
| Kafka ACL/security | Kafka security skill |
| JSON Schema only | JSON schema skill (`json-schema-design`) |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Mode | Reader/writer assumption | Practical meaning |
| --- | --- | --- |
| BACKWARD | New schema reads old data | Consumers upgraded first can read new+old if carefully… **Registry default often: new schema can read data written by previous** |
| FORWARD | Old schema reads new data | Producers can upgrade first |
| FULL | Both BACKWARD and FORWARD | Safest for mixed fleets |
| *_TRANSITIVE | Holds across all historical versions | Stronger than checking only last version |

Clarify with your registry docs: Confluent’s BACKWARD means a new schema can be used to read data written with the previous schema (consumers upgrade first). Align team language with the registry you use.

## Evolution Cheat Sheet

| Change | Usually OK when | Risk |
| --- | --- | --- |
| Add field with **default** | BACKWARD / FULL | Without default breaks old readers in some modes |
| Remove field with default previously | FORWARD considerations | Old writers still emit field — OK; new writers omit |
| Delete required field | Often **incompatible** | Breaks readers expecting it |
| Rename field | **Incompatible** unless aliases | Use `aliases` |
| Change field type | Often incompatible | Prefer add new field + deprecate |
| Add enum symbol | Careful | Old readers may fail unknown symbols |
| Change namespace/name | New subject / careful compat | May look like different type |

## Example Evolution

**v1**

```json
{
  "type": "record",
  "name": "OrderCreated",
  "namespace": "com.example.orders",
  "fields": [
    { "name": "order_id", "type": "string" },
    { "name": "total_cents", "type": "long" }
  ]
}
```

**v2 — add optional field with default (common BACKWARD-friendly)**

```json
{
  "type": "record",
  "name": "OrderCreated",
  "namespace": "com.example.orders",
  "fields": [
    { "name": "order_id", "type": "string" },
    { "name": "total_cents", "type": "long" },
    { "name": "currency", "type": "string", "default": "USD" }
  ]
}
```

**Rename via aliases**

```json
{ "name": "orderId", "type": "string", "aliases": ["order_id"] }
```

## Workflow

### 1. Confirm scope and success criteria

1. Record subjects, registry URL, compatibility mode per subject, producer/consumer deploy order.
2. Success: new schema registers; old consumers still process; CI blocks incompatible changes.
3. Identify peak deploy matrix (can both versions coexist?).

### 2. Inventory schemas and modes

```bash
# Confluent-style examples
curl -sS "$SCHEMA_REGISTRY/subjects"
curl -sS "$SCHEMA_REGISTRY/config/order-created-value"
curl -sS "$SCHEMA_REGISTRY/subjects/order-created-value/versions/latest"
```

1. List subjects and current compatibility.
2. Export last N versions for transitive review.
3. Map which services produce/consume each subject.

### 3. Baseline

1. Store current schema files in Git as SSOT if not already.
2. Capture a sample of production payloads (redacted) for decoder tests.
3. Note any `null` unions already in use (`["null","string"]` defaults).

### 4. Apply evolution safely

1. Prefer **add field + default** over rename/type change.
2. Use unions with `null` + default `null` for optional fields when appropriate.
3. Deprecate fields in docs; remove only when FULL/FORWARD rules and fleet allow.
4. Set subject compatibility explicitly:

```bash
curl -sS -X PUT -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data '{"compatibility":"FULL_TRANSITIVE"}' \
  "$SCHEMA_REGISTRY/config/order-created-value"
```

5. Register via CI service account; deny human permanent wide delete on subjects.

**Local check (example tools):**

```bash
# If using Confluent or community compatibility checkers in CI
# java -jar avro-tools.jar compile schema OrderCreated.avsc generated/
# Project-specific: mvn schema-registry:test-compatibility
```

### 5. Verify with evidence

1. Register schema in **dev** registry first — expect HTTP 200; incompatible → 409.
2. Consumer test: decode v1 payload with v2 schema and vice versa as mode requires.
3. Canary producer upgrade under monitoring.

```bash
curl -sS -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data '{"schema":"{\"type\":\"record\",...}"}' \
  "$SCHEMA_REGISTRY/subjects/order-created-value/versions"
```

### 6. Observe and harden

1. Metrics: serializer/deserializer errors, DLQ rates after deploy.
2. Alert on compatibility config changes to weaker modes.
3. Periodic cleanup of abandoned subjects with owner approval.

### 7. Hand off

1. Document per-domain default mode (often FULL or BACKWARD_TRANSITIVE).
2. Producer/consumer upgrade runbooks per mode.
3. Link AsyncAPI channel docs to schema subject names.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Add field | with default | required field, no default |
| Rename | aliases + dual-read | silent rename |
| Mode | FULL for mixed fleets | NONE in production |
| CI | registry compat gate | “just push schema” |
| Enum | additive with care | reorder/remove symbols casually |
| Docs | subject + mode + owners | tribal knowledge only |

## Output Checklist

- [ ] Subjects, registry, modes, owners recorded
- [ ] Baseline schemas and samples captured
- [ ] Evolution uses defaults/aliases appropriately
- [ ] Compatibility mode set intentionally (prefer transitive in prod)
- [ ] Dev registry registration evidence
- [ ] Cross-version decode tests pass
- [ ] CI blocks incompatible schemas
- [ ] Consumer/producer rollout order documented
- [ ] `code-quality-standards` applied if tooling shipped

## Rules

- Owned registries only; schema changes are production events.
- Prefer FULL or transitive modes when readers/writers intermix.
- Never set production compatibility to NONE without expiry and ticket.
- Defaults and aliases are your primary evolution tools.
- Focus on Avro compatibility; channel design and broker ACLs live in neighbor skills.
