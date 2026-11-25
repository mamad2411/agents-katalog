---
name: trekoon
description: "Use for Trekoon planning/execution: epics, tasks, subtasks, dependency graphs, status/progress, backlog, agent execution. Prefer for tracked planning/entity management even when unnamed."
---

# Trekoon Skill

Trekoon is source of truth for plans, readiness, owners, blockers, progress, verification, completion. Load only needed refs.

## Modes

- `trekoon plan <goal>`: create execution-ready epic.
- `trekoon brainstorm: <scope>`: design only; create no Trekoon items until user accepts.
- `trekoon code-review: <scope>` or `trekoon code-review`: review current changes/scope only; fix nothing until user asks.
- `trekoon <id>`: orient on epic/task/subtask; report state, blockers, ready work, next.
- `trekoon <id> execute`: execute until epic done, rest blocked with reasons, or real user input required; delegate independent work by default.

Do not stop at analysis while ready work exists or invent non-Trekoon parallel plans. Done means: plan recorded and validated with the user given epic ID + first wave; review findings reported by severity; orient state/blockers/next reported; execution epic `done`, remaining work `blocked` with reasons, or user input required.

## Load

| Situation | Load |
|---|---|
| Any Trekoon request | this file |
| Explicit `brainstorm:` | `reference/brainstorming.md`; after accepted design, `reference/harness-primitives.md` + `reference/planning.md` |
| Explicit `code-review` | `reference/code-review.md` |
| Plan/design tracked work | `reference/harness-primitives.md` + `reference/planning.md` |
| Execute/implement/complete | `reference/harness-primitives.md` + `reference/execution.md` |
| Sync gaps/conflicts/storage | `reference/sync.md` |

`harness-primitives` is required before planning or execution: questions, delegation/runtime, claim, append, finish, review.

## Route Input

Resolve first non-mode arg with `trekoon --toon session --item <id>`; use returned `kind`, `parentEpicId`, payload, readiness, `suggestedNext`. Targeted reads: `epic show <id> --all`, `task show <id> --all`, `subtask show <id>`. Before executing a task, read the full brief with `task show <task-id> --all`.

| Signal | Mode |
|---|---|
| ID only | Orient: `session --epic <epic-id>` or targeted show |
| `status`, `progress`, `analyze`, `review`, `check` | Analyze: `epic waves <id> --summary`, targeted show, session `suggestions` |
| `trekoon brainstorm:` | Brainstorm, then Plan only after accepted design |
| `code-review` | Code review: review-only diff/scope, then ask before fixes |
| `plan`, `break down`, `design`, `architect` | Plan |
| `execute`, `implement`, `do`, `complete`, `start`, `run` | Execute |

## Execution Defaults

Start with `session` (returns `suggestions`); add `--epic <id>` when known. Use `epic waves <id>` for lane shaping and `epic waves <id> --summary` for progress counts. Dispatch lanes with `task brief <task-id> --owner <lane>`. After claiming, read `task show <task-id> --all` before implementation. After each `task done`, inspect `unblocked`, `warning`/`openSubtaskIds`, `nextCandidate`. Delegate independent lanes; parent coordinates deps/comms/synthesis/close. If harness blocks subagents, ask. Non-trivial implementation needs tests + separate review; record evidence.

## Non-Negotiables

- Agents pass `--toon` explicitly; non-TTY stdout without `--json`/`--toon` stays JSON for compatibility.
- Prefer small reads: `session`, `task ready --limit 1`, `epic waves --summary`, `dep list/reverse`, targeted `show`.
- Planning: write plan JSON to gitignored `.trekoon/plans/plan-<datetime>.json` (verbatim values, owner inline), preflight `epic create --from-file <path> --dry-run`, create from that same file, validate with `epic waves <epic-id>`. Fix failures by editing one line in the file, not re-emitting. Never write plan files elsewhere in the project.
- Bulk updates: narrow `--ids`; tasks accept `--append`/`--status`/`--owner`.
- Append progress/verification/blockers with `--append`; rewrite descriptions only to fix plans.
- Claude Code: parallel `Bash` Trekoon batches are read-only except atomic `task claim`/`subtask claim`; serialize `task done`/status changes after reread.
- Preview search/replace before `--apply`. Never edit `.trekoon/trekoon.db`; keep `.trekoon` gitignored.
- Never run `trekoon wipe --yes --toon` unless explicitly requested.
- Branches, commits, merges, pushes, PRs only when asked and harness-allowed.

## Status/Recovery

Valid status moves: `todo→in_progress|blocked`, `in_progress→done|blocked`, `blocked→in_progress|todo`, `done→in_progress`; invalid returns `status_transition_invalid`. `task done` auto-walks tasks from `todo`/`blocked`; subtasks must claim or move through `in_progress` before `done`. Use `blocked` only with appended reason, evidence, unblock condition.

If diagnostics show `recoveryRequired`, stop selection; run `trekoon --toon init` then `trekoon --toon sync status`. If sync is behind/conflicted, resolve before claiming work; load `sync.md`.
