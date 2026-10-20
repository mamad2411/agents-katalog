---
name: daw-verify-module
description: >
  Verifies that a completed module meets every acceptance criterion in its PRD and every task in its
  spec. A blocking gate.
  Trigger: /daw-verify-module, during DAW's VERIFY phase.
---

# Skill: /daw-verify-module

## Description
Verifies that a completed module meets every acceptance criterion in its PRD and every task in its
spec. A blocking gate.

## Inputs
- The PRD at `docs/daw/prd/prd-{ticket}.md` (if `gates.define` is true and the tier is FEATURE).
- The spec/fix-plan at `docs/daw/specs/spec-{ticket}.md` or `docs/daw/specs/fix-{ticket}.md` (if
  `gates.spec` is true).
- The implemented code.
- The tests, and their results.
- `.daw/rules/validation-rules.instructions.md` §5 for the rules (F-VER-01 to F-VER-06, W-VER-01 to
  W-VER-03) — the single source of truth.
- The `tier` from `.daw-state.json`.

## Execution Protocol

### For FEATURE

1. **Verify the PRD's acceptance criteria** (F-VER-01):
   For EVERY acceptance criterion:
   - Does the code implement it? (exact location: file:function)
   - Is there a test verifying it — and is that test passing?
   - Does the test verify the actual behavior, or only the status code? Status-code-only is a
     WARNING, not a PASS.

2. **Verify the spec's tasks** (F-VER-02, F-VER-06):
   For EVERY checkbox in the spec:
   - Is it marked complete?
   - Does the corresponding code exist?
   - Does every test the spec listed exist and pass? Those are approved commitments.

3. **Verify coverage** (F-VER-03):
   - Lines ≥ 80%, branches ≥ 80%, functions ≥ 80% over the new/modified code. Below any of them is a
     FAIL, not a warning.
   - Core business logic between 80–90% is a WARNING (W-VER-02): it should be higher.

4. **Verify sad paths** (F-VER-04):
   - Every endpoint or function accepting input needs at least one test with invalid input.
     Happy-path-only is a FAIL.

5. **Verify quality:**
   - Lint/type checker passes with no errors (F-VER-05).
   - No dead code or unused imports (W-VER-01).
   - No fragile tests: order dependencies, global state, hardcoded timestamps/IDs (W-VER-03).

### For FIX

1. **Verify the fix-plan's solution:**
   - Were all the steps implemented (F-VER-02)?
   - Does the regression test exist, reproduce the original bug, and pass with the fix applied?

2. **Verify no regressions were introduced:**
   - The full test suite passes.
   - Lint passes (F-VER-05).

## Verification levels

| Level | Meaning |
|-------|---------|
| ✅ **PASS** | The code implements the criterion AND a test verifies the behavior |
| ⚠️ **WARN** | Code is fine but the test is superficial (status code only), or a non-critical item is missing |
| ❌ **FAIL** | Missing code, missing test, or a failing test |

## Output Format

```
┌─────────────────────────────────────────────────────────┐
│  /daw-verify-module [name] — [PASSED | BLOCKED]          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Acceptance criteria:                                    │
│    ✅/❌ [ID] AC-01: [criterion] → [file:function] →     │
│       [test]                                             │
│    ✅/❌ [ID] AC-02: ...                                 │
│                                                          │
│  Spec tasks:                                             │
│    ✅/❌ [ID] Block 1: [X/Y tasks completed]             │
│    ✅/❌ [ID] Block 2: ...                               │
│                                                          │
│  Coverage:                                               │
│    ✅/❌ [ID] Lines: XX% · Branches: XX% · Functions: XX%│
│    ✅/❌ [ID] Sad-path tests                             │
│                                                          │
│  Quality:                                                │
│    ✅/❌ [ID] Lint / type checker                        │
│    ✅/⚠️ [ID] No dead code                               │
│    ✅/⚠️ [ID] No fragile tests                           │
│                                                          │
│  ─────────────────────────────────────────────────────   │
│  Total: X passed, Y failed, Z warnings                   │
│  Result: [PASSED if Y == 0 | BLOCKED if Y > 0]           │
│  Next: [recommended action] (attempt N/3)                │
└─────────────────────────────────────────────────────────┘
```

## PASS/FAIL criteria
- **PASSED:** 0 FAILs → `gates.verify` = `true`. WARNINGs are reported and do not block.
- **BLOCKED:** 1+ FAILs → go back to the CODE phase to fix. Never patch the code in VERIFY. Max 3
  attempts, then escalate to the user.

For detailed cross-verification, spawn `daw-module-verifier` via the Agent tool — an agent that did
not write the code.

## Tier modifier: QUICK-FIX
Does not apply — that tier has no VERIFY phase.

## Updating .daw-state.json
- `gates.verify` → `true` on PASS. The report is saved to `docs/daw/reports/verify-{ticket}.md`
  (derived path), including the WARNINGs that did not block. A BLOCKED run is written too — the
  round that failed is what explains the corrective loop that follows it.

## Language

Write the report in the language the user is working in, citing the rule IDs verbatim.
