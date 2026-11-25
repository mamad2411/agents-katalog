---
name: impeccable-intent
description: Understand the true intent behind a request before writing any code. Use at the start of every non-trivial task, especially vague ones ("make it better", "add a page", "fix the layout").
---

# Impeccable Intent

Code written against a misunderstood requirement is worse than no code. Before
implementing anything non-trivial, lock the intent.

## Process

1. **Restate the goal in one sentence.** What does the user actually want to exist or
   change when this task is done? If you can't write that sentence, you don't understand
   the task yet.
2. **Identify what is NOT being asked.** Scope creep starts here. "Add a login page" does
   not mean "add auth, a user table, and password reset."
3. **Check the existing codebase first.** Does something similar already exist? Reuse and
   extend before creating. Search `src/components/` and `src/app/` before adding files.
4. **Surface assumptions explicitly.** If the request is ambiguous, state your
   interpretation before coding: "I'll add this as a Server Component at `/dashboard`,
   without auth — say so if you meant otherwise."
5. **Choose the smallest correct implementation.** The best change touches the fewest
   files while fully solving the problem.

## Red flags that mean STOP and clarify

- The request could reasonably mean two different features.
- Implementing it requires inventing product decisions (pricing, copy, data models).
- It conflicts with an existing pattern in this repo.
- It requires new dependencies — justify each one against what's already installed.

## Definition of done

A task is done when: the stated goal works end-to-end, `npm run lint`, `npm run
type-check`, and `npm run test` pass, and nothing unrelated was changed.
