---
name: couchbase-migration-execution
description: "Execute data migrations into Couchbase from MongoDB, PostgreSQL, MySQL, Oracle, SQL Server, DynamoDB, Cassandra, files, or custom sources. Use whenever the user asks about migrating, migration strategy, dual-write, change data capture / CDC, Debezium, AWS DMS, big-bang vs phased migration, strangler-fig, cutover, rollback, cbimport, cbexport, cbtransfer, validation after migration, count parity, traffic switching, feature flags during migration, reconciliation between source and target, or 'how do I move my data from X to Couchbase.' Triggers on operational mechanics distinct from couchbase-data-modeling (modeling AFTER migration) — this skill is about actually MOVING the data, keeping source and target in sync during transition, validating equivalence, switching traffic, and rolling back if needed. Use proactively for migration planning, ETL pipeline design, dual-write patterns, CDC tool selection, cutover runbooks, and migration rollback decisions."
license: MIT
---

# Couchbase migration execution

A skill for *executing* data migrations into Couchbase — the mechanics of moving data, keeping source and target in sync during transition, validating equivalence, and switching production traffic.

Distinct from the sibling skills:
- `couchbase-data-modeling` — how to MODEL the data after migrating (document shape, boundaries, access patterns)
- `couchbase-sizing` — how to size the target cluster
- `couchbase-app-integration` — how to write app code that uses Couchbase (relevant during dual-write)
- `couchbase-mcp` — operating the cluster (creating the target, running queries during validation)
- **`couchbase-migration-execution` (this skill)** — the operational mechanics of moving data and switching over

If the conversation is "how do I get my data from X into Couchbase," this is the right skill.

## When this skill applies

- "How do I migrate from MongoDB / Postgres / DynamoDB / MySQL to Couchbase?"
- "Should I do a big-bang migration or phased?"
- "What's dual-write?"
- "How do I keep the source and target in sync during migration?"
- "Can I use CDC for this?"
- "How do I validate the migration worked?"
- "How do I cut over production traffic?"
- "What if the migration goes wrong — can I roll back?"
- "Tooling for bulk loading into Couchbase?"

## Pick the right reference

| Question | Read |
|---|---|
| "Big-bang vs phased vs strangler-fig vs dual-write — which approach?" | `references/strategies.md` |
| "What tools exist — cbimport, ETL frameworks, CDC tools?" | `references/tooling.md` |
| "Migrating from MongoDB specifically" | `references/from-mongodb.md` |
| "Migrating from PostgreSQL / MySQL / Oracle / SQL Server" | `references/from-relational.md` |
| "Migrating from DynamoDB / Cassandra / files / something else" | `references/from-other-sources.md` |
| "Dual-write code patterns, CDC setup, keeping source and target in sync" | `references/dual-write-and-cdc.md` |
| "Validating the migration + cutting over + rolling back if needed" | `references/validation-and-cutover.md` |

## The five-question pre-migration checklist

Before any data moves, get answers to these. Without them, migrations turn into multi-week troubleshooting sessions:

1. **What's the source?** Database type, version, total size, current write rate. Different sources have very different migration shapes
2. **Can the source go offline?** If yes (planned downtime acceptable): big-bang is on the table. If no: you need dual-write or CDC
3. **What's the modeling change?** Direct table-to-collection translation or a re-model? See `couchbase-data-modeling` skill — the answer here determines whether you can use simple bulk tools or need transformation code
4. **What's the rollback bar?** If something goes wrong post-cutover, can you tolerate going back to the source (probably yes for the first hour, probably no after a week)?
5. **What's the validation plan?** Count comparison? Sample comparison? Checksum? Automated test suite? Decide before starting

If the user hasn't thought through these, walk them through them before suggesting any specific approach.

## The four migration approaches at a glance

| Approach | When it fits | Downtime | Complexity | Risk |
|---|---|---|---|---|
| **Big-bang** | Small data, planned downtime OK | Yes | Low | High (no rollback once cut over) |
| **Phased / table-by-table** | Multi-domain app, can migrate one slice at a time | Per-slice downtime | Medium | Medium |
| **Dual-write** | Need zero downtime, can modify app code | Zero | High | Low if done carefully |
| **CDC-based** | Need zero downtime, can deploy CDC tooling | Zero | High but mechanical | Low if validated |

`strategies.md` covers each in detail with the decision framework.

## Three principles for any migration

**Principle 1 — Validate at every step.**
A migration is only as good as your confidence that source == target. Count comparison, sample comparison, and checksum verification at each step catch problems early. Defer validation to the end and a single bad transformation can corrupt everything.

**Principle 2 — Make the cutover reversible for as long as possible.**
The first cutover should be: cut traffic to the new system, monitor for problems, cut back to source if needed. Keep source running in read-only mode for at least days, ideally weeks. The hardest migrations are the ones that decommissioned the source on day 1.

**Principle 3 — Migrations are projects, not commands.**
Even "simple" migrations from MongoDB to Couchbase typically take weeks of work: test the tooling, dry-run on a sample, validate, do a partial migration in staging, validate, set up dual-write or CDC, run for a soak period, plan cutover, execute, monitor, decommission source. Don't let the user expect "I'll just run `cbimport` and we're done."

## Common migration shapes

Recognize which shape the user is dealing with:

| Source | Typical shape | Reference |
|---|---|---|
| MongoDB → Couchbase | Schema is similar; mostly KV format mapping; tools exist | `from-mongodb.md` |
| Postgres / MySQL / SQL Server / Oracle → Couchbase | Major modeling change; relational JOINs → denormalization | `from-relational.md` |
| DynamoDB → Couchbase | Schema is similar; partition-key concept maps to document key | `from-other-sources.md` |
| Cassandra → Couchbase | Similar to DynamoDB; wide-column → document with arrays | `from-other-sources.md` |
| Files (CSV, JSON, Parquet) → Couchbase | One-shot bulk load; `cbimport` shines | `from-other-sources.md` + `tooling.md` |
| Custom application export → Couchbase | ETL code; the source has whatever shape you wrote | Depends; usually like file load |

## What this skill won't help with

- **Designing the target model** — see `couchbase-data-modeling` for that. This skill assumes the target model is decided
- **Sizing the target cluster** — see `couchbase-sizing`. Migrations need correctly-sized target clusters; this skill assumes that's done
- **Operating the cluster** — see `couchbase-mcp`. Bucket / index / user creation on the target happens via that skill
- **Application code that uses Couchbase** — see `couchbase-app-integration`. The dual-write phase needs application code; this skill references the patterns but the SDK details live there
- **Couchbase Mobile / Sync Gateway migrations** — different product; out of scope

Hand off explicitly when the conversation crosses these lines.

## A typical migration timeline

For a moderate-size migration (10-100 GB), expect roughly:

| Phase | Duration | What happens |
|---|---|---|
| Planning | 1-2 weeks | Modeling, sizing, approach selection, validation plan |
| Tooling setup | 1 week | Install / configure cbimport, ETL framework, or CDC tool |
| Dry run on sample | 1 week | Migrate a representative subset; validate; iterate |
| Staging migration | 1 week | Full migration in staging environment; full validation |
| Dual-write setup | 1-2 weeks | App code changes for dual-write or CDC setup |
| Soak period | 2-4 weeks | Source and target in sync; validate continuously |
| Cutover | 1 day | Switch traffic; monitor |
| Soak post-cutover | 2-4 weeks | Source still running read-only; rollback possible |
| Decommission source | 1 day | After successful soak, retire the source |

**Total: 8-16 weeks** for non-trivial production migrations. Big-bang migrations on small datasets can compress to days; large active-active dual-write migrations can stretch to months.

Don't surprise the user with this timeline — set the expectation up front. Migration projects that get "we'll be done by Friday" framing fail.

## Quick decision tree

- **Downtime allowed, small data, no live system?** → Big-bang with `cbimport`
- **Multi-domain app, can do it in slices?** → Phased / strangler-fig pattern
- **Live system, zero downtime, can modify app?** → Dual-write
- **Live system, zero downtime, can't modify app?** → CDC-based (Debezium, AWS DMS, etc.)
- **Source is MongoDB or DynamoDB?** → Document-to-document; tooling does most of the lift
- **Source is relational?** → Modeling change required; ETL code or careful CDC transformation
- **Unsure where to start?** → Read `strategies.md` and answer the five-question checklist

## Related skills

- `couchbase-data-modeling` — the modeling transformation that often accompanies migration
- `couchbase-sizing` — sizing the target cluster before data starts moving
- `couchbase-app-integration` — writing the dual-write layer in application code
- `couchbase-mcp` — creating the target bucket/scope/collection and running validation queries
