---
name: turn-eta
version: "0.1.0"
description: When a turn contains real work (editing files, running commands, digging through code), split it into steps, tell the user how many and when it will be done, time each step, and record the miss so the next estimate is closer. Skip it on conversation-only turns.
---

# turn-eta — say when this turn will be done, then learn from what it took

Before the work starts, write out the steps as a numbered list and say when it will be finished. Time
each step as it lands. When the turn ends, close the reply with the time it actually finished. The next
estimate reads that log.

## When this runs

**Every turn that contains real work** — editing a file, running a command, searching the codebase.

- Work in the turn → call `plan` **before** starting and open your reply with what it prints, in the
  order it prints it: **the `**ETA …**` line first, on its own, then the numbered steps**. The finish
  time is what the reader came for; the steps below are the reasoning behind it. Call `step <id>` as
  each step lands, and `done <id>` when the turn's work is finished.
- **The last paragraph is a time too, and which time depends on whether anything is still running.**
  - Everything finished before you write the reply → the whole block `done` prints: the finish line
    the finish line from `done`. By then the ETA has expired; reprinting it hands the reader a
    guess the clock already disproved, while the per-step times show where it went wrong.
  - Something is still running (a background job, a delegated task) → the forecast: `**ETA 17:45**`.
    Recompute it as you write, never paste the number `plan` printed earlier.
- Conversation-only turn (answering a question, deciding what to build) → do nothing. It is noise.
- A one-line fix is not worth the ceremony either. Use it when there is more than one step.

## Commands

Pure Node, no install. Call it from wherever the skill is installed.

```bash
# before the work — name the steps and get an ETA
node <skill>/scripts/eta.js plan \
  "reproduce the failure" "fix the date parser" "update the fixtures" "re-run the suite" \
  --provider anthropic --model claude-opus-5 --size M

# **ETA 17:45** (14 min)
#
# 1. reproduce the failure
# 2. fix the date parser
# 3. update the fixtures
# 4. re-run the suite
#
# 4 steps, ~14 min (3.5 min/step from anthropic/claude-opus-5 M, 6 turns)
#
# (last 6 estimates ran 3 min long)
# turn id: 48i35qek

# each time a step lands — measured, and the rest is re-forecast from the measured pace
node <skill>/scripts/eta.js step 48i35qek
# 2/4 fix the date parser — 8m 06s
#
# **ETA 17:49** (4 min later)

# when the turn's work is done
node <skill>/scripts/eta.js done 48i35qek
# **FINISHED 17:48** (estimated 14 min / actual 17 min)

# what the log says right now
node <skill>/scripts/eta.js stats
```

**Name the steps, don't just count them.** `plan` refuses a bare number. A count nobody can check is
not a plan — named steps let the person reading say "skip 3" before you start. Put that numbered list at
the top of your reply, then do the work.

**You must pass your own `--provider` and `--model`.** A shell cannot see which model is driving it.
Use the identifiers you know yourself by — `--provider anthropic --model claude-opus-5`,
`--provider openai --model gpt-5-codex`, `--provider google --model gemini-3-pro`. Anything missing
lands under `unknown/unknown`, which still works but pools every model together.

`--size` is `S` (small fix), `M` (normal, the default), or `L` (large chunk). Rough is fine; it only
keeps small turns from dragging the average of large ones.

**The turn id is required.** `plan` prints one; carry it through every `step` and the final `done` —
`step 48i35qek`, `done 48i35qek`. Another agent working in the same project writes to the same log, so a
call without an id used to close whichever turn happened to be open — someone else's. `step` and `done`
now refuse without it. A turn nobody has touched for four hours counts as abandoned.

## Where the log lives

```
<project root>/.eta/<provider>/<model>/log.tsv
```

Inside the project, so an agent whose permissions stop at its working directory can still read its own
history. Project root is the nearest `.git` going up, otherwise the current directory. Provider and
model are folders, so one model's pace never quietly becomes another's.

Add `.eta/` to `.gitignore`. It is a measurement of your machine on your turns; it means nothing to
anyone else and it changes on every turn.

Set `TURN_ETA_DIR` to another `.eta` directory to share history across projects. It is only consulted
when the local log is too thin to say anything.

## How the estimate gets better

`done` records the estimate, the actual, and the per-step times. `plan` reads them back and takes the
**median minutes per step**, walking from the narrowest match outward and stopping at the first rung
with at least 3 finished turns:

1. this provider + model + same size
2. this provider + model
3. this provider, any model
4. everything in this project's `.eta`
5. the shared log in `TURN_ETA_DIR`, same order
6. otherwise 4 minutes per step

Median rather than mean, so one turn that ran long does not drag every future estimate with it. Only
the last 20 turns per rung count. `plan` prints which rung it used, so the number is never a mystery.

Mid-turn, `step` blends that history with the pace this turn is actually running at, weighted by how
much of the turn is done: at step 1 of 4 the history still carries three quarters, by step 3 this turn
carries three quarters. One slow first step moves the finish time without hijacking it.
