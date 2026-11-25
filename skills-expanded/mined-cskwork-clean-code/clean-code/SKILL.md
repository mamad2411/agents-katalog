---
name: clean-code
description: Refactor legacy code for readability and maintainability while preserving observable behavior and externally consumed contracts.
---

# Clean Code

Make the requested code easier to understand and change. Preserve observable behavior unless the user authorizes a behavior change. Prefer precise names, simpler local control flow, cohesive ownership, and removal of proven duplication over new abstractions.

## Establish the boundary

Read relevant repository instructions, inspect the working tree, and discover verification commands from configuration and CI. Trace the target, its callers, state changes, and external effects. Record the relevant test baseline, including pre-existing failures; preserve unrelated work.

State the scope, observable behavior to preserve, and the evidence that will protect it. Reuse scope already established in the conversation. Keep bug fixes, new features, upgrades, and unrelated formatting outside a behavior-preserving refactor unless the user includes them.

## Protect current behavior

Use [characterization-tests.md](../../references/characterization-tests.md) when existing tests do not protect behavior at risk. Add retained tests through a stable observable seam and run them against unchanged production code before refactoring. Cover meaningful boundaries, errors, output shape, side effects, and consumer-dependent legacy quirks. Control nondeterminism only where needed.

Reuse adequate existing coverage instead of adding tests that repeat it. Do not weaken assertions or replace behavioral tests with implementation mirrors. When unrelated tests already fail, record that baseline and verify the affected behavior without claiming the whole repository is green.

## Preserve API contracts

For an externally consumed endpoint, library, CLI, event, or data contract, default to preserving the existing interface while refactoring internals. An ordinary behavior-preserving refactor does not require a new version or a repeated approval question.

If the requested result requires a contract change or the user wants v1 frozen, resolve the versioning choice before those changes; consult [api-versioning.md](../../references/api-versioning.md). Honor an existing choice:

- **Preserve v1:** protect the public contract with tests and refactor behind it.
- **Side-by-side v2:** keep v1 production files untouched, use the repository’s versioning mechanism, and retain v1 tests. Do not deprecate or redirect v1 or modify it for code sharing without authorization.

## Choose and apply the smallest useful change

For each change, identify the observed friction, smallest transformation, protecting check, and effect on navigation. Consult [refactoring-heuristics.md](../../references/refactoring-heuristics.md) when choosing a transformation.

Prefer renaming and simplifying local control flow before extracting or moving logic. Consolidate duplicated responsibilities only when sharing improves locality. A new abstraction must remove more complexity than its files, interfaces, and navigation add; existing variation or coupling must justify it.

Work in small coherent batches. Inspect the diff and run focused checks after each batch. Correct or revert a new regression without discarding unrelated changes. Avoid wholesale rewrites unless requested and adequately protected.

Do not alter validation, authorization, transactions, errors, logging, serialization, accessibility, or trust-boundary behavior as a simplification shortcut. Do not add dependencies, wrappers, interfaces, or extension points without a demonstrated need.

## Verify and report

Use [verification-and-reporting.md](../../references/verification-and-reporting.md) for the final review. Run required checks for the touched surface and broaden coverage when shared behavior or compatibility risk warrants it. Reuse evidence for unchanged state; rerun after relevant changes or unresolved failures.

Compare against the baseline. Check the diff for contract changes, changed defaults or side effects, weakened tests, unrelated edits, and unjustified abstractions. Under side-by-side v2, verify v1 production files remain untouched.

Report the main readability improvement, retained behavior, verification results, and any pre-existing failures or unverified risks. State API strategy only when relevant. Test and runtime evidence support compatibility claims; visual inspection alone does not prove equivalence.
