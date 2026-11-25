---
name: session-startup
description: "Obligatory sequence at session start: read AGENTS.md, load phase skills, check memory, run tests and present a plan."
license: MIT
---

# Session startup

> The operational contract lives in `AGENTS.md`. This skill is the procedure.

## Steps (in order)

1. **Read `AGENTS.md`** — it is the entry point. If `## Commands`, `## Structure` or
   `## Do Not Touch` are missing, stop and ask to complete them.
2. **Check the bootstrap state** — if `.atlas/state.json` exists and `status` is `pending`, run
   `.atlas/BOOTSTRAP.md` before anything else.
3. **Resolve the OpenSpec command preference** — read it from `AGENTS.md` (§ Preferences):
   - `user` or `agent`: no question.
   - `ask`: ask once at session start: *"Do I run the OpenSpec commands this session, or do you?"* and
     apply the answer to this session only.

   Combine it with the orchestration question if both are needed. `archive` and `sync` always require
   explicit approval.
4. **Load the phase skills** from the Skill Registry in `AGENTS.md`. Do not load skills from packs
   that are not activated.
5. **Review the previous session** — if persistent memory is configured, retrieve the context. If not,
   inspect the repo state (`git status`, `git log -5`).
6. **Run the tests** with the command declared in `AGENTS.md` (`## Commands`). They must be green
   before writing code.
7. **Present a plan to the user** before touching code.

## Workspace check (two phases)

**Phase 1 — at startup.** Report the current branch, whether the working directory is a worktree and
the active change. Informing creates nothing and asks nothing.

**Phase 2 — before the first write** (a change artifact, code, a QA report or documentation).
Recheck the branch. If it is the base branch, isolate the change with the `using-git-worktrees` skill or
stop and ask the human. A session that starts in read-only mode still repeats this check before it
writes.

## If something is missing

| Missing | Action |
|---|---|
| Test command | Ask; never invent one |
| "Do not touch" rules | Ask before editing |
| Bootstrap pending | Run the ritual first |
| Red tests | Report and do not proceed |
| Writing on the base branch | Isolate or stop; never write on it |

## Role announcement

When switching roles, announce it as `🎩 Ahora soy <rol>` before acting.
