# clipgen-test-perf — Keep new tests off the critical path

The suite runs on every `/check` and every push, so a slow test is a tax on all future
work. It has twice been paid at absurd rates: one test file took the CI step from 52 s to
565 s (`81ae6471`), and three tests spent 8.1 s of a 29.2 s suite blocked on waits whose
release provably never fired (`6f13f26d`). Neither was caught by review, because **a slow
test looks exactly like a correct test**.

Run this when you add or modify a test, and whenever `/check` feels slower than it did.

## Step 1 — Measure, twice

```bash
uv run --extra dev pytest -c tests/pytest.ini -p no:randomly --durations=20
```

`-p no:randomly` fixes the order so two runs are comparable. **Run it twice and only trust
what reproduces.** A one-off 6.79 s reading sent a previous pass chasing
`test_combined_server_forces_non_interactive`, which is 0.10 s; the real offenders sat
below it in the same list. Durations under ~0.1 s are noise.

To compare against the parallel shape CI actually runs (`-n 4` matches GitHub's core count):

```bash
uv run --extra dev --with pytest-xdist pytest -c tests/pytest.ini -p no:randomly -n 4
```

Reference points as of `6f13f26d`, for judging whether a number is anomalous: ~2400 tests,
**~20 s serial**, **~6.4 s at `-n 4`**, ~34 s for the CI step. The runners are ~4× slower
than a dev Mac, so multiply local `-n 4` by ~4 to predict CI. The slowest legitimate test is
~1 s and it runs real OCR. These drift with every PR — re-measure rather than trusting
them; what matters is the *shape* (nothing should stand out from the tail).

## Step 2 — Budget

| Test does | Acceptable |
|---|---|
| Pure logic, parsing, dict/JSON shaping | < 20 ms |
| Flask route via `client`, manifest round-trip | < 100 ms |
| Scans `assets/web` or `source/` source text | < 100 ms, and **one** pass (see C) |
| Spawns real ffmpeg / OCR / an HTTP stub server | up to ~1 s, needs to be genuinely necessary |
| Anything else over 0.3 s | Justify it in a comment or fix it |

A new test that lands in `--durations=20` at all deserves a second look.

## Step 3 — Diagnose against the four known patterns

### A. A wait whose release can never fire

**Tell:** the duration is suspiciously round and matches a timeout constant in the test —
2.00 s, 4.02 s (= 2 batches × 2 s).

Do not reason about it; **print timestamps** at every block, release, and test-thread step,
run with `-s`, and read the ordering. All three instances in `6f13f26d` showed the release
was unreachable: workers blocked on `proceed.wait(timeout=2)` while `proceed.set()` sat after a
`resp.close()` that itself blocks draining the pool. The trace showed all four workers
timing out and the `set()` never mattering.

**Two traps that produced these:**

- **`client.post()` buffers.** Werkzeug's test client does *not* iterate a streaming body in
  the background. It returns having buffered the first chunk; `resp.data` drains the rest.
  Two tests carried comments claiming the opposite and were built on it.
- **A mock must release on the call production actually makes.** One test unblocked a
  blocked `readline()` from `resp.close()`, but `_shutdown_response_socket` documents that it
  must *not* call `close()` (it races the blocked reader) — it shuts the socket down. So the
  cancel watcher could never wake the read, and the test only ever finished by expiring its
  own timeout, never once proving that cancellation interrupts a read.

**Fix:** release on the real mechanism (`sock.shutdown`), or if nothing on the test thread
can signal in time, use a small explicit hold and say why. Then go to Step 4 — this fix
class is the one that silently guts a test.

### B. Per-item regex over a whole corpus

**Tell:** a source-scanning test taking seconds. `for name in names: re.findall(rf"\b{name}\b", corpus)`
is O(names × corpus): 2056 names over 4 MB cost **69 s a call**.

**Fix:** one tokenizing pass, then dict lookups.

```python
tokens = Counter(re.findall(r"\w+", corpus))  # once
dead = {n for n in names if tokens[n] == 1}  # lookups
```

1024× here. `\bname\b` and "is a whole `\w+` token" are equivalent *for names made only of
`\w` characters* — so before switching, **prove it on the real corpus**: assert the per-name
counts agree for every name, not just at the threshold you branch on. Keep the slow path for
names the equivalence does not cover (a `$` in a JS identifier breaks it).

### C. A pure helper called by several tests, uncached

**Tell:** N tests in one file each cost the same conspicuous amount. Three tests × 69 s.

**Fix:** `@cache` on the helper. Always safe when it is pure over files that cannot change
mid-run and callers only read the result — check that no test mutates what it returns.

### D. A real production interval left real

**Tell:** duration is a multiple of a constant in `source/`, e.g. `_START_POLL_INTERVAL = 0.5`.

**Fix:** `monkeypatch.setattr(mod, "_START_POLL_INTERVAL", 0)`. The loop is under test, not
the spacing.

## Step 4 — Prove you did not make the test vacuous

Every wait you shorten was nominally buying a state window ("a worker is still in flight",
"the cancel lands mid-run"). Cutting it can leave a test that passes while asserting
nothing — strictly worse than a slow test, and this repo's most damaging failure class
(see [CODE-REVIEW.md](../../CODE-REVIEW.md) *Failure paths*).

So for each one:

1. **Assert the window actually held**, don't assume it.

   ```python
   assert in_flight_at_disconnect >= 1, (
       "no worker was still in flight when the client disconnected; "
       f"raise HOLD_SECONDS ({started_count[0]} started, {finished_count[0]} done)"
   )
   ```

   Same shape for a mock: `assert resp.fp.raw._sock.shutdown.called` pins that the watcher
   reached the real interrupt, so a broken watcher fails instead of quietly costing 2 s again.

2. **Mutation-test that assertion.** Set the hold to `0` and confirm it fires with a useful
   message; inject a dead function and confirm the scan still reports `file:line`. An
   unverified guard is not a guard.

3. **Prefer a loud failure to a timing margin.** Where a shortened test depends on behaviour
   you do not fully control, check that the mechanism breaking makes the test *red* rather
   than silently weaker, and record that in the comment.

## Step 5 — Flake-check, then state the numbers

```bash
for i in 1 2 3 4 5 6 7 8; do uv run --extra dev pytest -c tests/pytest.ini <the tests> -q || echo FAIL; done
uv run --extra dev --with pytest-xdist pytest -c tests/pytest.ini -n auto   # shuffled order, 3x
```

Timing fixes are exactly the ones that flake under load and under `pytest-randomly`'s
shuffle. Run the touched tests repeatedly and the whole suite shuffled, then quote
before/after in the commit — a perf claim with no number is not reviewable.

## Not a test problem: the coverage backend

If the whole step is slow rather than one test, check the measurement, not the tests.
CI sets `COVERAGE_CORE=sysmon` (`.github/workflows/tests.yml`) so coverage uses PEP 669
`sys.monitoring` instead of the `sys.settrace` C tracer — ~70 % less overhead for identical
numbers (verified: 20377 statements, 4397 missed, 78.42 % on both). Needs Python 3.12+ and
coverage 7.4+. If coverage totals ever shift, that env var is the first thing to drop; it
only selects a backend.
