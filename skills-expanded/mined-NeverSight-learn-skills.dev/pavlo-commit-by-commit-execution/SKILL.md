---
name: pavlo-commit-by-commit-execution
version: "2.0.0"
description: >
  Systematic approach to implementing multi-step plans
  with explicit user confirmation between each step.
  Each step is a committable, testable unit of work.
  Use when executing a plan to ensure visibility,
  prevent compound failures, and allow course-correction.
  After the last step, automatically verifies the codebase
  against the ticket's Acceptance Criteria
  and writes any gaps to a verification report
  in the project root.
metadata:
  author: Pavlo Glushko
  applies_to:
    - "**/plan-*.md"
    - "**/*-plan.md"
  triggers:
    - step execution
    - execute plan
    - start next step
    - implement steps
    - step by step
    - commit execution
    - execute step
    - start next commit
    - implement commits
    - commit by commit
  capabilities:
    - implement single steps from plan
    - run tests after each step
    - run linting and formatting checks
    - report changes and results to user
    - wait for explicit confirmation
    - handle user requests to redo a step
    - provide safety mechanisms for independent steps
    - verify codebase against ticket Acceptance Criteria after the last step
    - write a gap report to a verification .md file in the project root
---

# Skill: Step-by-Step Execution

Systematic approach to executing a multi-step plan
one step at a time,
with explicit user confirmation between each step.
Each step results in a single git commit.
Ensures visibility, prevents compound failures,
and allows course-correcting before moving forward.

## When to Use

When implementing a plan that spans multiple steps
(especially complex features, refactorings,
or multi-layer changes).
Provides safety and clarity at scale.

## Core Rule

**Execute only one step at a time,
then stop and wait for user confirmation.**

Do not proceed to the next step until the user
explicitly asks
(e.g., "start next step", "start step 2",
"implement step 3", or "continue").

## Execution Flow

1. **Read and understand the step plan**
   (created via Step-Oriented Planning skill)
2. **Implement Step N**:
   - Make all code changes described in the step
   - Run tests to ensure they pass
   - Run linting/formatting checks
   - **Do NOT create the git commit yet**
3. **Report to user** with:
   - Summary of what was done
   - Test results (e.g., "560 tests passed")
   - Any relevant file changes or decisions made
   - **Proposed commit message**
     (shown in the chat, not yet committed)
4. **STOP and wait** for user confirmation
   - User should review the changes
     (e.g., via `git diff`, IDE diff viewer)
   - User runs their own tests if desired
   - User then either approves or requests changes
5. **On confirmation**, user will say something like:
   - "Commit it" → create the git commit,
     then ask whether to proceed to the next step
   - "Next step" / "Start step 2" →
     create the git commit,
     then immediately start Step 2
   - "Redo step 1 with X change" →
     adjust, re-run tests/lint,
     show updated message, wait again
6. **Repeat steps 2–5** for each remaining step
7. **After the last step is confirmed**,
   run the post-execution verification
   (see [Post-Execution Verification](#post-execution-verification)
   below)

## Post-Execution Verification

After the user confirms the last step,
automatically verify the implemented codebase
against the ticket —
no additional user prompt is needed to start this check.

### What to Verify

1. **Acceptance Criteria** —
   go through every checkbox in the ticket's
   `## Acceptance Criteria` section.
   For each criterion, inspect the actual code
   to determine whether it is met.

2. **Scope coverage** —
   confirm that every item listed under
   `## Scope → In Scope` has a corresponding implementation.

3. **Out-of-Scope boundaries** —
   confirm that nothing listed under
   `## Scope → Out of Scope` was accidentally introduced.

### How to Verify

- Read the relevant source files, tests,
  and configuration to check each criterion.
- Do not rely on memory of what was implemented —
  re-read the actual files.
- For each criterion, produce one of three verdicts:
  - ✅ **Met** —
    implementation matches the criterion exactly.
  - ⚠️ **Partial** —
    implementation exists but is incomplete
    or differs in a detail.
  - ❌ **Missing** — no implementation found.

### Output File

Create a file named `<TICKET_ID>-verification.md`
in the `docs/`
(e.g., `PROJ-42-verification.md`
for a ticket named `PROJ-42_ticket.md`).

Structure the file as follows:

```markdown
# Verification Report: <TICKET_ID>

**Date:** <today's date>
**Plan:** <path to plan file>
**Ticket:** <path to ticket file>

## Summary

<N> of <Total> Acceptance Criteria met.
<count> partial, <count> missing.

## Acceptance Criteria Status

| # | Criterion (short form) | Status | Notes |
|---|------------------------|--------|-------|
| 1 | <first few words…>     | ✅ Met  | |
| 2 | <first few words…>     | ⚠️ Partial | <what is missing> |
| 3 | <first few words…>     | ❌ Missing | <what was expected> |

## Issues Found

### <Short label for each ⚠️ or ❌ item>

<Description of the gap: what the criterion requires,
what was found in the code, and a suggested fix.>
```

If every criterion is met and no gaps are found,
write a short
"All Acceptance Criteria met — no issues found." report
and do not create an Issues Found section.

### After Writing the Report

- Inform the user that verification is complete
  and state the summary
  (e.g., "28 of 30 criteria met;
  2 issues found in `PROJ-42-verification.md`").
- Do **not** automatically fix the gaps —
  present the report and wait for the user to decide
  whether to address them in follow-up steps.

## Implementation Guidelines

### Commit Naming

Two kinds of commits can arise during execution:

- **Plan step** — implements a specific step from the plan:
  title starts with `Step X:` where `X` is the plan step
  number
  (e.g., `Step 3: Add route distance caching`).
- **Unplanned commit** —
  does not correspond to any plan step
  (e.g., a lint-only fix, a missed import,
  a typo correction discovered mid-implementation):
  plain title with no `Step X:` prefix.

After the `Step X:` prefix (or for plain titles),
follow the conventions in
`.github/git-commit-instructions.md`.

### When Implementing Each Step

- Follow the **step plan exactly**:
  only implement what's in that step's description
- Use domain/application/adapters architecture rules
  from AGENTS.md
- Follow coding style from copilot-instructions.md
- Run **all linting checks** before reporting
  (`ruff format`, `ruff check`, etc.)
- Write clear, focused commits
  (1 logical change per step)

### When Reporting to User

- Always show:
  - What files were modified/created/deleted
  - Test results (pass/fail counts)
  - Any build or linting warnings
  - Any decisions you made
    (e.g., "used `dict` instead of `Dict`
    per style guide")
- Offer a summary of the changes in 2–3 sentences
- Be explicit:
  "Ready for review.
  Please confirm to proceed to Step 2."

### When User Asks to Redo

- User might say:
  "Wait, let me add X to this step"
  or "Actually, use Y approach instead"
- **Stop**, make the requested changes,
  re-run tests/lint, and report again
- Do NOT automatically proceed to the next step —
  wait again for confirmation

## Safety Mechanisms

1. **Tests must pass after every implementation**:
   If tests fail, report and wait for user
   before doing anything else
2. **One step at a time**:
   Never batch multiple steps together
3. **Explicit confirmation**:
   Do not assume silence = approval; always ask clearly
4. **Never commit without being asked**:
   Show the proposed commit message in chat
   and wait for the user to explicitly say "commit it"
   or equivalent before running `git commit`

## Example Confirmation Prompts

**Good:**
- "Step 1 implementation is ready:
  added User entity with immutable fields.
  560 tests pass.
  Proposed commit message above.
  Please review and say 'commit it'
  to create the commit, or request changes."

**Bad:**
- "Done with step 1 and 2." (batched)
- "Next?" (unclear what was done)
- "Should I continue?" (doesn't show what was done)
- "Committed!" (committed without user asking)

## Anti-Patterns to Avoid

- ❌ Implementing multiple steps before stopping
  (batching defeats the purpose)
- ❌ Assuming silence = approval
  (always ask explicitly)
- ❌ Proceeding after test failures
  (always wait for user confirmation
  even if tests pass)
- ❌ Adding extra features not in the plan
  (stick to the plan;
  extra features are a different task)
- ❌ Skipping linting/formatting
  (always ensure the code passes all checks)
- ❌ Creating the git commit
  before the user explicitly asks
  (show the message in chat; wait for "commit it")

## Related Skills

- **Step-Oriented Planning**:
  Creates the multi-step plan this skill executes.
- **Commit Rewriter**:
  Can improve commit messages after execution;
  expects `Step X:` prefix for plan-mapped commits.
