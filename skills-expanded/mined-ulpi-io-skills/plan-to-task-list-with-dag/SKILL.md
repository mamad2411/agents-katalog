---
name: plan-to-task-list-with-dag
version: 2.0.1
description: |
  Turn a request into a SCHEDULABLE task DAG — atomic tasks with real dependencies, not planning prose:
  challenge scope and pick a planning mode with the user first, explore the real repo so no path is
  invented, then decompose into atomic TASK-NNN entries — each with a ≤3-file write scope, 2-3 testable
  acceptance criteria, a slice-scoped validate command, explicit dependencies, and an assigned agent —
  emitted as one canonical object into matching `.ulpi/plans/<name>.md` and `.json`. Every named path
  comes from observed repo state, the dependency graph stays acyclic, and JSON is the source of truth the
  markdown is rendered from — no phantom files, no circular edges, no task that hides side effects it
  never provisions. Use when the user asks to plan, decompose, or break work into execution-ready tasks.
allowed-tools:
  - AskUserQuestion
  - Read
  - Glob
  - Grep
  - Skill
  - Write
  - TodoWrite
argument-hint: "[feature or planning request]"
arguments:
  - request
when_to_use: |
  Use when the task is to produce a structured, execution-ready plan rather than to code immediately.
  Examples: "plan this feature", "break this into tasks", "make a DAG plan", "decompose this for
  parallel agents". It opens with a scope-challenge question, so confirm intent first. Do NOT use for
  trivial single-file work, high-level brainstorming, code review, direct execution, or to gate a
  finished plan (that's plan-founder-review) — this produces the plan, it does not run or judge it.
---

<EXTREMELY-IMPORTANT>
This skill creates schedulable plan artifacts, not loose planning prose.

Non-negotiable rules:
1. Start with scope challenge and mode selection using AskUserQuestion.
2. Explore existing code before decomposing. Never invent file paths.
3. Build one canonical plan object, then emit both markdown and JSON from it.
4. Every task must have explicit ownership, validation, dependency handling, and an Agent field.
5. Keep the skill body focused on workflow. Load plan schema, agent mapping, and examples from references.
6. Every task needs 2-3 testable acceptance criteria, at least one covering a failure or edge case.
7. Never create tasks touching more than 3 files, never create circular dependencies, never assume codebase structure.
8. If a task claims side effects (persistence, WAL, network I/O, registration), state where the capability comes from.
9. For new files, explicitly assign export/registration/wiring ownership to a task.
10. If a task can be "completed" with placeholders or dead wiring, split semantic hardening into an explicit follow-up.
11. Treat JSON as the source of truth. Render markdown from the same canonical plan object.
12. Do not use vague contract language ("internal update", "eventually skipped", "graceful degradation") without defining owner, behavior, and recovery.
13. Distinguish local reuse from external references. Do not present external docs or clones as local code.
</EXTREMELY-IMPORTANT>

# Plan To Task List With DAG

## Inputs

- `$request`: Optional feature or planning request text

## Goal

Produce a concrete task DAG that is safe to execute:

- scope-challenged
- grounded in real repository structure
- atomic enough for parallel work
- persisted to `.ulpi/plans/<plan-name>.md` and `.ulpi/plans/<plan-name>.json`

## Step 0: Challenge scope before planning

Before decomposing, do a quick overlap check:

- prefer the `codemap` skill if available for semantic search
- otherwise use `Glob`, `Grep`, and `Read`

Identify:

- what already exists
- what can be reused
- what is truly new
- likely prerequisites
- likely non-goals
- whether the request is small enough to execute directly instead of planning

Then use `AskUserQuestion` to confirm:

- planning mode: `EXPANSION`, `HOLD`, or `REDUCTION`
- default post-task review: `claude`, `codex`, `kiro`, `all`, or `none`
- any scope cuts or explicit non-goals

Do not proceed until the scope framing is confirmed.

**Success criteria**: The user has confirmed the scope, selected a planning mode, and chosen a default review posture.

## Step 1: Explore the real code surface

Explore the repository before writing any task:

- likely modules and directories involved
- existing code that partially solves the request
- shared integration surfaces:
  - package roots
  - export barrels
  - registries
  - routers
  - manifests
  - startup hooks
- public surfaces:
  - API routes
  - CLI commands
  - config files
  - schemas
  - persisted formats

Rules:

- prefer semantic search via `codemap` skill when available
- use `Grep` for exact-string validation
- use `Read` on the actual files before naming them in tasks
- never invent paths, modules, or existing helpers

**Success criteria**: Every path named in the plan comes from observed repository state.

## Step 2: Capture planning contracts

Before tasking, record the conditions that make the plan valid:

- prerequisites
- non-goals
- cross-boundary contracts
- capability providers for side effects
- shared integration points
- ship cut if execution stops halfway

Explicitly note:

- where persistence comes from
- who owns export and registration edits
- which public surfaces must remain stable
- which failure paths or isolation invariants must be preserved

**Success criteria**: The plan explains what must already be true and what is explicitly out of scope.

## Step 3: Decompose into atomic tasks

Create tasks that are:

- atomic
- file-scoped
- dependency-aware
- reviewable

Task rules:

- prefer 1 to 3 files per task
- every file in `writeScope` must have an explicit role
- every task needs:
  - `TASK-NNN` id
  - title
  - description
  - `Type`
  - `Priority`
  - `Effort`
  - `Agent` (see Agent Selection Reference in `references/output-format.md`)
  - acceptance criteria
  - `writeScope`
  - `validateCommand`
- include 2-3 testable acceptance criteria per task; at least one must cover a failure or edge case
- for public surfaces, pin the exact signature/examples and add a wrong-shape or wrong-routing check
- for rewrite or composition tasks, add at least one criterion proving existing semantics were not silently dropped
- if a new file needs export or registration, assign that ownership to a specific task
- if a task only creates structure and semantic hardening is still needed, split that follow-up explicitly
- `validateCommand` MUST be SLICE-SCOPED — greenable by THIS task's `writeScope` plus its already-integrated dependencies, and runnable independently of unrelated work:
  - Scope it to the task's own files, never a whole package. For vitest, use `pnpm --filter <pkg> exec vitest run <path/to/file.test.ts>`. Do NOT use `pnpm --filter <pkg> test -- <file>` — the `--` makes vitest ignore the positional and run the ENTIRE package, so unrelated or pre-existing failures leak into this task's gate and can falsely block a correct slice.
  - Every test file the command runs must be in this task's `writeScope` or guaranteed green by an integrated dependency. Never point a task's validate at a test file another task owns and this task cannot fix.
  - Avoid whole-suite/e2e commands that only pass at end-state; if two pieces cannot each validate independently, they belong in ONE task.

**Success criteria**: Each task is executable without hidden context and small enough for independent review.

## Step 4: Map dependencies and maximize parallelism

Add dependencies only when they are real:

- file overlap
- data flow
- API contract
- shared integration surface
- capability provider
- lifecycle or bootstrap dependency

Do not over-constrain:

- independent tasks should stay parallel
- shared-file edits should be made explicit rather than hidden
- circular dependencies are invalid

Use `P0` through `P3` priorities:

- `P0`: foundations that unblock other tasks
- `P1`: core feature work
- `P2`: supporting work and edge cases
- `P3`: optional polish, docs, or cleanup

**Success criteria**: The dependency graph is acyclic, minimal, and exposes real parallel layers.

## Step 5: Render markdown and JSON from one canonical plan object

Before writing output, load `references/output-format.md`.

Write both files:

- `.ulpi/plans/<plan-name>.md`
- `.ulpi/plans/<plan-name>.json`

Requirements:

- markdown and JSON must describe the same tasks
- task ids must match exactly in both files
- dependency JSON is the source of truth
- markdown must not contain `[PLAN]` markers on disk

**Success criteria**: Both artifacts exist and describe the same DAG.

## Step 6: Validate before finishing

Run a final structural pass:

- all task ids exist in markdown and JSON
- every dependency target exists
- no cycles
- no phantom file paths
- no task exceeds sensible write scope
- acceptance criteria include edge or failure behavior where needed
- review default is present

Load `references/examples.md` only if you need a pattern for presentation shape.

**Success criteria**: The plan is schedulable, internally consistent, and ready for execution.

## Guardrails

- Do not skip AskUserQuestion-based scope challenge.
- Do not turn this into direct implementation.
- Do not invent existing files, helpers, or package boundaries.
- Do not keep giant examples or output templates inline in `SKILL.md`.
- Do not add `paths:`. This is a generic workflow skill.
- Do not add `context: fork`. This workflow depends on user interaction mid-process.
- Do not introduce agent-only headers.
- Do not create tasks that touch more than 3 files.
- Do not over-constrain dependencies -- independent tasks must stay parallel.
- Do not hide required shared-file edits behind narrow write scopes.
- Do not let a task claim side effects that require capabilities the task never defines.
- Do not present external docs, clones, or web research as local code unless the path exists in the repo.
- Do not use P1-P4 priorities. This skill uses P0-P3.
- Do not hand-maintain counts, layer summaries, or dependency references separately between JSON and markdown -- derive from canonical plan object.

## When To Load References

- `references/personality.md`
  Use at session start for role, expertise, traits, and communication style.
- `references/knowledge.md`
  Use for DAG semantics, parser assumptions, and plan-object knowledge.
- `references/output-format.md`
  Use before rendering final markdown and JSON artifacts.
- `references/examples.md`
  Use only when you need an example shape for a similar request.

## Output Contract

Report:

1. selected mode and review default
2. plan file paths
3. task count and critical path summary
4. major prerequisites and non-goals
5. any notable risks or cut-line decisions
