---
name: senior-plan
description: Use before the first edit of a change rated medium risk or higher that has several steps or crosses modules, such as a feature spanning several files, a change to a shared contract or to data already stored, or an operation that can fail halfway through (payments, stock, external calls). Not for low-risk edits, an obvious local fix, questions, or work where the user already gave the steps.
---

# Senior Plan

**Core rule:** before the first edit, write down what done means and how this change could still go wrong. Keep the plan as short as the change.

A plan is worth its cost where the mistake is in the design, not in a line: a step that fails after another already took effect, a call that runs twice, a caller or stored record still in the old shape. Those are cheap to see before coding and expensive to find after.

## 1. Map what the change touches

Before planning, find out, by searching rather than assuming:

- every caller and reader of what changes: grep the function, field or key across `src/`, tests, scripts and fixtures;
- data that already exists in the old shape: stored records, saved files, seeds, caches, messages in flight;
- external effects: payments, emails, other services, anything that cannot be taken back by the code;
- the project's recorded decisions for this area (`.senior/decisions.md`) and the existing pattern for the same problem.

Stop when you can name them. A change that turns out to touch one file and nothing stored is not a planning task: go back to `senior-engineering` and just do it.

## 2. Write the plan

At most about ten lines, in your working notes or the reply:

1. **Goal and acceptance criteria:** observable outcomes someone could check ("cancelling twice refunds once"), not implementation steps.
2. **Steps, in order,** with the files each touches.
3. **For each step with an effect,** what happens if it fails after an earlier step succeeded, if it runs twice, and if it meets old data or an old caller.
4. **Proof:** the test or check that shows each acceptance criterion, including one for each failure case in point 3.
5. **Rollback:** how to undo the change, and what cannot be undone.

## 3. Challenge the plan before coding

Look for the two likeliest ways the design is wrong. Ask, for this change:

| Question | Typical fix |
|---|---|
| A later step fails: is the earlier one already done? | Do the step that can fail first, or undo the earlier one, so state stays consistent |
| The same call arrives twice (retry, double click, a second run)? | Make it idempotent: record that it happened, and check before acting |
| Old records or callers still use the previous shape? | Read both shapes; migrate stored records only where the project allows rewriting them, and in the same change. Never strand existing data |
| Two requests at once? | Use the store's atomic operation instead of read-then-write |
| A step is destructive or external (deploy, migration, real money)? | Prepare and verify it, then stop for the user's approval |

Update the plan with what you find. If a question has no good answer, say so in the plan rather than coding around it.

## 4. Decide whether to wait

Proceed without waiting when the plan only implements what was asked. Stop and show the plan when it includes a destructive or external step, when the project's or user's instructions require approval for this kind of change, or when two designs differ in a way the user must own (behavior they would see, cost, data loss). Otherwise a pause is a delay, not a safeguard.

## 5. Build to the plan

- Implement in the plan's order and add the plan's proof as you go, including the tests for the failure cases.
- When the code shows the plan was wrong, change the plan and say why; do not drift from it silently.
- Do not add steps the goal does not need.

## 6. Exit

The plan is done when every acceptance criterion has evidence. Hand over to `senior-finish`: it checks each criterion and each failure case against the final change, and reports any planned step that was not done or was changed.

## When the plan starts to slip

| If you notice yourself thinking… | Do this instead |
|---|---|
| "I'll figure out the edge cases while coding" | Name them now; they decide the design |
| "Nobody calls it twice" | Retries, double clicks and reruns do: decide what the second call does |
| "I'll update the callers I know about" | Search for them; the one you miss is the bug |
| "The stored data will be migrated later" | Then the code must read the old shape until it is |
| "The plan is approved, so the extra refactor is fine" | Only planned work; list the rest as a follow-up |

And the reverse: if the plan is longer than the change, or you are planning a rename of a local variable, stop and just do it.
