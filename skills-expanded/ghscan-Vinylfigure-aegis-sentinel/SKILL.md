---
name: verdict-path-review
description: Review checklist for any PR touching CODEOWNERS-protected verdict-path files (src/verdict.py, evidence.py, db.py, probe.py, completeness.py, controls/, jit/, oscal/, schemas/, seeded fixtures). Use when reviewing a PR, when the user says "review this", or before approving any Replit Agent output that touches these paths.
---

# Verdict-path review

The review gate confers the safety; the tool that typed the code does not. A collector written by Replit Agent and reviewed here is exactly as trustworthy as one written by hand. Review is line-by-line for these paths — no skimming, no "tests pass so it's fine".

Work through every item; report each as OK / VIOLATION / N-A with a one-line justification.

## Determinism and independence

1. No AI client or `src.agents` import anywhere in the diff's verdict-path files. (The purity test enforces the import; you are checking for the sneakier version — verdict logic that branches on data an agent produced.)
2. No verdict is produced, revised, or influenced by anything non-deterministic: no clock-dependent pass criteria beyond declared tolerances, no randomness, no network reads inside `evaluate()`. Pure function in, pure function out.
3. New src modules are registered in `tests/test_verdict_path_purity.py::VERDICT_PATH_FILES` and `.github/CODEOWNERS`. The registration test fails otherwise — but confirm the registration is deliberate, not reflexive.

## Honesty of absence

4. Every path that fails to observe state emits UNKNOWN with a D-7 cause family — never PASS by default, never a guessed FAIL. Grep the diff for `except` blocks and 404 handling; each must route through `src/probe.py` semantics or produce UNKNOWN(basis_missing).
5. Partial collection cannot reach per-record verdicts: completeness assertions (`src/completeness.py`) run before evaluation, and their failure aborts to population-level UNKNOWN. Exit-code-4-style "partial but continuing" is a VIOLATION wherever it appears.

## Schema and fixture guardrails

6. If a schema changed: no loosening. Every `tests/fixtures/*/invalid/` case must still be rejected; a schema change that makes an invalid fixture pass is a VIOLATION even if all tests were "fixed" to match. `additionalProperties: false` and const-pinned `schema_version` remain.
7. Every new or changed `evaluate()` has a seeded-failure fixture that the changed code detects, and `TEST_FUNCTION_VERSION` is bumped on behaviour change (an assessor must be able to say which function version judged which record).

## Integrity machinery

8. Changes to `src/evidence.py` hashing/chain logic: reject unless accompanied by a corpus-cited rationale — canonicalization changes silently orphan every existing record_hash.
9. `src/db.py`: ledger stays INSERT+SELECT-only for the app role; no new UPDATE/DELETE grants; ratification gate (`assert_baseline_ratified`) still called at run start.
10. `src/jit/preconditions.py`: all preconditions still run (no short-circuit that hides subsequent denials — every failed check is evidence); AM-05 attributes A-E each still enforced; TTL cap and replay window unchanged unless ratified.
11. `src/oscal/`: exporter still filters to result|ratification; UNKNOWN still maps to not-satisfied + unknown-cause; F-7 test untouched.

## Process

12. The PR is not self-approved by its author, and this review is recorded in the PR (paste the checklist verdicts). For emergency merges, CM-04 applies: approval within 24h, evidence retained.

If any item is VIOLATION: request changes with the corpus citation (see `docs/corpus-index.md` for which doc to cite). Do not approve with TODOs on verdict-path items.
