---
allowed-tools: Skill, Agent, Read, Glob, Grep, Write, Bash
description: Review the quality of a build against its plan, score it, and list gaps
argument-hint: [path to plan file]
model: opus
---

# Purpose

Review the quality of a codebase build against a plan file specified in `PLAN_PATH`. Use the `/research-codebase` skill to investigate how well the plan was implemented, then produce a scored assessment with successes, failures, and gaps per the `Report` section.

## Variables

PLAN_PATH: $ARGUMENTS

## Instructions

- Read the plan file FULLY before doing anything else.
- Extract every deliverable, requirement, and acceptance criterion from the plan.
- Use `/research-codebase` with a focused instruction: investigate how each plan item was implemented (or not) in the codebase.
- Score using letter grades: A++ (exceeds all requirements), A (fully meets), A- (meets with minor issues), B+ (mostly meets), B (partially meets), B- (significant gaps), C+ (minimal implementation), C (barely started), C- (not implemented).
- Be honest and specific — cite file paths and line numbers for both successes and failures.
- ultrathink about the overall coherence of the build before scoring.

## Workflow

1. **Read the plan** — read `PLAN_PATH` fully. Parse out all deliverables, requirements, specs, and acceptance criteria.
2. **Research the build** — invoke `/research-codebase` with a prompt that asks it to verify each plan item against the codebase, checking for implementation completeness, correctness, and test coverage.
3. **Score and assess** — based on research findings, assign an overall grade and per-section grades. Identify where the build succeeds and where it falls short.
4. **List gaps** — enumerate every unmet or partially-met requirement as a gap with enough detail to act on.
5. **Save the report** — derive a slug from the plan filename (e.g. `plan-foo-bar.md` → `review-foo-bar.md`). Write the full report to `temp/specs/reviews/<slug>`. Create the directory if needed.
6. **Present the report** — output the report to the user as well.

## Report

Present the review in this format:

```
## Build Review: [Plan Title]

**Overall Score: [GRADE]**

### Successes
- [What was built well, with file:line references]

### Failures
- [What was built incorrectly or poorly, with file:line references]

### Gaps
- [ ] [Unmet requirement 1 — what's missing and where it should live]
- [ ] [Unmet requirement 2 — ...]
- [ ] ...

### Per-Section Scores
| Section | Score | Notes |
|---------|-------|-------|
| [Plan section 1] | [GRADE] | [One-line assessment] |
| [Plan section 2] | [GRADE] | [One-line assessment] |
| ... | ... | ... |
```