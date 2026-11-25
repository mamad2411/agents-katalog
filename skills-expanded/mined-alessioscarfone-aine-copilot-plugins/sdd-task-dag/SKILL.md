---
name: sdd-task-dag
description: 'Generates a conservative task-dependency DAG (task-dag.md) from tasks.md using codebase inspection. Groups tasks into conflict-free execution waves where tasks in the same wave touch no shared files. Use when preparing for parallel implementation, before running the sdd-dev-orchestrator, or when asked to "build the task DAG", "plan parallel execution", or "generate task-dag". Do not use for general task listing, project planning outside SDD, or implementation.'
---

> [!IMPORTANT]
> This skill generates the execution plan (`task-dag.md`) for parallel implementation.
 To run the parallel implementation itself, switch to the **sdd-team:sdd-dev-orchestrator** agent.

Builds `task-dag.md` for a change — a conservative dependency graph that groups tasks into sequential waves where tasks within the same wave are safe to run in parallel (no shared files, no logical dependencies).

---

**Input**: Optionally specify a change name (e.g., `/sdd-dev-orchestrator add-auth`). If omitted, infer from conversation context or prompt the user.

---

## Step 1 — Select the change

- Use the provided name if given
- Infer from conversation context if the user mentioned a change
- Auto-select if only one active change exists
- If ambiguous, list directories in `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/` (excluding `archive`) and use the **AskUserQuestion tool** to let the user select

Announce: "Using change: `<name>`"

If `task-dag.md` already exists at `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/<name>/task-dag.md`, show the existing DAG and ask whether to regenerate it or use it as-is.

## Step 2 — Read change artifacts and shared context

Read all of the following:
- `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/<name>/tasks.md` — task list (IDs, descriptions, groups)
- `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/<name>/design.md` — technical approach and decisions
- `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/<name>/proposal.md` — change scope and goals
- `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md` — tech stack, naming conventions (if exists)

If `tasks.md` is missing, stop and tell the user to run `/sdd-propose` first.
If all tasks are already marked `[x]`, congratulate and suggest `/sdd-verify`.

## Step 3 — Inspect the codebase for file touch points

For each task, use search and file-read tools to identify which source files it is likely to touch. Guidelines:
- A task creating a new module → the new file path(s) named in design.md + any index/barrel files that will import it
- A task updating an existing capability → search for the relevant symbols, types, or routes to find affected files
- A task adding tests → the new test file + the implementation file being tested
- A task updating docs/README → only the documentation files

**Be conservative**: when uncertain whether a task touches a file, assume it does.

## Step 4 — Build the dependency graph and agent bundles

### 4a — Assign waves

1. **Explicit dependencies first**: if task B can only be implemented after task A (e.g., B imports a type created by A), place B in a later wave.
2. **File conflict rule**: if two tasks share any file, they must be in different waves. Prefer a safe, low-conflict DAG — when in doubt, serialize.
3. **Group tasks with no dependencies and no file conflicts** into Wave 1.
4. **Repeat** for subsequent waves until all tasks are assigned.

### 4b — Bundle tasks within each wave

Once wave assignment is done, group tasks within each wave into **agent bundles** — a bundle is a list of tasks one agent implements *sequentially*. Multiple bundles in the same wave run in parallel.

Bundling algorithm (per wave):
1. **Candidate bundles by parent group**: tasks sharing the same parent group number (e.g., all `2.x` tasks) that are in the same wave are candidates for a single bundle.
2. **Inter-bundle file conflict check**: compute each candidate bundle's combined file set (union of all member tasks' files). If two bundles in the same wave share any file, they must be merged into one bundle or split across waves — never parallelize bundles that touch the same file.
3. **Order within bundle**: sort member tasks by natural task ID (ascending). The agent implements them in this order.
4. **Assign bundle IDs**: `W<wave>-A`, `W<wave>-B`, … (alphabetical within wave).


## Step 5 — Generate task-dag.md

Read `assets/task-dag.md` for the structure. Fill it in with:
- One row per task in the Task Dependency Table (Task ID, Group, Description, Depends On, Files Likely Touched, Status = `pending`)
- One Wave section per wave with a bundle table showing Bundle ID, ordered task list, combined file set, and status
- DAG Notes summary (total tasks, total waves, total agent slots, bundles per wave, conflicts resolved)

Save to `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/<name>/task-dag.md`.

## Step 6 — Present DAG summary

Show the user:
- The execution wave plan: wave number, number of bundles (= parallel agents), each bundle's task sequence
- Any file conflicts detected and how they were resolved
- Max parallelism: number of bundles in the widest wave
 - Next step: "Switch to `sdd-dev-orchestrator` to start parallel execution."

---

## Guardrails

{SKILL_ASSETS_NOTICE}
- **Conservative first**: when uncertain about file overlap, serialize — never guess at safety
- **No execution**: this skill only generates the plan; it does not launch subagents or modify source code
- **Verify file existence**: before saving, confirm the change directory exists
- **Regeneration**: if `task-dag.md` already exists, always confirm with the user before overwriting
