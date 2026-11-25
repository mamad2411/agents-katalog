---
name: port-verification-checklist
description: >
  Final gate before merging a large port or rewrite: confirm tests
  actually run (not skipped/stubbed), no functions were left as
  placeholders, no tests were deleted or weakened, and the green build is
  real. Use right before merging a big migration, when the user asks "is
  this port actually done / safe to merge", "did we really pass or did we
  cheat", "how do I verify the rewrite is complete", or when auditing
  machine-generated code for hidden stubs and skipped tests. Complements
  test-suite-driven-port (getting to green) by checking the green is
  trustworthy. Pairs with adversarial-code-review.
---

# Port verification checklist

A green test suite and a clean compile are necessary but not sufficient. Under parallel, machine-driven porting, the most likely way to get a false "done" is that the process quietly *lowered the bar* — stubbed a function, skipped a test, gated real code behind a shim — to make the signal turn green. This skill is the gate you run before pressing merge: verify the green is real.

The stakes: once merged to main, a rewrite is a commitment. Merging to main isn't necessarily a versioned release, so you can commit to the rewrite before you ship it to users — but you should only commit once you've confirmed the signals you're trusting mean what you think.

## Run this before merging

Go through each check deliberately. Any "no" blocks the merge.

### Tests actually ran

- [ ] **The suite executed — it wasn't skipped.** Manually spot-check that tests ran and asserted, rather than trusting the summary line. Count executed tests against the expected total.
- [ ] **Zero tests skipped or deleted.** Diff the test inventory before vs. after the port. No `skip`, `xit`, `#[ignore]`, `t.Skip()`, commented-out tests, or removed files snuck in to dodge a failure.
- [ ] **No assertions weakened.** Nobody changed `toThrow(RangeError)` to `not.toThrow()`, loosened an exact match to a substring, or replaced a value assertion with a truthiness check to get past a hard case.
- [ ] **Green on every target platform in the same build**, not "green on Linux, still red on Windows." Platforms finish at different times; wait for all of them.

### No stubs or gated-off code

- [ ] **No placeholder implementations.** Search the diff for `todo!()`, `unimplemented!()`, `panic!("not implemented")`, empty function bodies, `return null`/`return {}` stand-ins, and "temporary" constants (`// stand-in until phase B`). These are how "make it compile" silently becomes "make it stop complaining."
- [ ] **No real code gated behind a shim.** Confirm the actual implementation is wired in, not a compatibility stub that the tests happen not to exercise.
- [ ] **No paragraph-long justifying comments.** A comment that spends a paragraph explaining why a workaround is acceptable is a marker of code that should have been fixed instead. Treat each as a defect to resolve, not merge.

### The diff says what you think

- [ ] **Behavioral changes are intentional and reviewed.** Every place the port changed behavior (including tests that changed from failing to passing or vice versa) is understood and deliberate — see the release-vs-debug and comptime cases in `semantic-porting-pitfalls`.
- [ ] **Adversarial review covered the change**, and you verified the reviewers were actually catching discrepancies (spot-check a few of their findings against the original), not rubber-stamping.
- [ ] **A human read a representative sample** of the ported code side-by-side with the original. You don't read a million lines, but you do read enough to trust the machine did what the review says it did.

## How to check efficiently

- **Script the mechanical checks.** Grep the diff for stub markers and skip directives; compare test counts programmatically. These are fast, reliable, and repeatable across iterations — don't eyeball them.
- **Verify the reviewers, not just the code.** For a machine-generated port, your leverage is auditing that the adversarial review loop was correctly flagging real divergences between original and port, and that the porting/lifetime guides were followed. If the reviewers were sound and the suite is honestly green, the merge is defensible.
- **Run a few real commands locally** beyond the suite — exercise the actual product the way a user would — before you press merge.

## The bar

Merge when: 100% of the suite passes on all platforms, you've confirmed the tests genuinely ran, no functions are stubbed and no tests were skipped/deleted/weakened, behavioral changes are intentional, and you've personally verified a sample. Anything less means the green is decoration.
