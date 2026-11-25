---
name: testing-flaky
description: "Diagnosing and fixing flaky tests: the usual causes (async waits, shared state and order, time and time zones, randomness, network, leaked resources, parallel races, animations), how to reproduce them with repeats, random order and stress, the fixes for each, and quarantining with an owner instead of silent retries or sleeps. Read when a test passes and fails without code changes."
---

# Flaky tests: find the cause, fix the cause

The usual reaction to a flaky test is a retry, a longer timeout or a
`sleep(500)`. The suite slowly becomes a slot machine people rerun until it
pays out, and some of those flaky tests were right: they had found a race
that users hit too. This skill: measure the flake, reproduce it with
repeats, random order and stress, recognise the cause, apply the fix for
that cause, and quarantine with an owner when it cannot be fixed today.
Principles in `testing`; reproducing reported bugs in `testing-reproduce`.

## 1. Measure it first

- Confirm it is flaky, not broken: the same commit both passes and fails.
  Check the CI history of that test (the flaky list in Playwright's report,
  retried tests in JUnit XML, the CI's test analytics).
- Rerun it many times, alone and with its file and suite, and write down the
  rate. A test failing 1 run in 50 needs about 150 runs to fail about three
  times.
- The same arithmetic decides when it is fixed: after a 1-in-50 flake, 150
  clean runs still leave about a 5% chance it is there; 300 clean runs,
  about 0.2%.

| Runner | Repeat | Random order | More pressure |
|---|---|---|---|
| Playwright | `--repeat-each=50 --retries=0` | not built in | `--workers=8` |
| Vitest | `--repeats=50` | `--sequence.shuffle`, `--sequence.seed=<n>` | `--maxWorkers=8` |
| Jest | a shell loop | `--randomize --seed=<n>` (within a file) | `--maxWorkers=8` |
| pytest | `--count=50 -x` (pytest-repeat) | pytest-randomly, active once installed: `--randomly-seed=<n>` or `last` | `-n 8` (pytest-xdist) |
| Go | `-count=100` | `-shuffle=on`, replay with `-shuffle=<seed>` | `-race -parallel 16 -cpu 1,4` |
| Rust (nextest) | `--stress-count 100` | each test runs in its own process | `-j 16` |
| JUnit | `@RepeatedTest(100)` | `junit.jupiter.testmethod.order.default = org.junit.jupiter.api.MethodOrderer$Random` | `junit.jupiter.execution.parallel.enabled = true` |
| RSpec | a shell loop | `--order random --seed <n>`; `--bisect` finds the polluter | `parallel_rspec` (parallel_tests) |

## 2. Causes and fixes

| Cause | How it shows | Fix |
|---|---|---|
| Waiting a fixed time | passes on a fast laptop, fails on busy CI | wait for the condition: web-first assertions, `expect.poll`, `vi.waitFor`, Awaitility, testify `assert.Eventually`; fake timers for timer logic |
| Shared state | fails only after certain other tests | reset in teardown: `restoreMocks`, `monkeypatch`, `t.Setenv`, `t.Cleanup`; no module-level caches or singletons carrying data; fresh database state per test |
| Order dependence | passes alone, fails in the suite, or the reverse | run in random order; find the polluter (`rspec --bisect`, `detect-test-pollution --failing-test <id> --tests tests/`); fix its cleanup and make the victim set its own preconditions |
| Time | fails near midnight, at month end, on DST days, or only in CI (UTC) | inject or freeze the clock; set `TZ` for the suite; add a deliberate job in another zone |
| Randomness | random data sometimes hits an edge (an empty string, a duplicate unique value) | seed and print the seed; sequences or UUIDs for unique fields; explicit values where the test depends on them |
| Network | DNS errors, third-party timeouts, web fonts late in screenshots | fake at the network edge; block real network in tests (`testing-integration`) |
| Leaked resources | `EADDRINUSE`, open handles, stray timers or goroutines, exhausted connections | port 0 (the OS picks); close everything in teardown; `jest --detectOpenHandles`, `vitest --detectAsyncLeaks`, `goleak.VerifyTestMain(m)` |
| Parallel workers colliding | the same row, file, queue, bucket or port used by two workers | per-worker resources: `worker_id` (pytest-xdist), `testInfo.workerIndex`, `JEST_WORKER_ID`, `VITEST_POOL_ID`; unique names |
| A race in the code | fails under load or with `-race` | the race detector and a stress loop; fix the code (transaction, lock, `SELECT ... FOR UPDATE`, unique constraint, idempotency key), not the test |
| A promise not awaited | an assertion after the test ended; an error blamed on the next test | await or return every promise; lint with `@typescript-eslint/no-floating-promises` |
| UI in motion | clicks land on a moving element; a toast covers the button; content loads late | `reducedMotion: "reduce"` honoured by the app; web-first assertions; wait for the state the user waits for |
| Eventual consistency | a search index, replica, cache or queue not yet updated | poll for the condition with a timeout; refresh or drain explicitly in the test |
| Tight timeouts | times out only on slower CI machines | measure durations, remove the slowness; `test.slow()` for a known slow test; never raise the global timeout to hide it |
| Dirty environment | leftovers from a previous run: containers, files, caches | clean checkout in CI, Testcontainers' reaper, unique names per run |
| Locale and ICU | sorting or number formats differ between the CI image and a laptop | a fixed locale for the suite; explicit locales in `Intl` and collation calls |

## 3. Reproducing it

- Loop the single test, then its file, then the suite in random order with
  parallel workers, then under pressure: fewer CPUs (`docker run --cpus=1`),
  more workers, Go's `stress` tool on a compiled test binary
  (`testing-reproduce`, section 6).
- Recreate CI: the same image (the CI's container, the Playwright Docker
  image), `TZ` and `LANG`, parallelism, and environment variables (`CI=true`
  changes how Vitest writes snapshots and how Playwright configs behave).
- Take the artefacts of the failing run: logs, traces, screenshots, JUnit
  XML, the printed seeds. Replay the seed before guessing.
- Add evidence where the wait happens: timestamped logs, the state observed
  at failure (the DOM, the rows), not only "expected true, got false".

## 4. What the fixes look like

```ts
// Flaky: races the save request.
await page.getByRole("button", { name: "Save" }).click();
await page.waitForTimeout(1000);
expect(await page.getByText("Saved").isVisible()).toBe(true);

// Stable: retries until the message appears, up to the expect timeout.
await page.getByRole("button", { name: "Save" }).click();
await expect(page.getByRole("status")).toHaveText("Saved");
```

```ts
// Timer logic on fake time: no real waiting, no race with the clock.
beforeEach(() => { vi.useFakeTimers({ now: new Date("2026-09-29T10:00:00Z") }); });
afterEach(() => { vi.useRealTimers(); });

it("retries once after the backoff", async () => {
  const call = vi.fn().mockRejectedValueOnce(new Error("503")).mockResolvedValue("ok");
  const result = withRetry(call, { backoffMs: 2_000 });

  await vi.advanceTimersByTimeAsync(2_000);

  await expect(result).resolves.toBe("ok");
  expect(call).toHaveBeenCalledTimes(2);
});
```

```go
// Go 1.25: time inside the bubble is fake and moves only when every goroutine waits.
func TestCacheExpires(t *testing.T) {
	synctest.Test(t, func(t *testing.T) {
		c := NewCache(time.Minute)
		c.Set("k", "v")

		time.Sleep(61 * time.Second) // returns at once

		if _, ok := c.Get("k"); ok {
			t.Fatal("entry still present after its TTL")
		}
	})
}
```

```python
# Unique per test, so parallel workers and reruns never collide.
email = f"user-{uuid4().hex}@example.test"
```

## 5. Quarantine, with an owner

When the cause cannot be fixed today, quarantine the test instead of
retrying it into green, skipping it quietly or deleting it:

- Tag it and exclude the tag from the required suite; run the quarantined
  tests in a job that does not block merging, so their rate stays visible.
- Open an issue with the evidence, an owner and a deadline (two weeks is
  common). At the deadline it is fixed, or deleted with the behaviour it
  covered tested some other way.

| Runner | Mark | Required suite | Quarantine job |
|---|---|---|---|
| Playwright | `test("...", { tag: "@quarantine" }, ...)` | `--grep-invert @quarantine` | `--grep @quarantine` |
| Vitest 5 | `{ tags: ["quarantine"] }`, declared in `test.tags` | `--tagsFilter '!quarantine'` | `--tagsFilter quarantine` |
| pytest | `@pytest.mark.quarantine`, registered in `markers` | `-m "not quarantine"` | `-m quarantine` |
| Go | `t.Skip("quarantined: #1234")` unless `RUN_QUARANTINED` is set | default | `RUN_QUARANTINED=1 go test ./...` |
| Rust | `#[ignore = "quarantined: #1234"]` | default | `cargo nextest run --run-ignored only` |
| JUnit | `@Tag("quarantine")` | Gradle `excludeTags("quarantine")`, Surefire `excludedGroups` | `includeTags("quarantine")` |
| RSpec | `it "...", :quarantine do` | `--tag ~quarantine` | `--tag quarantine` |

A skip without an issue and an owner is deleted coverage that nobody knows
is gone.

## 6. Retries detect; they never hide

- CI may retry a failed test once or twice, as long as a pass on retry is
  reported as flaky and tracked: Playwright's flaky category and
  `--fail-on-flaky-tests`; nextest's `retries` with `--flaky-result fail`;
  pytest-rerunfailures `--reruns 1` with `--fail-on-flaky` (exit code 7);
  Jest `jest.retryTimes(1, { logErrorsBeforeRetry: true })`; gotestsum
  `--rerun-fails --rerun-fails-report`; Gradle's test-retry plugin with
  `failOnPassedAfterRetry`; Surefire `rerunFailingTestsCount`, which lists
  "Flakes".
- Once the suite is clean, make flaky passes fail the run, so a new flaky
  test is caught the day it arrives.
- Never retry inside the test code (a loop around the assertion, a caught
  exception), never raise timeouts until green, never add retries to make a
  release go out.

## 7. The bug a flaky test reveals

- Before blaming the test, ask whether a user can hit the same thing: a
  double submit creating two payments, an update lost between two requests,
  stale data after a save because the read went to a replica or a cache, an
  event handled before the row it refers to was committed.
- If yes, the test was right: fix the code (a unique constraint, an
  idempotency key, a transaction, reading your own writes), keep the test,
  and add a direct test for the race (`testing-integration`, section 7).
- Report the cause class, the evidence and the numbers: "failed 7 of 200
  before, 0 of 1,000 after".

## Check it

- The loop passes for several times the runs it took to fail before (the
  numbers in section 1), in random order and with parallel workers.
- The fix removed the cause: the diff adds no sleep, no longer timeout and
  no retry.
- Quarantined tests carry a tag, an issue, an owner and a deadline, and run
  in a visible non-blocking job.
- The report names the cause and gives the before and after rates.

## Avoid

Sleeps and longer timeouts as fixes; retries inside test code; raising CI
retries; `skip` without an issue; deleting a test without covering its
behaviour; assuming the test is wrong when users can hit the same race;
"works on my machine" without recreating CI; declaring a flake fixed after
one green run.
