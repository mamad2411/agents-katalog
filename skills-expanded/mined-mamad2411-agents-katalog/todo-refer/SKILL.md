---
name: todo-refer
description: >-
  Use when the user invokes /todo-refer, says "refer to project X", "pull in the context
  for X", "give me the plan for X to review against", or wants a hub project's plan/tasks
  loaded before another command — and equally when they say "where was I", "pick up where
  we left off", "continue the migration project", "what happened last session", "what's
  the state of X", or start a fresh session on a project with prior work. Also handles
  "what happened in R4"-style revision history questions. Replaces the former
  /todo-resume, which is now this skill's `resume` mode — treat that spelling as an
  invocation of this skill. Read-only, active-or-archived, and cross-repo.
---

# Project Refer Skill

Load a hub project's context into the current session. Read-only and cross-repo: always
reach the hub by absolute path, and never edit `index.md`, `archive.md`, `tasks.md`,
`plan.md`, or repo code. Acting on what you load is the follow-on command's job.

Three modes, differing only in how far you dig and what the digest emphasizes:

| Mode | Question it answers | Extra work |
|---|---|---|
| **grounding** (default) | "what is this project about" | none — plan + current task state |
| **resume** | "what happened, what's in flight, what's next" | hub trail + repo/git state + a next-command recommendation |
| **revision** (`R<n>`) | "what happened in R4" | one anchored journal entry; skips everything else |

Run inline on at least the **balanced** tier from
[`../todo-llm-routing/SKILL.md`](../todo-llm-routing/SKILL.md). Resume mode is judgment
work — assembling the picture means deciding what matters — so keep it on the session
model rather than delegating it.

## Hub location and registry contract

The hub root is `$TODO_HUB` (default `~/todo`) — an environment variable pointing at your
hub folder. Resolve **every** hub path against this absolute root regardless of the
current working directory; this skill is often invoked from another repo, so never assume
cwd is the hub.

- `index.md` contains active projects and is the default hot path.
- `archive.md` contains completed projects and is read only for an explicit archive view
  or when an exact short-name is absent from `index.md`.

Never use a same-named `index.md` from the current code repo.

## Invocation

```text
/todo-refer service-auth              grounding digest
/todo-refer service-auth resume       where the work stopped + next command
/todo-refer service-auth R4           one revision's history
/todo-refer                           ask which project
/todo-refer resume                    resume the most recently touched in-progress project
```

Plain language selects the mode: "pull in the context for X" and "give me the plan for X"
mean grounding; "where did we leave the token rotation work", "continue where we stopped",
"what's the state of X" mean resume; "what happened in R4" means revision.

## Step 1 — Resolve the project

1. Run bounded exact-name checks against both registry tables; do not load either file
   into model context.
2. If both match, stop and report registry corruption.
3. Otherwise select `index.md` first; select `archive.md` only on an active miss. Say so
   when the project turns out to be archived.
4. If exact lookup fails, fuzzy-match names from both files and ask for confirmation.
5. With no name in grounding mode, list active names from `index.md` only and ask which
   project.
6. With no name in resume mode, pick the active `in-progress` project whose files changed
   most recently (`ls -t` the project folders' `tasks.md`), say which one you picked, and
   offer the others. No `in-progress` projects at all → show the index the way
   `/todo-list` does and ask.

Record the owning registry, section, path, repo, status, and related names. Resolve the
project folder as `$TODO_HUB/<path>`.

For an archived row, always run Step 2's bounded context helper—even on the
revision-only fast path. Any `REVISION` row means the registry is stale. Keep this
read-only, flag the mismatch, and direct the user to
`/todo-state <short-name> in-progress`.

## Step 2 — Read current context economically

For a revision-only question such as "what happened in R4?", take the fast path: read
only the `## Goal` paragraph from `plan.md`, skip current task counts and related-project
expansion, then jump to Step 3. Every other mode uses the full path below.

Read `plan.md` because it is the grounding — in full for grounding mode; in resume mode
the `## Goal` paragraph and whether a `## Verification` block exists are usually enough,
with a full read only when the file is small. Extract current task state with the bundled
helper rather than loading `tasks.md`:

```bash
bash <todo-archive-skill-dir>/scripts/archive-report.sh context \
  "$TODO_HUB" "<project-path>"
```

`TASK` and `REVISION` rows are capped at 20 each. `SUMMARY` always carries complete
done / total / open-task / open-revision counts. The parser strips HTML comments,
ignores fenced examples and non-task Notes/Context sections, and reads only visible
current state.

Read all of `tasks.md` only when it is below about 15 kilobytes or the follow-on command
explicitly needs completed-task detail.

**Resume mode adds the rest of the hub trail** — extract, don't ingest whole files:

1. `artifacts/blockers.md` — every unresolved blocker, one line each.
2. `artifacts/journal.md` — the **last dated section only** (tail the file); it records
   the most recent closed work. If the user also named a revision, use Step 3's exact
   anchored lookup instead of the tail.
3. `artifacts/README.md` — the newest 2–3 rows (most recent outputs).

## Step 3 — Resolve requested revision history

When the user names a revision ID or explicitly asks about revision history, read only
that entry. Prefer the bundled read-only helper when `todo-archive` is installed:

```bash
bash <todo-archive-skill-dir>/scripts/archive-report.sh lookup \
  "$TODO_HUB" "<project-path>" "R4"
```

The helper returns a live or not-yet-tombstoned entry directly from `tasks.md`. For a
tombstone it resolves the stable `<a id="revision-r4"></a>` journal anchor and stops at
the next entry. It also supports legacy exact `## R4` / `### R4` headings, with a strict
boundary so `R1` never matches `R10`.

If the helper is unavailable:

1. Read the named revision block in `tasks.md`.
2. Follow its `artifacts/journal.md#revision-r<n>` link.
3. Read from that exact anchor until the next revision anchor or heading.
4. For a legacy unlinked pointer, search `journal.md` for exactly one case-insensitive
   `^#{2,3} R<n>(space-or-end)` heading and read only that block.

Zero or multiple journal matches are a broken tombstone. Report the ambiguity and do not
guess from nearby dated or aggregate sections.

## Step 4 — Load one bounded graph neighborhood

Skip this step on the revision-only fast path. Otherwise run:

```bash
python3 <todo-graph-skill-dir>/scripts/graph-report.py context \
  "$TODO_HUB" "<short-name>"
```

Use its exact one-hop `depends-on`, derived blocker, `related-to`, `supersedes`, and
legacy-context rows. Read only each named neighbor's `## Goal` paragraph when the
follow-on request needs that context; never load neighboring tasks or journals.

Record unsatisfied hard prerequisites as graph blockers. Canonical `related-to`,
`supersedes`, and legacy registry hints are context only. In resume mode, an in-progress
project whose dependency regressed is **at risk**: say so, prioritize
`/todo-graph why <short-name>`, and do not recommend more execution until the graph is
honest.

Graph issues are not stale names to skip: surface them and point at `/todo-graph audit`.
If the helper is unavailable, fall back to the owning registry row's legacy `related`
names as non-blocking context only. Never infer a dependency from the fallback.

## Step 5 — Gather the repo trail (resume mode only)

If the owning registry row names a target repo that exists locally:

```bash
git -C <repo> worktree list                          # is <repo>-wt/<short-name> still there?
git -C <repo> branch --list 'todo/<short-name>' 'feat/*'
git -C <repo> log origin/<base>..todo/<short-name> --oneline | head -5   # unshipped commits
git -C <repo>-wt/<short-name> status --short 2>/dev/null | head -10      # uncommitted work
gh pr list --repo <owner>/<repo> --head todo/<short-name> --state all --limit 3   # PR state (if gh works here)
```

Take what succeeds and skip what doesn't (no repo, no gh auth) — note gaps rather than
erroring. The point is to know whether work is **uncommitted, committed-but-unshipped,
in an open PR, or merged**.

## Step 6 — Emit the digest

**Grounding mode** — about 5–8 lines plus related projects:

```text
Loaded context: service-auth ($TODO_HUB/projects/work/service-auth)
Registry: active
Goal: <one line>
Status: in-progress
Open tasks: <first 3–5, then count>
Done: 12/20 tasks
Depends on: token-foundation — <goal> (done, archived)
Context: token-rotation — <goal> (in-progress)
```

**Revision mode** — the exact heading plus a compact Expected / Actual / Fix digest from
the extracted entry, together with the one-line goal and registry state. That is the
whole response; do not dump unrelated journal history.

**Resume mode** — one compact briefing, newest signal first:

```
## ⏪ queue-migration — where you left off

Goal: move order events from Redis pub/sub to RabbitMQ quorum queues
Status: in-progress · ▓▓▓▓▓▓░░░░ 12/20 tasks · 1 open revision

Last recorded work: R3 closed 2026-07-08 — consumer retry backoff (journal.md)
In flight:
- 🔄 worktree <repo>-wt/queue-migration exists · branch todo/queue-migration
- 🔄 3 commits unshipped (ahead of origin/main) · no open PR
- ⚠️ uncommitted changes in src/consumers/ (2 files)
Blockers:
- ❌ staging RabbitMQ creds missing (blockers.md, 2026-07-05)
Next open task: 4.2 dead-letter exchange for poison messages

▶ Next: /todo-execute queue-migration   (or /todo-push from the worktree to ship the 3 commits first)
```

The `▶ Next` line is resume mode's deliverable — pick ONE primary recommendation from the
evidence, with at most one alternative:

| Evidence | Recommend |
|---|---|
| Open tasks, no unshipped work | `/todo-execute <name>` |
| All tasks done, `## Verification` block in plan.md | `/todo-verify <name>` |
| Open revisions | `/todo-revise <name>` |
| Committed-but-unshipped worktree commits | `/todo-push` (from the worktree) |
| Only blockers remain | name the blocker — no command unblocks a missing credential |
| Unsatisfied project dependency | `/todo-graph why <name>` |

Grounding and revision modes end with one next-command nudge instead; do not run that
command or edit hub files.

## Notes

- Read-only and idempotent in every mode — safe to run at the start of any session.
- Missing files are reported, not scaffolded.
- Artifact bodies remain cold by default. A named revision lookup is the deliberate
  exception; arbitrary artifact requests list filenames unless the user asks for content.
- Uncommitted changes in a worktree are the highest-priority resume signal: surface them
  first, they're the easiest thing to lose.
- If hub state and repo state disagree (tasks ticked but no commits anywhere, or merged
  PRs for unticked tasks), say so in the digest and point at `/todo-state audit` — don't
  reconcile here.
- To change state use `todo-state`; to execute use `todo-execute`.
