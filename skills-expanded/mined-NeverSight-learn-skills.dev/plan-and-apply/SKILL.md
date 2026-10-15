---
name: plan-and-apply
description: Use this skill whenever the user asks to first analyze, first plan, not directly modify code, work in small slices, or complete a non-trivial implementation with clear scope and verification. Also use it whenever the task obviously spans multiple steps, multiple files, migration work, refactoring, page closure work, or requires strong validation and clean handoff. This skill enforces a workflow of read rules first, clarify scope, create the smallest viable plan, apply changes in controlled slices, then verify and close out.
---

# Plan And Apply

This skill is an upper-layer execution workflow for non-trivial development tasks.

It exists to stop four common failures:

- changing code before understanding the task
- drifting outside the requested scope
- doing large rewrites when a local fix is enough
- claiming completion without verification

Use it to control execution rhythm. Do not use it for simple one-step questions or tiny edits that do not need planning.

## When to use

Use this skill when any of these are true:

- the user says `先分析`、`先规划`、`不要直接改`
- the task spans multiple files or modules
- the task is a migration, refactor, or structured feature implementation
- the task needs a clear task list, progress tracking, or staged rollout
- the user cares about strict boundaries, minimal change, or explicit regression checks

Do not use this skill when:

- the user only wants explanation or brainstorming
- the change is trivial, isolated, and low risk
- the task is pure review with no implementation

## Core promise

Follow this order unless the user explicitly asks for a narrower path:

1. Read rules first
2. Clarify task scope and constraints
3. Decide whether planning is required
4. Break work into the smallest viable slices
5. Apply only the current slice
6. Verify the change and do regression checks
7. Close out with result, validation, and remaining risk

## Step 1: Read rules first

Before implementation, read the project-level instructions that control behavior.

Priority order:

1. `lessons.md`
2. `AGENTS.md`
3. task-specific rule files mentioned by the user
4. relevant reference implementation or old version

If there is no `lessons.md`, continue without blocking. Do not invent one.

## Step 2: Clarify the task

Before changing anything, answer these questions from local context:

1. What is the actual requirement?
2. What constraints did the user set?
3. What are the main risks?
4. What is the simplest viable approach?
5. How will the result be verified?

If a key constraint is missing and guessing would be risky, ask a short direct question. Otherwise, proceed with the safest reasonable assumption.

## Step 3: Decide whether planning is required

Planning is required when any of these are true:

- more than one meaningful step is needed
- the task touches multiple files or modules
- the user explicitly asked for planning
- the task includes migration, refactor, or page/module closure
- there are several constraints or non-obvious risks

Planning can be lightweight when:

- the task is a single local edit
- the user clearly wants direct execution
- the verification path is obvious and low risk

Even when planning is lightweight, still do a short internal structure pass before editing.

## Step 4: Build the minimum plan

When planning is required, structure the work in this shape:

`<files> / <action> / <verify> / <done>`

Each slice should have:

- clear target files or directories
- one concrete action
- one concrete verification method
- an obvious done condition

Good slices are small enough to validate independently.

Bad slices are broad, mixed, or vague.

### Planning output

When the user asked to plan first, present:

- goal
- constraints
- risks
- minimum approach
- slices
- verification method

When the user did not ask for a separate planning phase, keep this short and move into execution once the structure is clear.

## Step 5: Apply in controlled slices

During implementation:

- change only files relevant to the current slice
- prefer local edits over rewrites
- follow the existing structure before introducing new abstractions
- do not smuggle in extra optimization or unrelated cleanup
- protect unrelated user changes in the worktree

If a better solution appears but expands scope, stop and surface the tradeoff before taking it.

## Step 6: Verify and regress

No meaningful change is complete without verification.

Always do:

- targeted verification for the requested behavior
- regression checks for adjacent behavior likely to break

Verification should be as concrete as possible:

- build or test command
- static inspection against reference behavior
- file diff sanity check
- UI or interaction check when relevant

If you could not run verification, say exactly what was not verified and why.

## Step 7: Close out cleanly

The final closeout should include:

- what changed
- how it was verified
- any remaining risks or unverified areas

Do not claim completion if validation is missing.

## Hard rules

These rules override convenience:

- do not start with code edits before understanding scope
- do not exceed the requested boundary
- do not do unapproved broad refactors
- do not hide root causes with fallback patches
- do not overwrite unrelated user changes
- do not leave temporary artifacts or debug residue

## Frontend and product handling

When the task is UI or product-facing:

- inspect the current visual language first
- prefer continuity with the existing or legacy implementation
- default to a restrained, dense, product-like layout
- avoid decorative redesign without clear cause
- check mobile, dark mode, and interaction states when they matter

## Suggested task files

For non-trivial tasks, maintain these files when appropriate:

- `task_plan.md`
- `findings.md`
- `progress.md`

Use them to keep the work state externalized and recoverable across long sessions.

## Lightweight execution template

Use this shape when you need a short planning pass before implementation:

1. Requirement
2. Constraints
3. Risks
4. Minimum approach
5. Verification

## Full execution template

Use this shape for non-trivial tasks:

1. Read rules and references
2. Confirm requirement and boundaries
3. Create slices
4. Execute slice by slice
5. Verify each meaningful change
6. Do regression check
7. Close out with evidence and risk

## Example triggers

Example 1:
Input: `先分析一下这个模块迁移方案，不要直接改代码。`
Action: use this skill and produce a structured plan first.

Example 2:
Input: `这个页面补上分页和删除，只改当前目录，做完帮我回归验证。`
Action: use this skill, do a short plan, implement in slices, then verify.

Example 3:
Input: `帮我把这个老组件迁移到新项目，参考旧版实现，别超范围。`
Action: use this skill because the task is migration-based and boundary-sensitive.
