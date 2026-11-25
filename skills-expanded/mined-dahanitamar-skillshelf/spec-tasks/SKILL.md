---
name: spec-tasks
description: Turn a technical spec, a change proposal or a plain list of requirements into an ordered task list where every task cites the acceptance criteria it closes, or states its own done-condition. Use before any code is written, when starting a milestone, when picking up a change proposal, or when the user asks what to build first, how to break down a feature, or for an implementation plan. Writes docs/changes/NNNN-slug/TASKS.md. Writes no code.
---

# Spec Tasks

A spec says what the system must do. A task list says what to do next, in what order, and how you will know each step worked.

The difference that matters: **every task names the acceptance criteria it closes.** A task that closes nothing is either unnecessary work or evidence of a criterion nobody wrote. That single requirement is what lets an executor verify each step instead of guessing when it's finished.

## The one rule

**A task is done when a named criterion is satisfied — not when the code looks finished.**

If you cannot name the `AC-###` a task closes, you have one of two problems, and both are worth stopping for:

- The work isn't needed. Delete the task.
- The spec is missing a requirement. Go add it, then come back.

A criterion in an unmerged proposal written on a branch may carry a provisional id such as `AC-NEW-1`; cite it as written and it is renumbered at merge. Never invent a criterion inside the task list to resolve this. Criteria live in the spec; tasks cite them (that is what keeps one source of truth).

---

## Workflow

### Phase 0 — Read the source

In this order:

1. `docs/CONSTITUTION.md` — the verify command, size limits, layout. Tasks must produce code that obeys it.
2. `docs/SPEC.md` — especially §2.1 Acceptance Criteria, §5 Data Models, §10 Build Order.
3. `docs/changes/NNNN-slug/PROPOSAL.md` if you were pointed at a change rather than the base spec.

**If §2.1 does not exist**, the spec predates acceptance criteria. Do not stop. Write the task list with inline criteria — one plain sentence per task stating what "done" means — and tell the user, once, that the spec predates §2.1 and that the criteria can be backfilled. Then carry on. A degraded task list beats no task list.

**If there is no spec at all**, take the requirements from the user's message or a file they name. Give each task a one-sentence done-condition, say once that no spec file exists, and ask one question only if no task can be given a checkable done-condition.

### Phase 1 — Choose the slice

Take one milestone from §10, or one change proposal. Never the whole spec.

A task list covering four milestones is a project plan, and project plans go stale before they're executed. One milestone is a unit someone can finish, verify, and ship.

### Phase 2 — Decompose

Read `references/task-format.md` for sizing, ordering, and the exact line format.

The sizing rule, in short: **one task is one sitting and one verifiable outcome.** If a task needs three unrelated things to be true before it's done, it's three tasks. If a task can't be verified without also finishing the next one, merge them.

Order by dependency, then by demo value. `dependsOn` may only reference tasks earlier in the list — a forward reference means the order is wrong, and it makes the executor a scheduler instead of a single forward pass.

### Phase 3 — Check coverage both ways

This is the phase that catches real mistakes. Build the matrix before writing the file:

| Direction | Failure it catches |
| --- | --- |
| Every task closes ≥ 1 criterion | Invented work nobody asked for |
| Every criterion in the slice is closed by ≥ 1 task | Silently dropped requirements |

An uncovered criterion is the more dangerous of the two, because nothing downstream will notice: an executor only verifies criteria that a task cites, so an uncited one is never checked and never built. Report both gaps before writing.

### Phase 4 — Write `TASKS.md`

Location: `docs/changes/NNNN-slug/TASKS.md`. For a base-spec milestone with no proposal, create `docs/changes/NNNN-mN-slug/` and say so. When the milestone ships, the directory moves to `docs/changes/archive/` with its ordinal kept.

```markdown
# <Milestone or change title> — Tasks

> Source: docs/SPEC.md §10 M1 · Constitution: docs/CONSTITUTION.md

- [ ] T-01 <what changes> — closes AC-001 — files: src/store.js
- [ ] T-02 <what changes> — closes AC-002, AC-005 — files: src/store.js — depends: T-01
```

Do not write a verify command into `TASKS.md`; the verify command comes only from the constitution, so a copy here would be ignored and could drift.

The checkboxes are the only state a task file keeps. There is no status file, because two records of the same fact eventually disagree.

### Phase 5 — Hand over

Report: the path, the task count, the criteria covered, and — separately, because it is the part worth reading — any criterion in the slice that no task closes.

---

## Boundaries

**Writes no code.** Not a scaffold, not a stub, not "just the types". The moment this skill writes code, its task list stops being a plan and becomes a description of what already happened.

**Invents no criteria.** Citations only. A criterion authored here would live outside the spec, and no drift check would ever see it.

**One slice at a time.** Finish and ship a milestone before decomposing the next one.

## Calibration

A five-task milestone gets five lines and no commentary. Past 12 tasks (hard stop at 20) split along a dependency cut: take the smallest prefix that is independently shippable, name the directories `NNNN-mN-slug` and `NNNN-mN+1-slug`, give each its own slice of the criteria, and write `Continues in: <path>` in the first file. A criterion belongs to exactly one slice.

## Reference files

- `references/task-format.md` — sizing, ordering, the line format, and the coverage matrix
