---
name: data-modeling
description: >
  Designs and reviews Ditto data models so concurrent offline edits merge without data
  loss: CRDT type per field (REGISTER, MAP, COUNTER, ATTACHMENT), composite _id, embed
  vs split, document size and BLE budgets, strict-mode migration. Covers Ditto SDK
  4.14.x, 5.0.x, 5.1.x and 5.2.0. Use when someone shares JSON or a SQL schema to
  model in Ditto, or reports lost array appends, counter increments or overwritten
  objects after sync. Not for DQL syntax (write-dql).
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Data Modeling for Ditto

Design collections around how concurrent offline edits merge. Each field is a CRDT;
choosing `REGISTER`, `MAP`, `COUNTER`, `PN_COUNTER` or `ATTACHMENT` determines what
survives when peers reconnect. This skill owns model design; use `write-dql` for query
syntax, or <https://docs.ditto.live/dql/dql> if that skill is unavailable.

## When this skill applies

- "Review this JSON before we ship it to devices that edit offline."
- "We're moving this Postgres schema to Ditto — how should the collections look?"
- "Two tablets added items to the same order and one disappeared."
- "Should line items live in the order document or their own collection?"
- "How should I design `_id` so permissions can scope by store?"
- "Will this document sync fast enough over Bluetooth?"

## Start with the task

Read only the reference sections needed for the request. For a long file, inspect its
contents first, then read the matching section; do not load the entire skill directory.
The README is for installation and verification, not a prerequisite.

| Task | Read |
|---|---|
| Review raw JSON or produce a complete design | [workflow.md](references/workflow.md): intake, rubric and output contract |
| Choose a field's merge behavior | [crdt-types.md](references/crdt-types.md) |
| Resolve SDK differences or migrate strict-mode peers | [versions.md](references/versions.md) |
| Budget size, BLE airtime, observers or metadata growth | [performance.md](references/performance.md) |
| Audit logs, soft deletes, schema evolution, smart upserts, MongoDB Connector | [best-practices.md](best-practices.md), matching section |
| Adapt a worked design | One example: [orders](examples/order-management.md), [chat](examples/chat-messaging.md), [time series](examples/iot-timeseries.md) or [relational migration](examples/relational-migration.md) |

## Establish the baseline

Supports **4.14.x (LTS), 5.0.x, 5.1.x and 5.2.0**. Establish the SDK version and who edits
which fields offline before designing. Ask missing intake questions in one batch;
infer other facts from the supplied JSON when possible and state assumptions.
Intake covers transports, hardware, document growth, binaries, query patterns,
permission scopes and retention; the full checklist is in `references/workflow.md` §1.

**All examples assume `dql_strict_mode = false` on every peer.** This is the 5.x
factory default and the migration target for 4.14.x. The flag is per-peer and runtime
only: apply `ALTER SYSTEM SET dql_strict_mode = false` at every app start. Migrate 4.x
peers before upgrading to v5 so the upgrade changes no merge behavior.

- Lenient writes infer objects as `MAP`; scalars and arrays remain `REGISTER`.
  Lenient reads return every field type without declarations.
- Declare only `COUNTER`, `ATTACHMENT`, or a deliberate `REGISTER` override for an
  object that must remain atomic. Do not add routine MAP/REGISTER declarations.
- Unmigrated strict peers need declarations on both writes and reads; otherwise
  objects store as whole-object registers and undeclared MAP/COUNTER fields disappear
  from query results without an error. Use the transition rules in `references/versions.md`.

## Decisions that prevent data loss

1. **Arrays merge as one last-write-wins register at every depth.** Concurrent appends
   can lose data silently. Use a MAP keyed by stable ID or child documents for
   multi-writer/growing entities. Ordered lists need a sortable field or one writer
   responsible for position; a keyed MAP does not preserve order.
   Use a unique line/entity ID when repeated instances of the same SKU are distinct;
   keying those instances by SKU would collapse independent appends.
2. **Accumulating numbers need `COUNTER` (4.14+).** `SET` arithmetic on a register loses
   concurrent increments. Declare the counter when seeding it on INSERT; a plain number
   creates a register. Model money as integer minor units.
3. **Objects merge per key under the lenient baseline.** Force `REGISTER` only when
   the object must change atomically. A MAP overwrite keeps omitted keys; use dotted
   `UNSET` to remove them. Bulk key churn suggests a child collection.
4. **Decide `_id` at design time.** It is immutable and never a CRDT. Permission rules
   can see only `_id`; put scope values (store/site/tenant/region/user) in a composite
   object ID, e.g. `{ 'store_id': 42, 'order_id': 'o-1' }`. Subfields are queryable
   and indexable; avoid delimiter-joined IDs and redundant scope fields in the body.
5. **Move binary payloads to `ATTACHMENT`.** Bytes are fetched separately and excluded
   from document size. Ask about the MongoDB Connector first: it does not carry
   attachments, so connector-synced collections need inline base64 (as of the 5.2.0 baseline) with a
   strict size budget; see `best-practices.md`.
6. **Budget serialized size including CRDT metadata.** The soft warning is 256 KiB;
   the hard limit is 5 MiB. **5.1+ rejects oversized local writes; 4.14.x/5.0.x log.**
   **5.2.0 drops a replication diff that would push the document over its hard limit** and stops updates to that document until
   eviction/re-sync; see [versions.md](references/versions.md#sdk-520-modeling-implications).
   BLE is roughly 20 KB/s effective,
   so 250 KiB can consume 10+ seconds of airtime; size for the slowest required transport.
7. **Deletes have a retention window.** Default tombstone TTL is 7 days on Small Peers,
   30 on Big Peer (tunable). Longer-offline peers can resurrect deleted documents;
   consider soft deletes when that is unacceptable.

## Embed or split

Default to related data in one document with sub-entities as keyed MAPs: one atomic
write with per-field merge. Split when an entity grows without bound, breaches the
size budget, has a different permission scope, or is accessed independently at scale.

**JOINs require 5.1+**, an indexed or `_id` right-side key, and Small Peers; they are
not supported on Big Peer or in subscriptions. Child references must retain the full
composite parent identity, including its store/tenant scope. Joining only an unscoped
order number can match another store's order. Prefer matching the complete parent
`_id`; a right-side subfield join still requires an index. Consult `write-dql` before
emitting JOIN syntax. On 4.14.x/5.0.x, reassemble with app-side
fetches or denormalized read fields. Use the relational-migration example for the design
tradeoff and `write-dql` for grammar. Execute cookbook statements one at a time:
DQL rejects multi-statement strings.

## Deliver a reviewable design

For a complete JSON review, use the stable finding IDs in `references/workflow.md` §2;
do not invent replacements for rubric IDs. Return:

1. Findings: field path, rubric ID, severity and reason.
2. Recommended collections: per-field CRDT behavior and pasteable INSERT statements.
3. Split decisions: back-reference keys and how reads reassemble on the target version.
4. Budget notes: estimated serialized size, transport implications and observer scope.

For a narrow question, read and answer only the relevant part of that workflow.
