---
name: mutation-testing
description: Runs mutation testing, reads the surviving mutants and strengthens the tests whose assertions failed to notice a deliberate code change.
---

# Mutation testing

Prove the tests can fail. A surviving mutant is a bug the suite would let through.

## Steps

1. Choose the tool for the stack: Stryker (JavaScript, TypeScript, C#), mutmut or cosmic-ray (Python), PIT (Java), go-mutesting (Go). Use the one in the project if present.
2. Scope the run to one module or the files changed on this branch. Never mutate the whole repository first. Set a timeout per mutant.
3. Run it and read the report: killed, survived, timed out, no coverage.
4. For each survivor, read the mutated line and decide:
   - **Real gap:** a boundary (`>` to `>=`), a removed condition, a changed constant or a dropped return that no assertion checks. Add or sharpen a test with a concrete input that distinguishes the original from the mutant.
   - **Equivalent mutant:** the change cannot alter behavior (log text, an unreachable branch, a performance tweak). Record it and move on.
   - **No coverage:** write the missing test first.
5. Rerun only the affected files and confirm the mutant is now killed.
6. Stop at diminishing returns. Report the score, not a demand for 100 percent.

## Rules

- Never kill a mutant by asserting on the implementation detail. Assert behavior.
- Never exclude mutants just to raise the score.
- Keep the added tests fast.

## Report

Score before and after, mutants killed by category, the tests added, and the equivalent mutants left with a one-line reason each.
