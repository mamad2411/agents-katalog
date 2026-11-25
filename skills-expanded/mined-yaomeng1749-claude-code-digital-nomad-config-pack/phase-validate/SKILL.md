---
name: phase-validate
description: Phase B of the solution-design workflow: validate a proposed solution with security review, architecture critique, quality gates, first-principles audit, and optional multi-model adversarial review.
origin: ECC automation-pack
---

# Phase Validate

Use this skill when the user asks for `/phase-validate`, solution validation, architecture validation, adversarial review, or pre-implementation validation of a plan.

## Purpose

Find weaknesses in a solution before implementation begins.

## Workflow

1. Load the latest proposal, PRD, or design artifact.
2. Run a security and privacy review of the proposed design.
3. Run architecture review for feasibility, scalability, maintainability, and operational risk.
4. Apply first-principles audit:
   - Is every requirement justified?
   - What can be deleted?
   - Is the simplest viable version clear?
   - Are optimizations happening before simplification?
   - Which constraints are assumptions?
5. If external review tools are available, run an independent critique through Codex, Gemini, or another configured reviewer.
6. Merge findings, revise the proposal, and revalidate up to 3 rounds.

## Output

Use this shape:

```text
VALIDATION: PASS | FAIL
Security: PASS | FAIL
Architecture: PASS | FAIL
External Review: PASS | FAIL | SKIPPED
Iterations: N/3
Key Findings:
- ...
```

End with `PHASE_VALIDATE_PASS` or `PHASE_VALIDATE_FAIL`.
