---
name: tasks
description: "Keep every request in the project's TASKS.md so none gets lost: add each one before starting it, tick only what is verified, list what waits on the owner. Use whenever you take on, finish or hand over a request."
---

# Tasks (TASKS.md)

Why: when requests pile up, or the context is compacted, agents forget some of them. One line per request in
the project's TASKS.md is the record that survives.

## The rule

- **Every request gets its own line before you start it.** That includes requests sent mid-turn and each one in
  a message that asks for several things. Add them all first, then work.
- **Before you end a turn, read back the open lines you added.** Say which are still open and why. Never end a
  turn as if everything is done while one of your lines is open.
- **After a compaction or a resume, read TASKS.md first**, before anything else.

## Adding a line

```sh
overvibe tasks add "<what, in one sentence>"            # under To do; prints the id, e.g. T1112-15
overvibe tasks add --waiting "<what the owner must do>"  # under Waiting on the owner
overvibe tasks id                                        # only an id, if you write the line yourself
```

Run them in the project folder or pass `--dir <folder>`. The file is TASKS.md at the git repo's top; `add` makes it with
its three sections when it is missing. The line it writes:

```
- [ ] T1112-15 2026-11-12 <what> · session b2f0a6c3
```

The id is `T<MMDD>-<n>` (the next free one for today, never reused). The session tag is the first 8 characters
of your session id, so the owner can open your session from the Tasks view in Overvibe. `add` finds it for you:
Claude Code's `$CLAUDE_CODE_SESSION_ID`, Codex's `$CODEX_THREAD_ID`, or Overvibe's record for `$OVERVIBE_SESSION`.
Outside those, pass `--session <id8>` or leave the tag off. Working on a line someone else added? Add your own
tag after theirs (`· session <theirs> · session <yours>`).

Put under **Waiting on the owner** only what the owner alone can do: a decision, a login, a payment, approving a
deploy. Everything you can do yourself goes under **To do**.

## While you work

- The id goes in branch names and commit subjects: `feat/T1112-15-tasks-skill`, `Tasks skill and CLI [T1112-15]`.
- A follow-up you promise, or a bug you find and will not fix now, is a request too: give it a line.
- Never delete an open line you did not finish. Say on it what is left instead.

## Ticking

Tick a line only when the result is verified: a test that passes, a page that answers, a screenshot. Written
code is not done. A ticked line says the commit and how it was checked, and moves under `## Done`, below a
heading for the day (add the heading if today has none):

```
## Done

### 2026-11-12
- [x] T1112-15 2026-11-12 <what> · <commit> · checked: bun test, live run on a scratch repo · session b2f0a6c3
```

Commit the tick with the work when it is already verified, otherwise in one follow-up commit after the check.

## Before you end the turn

Run `overvibe tasks check`. It lists ticked lines outside Done, lines without an id, an id used twice, ticks that
do not say how they were checked, and ids already in commits on main whose line is still open. Fix what it lists
for your lines.

## The file

```
# TASKS

## Waiting on the owner
- [ ] T1112-3 2026-11-12 Approve the price change on the pricing page · session 1a2b3c4d

## To do
- [ ] T1112-2 2026-11-12 Fix the login button on mobile · session 1a2b3c4d

## Done

### 2026-11-12
- [x] T1112-1 2026-11-12 Add the export button · 9f8e7d6 · checked: bun test, clicked it on the local page · session 1a2b3c4d
```

New lines go first in their section. A repo's deck.json can name another file (`"tasks": "docs/TASKS.md"`); the
CLI and the Tasks view both follow it.
