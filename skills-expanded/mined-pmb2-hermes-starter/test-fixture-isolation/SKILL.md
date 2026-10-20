---
name: test-fixture-isolation
description: Prevent test fixture data drift by decoupling tests from live/production data files. Covers dedicated fixture creation, conftest path management, and verification patterns.
version: 1.0.0
author: Hermes Agent (Sentry)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [testing, fixtures, data-drift, isolation, conftest, qa-lead]
    triggers:
      - test fixture data drift
      - live data in tests
      - conftest references live data
      - test_open_loops failure
      - fixture isolation
      - data fixture hardening
    related_skills: [codebase-hardening, windows-cross-platform-debugging]
---

# Test Fixture Isolation

Prevent tests from breaking when live data files change. The canonical symptom:
a `conftest.py` fixture copies a live JSON/YAML/SQLite file into a temp directory,
and tests assert against hardcoded IDs or counts. When the live data gains a new
record, the test fails — even though the code under test is correct.

## When to Use

- A test fails because live data gained a new record, changing expected IDs
- `conftest.py` uses `shutil.copy2(LIVE_FILE, temp_path / ...)` for test data
- The live data file and test expectations are coupled, causing drift failures
- You see assertions like `assert "OL-004" in result.stdout` failing because
  the live data now has OL-004 (so the next generated ID is OL-005)
- **A test fails on hosts with real configured credentials (credential pools,
  auth stores, provider env vars) but passes in clean CI** — see the
  "Ambient-State Variant" section below
- **A monkeypatched dependency never fires, yet the function returns a value
  only a different code path could produce** — an earlier code path consumed
  ambient state before reaching the code under test

## Fix Pattern

### Step 1 — Create a Dedicated Test Fixture

Create `tests/fixtures/<name>-test-seed.<ext>` with a stable set of test data
matching your test docstring expectations:

```json
{
  "metadata": {
    "description": "Test fixture — three seeded loops",
    "created": "2026-05-29",
    "version": 1
  },
  "loops": [
    {"id": "OL-001", "status": "open", "priority": "critical", "category": "Technical"},
    {"id": "OL-002", "status": "open", "priority": "critical", "category": "Finance"},
    {"id": "OL-003", "status": "closed", "priority": "high", "category": "Business Development"}
  ]
}
```

### Step 2 — Update conftest.py

Point the fixture variable at the test seed file instead of the live data:

```python
# Before (live data — drifts)
OPEN_LOOPS_SRC = PROJECT_ROOT / "04-shared-memory" / "playbooks" / "open-loops.json"

# After (test fixture — stable)
OPEN_LOOPS_SRC = PROJECT_ROOT / "tests" / "fixtures" / "open-loops-test-seed.json"
```

### Step 3 — Verify

```bash
# Targeted test suite
pytest tests/test_open_loops.py -v -q

# Full suite — other tests may share the same conftest fixture
pytest tests/ -q
```

### Step 4 — Confirm Live Data Unchanged

Verify the real data file is untouched (still has all its records):

```bash
python -c "import json; d=json.load(open('path/to/live/file.json')); print(f'{len(d[\"loops\"])} records')"
```

## Verification

After applying the fix, run this ad-hoc check:

1. The fixture file exists with the expected number of records
2. The fixture IDs/statuses match test docstring expectations
3. conftest.py no longer references the live data file path
4. The live data file still has all its records (not accidentally modified)
5. Full test suite passes

## Pitfalls

- **Match docstring expectations precisely** — the test docstring describes the
  fixture state. Your seed data must match those descriptions exactly (IDs,
  statuses, priorities, deadlines).
- **Check schema parity** — the fixture schema must match the live file's schema.
  Same fields, same nesting, same required/optional distinctions.
- **Re-run the full suite** — other test files may share the same conftest
  fixture. A fixture swap affects all consumers.
- **Do not commit the live file as the fixture** — it WILL drift again.
- **Name clearly** — use `tests/fixtures/<name>-test-seed.<ext>` naming to
  distinguish test fixtures from production data.
- **Document in PULSE.md** — record which fixture was created and why, so future
  pulses understand the change.

## Ambient-State Variant — Real Credential Stores Short-Circuit the Code Path Under Test

Same class of bug as live-data drift, but the ambient state is **credentials,
not files**: resolution-chain code consults the environment (credential pools,
auth stores, config, provider env vars) BEFORE reaching the code path under
test. On a host with real credentials, that earlier path legitimately returns a
result, the mock set up for the target path is never invoked, and the test's
premise (e.g. "credentials fail → fall through") never happens. The TEST is
environment-dependent — the production code is fine.

### Diagnostic ladder (before touching anything)

1. **Run the test in isolation.** Still fails → deterministic, not order-dependent.
2. **Instrument the mock** (print at entry). Mock never fires but the function
   returns a value only the target block can produce? A different path returned
   first. Grep for the distinctive returned value (e.g. `source="qwen-cli"`) to
   locate the actual returning block — it's usually a literal unique to that path.
3. **Prove the code under test is correct.** Monkeypatch the ambient dependency
   to be EMPTY (e.g. `load_pool` → `SimpleNamespace(has_credentials=lambda: False)`)
   and re-run. If it now passes and takes the expected path, the failure is
   test-environment-dependency, not a code bug.
4. **Check upstream.** `git show origin/main:<test file>` — an identical unfixed
   test upstream means it is NOT a local regression; it's a latent test bug that
   clean-CI environments simply never trip.

### Fix — make the test hermetic

Mock the ambient dependency (empty pool / empty store / clean env) so the
intended code path is forced. The fix belongs in the TEST, never production
code. Re-run the full test file, then the owning commit's full scope, before
committing as a test-only fix.

### Prevention

Tests asserting on resolution/fallback behavior must neutralize ambient state
they don't own: credential pools (`load_pool`), auth stores, `HERMES_HOME`
config, provider env vars. A test that doesn't mock them passes only on hosts
that happen to lack those credentials. Sibling tests in the same file that DO
mock the store are the tell — mirror them.

Full worked example (qwen-oauth fallthrough test, Hermes Agent commit
`a163743ad`, Aug 2026): `references/env-dependent-credential-store.md`.

## Windows Filesystem Timestamp Pitfall — mtime Memoization Serves Stale Data

### The Trap
NTFS updates file timestamps via the cache manager's dirty-metadata flush, NOT
synchronously on write/close. Two `write_text()` calls microseconds apart —
even ~10ms apart — can report the **identical** `st_mtime_ns`. Consequences:
- Any cache/memo keyed on `(path, st_mtime_ns)` serves stale data after a real
  file edit on Windows (a genuine production bug, not just a test artifact).
- Any test that edits a file then re-reads it fails **intermittently** —
  phase-dependent, passes in isolation sometimes, fails others.

### Empirical Probe (run before blaming the memo logic or the test)
```python
p.write_text("{}")
m1 = p.stat().st_mtime_ns
p.write_text("changed")
m2 = p.stat().st_mtime_ns
print(m1 == m2)   # True on NTFS within the flush window
```

### Fix Pattern — key on size too
```python
st = path.stat()
memo_key = (str(path), st.st_mtime_ns, st.st_size)  # size changes instantly on content change
```
One `stat()` call captures both; content change → size change → cache miss,
deterministically — no sleeps, no `os.utime`. Verified 2026-08-01: flaky
`test_honcho_cache_busting_config_memoized_by_mtime` went 3/4-failing →
6/6-passing (Hermes Agent commit `d9d0aeec5`). Full worked example:
`references/ntfs-mtime-memoization.md`.

### Bisect Trap — phase-dependent flakes
A flake that appears to correlate with a specific sibling test file (pair A
fails, pair B passes) can be pure phase coincidence — the suspect test ran
FIRST in the pair (arg order), and its flake rate was independent of any other
file. **Reproduce the suspect test in isolation 5-6 times before concluding
cross-file causation.** A false bisect here wasted several cycles.
