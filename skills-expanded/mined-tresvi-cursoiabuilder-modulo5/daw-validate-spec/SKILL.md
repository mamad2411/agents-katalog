---
name: daw-validate-spec
description: >
  Validates that a spec/fix-plan is complete, coherent and consistent with its PRD, against the
  catalog's spec rules. Produces a disambiguation question for every FAIL.
  Trigger: /daw-validate-spec, during DAW's PLAN phase.
---

# Skill: /daw-validate-spec

## Description
Validates that a spec/fix-plan is complete, coherent and consistent with its PRD, against the rules
in section 2 of `.daw/rules/validation-rules.instructions.md`. Produces a concrete disambiguation
question for every FAIL.

## Inputs
- The path to the spec/fix-plan (an argument, or derived from the ticket:
  `docs/daw/specs/spec-{ticket}.md` / `docs/daw/specs/fix-{ticket}.md`)
- The PRD at `docs/daw/prd/prd-{ticket}.md` (if `gates.define` is true and the tier is FEATURE)
- The `tier` from `.daw-state.json`
- `.daw/rules/validation-rules.instructions.md` (the rule catalog)

## The rules live in the catalog, not here

**`.daw/rules/validation-rules.instructions.md` §2 is the single source of truth**: F-SPEC-01 to
F-SPEC-16 (FAIL) and W-SPEC-01 to W-SPEC-03 (WARNING). Do not re-derive criteria from memory and do
not duplicate them here — read the catalog and evaluate its rules mechanically, citing each rule's
ID in the report.

Summary of what each ID covers:

| ID | Fails when | Applies to |
|---|---|---|
| F-SPEC-01 | A PRD FR maps to no block | FEATURE |
| F-SPEC-02 | A PRD AC maps to no test in the spec | FEATURE |
| F-SPEC-03 | A PRD NFR has no technical strategy | FEATURE |
| F-SPEC-04 | A block lists no files | FEATURE |
| F-SPEC-05 | A block has no verifiable completion criterion | FEATURE |
| F-SPEC-06 | A block lists no tests | FEATURE |
| F-SPEC-07 | An endpoint has an incomplete contract | any |
| F-SPEC-08 | A schema has no constraints | any |
| F-SPEC-09 | Input with no documented validation | any |
| F-SPEC-10 | No error handling documented | all tiers |
| F-SPEC-11 | Dependencies between blocks/steps not declared | all tiers |
| F-SPEC-16 | A block documents an error that appears in no test of that block | all tiers |
| F-SPEC-12 | The spec contradicts the PRD | FEATURE |
| F-SPEC-13 | Terminology diverges from the PRD | FEATURE |
| F-SPEC-14 | A fix-plan has no regression test | FIX |
| F-SPEC-15 | A fix-plan has no rollback plan | FIX |

**F-SPEC-01 has no exceptions:** an approved FR with no coverage is a FAIL, never a WARNING. If the
requirement was deliberately deferred, it has to come out of the PRD first (with the user's
approval), through a corrective loop back to DEFINE.

**Tier modifier:** if `tier == "QUICK-FIX"`, none of `F-SPEC-*` applies — that tier has no PLAN
phase and no spec.

## Execution Protocol

### For FEATURE (full spec)
1. Read the spec and the PRD in full.
2. Read `.daw/rules/validation-rules.instructions.md` §2.
3. Build the coverage matrix FR → block and AC → test, and evaluate F-SPEC-01/02/03.
4. Evaluate per-block completeness (F-SPEC-04 to F-SPEC-11, and F-SPEC-16) on every block.
   For F-SPEC-16, count: the errors the block documents under F-SPEC-10 against the tests it lists
   under F-SPEC-06. Name every error left without one — a total is not actionable.
5. Evaluate consistency with the PRD (F-SPEC-12, F-SPEC-13).
6. Check the dependency order: circular dependencies between blocks are a FAIL under F-SPEC-11.
7. **For every FAIL, produce a concrete disambiguation question.**

### For FIX (lightweight fix-plan)
1. Read the fix-plan in full.
2. Evaluate F-SPEC-10, F-SPEC-11, F-SPEC-14, F-SPEC-15 and F-SPEC-16. Also
   F-SPEC-07/08/09 if the fix touches an endpoint, a schema or input.
3. Check coherence between the stated root cause and the proposed solution: a solution that does not
   address the declared cause is a FAIL.
4. **For every FAIL, produce a concrete disambiguation question.**

## Output Format

```
┌─────────────────────────────────────────────────────────────┐
│  /daw-validate-spec [name] — [PASSED | FAILED (N questions)] │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PRD coverage: (FEATURE only)                                │
│    ✅/❌ [ID]: FR-xx → [block or "NOT COVERED"]              │
│                                                              │
│  Per-block completeness:                                     │
│    ✅/❌/⚠️ [ID]: [what was checked]                          │
│       → [what is missing and how to fix it]                  │
│                                                              │
│  Consistency with the PRD:                                   │
│    ✅/❌/⚠️ [ID]: [what was checked]                          │
│                                                              │
│  Disambiguation questions:      (only if there are FAILs)    │
│                                                              │
│    Q1: [concrete question derived from the FAIL]             │
│        Options: a) ... b) ... c) ...                         │
│                                                              │
│  ────────────────────────────────────────────────────────────│
│  Total: X passed, Y failed, Z warnings                       │
│  Result: [PASSED if Y == 0 | FAILED if Y > 0]                │
│  Next: [recommended action]                                  │
└─────────────────────────────────────────────────────────────┘
```

## Result Rules

- **PASSED:** 0 FAILs. It may have WARNINGs.
- **FAILED (N questions):** 1+ FAILs. Each FAIL produces a disambiguation question.
- Questions must be concrete, with options where possible (a/b/c).
- The user answers → the answers are folded into the spec (via `daw-create-spec` in update mode) →
  re-validate.
- A spec in the FAILED state cannot be approved.

## Updating .daw-state.json
- Does not modify flags directly (the user's approval is what sets `gates.spec`).

## Language

Write the report in the language the user is working in, citing the rule IDs verbatim.
