---
name: spec
description: Use for nontrivial implementation, requirements, a PRD or vision document, or acceptance criteria. Defines done before code. Not for trivial edits, exploration, spikes or prototypes.
---

# Spec-driven development

Define what done means before code, because an agent fills every gap in intent from its training data. A spec adds no approval gate; ask only about material gaps.

Size the loop to the task (Stanford CS146S, 29 Sep 2026):

- a copy change or small fix: just ask the agent;
- a small feature across several files: one plan;
- a medium feature: research, then plan, in separate sessions;
- a big refactor or migration: several rounds of research and plans, split into stacked issues, one agent each.

For discovery, spike first and specify once the behavior is known. Review the spec and plan yourself; that review is where the leverage is.

The loop: **Specify, Plan, Execute, Verify.** Go back to Specify when evidence changes the intent.

## 1. Specify

Numbered items, each with an acceptance check and a status, written before work begins. A check is observable ("feature works" is not one). When the change touches money, data, security or an external integration, add all four risk checks:

1. **Failure:** what happens when a dependency or write fails.
2. **Concurrency:** what happens when actors or async events collide.
3. **Observability:** how production behavior is measured.
4. **Rollback:** how the old behavior comes back, and how that is checked.

When intent has gaps, interview the user (goal, constraints, criteria, non-goals, edge cases) before writing. Keep the spec in version control beside the code it governs. Two tiers, after [OpenSpec](https://openspec.dev): `specs/` holds the current truth of each capability; a change is a short proposal with its delta against that truth, and once shipped its delta is merged into `specs/` and the proposal archived. No competing specs for one capability.

```markdown
# SPEC: [Feature]

Goal: [1-3 sentences: the problem and the outcome]
Invariants: [contracts and rules that must not break]
Constraints: [stack, banned dependencies, limits]

| # | Item | Acceptance check | Status |
| --- | --- | --- | --- |
| 1 | [observable happy path] | [command or action → result] | todo |
| 2 | [failure / concurrency / rollback, as relevant] | … | todo |

Non-goals: [what must not be touched]
Stop and ask: [3-5 task-specific conditions, e.g. a test still fails after 3 fixes; data would be deleted outside a test environment]
```

## 2. Plan

Read the spec and the codebase's conventions; write the approach, the trade-off chosen and why, the files affected and the order. Then split it into tasks: one atomic change each, ordered by dependency, each with a binary done-check (if it needs "and" twice, split it). Rate each task's **importance** (foundational, important, nice-to-have) and **difficulty** (easy, medium, hard) separately: importance is value, difficulty routes the work.

## 3. Execute

One task per fresh session when a combined diff would be too big to review; otherwise run the list in one session. Tick each item's status as its check passes. When reality contradicts the spec, stop, update the spec, then resume.

## 4. Verify

Every project gate passes first (lint, types, tests). A claim of "passes" or "fixed" needs the command run in this turn and its full output read; an earlier run or a subagent's report is a lead, not evidence. Evidence ranks: an agent's claim (untrusted) < automated tests or CI (necessary, not sufficient) < a real end-to-end run < the user's own acceptance, the only thing that closes "done". Name the level behind every completion claim, and give the user a one-line check per item.

For a vision document or PRD, follow `project-docs` (`VISION.md`): thesis, purpose, value, non-goals, kept apart from status.

Source: *AI-Native Software Engineering*, chapters 5 and 6.
