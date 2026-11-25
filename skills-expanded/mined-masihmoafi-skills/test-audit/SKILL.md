---
name: test-audit
description: "Invoke whenever writing, changing, reviewing, or sweeping tests: an authoring gate for new tests, an audit for low-value, implementation-coupled or duplicate tests, and layered verification for AI-generated code."
---

# Test Audit

Keep only tests that earn their maintenance cost. Two modes, one value bar: the **authoring gate** for every new or changed test, and the **audit** that sweeps existing ones. Optimize for confidence, not deletion count. The [tdd skill](../tdd/SKILL.md) defines a good test and the regression rule.

## Authoring gate

Before adding a test, answer all four; a missing answer means wait:

1. What observable behavior, invariant or independent contract does it protect?
2. What credible regression makes it fail?
3. Why does existing coverage miss that failure? Each contract has one owner test at the strongest boundary; another layer needs its own risk. Extend a table-driven case or shared fixture rather than adding a near-duplicate.
4. Does it need a production seam (export, flag, wrapper, hook) no production caller needs? Then test at the real boundary instead.

A test that matches a junk pattern fails the gate unless the retention bar names the contract it alone guards.

## Junk patterns

- assertion-free coverage probes, self-comparisons, identity copiers;
- copied fixtures, inventories, manifests or export lists; exact source, import or string greps;
- private predicates or call shapes already tested at a real boundary; duplicate calls of one contract;
- tests that only keep test-only exports, globals or wrappers alive; production code whose only callers are tests;
- expected values produced by the code under test; mocks that implement the asserted behavior;
- fixtures that supply what the owner should produce, or assert a store the path never writes;
- capability tests that restate declared flags instead of exercising the delivery;
- negative controls that pass for an unrelated reason;
- names that promise more than the input exercises.

## Retention bar

Keep a test that independently enforces a public API, protocol, config, migration, storage, security, platform, default, generated-code, package, release or architecture contract. Also keep observable call ordering, regressions with a credible failure mode, and a source check when it is the cheapest independent guard (it fails when the user-facing key, byte or path changes and survives a rename). Static or slow is not a reason to delete. A kept test that fails on the baseline may be a product bug: reproduce it and fix the owner.

## Audit

1. Read root and scoped `AGENTS.md`, then the whole test, its production owner, callers, siblings, overlapping tests, CI routing and history. Stay read-only until the evidence is in.
2. For each candidate record: name and location; what failure it can detect; non-test callers of its seam; the stronger proof that remains; why it exists; what deletion it unlocks; risk and the focused command. A missing field means not ready.
3. Edit one coherent batch: delete obsolete test-only seams and dead paths (no aliases), move kept regressions to their owners, consolidate repeated assertions. Prefer net-negative production lines; add no replacement that restates the implementation.
4. Validate: run the smallest owner and sibling tests, the real script behind any removed grep, formatting and `git diff --check`, then the checks the repo requires. Never edit files a running test reads.
5. Report: what went and why, false positives kept and why, the proof run, production versus test lines (`git diff --numstat`), follow-ups. Land only when authorized, one batch at a time.

## Layered verification

Tests are one layer; stack cheaper ones before human attention, scaled to risk: deterministic guardrails (types, lint, tests, secret scans); a fresh-context LLM review; deploy-time flags, canaries and rollback; runtime traces and SLOs; then focused human review of intent and architecture.
