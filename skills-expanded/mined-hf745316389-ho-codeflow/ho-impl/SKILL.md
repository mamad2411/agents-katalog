---
name: ho-impl
description: Use when an approved design exists and the change has to be built from it, including when the design was written by another agent or in an earlier session, or when the work must be handed on afterwards with a record of what actually changed.
---

# Implement

Build what the design says. You are not redesigning it, and you are not
deciding anything it left open.

## Before you touch a file

Read `change.yaml`, the whole of `01-design.md`, and any earlier
`02-implementation.md` from a previous round. Then read every file the design
puts in scope. `status` must be `ready_for_implementation` or `rework`; if
`Open questions` still lists anything, the design is not ready — say so and
stop.

Set `status: implementing`.

## When the design does not match the project

The design was written against the project at some earlier moment. Acceptance
criteria name fixture rows, flags, files, and functions that may not be there.

**A design that does not fit what is actually in the project is a question,
not a puzzle to solve.** Stop, quote the criterion, quote what you found
instead, and ask.

This is the failure that shows up most in practice. Five independent agents
given one design whose AC named a fixture row that did not exist produced
three different repairs and none of them asked.

| Rationalization | Why it fails |
|---|---|
| "There is a clean local fix, so it isn't really a conflict" | The cleanness of your repair says nothing about whether it is the repair the author wanted. |
| "I documented it in a comment next to the code" | A comment in a file is not a report to the person who has to accept the change. |
| "Editing that existing assertion is outside the design's tasks, so I worked around it" | Both the edit and the workaround are decisions the design did not authorize. Noticing that is the moment to stop, not the moment to pick the other one. |
| "It only changes a test fixture, not behaviour" | An assertion is a claim about what the system should do. Changing one changes that claim. |
| "The intent is obvious even though the letter is wrong" | Then say what you think the intent is and get one word back. |

**Red flags:** "I'll just add a parallel fixture" · "this reflects the larger
fixture, not a behaviour change" · "the design clearly meant" · "I'll note it
in the deviations section and carry on".

What does **not** require asking: anything the design left unspecified that you
can settle without changing existing behaviour, an existing assertion, or the
files-in-scope list. Do it, and record it under `Deviations`.

Files a command produced as a side effect — byte-code caches, build output,
coverage data, lockfiles a test runner rewrites — are not files you wrote. The
scope list does not reach them, and running a command the project requires is
not a scope breach. Note them under `Actual file changes` if they are tracked,
say what produced them, and leave them as the command left them. Do not revert
them to make the tree look clean.

## Stop and ask, always

Irreversible deletion. Data migrations. Writes to systems outside this project.
Publishing or sending anything anyone else will see. Production changes.
Anything this project's own rules gate.

Confirming that the blast radius matches the request is not the same as being
allowed to do it. A standing "don't stop to ask me" covers ordinary
implementation steps; it does not extend here.

## Configuration

`.ho/config.yaml` governs two things in this phase.
`concurrency.verify_file_fingerprints` turns the fingerprint step below on or
off. `paths.changes` says where change directories live if the project moved
them from the default.

The approval keys do not lower the floor. `approval.destructive_actions: false`
says the project does not want a routine prompt for that class of action; it
does not turn an irreversible action into a routine one, and it is not the
user telling you to go ahead. Everything under **Stop and ask, always** stands
whatever the config says.

## Files changing underneath you

When you first read a file you will change, record its path and a SHA-256 of
its contents. Before you write, read it again and compare. If it changed and
the change is not yours:

1. Do not write.
2. Re-read the current file.
3. Apply your change on top of the new baseline if it still makes sense.
4. If the two changes contradict each other, stop and ask.

Never resolve an unexplained concurrent change by reverting it, overwriting the
whole file, or restoring an old copy.

## The artifact

Write `02-implementation.md` with these sections, in this order:

1. **Design and round reference** — which design, which round
2. **Task completion table** — every task from the design, with its outcome
3. **Actual file changes** — path by path, what changed
4. **Deviations and reasons** — every departure from the design, however small
5. **Verification commands and observed results** — the command, and its real output
6. **Unverified items and reasons** — what you could not check, and why
7. **Remaining risks**

## change.yaml

`status` takes exactly one of these values. There is no other vocabulary —
do not coin one:

`draft` · `ready_for_implementation` · `implementing` · `ready_for_review` ·
`rework` · `complete` · `abandoned`

Set `ready_for_review` only when every task in the design is done and every
acceptance criterion is met. If any task is unfinished or any criterion is
unmet — including because you stopped to ask something — the status stays
`implementing` and the question goes in `Deviations`. Blocked is not a status.

A report that says "blocked" while `change.yaml` says `ready_for_review` tells
the reviewer the work is finished. Only one of the two can be true.

## A second round

`02-implementation.md` keeps its name. Round 2 goes at the top; round 1 stays
below it, verbatim, under `## Round 1 (superseded)`.

Do not overwrite it and do not replace it with your own summary of it. The
reviewer needs round 1's own words — which deviations were accepted, what was
left unverified, why it stopped. Keeping the name is what lets the next agent
find the file; it is not permission to delete what is in it.

Label every result with its round. Round 1's command output is evidence about
round 1, and repeating it as though you ran it is the one thing this report
must never do.

## When the fix is to the design itself

A review can find that an acceptance criterion is wrong rather than unmet. You
cannot decide that — but once the user has answered it, write their answer into
`01-design.md` rather than leaving the design and the code contradicting each
other. Change only what the answer settles, record it under `Amendments` in the
design with the round and date, and note it as a deviation here.

If the user has not answered, do not amend. Say what needs deciding, leave the
status at `implementing`, and stop.

## What this file is and is not

The reviewer reads your code, not your prose. This report tells them where to
look and what you already ran; it is not evidence that any of it is correct.

So: every command in section 5 is one you actually ran this round, and the
result is its real output. Do not carry forward a result from an earlier round,
and do not write down what a command would print.

A task you could not finish is `not done`. A task whose acceptance criterion
fails is `failed`. Neither of them is `not applicable` — you do not have the
authority to retire an item the design put in.

## Ending the phase

Lead with what the status means. `ready_for_review` is waiting for a review;
`implementing` after a stop is waiting for an answer, and those are not the
same message.

In `relay`, end with a fenced block the user can copy: change id, directory,
next phase, what to read first, no product name. If you stopped on a question,
the block is for answering it — do not hand work forward that is not finished.
