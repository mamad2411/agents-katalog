---
name: run-sprint
description: Run one Sprint end to end against the real board — Planning that produces a Sprint Goal before it selects items, a Daily that replans the next 24 hours, a Review that changes the Product Backlog, and a close-out that returns undone work instead of rolling it silently. Each event has an entry gate that can fail. Use to start, run or close a Sprint, or to repair one that produced no usable Increment. Not for ordering the backlog, writing requirements, forecasting a release date, or configuring a board.
argument-hint: "[--plan | --daily | --review | --close] [--sprint \"S14\"] [--dry-run]"
user-invocable: true
agent: foundry-pmo:scrum-facilitator
model: sonnet
effort: medium
metadata:
  foundry.vertical: management
  foundry.io: "plan.v1 + tracker-item.v1 -> Sprint Goal, Sprint Backlog, review.v1"
license: Apache-2.0
---

# Run sprint

One Sprint, four entry points. Each phase refuses to start until its gate passes, because a
Planning without a Goal or a Review without a working Increment produces a ceremony rather than
a decision, and the cost lands two weeks later.

`--dry-run` is the default posture for every tracker mutation: show the command, apply on
approval.

## Phase gates

| Flag | Gate — fail means stop and fix, not proceed |
|---|---|
| `--plan` | a written Definition of Done exists; capacity is known; the top of the backlog has acceptance criteria |
| `--daily` | the Sprint Goal is retrievable in one line |
| `--review` | an Increment exists that meets the Definition of Done |
| `--close` | every selected item is `done`, `cancelled`, or explicitly returned to the Product Backlog |

## Step 1 — Read the real board, never the intention

```bash
node -e "process.stdout.write(process.env.FOUNDRY_WAVE || 'current')"
```

Get the normalised board from `foundry-pmo:tracker-operator` and read it from
`.foundry/blackboard/<wave>/tracker-operator.json`. Never ask the team what is on the board when
the board can be read.

If no `tracker-item.v1` set is available, continue from what the team reports and label every
empirical statement in the output `self-reported`. Do not silently mix reported and measured
numbers in the same table — that is how a Sprint report becomes fiction.

## Step 2 — `--plan`

Answer the three topics **in order**. The order is the whole method: starting from "what"
produces a ticket list with a goal painted on afterwards.

**Why — the Sprint Goal.** One sentence, describing an outcome, not a list of items. Test it two
ways before accepting it:

- *Droppability*: name at least one selected item that could be cut with the Goal still met. If
  nothing can be cut, there is no Goal, only a scope.
- *Falsifiability*: state how you will know at the Review whether it was met. "Make progress on
  checkout" fails. "A returning customer can complete checkout with a saved card" passes.

**What — selection.** Pull from the ordered backlog until capacity is reached. Capacity is
measured, not assumed:

- available person-days, minus known leave, minus the measured share that historically goes to
  interrupts and support;
- for a first Sprint with no history, reserve 20% and say plainly that the figure is a placeholder
  to be replaced by measurement after two Sprints.

Refuse to select an item with no acceptance criteria. Label it `needs:criteria` and route it to
`foundry-pmo:requirements-analyst`. Refuse an item larger than half the Sprint: split it with
SPIDR via `foundry-pmo:groom-backlog` or leave it out.

**How — enough plan to start.** Only the first days need decomposing. A fully task-decomposed
Sprint is a plan that will be wrong by Wednesday.

Record dependencies that leave the team as `risk.v1` with a named owner. A dependency discovered
at the Review was always visible at Planning; the difference is whether anyone wrote it down.

Output of this phase: the Sprint Goal, the selected items, capacity arithmetic shown, and the
explicit list of what was deliberately not selected.

## Step 3 — `--daily`

Fifteen minutes, for the Developers, producing an adjusted plan for the next 24 hours. Not a
status round.

Ask three things about the *board*, never about people:

1. What has moved since yesterday, and does the Sprint Goal still look reachable?
2. Which items are ageing past the p85 cycle-time line? Name them; they are the ones that will
   miss.
3. What is blocked, who owns unblocking it, and since when?

Blocked ageing is the single number worth tracking daily. An item blocked for three days with no
named owner is not blocked, it is abandoned.

If the Sprint Goal is no longer reachable, say so on the day it becomes true, not at the Review.
The Product Owner decides what happens next — renegotiate scope, or in the extreme cancel the
Sprint, which only the Product Owner may do.

## Step 4 — `--review`

A working session whose output is a **changed Product Backlog**. If the backlog is identical
afterwards, the Review did not happen; a demo happened.

Gate: only Increment that meets the Definition of Done is shown. Showing work that is nearly
done trains stakeholders that "done" is negotiable, and it is the fastest way to destroy the
meaning of the word on a team.

Run it in this order:

1. State the Sprint Goal, then whether it was met — yes or no, before any demonstration.
2. Show working software, not slides.
3. Take feedback as backlog changes, recorded live with `foundry-pmo:tracker-operator`.
4. Restate what changed in the market, the product or the dependencies since Planning.

Record the met/not-met verdict as a fact. Two consecutive not-met Sprints is a signal about
Planning, not about effort, and it belongs in the Retrospective as evidence.

## Step 5 — `--close`

Every selected item ends in exactly one of three states, and the third one is the one teams skip:

| Outcome | Action |
|---|---|
| `done` | meets the Definition of Done, counts as throughput |
| `cancelled` | closed without delivery — never counted as throughput |
| returned | moved back to the Product Backlog, re-ordered by the Product Owner, estimate discarded |

**Undone work is returned, not rolled.** An item that silently carries to the next Sprint keeps
its stale estimate, distorts the next Planning, and quietly makes the backlog stop describing
reality. Returning it forces a re-decision, which is the point.

Then hand off:

- close-out counts and the met/not-met verdict to `foundry-pmo:delivery-reporter`;
- the measured throughput to `foundry-pmo:flow-analyst`, which owns the forecast;
- the Retrospective to `run-retrospective` — always after close, never merged into the Review.

## Anti-patterns this skill refuses

- Extending the Sprint to finish the work. Length is fixed; scope flexes.
- Adding work mid-Sprint without renegotiating against the Goal.
- Planning that opens with the ticket list.
- A Review that shows undone work.
- Merging Review and Retrospective into one meeting to save an hour: one inspects the product,
  the other inspects the process, and the product always eats the whole hour.
- Reporting velocity outside the team.

## Degradation

- **No tracker.** Runs entirely from team input; everything is labelled `self-reported`.
- **No Definition of Done.** `--plan` and `--review` both fail their gate. Drafting one from what
  the team already checks before merging becomes the first task.
- **`superpowers` absent.** Retrospective discipline falls back to the rules in
  `run-retrospective` rather than the shared skill; announce which path was used.

## Progressive disclosure

- `references/sprint-goal.md` — worked examples of goals that pass and fail the two tests.
- `references/capacity.md` — capacity arithmetic, interrupt-share measurement, first-Sprint defaults.
- `references/definition-of-done.md` — a DoD whose every line is answerable yes/no.
