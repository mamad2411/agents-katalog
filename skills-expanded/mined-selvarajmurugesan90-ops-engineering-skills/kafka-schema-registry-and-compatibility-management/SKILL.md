---
name: kafka-schema-registry-and-compatibility-management
description: >
  Manages Avro/Protobuf/JSON Schema in a schema registry for Kafka topics,
  including compatibility mode selection (backward/forward/full) and
  schema evolution that doesn't break existing consumers. Use when the
  user asks to "register a Kafka schema," "change compatibility mode,"
  "evolve an Avro schema without breaking consumers," "add a field to a
  Kafka message schema," or troubleshoots a schema-registry rejection or a
  consumer deserialization failure after a schema change.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: messaging-and-data-orchestration
  maturity: stable
---

# Kafka Schema Registry and Compatibility Management

## Purpose

Kafka itself is schema-agnostic — it stores bytes. A schema registry
(Confluent Schema Registry, Apicurio, AWS Glue Schema Registry, or
equivalent) adds the contract that lets producers and consumers evolve
independently without breaking each other, by validating every new schema
version against a configured compatibility mode before it's allowed to be
registered. Getting the compatibility mode wrong, or evolving a schema in
a way the mode doesn't actually permit, produces either an accidental
production outage (consumers failing to deserialize a new message) or a
false sense of safety (a compatibility check that technically passes but
still breaks downstream logic). This skill covers choosing the right mode
and evolving schemas safely within it — the topic/partition-level
configuration this schema sits on top of is covered in
[kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md).

## When to use

- Registering the first schema version for a new Kafka topic.
- Adding, removing, renaming, or changing the type of a field in an
  existing Avro/Protobuf/JSON Schema used on a Kafka topic.
- Choosing or changing a subject's compatibility mode
  (`BACKWARD`, `FORWARD`, `FULL`, and their `_TRANSITIVE` variants, or
  `NONE`).
- Diagnosing a producer's schema registration being rejected by the
  registry, or a consumer failing to deserialize messages after a schema
  change elsewhere.
- Planning a breaking schema change (field type change, required-field
  removal) that genuinely cannot be done compatibly, and needs a
  new-topic/dual-write migration instead.

## Prerequisites & environment

- A schema registry deployed and reachable from both producers and
  consumers (Confluent Schema Registry, Apicurio Registry, or a
  cloud-managed equivalent like AWS Glue Schema Registry — API shape
  differs by product; examples here use the Confluent Schema Registry
  REST API, which is also implemented by several open-source
  alternatives).
- Serializers/deserializers on the client side configured to use the
  registry (`KafkaAvroSerializer`/`KafkaAvroDeserializer` or the
  Protobuf/JSON Schema equivalents) — schemas registered but not actually
  used by the client serialization path provide no protection.
- Agreement within the team on subject naming strategy — `TopicNameStrategy`
  (one schema per topic, the common default), `RecordNameStrategy`, or
  `TopicRecordNameStrategy` (multiple record types per topic) — decided
  before registering the first schema, since changing strategy later
  means re-registering under different subject names.
- For Protobuf/Avro: familiarity with each format's specific
  compatibility rules — they are not identical (e.g. Avro requires
  `default` values for compatible field additions; Protobuf's field-number
  based wire format has different safe/unsafe change rules).

## Step-by-step guidance

1. **Choose a compatibility mode deliberately per subject, not by
   accepting the registry's global default unexamined.** Set it
   explicitly when the subject is created:
   ```bash
   curl -X PUT -H "Content-Type: application/vnd.schemaregistry.v1+json" \
     --data '{"compatibility": "BACKWARD"}' \
     http://schema-registry:8081/config/order-events-value
   ```
   - `BACKWARD` (most common default): new schema can read data written
     with the *previous* schema — safe when consumers upgrade before
     producers, i.e. deploy new consumer code first, then start
     producing with the new schema.
   - `FORWARD`: old schema can read data written with the *new* schema —
     safe when producers upgrade before consumers, i.e. it's fine if some
     consumers haven't upgraded yet when new-format messages start
     flowing.
   - `FULL`: both directions hold — safest but most restrictive; use for
     topics with many independent consumer teams where you can't control
     or know everyone's upgrade order.
   - `_TRANSITIVE` variants (`BACKWARD_TRANSITIVE`, etc.) check
     compatibility against *all* previous versions, not just the
     immediately prior one — use when a topic has a long history and a
     consumer might still be running code from several versions back.
   - `NONE` disables checking entirely — treat this as a deliberate,
     documented exception (e.g. a topic with a single producer and
     single consumer deployed in lockstep), never a default.

2. **Add fields as optional with a default, never as required, for
   backward-compatible evolution** (Avro example):
   ```json
   {
     "type": "record",
     "name": "OrderEvent",
     "fields": [
       {"name": "order_id", "type": "string"},
       {"name": "customer_id", "type": "string"},
       {"name": "amount_cents", "type": "long"},
       {"name": "currency", "type": "string", "default": "USD"}
     ]
   }
   ```
   Adding `currency` with a `default` is backward-compatible: old data
   (without the field) deserializes fine into the new schema, using the
   default. Adding it *without* a default breaks `BACKWARD` compatibility
   — the registry will reject registration of that schema version.

3. **Never remove a field or change its type in place** — both break
   compatibility in every mode except `NONE`. To retire a field safely:
   mark it deprecated in a comment/doc, stop populating meaningful data
   in it, but leave it declared (with a default) for at least one full
   deprecation window before actually removing it, and only remove it
   once every consumer has confirmed they've stopped reading it.

4. **For a genuinely breaking change** (a required type change, a field
   rename with different semantics, a restructured nested record), don't
   force it through the existing subject — create a new topic (and new
   subject) for the new schema version, dual-write to both old and new
   topics during a migration window, and cut consumers over on their own
   schedule before retiring the old topic:
   ```bash
   # register the new shape under a distinct topic/subject rather than
   # trying to coerce an incompatible change through the existing one
   curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
     --data '{"schema": "{...new OrderEventV2 schema...}"}' \
     http://schema-registry:8081/subjects/order-events-v2-value/versions
   ```

5. **Validate a proposed schema change against the registry before
   deploying the producer**, as an explicit CI step rather than
   discovering incompatibility at deploy time:
   ```bash
   curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
     --data '{"schema": "{...new schema...}"}' \
     http://schema-registry:8081/compatibility/subjects/order-events-value/versions/latest
   ```
   A response of `{"is_compatible": false}` should fail the build, the
   same way a failing unit test would — this check belongs in the same
   CI gate that
   [kafka-configuration-validation](../kafka-configuration-validation/SKILL.md)
   uses for topic config, run against every schema-affecting change.

6. **For Protobuf specifically, never reuse or renumber a field number**
   — Protobuf's wire compatibility is keyed on field number, not name:
   ```protobuf
   message OrderEvent {
     string order_id = 1;
     string customer_id = 2;
     int64 amount_cents = 3;
     // reserve retired field numbers so they're never accidentally reused
     reserved 4;
     reserved "legacy_status";
     string currency = 5;
   }
   ```
   Reusing field number `4` for an unrelated new field after it was once
   used for `legacy_status` causes old messages (serialized against the
   old meaning of field 4) to be misinterpreted under the new schema —
   `reserved` prevents the registry/compiler from allowing that reuse
   silently.

7. **Confirm consumers are actually configured to fetch and cache schema
   versions from the registry**, not hardcoding a schema client-side —
   a hardcoded consumer-side schema defeats the entire point of registry
   validation, since it won't pick up compatible changes and will fail
   unpredictably on incompatible ones instead of failing at registration
   time where the mistake is caught early.

## Best practices

- Default new subjects to `BACKWARD` (or `FULL` for topics with many
  independent consumer teams) rather than leaving the registry's global
  default unexamined for each new subject.
- Add new fields as optional with sensible defaults; treat "remove a
  field" and "change a field's type" as always requiring a deprecation
  window or a new schema version, never a direct in-place edit.
- Run schema compatibility checks in CI against the registry's
  `/compatibility` endpoint before merging a producer change, the same
  way a database migration gets checked against the current schema
  before deploy.
- Use `TopicRecordNameStrategy` (or `RecordNameStrategy`) instead of the
  default `TopicNameStrategy` for any topic that carries more than one
  logical record type — otherwise the registry can't distinguish
  compatibility rules per record type sharing a topic.
- For Protobuf schemas, always `reserve` retired field numbers and names;
  for Avro schemas, always give new fields a `default` — these are the
  two most common compatibility footguns per format.
- Keep schemas in version control alongside the producer/consumer code
  that uses them, with the registry as the enforced source of truth at
  runtime, not the only place the schema is defined.

## Common pitfalls

- **Symptom:** A producer deploy fails with a schema registration
  rejection (`409 Conflict` / `"Schema being registered is incompatible
  with an earlier schema"`), blocking the deploy.
  **Fix:** This is the registry doing its job — check what changed
  (usually a field removed, a type changed, or a new required field with
  no default) via the `/compatibility` check output, and fix the schema
  to be additive-with-defaults instead of forcing it through by loosening
  the subject's compatibility mode to `NONE`, which would remove the
  protection for every future change on that subject too.

- **Symptom:** Consumers start throwing deserialization errors
  immediately after a schema change that *did* pass the registry's
  compatibility check.
  **Fix:** The compatibility mode may be checking against only the
  immediately previous version (`BACKWARD`) while a consumer still
  running much older code needs compatibility against a version several
  releases back. Switch the subject to the `_TRANSITIVE` variant
  (`BACKWARD_TRANSITIVE`) so every new version is checked against the
  full version history, not just its immediate predecessor, and confirm
  which consumer versions are actually still deployed before assuming
  everyone is on recent code.

- **Symptom:** A Protobuf schema change passes review and compatibility
  checks (Protobuf's built-in wire compatibility doesn't catch this
  class of issue) but old messages start being misread after deploy —
  fields showing wrong or garbled values.
  **Fix:** A field number was reused after being retired (e.g. a
  removed `legacy_status` field's number `4` was assigned to an
  unrelated new field). Protobuf compatibility checks catch type/wire
  mismatches but won't stop semantically-wrong reuse of a `reserved`-less
  field number. Always mark retired field numbers and names `reserved`
  so this class of mistake becomes a compile-time error instead of a
  silent data-corruption bug.

- **Symptom:** Two different logical record types are published to the
  same topic (e.g. `OrderCreated` and `OrderCancelled`), and registering
  a compatible change to one record type gets rejected because the
  registry is comparing it against the other record type's schema.
  **Fix:** The subject is using the default `TopicNameStrategy`, which
  assumes one schema per topic. Switch to `RecordNameStrategy` or
  `TopicRecordNameStrategy` so each record type gets its own subject
  (and its own independent compatibility history) even though they share
  a topic.

## Worked example

**Scenario:** The `order-events` topic (Avro, `BACKWARD` compatibility,
`TopicNameStrategy`) needs a new `discount_code` field added to support a
new promotions feature, and separately a `legacy_shipping_method` field
needs to be retired.

Current registered schema (v3):
```json
{
  "type": "record",
  "name": "OrderEvent",
  "fields": [
    {"name": "order_id", "type": "string"},
    {"name": "customer_id", "type": "string"},
    {"name": "amount_cents", "type": "long"},
    {"name": "currency", "type": "string", "default": "USD"},
    {"name": "legacy_shipping_method", "type": ["null", "string"], "default": null}
  ]
}
```

Proposed v4 schema: add `discount_code` with a default (compatible
addition), and stop populating `legacy_shipping_method` in the producer
while leaving the field declared (deprecation window, not immediate
removal):
```json
{
  "type": "record",
  "name": "OrderEvent",
  "fields": [
    {"name": "order_id", "type": "string"},
    {"name": "customer_id", "type": "string"},
    {"name": "amount_cents", "type": "long"},
    {"name": "currency", "type": "string", "default": "USD"},
    {"name": "legacy_shipping_method", "type": ["null", "string"], "default": null},
    {"name": "discount_code", "type": ["null", "string"], "default": null}
  ]
}
```

CI compatibility check before merge:
```bash
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data @order-event-v4.json \
  http://schema-registry:8081/compatibility/subjects/order-events-value/versions/latest
# {"is_compatible": true}
```
The check passes because `discount_code` is nullable-with-default and no
existing field's type or presence changed. `legacy_shipping_method`
remains declared (still `BACKWARD`-compatible for any consumer still
reading it) — a follow-up ticket tracks removing it entirely once
telemetry confirms no consumer has read a non-null value for it in the
agreed deprecation window, at which point it becomes a v5 schema change
reviewed the same way.

## Cross-references

- [kafka-cluster-configuration](../kafka-cluster-configuration/SKILL.md) — the topic-level design this schema layer sits on top of.
- [kafka-configuration-validation](../kafka-configuration-validation/SKILL.md) — the broader pre-production validation gate this schema-compatibility check should run alongside.
- [kafka-consumer-lag-and-partition-troubleshooting](../kafka-consumer-lag-and-partition-troubleshooting/SKILL.md) — a consumer stalled on repeated deserialization errors after an incompatible schema change can present similarly to lag caused by a slow consumer, but needs this skill's fix instead.
