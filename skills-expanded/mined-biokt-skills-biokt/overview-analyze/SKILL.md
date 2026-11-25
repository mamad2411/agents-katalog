---
name: overview-analyze
description: Analyse saved /overview logs to track research progress over time — task velocity, stale projects, backlog trends, job activity. Use when reviewing mid/long-term progress, identifying stalled work, or evaluating which projects are moving.
allowed-tools: Read, Glob, Bash
---

# Overview Analyze

Mine the saved `/overview save` logs in `~/Research/logs/overview/` to produce a longitudinal progress digest.

Parse `$ARGUMENTS`:
- *(empty)* — full trends digest across all projects and all logs
- `<ProjectName>` — task-by-task timeline for that one project across all logs

---

## Step 1 — Discover logs

Glob `~/Research/logs/overview/*.md` and sort by filename (filenames are `YYYY-MM-DD_HH-MM.md`, so lexicographic = chronological).

If **0 logs** found: tell the user to run `/overview save` first to create a baseline snapshot.

If **exactly 1 log** found: report the date, list all projects with their open task counts and writing status found in it, and tell the user that trends require at least 2 logs — run `/overview save` again after some time has passed.

If **2+ logs** found: proceed to Step 2.

---

## Step 2 — Parse each log

Read each log file. For every log, extract:

### Per-log metadata
- **Date** — from the `# Research Overview — YYYY-MM-DD` header line
- **Time** — from the log filename (`HH-MM` component)

### Per-project data (repeat for every `## <ProjectName>` section)
- **Project name** — the heading text before `[machine:` (strip trailing whitespace)
- **Machines** — text inside `[machine: ...]`
- **Open task count** — integer N from `**Open tasks (N):**`; default 0 if section absent
- **Running job count** — integer N from `**Running jobs (N):**`; default 0 if section absent
- **Writing status** — value from `**Writing:** <value>` line; default `none` if absent. Valid values: `none`, `draft`, `submitted`, `review`, `published`.
- **Task set** — all lines matching `- [ ] ` → extract the task text (strip the `- [ ] ` prefix); store as a set for diffing

Build a **timeline table**: list of records `(date, project, machines, open_tasks, running_jobs, writing, task_set)` sorted by date then project.

---

## Step 3 — Compute metrics

Work through consecutive log pairs `(log[i], log[i+1])` for each project.

### Task velocity (per project, per interval)
- **Completed tasks**: tasks in `log[i].task_set` that are absent from `log[i+1].task_set`
- **Added tasks**: tasks in `log[i+1].task_set` that are absent from `log[i].task_set`
- **Net**: completed − added (positive = backlog shrinking)

Sum totals across all intervals for each project.

### Project presence
- **Runs present**: count of logs containing this project
- **First seen** / **Last seen**: dates
- **Active job fraction**: fraction of runs where running_jobs > 0

### Stale detection
A project is **stale** if its `task_set` is identical across 3 or more consecutive logs AND running_jobs = 0 in those logs. List the unchanged tasks.

### Backlog trend
Compare open_tasks in the earliest log vs. the latest log for each project. Flag projects where the backlog has grown (latest > earliest).

### Portfolio-level
- Projects present in latest log = active
- Projects absent from latest log but present in earlier logs = completed or dropped (distinguish: completed if open_tasks reached 0, dropped if tasks still open when it disappeared)

---

## Step 4 — Output

### Full digest (empty `$ARGUMENTS`)

```
# Research Progress Analysis — <latest date>
Logs analysed: N  (<earliest date> → <latest date>)

## Portfolio summary
Active projects: X  |  Completed since first log: Y  |  Dropped (tasks unfinished): Z  |  New since first log: W

## Per-project trends  (sorted: worst net progress first)

### ProjectName  [workstation]
Runs present: 8/10  |  Active jobs: 6/10 runs  |  First seen: 2026-01-15  |  Last seen: 2026-04-10
Writing: none → draft → draft  (current: draft)
Tasks completed: 12  |  Tasks added: 5  |  Net: +7 done
Backlog: 9 → 4 open tasks  ▼ improving

⚠️  Stale tasks (unchanged across last 3 logs):
  - Verify ω atom indices after pdb2gmx renumbering

---

### AnotherProject  [gpu-server]
Runs present: 3/10  |  Active jobs: 3/10 runs  |  First seen: 2026-03-01
Tasks completed: 0  |  Tasks added: 6  |  Net: −6 (backlog growing)
Backlog: 2 → 8 open tasks  ▲ worsening

---

## Completed projects
- OldProject — last seen 2026-02-14; reached 0 open tasks ✓

## Dropped projects (tasks unfinished when last seen)
- AbandonedProject — last seen 2026-01-30; 3 open tasks at disappearance

## Flags
⚠️  ProjectX — backlog grew by 8 tasks in last 3 logs
⚠️  ProjectY — stale (no change in 4 logs, no running jobs)
```

### Single-project deep dive (`$ARGUMENTS` = project name)

Show a chronological table of every log that contained this project:

```
# ProjectName — Task Timeline

| Date       | Open | Jobs | Writing   | Completed since prev            | Added since prev               |
|------------|------|------|-----------|---------------------------------|--------------------------------|
| 2026-01-15 |   9  |  2   | none      | (baseline)                      | (baseline)                     |
| 2026-02-01 |   7  |  0   | none      | Task A; Task B                  | —                              |
| 2026-03-10 |   8  |  1   | **draft** | Task C                          | New task X; New task Y         |
| 2026-04-10 |   4  |  2   | draft     | Task D; Task E; New task X      | —                              |

Current open tasks (as of latest log):
- [ ] task one
- [ ] task two
...

Stale tasks (present in every log since first seen):
- [ ] stale task
```

---

## Rules

- Read logs only — do not modify any files.
- If a project appears under different machines across logs, track it as one project (match by name).
- Task matching is exact string comparison after stripping the `- [ ] ` prefix and trimming whitespace.
- If a log is malformed or unreadable, skip it silently and note the skipped filename at the end.
- Dates in output use `YYYY-MM-DD` format.
- If `$ARGUMENTS` is a project name that doesn't appear in any log, say so clearly.
