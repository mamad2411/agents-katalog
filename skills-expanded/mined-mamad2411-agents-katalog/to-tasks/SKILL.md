---
name: to-tasks
description: Break a plan, spec, or PRD into sequential local task files under .tasks/, checked into the repo. Use when user wants to convert a plan into a local task backlog, break a feature into sequential chunks, or set up work without GitHub issues. Companion to /next-task.
---

# To Tasks

Break a plan into sequential tracer-bullet task files, checked into `.tasks/`.

Tasks are **always sequential** — no parallel work. Each task is worked one at a time via `/next-task`, with the context cleared between tasks to keep the agent from getting overwhelmed.

Only one feature at a time — `.tasks/` holds the current feature's plan and is deleted when the feature is done.

## Process

### 1. Check for an existing plan

If `.tasks/` already exists and contains task files, stop and tell the user. Either they need to finish the current feature (via `/next-task`) or explicitly discard it before starting a new plan.

### 2. Gather context

Work from whatever is already in the conversation context. If the user passes a plan/spec/PRD reference (path, URL), read it in full.

### 3. Explore the codebase (optional)

If you have not already explored the codebase, do so to ground the plan in the current code. Task titles and descriptions should use the project's domain glossary vocabulary and respect ADRs in the area you're touching.

### 4. Draft sequential tasks

Break the plan into **sequential tracer-bullet tasks**. Each task is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

<rules>
- Tasks are ordered — later tasks may depend on earlier ones
- Each task must be small enough to fit comfortably in one focused context window
- Each task delivers demonstrable end-to-end behavior on its own
- Prefer many thin slices over few thick ones
- Do NOT identify parallel work or "blocked by" relationships — the order IS the dependency
</rules>

### 5. Quiz the user

Present the proposed breakdown as a numbered list. For each task, show:

- **Title**: short descriptive name
- **What**: one-line description
- **Key acceptance criteria**: 2-3 bullets

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Should any tasks be merged, split, or reordered?
- Is anything missing?

Iterate until the user approves the breakdown.

### 6. Set up the feature branch

Pick a short kebab-case feature name (e.g. `credential-storage`, `add-model-wizard`) — used for the branch and for `TODO.md`'s heading.

Check the current branch:

    git branch --show-current

If on `main`, `master`, or `develop`, switch to a new feature branch named `<slug>/<feature-name>` where `<slug>` is the git user handle (`git config user.name`).

If already on a non-main branch, stay on it — the user has picked the branch deliberately.

### 7. Write the task files

Create `.tasks/` and write:

- `TODO.md` — feature overview and checkbox list of tasks
- `NN-<slug>.md` — one file per task, zero-padded numbers (`01`, `02`, ...)

<todo-template>
# <Feature name>

<1-2 paragraph description of what's being built and why.>

## Tasks

- [ ] 01: <title> — [details](01-<slug>.md)
- [ ] 02: <title> — [details](02-<slug>.md)
- ...
</todo-template>

<task-file-template>
# NN. <Task title>

## What to build

Concise description of this vertical slice. Describe end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline the decision-rich parts.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
</task-file-template>

### 8. Commit the plan (and any context/ADR updates)

If the planning conversation produced changes to `CONTEXT.md`, ADRs under `docs/adr/`, or other project documentation, include them in this initial commit — they belong on the feature branch with the plan that motivated them.

    git status                     # confirm what's being committed
    git add .tasks/ CONTEXT.md docs/adr/  # plus any other touched docs
    git commit -m "chore: plan <feature-name> tasks"

Then tell the user:

> Feature branch created and plan committed with N tasks. Run `/clear` to start with a fresh context, then `/next-task` to start on task 01. Clear the context between tasks.
