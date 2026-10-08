---
name: pipeline
description: Full test automation pipeline — Jira → code analysis → test design → MCP check → write code → review → coverage
version: 4.0.0
---

# pipeline — Universal Test Automation Pipeline

You are orchestrating an **11-phase test automation pipeline** for the current project.
Each phase is a distinct step. Complete each phase fully before moving to the next.

**IMPORTANT:**
- You MUST execute ALL phases (0 through 10) in order. Phases 6 and 7 are optional — the user may skip them.
- Read CLAUDE.md at the project root for project-specific conventions, architecture, and coding rules.
- If `.claude/PIPELINE_FLOW.md` exists in the project, read it for the visual flow diagram.
- All coding conventions (locator style, assertion patterns, test structure) come from the project's CLAUDE.md — do NOT hardcode any project-specific rules here.

---

## Phase 0 — Branch Setup

**Goal:** Ensure all work happens on a dedicated branch from `main`.

Launch the **branch-setup** agent (available globally).
Pass the task description as context — the agent will generate a branch name from it.

**If there are uncommitted changes** — inform the user and ask how to proceed (commit, stash, or abort).

After the branch is created, confirm the branch name to the user and proceed to Phase 1.

---

## Phase 1 — Jira Analysis

**Goal:** Understand the task. Accepts a Jira link OR a text description.

### Option A — User provides a Jira link

If `.claude/agents/jira-reader.md` exists in the project, launch the **jira-reader** agent.
Otherwise, use the Bash tool to fetch the issue via Jira REST API (credentials from `~/.claude/.env`).

Extract: summary, description, acceptance criteria, subtasks, labels.
Present the summary to the user. Confirm understanding in 2-3 sentences.

### Option B — User provides a text description

Structure the requirements:
1. **What feature/page** is being tested
2. **Key scenarios** — happy path, negative cases, edge cases
3. **Known blockers** — features that don't work yet

Confirm understanding with the user.

**Note:** Do NOT map to test coverage yet — that happens in Phase 4.

---

## Phase 2 — Code Analysis

**Goal:** Understand how the feature is implemented in the source code.

### Step 0 — Switch to the task branch and pull latest

Ask the user for the **branch name** of the task (if not obvious from Jira).

Check CLAUDE.md for source repository paths. If the project defines backend/frontend repositories, switch to the task branch in each:

```bash
git -C <repo-path> fetch && git -C <repo-path> checkout <branch> && git -C <repo-path> pull
```

Run repos in parallel. If a branch doesn't exist in one repo, use `main`. If a repo is unavailable, skip and note it.

**IMPORTANT:** After the pipeline completes, switch source repos back to `main`.

### Step 1 — Launch code analysis

If `.claude/agents/codebase-analyzer.md` exists, launch the **codebase-analyzer** agent.
Otherwise, use the Explore agent to analyze the source code directly.

Pass:
- Feature name and description from Phase 1
- Keywords: relevant endpoints, entities, components
- Scope: what repos to analyze

Present the combined report to the user.

---

## Phase 3 — Test Design (interactive)

**Goal:** Design test coverage based on requirements AND code analysis.

This phase has 3 steps:

### Step 1 — Clarifying Questions

Based on Phases 1 and 2, ask **3-5 targeted questions** to uncover gaps. Tailor questions to the specific feature — do not ask generic questions.

Question categories (pick the most relevant):
1. **Requirement vs code gaps** — Jira says X, but code implements Y differently. Which is correct?
2. **Access control** — Who should/shouldn't have access? What roles are involved?
3. **Error states** — What happens on API error? Is there a retry or error message?
4. **Boundaries** — Max length, file size, count limits? What happens at the boundary?
5. **Edge cases** — Empty states, concurrent operations, special characters?
6. **Destructive actions** — Confirmation dialogs? Undo support?
7. **Integration points** — Side effects (emails, notifications, events)?

Format each question with context and code references.

**Wait for user answers.** If the user says "skip" — proceed with assumptions from the code.

### Step 2 — Test Cases

If `.claude/agents/test-case-designer.md` exists, launch the **test-case-designer** agent.
Otherwise, design test cases directly based on Phases 1-2 and the user's answers.

Test cases should include:
- Steps and assertions using **actual values** from the code
- Categories: happy path, negative, edge cases, access control, UI state
- Priority (P1/P2/P3)

### Step 3 — ASCII Diagrams (if needed)

If the feature has a complex flow (state machine, multi-step wizard, branching logic), create ASCII diagrams. Skip for simple features.

Present all test cases (and diagrams if any) to the user.

---

## Phase 4 — Autotests Mapping

**Goal:** Analyze existing test infrastructure and map to coverage documentation.

If `.claude/agents/test-analyzer.md` exists, launch the **test-analyzer** agent.
Otherwise, use the Explore agent to analyze the test project directly.

Analyze:
- Existing page objects, flows, helpers, utilities
- Existing tests for this feature
- Coverage documentation (TEST_COVERAGE.md or equivalent) — what's automated, what's TODO

Also launch a general-purpose Agent in parallel to find reusable test patterns:
```
"Analyze existing tests related to [FEATURE].
1. Read 2-3 existing spec files that cover similar functionality
2. Identify reusable patterns
3. Show concrete code examples
Return: reusable patterns with code snippets."
```

---

## Phase 5 — Approval

**Goal:** Get user confirmation before any coding or MCP checks.

Present a consolidated summary:

```
## Plan Summary

### Scope
- What will be automated
- What is out of scope (and why)

### Test cases
1. [TC-ID] Title — type (positive/negative/edge) — priority
2. ...

### Infrastructure
- Reuse: [existing helpers]
- Create: [new page objects, locators, methods]
- Spec file: [path]

### MCP checks (Phase 6-7)
- Smoke: [list of basic checks]
- Edge cases: [list]

### Risks & blockers
- [list]
```

**Wait for explicit user approval before proceeding.**

---

## Phase 6 — MCP Smoke Check (optional)

**Goal:** Verify basic functionality works before writing tests.

### Step 1 — Propose checks
Based on happy-path test cases, propose a list of basic UI checks. Ask the user which to run or skip entirely.

### Step 2 — Execute checks
Use MCP Playwright tools (or similar) to navigate, interact, and verify.

### Step 3 — Report
If a check fails — report, ask about creating a Jira issue, decide whether to proceed.

---

## Phase 7 — MCP Edge Cases Check (optional)

**Goal:** Verify edge cases and negative scenarios before writing tests.

Same flow as Phase 6, but for edge case / negative test cases.

---

## Phase 8 — Code Writing

**Goal:** Write the test code following **all project conventions from CLAUDE.md**.

Read the project's CLAUDE.md for:
- Test structure conventions (test.step, describe, etc.)
- Assertion patterns (visibility checks before interactions, etc.)
- Page Object Model rules (locator placement, method patterns)
- User creation strategy (API vs UI)
- Navigation rules (waitUntil, waitForResponse patterns)
- TC annotation format

Steps:
1. Create/update Page Objects if new locators are needed
2. Create/update Flows if new orchestration is needed
3. Write the spec file with all test cases
4. **Run each test** — this is MANDATORY. Use the test-runner agent if available, otherwise run via `npx playwright test` or the project's test command from CLAUDE.md.
5. If a test fails — read the error, fix, re-run. Do not give up.

---

## Phase 9 — Code Review

**Goal:** Review the written code for quality and correctness.

Launch the **code-reviewer** agent (available globally).
Pass the list of all written/modified files as context.

If issues are found — fix them and re-run the affected tests.

---

## Phase 10 — Coverage Update

**Goal:** Update coverage documentation to reflect the new automation.

If `.claude/agents/coverage-mapper.md` exists, launch the **coverage-mapper** agent.
Otherwise, update the coverage file (TEST_COVERAGE.md or equivalent) directly.

Pass as context:
- List of implemented TC-IDs with their spec file paths
- Any blocked cases with Jira ticket references

Show the diff to the user.

---

## Summary format

After all phases complete, present a final summary:

```
## Pipeline Complete

### Tests written:
- [TC-ID]: [title] — passing / failing (reason)

### Files modified:
- [list of created/modified files]

### MCP check results:
- Smoke: X/Y passed
- Edge cases: X/Y passed
- Bugs found: [list with Jira links if created]

### Coverage change:
- [TODO] → [AUTO]: N cases
- New [BLOCKED]: N cases (with Jira links)
```
