---
name: roadmap
description: Use when planning a product's roadmap or milestones, asking which task to take next, what the priority is or what can run in parallel, asking what is left to close a milestone, putting a task off to Later, re-planning after a milestone closes, triaging new issues that have no label or no milestone, or when an agent needs the project's roadmap as context.
---

# Planning on GitHub

The plan lives in GitHub: milestones, "blocked by" links and sub-issues.
Scripts read it at the moment of the question, so the answer cannot be out of
date. Nothing is kept in the repository. Everything here needs `gh`
authenticated against a GitHub remote; `board.sh` also needs the `project`
scope on the token, as *The board* says. Where `gh` does not work, say so
and stop.

| Moment | What must happen | Read first |
| --- | --- | --- |
| "What can I take now", "what is the priority", "what can run in parallel" | `next.sh`, then the overlap check; at most three lanes, none overlapping: lane 1 the main path to the goal, then the top bug that can run; one task, or a table per lane | *The lanes* below |
| "What is needed to close M1" | `roadmap.sh M1`; its open tasks in dependency order, what is in progress, what is blocked and by what | *The roadmap* below |
| "What can I take from Later" | `roadmap.sh Later`; offer its free tasks | *The roadmap* below |
| The person decides, in the conversation, to put a task off | `plan.sh later <n>`; a refusal names the issues that wait on it | *Putting a task off* below |
| An agent needs the roadmap as context | `roadmap.sh` | *The roadmap* below |
| Start a roadmap | read `docs/`, propose, one approval, then write | `planning.md` |
| A milestone has no open issues left, or the person asks to re-plan | the same, from that milestone | `planning.md`, *Re-planning* |
| Open issues have no label or no milestone, or the person asks to triage | duplicates first; a verdict for each with no entry in its `status:` line, then its label and milestone, or its close; one approval, then write | `triage.md` |
| The person wants the board | `board.sh`; pass on the two settings it prints | *The board* below |

A file in the last column sits next to this one, in this skill's base
directory. Read all of it before the first step of that moment.

## How the plan lives in GitHub

- **A stage is a milestone**, titled `M<n> · <name>`. Its description is a
  short goal and a `Done when` list: the outcomes that someone can check, as
  in a demo, each with the issues that it needs, as `(#21, #22)`.
  The order comes from the number after `M`; other titles come after; `Later`
  is last and holds what is wanted but not planned. One number belongs to one
  open milestone: `plan.sh create` and `rename` refuse a second `M1`, and an
  `m1` or `M01` too. When two open titles start with `M1` and then no digit
  anyway, as two made by hand, the scripts list both: give a whole title. A
  whole title, in any case, wins over `M1`.
- **The current milestones** have the line `Current.` in their description.
  `plan.sh current` and `plan.sh not-current` set and remove it. When no
  milestone has it, the first open one is current. `Later` is never current.
- **A dependency** is GitHub's "blocked by" link. A task too large for one PR
  is a parent issue with sub-issues. A sub-issue without a milestone takes its
  parent's, and it waits on its parent's blockers too. A parent with open
  sub-issues is never offered: its sub-issues are.
- **Busy** means an assignee, the label `in progress`, a linked branch, or an
  open PR that closes the issue. Your own assignee alone is not busy: it says
  who may take the issue, not that its work runs. **Free** means open, not
  busy, with no open blocker of its own or of its parent, no open sub-issue,
  and not in `Later` — unless an open issue outside `Later` waits on it,
  through any chain: then it is needed.
- **The goal and the tracks.** The goal is the nearest milestone: the first
  current one. The main path is the free issues of the path to it: the open
  issues, with any label, that its `Done when` names, and every issue they
  wait on, wherever it is. When the `Done when` names no issue, the path is
  the issues of the milestone without the bug label, and what they wait on.
  Bugs are the other free issues with the bug label. Secondary is every other
  free issue, the rest of the goal milestone too. A track ranks by milestone
  order — a blocker of an `M1` task ranks with `M1` — then by how many issues
  wait on it, then oldest first.
- An issue goes into a milestone with `gh issue edit <n> --milestone '<title>'`,
  out of it with `--remove-milestone`, and into `Later` with `plan.sh later`.

The developers are equal: a free task goes to whoever takes it first. The
answer is for the account that `gh` is logged in as. Its own work in progress
shows as context; other people's busy tasks are never offered.

## Scripts

The scripts are in `scripts/`, next to this file. Run each one as
`bash <dir>/scripts/<name>.sh`, where `<dir>` is this skill's base directory.
They need only `bash`, `gh` and `awk`. `GH_REPO=<owner/repo>` points them at
another repository than the checkout's. `plan.sh` and `board.sh` write; with
`DRY_RUN=1` they print their write commands and run none.

A script can stop with an error, from `gh` or from its own usage check. Then
its step is not done: report the error and stop at that step. Do not do the
step by hand with `gh`: that skips the checks the script makes. A line that
starts with `refused:` is not an error: it says why `plan.sh` wrote nothing.
Tell the person, and change the plan, not the check.

## The lanes

The three questions get one answer: the path from now to the goal, with the
top bug beside it, in at most three lanes.

```bash
bash <dir>/scripts/next.sh bug
```

The argument is the repository's name for the bug label in `gh label list`.
The script prints the current milestones, the goal with its `Done when`,
then the sections `== main path`, `== held on the main path`, `== bugs` and
`== secondary` — each track's top 5, ranked, as `#21 <title> (<milestone>),
unblocks 2`, and each held task with what holds it — then `== in progress`,
and last the path of the overlap file. When nothing on the main path of the
first current milestone is free, the goal is the next milestone that is not
`Later`, and a `note:` line says so; with no such milestone, the goal stays.
A `note:` line also says when a milestone has no `Done when` that names an
issue, or one that names only closed ones: say so, and offer to re-plan that
milestone (`planning.md`, *Re-planning*). With no milestone, the main path
is the free tasks that the current goal of the project's `PRODUCT.md` needs,
by your reading, and the answer says that the pick is yours.

Then run the overlap check on the file that `next.sh` printed. In Claude
Code, send one `Agent` call with `model: "haiku"` and this prompt, whatever
the file's size — the reading it saves is in the code:

```
Read <dir>/lanes.md and do what it says.
File: <the path next.sh printed>
Tree: <the repository's top directory>
```

In Codex, follow `lanes.md` yourself and write its return as your notes.

Then put the free tasks into at most three lanes of new work. Work in
progress, your own included, is no lane. Take the tasks one at a time, each
track in its rank: the main path until one task starts lane 1, then the bugs
until one takes a lane, then the rest of the main path, the rest of the bugs,
and secondary. For each task, the first of these that holds decides:

1. It overlaps with work in progress, or the overlap check marks it
   `ready: no`: it waits.
2. It overlaps with the tasks of two or more lanes: it waits.
3. It overlaps with the tasks of one lane: it goes into that lane, after
   them. A task off the main path waits instead of going into lane 1.
4. It is on the main path, and lane 1 has no task yet: it starts lane 1.
5. Lane 2 or lane 3 is not open yet: it opens the first of them that is not
   open.
6. It is on the main path: it goes into lane 1, after its tasks. Any other
   task waits.

Say what holds each task that waits. So the goal starts lane 1, the top bug
that can run takes the next lane, and a main-path task that can run beside
them takes the last one before the other bugs, tests and improvements do.
With no main-path task to start, lane 1 stays empty.

## One task

For "what can I take now", give the first task of lane 1, else of lane 2:
its number, title, a few words on what it changes, its milestone, and why it
is first, as "M1 · First demo needs it for 'a new user signs up', and 2
issues wait on it". Then name each other lane in one line: its first task
with its title, and its area. When the person takes a task, the
`craft:github` skill's take-in starts with its bare number, as `#21`: it
checks the task, assigns it and marks it `in progress`.

## Parallel work

For the priority and for parallel work, answer with one table per lane: each
task with its title, a few words on what it changes, its area and its files.
After lane 1's tasks, also when lane 1 has none, list the held tasks of the
main path, with what holds each; they are not offered. Then each overlap in
one line, with the file and the function, and each task that waits. The
first task of each lane starts through take-in, in its own worktree. The
next task of a lane starts after it: when it is closed, the person asks
again, as the lanes change with the work in progress. The file holds every main-path task, but only the top 5 of bugs
and of secondary: when all five overlap, say so.

## The roadmap

```bash
bash <dir>/scripts/roadmap.sh
bash <dir>/scripts/roadmap.sh M1
```

With no argument, it prints each open milestone in order: its progress
(`current, 22 of 54 closed`, then `, due 2026-12-01` when it has a due date),
its description, and its open issues in dependency order, each with its state —
`free`, `blocked by #21`, `open sub-issues: 2`, or what makes it busy. The
progress counts the milestone's issues, not its pull requests; a milestone
closed while the script runs shows `not counted`. `Later` shows titles only.
Issues with no milestone come last, as a count and a list of their numbers and
titles: they wait for triage (`triage.md`). With a milestone — `M1`, `Later` or
a whole title — it prints that milestone alone, with its states, and with the
open issues it waits on in other milestones, each marked with where it is.

## Putting a task off

When the person and the agent agree, in the conversation, that a task can
wait, it goes into `Later`. Move it only after the person says so.

```bash
bash <dir>/scripts/plan.sh later 21
```

It opens the `Later` milestone again when it is closed, and makes it when there
is none. A task in `Later` that an issue outside `Later` waits on is still
offered, so the move would not put it off: the script refuses when an open
issue outside `Later` waits on the task, through any chain — a blocked issue,
or a parent that waits on its sub-issue — and names them with their titles. A
sub-issue with no milestone of its own goes into `Later` with its parent, so an
issue that waits on it counts too, and `plan.sh sub` refuses the same for a
child that goes under a parent in `Later`. Then ask the person: put those off
too, or remove the link with `plan.sh unblock`. A task comes back from `Later`
with `gh issue edit <n> --milestone '<title>'`.

## The board

```bash
bash <dir>/scripts/board.sh
```

It finds the GitHub Project titled `<repository> roadmap`, or creates it
under the repository's owner, and links it to the repository. It adds the
open issues it does not hold yet, and creates two views: *Unassigned*, a board
of the open issues that nobody has, and *By milestone*, a table. It ends with
two settings the API cannot make; pass them to the person. Run it again at
any time: it only adds what is missing. The *Unassigned* view does not know
blockers or sub-issues, so it is not the list of free tasks: `next.sh` is.

When `board.sh` stops on the `project` or `read:project` scope, give the
person this command, in place of what the message of `gh` says to do. The
person runs it once on each machine, in a terminal of their own, not through
`!` in Claude Code. On another host, as GitHub Enterprise Server, that host
goes in place of `github.com`.

```bash
gh auth refresh -h github.com -s project
```
