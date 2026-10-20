---
name: schema-evolution-compatibility
description: Evolves shared data contracts (events, API payloads, DB columns, protobuf/avro) without breaking live consumers — additive-only changes with optional+default fields, NEVER remove/rename/repurpose a field or reuse a protobuf tag / avro position (reserve them with `reserved`/aliases instead), backward vs forward vs full compatibility chosen per producer/consumer upgrade order, expand-then-contract (dual-write/dual-read) migrations for renames and type changes, and a schema registry (Confluent/Buf) wired into CI to mechanically reject incompatible diffs before merge. Tolerant reader, unknown-field preservation, and explicit versioning when a true break is unavoidable.
when_to_use: Changing a schema that something else already reads or writes — adding/removing/renaming a field on a Kafka event, API JSON payload, protobuf/avro/JSON-Schema, or a DB column other services depend on; deciding if a change is safe to deploy and in what order; or wiring registry compat checks into CI. Distinct from design-protobuf-grpc-service (designs the IDL/RPCs from scratch; this evolves an existing one safely) and db-migration-safety (runs the ALTER without locking/downtime; this decides whether the column change breaks readers at all).
---

## When to Use

Reach for this skill when a contract that *another* process already produces or consumes is changing and you must not break it mid-deploy:

- "Add a field to this Kafka event / API response — will old consumers still parse it?"
- "Rename / remove / change the type of a field that other services read"
- "Which compatibility mode (backward/forward/full) for this Avro subject?"
- "We reused a protobuf field number and a consumer is reading garbage"
- "Deploy producers or consumers first? what's the safe order?"
- "Wire `buf breaking` / Confluent compat checks into CI so bad diffs get blocked"
- "Migrate a column/field rename with zero downtime across services"

NOT this skill:
- Designing the proto/gRPC service, message shapes, and RPCs from scratch → design-protobuf-grpc-service (this skill *evolves* an IDL that already has live readers)
- Running the `ALTER TABLE` itself without locks/downtime (lock-free index, batched backfill, `NOT VALID` constraints) → db-migration-safety (it makes the DDL safe; this skill decides if the column change breaks consumers)
- Designing the relational schema / normalization / keys → design-relational-schema
- The REST/GraphQL field-type and nullability contract for one endpoint → rest-graphql-contract
- API versioning policy, deprecation headers, pagination contracts → api-design-review / design-api-pagination
- Validating one payload against a schema at the edge (request validation) → build-form-validation / validate-data-quality
- Verifying producer and consumer agree via recorded pacts → contract-testing (it tests the agreement; this skill governs how the schema may change)
- Big phased rewrite/cutover of a whole system → plan-strangler-migration

## Steps

1. **Pick the compatibility mode from your upgrade order — it's the whole game.** Compatibility is asymmetric and defined by *who reads data written under the other schema*:

   | Mode | Guarantees | Allowed change | Upgrade FIRST |
   |---|---|---|---|
   | **BACKWARD** | new consumer reads data from old + new producers | **add** optional field (w/ default), **delete** optional field | **consumers** |
   | **FORWARD** | old consumer reads data from new producer | **add** optional field, **delete** field that had a default | **producers** |
   | **FULL** | both directions | **only** add/remove **optional fields with defaults** | either |
   | **\*_TRANSITIVE** | same, but vs **all** prior versions not just the last | — | — |

   Default to **BACKWARD** for events/topics (Confluent's default — consumers lag and replay history, so the new reader must handle old records). Use **FORWARD** when producers ship ahead of consumers. Use **FULL_TRANSITIVE** for long-lived event logs you replay from the beginning. The rule of thumb: **add a field → forward-safe; remove a field → backward-safe; do both safely → only optional+default**.

2. **Additive-only is the safe default. Every new field is optional with a default — never required.** A new *required* field breaks every old producer (forward) and every old record (backward) instantly. Concretely:
   - **JSON / JSON-Schema:** add the key, do NOT add it to `required`, give consumers a default. Keep `additionalProperties` permissive (or `unevaluatedProperties` in 2020-12) so old readers tolerate fields they don't know.
   - **protobuf (proto3):** every field is already optional; new scalar fields default to `0`/`""`/`false`. Just append with a **fresh field number**. Use `optional` (proto3 explicit presence) when you must distinguish "unset" from "zero".
   - **Avro:** a new field **must** carry a `"default"`, or it's neither backward- nor forward-compatible — `{"name":"x","type":["null","string"],"default":null}`. This is the #1 Avro footgun.

3. **NEVER remove, rename, or repurpose a field in place — and NEVER reuse a tag/number/position.** Renaming = remove + add to every consumer; changing a field's *meaning* while keeping its name/number is the worst break because it passes schema checks but silently corrupts data. Reuse of an identifier makes old payloads decode into the wrong field. Reserve instead:
   - **protobuf** — when you drop field `7` (name `email`), reserve both so the number and name can never be re-added:
     ```proto
     message User {
       reserved 7, 9 to 11;          // numbers
       reserved "email", "legacy_id"; // names
       string username = 3;
     }
     ```
   - **Avro** — never reuse a removed field's name; to *rename* keep the old name reachable via `"aliases": ["old_name"]` so readers using the old schema still resolve it.
   - **JSON** — treat a removed key as permanently retired; never recycle a key name for a different type/meaning.

   A type change (e.g. `int32 → string`, `string → enum`) is **not** additive even if the name stays — it's a remove-and-add. Wire-compatible widenings exist in proto (`int32`/`int64`/`uint32`/`bool` are interchangeable on the wire; `sint*`/`fixed*` are **not**) but treat them as breaking unless you've verified the exact pair.

4. **For a true rename or type change, run expand → migrate → contract (dual-write/dual-read).** You cannot atomically change a field across N independently-deployed services. Phase it:

   | Phase | Producer | Consumer | DB column |
   |---|---|---|---|
   | **1 Expand** | write BOTH `old` + `new` | still reads `old` | add `new` col, backfill, dual-write trigger |
   | **2 Migrate** | writes both | switch reads to `new` (fallback to `old`) | — |
   | **3 Contract** | stop writing `old`; reserve it | reads `new` only | drop `old` col (after grace + replay window) |

   Each phase is independently deployable and rollback-safe. The grace window between expand and contract must exceed your **longest consumer lag + replay/retention window** (e.g. Kafka topic retention) so no in-flight or replayed record still needs the old field. The DB column drop is where db-migration-safety takes over.

5. **Deploy in the order the compatibility mode dictates — getting this backwards is the classic outage.**
   - **BACKWARD** change (added/removed optional): deploy **consumers first**, then producers. New consumers can read both shapes; once all consumers handle the new shape, flip producers.
   - **FORWARD** change: deploy **producers first** — old consumers tolerate the new field (they ignore unknowns), then upgrade consumers to use it.
   - **FULL**: either order, but still roll out gradually and watch dead-letter/parse-error metrics during the canary.
   - Never deploy producer and consumer in lockstep assuming atomicity — there is always a window where mixed versions run.

6. **Run a schema registry with mechanical compatibility checks, and gate CI on them.** Humans miss breaks; the registry doesn't.
   - **Confluent Schema Registry** (Avro/Protobuf/JSON-Schema over Kafka): set per-subject mode and test the candidate before publishing — `curl -X PUT .../config/<subject> -d '{"compatibility":"BACKWARD_TRANSITIVE"}'`, then `POST .../compatibility/subjects/<subject>/versions/latest` returns `{"is_compatible": true|false}`. The Maven/Gradle `schema-registry:test-compatibility` goal does this in CI.
   - **protobuf** → **`buf breaking --against '.git#branch=main'`** in CI; rules `FIELD_NO_DELETE` (forces `reserved`), `FIELD_SAME_TYPE`, `RESERVED_*` catch exactly the breaks above. Pair with `buf lint`.
   - **Avro** standalone → `java -jar avro-tools` or the `avro-compatibility` checker; gate the PR.
   - **JSON-Schema** → `json-schema-diff` / `oasdiff` (for OpenAPI) flag breaking changes.

   Make the check **fail the build**, not warn. The registry's `compatibility` setting per subject is the contract; CI is the enforcement.

7. **Write consumers as tolerant readers — ignore unknown fields, never hard-fail on them.** Forward compatibility depends on the *reader's* behavior as much as the schema:
   - JSON: don't use a strict/closed deserializer that throws on unknown keys. Jackson → `@JsonIgnoreProperties(ignoreUnknown = true)` / `FAIL_ON_UNKNOWN_PROPERTIES=false`; Go `encoding/json` ignores unknowns by default (avoid `DisallowUnknownFields`); Pydantic → `model_config = ConfigDict(extra="ignore")` (NOT `"forbid"`).
   - **Preserve, don't drop, unknown fields** on a read-modify-write path, or a round-trip through an old service silently deletes data a newer one added. protobuf keeps unknown fields by default; for JSON, capture them (`@JsonAnySetter`, `additionalProperties` map) and re-emit. This is the subtle one — a "harmless" old service in the middle of a pipeline strips new fields.
   - Always provide a default when a field is absent; don't assume presence.

8. **When a break is genuinely unavoidable, version explicitly — don't mutate in place.** Some changes (splitting one field into two, restructuring nesting, semantic redefinition) can't be made compatible. Then:
   - **Events:** new schema = **new subject / new topic** (`orders.v2`) or an explicit `schema_version` field; run v1 and v2 in parallel; migrate consumers; retire v1 after the replay window. Never silently change `v1`'s meaning.
   - **APIs:** new path/header version (`/v2`, `Accept: application/vnd.api.v2+json`); deprecate v1 with a sunset header and timeline.
   Versioning is the escape hatch, not the default — additive evolution avoids a version bump for the 90% case.

## Common Errors

- **Adding a required field.** Breaks every old producer and every historical record at once. Fix: optional + default, always.
- **Avro field with no `default`.** Silently fails both backward and forward compat. Fix: every Avro field added/removed needs an explicit `"default"`.
- **Reusing a protobuf field number (or Avro position).** Old payloads decode into the wrong field — type-confused garbage that passes schema checks. Fix: `reserved` the number AND the name; only ever append fresh numbers.
- **Renaming a field in place.** It's a delete + add to every consumer simultaneously. Fix: expand→migrate→contract, or Avro `aliases`.
- **Repurposing a field's meaning while keeping its name.** Passes all mechanical checks, silently corrupts semantics. Fix: new field; reserve the old one.
- **Wrong deploy order for the compat mode.** Backward change with producers-first (or forward with consumers-first) → mixed-version outage. Fix: consumers-first for backward, producers-first for forward.
- **Strict deserializer that throws on unknown fields.** Kills forward compatibility the moment a producer adds a field. Fix: tolerant reader (`ignoreUnknown`, `extra="ignore"`, no `DisallowUnknownFields`).
- **Dropping unknown fields on read-modify-write.** An older service in the pipeline silently erases data newer services added. Fix: preserve and re-emit unknown fields.
- **Treating a type widening as free.** `int32→string` or `string→enum` is a break even with the same name; not all proto widenings are wire-safe. Fix: verify the exact pair or run expand→contract.
- **No registry / CI gate.** Relying on review to catch breaks. Fix: `buf breaking` / Confluent compat check that **fails the build**.
- **Checking only against the latest version, not all.** A change compatible with v3 but not v1 breaks replay. Fix: `*_TRANSITIVE` mode for replayable logs.
- **Contracting before the replay/retention window passes.** Dropping the old field while replayable records still reference it. Fix: grace window > longest consumer lag + topic retention.

## Verify

1. **Mechanical compat check passes in CI:** `buf breaking` / Confluent `is_compatible:true` / Avro checker runs on the PR diff and **fails the build** on an incompatible change — proven by intentionally introducing a remove/rename and watching CI go red.
2. **Old-schema read of new data, and vice versa:** serialize a record with the new schema, deserialize with the old (forward); serialize with old, read with new (backward) — both succeed, defaults fill absent fields. This is the literal compatibility definition; test it, don't assume it.
3. **No required field added, every new field has a default:** grep the diff — new fields are optional and defaulted (`"default"` in Avro, not in JSON `required`, appended proto numbers).
4. **Removed fields are reserved:** any dropped proto field has its number AND name in `reserved`; any renamed Avro field has `aliases`; no identifier is reused.
5. **Tolerant reader confirmed:** feed a consumer a payload with an extra unknown field → it parses and ignores it (no exception); on read-modify-write, the unknown field survives the round-trip.
6. **Deploy order documented and rehearsed:** the rollout plan states consumers-first (backward) or producers-first (forward), and a mixed-version canary shows zero parse errors / dead-letters during the window.
7. **Rename via expand→contract, not in place:** the migration is staged (dual-write, switch reads, then drop + reserve) and each phase is independently rollback-safe; the old field is dropped only after the replay window.
8. **Transitive check for replayable logs:** for an event log replayed from offset 0, compat mode is `*_TRANSITIVE` and a candidate is checked against all prior versions, not just latest.

Done = the change is additive (optional + defaulted) or staged through expand→migrate→contract, no field/tag/position is ever removed-without-reserving or repurposed, the compatibility mode matches the deploy order, consumers are tolerant readers that preserve unknowns, and a schema-registry compat check fails CI on any incompatible diff — all proven by the old↔new round-trip and the red-CI test in checks 1–2.
