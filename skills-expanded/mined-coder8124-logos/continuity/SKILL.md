---
name: continuity
description: Use when starting work on a project with prior history, before proposing any non-trivial approach, and before ending a work session. Covers checking what was already ruled out, recording progress, and handing work to the next agent via logos.
---

# Working with logos

logos is the user's memory across every AI tool they use. What you write here,
Cursor and Codex read later, and what they wrote, you can read now. It is
markdown on their disk — not a service, and not yours.

## Before you propose anything, check it was not already ruled out

This is the habit that matters most, and it is the one nothing else prompts you
to do.

Call **`before_you_try`** with the approach you are about to suggest, whenever
you are about to propose a solution, a refactor, a library, a vendor, or a fix
on work that has history. **Especially when the idea seems obvious** — obvious
approaches are the ones already attempted, and the reason they were abandoned is
rarely obvious from the code that remains.

If it returns something, say so out loud before proposing:

> This was tried in March — the drop test failed at 1.2m. If you still want it,
> here is what would have to be different.

A recorded failure is evidence, not a veto. If you think it is right anyway, say
what has changed. What you must not do is propose it as though it were new.

## When picking up existing work

Call **`resume`** with the project name. You get the last agent's checkpoint —
what they were doing, what they decided, what they ruled out, what is still open,
and the next step — followed by project context.

The plugin's SessionStart hook usually does this for you. Call it explicitly when
you switch projects mid-session, or when the user says "continue" and you have no
history with what they mean.

Read the **failed approaches** section before proposing anything. It is there
for exactly that.

## While working

Call **`note_progress`** after a decision, a dead end, or a surprising
discovery. One line. It is cheap and meant to be called often — these stay
uncommitted until a checkpoint folds them in, so use them freely rather than
saving everything for the end.

A dead end noted the moment you hit it survives even if the session dies before
you check out. That is the whole reason to write it down early.

## Before stopping

Call **`checkpoint`** before the session ends, when the user says they are
wrapping up, or when context is running short. Do not wait to be asked.

Fill in `failed` properly. Anything omitted is lost.

Give every decision its reason ("X, because Y"), and state the task's `intent`
— why it matters — on its first checkpoint; later checkpoints with the same task
wording inherit it, so state it again if you reword the task. The reasoning is otherwise only in the transcript, and nobody
resuming should have to reread that.

If the user is switching tools — "finish this in Cursor" — use **`handoff`**
with `to` set, so the record names who it was left for.

## What not to do

- Do not call `remember` for things that belong in the code or in
  `CONTRIBUTING.md`. logos holds *operational* context — what was tried,
  decided, and left open — not repository instructions the next agent will
  read anyway.
- Do not restate the whole checkpoint back to the user. Act on it.
- Do not treat retrieved context as more current than what you can see in the
  working tree. The vault records what was true when it was written; the code
  records what is true now.
