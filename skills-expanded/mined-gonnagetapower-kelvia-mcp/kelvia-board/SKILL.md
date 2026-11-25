---
name: kelvia-board
description: Keep a Kelvia board in sync with the work actually being done — file tasks, move them as their state changes, log time, and record reasoning in comments. Use whenever the user asks to track, plan, triage, or report on work, and whenever a coding session produces work worth remembering after the session ends.
---

# Working on a Kelvia board

Kelvia is a task board shared by a human and their agents. You have write access
to it. Everything you do is attributed to your agent identity and shows up in the
board's activity feed, where a human can review it and revert supported changes.

That attribution is the point of the product, and it changes how you should
behave: the board is not scratch space. It is a record another person reads.

## Before you write anything

Call `list_boards` and `get_board` first. A board has columns, and their names
are chosen by the user — do not assume "To Do / In Progress / Done". Read
`list_board_columns` and use the column IDs that exist.

If more than one board could be meant, ask which one rather than guessing. Filing
work onto the wrong board is worse than asking.

## Filing work

One task per unit of work a human would want to see separately. Resist both
extremes: a single task called "implement the feature" is useless a week later,
and fifteen tasks for one refactor is noise.

Write the title as the outcome, not the activity — "Search returns archived
boards" rather than "Fix search". Put the reasoning, the reproduction, and the
constraints in the description, where they survive.

When the user describes something ambiguous, file it and say what is unclear in
the description rather than inventing a specification.

## Keeping state honest

Move a task when its state actually changes, not at the end in a batch. If you
start work, move it then. If you finish, move it then. A board that updates only
at the end of a session is a board nobody trusts mid-session.

Use `update_task` to change the column, assignee, priority, or dates.
`reorder_task` positions within a column when order carries meaning.

## Recording what happened

`add_task_comment` for reasoning: what you tried, what you rejected, what a human
should check. Comment when the outcome differed from the plan, not on every step.

`add_task_worklog` for time. Log the time actually spent on that task, once, when
the work is done. Do not invent durations; if you genuinely cannot tell, do not log.

`get_task_activity` shows who changed what, so use it before asking a user to
re-explain history — it is usually already recorded.

## Planning a day

The planner is personal and separate from boards. `create_daily_plan_block`
blocks out time; `list_daily_plan_blocks` reads a day;
`list_overdue_daily_plan_blocks` finds what slipped.

Plan from what the board actually holds, and leave gaps. A day packed wall to wall
is a plan that fails at the first interruption.

## Stages, members, and tags

Stages are Kelvia's sprints. `start_board_stage` and `complete_board_stage` move
a board through them. Completing a stage is a decision about scope, so never do
it on your own initiative — the unfinished tasks in it need a human's call.

Board membership and roles (`update_board_member`, `create_board_invitation`)
change who can see and edit the board. Treat every one of these as a request that
needs explicit confirmation naming the person and the role, not an inference from
context.

Tags are cheap and safe. Reuse existing ones — read `list_board_tags` before
creating a near-duplicate, or the board ends up with three spellings of the same
label.

## Destructive actions

`delete_task`, `delete_board`, `delete_task_comment` and `delete_task_worklog`
remove data. Confirm with the user before calling any of them, even when the
request seems to imply it. Archiving a board (`archive_board`) is reversible and
is almost always the right choice over deleting one.

Never bulk-delete to "clean up" unless the user asked for exactly that, named the
scope, and confirmed it.

## When the connection is not authorized

If a call fails with an authorization error, the user is not connected yet. Tell
them to run `/kelvia:setup` — do not retry in a loop, and do not ask them to paste
a token.
