---
name: evolve-schema
description: Change an API or event schema without breaking consumers — classify the change against backward/forward compatibility, run an expand-contract (parallel change) migration, and apply the deprecation policy with dated timelines and brownouts. Use before editing any published OpenAPI, AsyncAPI, JSON Schema, Avro, Protobuf or event-store schema. Not for internal DTOs nobody else consumes.
user-invocable: true
argument-hint: "<contract-file> [--change \"<what you want to change>\"]"
metadata:
  foundry.vertical: dev
  foundry.io: "schema change -> review.v1 + expand-contract plan.v1 + deprecation entries"
license: Apache-2.0
---

# Evolve a schema without breaking anyone

Once a schema is published you no longer own it — you own a promise about it. Every change is
either compatible, or it is a migration with a timeline, a budget and someone else's sprint in it.

The only question this skill answers: **which of the three is this change, and what is the
sequence?**

1. **Compatible** — ship it.
2. **Breaking, avoidable** — restructure it into an expand-contract migration and ship that.
3. **Breaking, unavoidable** — new major version, deprecation timeline, dual running.

## Step 1 — Get the direction of compatibility right

The words are used backwards constantly. Fix them before arguing.

| Term | Definition | Who can upgrade first |
|---|---|---|
| **Backward compatible** | A reader on the **new** schema can read data written with the **old** schema | **Consumers first**, then producers |
| **Forward compatible** | A reader on the **old** schema can read data written with the **new** schema | **Producers first**, then consumers |
| **Full** | Both hold | Either order |
| **Transitive** | The property holds against *all* previous versions, not just the immediately previous one | Required whenever old data is replayable |

Which one you need is a property of your deployment, not a preference:

- **Request payloads (client → server):** you need forward compatibility from the server's point
  of view — old clients keep sending old bodies for a long time after you deploy.
- **Response payloads (server → client):** you need the clients to be tolerant readers, and you
  must never remove or retype a field they already read.
- **Events on a log with replay (Kafka, event store):** you need **FULL_TRANSITIVE**. A consumer
  replaying from offset 0 will meet every version you ever produced. This is the case people
  forget, and it is the one that produces a stuck consumer at 3 a.m.
- **Events on a queue with short retention:** BACKWARD is usually enough; state the retention
  that makes it so.

## Step 2 — Classify the change

Look it up in `references/compatibility-matrix.md` — it covers JSON/OpenAPI, JSON Schema, Avro
and Protobuf per change type. The five that account for most incidents:

| Change | Verdict |
|---|---|
| Add an **optional** response field | Compatible **only if** consumers are documented tolerant readers. Otherwise breaking for strict validators. |
| Add a **required** request field | Breaking. Always. Add it optional, backfill a default, then tighten in a later major. |
| Add a member to a **response** enum | Breaking unless the contract already told clients to tolerate unknown members. Adding to a **request** enum is safe. |
| Remove or rename anything | Breaking. Rename is never a rename — it is add + migrate + remove (Step 3). |
| Change the **meaning** of an existing field while keeping its shape | The worst class: invisible to every automated compatibility checker, and it will silently corrupt consumer behaviour. Never do it. Add a new field. |

The last row deserves the emphasis. `status: "cancelled"` now also meaning "expired" passes
`oasdiff`, passes the schema registry, passes every test, and produces wrong refunds.

Automate what can be automated, and put it in CI:

```bash
oasdiff breaking origin/main:contracts/http/orders.openapi.yaml contracts/http/orders.openapi.yaml
buf breaking --against '.git#branch=main'                     # protobuf
# Confluent-compatible registry: check before publishing
curl -s -X POST -H 'Content-Type: application/vnd.schemaregistry.v1+json' \
  --data @payload.json \
  "$REGISTRY/compatibility/subjects/sales.orders.v1-value/versions/latest?verbose=true"
```

Pin every CLI version from `${CLAUDE_PLUGIN_ROOT}/references/stack-versions.json`.

## Step 3 — Expand-contract (parallel change)

Every avoidable breaking change becomes three deployments. Never two, never one.

### Phase E — Expand

Add the new thing **alongside** the old. Nothing is removed, nothing is required.

- New field/endpoint/topic exists; old one is untouched and still authoritative.
- Producers write **both**. Readers still read the old one.
- The new field is optional in the schema even if it will eventually be required.
- Instrument now: count reads of the old field per consumer (Step 4 depends on this data).

**Gate:** both fields present in production traffic; new-field write rate equals old-field write
rate; zero consumer errors.

### Phase M — Migrate

- Backfill historical data so the new field is populated for old records. Batched, idempotent,
  restartable, with a progress metric.
- Switch readers to the new field, one consumer at a time, behind a flag.
- Reconcile continuously: a job comparing old and new for a sample, alerting on divergence
  above a stated rate (0.01% is a reasonable starting bar).
- Old field is still written, so every switch is reversible by flipping the flag.

**Gate:** backfill complete (a count query proving 0 unpopulated rows in scope); divergence below
threshold for a full business cycle; every known consumer switched.

### Phase C — Contract

- Stop writing the old field; mark it deprecated in the contract with its sunset date.
- Remove it only after the deprecation timeline in Step 4 has fully elapsed **and** usage is zero.
- Remove the flag, the dual write and the reconciliation job in the same change. A migration that
  leaves its scaffolding behind has not finished.

**Gate:** zero reads of the old field for 30 consecutive days; the contract no longer mentions it;
`grep` finds no dual-write code.

For a database column the same three phases apply: add nullable column → dual write → backfill →
switch reads → stop writing old → drop. Never `ALTER ... RENAME` a column on a table a running
application writes to; the deploy is not atomic with the migration and one of the two will be
wrong for the duration.

### The rename special case

There is no such thing as renaming a published field. `customerRef` → `customerId` is:
add `customerId` → write both → migrate readers → deprecate `customerRef` → remove after sunset.
Four deployments and a timeline, for a rename. This is exactly why field names should come from
`domain-modeler`'s glossary before publication and not from whoever typed first.

## Step 4 — Deprecation policy

A deprecation without a date is a decoration. Every deprecated element gets all five:
an announcement date, a sunset date, a named replacement, a measured usage number, and an owner.

| Consumer class | Minimum notice from announcement to removal |
|---|---|
| Internal, same team | 30 days |
| Internal, other teams | 90 days |
| Named partners under contract | 180 days, and check the contract — it may say more |
| Public/anonymous consumers | 12 months |

Rules that make the timeline real:

- **At most two major versions run in parallel.** Announcing v3 starts v1's clock immediately.
- **Announce in the contract and on the wire.** In the contract: `deprecated: true` plus a
  description naming the replacement and the removal date. On the wire: a `Sunset` header
  (**RFC 8594**) carrying the removal date, and the IETF HTTPAPI deprecation header field — that
  one has been standardised, so read its current RFC number from the specification rather than
  writing a number from memory.
- **Measure usage per consumer**, not in aggregate. "Traffic is down to 0.2%" means nothing if
  that 0.2% is your largest customer's nightly batch. Break it down by client id / API key /
  consumer group and name the remaining callers.
- **Brownouts before removal.** Schedule short, announced outages of the deprecated element so
  consumers discover the dependency while it is still a test rather than an incident:
  at 50% of the notice period, 1 hour; at 75%, 4 hours; at 90%, 24 hours. Announce each one, and
  respond to `429`/error reports by naming the caller rather than by cancelling the brownout.
- **Removal condition** is a conjunction: notice period elapsed **AND** (usage zero for 30
  consecutive days **OR** every remaining named consumer has signed off). Silence is not sign-off.
- **One `docs/deprecations.md` table** is the single source of truth, and it is reviewed monthly.

For events, deprecation is per message type, and the retention window is part of the timeline:
you cannot remove a schema version while any consumer can still replay a record written with it.
With 7-day retention the schema can go 7 days after the last write; with infinite retention it
can never go, which is why event-store schemas need upcasting instead (see the matrix reference).

## Step 5 — Make consumers tolerant, in writing

Half of all "breaking" changes are breaking only because consumers validate too strictly. Put
these obligations in the contract description, so they are a promise both ways:

1. **Ignore unknown fields.** No strict deserialisation of responses or events.
2. **Tolerate unknown enum members** by mapping them to an explicit `UNKNOWN` and handling it,
   never by throwing.
3. **Do not depend on field order,** on `null` vs. absent being different, or on the exact
   textual form of an opaque identifier or cursor.
4. **Do not parse human-readable strings.** `title`/`detail` in a problem document are not an API.
5. **Pin the major version, not the minor.** Consumers that pin an exact contract build cannot
   receive additive changes and force every change into a major.

Where you own the consumer, add a test that feeds it a payload with an extra field and an unknown
enum member and asserts it still works. That test is what makes additive changes actually safe
instead of theoretically safe.

## Quality gate

- [ ] Compatibility direction stated (backward / forward / full / transitive) with the reason —
      replay, deployment order, retention.
- [ ] Change classified against `references/compatibility-matrix.md`, with the row cited.
- [ ] Automated check run (`oasdiff` / `buf breaking` / registry compatibility) and its output recorded.
- [ ] If breaking and avoidable: an expand-contract `plan.v1` with three waves and a
      machine-checkable gate on each.
- [ ] If breaking and unavoidable: new major version, deprecation row in `docs/deprecations.md`
      with announcement date, sunset date, replacement, owner and current per-consumer usage.
- [ ] Brownout schedule fixed with dates.
- [ ] Tolerant-reader obligations present in the contract description.
- [ ] Semantic changes to existing fields: rejected outright, replacement field proposed.
- [ ] `contracts/CHANGELOG.md` entry written by a human.
- [ ] `review.v1` emitted with `dimension: "schema-evolution"` and validated with `contract_validate`.

## Progressive disclosure

| File | Load when |
|---|---|
| `references/compatibility-matrix.md` | classifying any change — per-format rules for JSON/OpenAPI, JSON Schema, Avro, Protobuf, plus event-store upcasting |
| `references/deprecation-policy.md` | writing the timeline, the announcement text or the brownout schedule |

## What this skill deliberately does not cover

- **Designing the contract in the first place.** `design-api-contract`.
- **Choosing names.** `domain-modeler` owns the ubiquitous language; a good name avoids most of
  the migrations described here.
- **Database performance of a migration** — locking behaviour, online DDL, index rebuild cost,
  batch sizing under load. The database agents and `foundry-ops` own that; this skill owns the
  *sequence*, not the DDL.
- **Data migration correctness for business logic** (recomputing derived values, currency
  redenomination). That is a domain problem with its own tests.
- **Schema registry operation** — subject naming strategies, cluster setup, ACLs: `foundry-ops`.
- **Contract negotiation with a partner** whose contract forbids the change: `foundry-legal`.
- **Consumer-side code generation.** Generators differ in strictness; this skill tells you what
  the schema may do, not how to configure someone's generator.
