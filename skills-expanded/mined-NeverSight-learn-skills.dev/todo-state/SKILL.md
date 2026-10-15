---
name: todo-state
description: >-
  Use when the user invokes /todo-state, says "mark X as done", "tick off task Y",
  "uncheck that", "set this to in-progress", "mark this project done", or wants to record
  progress without a full execution pass — and equally when they say "is the index
  accurate", "does the todo match reality", "audit my project statuses", "this says done
  but it never shipped", or suspect hub state has drifted from what actually happened in
  the repos. Edits tasks.md checkboxes and the owning active or archived registry row in
  sync; audits recorded status against tasks and git evidence and fixes drift only on
  confirmation. Replaces the former /todo-update-state (now the default mode) and
  /todo-sync (now `audit`) — treat either of those spellings as an invocation of this
  skill.
---

# Project State Skill

You own the hub's **recorded state** — task checkboxes and registry rows — in both
directions:

| Mode | Trigger | Writes |
|---|---|---|
| **set** (default) | the user tells you what changed | exactly the requested edit |
| **audit** | the user asks whether the record is honest | nothing until they confirm |

Set mode is the lightweight write companion to `todo-execute`: use it when the user just
wants to *record* progress without the agent doing the work. Audit mode checks the record
against reality — a project marked `done` whose branch never merged, an `in-progress`
project whose PR landed weeks ago, ticked tasks with no commits anywhere. Each is drift,
and drift compounds: triage routes wrong, refer misleads, sort lies.

Both modes touch the same two surfaces:

- **`tasks.md`** in each project — task checkboxes: `- [ ]` (not done) and `- [x]` (done)
- **`index.md` / `archive.md`** in the hub root — active and completed project rows,
  including `status`, `started`, and `completed` columns (see
  [Date stamping](#date-stamping))

## Execution tier

Hybrid, matching the hub's house pattern. The **edits are mechanical** — use the **fast**
tier from [`../todo-llm-routing/SKILL.md`](../todo-llm-routing/SKILL.md) when dispatching
is available, otherwise perform them inline. Audit mode's **evidence-gathering across 3+
projects** is mechanical too and delegates the same way; for 1–2 projects gather inline.
The drift *verdicts* are judgment — always yours, inline on the main model.

## Hub location

The hub repo root is `$TODO_HUB` — an environment variable pointing at your hub folder
(default `~/todo`). Resolve **every** path against this absolute root — active
`index.md`, cold `archive.md`, and each project's `path`/`tasks.md` — regardless of the
current working directory. This skill may be invoked from another repo; never assume cwd
is the hub. Pass this absolute root to any edit subagent so it writes there, not into the
cwd. (Same convention as `todo-refer`.)

## How the user invokes this

```
/todo-state queue-migration          ← show that project's state, then edit it
/todo-state queue-migration done     ← mark the whole project done
/todo-state                          ← ask which project, or act on context
/todo-state audit                    ← audit every ready/in-progress/done project
/todo-state audit queue-migration    ← audit one project
/todo-state audit fix                ← audit, then apply confirmed fixes
```

The user will usually say what they want in plain language. Set mode: "mark the migration
done", "tick off the first two tasks", "uncheck task 3", "set queue-migration back to
ready". Audit mode: "does my registry match reality", "audit the hub", "is the index
accurate". Interpret that against the resolved project.

---

# Set mode

## Step S1 — Resolve the project

Resolve exact short-names in `$TODO_HUB/index.md` first, then `$TODO_HUB/archive.md`
only on an active miss. Record the owning file and section with the full path and status.

- Short name → look it up active-first to get the `path`
- Full path passed directly → use as-is
- Duplicate across both registries → stop; the hub is corrupt and choosing one loses state
- Not found in either registry → tell the user and stop
- No project named and it's not obvious from context → ask which project before changing anything

## Step S2 — Show current state before editing

Read the project's `tasks.md` and report the current checklist with each task's checkbox
state, plus the current `status` and whether its row is active or archived. This grounds
the edit so the user (and you) act on what's actually there, not what you assume. Number
the tasks so the user can refer to them ("task 3").

If `tasks.md` is missing or empty, say so — there's nothing to check off yet, and
`/todo-plan <name>` is the way to create tasks.

## Step S3 — Apply the requested change

Make exactly the edits the user asked for. The common operations:

**Mark a task done / not done** — flip the checkbox in `tasks.md`:
- done: `- [ ] …` → `- [x] …`
- not done: `- [x] …` → `- [ ] …`

Match on the task's text, not its position alone, so you edit the right line even if the
list shifts. If the user refers to a task by number, map the number to the task you showed
in Step S2.

**Mark the whole project done / not done:**
- "done" → check every task in `tasks.md` and set `status: done` in `index.md`
- "not done" / "reopen" → the user will usually mean the status, not unchecking every task; confirm whether they want tasks unchecked too before doing it, since that's destructive to recorded progress.

**Change status only** — update the owning row's `status` column to one of `planning` /
`ready` / `in-progress` / `done`; the archived-project reopen rule below still applies.

Before a flip to `in-progress` or `done`, run:

```bash
python3 <todo-graph-skill-dir>/scripts/graph-report.py context \
  "$TODO_HUB" "<short-name>"
```

Refuse the status flip when a hard prerequisite is unsatisfied or an incident graph
identity/cycle issue exists. Name the blocker and point at `/todo-graph why <short-name>`
or `/todo-graph audit`. Context and lineage edges never gate state. A direct state edit
must not bypass the same dependency gate that `/todo-execute` enforces.
If the helper is unavailable, stop before a flip to `in-progress` or `done`; do not infer
dependency safety from the registry's legacy `related` cell.

**Reopen an archived project** — any status change away from `done` is also a registry
move. Remove the row verbatim from its section in `archive.md`, append it to the same
section in `index.md`, then update status and dates there. Preserve custom section names;
if a legacy row's source section is unknown, ask before moving it. The row move, status
change, and date clearing are one atomic edit.

Do not touch anything the user didn't ask about. Leave `plan.md`, `research/`, and
`artifacts/` alone — this skill edits state, not content.

## Step S4 — Keep status and tasks in sync

After editing, the project's status in its owning registry row and its task completion in
`tasks.md` should tell the same story. When they'd otherwise disagree, reconcile — and
say what you did:

- All tasks now checked, but status isn't `done` → offer to set it `done` (or just set it and report, if the user already said "mark done").
- A task got unchecked on a project marked `done` → it's no longer truly done; flag it and suggest moving status back to `in-progress`.
- First task checked on a `planning`/`ready` project → work has started; suggest `in-progress`.

Don't silently override the user's explicit instruction — if they said "set status to
ready" while tasks are all checked, do what they asked and just note the mismatch.

**Archive housekeeping:** if the `tasks.md` you touched exceeds 20,480 bytes, mention it
and offer `/todo-archive <short-name>`. When this skill itself flips a revision tag to a
case-insensitive `[done…]`, immediately apply `todo-archive`'s canonical single-entry
rule: add `<a id="revision-r<n>"></a>` before the exact journal entry and leave
`[journal:R<n>](artifacts/journal.md#revision-r<n>)` in the two-line tombstone. Never
archive ordinary task checkboxes.

## Step S5 — Confirm what changed

Report the edits plainly: which tasks flipped, the new completion count, and the status
before → after. If a status flip stamped or cleared a `started`/`completed` date, say so
in the same line. Keep it short. If you reconciled a mismatch in Step S4, say so
explicitly so the user knows state was kept consistent.

---

# Audit mode

Detection is the deliverable; **fixing needs a yes**. Report first, then apply only the
corrections the user confirms, through set mode's edit rules.

## Step A1 — Resolve scope

Read `$TODO_HUB/index.md`. Default scope is every active `ready`, `in-progress`, or
`done` row; `planning` has nothing to drift against. An explicit short-name resolves
active-first, then by exact match in `archive.md`. Duplicate or missing names stop.

## Step A2 — Gather evidence per project

Four sources, cross-checked:

1. **Recorded status** — the `status` column.
2. **Task state** — `done/total` via the [shared awk snippet](#counting-tasks), plus
   case-insensitive open `### R<n> … [open]` revision headings.
3. **Repo evidence** — when the row names a local repo:
   ```bash
   git -C <repo> fetch origin --quiet
   git -C <repo> branch -a --list '*todo/<short-name>*' '*feat/*'
   git -C <repo> log origin/<base> --oneline --since='30 days' -- <plan-scoped-paths> | head -5
   gh pr list --repo <owner>/<repo> --search 'head:todo/<short-name>' --state all --limit 3
   git -C <repo> worktree list | grep '<short-name>'
   ```
   Take what succeeds (no gh auth, no repo → note the gap, don't fail the audit). What
   you want per project: **branch merged / PR open / commits exist / worktree lingering /
   no trace at all**.

   Hub-only projects (repo `-`) are checked on sources 1–2 plus artifacts: `done` with an
   empty `artifacts/` is suspicious; say so.

4. **Project-graph evidence** — run one bounded audit for the hub, then associate its
   incident issues and hard blockers with each in-scope project:
   ```bash
   python3 <todo-graph-skill-dir>/scripts/graph-report.py audit "$TODO_HUB"
   ```
   An in-progress project with an unsettled prerequisite is **at risk**; a done project
   with one is graph drift. Context and lineage edges never count.

## Step A3 — Judge drift

Compare the sources. The canonical mismatches and their fixes:

| Recorded | Evidence | Drift | Suggested fix |
|---|---|---|---|
| `done` | open tasks or `[open]` revisions | not actually done | status → `in-progress` |
| `done` | branch never merged / PR open | shipped on paper only | status → `in-progress`, point at `/todo-push` |
| `in-progress` | all tasks ticked, PR merged, worktree clean | finished but never recorded | status → `done` (via `/todo-verify` if plan.md has a `## Verification` block — the gate flips `done`, not this skill) |
| `ready`/`in-progress` | no commits, no worktree, tasks all unticked | stale — never started | status → `ready`, or ask if it's abandoned |
| any | ticked tasks but no commits/artifacts evidencing them | unbacked claims | flag the specific tasks; suggest `/todo-review <name>` for the audit-by-diff |
| any | lingering worktree with uncommitted changes | work at risk | surface it — `/todo-refer <name> resume` before anything else |
| `in-progress` | hard prerequisite is no longer settled | execution order at risk | stop execution; `/todo-graph why <name>` |
| `done` | hard prerequisite is unresolved or dishonest | completion graph is inconsistent | audit evidence; do not auto-reopen |

Evidence gaps (couldn't check gh, repo missing locally) make a project **unverifiable**,
not drifted — report it in its own bucket, never guess a verdict from partial evidence.

## Step A4 — Report the drift board

```
## 🔎 Hub audit — 14 projects checked

| project | recorded | evidence | verdict | fix |
|---|---|---|---|---|
| queue-migration | done | PR #42 still open | ❌ drifted | → in-progress, ship via /todo-push |
| api-token-rotation | in-progress | merged, 20/20 tasks | ❌ drifted | → done (verify gate first) |
| service-auth | ready | no repo locally | ⚠️ unverifiable | clone repo or fix repo column |
| 11 others | — | — | ✅ consistent | — |

2 drifted · 1 unverifiable · 11 consistent
```

Every drifted row cites its evidence (PR URL, branch, task numbers) — a verdict without
the evidence line is not reportable.

## Step A5 — Apply fixes (only on a yes)

If invoked as `/todo-state audit fix`, or the user confirms after the board: apply exactly
the confirmed corrections — status changes in the owning registry, checkbox reconciliation
in `tasks.md`, and any required archive→active row move — following set mode's Step S3 and
Step S4 rules **including [Date stamping](#date-stamping) in full** (delegate the
mechanical edits to the fast tier when available). Re-render the fixed rows.

Never fix silently, never fix beyond what was confirmed, and never flip a status to `done`
past an unrun `## Verification` gate — point at `/todo-verify` instead.

---

## Date stamping

**This section is the authority on `started` / `completed` / `elapsed (days)` for the
whole hub.** Other skills that flip a status — `todo-execute`, `todo-verify`,
`todo-revise`, `todo-archive` — apply these same rules.

`started` picks the earliest reliable signal, in priority order — **`in-progress` >
`ready` > `planning` > `completed`**. The tiers exist because the early signals only say
work is *intended* (project created, plan confirmed) while a real `ready`→`in-progress`
flip says work *began*: lower tiers stamp provisionally, higher tiers overwrite them, and
the real start is never overwritten. Whenever an edit changes a row's `status` cell, also
update that row's `started` / `completed` cells, using today's date (`YYYY-MM-DD`):

- **Flips to `planning`** (new project via `/todo-add`) — stamp `started` to today if it's
  currently `-`. This is the lowest-tier provisional stamp — see the overwrite rules below.
  A flip *back* to `planning` on an existing project (rare) leaves `started`/`completed`
  unchanged — it's not a new project.
- **Flips to `ready`** (from `planning`) — stamp `started` to today, **overwriting** any
  tier-3 (`planning`) stamp already there. Still provisional — see next bullet.
- **Flips to `in-progress`** *from `ready` or `planning`* — always stamp `started` to today,
  **overwriting** any tier-2/tier-3 value (a direct `planning`→`in-progress` jump skips the
  `ready` stamp but is just as real a start). This is the real, final signal: once set this
  way it is never overwritten again.
- **Flips to `in-progress`** *from anything else* (e.g. reopened from `done`)
  — leave `started` alone. It already holds the best available first-start date; a later
  resume doesn't reset it.
- **Flips to `done`** — set `completed` to today. This one *does* overwrite — if the project
  was reopened and is completing again, the newer date is the honest one. Then, if `started`
  is *still* `-` at this point (none of tiers 1–3 ever fired — typically a row added
  directly as `done`, retroactively documenting work finished elsewhere), fall back to the
  last resort: set `started` to the same date as `completed`. Finally, compute
  `elapsed (days)` = `completed − started` in whole days (0 if same-day) and stamp it —
  computed at the moment `completed` is set (recomputed if the project re-completes),
  never live-recomputed afterwards.
- **Flips away from `done`** (reopened to `in-progress`/`ready`) — clear `completed` back to
  `-`, and clear `elapsed (days)` back to `-` alongside it; it's no longer true that the
  project is finished, so neither a completion date nor a duration is honest anymore.

A status column edit and its date-column edit are the same logical change — make them in
one pass, not as a follow-up.

If a row's table predates these columns (header has no `started`), the plugin's
SessionStart hook (`hooks/migrate-index-dates.sh`) migrates and git-backfills it on the
next session. If you hit an unmigrated table mid-edit, widen it yourself first: insert
`started` / `completed` / `elapsed (days)` after `status` in the header and separator, and
`-` cells in every row, then apply the stamp.

## Counting tasks

To report progress (e.g. "5/8 done"), count the checkboxes — but skip the `## Status`
legend block that the `tasks.md` template includes (its `- [ ] Not started` / `- [x] Done`
lines are documentation, not real tasks), skip `## Notes` / `## Context` sections, skip
anything inside HTML comments (the template's `## Revisions` section ships a commented-out
example with a `- [ ]` line), and skip fenced code blocks. These are the same exclusions
the deterministic helpers apply (`graph-report.py`, `archive-report.sh`), so counts agree
everywhere. Count only checkboxes under the actual work sections (`## Tasks`,
`## Phase …`, or real `## Revisions` entries).

A quick count from the shell (the shared snippet `todo-list` sort mode, `todo-triage`, and
`todo-infographic` also use):

```bash
# completed/total real tasks — skips ## Status/Notes/Context, HTML comments, and fences
awk '/<!--/{c=1} c{if(/-->/)c=0; next} /^[[:space:]]*(```|~~~)/{f=!f; next} f{next} /^## /{p=($0!~/^## (Status|Notes|Context)([[:space:]]|$)/)} p&&/^[[:space:]]*- \[/{t++} p&&/^[[:space:]]*- \[x\]/{d++} END{print d+0"/"t+0}' tasks.md
```

## Notes

- Audit detection is idempotent and safe to run weekly; nothing changes without confirmation.
- This skill reconciles **state**; it never edits code, plans, or task text.
- `/todo-verify` proves behavior via a verification run; audit mode cross-checks
  bookkeeping against git. Verify is the gate, audit is the bookkeeping check.
- Registry status is not dependency readiness. "What can I start now?" belongs to
  `todo-graph`.
