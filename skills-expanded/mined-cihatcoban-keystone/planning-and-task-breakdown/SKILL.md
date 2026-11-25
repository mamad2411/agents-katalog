---
name: planning-and-task-breakdown
description: Decomposes an approved spec into small, ordered, independently verifiable tasks. Triggers - break this spec into tasks, make a plan, how should we sequence this work, where do we start, this task feels too big to start.
---

# Planning and Task Breakdown

Decomposition decides whether work lands smoothly or becomes a three-week
branch nobody can review. The goal is a sequence of slices, each of which
leaves the system **working, tested and shippable** — even if the feature is
not yet visible.

## The task test

A task is correctly sized when all of these hold:

- It maps to one acceptance criterion (or one clear part of one)
- It ships with its own test
- It is one reviewable commit or a small PR (≤ ~400 changed lines)
- The system is releasable when it lands — behind a flag if incomplete
- "Is it done?" has an unarguable answer
- One focused session finishes it

Any failure means split. A task that cannot be split without leaving the system
broken usually indicates a design problem, not a planning problem — say so.

## Vertical, not horizontal

The most common decomposition error is slicing by layer.

| Horizontal (wrong) | Vertical (right) |
|---|---|
| "Build all the data models" | "One entity end to end: schema → API → UI → test" |
| "Write the API layer" | "One endpoint, real response, contract test" |
| "Add all validation" | "Reject the one invalid case that matters most, with a test" |

Horizontal slices integrate at the end, which is where the surprises are.
Vertical slices surface them on day one.

## Ordering

1. **Unknowns first.** The task whose outcome could change the plan goes first,
   even if it is not the foundation. A spike is a legitimate first task, with a
   time box and a question it must answer.
2. **Contracts before consumers.** The interface (schema, API shape, event
   format) is agreed before both sides build against it.
3. **Reversible before irreversible.** Postpone data deletion, public API
   commitments and vendor lock-in until you have learned what you can.
4. **Walking skeleton early.** One thin path through every layer, end to end,
   before depth anywhere. It proves the integration, deployment and observability
   all exist.
5. **Cleanup is a task, not a hope.** Flag removal, dual-write teardown and
   dead-code deletion get their own numbered entries.

## Plan shape

`docs/plans/NNN-short-name.md`, from `templates/plan.template.md`: tasks with
criterion, test, evidence, files, brief, size and dependencies; then
sequencing rationale, risk, rollout, a change log and cleanup.

## Tasks someone else can pick up cold

A plan is executed by whoever is free — another session after compaction, a
subagent, a teammate. Write each task so it needs nothing outside itself:

- **Files** — the paths it owns. A task without them cannot be checked for
  overlap and will collide with its neighbor.
- **Brief** — two to four lines: the existing pattern to copy (`path:line`),
  the contract to honor, the constraint that applies. Not the spec again;
  only what a cold reader would otherwise have to rediscover.
- **Test** — the exact proof, so "done" is not a judgment call.

**Mark parallel work explicitly.** Two tasks may run in parallel only when they
share no files and neither needs the other's output; write `Parallel with:` on
both. Everything else is sequential by default. How to run them:
`agent-orchestration`.

## Review the plan before T1

For a plan with more than five tasks, a parallel section, or any irreversible
step, have a fresh-context reviewer (`adversarial-reviewer`) check it against
the spec before work starts. Give it the spec and the plan only. It answers:

1. Is every acceptance criterion covered by a task — and every task by a
   criterion?
2. Is the riskiest task first, and is anything irreversible postponed?
3. Do any two "parallel" tasks touch the same file or depend on each other?
4. Are flag removal and cleanup tasks present?

Fix the findings in the plan, not in a comment beside it. A plan error found
now costs a line; found at T6 it costs the tasks built on it.

## Sizing

Use S / M / L, not hours.

- **S** — path is obvious, no unknowns
- **M** — one unknown, resolvable within the task
- **L** — two or more unknowns → **split it now**; L never survives into a plan

Sizing is an uncertainty signal, not a schedule. If someone needs dates, count
S/M items and state the assumption explicitly.

## Replanning

Plans are wrong on contact; that is expected, not a failure. Replan when:

- A task turns out 3× its estimate → the decomposition was wrong, redo it
- A spike invalidates an assumption → revisit the spec, not just the plan
- Two tasks keep blocking each other → the boundary between them is wrong
  (`boundaries-and-dependencies`)

Update the plan file and log the change in its `Changes` section: split,
inserted, skipped, reordered or abandoned, with the date and the reason. A
plan that has silently diverged from reality is worse than none, because
people still trust it.

## Exit checklist

- [ ] Every task maps to a spec criterion
- [ ] Every task is vertical and independently verifiable
- [ ] Every task names its files and a brief a cold reader can act on
- [ ] Parallel tasks share no files and no outputs, and are marked as such
- [ ] Plans over five tasks, with parallel work or an irreversible step were
      reviewed against the spec by a fresh-context reviewer before T1
- [ ] Every change to the plan is logged with a date and reason
- [ ] No L-sized tasks remain
- [ ] Highest-uncertainty task is first or near-first
- [ ] Dependencies are explicit; no hidden ordering
- [ ] Cleanup and flag-removal tasks exist
- [ ] Rollout plan names the flag and its removal condition
