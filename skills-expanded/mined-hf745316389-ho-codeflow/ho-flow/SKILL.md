---
name: ho-flow
description: Use when the user asks to run a change through design, implementation and review as one flow, names solo or relay or auto, or wants a change handed between agents or sessions rather than done in one conversation.
---

# Flow

Set up the change, then run the phases in order. The phase skills do the work;
this one decides which phase runs, and where the flow stops.

## Reading the request

```
solo <request>        one agent runs every phase
solo auto <request>   the same, without pausing after the design
relay <request>       each phase hands off to another agent
```

If the request names no mode, use `mode` from `.ho/config.yaml`. If there is no
config, use `solo` and say so.

`auto` is an option on one task, never a mode and never a stored setting. It
does not survive into the next request.

## Setting up

If `.ho/` does not exist, create it: copy the protocol and config templates in,
then tell the user what you added. Do not silently add a directory to someone's
project.

If one or more changes are already open and the request does not name one,
list them and ask. Do not infer from recency, from ordering, or from which
looks more prepared, and do not run all of them.

Otherwise create `.ho/changes/YYYY-MM-DD-<slug>/change.yaml` with
`status: draft`.

## Names

These are the names. Do not invent variants — the next agent looks for exactly
these:

```
.ho/config.yaml
.ho/protocol.md
.ho/changes/YYYY-MM-DD-<slug>/change.yaml
.ho/changes/YYYY-MM-DD-<slug>/01-design.md
.ho/changes/YYYY-MM-DD-<slug>/02-implementation.md
.ho/changes/YYYY-MM-DD-<slug>/03-review.md
```

`status` is one of `draft`, `ready_for_implementation`, `implementing`,
`ready_for_review`, `rework`, `complete`, `abandoned`. Nothing else — a status
you coined is a status no other agent and no validator understands. There is no
`blocked` and no `reviewed`: a change that stopped on a question keeps the
status of the phase it stopped in, and a change whose review passed is
`complete`.

## Configuration

Read `.ho/config.yaml`: `mode` when the request names none, `paths.root` and
`paths.changes` if the project moved the directory from the default. `auto` is
never read from there — it is an option on one request.

Setting an approval key to `false` says the project does not want a routine
prompt for that class of action. It does not authorize anything, and the list
under **What `auto` does not cover** stands whatever the config says.

## Running the phases

1. Design. Follow `ho-design`.
2. **Stop.** Show the design and the open questions, and wait.
3. Implementation. Follow `ho-impl`.
4. Review. Follow `ho-review`.

The stop at step 2 is where the user approves the design. Under `auto`, skip
it — but only it.

## What `auto` does not cover

`auto` removes one pause: the routine approval of a design. It does not grant
anything. Irreversible deletion, data migrations, writes to systems outside the
project, publishing anything other people will see, production changes, and
anything the project's own rules gate all still stop and ask, in `auto` exactly
as without it.

A user who says "work straight through, don't ask me anything" is describing
the ordinary steps they do not want to be consulted on. Read it that way.
Checking that the blast radius matches what they asked for tells you what would
happen; it does not tell you they agreed to it.

## Relay

In `relay`, stop after each phase. The artifacts in `.ho/changes/<id>/` are the
entire handoff — the next agent has none of this conversation.

Before you stop, make sure the phase artifact and `change.yaml` are written,
then tell the user which change id to continue and which phase comes next.

Write that instruction so it works for whatever agent they open next. Name the
change id, the directory, and the phase. Do not name a product, a slash
command, or a config file — you do not know what they will use.

## Ending a stop

Two things the reader needs at every stop and does not reliably get. Everything
else about the message — headings, how much evidence, what order — is yours.

**Say what the status means, not only what it is.** `draft` reads as
"unfinished work"; it usually means "waiting for you". Whenever a raw status
appears, put its meaning beside it:

| Status | What it is waiting for |
|---|---|
| `draft`, with an open question | your answer |
| `draft`, with none | your approval of the design |
| `ready_for_implementation` | implementation to start |
| `implementing` | in progress, or stopped on a question |
| `ready_for_review` | a review |
| `rework` | another implementation round |
| `complete` | nothing — the change is done |

**End with a block the user can copy.** Not a sentence describing what to tell
the next agent — a fenced block they can select and paste. It names the change
id, the directory, the phase, and what to read first. It names no product and
no slash command, because you do not know what they will open.

```text
Continue change 2026-08-05-monthly-active-users, phase: implementation.
Directory: .ho/changes/2026-08-05-monthly-active-users/
Read change.yaml and 01-design.md before changing any code.
```

While a question is open, the block carries the answer into the next phase
rather than sending work that is not ready — and say so in one line, so the
reader knows the answer comes first.

The structure above is fixed. The language is not: write the message in the
user's language. Status values, file names and change ids stay as they appear
in `change.yaml`.

## Solo

In `solo`, the same agent continues. The artifacts still get written in full,
because the review has to check the work rather than remember it, and because
the user may hand it on later. A review you perform on your own work is
`review_kind: self` — label it and do not present it as independent.

## When a phase stops

A phase that stops on a question does not advance the status. Report the
question, leave the change where it is, and wait. Do not start the next phase
to make progress while the question is open.
