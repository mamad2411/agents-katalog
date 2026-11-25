---
name: legacy-refactoring
description: Changes legacy or untested code safely by pinning current behavior with characterization tests, finding seams to break dependencies, and refactoring in small behavior-preserving steps that keep the build green. Use when modifying code that has no tests, cleaning up a large class or function, untangling dependencies, preparing old code for a new feature, or replacing a module piece by piece. Not for rewriting or migrating whole systems.
license: MIT
---

# Legacy Refactoring

Refactoring changes structure without changing behavior. If you cannot show that behavior did not change, you are rewriting, not refactoring. Pin the current behavior first, then move in small steps, running the tests after every step.

## When to use

- You must change code that has no tests or poor tests.
- A function or class is too large or tangled to change safely.
- A new feature is hard to add because of the current structure: "make the change easy, then make the easy change".
- A module needs to be replaced gradually while the system keeps running.

## When not to refactor

- The code works, rarely changes, and nobody needs to touch it.
- An urgent fix is needed: make the minimal fix with a test, and propose the refactor separately.
- You do not yet understand what the code does: characterize it first (step 3).
- There is no way to verify behavior and no time to add tests. Tell the user the risk instead of refactoring blind.

## Workflow

1. **Agree on the goal.** What change is the refactor enabling? Keep the scope to what that change needs, and confirm it with the user.
2. **Map the area.**
   - Entry points and callers (search for references, including strings in config, templates, reflection and dependency-injection setup).
   - Side effects: database, files, network, global state, time, randomness, environment variables.
   - History: `git log --follow -p -- <file>` and `git blame` explain why odd-looking code exists. Odd code often encodes a past bug fix.
3. **Pin the current behavior with characterization tests.**
   - Call the code with representative inputs and assert what it *currently* returns or does, even if it looks wrong.
   - If you find behavior that looks like a bug, record it in the test name or a comment and report it to the user. Do not fix it during the refactor.
   - For large or complex outputs, use approval / golden-master testing: capture the output to a file, review it once, and compare future runs against it. Tools: ApprovalTests (many languages), Jest/Vitest snapshots, syrupy (pytest), Verify (.NET), insta (Rust), golden files in Go (`testdata/*.golden`).
   - Scrub non-deterministic parts (timestamps, generated IDs, ordering) before comparing.
   - Run coverage on the characterization tests to see which branches are still unpinned, and add inputs until the code you will touch is covered.
4. **Break dependencies so the code can be tested** using the smallest seam that works (table below).
5. **Refactor in small steps.** One refactoring at a time (see [references/refactoring-catalog.md](references/refactoring-catalog.md)). Run the tests after every step. Prefer the editor's or IDE's automated refactorings (rename, extract, move, change signature), which are safer than manual edits.
6. **Commit each green step.** Keep refactoring commits separate from behavior changes. Never mix them in one commit. A reviewer should be able to read a refactor commit and trust that it changes nothing.
7. **Make the behavior change** the refactor was for, in its own commits, with its own tests.
8. **Clean up.** Remove seams and scaffolding that are no longer needed, and delete dead code only with evidence it is unused (search, logs or usage metrics for public endpoints). Replace characterization tests with clear behavioral tests where that improves readability; keep them if they still add protection.

## Seams: getting code under test

| Problem | Seam |
|---|---|
| The code creates its own dependency (`new DbClient()` inside a method) | **Parameterize:** pass the dependency in through the constructor or a parameter, defaulting to the current one so callers do not change |
| It calls a static or global (current time, random, a config singleton) | **Extract and inject:** wrap the call in a small interface or function parameter; or **extract and override** it in a test subclass |
| A method is too large to test, but you need to add logic | **Sprout method/class:** write the new logic in a new, fully tested function and call it from the old code |
| You need behavior before or after existing logic | **Wrap method/class:** rename the original, create a new method with the old name that calls the original plus the new behavior (a decorator) |
| The code talks directly to an external system | **Adapter:** introduce a narrow interface around the external system; use a fake in tests |
| A module imports something with side effects at load time | **Link/module seam:** module-level mocking or test build configuration (`jest.mock`, `unittest.mock.patch`). Use as a last resort; it couples tests to file layout |

Prefer seams that also improve the design (parameterize, adapter) over seams that exist only for tests (subclass-and-override, module patching).

## Replacing a module gradually (code-level strangler fig)

1. Put a facade or interface in front of the old module and route all callers through it, with no behavior change.
2. Implement the new version behind the facade, one case at a time (by operation, input type, tenant or feature flag).
3. For high-risk logic, run both paths and compare: call the new path in the background, log any differences, and keep returning the old result until differences reach zero.
4. Switch traffic gradually, with a quick way to switch back.
5. Delete the old path once nothing uses it.

## Keeping the build green

- Every commit compiles and passes the tests. If a step breaks many tests, revert it and take a smaller step.
- To change a widely used signature, use **parallel change** (expand, migrate, contract): add the new function or parameter alongside the old one, move callers over in small batches, then remove the old one.
- Mark public APIs you plan to remove as deprecated, with a pointer to the replacement, before removing them.
- Let the compiler or type checker do the searching: change a type or signature and use the resulting errors as the list of call sites.
- Merge to the main branch often. A long-lived refactoring branch diverges quickly and becomes a rewrite.

## Anti-patterns

- **Big-bang rewrite** of a module without tests, presented as a refactor.
- **Fixing bugs mid-refactor:** behavior changes hidden inside structural commits. Record them, then fix separately with a test.
- **Scope creep:** refactoring everything nearby until the diff is unreviewable.
- **Tests coupled to the old structure:** characterize at the public boundary, or the tests will break on every step and stop protecting you.
- **Mixing formatting and logic:** run formatters in a separate commit, and list that commit in `.git-blame-ignore-revs` so blame stays useful.
- **Deleting "dead" code that is alive:** code reached through reflection, dependency injection, templates, routes defined in config, scheduled jobs, feature flags, or external clients. Search for string references too.
- **Refactoring without running the tests** after each step, then debugging a pile of changes at once.

## Done when

- Characterization tests covered the touched code and passed before and after every step.
- The goal is met: the intended change is now simple, and it is in its own commits with its own tests.
- Refactor commits and behavior commits are separate.
- Suspected bugs found along the way are reported, not silently fixed.
- Dead code was removed only with evidence it was unused, and temporary seams are gone.

## References

- [references/refactoring-catalog.md](references/refactoring-catalog.md) — read for step-by-step mechanics and gotchas of common refactorings (extract, inline, move, rename, parameter object, replace conditional with polymorphism, guard clauses, split loop, and more).
