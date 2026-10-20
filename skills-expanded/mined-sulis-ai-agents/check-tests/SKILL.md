---
name: check-tests
description: "Runs the tests and flags anything that used to work but now doesn't."
standards:
  input: [REFERENTIAL_INTEGRITY_STANDARD]
  processing: [CRITICAL_THINKING_STANDARD, DECOMPOSITION_PROCEDURE]
  output: [CRITICAL_THINKING_STANDARD]
verification_spiral:
  tier: standard
  template_base: STANDARD_TIER_DEFAULT
  custom_dimensions:
    - name: "Primitive Coverage Completeness"
      threshold: ">= 4/5"
      standard_reference: "plugins/sulis/skills/codebase-assess/references/primitives.md CQ-02"
      scorer: generating_agent
      evidence_required: "Regression detection (existing) + CQ-02 test coverage quality both have status"
related_skills:
  - relationship: depends_on
    skill: code-health
    notes: invoked as wired tier 3 (Works) in code-health orchestrator
  - relationship: depends_on
    skill: _lib/baseline
  - relationship: depends_on
    skill: _lib/tools
  - relationship: depends_on
    skill: _lib/tools/coverage
    notes: NEW — to be created — covers CQ-02 (pytest-cov / vitest coverage / jest coverage)
---

# Check Tests

The regression check. Runs the test suite (or reads cached results),
compares the pass/fail state to a stored baseline, and reports what
changed. Newly-failing tests are **regressions** — things that worked
before and don't now.

The skill is the foundation for "did our changes break anything?" — the
question every founder asks before shipping.

## Detecting versus running

The skill operates in three modes depending on what's available:

1. **Cached results found** — read existing test-run results from
   conventional locations (`.pytest_cache/`, `test-results.xml`,
   `coverage/`, `jest-results.json`). Compare to baseline. Fast.
2. **No cache, `--run` passed** — detect the test framework, run the
   suite (default 120s timeout; `--timeout N` to override). Compare to
   baseline.
3. **No cache, no `--run`** — report "tests detected (N files, framework=X)
   but not run. Pass `--run` to execute, or your CI's results will be
   read when present." This avoids blocking the founder on a long test
   suite they didn't ask to run.

## How the baseline works

The baseline is a snapshot at `.checkup/{project}/baseline.json` capturing:

- Commit SHA at baseline time
- Per-test signature → pass/fail/skip status
- Framework + version detected

First-run behaviour: no baseline exists, so this run **captures** one and
reports "captured baseline against {SHA}; next run will detect any
regressions against this point." The founder sees this explicitly — never
silent.

Updating the baseline: explicit `--update-baseline` flag. The skill never
silently overwrites; founder consent always required (echo-before-act per
founder-facing-conventions Rule 3).

## Auto-detection of scope

Like check-readability and code-health, this skill auto-detects PR-scope
vs codebase-scope from local git state. In PR-scope, only tests in changed
files are run (where possible — some frameworks don't support per-file
filtering well; falls back to "tests in changed packages" or full suite).
Override with `--scope=codebase` to force full run.

## Two modes

- **Founder mode (default).** Verdict in plain English: "5 tests that
  were passing before are now failing." Lists newly-failing tests
  by founder-readable name (test name + brief description from docstring
  if available).
- **Operator mode (`--raw`).** JSON envelope with full test-signature
  → pass/fail state + delta + framework metadata. Pipe-friendly.

## When invoked

1. **Resolve scope.** Auto-detect PR vs codebase. Echo what was decided:
   *"Checking tests in this branch's changes (12 test files)."*
   or *"Checking the whole test suite (87 test files)."*

2. **Resolve the framework.** Auto-detect from project signals (pytest:
   `pyproject.toml` / `setup.cfg` / `pytest.ini`; jest: `package.json`
   `scripts.test` or `jest.config.js`; go test: any `*_test.go`; etc.).
   If multiple frameworks present, ask which to run (or list them).

3. **Resolve test state.** Try cached results first; if absent and
   `--run` was passed, run; else report detection-only with the "pass
   --run to execute" guidance.

4. **Compare to baseline.** Load `.checkup/{project}/baseline.json` if
   present. Compute:
   - newly-failing (was passing, now failing) → regressions
   - newly-passing (was failing, now passing) → improvements
   - newly-added (didn't exist in baseline) → information
   - newly-removed (existed in baseline, gone) → information
   - flaky (in baseline as one state, here as the other, AND in the
     known-flaky list) → suppress as flaky-not-regression

5. **Present the verdict.** Use this template (omit empty sections):

   ```
   🧪 Test check — {scope description}

   Verdict: {clear / something broke / mostly clear / hard to read}

   Summary: 87 tests · 84 passing · 3 failing
   Compared to baseline at commit a3f2c1d8 (2 days ago).

   ⚠ Newly-failing (regressions) — 2

     • test_user_can_pay (apps/api/tests/test_billing.py)
       Was passing at baseline; failing now.
       Last shipped change touching this code: WP-AUTO-018.
       To investigate: open the test file at line 47.

     • test_signup_sends_welcome_email (apps/api/tests/test_signup.py)
       Was passing at baseline; failing now.
       To investigate: open the test file.

   ✓ Newly-passing (improvements) — 0

   ℹ Test-suite changes — 4 added, 0 removed

   Flaky tests (suppressed from regression report): 1
     (see references/check-tests-known-flaky.md to manage)

   The test suite ran successfully. No code was changed.
   ```

6. **Handle shortcuts** the founder might ask for:
   - **Safe shortcuts:** `[N] open test file`, `[N] show last passing
     commit for this test`, `[u] update baseline to current state` (with
     explicit confirmation prompt because it's mutating shared state).
   - **No fix shortcut.** This skill identifies regressions; it does not
     fix them. Fixing a failing test is a separate engineering action.

## Gotchas

- **First run has no baseline to compare against.** The first invocation
  captures the baseline and reports this explicitly — it never silently
  passes. The second invocation is the first real regression check. Tell
  founders this upfront so they don't expect instant regression output.
  *Source: signature-dedup pattern from sulis-execution's wpx-findings.*

- **Test framework detection brittleness.** Projects with multiple
  frameworks (pytest + jest monorepos), non-standard configs, or custom
  runners can confuse auto-detection. Mis-detection produces wrong test
  runs → false verdicts. Always echo the detected framework before running;
  founder verifies. Override with `--framework`.
  *Source: HD-008's source-discovery brittleness; check-readability's
  PR-scope brittleness gotcha.*

- **Slow test suites block founders.** A 30-minute suite makes the skill
  unusable interactively. Default timeout 120s; if cache exists, read
  from cache (no timeout); `--timeout N` to override; graceful fallback
  to "detected but not run" if timeout exceeded.
  *Source: author-experience — slow CI is a universal frustration.*

- **Flaky tests appear as regressions on every run.** A test that
  passes 90% of the time will flip-flop between baseline and HEAD; each
  run reports it as a regression; founder loses trust. Maintained
  allow-list at `references/check-tests-known-flaky.md` (per-project
  file `.checkup/{project}/known-flaky.md` overrides). Flaky tests
  surface as "flaky" not "regression."
  *Source: sulis-execution's wpx-train has 1 known-flaky concurrency
  test that gets explicitly suppressed in count assertions.*

- **Founder might expect this to FIX failing tests.** Universal
  destructive-action ambiguity. The skill DETECTS; it does NOT fix.
  Fixing a failing test (deciding whether the test or the production
  code is wrong; writing the fix; re-running) is a separate engineering
  action requiring explicit founder consent.
  *Source: check-readability gotcha #5 + code-health gotcha #4 +
  founder-facing-conventions Rule 3 — cross-skill pattern for read-only
  audit skills.*

## Vocabulary

- **regression** — a test that was passing in the baseline and is
  failing at HEAD. The load-bearing concept this skill exists to detect.
- **baseline** — the snapshot of test state at a known-good moment
  (commit SHA + per-test pass/fail status). Stored at
  `.checkup/{project}/baseline.json`. Disambiguates from
  `sea:code-review`'s "mechanical baseline" (a CR-01 pre-lens gate) and
  `sea:probe`'s "baseline-aware" (a secret-detection allowlist). Three
  distinct uses; same word; non-overlapping contexts.
- **test-pass-delta** — the diff of passing/failing tests between
  baseline and HEAD. Three categories: newly-failing (regressions),
  newly-passing (improvements), unchanged.
- **newly-failing** — was-passing-now-failing tests. The regression
  category.
- **newly-passing** — was-failing-now-passing tests. The improvement
  category.
- **test-signature** — the unique identifier for a test across runs.
  Typically `{relative_file_path}::{class_name}::{test_name}` for
  pytest; equivalent for other frameworks. Used so we can compare
  across runs even when test counts change.

## When to invoke this skill

- Founder asks "did my changes break anything?", "did anything that was
  working stop working?", "did the tests still pass?"
- Founder is about to ship and wants regression confidence
- After a merge, an autonomous run, or a refactor — check before moving on
- The `/sulis:code-health` wrapper (tier 3) invokes this when running
  comprehensive checks

## When NOT to invoke this skill

- Founder asks "do my tests cover everything?" — this skill is about
  pass/fail, not coverage. Coverage is a tier 6 (evolves) concern.
- Founder asks "are my tests well-designed?" — test quality is a
  separate skill (planned: `sea:test-audit` per the matrix).
- Founder wants to WRITE new tests — that's a separate workflow.
- Founder wants to FIX failing tests — this skill reports; fixing is
  separate engineering work.
- Operator wants raw test-runner output — run pytest/jest/etc. directly
  for that, or use `--raw` for the JSON envelope.
