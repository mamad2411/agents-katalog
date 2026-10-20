---
name: deprecation-migration
description: Retire an API, library, field, or pattern safely - parallel-run old and new, migrate consumers with warnings and deadlines, then remove the old path completely. Use when the user wants to deprecate an endpoint or feature, replace a library or framework, rename/remove a schema field, or asks how to migrate consumers without breaking them.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep, edit, write
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [deprecation, migration, api, legacy]
---

# Deprecation & Migration

Retiring something is a **project, not a deletion**. The pattern is always the same: build the new, run both, move consumers, measure zero usage, then — and only then — delete.

## When to use

- "We want to kill endpoint/field/feature X"
- Replacing a library, framework version, or internal pattern across a codebase
- Renaming or removing database columns or API response fields
- Consumers (internal or external) depend on the thing being removed

## Principles

- **Expand → migrate → contract.** New path first, both alive in parallel, old path removed last. Never in-place mutation of a contract.
- **You can't deprecate what you can't measure.** Usage telemetry on the old path comes before any deadline.
- **Loud, early, repeated.** Consumers ignore the first announcement. Warnings belong in the response/log they already look at.
- **The job isn't done until the old code is deleted.** A "deprecated" path that lives forever is worse than either alternative.

## Process

### 1. Inventory the blast radius

```bash
# Who uses it? (internal)
grep -rn "oldThing" --include="*.{php,ts,js,py}" .
```

- Internal callers, external API consumers, scheduled jobs, stored data, docs/examples
- Classify consumers: ones you can change, ones you can ask, ones you can't reach

### 2. Build the replacement (expand)

- New endpoint/field/function exists alongside the old — same release, zero behavior change for existing consumers
- For data: write to **both** old and new (dual-write) or backfill, so the new path is complete before anyone switches

### 3. Instrument the old path

- Count calls: who, how often, from where (per consumer/API key if external)
- This number is your progress bar and your "safe to delete" proof

### 4. Announce and warn

- Deprecation notice with: what, why, the replacement, **the date**, and a migration example
- Machine-readable where possible: `Deprecation`/`Sunset` HTTP headers, `@deprecated` annotations, runtime warnings in dev logs
- Repeat at intervals; escalate channel as the deadline approaches

### 5. Migrate consumers

- Internal: migrate them yourself, mechanically, one PR per consumer area — don't wait for teams to "get around to it"
- External: provide a side-by-side example (old call → new call); offer a compat shim only if it has its own removal date
- Watch the usage metric drop after each wave

### 6. Contract (remove)

- Usage at zero (or only known stragglers with explicit sign-off) for an agreed quiet period
- Remove the old path, its tests, its docs, its feature flags — **all of it**
- For schema: drop columns in a later release than the code stops reading them (see `database-migration`)

## Output format

```markdown
## Deprecation plan: <thing>

**Replacement:** <new thing> (status: built / in progress)
**Why:** one sentence.

### Consumers
| Consumer | Type | Usage/day | Migration | Status |
|----------|------|-----------|-----------|--------|
| …        | internal/external | … | … | pending/done |

### Timeline
- T0: replacement live, dual-running
- T0+…: deprecation announced, warnings active
- T0+…: internal consumers migrated
- **Sunset date:** … (old path removed)

### Rollback
<how to re-enable the old path if migration reveals a gap>

### Done when
- [ ] Old-path usage = 0 for <period>
- [ ] Old code, tests, docs, flags deleted
```

## Anti-patterns

- ❌ Deleting first and discovering consumers via the incident channel
- ❌ A deprecation notice with no date — that's a suggestion, not a deprecation
- ❌ Big-bang migration ("we switch everything Saturday night") when parallel running was possible
- ❌ Compat shims with no removal date — you now maintain three things
- ❌ Declaring victory at "new thing launched" while the old path still serves traffic
- ❌ Migrating external consumers without a worked example of the new call
