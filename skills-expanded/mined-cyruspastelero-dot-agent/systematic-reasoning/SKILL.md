---
name: systematic-reasoning
description: Use when the task is non-trivial, ambiguous, or spans multiple files/systems. Forces an explicit mental model before proposing changes. Invoke before debugging, architecture decisions, cross-file refactors, or any change where "I think I know what's happening" is tempting.
---

# Systematic Reasoning

Stop. Before you edit, build the model.

The cheapest mistake is one you make *before* writing code — when you jump to a fix that matches a shallow pattern instead of the actual behavior. This skill is the forcing function that prevents it.

## When to invoke

- Any bug that isn't a one-line typo.
- Any change touching more than one file or crossing a module boundary.
- Any refactor, migration, or schema change.
- Any performance/correctness question where the answer starts with "probably".
- Any ambiguous user request. Ask instead of guessing.

If you find yourself thinking "I'll just try X and see if it works," invoke this skill first.

## The four passes

Walk every pass. Do not skip. State your findings out loud in the response.

### Pass 1 — Restate the problem in your own words

Write the problem statement from scratch. Not a copy-paste of the user's request. If you cannot write it cleanly, you do not understand it yet — ask a clarifying question.

Required artifacts:
- **Goal**: what success looks like, in one sentence.
- **Constraints**: explicit (deadlines, deps) and implicit (no breaking changes, maintain API, etc.).
- **Out of scope**: what you will NOT touch.

### Pass 2 — Build the mental model

Read the code top-to-bottom, not keyword-search. Aim for *first principles*, not pattern recognition.

For every file touched or called:
- What is its single responsibility?
- What does it assume about its inputs?
- What does it guarantee about its outputs?
- Who calls it? Who does it call?

For any data flow crossing functions:
- Trace the variable from source to sink. Every transformation. Every boundary crossing (HTTP, DB, queue, file).
- Note every point where the type, shape, or invariant could change silently.

For any error path:
- What happens on failure? Is it retried? Logged? Propagated? Swallowed?
- Is there a partial-failure state the caller doesn't know about?

Output: a short "model" paragraph the user can read to confirm your understanding is correct.

### Pass 3 — Enumerate hypotheses (for debugging only)

List *every* plausible cause, even ones you think are unlikely. Rank by probability. For each:
- What evidence would confirm this?
- What evidence would rule it out?
- What's the cheapest check?

Then check in order of cheapest-ruleout-first. Never commit to a fix before you've ruled out the top 3.

### Pass 4 — Design the change

Only now propose code. The proposal must answer:
- **Blast radius**: what else could this affect? List the call sites you checked.
- **Reversibility**: is this easy to roll back? If no, flag it.
- **Test**: what test proves this works? What test proves it doesn't regress?
- **Counterfactual**: "if my model is wrong, how would I know?" Add a log, an assertion, or a test that would reveal the wrong model fast.

## Red flags — if you catch yourself thinking these, STOP and restart

| Thought | What it really means |
|---|---|
| "This looks like X, so it's probably Y" | You're pattern-matching, not reasoning. Read the actual code. |
| "I'll just try it and see" | You don't have a model. Build one first. |
| "The fix is obviously Z" | Obvious fixes are often the wrong-layer fix. Pass 2 first. |
| "It's probably just a race condition" | "Probably" ≠ evidence. Enumerate hypotheses. |
| "I'll add defensive checks to be safe" | Shotgun code. Find the real invariant first. |
| "This is too complex to fully model" | Then scope-narrow the change until it isn't. Don't ship guessing. |

## Anti-scope

Do not use this skill for: one-line typo fixes, rename operations, documentation edits, adding a single log line, or other changes where the whole blast radius fits on one screen.

## Pairs well with

- `systematic-debugging` for stack-trace-driven investigation.
- `writing-plans` for multi-step features.
- `verification-before-completion` after the change lands.
