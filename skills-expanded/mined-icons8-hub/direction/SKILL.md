---
name: direction
description: You run a direction — a big task you cut into slices yourself. Use when the task says "direction <slug>", after context compaction or in a new direction session (resume first), when you take the next slice, make a decision the further work depends on, or the direction is finished.
---

# Direction: the backlog is your memory

A direction is one big task run by one long session. You cut it into slices and pick the next one yourself: bring the
owner forks, not "which slice next?". The backlog lives in the hub, not in the project repo: `hub direction <slug>
<backlog command>` (`--help` — the list) — don't edit its files by hand.

**After context compaction or in a new session — first `hub direction resume <slug>`** and trust it more than the
compaction summary. Its cleanup list at the end is yours, before the next slice: fill in or replace empty decisions,
merge duplicates, close stale tasks.

**One repo.** `hub direction where <slug>` — the direction's repo. Your folder is not it — stop and write to the hub
(`hub send hub "…"`): don't work in another copy.

## Write as you go, not at the end

```
hub direction <slug> task create "Slice N: <what>" --ac "<checkable criterion>"   # a slice — a task with AC
hub direction <slug> task edit N --status "In Progress"                           # taken
hub direction <slug> task edit N --append-notes "<what's done, what's checked>"   # slice progress
hub direction <slug> task edit N --check-ac 1                                     # criterion met
hub direction <slug> task edit N --status Done                                    # slice closed
hub task run <name> "<brief>" --work … --board TASK-N                          # executor on a card: who works on it
hub direction decide <slug> "<title>" --decision "…" --context "…" --consequences "…"
hub direction <slug> doc create "Goal" / doc update …                             # goal and invariants
hub direction board <slug>                                                        # board for the owner: links
```

A decision the further work depends on (an invariant, a rejected option, a contract's shape) — `decide` at once (not
`decision create`: it writes an empty template). Goal and invariants — in documents, keep them fresh.

**The board is the cards, not a plan doc**: "update the board" is `task edit`. Edit the cards in the same turn as what
changes them: the owner's word on a new order or a pause, an executor's hand-in, a wait that is over (in every card
that says "waits for" it). Statuses are the truth: done — Done, taken — In Progress, moved to another direction —
archive with a note where. A one-off question changes no card. "the board lags" in `task list` — events since the last
card edit: check the cards against them.

## Say what you wait for

"Free" in the list says nothing. Ending a turn with open tasks left on the board — name what you wait for in one line:
`hub waiting "<whom or what> — task-N"` (e.g. "review from a colleague — task-2"). It shows in the list instead of
"free", with since when. Got it and working on — `hub waiting --clear` or a new line. Waiting for the owner's
decision — ask via the form, never wait silently.

## The backlog is not a report

To the owner — as always: the turn result, questions as options, in the owner's language. A slice result — 3–5 lines:
what's closed, how checked, a question to them; details stay in the backlog. An executor's result reaches you, not the
owner: a result for the owner that came to you (a summary, a report, a file) — hand it over yourself in this turn, the
content or `hub send-file <full path>` (a long text — into a file first); never "see above" or "X sent it to you". In a
repo with its own tracker (Jira, the project's `backlog/`) the project's tasks and decisions go where the project
says; the direction backlog is only your working memory.

## Tidy up yourself

Ready → Done; stale → `task archive`; duplicates — merge. The big task is finished (no open tasks) → result to the owner
and a form question "finish the direction?". Only the owner finishes a direction: the archive (`hub direction archive
<slug>`) — after their yes, not on your own.
