---
name: pbs-phase-validation
description: "Use after completing all tasks in a phase, to verify the implementation against the phase spec before closure"
---

# Phase Validation

## Overview

Validate a completed phase against its spec using a 2-stage review: first spec compliance, then code quality. You are the reviewer — report issues, never fix them.

**Core principle:** The spec is the source of truth. If the implementation doesn't match the spec, the implementation is wrong — not the spec.

**Announce at start:** "I'm using the pbs-phase-validation skill to validate phase [N] against its spec."

## When to Use

- All tasks in a phase are marked complete
- Human wants to verify the phase before closing it
- Re-validating after blockers have been fixed

## The Iron Law

```
YOU ARE THE REVIEWER, NOT THE IMPLEMENTER.
REPORT ISSUES — DO NOT FIX THEM.
```

If you find a bug, document it. If a test is missing, document it. Do NOT write code, do NOT fix anything, do NOT create files. Your output is a report — nothing else.

## Input

- `.pbs-framework/phases/phase-XX/spec.md` — the source of truth for this phase
- `.pbs-framework/phases/phase-XX/tasks.md` — task definitions and validation commands
- Completed implementation (code, tests, artifacts produced during the phase)

## The Process

### Stage 1: Spec Compliance

This stage answers: **Does the implementation match what was planned?**

1. Read the phase spec: `.pbs-framework/phases/phase-XX/spec.md`
2. Read the tasks: `.pbs-framework/phases/phase-XX/tasks.md` (for reference)
3. For EACH acceptance criterion in the spec:
   - Is it implemented? (Yes / No / Partial)
   - Is there a test that covers it? (Yes / No)
   - Evidence: test name, command output, or file reference
4. For EACH contract defined in the spec:
   - Does the interface match? (Yes / No)
   - Does the error handling match? (Yes / No)
5. Check scope: were files modified outside the phase's boundaries?
6. Run ALL validation commands from the tasks
   - **REQUIRED:** Use superpowers:verification-before-completion
   - Run each command. Read the actual output. Report the real result.
   - Do NOT assume, guess, or say "should pass"

```
Stage 1 result:
  ALL criteria implemented + ALL criteria tested + ALL commands pass
    → STAGE 1 PASS → proceed to Stage 2
  ANY criterion missing or failing
    → STAGE 1 FAIL → skip Stage 2, report issues
```

### Stage 2: Code Quality

This stage answers: **Is the code well-written?** Only run if Stage 1 passes.

1. **Convention compliance:**
   - Does the code follow AGENTS.md patterns?
   - Naming, error handling, import style consistent with codebase?

2. **Design quality:**
   - SOLID principles respected?
   - Appropriate error handling (not over-engineered, not missing)?
   - Type safety maintained?

3. **Test quality:**
   - Do tests validate behavior or implementation details?
   - Are edge cases covered?
   - Are tests readable and maintainable?

4. **Domain-specific checks** (apply only when relevant):

   | Domain | Checks |
   |--------|--------|
   | Blockchain | Reentrancy protection, overflow/underflow guards, fund safety, access control |
   | Finance | Decimal precision, rounding strategy, idempotency, audit trail |
   | General | Input validation at system boundaries, OWASP top 10 awareness |

## Issue Severity Classification

Every issue MUST be classified. Use these definitions precisely:

| Severity | Definition | Action |
|----------|------------|--------|
| **blocker** | Breaks an acceptance criterion or a contract from the spec. | MUST be fixed before phase closure. |
| **tech_debt** | Works today but will cause problems later. Not a spec violation. | Register in Tech Debt Register. Human decides priority. |
| **skippable** | Cosmetic, style preference, minor improvement. | Can be ignored entirely. |

```
IMPORTANT: Be precise with severity.
Use "blocker" ONLY for things that break the spec's acceptance criteria or contracts.
Cosmetic issues and minor improvements are NOT blockers.
Over-classifying severity wastes time and erodes trust.
```

## Report Template

Generate `.pbs-framework/phases/phase-XX/validation-report.md`:

```markdown
## Validation Report — Phase [N]

### Overall Status: PASS / FAIL

### Stage 1: Spec Compliance

#### Acceptance Criteria Coverage
| # | Criterion | Implemented | Tested | Evidence | Status |
|---|-----------|-------------|--------|----------|--------|
| 1 | [criterion text] | Yes/No/Partial | Yes/No | [test name or evidence] | pass/fail |

#### Contract Compliance
| Contract | Interface Match | Error Handling | Status |
|----------|----------------|----------------|--------|
| [Module A → Module B] | Yes/No | Yes/No | pass/fail |

#### Validation Command Results
| Command | Result | Output |
|---------|--------|--------|
| [exact command] | pass/fail | [actual output — not summarized] |

#### Files Modified Outside Scope
[List any files touched that shouldn't have been, or "None"]

### Stage 2: Code Quality
(Only if Stage 1 passed)

#### Findings
| # | Severity | Category | File:Line | Description | Suggestion |
|---|----------|----------|-----------|-------------|------------|
| 1 | blocker/tech_debt/skippable | convention/design/tests/security | file:line | [description] | [suggestion] |

### Issues Summary
| Severity | Count |
|----------|-------|
| blocker | [N] |
| tech_debt | [N] |
| skippable | [N] |

### Summary
[2-3 sentences: what works, what doesn't, what needs attention before closure]
```

<HARD-GATE>
Do NOT fix any issue found. Do NOT write code. Do NOT create files other than the validation report.
Present the report to the human. The human decides:
- Which blockers to fix (via pbs-fixing-issues skill)
- Which tech_debt to register
- Which skippable issues to ignore
- Whether to re-validate after fixes
</HARD-GATE>

## Common Mistakes

- **Declaring PASS based on test names, not test content** — a test called "testPayment" might test the wrong thing. Read the test body.
- **Summarizing command output instead of showing it** — real output is evidence. Summaries hide failures.
- **Over-classifying severity** — marking cosmetic issues as "blocker" erodes trust. Use severity definitions precisely.
- **Fixing issues instead of reporting them** — you are the reviewer. Writing code is a role violation.

## Red Flags

Signs the agent is about to violate the process — STOP immediately:

- Declaring PASS without running ALL validation commands → Run them. Read output.
- "It probably passes" without evidence → "Probably" is not evidence.
- Fixing an issue instead of reporting it → You are the reviewer, not the implementer.
- Skipping Stage 1 to go directly to code quality → Stage 1 first, always.
- Marking a broken criterion as "Partial" to avoid FAIL → If it doesn't meet the criterion, it fails.
- Summarizing command output instead of showing it → Show the actual output.
- "The test exists so the criterion is covered" → Does the test actually validate the criterion? Read it.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "It's a quick fix, I'll just do it" | You are the reviewer. Report it. Someone else fixes it. |
| "The test passes so the criterion is met" | A passing test might test the wrong thing. Verify what it actually checks. |
| "This is clearly a skippable issue" | If it breaks a spec criterion, it's a blocker regardless of how small. |
| "Stage 2 will catch it" | Stage 2 only runs if Stage 1 passes. Don't skip. |
| "I already know the commands pass" | Evidence from a previous run is stale. Run them fresh. |
| "The output is too long to include" | Include the relevant parts. Summarizing hides failures. |
| "This criterion is tested by another criterion's test" | Each criterion needs its own evidence. Shared tests are fine if explicitly mapped. |

## Integration

**Called after:**
- All pbs-task-execution tasks are complete for the phase

**Required skills:**
- **REQUIRED:** superpowers:verification-before-completion — evidence before claims, always

**Transitions:**
- If blockers found → pbs-fixing-issues (for each blocker, then re-validate)
- If PASS → pbs-phase-closure

**Language:** Write all `.pbs-framework/` documents in the language defined in AGENTS.md `framework_language` field.
