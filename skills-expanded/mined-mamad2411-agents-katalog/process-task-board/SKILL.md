---
name: process-task-board
description: "Processes a folder-based task queue — completes tasks and moves them to the output folder together with artifact directories"
---

# Task board processing (folder → folder)

The user provides an **input folder** (pending tasks) and an **output folder** (completed work awaiting review or final completion). The agent completes tasks one at a time or in batches (if the user specifies), creates **artifact directories** when needed, and moves the task file(s) to the output location.

> **User guide (board flow vs `implement-feature`, execution order):** [docs/task-board.md](../docs/task-board.md)

> **Prerequisite:** Paths and filenames are in English (code and structure). Task content or artifacts may be in Estonian only if the user explicitly requests it.

---

## Recommended folder structure (in a project)

Default layout (names may vary by project — the user may supply their own paths):

```
<project-root>/
└── Agent_reports/
    └── Tasks/
        ├── To-Do/         # input — unprocessed tasks
        ├── To-Validate/   # first pass complete; awaiting **`/validate-task-board`** review
        └── Done/          # finally approved (after validation or if skipped)
```

- **`To-Do` → `To-Validate`:** preferred output after completing a task when you want a **second pass** (stronger model) before `Done`.
- **`To-Do` → `Done`:** allowed for simple or low-risk tasks — state this clearly in the summary.
- Optional temporary work folder: `Agent_reports/Tasks/.working/` (gitignore recommended) if you do not want to mix `in_progress` files with the `To-Do` indicator.

The user may supply arbitrary paths, e.g. only `.../To-Do` and `.../To-Validate`. Adjust steps accordingly.

---

## Project defaults file (recommended)

To avoid a long prompt on every run, support a config file alongside the project:

- `Agent_reports/Tasks/board-config.yaml` (preferred)
- if missing, use paths given in the prompt and default rules as in this file

Example:

```yaml
paths:
  # may also be absolute paths outside the git repo
  todo: /Users/your-user/Agent_reports/Tasks/To-Do
  to_validate: /Users/your-user/Agent_reports/Tasks/To-Validate
  done: /Users/your-user/Agent_reports/Tasks/Done

repos:
  include:
    - id: backend
      path: services/backend
    - id: frontend
      path: apps/frontend
  discover:
    enabled: false
    roots: [services, apps]
    max_depth: 4
    ignore_paths: [Agent_reports, node_modules, .git]

execution:
  single_task_at_a_time: true
  create_branch_before_changes: true
  move_completed_to: to_validate   # to_validate | done
  run_validation_pass: true

git:
  strategy: ask            # ask | mr | auto_merge_target
  merge_target_branch: develop
  checkout_target_after_merge: true
```

If the user prompt and config conflict, **the user prompt wins**.

---

## Task file format

Each task is preferably a **Markdown** file (`.md`); `.txt` is also acceptable.

Recommended YAML frontmatter:

```yaml
---
id: PROJ-1842
type: code              # code | analysis | validation | breakdown | epic
code_workflow: implement-feature  # optional: implement-feature | fix-bug | refactor
title: Short title
source: jira
jira_id: ""             # optional: Jira key (e.g. VAHE-3174), set by business-brief-to-tasks
epic_of: ""             # optional: parent epic id, set by business-brief-to-tasks
status: open            # open | in_progress | pending_validation | done | blocked | needs_revision
depends_on: []          # optional: list of blocking task ids
follow_up_tasks: []     # optional: ids of follow-up tasks created during processing
---
```

Fields added automatically during the validation pass (`/validate-task-board`), not set at creation: `validation_status`, `validated_at`, `reviewer`.

**`type` drives behavior:**

| `type` | Action |
|--------|--------|
| `code` | Do **not** limit yourself to “writing code only”. Follow **`type: code` — chaining** below; select and **execute fully** one primary workflow (`implement-feature`, `fix-bug`, or `refactor`) together with the **sub-workflows** described there (slash commands). |
| `analysis` | Produce structured analysis (goals, constraints, options, recommendation). Add diagrams (`mermaid`), data model sketches, API patterns as needed — keep them **in the same artifact directory**. If the analysis requires deep codebase understanding, start with **`/analyze-codebase`**. |
| `validation` | Follow the **`/validate-external-proposal`** workflow (or its checklist). |
| `breakdown` | Follow **`/business-brief-to-tasks`** — create smaller tasks in the **`To-Do`** folder (or the queue the user specified); mark this task complete only after subtasks are created, then move per output rules (`To-Validate` or `Done`). |
| `epic` | Like `breakdown`, but allow **EPIC**-level items (large bundles) + subtasks in subfolders; do not cram large work into one overly small file. |

If frontmatter is missing: infer `type` from the task text and ask the user for confirmation if uncertain.

---

## `type: code` — chaining with existing workflows

**This file (`/process-task-board`) only sequences tasks and folders.** For code-changing tasks, the **main work** is always in the corresponding **command/workflow** — the agent must run the right command (e.g. `/implement-feature`) and **complete every phase in order**, not a shortened “patch only” version.

### Choosing the primary workflow

| Situation | Primary workflow | Note |
|--------|-----------------|--------|
| New functionality, extension | **`/implement-feature`** | Default when the task does not describe a bugfix |
| Bugfix, regression | **`/fix-bug`** | Use `code_workflow: fix-bug` or a clear bug description in the task |
| Structural change, **same behavior** | **`/refactor`** | If behavior changes → that is a `feat` or `fix`, not a refactor |

If the task has **`code_workflow`** in frontmatter, follow it. If missing, choose using the table.

### Which sub-workflows must follow (summary)

These are **embedded** in the chosen primary workflow file; the agent must not skip them if that workflow requires them:

| Primary workflow | Typical internal references (read and follow in full) |
|-----------------|------------------------------------------------------|
| **`implement-feature`** | `/analyze-codebase` → `/create-branch` (feature) → implement → `/update-docs` → `/run-tests` → `/conventional-commit` → MR draft |
| **`fix-bug`** | `/analyze-codebase` → `/create-branch` (fix) → fix + regression test → `/run-tests` → `/update-docs` → `/conventional-commit` → MR draft |
| **`refactor`** | `/analyze-codebase` → `/run-tests` (before change) → `/create-branch` → refactor → `/run-tests` → `/update-docs` → `/conventional-commit` |

Each referenced slash command points to the canonical workflow with the same ID; run it in full when you need more detailed steps.

### Other code-related tasks (less common)

- **Documentation only** (no code changes): follow **`/update-docs`**.
- **Dependency audit / upgrade**: follow **`/update-dependencies`** (when the task is specifically about dependencies).
- **Release preparation**: follow **`/release`** (when the task requires it).

If the task explicitly says “do not branch / do not commit” (e.g. spike), note an **exception** in the task file and summary and stay within what the user allowed.

---

## Index of existing workflows (repos `skills/`)

For use with this board (full list):

| Workflow | Use |
|---------|--------|
| `implement-feature` | New functionality cycle |
| `fix-bug` | Bugfix |
| `refactor` | Structure without behavior change |
| `analyze-codebase` | Base exploration, AGENTS.md context |
| `create-branch` | Branch creation |
| `run-tests` | Tests + lint + coverage |
| `update-docs` | CHANGELOG, README, OpenAPI, diagrams |
| `conventional-commit` | Commit message |
| `update-dependencies` | Dependency updates |
| `release` | Release cycle |
| `business-brief-to-tasks` | Breaking down business requirements |
| `validate-external-proposal` | External proposal review |
| `validate-task-board` | To-Validate review |
| `process-task-board` | This file — queue and folders |

---

## Work protocol

### 1. Initialization

1. Load project config if present: `Agent_reports/Tasks/board-config.yaml`.
2. If the user **does not supply paths**, use config `paths.*`; if config is missing, assume from project root: input **`Agent_reports/Tasks/To-Do/`**, output **`Agent_reports/Tasks/To-Validate/`** (create folders as needed).
3. If config has `repos.include`, use those paths for tests and changes.
   If `repos.discover.enabled: true`, discover repos only under `roots` and skip `ignore_paths`.
4. Set execution mode:
   - by default **one task at a time** (`single_task_at_a_time: true`);
   - do not start the next task until the current one is finished and moved.
5. Ensure input and output folders exist (create output if needed).
6. List tasks in the input folder; order:
   - first those without `depends_on` or with satisfied dependencies;
   - skip `blocked` unless the user says otherwise.

7. If the user asks to go **straight to `Done` without `To-Validate`**, set output to `Agent_reports/Tasks/Done/` (or the path they gave).
8. If the queue has `type: code` tasks, set Git strategy:
   - if `git.strategy` is `mr` or `auto_merge_target`, use it **without extra questions**;
   - if `git.strategy` is `ask` (or missing), ask once before the first code task:
     - **MR:** commit to branch, end state MR-ready
     - **auto-merge:** commit to branch, merge into `git.merge_target_branch` and check out `git.merge_target_branch` again
   Save the choice for the run and apply to all `type: code` tasks in the same run unless the user says otherwise.
9. If `execution.create_branch_before_changes: true`, apply a **strict branch rule** for each `type: code` task:
   - before changing the first file, the **active branch must** be a work branch (e.g. `feature/*`, `fix/*`, `hotfix/*`), not the target branch;
   - if the active branch is `git.merge_target_branch` (or `main`/`develop`), run `/create-branch` first, then start changes;
   - if branch creation fails or you cannot safely continue, mark the task `blocked` and do not make code changes on the target branch.

### 2. Processing one task

1. Move or copy the active task temporarily to **`Agent_reports/Tasks/.working/`** (create under `Tasks` if the user agrees) or set `status: in_progress` in frontmatter and leave under `To-Do` for now.
2. Read the task in full.
3. Complete the task according to `type`:
   - **`type: code`:** run the chosen primary command/workflow (`/implement-feature`, etc.) and **complete all phases**; each slash command in a phase means **full** application of the workflow with that name, not just the title.
   - If Git strategy was already set during initialization (config or asked once), treat it as input to the main code workflow and **do not ask the same strategy again** inside each task.
   - **Other `type`:** follow the corresponding row and referenced workflow.
   - Use repo tools (tests, search) as usual.
4. **Artifact directory:** if the task produces multiple files (diagrams, CSV, code snippets, models):
   - Create a subfolder under **output** (e.g. `To-Validate`): `<id>-<slug>/` (slug derived from `title`).
   - Add a short `README.md` in that folder: what was done, where the main artifact is.
   - Place all result files there.
5. If the task is a single file (e.g. answer only in markdown), you may place it **directly** in the output folder; for multiple files prefer one subfolder (step 4).
6. **Update the task file content as required:**
   - append an **Execution summary** section:
     - what was done
     - which conditions were met / what was not completed
     - references to commit, branch, MR, artifacts, and test results
   - update frontmatter to reflect actual state (do not default to `done`):
     - if work goes to validation: `status: pending_validation`
     - if work goes straight to Done folder: `status: done`
     - if conditions were not met: `status: needs_revision` or `blocked`
   - if the task has acceptance criteria, mark each item (done / partial / blocked) in the same summary.
7. Move the final task file to the output folder (or the same `<id>/` folder with artifacts).
8. Remove the duplicate from the temporary work folder if you used copy.
9. If conditions cannot be met because a new task is needed:
   - create a new task in **To-Do** with correct format (new `id`, clear `title`, `type`, rationale);
   - add a reference from the original task to the new one (e.g. `follow_up_tasks: [NEW-ID]` or link/id in the summary section);
   - mark the original task complete only within its scope (`status: pending_validation` or `done` per output rules), not “done by default”;
   - state clearly what was handed off to the new task.
10. If the task changed code:
   - **MR strategy:** leave changes on the branch and note branch/MR info in the task summary.
   - **auto-merge strategy:** merge into that repo’s `git.merge_target_branch` (default `develop`), then switch back to `git.merge_target_branch` in the same repo.
   - Only then start the next task.

### 3. Reporting

After a batch or all tasks: table / list — which files went where, what stayed `blocked`, what needs a human decision.

---

## Safety and quality

- Do not delete original files in the input folder until output is verified; prefer **moving** after successful completion.
- If the task requires secrets or production data — **stop** and ask the user.
- If the task is too vague — set `blocked` with a reason or create subtasks (`breakdown`).

---

## References

- Full cycles: **`/implement-feature`**, **`/fix-bug`**, **`/refactor`** (including **`/analyze-codebase`**, **`/create-branch`**, **`/run-tests`**, **`/update-docs`**, **`/conventional-commit`**, etc. inside them)
- Breaking down business tasks: **`/business-brief-to-tasks`**
- Partner / external proposal review: **`/validate-external-proposal`**
- Second pass / `To-Validate` → `Done` or `To-Do`: **`/validate-task-board`**
