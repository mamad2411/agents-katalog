---
name: bulletproof-building-and-review
description: Use when reviewing code adversarially or building production-bound features where rigour matters more than speed. Required for code reviews ending in a verdict (PASS/HOLD), when verifying that "tests pass" actually proves a feature works end-to-end, before closing findings as non-issues, before signing off your own work for peer audit, or when an author has already self-reviewed and you need to confirm or push back.
---

# Bulletproof Building and Review

## Overview

When building: prove the feature reaches production-shaped data, not just constructed test inputs.

When reviewing: prove that "tests pass" actually catches regressions.

Both sides share one discipline: verify against what production can actually produce, not what the test fixture constructs.

## Companion Skill

Use `orchestrated-agentic-delivery` for the role workflow: orchestrator, builder, reviewer, reviewer-fix mode, and final signoff. This skill remains the evidence and verdict discipline: production-shaped data paths, test mapping, severity calls, and PASS/HOLD/REQUEST CHANGES.

## The Iron Rule

**Verify production-shaped behaviour, not math primitives.** Trace upstream data paths. Find the writer for every field the reader consumes. If the writer does not exist, the feature is structurally inert. That is HIGH severity even if all tests pass.

Example: a scoring path read `evidence.signal_id` for empirical correlation weighting. The math was correct and all tests passed. But no ingestion path ever wrote `signal_id`, so the feature was permanently inert in production. The correct verdict was HOLD with HIGH severity: fix the ingestion contract.

## When to Use

- Adversarial code review where you will write a verdict.
- Building a slice you will self-sign-off for peer audit.
- Reviewing scoring, security, ingestion, permissions, money movement, AI validation, or other production-bound logic.
- Before closing a finding as "not an issue".
- When the author claims pytest green, "tests exist elsewhere", or "I evaluated X and chose Y".

Do not use this for throwaway prototypes or work explicitly scoped as exploratory.

## The 12 Rules

### Semantic verification

**Rule 1: Trace data flow upstream before signing off.** For every field a function reads, locate the writer. No writer means structurally inert feature, which is HIGH severity.

### Verdict structure

**Rule 2: No "Blind Spots" section.** Every uncertainty is either a Finding with severity and evidence, or Closed with evidence. No third bucket.

**Rule 3: "Not blocking" is not a severity.** HIGH, MEDIUM, LOW, or drop it.

**Rule 4: Regression analysis is mandatory before severity.** For every Finding, answer: if this regresses, which test catches it? If no test catches it, severity is at least MEDIUM.

**Rule 5: "Tests exist elsewhere" requires reading those tests by name.** Open the file. List test names. Cite line numbers. Then close.

**Rule 6: "X evaluated and chose Y" is not closure.** Author reasoning is input, not verdict. Verify independently.

**Rule 7: Round-trip before publishing.** Re-read the verdict. If you find a banned phrase, stop and re-verify the claim.

### Process

**Rule 8: Map every brief-required test to an actual test by name.** Use a row-by-row table.

**Rule 9: Read every helper.** Cite line numbers. Do not trust function names.

**Rule 10: Treat injected-fake LLM tests as gaps.** If the validator is the boundary, per-rule tests are required. Mocked model responses do not prove the validator works.

**Rule 11: Adversarial pass on docs too.** Treat PR descriptions, design docs, and author notes as claims to verify, not evidence.

**Rule 12: Destructive ops need full audit.** Before prune, delete, migration, or schema changes: identify writers, readers, freshness dependencies, and active usage.

## Banned phrases

| Phrase | Replacement |
|---|---|
| "Blind spot" | Finding with severity, or Closed with evidence |
| "Not blocking" / "Worth noting" | HIGH/MEDIUM/LOW with regression rationale, or drop |
| "Cosmetic, but..." / "Minor, but..." | Finding with severity, or omit |
| "Likely unintended" / "Probably fine" | Verify with author, test, code, or grep |
| "Tests exist elsewhere" | Name file:test_name with line numbers |
| "X evaluated and chose Y" | Verify Y independently |
| "Pytest green locally" | Cite end-to-end test covering production path |
| "Code smell" / "Maintenance smell" | Specific regression mode or omit |
| "Good enough for now" | Assign severity and mark as an open decision |

## Building side

Before signing off your own slice:

1. Trace each field your code reads back to its writer.
2. Run the production data path end-to-end where possible.
3. Do not reference tests by name without checking they exist.
4. Avoid vague confidence. Use evidence.

## Verdict template

```text
## Top line: PASS | HOLD | REQUEST CHANGES

## Findings
### HIGH-1: [one-line summary]
- Evidence: file.py:LN
- Regression analysis: if [specific change] happens, which test catches it?
- Fix scope: [paragraph]

## Closed, verified non-issues
- CLOSED-1: [item] verified by [test_name at file.py:LN]. Regression: [if X changes, test Y fails].

## Required tests mapped
| Brief requirement | Actual test | File:LN |
|---|---|---|

## Open decisions
- [Question requiring owner signoff, with options]

## Round-trip check
- Re-read for banned phrases: yes/no
- Brief-required tests mapped row-by-row: yes/no
- Every Finding has regression analysis: yes/no
- Every Closed item has file:line evidence: yes/no
```
