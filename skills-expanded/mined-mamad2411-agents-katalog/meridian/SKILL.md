---
name: meridian:status
description: Use when the operator asks for the Meridian board state of the current project - lists the top tasks per status and surfaces interrupted work. Invoked as `/meridian:status` or `meridian:status`.
---

# Meridian Status

Reports the current project's board: the top tasks in each status, any
dependency inconsistency, and any work that was left running when a previous
session ended. Invoked as `meridian:status`.

This skill is **read-only**. It issues `GET` requests and nothing else. It never
creates, updates or deletes a task, and it never edits `.meridian/` by hand.
Field names, statuses and priorities follow `schema.md`; if anything
here disagrees with that file, that file wins.

## 0. Resolve the shared references

`preamble.md`, `pipeline.md`, `stages.md` and `schema.md` are shared by all four
Meridian skills and live in the plugin's own `references/` directory — **not** inside
this skill's own folder. Wherever this file names one of them, resolve it by
trying these two paths in order and using the first that exists:

1. `${CLAUDE_PLUGIN_ROOT}/references/<file>.md`
2. `../../references/<file>.md`, relative to the `Base directory for this
   skill: <absolute path>` line the harness states at invocation — use this
   when the first path does not exist, or when `${CLAUDE_PLUGIN_ROOT}` arrives
   unexpanded, as that literal text.

Both are given because only one of them is directly observed: the base
directory line appears on every invocation, while the expansion of
`${CLAUDE_PLUGIN_ROOT}` inside skill prose is unverified either way. Test which
one exists by READING it — `Read` the first candidate, and if that read fails,
read the second — then use the path that worked everywhere this file asks for
one. Do not probe with a shell command. A headless dispatch runs under a
permission allowlist that matches a command by its prefix, so `test -f`, and
above all the loop an agent naturally writes to try both candidates at once, is
refused before it runs; a failed `Read` is the same test and needs no
permission. The plugin's permission hook allows reading these files.

Never read a bare `references/<file>.md`. Relative to this skill's own folder
that path does not exist, and the read fails.

## 1. Perform the shared preamble

Follow `preamble.md` in order, and stop where it says stop. It
resolves `$BASE`, resolves the project to the current working directory (never a
parent), and gets the server running. Do not repeat or shortcut any of its
steps here.

`$BASE` does not survive between bash calls: shell state is not shared across
Bash tool invocations, only the working directory is. Every block below sets
`BASE` again on its own first line, and so must every block you write. A block
that inherits nothing runs with `BASE` empty and requests a relative URL.

If the operator declines registration, stop — there is no board to report.

If the server cannot be started, the preamble's read-only fallback applies:
read `./.meridian/tasks.jsonl` directly. It is one JSON object per line, in file
order, so you must apply the ordering of section 2 yourself in that case (specifically:
sort by `priority` then oldest `created_at`, or for `done` sort by `completed_at` descending,
and take **AT MOST 5 tasks** per status), and say that you are reporting from the file
because the server is down.

## 2. Fetch the board — once

```bash
BASE="${MERIDIAN_URL:-http://localhost:3333}"
curl -sS -G "$BASE/api/status" \
  --data-urlencode "project=<absolute path of the current directory>" -d 'limit=5'
```

One call. It answers both jobs, because `limit` makes the server return a
`summary` computed over the **whole** board alongside the capped task list.

Do not also fetch the board unlimited. Sections 4 and 5 need completeness, not
the full task list — and the whole list is the expensive thing: a project with
sixty tasks is a six-figure payload fetched to answer two small questions. The
server holds the list already and answers them there.

**`tasks` is the display page.** The server ranks each status and returns the
top five: the eight unfinished statuses by priority — `critical` before `high`
before `medium` before `low`, an absent priority read as `medium` — then by
oldest `created_at`. **`done` is ranked differently**, by `completed_at`
descending, so you get the five most recently finished, which is the useful
five. Take the table from this, in this order. Do not re-sort it and do not
rebuild it from `tasks.jsonl`: the ordering and the `medium` default are the
server's, and reimplementing them here is how the two drift apart. (Reading the
file is the section 1 fallback for a server that will not start, and only then.)

**`summary` is the analysis set**, over every task, not just the page:

- `summary.counts` — how many tasks each status really holds. Use it for the
  totals in section 3; a status showing five rows may hold thirty.
- `summary.interrupted` — every task with status `in_progress` **or**
  `running: true`, with both flags on each entry. This is section 5's input.
- `summary.unblockable` — every `blocked` task whose `blockedBy` ids have all
  reached `done`. This is section 4's input. A `blocked` task with an empty
  `blockedBy` is deliberately not listed: it was blocked by an iteration cap or
  a failure, and only a human clears those.

The response shape is `{ "projects": [ ... ], "errors": [ ... ] }`. With
`project=` set, `projects` holds at most one entry. If `projects` is empty, this
directory is not in the workspace registry — say so rather than reporting an
empty board. If `errors` is non-empty, show it: a malformed `tasks.jsonl` or a
missing project path is reported there, and a silent empty board would otherwise
look like a clean one.

## 3. Show the board

**Findings only, throughout this skill.** Every check below runs every time,
but a check that comes back clean produces no output. Silence after the table
means checked-and-clean, and the operator learns to read it that way; a report
padded with healthy checks buries the one line that matters.

Print one compact table grouped by status, in pipeline order:

`backlog`, `spec_review`, `ready_todo`, `in_progress`, `code_review`, `qa_review`,
`blocked`, `done`, `nope`.

One row per task: `id`, `title`, `priority`, and `running` when it is `true`.
Skip a status with no tasks rather than printing an empty group.

Each group shows at most five tasks. Take the per-status totals from
`summary.counts` and say when a group is truncated — `blocked (7, showing 5)`
— so the operator can tell a five-task status from a fifty-task one.

## 4. Consistency line

Report `summary.unblockable` — the server evaluates it over the whole board, so
a dependency that the five-per-status page happens not to show is still counted
correctly.

A `blocked` task that appears in the page but not in `summary.unblockable` is
still blocked for a reason. Two of those reasons deserve a separate line when
you can see them in the page: an **empty** `blockedBy` (blocked by an iteration
cap or a specialist failure — only a human clears it; show its
`justification`), and a `blockedBy` id that matches no task on the board (a
dangling dependency can never reach `done`, so that task is stuck permanently).

When there is nothing to report, report nothing — no "no blocked task has all
its dependencies done", no "all running flags are consistent". A finding earns
a line; health does not. The operator asked for the board, not for a checklist
of everything that is not wrong with it.

Do not unblock anything. Moving those tasks back to `backlog` is the unblocking
sweep in `pipeline.md`, which runs inside `work`; this skill only
reports.

## 5. Interrupted tasks

Report `summary.interrupted`. The server computes it as the union of two
conditions checked independently — `status == "in_progress"`, and
`running == true` — because they are not the same set: `running: true` is set
around every specialist dispatch, so during a live run it legitimately appears
on tasks in `backlog`, `spec_review`, `code_review` and `qa_review` as well.
Each entry carries both flags so you can say which condition caught it.

Why both flags mean abandoned work: this skill runs in a **fresh session**. No
agent dispatched by a previous session is still alive — when that session
ended, its subagents ended with it. So a task that says an agent is working it,
or that sits in the status the developer occupies while working, is describing
work that stopped mid-flight. Neither flag can be true and honest at the moment
this skill reads the board.

For each interrupted task report `id`, `title`, `status`, `running`, the
open round's `last_review_findings` if it has any, and its `resume_context`
if present — that note was left at the moment of interruption, by the
stopping session or by the plugin's stop hook, precisely to be read now.

## 6. Offer to resume

If section 5 found nothing, stop — silently, per section 3. An empty
interrupted set is health, not a finding.

If it found anything, **ask the operator** whether to resume one, and which.
Ask; do not pick one and start it. If they decline, stop — leave the task
exactly as it is, including its `running` flag. Clearing a stale `running` is a
write, and this skill does not write.

On a yes, hand the chosen id to `meridian:work`, which owns every transition
from here. `work` re-enters the task at the stage its status indicates and is
the only thing that writes task state.

When the chosen task's status is `in_progress`, say so explicitly in the
hand-off: an interrupted `in_progress` task may have left partial work in the
working tree, so `work` owes its `meridian:developer` dispatch the **resumption
briefing** defined in `meridian:work`. Do not restate the briefing's contents
here — `work` assembles dispatch payloads and holds those rules; the status is
the fact you are handing over.

A task interrupted in any other status needs no briefing. Those stages produce
a spec or a verdict, not a working tree.
