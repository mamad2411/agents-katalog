---
name: refactor-cleanup
description: Improves changed code for reuse, simplification, readability, and efficiency without changing behavior, then re-runs tests to prove behavior is unchanged. Quality-only — it does NOT hunt for correctness bugs (use code-review for that).
when_to_use: โค้ดทำงานถูกแล้วแต่รก/ซ้ำ/ซับซ้อนเกิน; หลัง green ของ TDD; เมื่อสั่ง simplify/cleanup
---

## When to Use

Use after code already works and is verified — you are improving shape, not correctness.

- After a TDD cycle reaches green and the diff is messy (duplication, deep nesting, long functions).
- When asked to "simplify", "clean up", "dedupe", or "make this readable".
- When a working diff has obvious quality debt before commit/PR.

Do NOT use this to find bugs. If the goal is "is this correct?" use `code-review` instead. This skill assumes behavior is right and keeps it right.

Scope = the changed code (current diff / files just touched). Do not refactor unrelated parts of the codebase you happened to open.

## Steps

1. **Establish a green baseline first.** Run the test suite (or the narrowest relevant subset) and confirm it passes BEFORE touching anything. If you cannot run tests, stop — there is no witness for "behavior unchanged", so refactoring is unsafe. Record the baseline pass count.
2. **Scope to the diff.** Use `git diff --name-only` (or the list of files you just edited). Only target code inside that scope.
3. **Scan for specific smells**, in priority order:
   - **Duplication** — same logic in ≥2 places (grep the literal/pattern to find all copies).
   - **Dead code** — unused vars, params, imports, unreachable branches, commented-out blocks.
   - **Deep nesting** — `if` pyramids ≥3 levels → candidates for early-return / guard clauses.
   - **Magic values** — repeated literals (numbers, strings) that should be a named constant.
   - **Long functions** — one function doing several jobs → extract a well-named helper.
   - **Bad names** — variables/functions whose name does not say what they do.
4. **Fix one smell at a time, smallest viable edit.** Pick ONE change type per step:
   - *Extract* a function/constant.
   - *Rename* for clarity.
   - *Dedupe*: grep the repeated form, then `Edit` with `replace_all` to the single shared call.
   - *Flatten*: invert a condition and `return`/`continue` early to kill nesting.
5. **Re-run tests after EVERY step.** Same pass count = behavior preserved → keep going. Any failure = the refactor changed behavior → revert that single step (it was the only change) and try a smaller/different cut. Never edit the test to make it pass.
6. **Stop at the right altitude.** When the diff is clean and each further change would add indirection without clear payoff, stop. Compare before/after: line count should usually go down or stay flat, never balloon.
7. **Keep refactor commits pure.** Commit only the no-behavior-change cleanup, separate from any feature/bugfix commit. A refactor commit message should say what was reshaped, not what was added.

## Common Errors

- **Refactoring on a red/unknown baseline.** If you never confirmed green at step 1, a later failure is ambiguous — you can't tell if you broke it or it was already broken. Always baseline first.
- **Batching many edits before testing.** When ten changes ship together and tests go red, you can't isolate the culprit. One change → one test run.
- **Silent behavior drift.** Reordering side effects, changing default values, swapping `==`/`is`/`===`, altering error/exception flow, or changing iteration order are NOT pure refactors. If a test can't see the difference, add no such change — or treat it as a behavior change outside this skill.
- **Over-abstraction.** Extracting a "helper" used once, or a generic for two slightly-different cases, makes the code harder to read. Rule of three: dedupe at the 3rd real repetition, not the 1st.
- **`replace_all` over-reach.** A literal like `5` or `"id"` may match unintended spots. Grep first, eyeball every hit, then replace — or scope the rename narrowly.
- **Mixing in a feature/fix.** "While I'm here…" edits that change behavior contaminate the refactor and break the "tests are the witness" guarantee. Keep them out; do them as a separate change.

## Verify

- Test suite passes with the **same** pass/fail count as the step-1 baseline (no tests skipped, weakened, or deleted).
- `git diff` contains only structural changes — no altered literals/logic that change outputs, no removed assertions.
- Lint/format/typecheck (if the project has them) still pass.
- The changed code is measurably simpler: fewer lines, shallower nesting, fewer duplicated blocks, or clearer names — and no new layer of indirection added without payoff.
- If any check fails or can't run, the refactor is not done — revert the last step rather than ship unverified.
