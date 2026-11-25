---
name: testing-reproduce
description: "Turning a bug report into a failing test: gathering the facts, reproducing locally, shrinking the input, choosing the lowest level that shows the bug, git bisect for regressions, catching intermittent failures with loops, confirming the fix makes the test pass and that the test fails without it, and naming it for the behaviour. Read before fixing a reported bug."
---

# From bug report to failing test

The naive fix: read the report, guess the cause, change the code, see nothing
obviously broken, ship. Half the time the guess was wrong, or right for a
different case, and the bug returns months later because nothing pins it.
This skill: facts first, a reproduction, the smallest input that still
fails, a failing test at the lowest level that shows it, the root cause, and
proof in both directions. Principles are in `testing`; tests that fail only
sometimes without a code change are in `testing-flaky`.

## 1. Collect the facts

- **Where**: the version, deployed commit or app build where it happens,
  and the last one where it did not, if it is a regression.
- **Input**: the exact request, file, record, query string, and the shape of
  the data involved (not the personal data itself).
- **Steps**: numbered, from a known starting state.
- **Environment**: OS, browser and version, device, locale, time zone,
  feature flags, configuration, the account's role and plan, data volume.
- **Evidence**: the error message and stack trace, log lines found by
  request id and timestamp, the error tracker's event (release, tags,
  breadcrumbs), a screenshot or HAR file.
- **Expected and actual**, one sentence each, and **frequency**: always,
  sometimes (how often), since when.

Look before asking: the issue, the error tracker, the logs for that request
id, the deploy history. Ask the reporter (with `ask` where available) only
for what blocks reproduction, as a specific question: "Which time zone is
the account set to?", not "Can you give more details?".

## 2. Reproduce in the same conditions

- The same commit (`git switch --detach <sha>`), configuration and flags.
- The same data, built with factories to the reported shape (`testing-data`);
  never production records copied into the repository.
- The same time zone, locale and clock: `TZ=America/New_York`,
  `LANG=de_DE.UTF-8`, time frozen at the reported moment.
- The same client: the browser engine (a Playwright WebKit project for
  Safari), the device, the app version.
- The fastest path first: call the function, then the endpoint with curl or
  the test client, then the UI.
- Keep the reproduction as a command or script: it becomes the test.
- Cannot reproduce? Change one condition at a time (zone, locale, data size,
  concurrency, browser, version), compare your environment with the report,
  read the logs for the actual input. Report what was tried. A fix for a
  bug never reproduced is a guess: say so, and add logging or an assertion
  that will catch it next time.

## 3. Shrink the input

- Delta debugging by hand: remove half of the input (rows, fields, steps,
  flags, files). Still fails: keep the smaller one. Passes: try the other
  half. Repeat until nothing more can go.
- Tools: shrinkray (reduces any file against a script that says whether it
  still fails), C-Vise for source files, and the shrinking of property-based
  tools: write the property the bug breaks and let Hypothesis or fast-check
  find the minimal failing input (`testing-unit`).
- The minimal case often names the cause: "fails only when the name ends in
  a combining accent", "only for the 25-hour day".

## 4. The failing test, at the lowest level

| Where the bug lives | Level |
|---|---|
| A calculation, parsing, formatting, a state transition | Unit |
| A query, a constraint, a transaction, serialisation, a call to another service | Integration, with a real database and a faked HTTP edge |
| Two requests racing (double submit, stock, balances) | Integration, with concurrent requests |
| Only in the browser (focus, a race between screen and API, state across pages) | End to end, and look for a lower test too |

- The test states the expected behaviour, not the bug: name it
  `includes_the_last_hour_when_clocks_go_back`, not `test_bug_4812`; link
  the issue in a comment or annotation.
- Run it before touching the code: it must fail with the reported symptom
  (the same wrong value or error). A different failure means the test is
  wrong, or you found another bug.
- It lives with the related tests, in the project's style.

```python
@pytest.mark.parametrize(
    ("tz", "day"),
    [("Europe/London", date(2026, 10, 25)), ("America/New_York", date(2026, 11, 1))],
)
def test_daily_report_includes_the_last_hour_when_clocks_go_back(tz, day, make_order):
    # Regression for #4812: orders after 23:00 local were dropped on the 25-hour day.
    late = make_order(placed_at=datetime.combine(day, time(23, 30), ZoneInfo(tz)))

    report = daily_report(day, tz=tz)

    assert late.id in report.order_ids
```

## 5. Regressions: `git bisect`

When it worked in an older version, let git find the commit:

```bash
git bisect start
git bisect bad HEAD              # or the first release tag that fails
git bisect good v2.3.0           # a version where it worked
git bisect run ./repro.sh        # or mark each step by hand: git bisect good | bad | skip
git bisect log > bisect.log      # the record, for the report
git bisect reset                 # back where you started
```

The script's exit code decides each step: 0 good, 1 to 127 bad (except
125), 125 skip (this commit cannot be tested), anything else aborts.

```bash
#!/usr/bin/env bash
# repro.sh: keep it and the test outside the working tree; bisect checks out other commits.
npm ci --silent || exit 125                      # does not build: skip this commit
cp /tmp/repro/discount.repro.test.ts src/
npx vitest run src/discount.repro.test.ts
status=$?
rm -f src/discount.repro.test.ts
[ "$status" -ge 128 ] && exit 1                  # a crash counts as bad instead of aborting
exit "$status"
```

- Run the script by hand on the known good and bad commits first: a typo
  that exits 127 marks every commit bad.
- About log2(N) steps: 1,000 commits take about 10.
- `git bisect start --first-parent` steps over merge commits only; then
  bisect inside the pull request it names.
- Performance regressions: `git bisect start --term-old=fast --term-new=slow`
  with a script that times the operation against a threshold.
- The first bad commit shows where the behaviour changed. Read its diff for
  the cause; do not revert it blindly.

## 6. Intermittent failures

Run it in a loop until it fails, and count the runs:

```bash
for i in $(seq 1 200); do npx vitest run src/queue.test.ts > /tmp/run.log 2>&1 || { echo "failed on run $i"; break; }; done
pytest tests/test_queue.py --count=200 -x -p no:randomly      # pytest-repeat
go test ./queue -run 'TestDrain$' -count=500 -race -failfast
cargo nextest run drain --stress-count 200
npx playwright test e2e/checkout.spec.ts --repeat-each=50 --retries=0
```

- Add pressure to expose races: more workers (`-n 8`, `--workers=8`,
  `-parallel 16`), fewer CPUs (`docker run --cpus=1`), or Go's stress tool:
  `go install golang.org/x/tools/cmd/stress@latest`, then
  `go test -c -race -o queue.test ./queue && stress ./queue.test -test.run=TestDrain`.
- Replay seeds: the order seed (`go test -shuffle=<seed>`,
  `pytest --randomly-seed=<seed>`, `vitest --sequence.seed=<seed>`,
  `rspec --seed <seed>`) and any data or property seed the failure printed.
- Order-dependent? Find the test that pollutes: `rspec --bisect`,
  `detect-test-pollution --failing-test tests/test_a.py::test_x --tests tests/`.
- Capture more while looping: timestamps in milliseconds, thread or
  goroutine ids, the race detector (`-race`), the state at the moment of
  failure. Causes and fixes are in `testing-flaky`.

## 7. The root cause, not the symptom

- Ask why until the answer is a decision in code or data: the total is wrong,
  because rounding happens per line, because the line model rounds on
  assignment, because the amount is stored as a float.
- Fix it where the cause is (the float), not where it shows (a `Math.round`
  in the view).
- Look for siblings: search for the same pattern or helper elsewhere; add
  their cases to the test table, or list them in the report.
- Keep the fix small. A refactor mixed into a bug fix makes both hard to
  review.

## 8. Prove it both ways

1. The test fails before the fix; keep the output.
2. With the fix, it passes.
3. Undo only the fix (`git stash push -- src/report.py`, the fixed files and
   not the test), run the test: it fails again. Restore (`git stash pop`).
4. Run the related tests, then the whole suite.
5. Intermittent bugs: loop again with several times the runs it took to
   fail. Failing within 40 runs before and 200 clean runs after is evidence;
   one green run is not.

## 9. Report

```
Cause: daily_report() built the day as [midnight, midnight + 24h); the day clocks go
       back has 25 hours, so orders after 23:00 local fell outside (report.py:88).
Fix:   the range ends at the next local midnight, computed in the report's zone.
Proof: tests/test_report.py::test_daily_report_includes_the_last_hour_when_clocks_go_back
       fails before (order missing), passes after; fails again with the fix reverted.
       pytest -q: 614 passed.
Not checked: other reports using the same helper (listed in #4815).
```

## Check it

- The test fails for the reported reason without the fix and passes with it,
  and you saw both.
- Its name states the behaviour; a comment links the issue.
- It sits at the lowest level that shows the bug.
- The full suite passes; for an intermittent bug, the loop count is in the
  report.

## Avoid

Fixing before reproducing; a test that already passes before the fix; an
end-to-end test where a unit test shows the bug; tests named after tickets;
reverting the first bad commit without reading it; a retry, a sleep or a
longer timeout as the fix; declaring an intermittent bug fixed after one
run; production personal data in the reproduction; asking the reporter for
"more details" without saying which.
