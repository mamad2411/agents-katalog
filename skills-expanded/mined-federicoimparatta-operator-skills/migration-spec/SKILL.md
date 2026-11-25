---
name: migration-spec
description: Use this skill when the user asks to plan a platform-to-platform migration, data migration, system rebuild, or cutover from a legacy product to a new one. Trigger phrases include "migration plan", "cutover plan", "migrate from X to Y", "legacy sunset", "replatforming", "plan de migración", "migrar este sistema", "cutover", "data migration". Produces a migration spec structured around parity, cutover, and rollback, with an inventory-level matrix.
---

# migration-spec

> **Anchor:** A migration fails at the edges. Plan parity, cutover, and rollback in that order.

## When to use

Use this skill when the user needs to specify the work required to move from one system to another. Works for:

- Platform-to-platform migration (CRM, analytics, CMS, e-commerce, auth provider, billing).
- Data migration from a legacy database to a new schema.
- Monolith-to-services rewrites where parity with the current product is required.
- Account migration between tenants, regions, or corporate entities.

Do not use when:

- The user is shipping a new feature inside an existing system. Use `prd-authoring`.
- The user is scoping a custom build with no legacy source. Use `proposal-scoping`.
- The user is rebuilding a dashboard from the same data. Use `dashboard-spec`.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: cutover, rollback, freeze, dual-run, parity, schema, backfill, source of truth, kickoff.
- **EN.** Direct US business register. Write the document in the language of the decision maker who signs off on the cutover, not the language of the engineers doing the work.
- Object names (tables, columns, API fields) stay in their original casing and language.

## Method

### Step 1. Lock the boundary before you start

Write in one page:

- **Source system.** Name, owner, version, known quirks.
- **Target system.** Name, owner, version, known quirks.
- **In scope.** Domains, modules, data ranges, user segments that will migrate.
- **Out of scope.** What stays on the source, permanently or temporarily.
- **Dual-run window.** Will source and target run in parallel, and for how long.

If any of these is unknown, the spec is not ready. The cost of writing a migration plan on fuzzy boundaries is a second migration.

### Step 2. Build the inventory

Every object that might need to move is one row. Nothing is too small to inventory.

For each row:

- **Object.** The table, entity, module, feature, document type, or report.
- **Source location.** Where it lives today.
- **Volume.** Count, size, and rate of change.
- **Ownership.** Who owns the data or the behavior on the source.
- **Classification.** Migrate as-is, transform, drop, or park.
- **Target location.** Where it will live. "New" if it has no direct target.
- **Risk.** Low, medium, high. The reason in one line.

"Park" means leave on the source system in read-only mode. This is often the right answer for low-value historical data and is cheaper than a full migration.

### Step 3. Write the parity matrix

For every object classified as migrate or transform, write a parity row:

- **Source shape.** Fields, types, constraints, enum values.
- **Target shape.** Fields, types, constraints, enum values.
- **Mapping.** Field-by-field, including transformations.
- **Identity strategy.** How records are matched. Natural key, surrogate, deterministic hash, new ID on target.
- **Gaps.** Anything that cannot be represented on the target, or that loses fidelity.

A gap that cannot be closed becomes a parked exception, a product decision, or a cutover blocker. Name which one, per gap.

### Step 4. Resolve the cross-cutting mapping decisions

These are the decisions that apply to the whole migration and that usually get fought about mid-cutover if not decided up front.

- **Identity.** User, account, and entity IDs across systems.
- **Timestamps.** Timezones, UTC conversion, sub-second precision.
- **Enums.** How values are translated when the target has a different closed list.
- **Nulls and missing.** What a missing field on the source becomes on the target.
- **PII and access.** What is re-authenticated, re-consented, or dropped.
- **Soft-deleted records.** Whether they move and how they are represented.

Write one paragraph per decision. Name the decision and the reason.

### Step 5. Write the cutover plan

The cutover is the specific sequence that flips source to target as the system of record.

Must include:

- **Freeze window.** What is frozen on the source and when.
- **Bulk migration.** When, how long, who runs it.
- **Delta migration.** How changes during the freeze are caught up.
- **Switchover moment.** The single minute when target becomes the source of record.
- **DNS, feature flags, or routing changes.** With owners and order.
- **Verification steps.** The checks that must pass before traffic flips.
- **Communications.** Who is notified before, during, and after.

The plan is written as a runbook. Numbered steps. Named owner per step. Expected duration per step. Fail-forward or abort decision per step.

### Step 6. Write the rollback plan

The rollback plan is not optional. Cover:

- **Rollback window.** How long after cutover rollback is possible.
- **Rollback trigger.** The signals that would cause rollback.
- **Rollback steps.** As a runbook.
- **Data reconciliation.** What happens to writes that landed on the target during the partial cutover.
- **Communications during rollback.** What users hear.

A migration without a rollback plan is a migration without an exit. Do not ship one.

### Step 7. Define success

Success is explicit, not vibes.

- **Functional parity.** A list of flows or reports that must match between source and target within a tolerance.
- **Data parity.** Counts, sums, and spot-checks of key records.
- **Performance.** Latency, error rate, and throughput targets on the target.
- **Business metrics.** Revenue, activation, and retention must not regress beyond a named threshold during the cutover window.

Sign-off on success is by a named person, not a committee.

### Step 8. Plan the long tail

Post-cutover is usually where migrations fail quietly. Plan:

- **Dual-read phase.** If target is written but source still reads for audit, for how long.
- **Deprecation window.** When the source is frozen read-only, then archived, then deleted.
- **Archive strategy.** Where the source data lives for compliance or reference.
- **Training and support.** What is needed for internal users and support teams.

## Templates

- `templates/en/migration-plan.md`: full migration plan.
- `templates/en/parity-matrix.md`: object-by-object parity matrix.
- `templates/es/migration-plan.md`: plan completo de migración.
- `templates/es/parity-matrix.md`: matriz de paridad objeto por objeto.

## Related skills

- `prd-authoring`: use it instead when shipping a new feature inside an existing system, not moving systems.
- `proposal-scoping`: use it when scoping a custom build with no legacy source.
- `dashboard-spec`: use it when rebuilding a dashboard from the same data, not migrating the data.
- `red-team-review`: run it on the cutover and rollback plan before execution.

## Anti-patterns

This skill must never produce:

- A plan without a rollback.
- A plan where the inventory is a summary, not a list.
- A cutover written as a paragraph instead of a runbook.
- A parity matrix that names only fields, not identity strategy and enums.
- A success definition that relies on "it feels right".
- A plan that does not say who pushes the button at switchover.
- A dual-run window without a defined end date.
- A migration that is presented as low-risk without naming what would make it high-risk.
- A plan that uses "minor discrepancies" as a category.

## Checklist before delivery

- [ ] Source and target systems are named, with owners.
- [ ] Inventory includes every object that could need to move.
- [ ] Each row has a classification and a target location.
- [ ] Parity matrix covers identity, fields, enums, and gaps.
- [ ] Cross-cutting mapping decisions are written as paragraphs with reasons.
- [ ] Cutover is a numbered runbook with owners and durations.
- [ ] Rollback plan exists and has a trigger.
- [ ] Success criteria are concrete and signed off by a named person.
- [ ] Long-tail plan covers dual-read, deprecation, archive, and support.
- [ ] No buzzwords from the voice rules appear.
