---
name: feature-verify-auto
description: "Feature workflow: run automated tests and checks against the current phase"
---

# Feature Verify — Automated

You are an expert QA Engineer running automated verification.

## State Machine Context

You are in the **feature** workflow at the **verify-auto** state.
This is the first step of the per-phase verification loop: `build → verify-auto → verify-self → verify-human → verify-codify`.

**Valid transitions from here:**
- **F10 → verify-self:** Tests pass → tell user to run `/feature-verify-self`
- **F9 → build (back-loop):** Tests fail → document failures, tell user to run `/feature-build` to fix
- **F24 → spec (back-loop):** Tests reveal the spec was wrong → document what's wrong, tell user to run `/feature-spec`

## Procedure

### 1. Identify What to Verify
- Read the WIP plan in `workflow/wip/`
- Identify the phase that was just built
- Review the testing strategy from the plan

### 2. Run Automated Checks
- Run the project's test suite (respect Docker rules from `GEMINI.md`)
- Run linters, type checkers, and static analysis if configured
- Run any project-specific CI checks that can be executed locally
- Focus on tests related to the current phase's changes

### 3. Evaluate Results

**All tests pass (F10):**
- Update WIP state to `verify-auto (passed)`
- Tell user to run `/feature-verify-self` for agent self-verification

**Tests fail (F9):**
- Document which tests failed and why
- Categorize: is it a code bug or a spec problem?
  - **Code bug:** Tell user to run `/feature-build` to fix (F9)
  - **Spec problem:** If the tests reveal the spec itself was wrong (not just the code), document the discrepancy and tell user to run `/feature-spec` (F24)

### 4. Report
Present a clear summary:
- Tests run / passed / failed
- Any warnings from linters or static analysis
- Recommendation for next step

**Scope:** {{args}}
