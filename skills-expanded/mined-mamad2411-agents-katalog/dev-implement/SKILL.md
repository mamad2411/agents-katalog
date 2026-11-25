---
name: dev-implement
description: Use when executing an implementation plan task-by-task - dispatches subagents for implementation, manages git worktrees, handles phased multi-service deployment
---

# dev-implement

## Overview

Execute implementation plans using test-driven development with subagent-driven development. Each task in the plan gets a fresh subagent. Every task passes through a two-stage review gate: spec compliance first, then code quality. Nothing ships without both gates green.

This is the core engine. It takes a plan and turns it into working, tested, reviewed code.

## Announcement

When this skill activates, announce:

> I'm using enggenie:dev-implement to execute this plan.

---

## Entry Condition

This skill requires one of:

1. An approved plan produced by enggenie:architect-plan
2. A Jira ticket reference (e.g., "Pick up PROJ-1234", "Implement PROJ-1234")
3. A direct user request to implement specific tasks

### Jira Ticket Entry

When the user references a Jira ticket, read the ticket first using MCP tools. The ticket contains handoff context from PM and/or Architect:

1. Read the ticket description — look for "For Dev" section with spec path and constraints
2. Read the "Implementation Plan" comment (if architect-plan added one) — get the plan file path
3. Open the linked spec and plan files. Do not work from the Jira description alone — it is a summary, not the full context.
4. If anything is unclear or missing, ask the user for clarification before starting. Do not guess.

If Jira MCP is not available, ask: "I can't read PROJ-1234 directly. Can you share the plan file path or paste the relevant details?"

**If no plan or Jira ticket is found:**

> No plan or Jira ticket found. Should I create a plan with enggenie:architect-plan first, or proceed without a plan?

Wait for the user's answer. Do not assume.

---

## Phase 0: Worktree Setup

Worktree management is built into this skill. Do not delegate it elsewhere.

### Step 1 -- Detect Worktree Directory

Check the project root for an existing worktree directory:
- `.worktrees/`
- `worktrees/`

### Step 2 -- Ensure Gitignore Coverage

If a worktree directory exists, verify it appears in `.gitignore`.

If it is NOT gitignored:
1. Append the directory name to `.gitignore`
2. Commit with message: `chore: add worktree directory to .gitignore`

### Step 3 -- Create or Confirm Directory

If neither `.worktrees/` nor `worktrees/` exists:
1. Check `CLAUDE.md` (or project config) for a stated preference
2. If no preference found, ask the user which name they want
3. Create the directory

### Step 4 -- Create Worktree with Feature Branch

```bash
git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"
```

Branch naming: use the plan name or ticket ID as the branch name. If neither exists, ask the user.

### Step 5 -- Project Setup

Auto-detect the project type and run the appropriate install command:

| Indicator         | Command            |
|-------------------|--------------------|
| `package.json`    | `npm install`      |
| `Cargo.toml`      | `cargo build`      |
| `requirements.txt`| `pip install -r requirements.txt` |
| `pyproject.toml`  | `poetry install`   |
| `go.mod`          | `go mod download`  |
| `*.csproj`        | `dotnet restore`   |

If multiple indicators are present (monorepo), run all relevant commands.

### Step 6 -- Baseline Test Verification

Run the project's test suite. Every existing test must pass before any new work begins.

**If tests fail:**
- Report the specific failures
- Ask the user: "Baseline tests are failing. Should I proceed anyway, or fix these first?"
- Do NOT silently proceed

---

## Phase 1: Per-Task Execution Loop

For each task in the plan, execute the following cycle. Do not skip steps. Do not reorder steps.

### Step A -- Dispatch Implementer Subagent

Create a subagent with:

1. **The full task text** -- inline the complete task description. Do NOT pass a reference to the plan file. The subagent must have everything it needs without reading external files.
2. **Context from prior tasks** -- what was already built, what modules/functions are available for import, what interfaces were established.
3. **Project conventions** -- naming patterns, file structure, test patterns, linting rules.

The implementer subagent follows the prompt template at `agents/implementer-agent.md`.

### Step B -- TDD Execution (RED-GREEN-REFACTOR)

The implementer follows enggenie:dev-tdd discipline:

1. **RED** -- Write a failing test that describes the expected behavior. Run the test. Confirm it fails. If it passes, the test is wrong or the feature already exists. Investigate.
2. **GREEN** -- Write the minimum code to make the test pass. No more. Run the test. Confirm it passes.
3. **REFACTOR** -- Clean up the code. Remove duplication. Improve naming. Run tests again to confirm nothing broke.
4. **COMMIT** -- Commit the passing state with a clear message.

**Hard Rule: No production code without a failing test first.**
Skipping this is not a shortcut. It is debt. Shortcut Tax applies -- if you write code before the test, you must delete the code, write the test, watch it fail, then rewrite the code.

### Step C -- Dispatch Spec Reviewer Subagent

After the implementer finishes, dispatch a spec review subagent with:

1. **Git diff** from `BASE_SHA` to `HEAD_SHA` -- the exact changes made by the implementer
2. **The spec/requirements** for this task -- the same text the implementer received
3. **Review checklist:**
   - Does the implementation match the spec?
   - Is anything specified but missing?
   - Is anything present but not specified? (scope creep)
   - Are edge cases from the spec handled?

The spec reviewer follows the prompt template at `agents/spec-reviewer-agent.md`.

### Step D -- Address Spec Issues

If the spec reviewer identifies issues:
1. Send the issues back to the implementer subagent
2. Implementer fixes them (maintaining TDD -- new test for each fix)
3. Re-dispatch the spec reviewer to verify
4. Repeat until the spec reviewer passes with no issues

### Step E -- Dispatch Code Quality Reviewer Subagent

After spec review passes, dispatch a code quality review subagent with:

1. **Git diff** from `BASE_SHA` to `HEAD_SHA`
2. **Quality checklist:**
   - Clean code: readable, well-named, no dead code
   - No bugs: null checks, error handling, boundary conditions
   - Good tests: meaningful assertions, edge cases covered, no testing implementation details
   - YAGNI: nothing built that the task did not ask for
   - No duplication with existing code

The quality reviewer follows the prompt template at `agents/quality-reviewer-agent.md`.

### Step F -- Address Quality Issues

If the quality reviewer identifies issues:
1. Send the issues back to the implementer subagent
2. Implementer fixes them
3. Re-dispatch the quality reviewer to verify
4. Repeat until the quality reviewer passes with no issues

### Step G -- Mark Complete, Advance

Mark the task as complete. Record what was built (exported functions, new files, interfaces) so the next task's implementer has accurate context. Move to the next task.

---

## Phase Boundaries (Multi-Phase Plans)

When the plan has multiple phases, enforce a hard stop between them.

After completing all tasks in a phase:

1. **Run the deployment readiness checklist:**
   - All tests pass (full suite, not just new tests)
   - No lint errors
   - No type errors
   - No unresolved TODOs from this phase
   - All review gates passed

2. **Ask the user to verify manually:**

   > Phase [N] is complete. All automated checks pass. Please verify manually before I proceed to Phase [N+1].

3. **Wait for explicit confirmation.** Do not proceed to the next phase without it.

---

## Model Selection for Subagents

Choose the model based on task complexity. Do not over-provision simple work or under-provision complex work.

| Subagent            | Condition                                      | Model   |
|---------------------|------------------------------------------------|---------|
| Implementer         | Simple task (1-2 files, clear spec)            | haiku   |
| Implementer         | Complex task (multi-file, integration, ambiguity) | sonnet  |
| Spec reviewer       | Always                                         | sonnet  |
| Code quality reviewer | Always                                       | sonnet  |
| Final reviewer      | After all tasks complete (full codebase review)| opus    |

**Gut Check:** If you are unsure whether a task is simple or complex, it is complex. Use sonnet.

---

## Handling Subagent Status

Every subagent returns a status. Handle each one correctly.

### DONE

The subagent completed its work successfully. Proceed to the next step in the cycle (e.g., from implementer to spec review).

### DONE_WITH_CONCERNS

The subagent completed but flagged concerns. Read them carefully.

- **Correctness or scope concerns** (e.g., "this might not handle X", "the spec is ambiguous about Y") -- address these BEFORE proceeding to review. Send back to the implementer or escalate to the user.
- **Observations** (e.g., "this could be optimized later", "related module might benefit from similar changes") -- note them in the task log and proceed. Do not act on them now.

### NEEDS_CONTEXT

The subagent could not proceed because it lacked information. Identify what is missing, provide it, and re-dispatch.

Common causes:
- Missing type definitions or interfaces from prior tasks
- Unclear spec language
- Missing project configuration details

### BLOCKED

The subagent hit something it cannot resolve. Assess the root cause:

- **Context problem** -- provide the missing context, re-dispatch
- **Task too large** -- break the task into smaller subtasks, dispatch each separately
- **Plan is wrong** -- escalate to the user. Do not guess.

**Hard Rule: NEVER retry the same model with the same context.** If a subagent failed with a given prompt, sending the identical prompt again will produce the identical failure. Change the context, change the model, or change the task decomposition.

---

## Parallel Agent Dispatch

When multiple tasks in the same phase are independent (no shared state, no import dependencies), dispatch them in parallel.

### Rules

1. **One agent per independent task.** Each agent gets its own focused prompt with full context and constraints.
2. **Maximum 3 concurrent agents.** More than 3 creates coordination overhead that exceeds the time savings.
3. **Independence must be real.** If task B might import something from task A, they are not independent. When in doubt, run sequentially.
4. **Merge carefully.** After parallel tasks complete, run the full test suite before proceeding. Parallel work can create integration conflicts that individual task tests will not catch.

### Decision Criteria

Before dispatching in parallel, evaluate:

```
Multiple tasks in the same phase?
  -> Are they independent? (no shared state, no import dependencies)
    -> NO: Run sequentially. Parallel investigation of coupled tasks produces conflicts.
    -> YES: Can they realistically run in parallel?
      -> YES: Parallel dispatch (max 3)
      -> NO (e.g., same file, same test suite): Sequential.
```

### Agent Prompt Quality

Every parallel agent prompt must be:

1. **Focused** -- One clear task, one domain. Not "fix everything."
2. **Self-contained** -- All context the agent needs is inline. No "read the plan file."
3. **Specific about output** -- What should the agent return? (files changed, tests added, commit hash, issues found)

### Common Dispatch Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| "Implement the feature" | Too broad -- agent gets lost | "Add the HeistCard component with CSS module and barrel export" |
| No error context | Agent does not know where to look | Paste the error messages and test names inline |
| No constraints | Agent might refactor everything | "Do NOT change existing tests. Add new files only." |
| Vague output expectation | You do not know what changed | "Return: root cause, files modified, tests added, commit hash" |

### Dispatch Pattern

```
Tasks in phase: [T1, T2, T3, T4, T5]
Independence analysis:
  T1, T2, T3 -- independent (different modules, no shared interfaces)
  T4 depends on T1
  T5 depends on T2

Execution:
  Batch 1: dispatch T1, T2, T3 in parallel (3 agents)
  Wait for all three to complete + pass review gates
  Run full test suite
  Batch 2: dispatch T4, T5 in parallel (2 agents)
  Wait for both to complete + pass review gates
  Run full test suite
```

---

## Subagent Prompt Templates

Each subagent type has a dedicated prompt template. These templates live in the `agents/` directory relative to this skill:

- `agents/implementer-agent.md` -- Full TDD implementation instructions, commit conventions, what to do when stuck
- `agents/spec-reviewer-agent.md` -- Spec compliance checklist, how to flag issues vs. observations, output format
- `agents/quality-reviewer-agent.md` -- Code quality checklist, common anti-patterns to watch for, output format

When dispatching a subagent, load the appropriate template and inject the task-specific context (task text, git diff, prior task context) into the designated sections.

---

## Subagent Context Preservation

After each subagent completes (Implementer, Spec Reviewer, Code Quality Reviewer), explicitly capture their key outputs back to the main conversation:

- **Implementer:** Files created/modified, test names and results, commit hash
- **Spec Reviewer:** Compliance status, any issues found, whether re-work is needed
- **Code Quality Reviewer:** Quality assessment, issues found, whether re-work is needed
- **Cross-task context:** What was built in this task that the next task depends on (imports, interfaces, shared types)

This context feeds into subsequent tasks. If you lose it, the next subagent starts blind.

---

## Recommended Model

**Orchestrator:** sonnet
**Why:** The orchestrator manages plan execution, dispatches subagents, and tracks progress. Sonnet balances speed and capability for this coordination role.

**Subagent model selection** (already documented in the skill):
- Implementer on simple tasks (1-2 files) -> haiku
- Implementer on complex tasks (multi-file, integration) -> sonnet
- Spec reviewer -> sonnet
- Code quality reviewer -> sonnet
- Final reviewer (after all tasks) -> opus

This is a recommendation. Ask the user: "Confirm model selection or override?" Do not proceed until the user responds.

---

## Hard Rules

These are non-negotiable. Violating any of them is a defect in the process, not a judgment call.

1. **No production code without a failing test first.** The Shortcut Tax for skipping this: delete the code, write the test, watch it fail, rewrite the code. Every time.

2. **Never retry the same model with the same context.** If it failed, something must change before you try again.

3. **Never proceed past a phase boundary without user confirmation.** Automated checks are necessary but not sufficient. The user verifies.

4. **Every task gets both review gates.** Spec compliance AND code quality. Skipping one because "it is a simple change" is how bugs ship.

5. **Inline the full task text to subagents.** Never pass a file reference and expect the subagent to read it. The subagent prompt must be self-contained.

6. **Maximum 3 concurrent agents.** This is a limit, not a target. Use fewer when tasks are large.

---

## Gut Checks

Before each major decision, pause and verify:

- **Before dispatching an implementer:** Do I have the full task text, prior context, and project conventions ready? If any of these is missing, the subagent will produce garbage.
- **Before marking a task complete:** Did both review gates pass? Are all tests green? Is the commit clean?
- **Before moving to the next phase:** Did the user confirm? Is the full test suite passing?
- **Before choosing haiku over sonnet:** Is this task truly simple, or am I just being optimistic?

---

## Exit Action

When all tasks across all phases are complete and verified:

1. Run the full test suite one final time
2. Dispatch a final reviewer (opus) to review the complete set of changes across all tasks
3. Address any final review findings
4. Invoke enggenie:qa-verify to verify all claims with evidence before shipping

---

## Complete Execution Flow

```
Entry: Plan approved OR user request
  |
  v
Phase 0: Worktree Setup
  Detect/create worktree dir -> gitignore check -> create worktree ->
  project setup -> baseline tests
  |
  v
For each phase in plan:
  |
  For each task in phase:
  |  |
  |  v
  |  Dispatch Implementer (RED-GREEN-REFACTOR)
  |  |
  |  v
  |  Dispatch Spec Reviewer
  |  |-- Issues? -> Implementer fixes -> Spec re-review
  |  |-- Clean? -> proceed
  |  |
  |  v
  |  Dispatch Code Quality Reviewer
  |  |-- Issues? -> Implementer fixes -> Quality re-review
  |  |-- Clean? -> proceed
  |  |
  |  v
  |  Mark task complete, record context for next task
  |
  v
  Phase boundary: run full suite, ask user to verify, wait
  |
  v
Next phase (or exit if final)
  |
  v
Exit: Final opus review -> enggenie:qa-verify
```
