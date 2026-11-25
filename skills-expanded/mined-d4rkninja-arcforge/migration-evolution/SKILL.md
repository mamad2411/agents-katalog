---
name: migration-evolution
description: "Use when thinking through, reviewing, changing, or verifying data and contract evolution: schema migrations, expand-and-contract, resumable backfills, API or event compatibility, synchronization, CDC, reindexing, traffic cutover, or legacy integration. For outbox and inbox delivery use async-messaging; for transaction invariants use transactions-consistency; for deployment mechanics use runtime-delivery."
---

# Think Through Migrations & Evolution

## Overview

Production guidance for changing running systems safely. Each reference paper captures the sequences that prevent outages: expand-and-contract instead of in-place renames, resumable backfills that do not overwrite newer writes, compatibility windows for old clients, CDC pipelines with reconciliation, and cutover plans with genuine rollback.

**Core principle:** A migration is a distributed system that runs while the old and new versions are both live. Every step must tolerate mixed versions, partial failure, and rollback — code rollback never undoes committed data.

Every response MUST begin with this exact identity shape, before any other prose:

```text
Skill and mode: Think Through Migrations & Evolution (`migration-evolution`) — <Think|Review|Change|Verify>.
```

Replace the angle-bracketed value with the selected mode, or the ordered combined modes when the request spans phases. Do not paraphrase the public display name or technical ID, and do not move this identity below an introduction.

## Domain Law

```text
NO MIGRATION WITHOUT:
1. the minimum required primary paper(s) for the change type selected from the context table;
2. current state, target state, and every intermediate state written
   down before the first migration step;
3. "Existing-codebase checks" run against deployed versions, consumers,
   and retained data — not just the latest code;
4. every applicable MUST mapped to a migration step, a verification gate,
   or a documented exception.
```

## When to Use

Use this skill when thinking through, reviewing, changing, or verifying:

- database schema migrations, online/zero-downtime migrations, lock behavior;
- additive vs destructive changes, column renames, type changes, nullability flips;
- data migrations and backfills: chunking, resuming, idempotency, rate control;
- API and event schema evolution with old consumers;
- backward/forward compatibility windows and deprecation sequencing;
- data synchronization between two systems during transition;
- change data capture pipelines and their failure/replay behavior;
- search index rebuilds and dual-index cutover;
- feature migration: moving behavior between services with traffic cutover;
- legacy integration: strangler patterns, adapters, retirement sequencing.

## When Not to Use

- Transactional outbox/inbox relay, delivery, and replay behavior from paper 047: use `async-messaging`.
- Local transaction and commit invariants that keep the business write and outbox insert atomic: use `transactions-consistency`.
- CI/CD pipeline mechanics and deployment tooling: use `runtime-delivery` (106, 107).
- Whole-system replatforming or rewrite decisions: use `system-architecture-harness` (references 18).
- Contract design for new APIs: use `api-contracts`.

## Select the Operating Mode

| Mode | Use when | Required result |
|---|---|---|
| **Think** | The safe decision is not settled | requirements, constraints, invariants, risks, alternatives, decision, and validation path |
| **Review** | An artifact, repository, diff, or operating state already exists | evidence separated from assumptions, prioritized findings, and blockers |
| **Change** | Decisions are approved and repository changes are requested | the smallest safe change, compatibility notes, and verification still required |
| **Verify** | A claim needs proof | tests or measurements run, observed evidence, and residual risks |

If the user names a mode, use it. Otherwise infer the mode from intent and state the inference in one sentence. For a combined request, run **Think → Review → Change → Verify** and preserve the trace between phases. Think may stop with a decision; Review may stop with findings. Change must not claim completion before Verify. Verify must never turn a planned or unavailable check into evidence.

## Required Context Loading

| Situation | Papers |
|---|---|
| Additive vs destructive schema change, dual-read/dual-write | [029 Schema Evolution](references/papers/029-schema-evolution.md) |
| Online migrations, locks, ordering, rollback limits | [030 Database Migrations](references/papers/030-database-migrations.md) |
| Backfills: chunking, resume, idempotency, load control | [031 Data Migrations & Backfills](references/papers/031-data-migrations-and-backfills.md) |
| Event/API schema versioning and tolerant readers | [070 API / Event Schema Evolution](references/papers/070-api-event-schema-evolution.md) |
| Compatibility windows, old-client behavior | [071 Backward Compatibility](references/papers/071-backward-compatibility.md) |
| Two systems coexisting: precedence and reconciliation | [072 Data Synchronization](references/papers/072-data-synchronization.md) |
| CDC pipelines, replay, failure handling | [073 Change Data Capture](references/papers/073-change-data-capture.md) |
| Dual-index rebuild and cutover | [130 Search Index Synchronization](references/papers/130-search-index-synchronization.md) |
| Deploy ordering for mixed versions | [134 Zero-Downtime Changes](references/papers/134-zero-downtime-changes.md) |
| Moving a feature with traffic cutover | [135 Feature Migration](references/papers/135-feature-migration.md) |
| Strangler patterns and legacy coexistence | [136 Legacy-System Integration](references/papers/136-legacy-system-integration.md) |

Load context in stages:

1. For the minimum required primary paper(s), read the executive engineering summary, pre-implementation questions, and the applicable normative requirements, failure modes, and verification checks needed to establish the obligations.
2. Then read only the named request-specific sections needed to decide or verify this change; record those section names in the output.
3. Treat every other owner paper or section as optional depth. Load it only when the request, a newly discovered dependency, risk, or unresolved evidence gap requires it; promote that depth to required when it becomes necessary.

Never load every paper in this skill by default.

## Workflow

Use the domain workflow as shared gates, then branch by the selected mode:

- **Think:** answer the questions and stop with a reasoned decision and validation path; do not edit by default.
- **Review:** inspect the available artifact or repository and stop with evidence-backed findings; do not claim changes.
- **Change:** apply only approved decisions, then continue to Verify before claiming completion.
- **Verify:** run the relevant checks, report observed results, and label every unavailable or unrun check.

1. Write the current state, target state, and each intermediate state, including which versions can read/write each representation.
2. Apply the staged loading contract above to the change type; do not turn a touched boundary into a full read of every owner paper.
3. Answer the paper's pre-implementation questions; label autonomous assumptions and their impact.
4. Run the existing-codebase checks: inventory deployed clients, consumers, workers, retained messages/jobs, and data that already violates the target shape.
5. Convert each MUST/SHOULD/AVOID/NEVER into ordered migration steps with verification gates between them (counts match, behavior compared, usage at zero) and explicit rollback or roll-forward at each step.
6. Apply the active mode: stop at a sequence decision in Think; stop at findings in Review; make the smallest approved safe change in Change; run mixed-version, backfill-resume, replay, reconciliation, and rollback checks in Verify.
7. Before completion, re-scan the normative lists and stop if any rule lacks a decision, test, or documented exception.

## Companion Skills and Standalone Safety

| Type | When | Companion | Missing companion behavior |
|---|---|---|---|
| **Required** | Transactional outbox or inbox paper 047, relay delivery, replay, or retained old and new consumers are in scope | `async-messaging` | Keep relay, delivery, replay, and retained-consumer semantics unresolved; do not misroute paper 047 or invent unavailable depth. |
| **Required** | The local business write plus outbox insert, transition writes, concurrency, or saga boundaries need an authoritative commit invariant | `transactions-consistency` | Keep the local commit invariant, writers, interleavings, and outcomes unresolved; never replace it with independent database and broker writes. |
| **Required** | Deployment ordering, exact artifacts and versions, startup or readiness gates, rollback, or CI/CD mechanics are in scope | `runtime-delivery` | Stop before prescribing or claiming unverified artifact, pipeline, startup, readiness, deploy, or rollback mechanics. |
| **Recommended** | Compatibility, backfill, or cutover claims need proof | `quality-release` | State exact tests and label them unrun. |

If a companion is unavailable, complete only the safe local migration sequence, name the missing depth, and recommend the exact technical ID or relevant installation group. Never claim unavailable material was read, route paper 047 to `transactions-consistency`, or weaken mixed-version, rollback, reconciliation, or no-dual-write requirements.

### Required companion handoff payloads

Whenever a required companion condition is met, emit an explicit **Receives / Owns / Produces** handoff. Do not substitute a responsibility list for this payload.

- **`transactions-consistency`**
  - **Receives:** the current, target, and intermediate write paths; every writer, retry, old binary, backfill, and administrative path; the local business mutation and outbox insert; candidate commit points; and ambiguous/crash interleavings.
  - **Owns:** the authoritative local commit invariant that the business write and outbox record become durable together in one local transaction or another explicitly proven safe mechanism; enforcement, winner/loser and retry outcomes, and reconciliation when one atomic boundary is impossible. It does not own relay publication, delivery, or consumer replay.
  - **Produces:** the exact invariant, enforcement point, commit point, writer/interleaving matrix, observable outcomes, and constraints the migration sequence must preserve. If unavailable, all of those semantics remain explicitly unresolved; migration-evolution must not invent them.
- **`async-messaging`**
  - **Receives:** the committed outbox/inbox contract and commit point; event identity and schema versions; relay, acknowledgment, retry, and replay boundaries; retained-message horizons; and a complete inventory of retained old and new consumers with their read/processing compatibility.
  - **Owns:** paper 047 relay claim/publication, delivery, acknowledgment, redelivery, deduplication or inbox behavior, poison handling, replay, and retained-consumer coexistence. It does not own the local business-write commit invariant or migration cutover order.
  - **Produces:** relay and replay semantics, consumer/version compatibility obligations, reconciliation and retirement criteria, plus the exact failure and coexistence evidence needed before cutover. If unavailable, these outputs and the retained-consumer inventory remain explicitly unresolved.
- **`runtime-delivery`**
  - **Receives:** immutable source and artifact identity, including exact commit/ref and artifact digest where available; exact old and new artifact or binary versions; the schema/data/event version matrix; deployment ordering constraints; per-stage migration gates; startup compatibility checks; readiness conditions; rollback triggers; irreversible data boundaries; and roll-forward, reconciliation, and cleanup obligations.
  - **Owns:** pipeline, promotion, deployment, startup, readiness, canary, abort, rollback, and roll-forward mechanics against the actual runtime and immutable artifacts. It does not redefine migration compatibility or authority semantics.
  - **Produces:** the exact artifact-bound deployment order, implemented startup/readiness gates, rollback or roll-forward procedure, and observed validation evidence with every unrun check labeled. If unavailable, artifact identity and all runtime mechanics and evidence remain explicitly unresolved.

## Output Contract

The selected mode is authoritative. Include only applicable fields below; a planned check is a validation path, not verification evidence.

Scale the output to the active mode: Think returns current, target, and transition decisions; Review returns findings; Change returns the approved migration sequence plus pending proof; Verify returns observed compatibility, reconciliation, cutover, and rollback evidence with unrun checks labeled. A combined flow preserves all four phases.

1. **Skill and mode** — the mandatory first line with exact public display name, technical ID, and selected or inferred mode.
2. **Papers consulted** — numbers and the sections relied on.
   When transactional outbox paper 047 is in scope, follow this immediately with **Companion ownership**: state explicitly that `async-messaging` owns paper 047 relay publication, delivery, acknowledgment or redelivery, replay, and retained-consumer coexistence, while `transactions-consistency` owns the local business-write-plus-outbox commit invariant and forbids independent database/broker writes. Keep this routing explicit when companions are unavailable and label their outputs unresolved; do not claim paper 047 was consulted when it was not.
3. **State plan** — current, target, and intermediate states with version read/write matrices.
4. **Assumptions and unanswered questions** — labeled, with their design impact.
5. **Rule-to-decision map** — each applicable MUST → migration step, verification gate, and rollback/roll-forward action.
6. **Failure modes addressed** — interrupted backfill, mixed-version writes, replayed old events, rollback with newer data.
7. **Verification evidence** — coexistence tests, resumability drills, count/behavior comparisons, rollback rehearsal.

## Stop Conditions

Stop and revise when any of these appears:

- code is written before current/target/intermediate states are written down;
- the mandatory first-line skill and mode identity is absent, paraphrased, or appears after other prose;
- a triggered required companion lacks Receives, Owns, Produces, or explicit unresolved outputs when unavailable;
- a destructive or renaming change without expand-and-contract sequencing;
- a backfill without chunking, resumability, idempotency, or protection against overwriting newer writes;
- a dual write with no reconciliation or precedence rule;
- a schema/event change with no compatibility window for old clients, consumers, or retained messages;
- a deployment order that lets a version write what another version cannot read;
- a rollback plan that assumes data changes undo themselves;
- a cutover with no traffic verification or reversal trigger;
- a CDC/reindex path with no failure recovery or replay behavior;
- a legacy integration with no retirement criterion;
- any migration MUST downgraded to a TODO without a documented exception.

## References

Eleven production papers under `references/papers/`: 029 Schema Evolution, 030 Database Migrations, 031 Data Migrations & Backfills, 070 API / Event Schema Evolution, 071 Backward Compatibility, 072 Data Synchronization, 073 Change Data Capture, 130 Search Index Synchronization, 134 Zero-Downtime Changes, 135 Feature Migration, 136 Legacy-System Integration. Cross-domain pointers inside the papers name the sibling skill to activate.

Worked example: [a safe column rename through expand-and-contract](examples/worked-example-email-column-rename.md).
