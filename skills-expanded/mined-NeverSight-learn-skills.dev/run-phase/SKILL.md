---
name: run-phase
description: Orchestrate a complete build-review-fix cycle for a given phase. Invokes the builder agent, then the reviewer, and loops until the review passes or the user intervenes.
disable-model-invocation: true
argument-hint: "[phase-number] [path-to-spec-or-widget]"
---

Orchestrate build-review-fix cycle for Phase $ARGUMENTS[0].

Window/header JSON widgets only (5 phases).

## Phase 1 (Spec)

1. Invoke **spec-writer** agent (uses `phase-1-spec`)
2. Invoke **reviewer** agent for Phase 1 (uses `phase-1-review`)
3. PASS -> notify user spec is ready
4. FAIL -> pass failures to spec-writer to fix, re-run reviewer
5. Loop until PASS or user intervenes

## Phase 2 (Mock — HTML)

1. Invoke **mock-builder** agent with spec at $ARGUMENTS[1] (uses `phase-2-mock`, output: `widgets/{name}/_mock/`)
2. Invoke **reviewer** for Phase 2 (uses `phase-2-review`)
3. PASS -> notify user mock is ready
4. FAIL -> pass failures to mock-builder, re-run reviewer
5. Loop until PASS or user intervenes

## Phase 3 (Primitives)

1. Read gap report: `widgets/{name}/_mock/gap-report.md`
2. No gaps -> skip to Phase 4
3. Fill gaps per `phase-3-primitives` skill (create primitives in `/home/martin/tercen/sdui/`, run `dart analyze`, regenerate theme/style as needed)
4. Confirm all gaps resolved before proceeding

## Phase 4 (Catalog)

1. Invoke **catalog-integrator** agent with mock at $ARGUMENTS[1] (uses `phase-4-catalog`, authors catalog.json entry)
2. Invoke **reviewer** for Phase 5 (uses `phase-5-review` with `checks-catalog.md`)
3. PASS -> validate catalog.json parses, notify user
4. FAIL -> pass failures to catalog-integrator, re-run reviewer
5. Loop until PASS or user intervenes

## Phase 5 (Review)

Executed as part of Phase 4 loop (step 2). No separate invocation.

## Rules

- Max 5 review-fix cycles per phase before asking user for guidance
- Same issues after 2 cycles -> stop and ask user
- Builder does work, reviewer checks. Reviewer verdict is final — no negotiation.
- All agents log to `_issues/session-log.md`
- After PASS, present report location: `_local/review-{phase}.md`
