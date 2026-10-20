---
name: follow-agents-md
description: Execute the workspace AGENTS.md fully, with subagents for independent work
argument-hint: "[target]"
related:
  - update-docs
  - review-devin-global-harness
  - use-subagents
  - update-devin
  - create-plan-in-dot-devin

---

## Goal

Follow the workspace `AGENTS.md` completely, using subagents for multi-faceted work

## Scope

Find and follow `AGENTS.md` in every workspace, using subagents when the work involves multiple independent workflows/skills

## Execute

### 1. Update AGENTS.md

> Goal: bring `AGENTS.md` up to date before any other work

1. Always run `/update-agents-md` to write/update `AGENTS.md` first, before anything else
2. Check that `AGENTS.md` is written correctly and is up to date
3. Never skip this step under any circumstance

### 2. Read And Summarize Related

> Goal: know what needs to be done

1. Run `/review-devin-global-harness` to read the relevant workflows/skills
2. Summarize the to-do list: workflows, skills, order, dependencies
3. If several workflows are independent → note them for `/use-subagents`

### 3. Execute AGENTS.md

> Goal: carry out every step in `AGENTS.md`

1. Read `AGENTS.md` in the workspace root and every sub-workspace if it is a monorepo
2. Analyze the specified workflows and skills
3. If there is a single workflow, follow it directly
4. If it is a monorepo: repeat for each workspace
5. If `AGENTS.md` lists many new tasks at once → always run `/create-plan-in-dot-devin` first, then execute per the plan

### 4. Use Subagents

> Goal: run independent workflows in parallel with subagents, always

1. If there are multiple independent workflows/skills (from Step 2) → run `/use-subagents` to spawn subagents working in parallel — 1 workflow = 1 subagent
2. Give each subagent: workspace path, assigned workflow, deliverable, acceptance criteria
3. Merge structured reports from all subagents before verify — subagents must not commit
4. If custom subagent profiles are needed → run `/update-devin-global-subagents` before `/use-subagents`

### 5. Verify Execution

> Goal: confirm all workflows and skills were executed completely

1. Check that every workflow in `AGENTS.md` was invoked
2. Check that every skill was loaded
3. Skip any workflow or skill that does not exist and record it

## Rules

### 1. File Location

- `AGENTS.md` must be in the workspace root and sub-workspaces if it is a monorepo
- If it is a monorepo: follow the `AGENTS.md` of every workspace
- If no `AGENTS.md` exists → fall back to `README.md` as the source of truth for setup, install/run commands, and conventions (verify commands against `package.json`/`Cargo.toml`/`Makefile` before trusting them); if README is missing or stale → `/update-readme-md` (fallback merged from the deleted `/follow-readme-md`)

### 2. Execution Order

- Follow the order specified in `AGENTS.md`
- Confirm the workflows and skills actually exist
- Skip workflows or skills that do not exist
- Use /update-docs if needed

### 3. Plan Always

- A large batch of new work at once (multiple features/files/tasks) → always run `/create-plan-in-dot-devin` before executing per `AGENTS.md`


## Expected Outcome

- All workflows listed in `AGENTS.md` are executed completely
- The skills listed in `AGENTS.md` are loaded
- Every workspace in the monorepo is processed completely
- subagents are used when the work spans multiple independent workflows/skills