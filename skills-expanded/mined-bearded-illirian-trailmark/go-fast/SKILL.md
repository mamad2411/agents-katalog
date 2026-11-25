---
name: go-fast
description: |
  Thin entry point into a self-organizing skill chain for a fast-track task.
  Creates a task (slug, number, task.md, routing.db entry) and passes control
  to `idea-first`. The chain then runs autonomously via `Skill()` calls.

  Use when: "/go-fast", start a fast-track task, quick task with autonomous
  routing through the skill chain.
---

# /go-fast

Thin entry point into a self-organizing skill chain for a fast-track task.
Creates a task and passes control to `idea-first`. The chain then runs
autonomously via `Skill()` calls:

```
go-fast → idea-first → habit-first / arch-first / audit-first → per-block cycle → ship-first
```

Usage:
- `/go-fast {task description}` — inline description
- `/go-fast` — asks for description

## Input

A task description (inline after `/go-fast` or requested via prompt); optional project id from a prior `/go-start` invocation.

## Output

A task folder `{tasks_root}/log/{date}-{slug}/` containing `task.md`; a new row in `routing.db` `artifacts` table with `status='open'`; session context (`{slug}`, `{log_dir}`, `{project_id}`) populated for downstream skills.

## Hands off to

`idea-first` — determines task type (product / feature / fix) and routes to the correct branch (`habit-first` / `arch-first` / `audit-first`).

---

## Step 1 — Determine project

**Early return** — if `{project_id}`, `{project_path}` and `{project_name}` are already set in session context (e.g. after `/go-start`) — use them without re-asking. Output confirmation with override option:

```
Using project from go-start: {project_name}
Override? (Enter / no — continue with this, or number from list)

1. {project 1}
2. {project 2}
...
```

| Response | Action |
|---|---|
| Enter, "no", empty | Use the set `{project_id}` — go to Step 2 |
| Number from list | Set new `{project_id}` + `{project_path}` + `{project_name}` — go to Step 2 |

**Standard flow** — if `{project_id}` is NOT set (go-fast called without go-start):

Read the projects config and show only `status: active` projects:

```
Which project is this task for?

1. {project 1}
2. {project 2}
...

Enter number:
```

Wait for answer. Save chosen project `id` and `path` as session context: `{project_id}`, `{project_path}`, `{project_name}`.

---

## Step 2 — Receive task

If task description was provided inline after `/go-fast` — use it directly.
If not provided — ask `What are we doing?` and wait.

**After receiving the description — immediately proceed to Step 3 → Step 3.5. No clarifying questions about protocols, task type or execution flow. Task type will be determined by idea-first.**

---

## Step 3 — Create task log

Get current date: `date +%Y-%m-%d`.

Create short slug from task description (2-4 words, lowercase, hyphens, latin) — this is `{short_slug}`.

**Auto-assign task number:**

```bash
next_number=$(sqlite3 {tasks_root}/routing.db \
  "SELECT COALESCE(MAX(number), 0) + 1 FROM artifacts;")
```

Form the full slug: `{slug}` = `{project}--{next_number}-{short_slug}`.

Log dir: `{log_dir}` = `{tasks_root}/log/{date}-{slug}/`.

Create directory and write `{log_dir}/task.md`:

```markdown
# {slug}

**Date:** {date}
**Project:** {project name}
**Type:** fast-track

## Task

{full task description}
```

**Register task in routing.db immediately:**

```bash
sqlite3 {tasks_root}/routing.db \
  "INSERT OR IGNORE INTO artifacts (id, type, project, title, file_path, status, created_at, number)
   VALUES ('{slug}', 'fast-track', '{project}', '{title}',
           'tasks/log/{date}-{slug}/task.md', 'open', '{date}', {next_number});"
```

Task is visible in downstream browsers from the moment of creation.

**Save as session context** — `{log_dir}`, `{slug}`, `{project}`, `{project_path}`, `{date}`. These variables are inherited by all subsequent skills; their Step 0 will pass automatically.

---

## Step 3.5 — Skill(idea-first)

Call `/idea-first` without any parameters. idea-first:
- Will ask 5-7 Discovery questions
- Will determine task type (product / feature / fix)
- Will write artifact `idea-first-{N}.md`
- Will pass control to the next skill on its own (`habit-first` / `arch-first` / `audit-first`)

After calling `/idea-first` the `/go-fast` command is complete. Further routing — inside the skill chain:

| Type (determined by idea-first) | Next skill | What happens |
|---|---|---|
| New product | `habit-first` | Habit Brief → `arch-first` → per-block |
| New feature | `arch-first` | Decomposition → per-block (flow → library → plan → execute → ship) |
| Fix / problem | `audit-first` | Holes table → per-block for each hole |
| Hot-fix | (idea-first skipped) | Execute directly |

**Escalation to `/brief`:** if idea-first or library-first determine the task is too large (LOC > 150 or >3 "From scratch ⚠️" rows) — they will suggest `/brief` themselves. go-fast does not hold this logic.

---

## Rules

- ALWAYS create `task.md` before calling `/idea-first`.
- The `/go-fast` command ends after Step 3.5. Final task closure is the responsibility of `ship-first`, which will be called from `arch-first` / `audit-first` after all blocks are closed.
- For a sandbox project (id = 0): skip INSERT in routing.db (Step 3) and any deploy operations in subsequent skills.
- NEVER write "done" / "task completed" at the end of `/go-fast` — the task is just beginning. The skill chain will close it through `ship-first`.
