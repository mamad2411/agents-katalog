<!--
Canonical Skill Source: docs/skills/sample-brain-issue-to-session-plan/SKILL.md
Surface: docs (canonical)
Sync Status: canonical
Last Verified: 2026-08-09
Drift Policy: Cursor mirrors must match this skill body.
-->
---
name: sample-brain-issue-to-session-plan
description: >
  Turn one Sample Brain GitHub issue into a current, small, test-first session
  plan without treating an open issue as authorization to implement.
---

# Sample Brain Issue-To-Session-Plan Skill

## Purpose

Use this skill to turn one GitHub issue into a small, current work plan. An open
issue is a work candidate, not automatic authorization to implement. The plan
must identify the smallest useful slice and its blockers before any product
change begins.

## Required Context And Safety

Before reading beyond the target issue, read current repository governance,
`docs/BOOTLOADER_AND_CONTEXT_STRATEGY.md`, and
`docs/DATA_AND_ARTIFACT_POLICY.md`. Then inspect the target issue, parent issue
when present, direct dependencies, materially relevant open PRs, the current
`main` state, existing implementation, and existing tests.

Read only the additional documentation needed to ground the issue. Do not widen
the search to adjacent work without an explicit dependency. Tracked
repository-local paths in the current Sample-Brain checkout are allowed for
read-only planning, including repo-relative documentation, product code, and
tests. Do not read private local files outside the repository, user-specific
absolute paths without explicit relevance and approval, private tracks, samples,
databases, caches, generated artifacts, secrets, model caches, or other
environment-specific files outside the tracked repository canon. Do not create
files, tests, code, issues, or PR changes merely because this skill produced a
plan.

## Method

1. Restate the issue outcome and acceptance criteria in current repository
   terms. Mark missing or contradictory requirements as unconfirmed.
2. Determine the applicable canonical documentation, current implementation,
   existing tests, direct dependencies, and relevant open PRs.
3. Classify the slice before choosing a handoff: `product_code`, `docs`,
   `ci_tooling`, `dependency`, `workflow`, `governance`, or `unknown`.
4. Define one small slice, likely affected paths, explicit non-goals, blockers,
   and a minimum validation set.
5. For a significant `product_code` slice, require this fixed sequence:

```text
DOCS_GATE -> TEST_GATE -> TEST_FREEZE -> IMPLEMENTATION -> CHECKS
```

6. Route by slice class: `product_code` to `sample-brain-test-first`; `docs` to
   `jMerta/docs-sync`; `ci_tooling` to `jMerta/ci-fix` and, when appropriate,
   `sample-brain-ci-debugger`; `dependency` to
   `jMerta/dependency-upgrader`; `workflow` through the existing
   `.cursor/rules/skill-routing.mdc` rule; and `governance` through the
   applicable existing repository governance path. Do not create a parallel
   routing policy. For `unknown`, return `planning_blocked` and name the exact
   information needed to classify the slice.

## Output

```yaml
issue: <number or URL>
goal: <concrete outcome>
canonical_docs: []
current_state: <implementation and test evidence>
direct_dependencies: []
relevant_open_prs: []
small_slice: <bounded work>
slice_class: product_code | docs | ci_tooling | dependency | workflow | governance | unknown
route_to: <existing specialized route or planning_blocked>
test_first_required: true | false
likely_paths: []
must_not_touch: []
blockers: []
test_first_sequence: DOCS_GATE -> TEST_GATE -> TEST_FREEZE -> IMPLEMENTATION -> CHECKS | not_required
minimum_validation: []
next_recommended_step: <route_to>
```

## Stop Conditions

- The issue, acceptance criteria, dependency, or canonical documentation is
  missing, contradictory, or too vague: return `planning_blocked` and name the
  needed evidence.
- Current `main`, a relevant PR, or existing tests change the intended slice:
  narrow or stop; do not plan against stale assumptions.
- The plan expands into unrelated issues, refactors, dependencies, models,
  private data, or generated artifacts: stop and remove that expansion.
- An issue requests runtime implementation but no test-first path can be named:
  stop before implementation.
- The slice class is `unknown`: return `planning_blocked` and name the exact
  missing classification evidence.

## Relationships

**Standalone Guarantee:** `standalone: true`

This skill runs independently with complete inputs. Other skill outputs are optional
context enhancements. An open issue is a work candidate; receiving a handoff from
another skill does not authorize implementation.

### Can Receive From

- `sample-brain-control-orchestrator` — orchestrated work priority
- `sample-brain-repository-auditor` — repository-level concerns
- `sample-brain-skill-routing-auditor` — skill/routing governance
- `sample-brain-issue-backlog-maintainer` — backlog triage results

### Route If

| Condition | Target | Required | Notes |
|-----------|--------|----------|-------|
| `product_code` | `sample-brain-test-first` | Yes | Significant product changes require test-first sequence |
| `docs` | `sample-brain-docs-sync-maintainer` | No | Documentation-only changes |
| `ci_tooling` | `sample-brain-ci-debugger` | No | CI or tooling infrastructure issues |
| `dependency` | `sample-brain-dependency-upgrader` | No | Dependency or upgrade work |
| `workflow` | `sample-brain-control-orchestrator` | No | Workflow or process changes (existing path) |
| `governance` | `sample-brain-skill-routing-auditor` | No | Governance or policy changes (existing path) |
| `unknown` | `PLANNING_BLOCKED` | Yes | Missing classification evidence required |

**Critical Note:** The condition `product_code` is the only direct path to `test-first`.
A generic "new feature or issue" classification is not sufficient; slice class must be
determined before routing to implementation.

### Next Recommended

After routing by slice class, the recommended next step is determined by the target:
- For `product_code`: `sample-brain-test-first` enforces DOCS → TESTS → FREEZE → IMPLEMENTATION → CHECKS
- For `docs`: existing documentation path
- For `ci_tooling`: existing CI path
- For others: existing specialized paths

### Optional External Routes

| External | Local Fallback | Notes |
|----------|----------------|-------|
| `jMerta/plan-work` | `sample-brain-control-orchestrator` or direct start | Declared but not verified; use local fallback |

### When to STOP

- `PLANNING_BLOCKED`: Issue, acceptance criteria, canonical documentation, or slice
  classification is missing or contradictory. Name the exact required evidence.
- Unknown slice class after reasonable review: cannot route safely.

### Cycle Rules

No forward loop back to issue planning from test-first or implementation. Planning
ends when a clear slice is routed to its designated handler.

Issue `#233` is a valid future input: this skill may identify its documented
one-shot analysis scope and direct dependencies, but it does not implement it.
