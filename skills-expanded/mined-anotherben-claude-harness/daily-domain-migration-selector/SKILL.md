---
name: daily-domain-migration-selector
description: Use when choosing daily Helpdesk service-to-domain migration candidates, table ownership moves, write seam consolidation, domain README gaps, or A-plus architecture burn-down work before implementation.
---

# Daily Domain Migration Selector

## Overview

Use this skill to pick 2-5 Helpdesk services that should move toward `apps/api/src/domains/**`. The output is a ranked, evidence-backed candidate list and lane cards; it is not an implementation pass.

Core rule: select from current source, ownership, and ratchet evidence. Do not select by instinct or filename alone.

## Required Sub-Skills

- **REQUIRED PRECHECK:** Use `deep-think` before ranking candidates.
- **REQUIRED MAP:** Use `zoom-out` on any unfamiliar candidate surface.
- **REQUIRED TRACE:** Use `blast-radius` in inline plan mode for each selected lane before coding; do not write repo artifacts from selector dry runs.
- **REQUIRED CONTROL WHEN DELEGATING:** Use `nested-agent-control`; one subagent gets one job.

## Read-Only Boundary

This selector is read-only. It may inspect route cards, source, ownership registries, vault state, and scripts. It must not edit files, create branches, fetch into a guarded root, push, open PRs, or run live write canaries.

For freshness in read-only mode, compare current `HEAD` with the remote `dev` SHA from `ls-remote`; do not update local refs in a guarded root. If current docs disagree about whether program work targets `dev` or an integration branch, surface that as a planning conflict in every lane card.

## Hard Stops

Stop and report instead of selecting or editing when:

- The checkout is not a Helpdesk repo.
- The target branch/base cannot be proven from current source and remote state.
- The route card says `allowed_to_edit_here=false` for any mutating action.
- The task asks to implement directly from the selector. Hand off to `$daily-domain-refactor-runner` or the enterprise workflow instead.
- Ownership evidence is missing: `apps/api/ownership/db-write-owners.json` or `scripts/db-write-enforcement.cjs` cannot be read.
- A selected candidate lacks a deterministic disposition: `select`, `reject`, or `discovery-only`.

## Daily Workflow

1. State `WORKFLOW BUDGET: high | reviewer-subagent if useful | narrow tools`.
2. Record branch, current head SHA, remote dev SHA, route-card status, vault-index claim state, and cortex/source-tool availability.
3. Read the route card when present. Missing route card is acceptable for read-only selection, but blocks implementation.
4. Run the candidate script: `node /Users/ben/.codex/skills/daily-domain-migration-selector/scripts/select-domain-migration-candidates.cjs --repo "$PWD" --count 5`.
5. Search current contracts, plans, preflight artifacts, and docs for each top candidate before selecting it. A contract that says not to move a write owner overrides the script score.
6. Read source for the top candidates: `docs/architecture/domain/INDEX.md`, relevant flow docs, candidate services, callers/importers, colocated `GOTCHAS.md`, target domain README, target ratchets, ownership registry entries, and focused tests.
7. Produce exactly 2-5 lane cards plus an explicit rejection/discovery-only section for script top candidates not selected.

## Candidate Disposition

Every script top candidate must be classified:

- `select`: bounded enough for a daily migration lane, with a clear domain target, owner tables, tests, and enterprise path.
- `discovery-only`: valuable but needs source mapping, domain target decision, contract/preflight artifact, or live schema proof before migration.
- `reject`: too broad, blocked by contract, wrong target for domain migration, or requires external writes or unsafe integration scope.

Risk flags require disposition:

- `integration-or-async`: default `discovery-only` unless the lane isolates pure table ownership without queue/worker semantics.
- `data-integrity`: default `enterprise-required`; select only with exact tests, live DB proof plan, and stop gates.
- `security-or-tenant`: reject daily migration unless Ben explicitly frames it as an xhigh enterprise lane.

## Candidate Ranking

Prefer candidates with:

- service-owned active tables that should become domain-owned
- many mutation sites in `apps/api/src/services/**`
- current `services/*Gatekeeper*` write seams with clear domain targets
- documented temporary exceptions or sunset dates
- existing domain folders where the move is incremental, not a new architecture invention
- target domain README and ratchet coverage that can be updated without inventing a parallel pattern
- thin, testable seams that can move without broad behavior changes

Deprioritize:

- low-write utilities without table ownership impact
- one-off repair scripts
- surfaces with unknown ownership, missing tests, missing README/ratchet contract, or unclear runtime proof unless the lane is explicitly discovery-only
- anything requiring Shopify/REX writes unless Ben approved the exact object and scope

## Required Table Checks

For every selected table, record:

- lifecycle is active
- current owner path and owner type
- target owner path
- required live test exists
- live verification status is present
- table is not retired, exception-only, or blocked by a contract

## Lane Card Format

```markdown
### <rank>. <slug>

- Disposition: `<select|discovery-only|reject>`
- Candidate: `<service path>`
- Likely domain: `<apps/api/src/domains/<domain>>`
- Tables: `<table list>`
- Registry checks: `<per-table lifecycle/owner/live-test summary>`
- Why now: `<ownership/write-site/readme/ratchet evidence>`
- Proposed seam: `<domain writeBoundary/readModel/service route>`
- Scope: `<files likely touched>`
- Forbidden scope: `<routes, unrelated services, schema, external writes, etc.>`
- Required source reads: `<docs and files>`
- Caller/importer scan: `<bounded rg/cortex result summary>`
- Required subagents:
  - source-truth-mapper: one job
  - ownership-auditor: one job
  - plan-adversary: one job
- Required gates:
  - `npm run architecture:ratchet:test`
  - `node scripts/db-write-enforcement.cjs --mode audit --fail-on-unowned --fail-on-live-ownership`
  - focused tests for touched domain
  - `npm run local:canary` before PR
  - If `architecture:ratchet:test` or the underlying current SRP/domain architecture gates are absent, stop as `ARCH_GATE_MISSING`; do not skip, raise a baseline, or claim architecture proof.
- Stop conditions: `<what makes this lane too wide or unsafe>`
- Planning conflicts: `<branch-target, route-card, dependency, schema, contract, or vault blockers>`
```

## Rejection Section

For each script top candidate not selected, write:

```markdown
### Rejected or Discovery-Only: <candidate>
- Disposition: `<reject|discovery-only>`
- Reason: `<contract/preflight/risk/scope/proof blocker>`
- What would unblock it: `<specific source proof or enterprise artifact>`
```

## Subagent Pattern

Use subagents only after local source evidence names the candidate. One job each:

- `source-truth-mapper`: map current service, owner table entries, callers/importers, tests, and docs.
- `ownership-auditor`: confirm table ownership, live-test references, exceptions, target owner path, target README, and ratchet coverage.
- `plan-adversary`: try to reject the lane for scope creep, wrong seam, missing proof, unsafe merge path, branch-target conflict, or hidden contract/preflight blocker.

Do not let a subagent both choose and approve the same lane.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Picking the largest file | Pick table ownership and write-seam leverage first. |
| Treating a service owner as domain ownership | Domain ownership means owner paths under `apps/api/src/domains/**` unless a sunset exception is explicit. |
| Selecting five high-risk lanes | Pick fewer lanes when one crosses data integrity, async, or external integration boundaries. |
| Calling selection done after the script | Read current source and produce lane cards with proof and stop gates. |
| Ignoring a contract/preflight artifact | Contract/preflight blockers override script scores. |
| Implementing from the selector | Hand off to `$daily-domain-refactor-runner` after selection. |

## Dry-Run Proof

A valid dry run produces:

- current head SHA and remote dev SHA
- route-card status
- vault-index and cortex/tooling status
- script output
- contract/preflight search summary
- 2-5 lane cards with dispositions
- rejection/discovery-only section for non-selected top candidates
- explicit hard stops, planning conflicts, and non-goals
- no file edits, commits, pushes, PRs, or live writes
