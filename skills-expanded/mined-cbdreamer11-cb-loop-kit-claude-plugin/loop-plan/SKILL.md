---
name: loop-plan
description: The planning session. Turns a goal into an ordered list of thin complete slices, decides which role and model runs each following session, and writes it all to the plan file. Use at the start of an epic, before any code.
effort: xhigh
---

# Plan the epic

This is the session that decides everything the cheaper sessions will do. It is
worth spending real thinking here — but the thinking must **land on disk**, because
a plan that only exists in this conversation dies with it.

## 1 · Get the goal straight first

Before planning *how*, state **what this is for and what it has to actually achieve**.
If that is not clear, clarify it now — with the owner if it is a business decision,
by reading the code if it is a technical one. A plan aimed at a fuzzy goal produces
work that is complete and useless.

## 2 · Dispatch the expensive thinking

Send the planning work to the **`loop-planner`** agent (its model and effort are
fixed in its own definition, so the quality of the plan does not depend on how this
session happened to be launched). Give it: the goal, the relevant paths, and
`.loop/VERIFY.md`.

If the epic has more than one plausible shape, dispatch **two or three planners with
different framings** in a single message (for example: smallest-shippable-first,
risk-first, user-first), then take the best and graft what is worth keeping from the
others. Say which framing won and why.

For anything touching money, permissions, auth, or schema, run `loop-council` on the
design **before** it becomes a slice.

## 3 · Write the plan to `.loop/STATE.md`

```
# Epic: <name>            Goal: <what it must actually achieve>

[ ] 1. <slice>
      non-negotiables: <what must be true to count as done>
      verify: BUILD + OBSERVE + DATA
      run: ./loop build          # session role that should execute it
[ ] 2. <slice>
      ...
Deliberately out of scope: <what and why>
```

Order the slices so each one is safe to stop after. Depth before breadth: one epic
at a time, and nothing new opens until what is open is closed.

## 4 · Assign a role to each following session

Each slice carries the command that runs it. The roles exist because the work is not
all the same shape:

| Role | Command | What it is for |
|---|---|---|
| plan | `./loop plan "<goal>"` | this session — split, decide, do not code |
| build | `./loop build` | implement the next slice completely |
| verify | `./loop verify` | run the contract and judge honestly |
| close | `./loop close` | adversarial audit, ledger, handoff |

**Be honest about the limit:** a session cannot change its own model once it is
running, and it cannot even read which model it is on. So a plan does not *switch*
the next session — it hands over the exact command to launch it, and the expensive
roles carry their model in their own agent definition so that quality survives a
sloppy launch. If unattended runs are wanted, the same command goes in a scheduler.

## 5 · Close the planning session

Print the slice list, the first command to run, and what you left out. Do not start
building — a planning session that starts coding stops planning.
