---
name: writing-plans-self-improvement-assistant
description: Use alongside writing-plans to add evidence-based planning memory, plan-quality linting, reusable planning lessons, and safer future implementation plans without weakening the writing-plans workflow
---

# Writing Plans Self-Improvement Assistant

Use this skill only as a companion to `writing-plans`. It does not replace the main planning workflow. The main skill still controls plan structure, task decomposition, exact file paths, complete code steps, TDD flow, self-review, and execution handoff.

This assist skill adds a durable planning improvement system. It learns from previous plans, execution feedback, reviewer findings, blockers, false starts, task-size mistakes, missing context, test-command failures, and human decisions so future plans become clearer, smaller, safer, and easier for subagents or engineers to execute.

## Core Principle

`writing-plans` creates the implementation plan. This skill improves planning quality over time.

The planning memory is not dumped wholesale into a plan. The controller reads it, extracts only relevant evidence-backed planning lessons, and uses them to improve scope checks, file structure, task boundaries, test strategy, interface definitions, and execution handoff.

A plan remains authoritative only after it is written from the current spec and passes the writing-plans self-review. Memory is a planning aid, not a replacement for the current spec.

## Relationship With writing-plans

This skill extends these planning checkpoints:

1. Before plan writing: read planning memory and prior plan-quality lessons.
2. During scope check: compare the spec against known decomposition risks.
3. During file-structure mapping: reuse known repo conventions without overfitting.
4. During task decomposition: avoid recurring task-size and interface mistakes.
5. During test planning: prefer commands and test patterns proven in the repo.
6. During placeholder scan: apply stronger plan-lint rules learned from prior failures.
7. During self-review: check for prior failure modes before saving the plan.
8. After execution feedback: record lessons that should improve the next plan.

This skill must never weaken writing-plans requirements. It must not allow placeholders, vague steps, missing file paths, incomplete commands, missing expected outputs, undefined interfaces, skipped tests, or broad tasks that cannot be reviewed independently.

## Compatibility Matrix

| Runtime | Support Level | Notes |
|---|---:|---|
| Claude Code with Superpowers `writing-plans` | Native | Primary target. Use alongside the official planning skill. |
| Claude Code without Superpowers | Partial | Can be used as a planning checklist and memory system. |
| Codex or other coding agents | Adapter Required | Use the principles, but verify file locations, skill invocation, and memory behavior. |
| Generic chat assistant | Conceptual Only | Use as a planning quality rubric, not as an executable skill. |

Do not claim this skill is universally executable in all agents. It is portable as a process pattern only when the runtime supports similar file access, plan writing, and memory handling.

## Operating Modes

Choose the lightest mode that fits the work.

### Light Mode

Use for small changes, single-feature fixes, or plans with 1-3 tasks.

- Read only the most relevant planning memory.
- Apply plan lint before saving.
- Update memory only if a durable planning lesson is discovered.

### Standard Mode

Default mode for normal multi-step implementation plans.

- Read planning memory before writing.
- Apply scope, file-structure, task-size, interface, and test-plan checks.
- Save durable lessons after the plan or after execution feedback.

### Strict Mode

Use for security-sensitive work, migrations, large refactors, production-critical systems, multi-agent execution, or plans likely to be executed by fresh subagents.

- Run the full planning checklist.
- Require explicit assumptions and non-goals.
- Add rollback and verification notes where appropriate.
- Use stronger decomposition and interface checks.
- Create or update memory after execution feedback.

## Durable Planning Memory Files

Create and maintain planning memory inside the repository:

```text
.superpowers/planning/plan-memory.md
.superpowers/planning/decision-log.md
.superpowers/planning/plan-review-patterns.md
.superpowers/planning/false-starts.md
.superpowers/planning/test-command-memory.md
```

If the repo already has a Superpowers scratch directory convention, keep this directory near the existing `.superpowers/` files.

### Git Safety Warning

Planning memory files may be untracked or git-ignored. They can be permanently destroyed by `git clean -fdx`, worktree deletion, or workspace reset.

At skill start, identify the memory policy:

- **Tracked memory:** safe to persist in repo, but must be sanitized.
- **Local memory:** useful during active work, but can be deleted by cleanup commands.
- **Unknown policy:** treat as local-risk and warn before destructive cleanup.

Before any destructive git operation, back up `.superpowers/planning/` if the lessons should survive.

## Memory File Responsibilities

### plan-memory.md

Stable planning knowledge useful for future plans.

Examples:

- repo-specific planning conventions
- preferred task boundaries
- important architectural seams
- modules that require extra setup in plans
- generated files that plans should not edit manually
- recurring integration risks
- known dynamic behavior that affects planning
- plan sections that must be included for this repo

### decision-log.md

Explicit human decisions that affect planning.

Examples:

- human chose one architecture approach over another
- human decided to keep backward compatibility
- human rejected a dependency
- human approved a risky migration strategy
- human confirmed a non-obvious product constraint

### plan-review-patterns.md

Recurring plan-quality problems and prevention rules.

Examples:

- tasks too large for one reviewer gate
- missing interface signatures between tasks
- tests planned after implementation instead of TDD
- exact expected output missing from commands
- tasks rely on context from previous task instead of explicit `Interfaces`
- plan omitted migration rollback or data verification

### false-starts.md

Planning paths that looked reasonable but were rejected or failed.

Examples:

- proposed file split conflicted with repo convention
- planned dependency was rejected by constraints
- initial test strategy could not run in this repo
- task decomposition caused cross-task coupling

### test-command-memory.md

Test/build/lint commands that are known to work or fail in this repo.

Examples:

- focused test commands for common modules
- required setup before running tests
- commands that look right but fail because of repo-specific configuration
- expected failure modes when dependencies are missing

## Planning Memory Entry Format

Every entry must be evidence-based.

Use this format:

```md
## YYYY-MM-DD - Short Title

- Type: Planning Convention | Human Decision | Plan Review Pattern | False Start | Test Command | Risk Area
- Scope: repo, folder, module, feature, or plan name
- Confidence: High | Medium | Low
- Evidence: plan path, task number, execution report, reviewer finding, test output, commit range, or human decision
- Rule for future plans: concise instruction that improves future planning
- Expiry: Keep | Re-check after refactor | Re-check after date/version/feature
```

Do not write vague memory such as “this area is complicated” without evidence and a future planning rule.

## Evidence Rules

Create planning memory only from:

- a completed implementation plan
- execution feedback from `subagent-driven-development` or `executing-plans`
- reviewer findings caused by plan quality
- blocker caused by missing planning context
- test/build/lint command results
- explicit human decision
- repeated planning issue seen across at least two plans or tasks
- visible repo convention verified from files and cited in the plan notes

Do not create memory from guesses, vibes, or one-off speculation.

## Pre-Planning Memory Review

Before writing a new plan:

1. Read relevant planning memory files if they exist.
2. Read the current spec or requirements.
3. Identify only memory entries that affect this plan’s scope, architecture, tests, files, or risk.
4. Check whether the current spec conflicts with prior human decisions or repo conventions.
5. If a conflict blocks planning, batch it into one concise question.
6. If the conflict is not blocking, record an explicit assumption in the plan.

Do not stop planning just because memory exists. Memory informs the plan; it does not replace the spec.

## Priority Rules

When the spec, memory, current code, and prior decisions disagree, apply this order:

1. Explicit human decision in the current session.
2. Current spec and requirements.
3. Current code/config evidence with exact file path and line or command output.
4. High-confidence planning memory with evidence.
5. Medium/Low-confidence planning memory.
6. Assumptions.

If memory conflicts with the current spec, do not silently follow memory. Raise the conflict if blocking, or document the assumption if not blocking.

## Scope and Decomposition Assist

During the writing-plans scope check, add these checks:

- Does the spec contain multiple independent subsystems?
- Can each task produce working, testable software independently?
- Would one reviewer be able to reject one task while approving the neighboring task?
- Are setup/config/docs folded into the task whose deliverable needs them?
- Are tasks too small to be meaningful or too large to review?
- Does each task expose clear `Consumes` and `Produces` interfaces?
- Are there hidden dependencies between tasks that must be made explicit?

If the spec spans independent subsystems, suggest separate plans before writing a giant plan.

## File-Structure Assist

Before defining tasks, strengthen the official file-structure mapping with these checks:

- Identify files to create, modify, test, and leave untouched.
- Identify generated files that should not be edited manually.
- Identify risky files that require compatibility or migration notes.
- Identify existing patterns that the plan should follow.
- Prefer focused files, but do not restructure existing code without need.
- If a file split is planned, explain why the split reduces risk or improves task review.

The file-structure map should make task decomposition obvious.

## Task-Quality Lint

Each task must pass this lint before the plan is saved:

```text
[ ] Task has exact files to create/modify/test.
[ ] Task has explicit Consumes and Produces interfaces.
[ ] Task has a failing test step before implementation, unless the task is non-code and explains why.
[ ] Test code is concrete, not placeholder text.
[ ] Test command is exact and has expected failure output.
[ ] Implementation step contains actual code or exact edit instructions.
[ ] Passing test command is exact and has expected passing output.
[ ] Commit command includes exact files and a specific commit message.
[ ] Task can be reviewed independently.
[ ] Task does not rely on accumulated session history.
[ ] Later task signatures match earlier task outputs.
```

If a task fails lint, fix the plan before saving it.

## Strong No-Placeholder Rules

In addition to the official no-placeholder rules, reject these patterns:

- “use existing pattern” without naming the exact file or function to follow
- “validate input” without listing exact invalid inputs and expected errors
- “handle edge cases” without naming each edge case
- “update docs” without the exact doc path and text to add
- “run tests” without command and expected output
- “wire it up” without exact integration points
- “refactor as needed” without exact refactor boundaries
- “ensure compatibility” without compatibility target and verification command
- “similar to previous task” instead of repeating required code or interfaces

## Plan Risk Register

For Standard and Strict Mode, include a short risk register near the end of the plan when relevant:

```md
## Plan Risk Register

| Risk | Why It Matters | Mitigation in Plan | Verification |
|---|---|---|---|
| ... | ... | Task N covers ... | Command/output ... |
```

Use this only for real implementation risks. Do not add boilerplate risks.

## Assumptions and Non-Goals

If the spec is incomplete but planning can proceed safely, include:

```md
## Assumptions

- Assumption with reason and where it affects the plan.

## Non-Goals

- Explicitly out-of-scope item to prevent overbuilding.
```

Do not hide assumptions inside tasks.

## Plan Self-Review Add-On

After the official writing-plans self-review, run this additional checklist:

```text
[ ] Every spec requirement maps to at least one task.
[ ] Every global constraint is copied exactly and reflected in tasks.
[ ] Every task has independent test value.
[ ] Every interface used later is defined earlier or in the same task.
[ ] No task requires the implementer to read the whole plan history.
[ ] No code step contains placeholder prose.
[ ] No test step asserts only that code exists.
[ ] No command lacks expected output.
[ ] No memory entry overrides the current spec.
[ ] Known prior planning mistakes were considered.
```

If any item fails, fix the plan before saving.

## Execution Feedback Loop

After a plan is executed, collect lessons that improve future planning:

- Which tasks were too large or too small?
- Which task instructions were ambiguous?
- Which interfaces were missing or inconsistent?
- Which test commands were wrong or incomplete?
- Which reviewer findings were caused by plan gaps?
- Which blocker would have been prevented by better planning?
- Which assumptions turned out false?
- Which files or modules required non-obvious context?

Write only durable lessons to planning memory.

## False-Start and False-Positive Handling

If a planning approach was rejected or failed, add it to `false-starts.md` only when it can prevent future wasted work.

If a plan reviewer or execution reviewer repeatedly flags a planning concern that has been proven acceptable:

1. Record the evidence.
2. Do not tell future reviewers to ignore the category globally.
3. Provide the evidence as context only.
4. If it recurs multiple times, escalate to the human instead of endlessly documenting it.

## Self-Improvement Proposal Boundary

This skill must not directly edit its own `SKILL.md` during normal planning.

A universal improvement may be proposed only as a patch. The patch must not be applied until the human explicitly approves it or a separate reviewer process approves it.

Never edit an installed/cache copy of this skill. Only propose patches against the canonical source file.

## Universalization Test

Before proposing a skill improvement, answer yes to all five:

1. Would this rule help on an unrelated repo with a different language or framework?
2. Can this rule be stated without mentioning the current repo, files, names, tasks, or business domain?
3. Is this a planning process improvement rather than a project fact?
4. Would it still be valid after the current project is deleted?
5. Does it preserve all `writing-plans` requirements?

If any answer is no, store the lesson in planning memory instead.

## Forbidden Skill Upgrades

Never add these to the skill file:

- current repo, branch, company, product, feature, file, route, class, table, endpoint, or module names
- current project test commands
- current project architecture decisions
- current human decisions
- current false starts or false positives
- one-off task outcomes
- secrets, private URLs, tokens, or credentials
- rules that weaken TDD, exact paths, exact commands, complete code steps, or self-review

## Cross-Agent Distribution Check

If an approved universal skill improvement is applied:

- Update the canonical `SKILL.md` first.
- Synchronize copies installed for Claude, Codex, or other agents manually.
- Verify copies with `diff` or equivalent.
- Record the skill version and changelog entry.
- Do not assume one agent’s local skill cache updated another agent’s copy.

## Skill Changelog

Add only generic, approved skill changes here.

### 2026-07-02

- Initial companion skill for `writing-plans`.
- Added planning memory files, plan-quality linting, execution feedback loop, operating modes, git safety warning, and propose-only self-improvement boundary.

## Controller Checklist

At planning start:

```text
[ ] Announce use of writing-plans if this skill is being used with it.
[ ] Choose Light, Standard, or Strict mode.
[ ] Read relevant planning memory files if present.
[ ] Identify spec-memory contradictions.
[ ] Decide whether planning can proceed or needs one batched question.
```

Before writing tasks:

```text
[ ] Scope is not too broad for one plan.
[ ] File structure is mapped.
[ ] Existing repo conventions are identified.
[ ] Generated/risky files are marked.
[ ] Task boundaries are reviewable.
```

Before saving the plan:

```text
[ ] Official writing-plans header is present.
[ ] Global constraints are exact.
[ ] Tasks use checkbox syntax.
[ ] Every task has exact files, interfaces, steps, commands, expected outputs, and commit command.
[ ] No placeholders remain.
[ ] Plan self-review add-on passes.
```

After execution feedback:

```text
[ ] Record only durable planning lessons.
[ ] Update test-command memory if commands were proven.
[ ] Record human decisions if they affect future plans.
[ ] Add plan-review patterns only if likely to recur.
[ ] Keep memory compact and evidence-based.
```

## Suggested Prompt Add-On for Plan Creation

Use this when asking an agent to create a plan:

```md
Use `writing-plans` with `writing-plans-self-improvement-assistant`.
Before writing the plan, read only relevant planning memory.
Use the current spec as authoritative.
Create a plan with exact files, exact interfaces, TDD steps, exact commands, expected outputs, and frequent commits.
Apply the plan-quality lint before saving.
If memory conflicts with the spec, raise only blocking conflicts; otherwise document assumptions.
Do not update the companion skill itself. If you find a universal improvement, propose a patch separately.
```

## Done Definition

This assist skill is done for a planning session when:

- the plan follows the official `writing-plans` format
- scope and file structure are clearly mapped
- tasks are independently testable and reviewable
- exact paths, code, commands, expected outputs, and commits are included
- no placeholders remain
- assumptions and non-goals are explicit when needed
- memory was used only as evidence-backed context
- useful planning lessons were recorded without secrets or repo contamination
