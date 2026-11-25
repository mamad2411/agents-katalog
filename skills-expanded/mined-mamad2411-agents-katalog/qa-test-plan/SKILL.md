---
name: qa-test-plan
description: "Generate a test plan defining what needs to be tested and at what level. Use when the user wants to create or update a test plan for a milestone or task, or when QA needs to define test requirements before SWE implementation begins."
---

Generate a test plan that defines what needs to be tested and at what level.

The user may specify a milestone or task: $ARGUMENTS

## Step 1: Load Context

Read these files:
1. `docs/project-brief.md` — understand the project goals and constraints
2. `docs/roadmap.md` — understand the milestone structure
3. `.sdlc/env-context.md` (when present) — understand environment constraints, test infrastructure, and hardware requirements
4. `.sdlc/architecture.md` (when present) — understand system-level constraints and component boundaries relevant to testing
5. Most recent handoff note in `.sdlc/handoff-notes/qa/` (if any exist) — understand what QA has already covered
6. The relevant issue files:
   - If a milestone was specified: scan all `.sdlc/issues/` subdirectories for files matching that milestone
   - If a task was specified: find and read the issue file from `.sdlc/issues/`
   - If nothing specified: ask the user what to scope the test plan to

For each issue in scope, read the acceptance criteria carefully — these are the behaviors that must be tested.

## Step 2: Determine Test Scope

Identify:
- What milestone or tasks this test plan covers
- All acceptance criteria across the in-scope issues
- Any non-functional requirements from the project brief (performance, security, compliance)
- Any environment-specific testing needs from `.sdlc/env-context.md`

## Step 3: Build the Test Matrix

For each acceptance criterion or behavior, determine:
- **What to test** — the specific behavior or requirement
- **How to verify it** — the test approach (automated assertion, manual check, visual inspection, etc.)
- **Test level** — unit, integration, system, or manual
- **Infrastructure needed** — does this need hardware, an emulator, a specific environment, or just a local dev machine?

## Step 4: Produce the Test Plan

Save to `.sdlc/test-plan.md`:

```markdown
# Test Plan

**Scope:** [Milestone name or task numbers]

## Test Scope

[1-2 sentences describing what this plan covers.]

### In Scope
- [Feature / behavior area]
- [Feature / behavior area]

### Out of Scope
- [What is NOT being tested and why]

## Test Matrix

| # | Behavior | Source | Test Level | Approach | Infrastructure | Priority |
|---|----------|--------|-----------|----------|---------------|----------|
| 1 | [What to test] | [issue filename], AC 1 | Unit | [How to verify] | Local | P1 |
| 2 | [What to test] | [issue filename], AC 2 | Integration | [How to verify] | Local | P1 |
| 3 | [What to test] | [issue filename], AC 3 | System | [How to verify] | [Emulator/HW] | P2 |

### Priority Key
- **P1** — Must test. Core functionality, high risk, or blocking.
- **P2** — Should test. Important but not blocking.
- **P3** — Nice to test. Low risk, edge cases.

## Test Infrastructure Requirements

[Only include this section if `.sdlc/env-context.md` exists and testing needs go beyond a local dev machine.]

- [What's needed — emulator, hardware-in-the-loop rig, specific OS version, etc.]
- [What's needed]

## Acceptance Test Procedures

[For system-level or manual tests, provide step-by-step procedures.]

### ATP-1: [Test name]
**Tests:** Matrix row #N
**Prerequisites:** [What must be set up first]
1. [Step]
2. [Step]
3. [Step]
**Expected result:** [What should happen]

## Test Coverage Gaps

[List anything that SHOULD be tested but CAN'T be with current infrastructure or knowledge.]

- [Gap — and what would be needed to close it]
```

## Step 5: Review with User

Present the test plan to the user for review. Key questions:
- Are the priorities right?
- Are there behaviors we missed?
- Is the infrastructure available for the tests that need it?
- Any tests that should be added or removed?

Don't save until the user approves.

## Step 6: Update Documents

After user approval:
- Save `.sdlc/test-plan.md`
- Update `docs/roadmap.md` change log noting that a test plan was created for this scope

The test plan asks what the project needs based on the context PM captured. It doesn't assume any particular test infrastructure exists — it states what's needed and lets DevOps figure out how to provide it.
