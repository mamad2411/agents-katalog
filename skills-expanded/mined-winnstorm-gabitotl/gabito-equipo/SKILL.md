---
name: gabito-equipo
description: Coordinates with other people on the same project using who, session, work and worktree commands. Advisory only: warn, never block. Trigger: starting a task, touching an area others may be editing, or when asked who is working on what.
license: Apache-2.0
metadata:
  author: gabitotl
  version: "1.0"
---

# Gabito team: know who else is here, advisory only

Several people (and their agents) can work on one project. GabitoTL tells you what it knows;
Git decides real conflicts. You warn the user. You never block, refuse or reorganize someone's work.

## Identity

Your identity comes from the OS user (override with `GABITOTL_USER` or `--user`). Never ask who the user is
and never invent an id. Per-person files live under `.gabitotl/local/users/<id>/` and stay out of Git.

## Before starting

1. Run `gabitotl who`. It lists active sessions, other worktrees and pushed work, plus shared memory.
   Add `--json` for scripts; `--no-memory` or `--no-worktrees` to skip a source.
2. Before touching an area, run `gabitotl work overlap --areas a,b --files x,y`
   (modules or paths you are about to change). Add `--task ID` when you have one.
3. If the command fails because there is no `.gabitotl/`, say so and continue; the check is advisory.

## Register your work

- `gabitotl session start --task ID --branch B --areas a,b --runtime NAME` when you begin.
  It records presence; hooks usually do this, so check `gabitotl who` before repeating it.
- `gabitotl session touch` on long sessions to refresh `last_seen`.
- `gabitotl session end` when you finish. Presence also expires when the anchor process ends.
- `gabitotl work start --task ID --areas a,b --files x,y --branch B --objective "..."` declares the task.
- `gabitotl work update --task ID --status in-progress|blocked|paused|done --next "..."` keeps it current.
  Mark `done` when the work is delivered.
- `gabitotl work status` shows the declared work.

Declare areas honestly and narrowly. Wide areas create noise for everyone.

## One worktree per person and task

- Create it: `gabitotl worktree add --task ID` (branch defaults to `feature/<task>`; use `--branch` to override).
- List with `gabitotl worktree list`; remove a finished one with `gabitotl worktree remove <name|path>`.
- Never work two tasks in one worktree and never commit on the base branch.
- Back up shared files before modifying them: `gabitotl backup create --task ID <file>...`.

## When there is overlap

Overlap is information, not a verdict. Raise an OJO (the Heads-up block when the persona speaks English) with: who, which area or file, which branch, and what
you suggest. Keep it to two or three lines:

> OJO (Heads-up in English): ana is working on `internal/auth` (branch `feature/mfa`, active 10 min ago) and you are about to
> change `internal/auth/session.go`. Suggest syncing with her first, or I keep to `internal/api`.

Then:

- Ask one short question only if proceeding could lose someone's work or is hard to revert.
- Otherwise continue on the part that does not collide, or on your own worktree, and say what you chose.
- Never edit another person's worktree, branch, session file or declared work.
- Never tell the user to wait. They decide.

## Handoffs

- Save decisions that affect others to memory (`gabito-memoria`) with a stable `topic_key`.
- Put the next step in `work update --next`, so whoever resumes knows where to start.
- Deliver through `gabito-entrega`: small, task-scoped PRs avoid collisions.

## Rules

- Advisory only. Git resolves conflicts; you describe them.
- Do not include personal data beyond user ids, branches and file paths.
- No secrets in session or work files.
- No AI attribution in anything shared with the team.
