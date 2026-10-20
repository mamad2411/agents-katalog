---
name: debug-flaky-tests
description: Diagnoses and fixes non-deterministic test failures at root cause instead of masking them with retries — classify the flake (test-order/shared-state pollution, async timing/sleep races, real-clock/timezone dependence, unseeded RNG, network/IO/external calls, resource leaks, port/temp-dir collisions), reproduce it reliably (loop the test 50–1000×, randomize order with a fixed seed, run in isolation vs full suite to localize), then fix it: inject a fake clock (jest fake timers, `freezegun`, `time-machine`) instead of `Date.now()`, await a condition/`waitFor` instead of `sleep`, seed the RNG and log the seed, isolate state per test (fresh DB transaction-rollback or unique schema/tmpdir per worker, reset globals/singletons in teardown), and pin timezone/locale (`TZ=UTC`, `LC_ALL=C`). Quarantine policy: tag `@flaky`, skip-with-tracking-issue, fix within an SLA, never `retry()` as a permanent fix because retries hide real product races.
when_to_use: A test passes locally but fails in CI, passes alone but fails in the suite, fails ~1 in N runs, or only fails on a specific machine/timezone/order/parallelism — and you need to find the actual source of non-determinism and kill it, not paper over it with a retry. Distinct from write-tests (authoring a correct suite from scratch; this skill repairs an existing test that is already non-deterministic) and async-concurrency-correctness (fixing the real race/locking bug in PRODUCTION code, which a flaky test sometimes legitimately surfaces — this skill decides whether the flake is in the test harness or is a true product race).
---

## When to Use

Reach for this skill when a test's pass/fail result is **non-deterministic** — same code, different outcome:

- "Passes locally, fails in CI" / "green on my machine, red on the runner"
- "Passes when I run it alone, fails inside the full suite" (order/state pollution)
- "Fails about 1 in 20 runs with no code change" (timing/RNG)
- "Only fails at midnight / on the build box / in a different timezone"
- "Only fails when tests run in parallel" (shared port, temp file, DB row)
- "CI added `jest --retry 3` / `flaky-test-handler` and now it's 'green'" (masked, not fixed)

NOT this skill:
- Writing a brand-new test suite, choosing assertions/coverage, structuring fixtures from scratch → write-tests (this skill repairs an *existing* test that is already flaky)
- Fixing the actual data race / missing lock / lost-update in **production** code (the flake may be a true symptom) → async-concurrency-correctness (this skill localizes whether the non-determinism is in the test or the product, then hands a confirmed product race to it)
- Date/TZ/DST arithmetic correctness in product logic (not "the test reads the real clock") → datetime-timezone-correctness
- A CI job that fails for non-test reasons (cache, OOM, missing secret, runner image) → debug-ci-pipeline-failure
- Generating deterministic, isolated fixture/seed data → test-data-factories (this skill consumes it to remove shared-state flakes)
- Finding minimal failing inputs / shrinking via generated cases → property-based-testing
- Screenshot/DOM diffs that flicker due to fonts/animation → visual-regression-testing (its own determinism toolkit)
- A general non-flaky bug where you need the root cause → debug-root-cause

## Steps

1. **Confirm it's actually flaky and classify it — don't guess.** A flake is non-determinism, not a real failure. Match the symptom to the cause; the cause dictates the fix:

   | Class | Tell-tale symptom | Root cause |
   |---|---|---|
   | **Order / shared state** | passes alone, fails in suite (or vice versa); fails only after another test | global/singleton/module-cache/env mutated and not reset; shared DB row; ordering-dependent assertion |
   | **Async timing** | `sleep(100)` "fixes" it; fails under load/slow CI; "element not found" intermittently | asserting before an async effect settles; `setTimeout`-based wait |
   | **Real clock / TZ** | fails near midnight, month/DST boundary, or on a UTC vs local runner | code reads `Date.now()`/`new Date()`/`time.Now()`; suite runs in non-UTC TZ |
   | **Unseeded randomness** | fails ~1/N, no pattern; UUID/shuffle/sampling involved | `Math.random()`/`uuid()`/`random.shuffle` with no fixed seed |
   | **Network / external IO** | fails on DNS/timeout/rate-limit; depends on a live endpoint | real HTTP/clock/filesystem dependency not stubbed |
   | **Resource collision** | fails only in parallel; "address in use", "file exists", deadlock | hardcoded port, shared temp dir/file, one DB shared across workers |
   | **Leak / pollution** | flakiness grows as suite grows; later tests degrade | unclosed conn/timer/listener; un-awaited promise bleeding into the next test |

2. **Reproduce deterministically BEFORE touching code — a flake you can't trigger, you can't prove fixed.** Increase the failure rate until it's reliable:

   | Tool | Loop a test until it fails | Randomize order (reproducibly) |
   |---|---|---|
   | **Jest** | `jest --runInBand --testNamePattern=X` in a `for i in {1..200}` loop; or `jest-circus` retry off | `--shard`, plugin `jest-randomize`; record/replay the order |
   | **Vitest** | `vitest run --no-isolate` to *expose* leaks; `vitest --repeat=200` | `--sequence.shuffle --sequence.seed=12345` |
   | **pytest** | `pytest -p no:randomly --count=500 test_x.py` (`pytest-repeat`); `pytest -x` to stop on first | `pytest -p randomly --randomly-seed=12345` (`pytest-randomly`) |
   | **Go** | `go test -run TestX -count=500`; `-race` ALWAYS | `-shuffle=on -shuffle.seed=12345` |
   | **JUnit** | repeat via `@RepeatedTest(500)`; Maven Surefire `rerunFailingTestsCount=0` | Surefire `runOrder=random` + `runOrderRandomSeed` |

   Run **in isolation** and **in the full suite** separately — same test, two contexts localizes order/state flakes immediately. Capture the seed and order on failure so the repro is replayable. Run `go test -race` / TSan / `--detectOpenHandles` (Jest) to surface leaks and races for free.

3. **Kill clock-dependent flakes with a fake clock — never read the real time in code under test.** Freeze or control time so the same instant is observed every run:

   | Stack | Fake the clock |
   |---|---|
   | **Jest** | `jest.useFakeTimers().setSystemTime(new Date('2025-01-01T00:00:00Z'))`; advance with `jest.advanceTimersByTime(ms)` / `runAllTimersAsync()` |
   | **Vitest** | `vi.useFakeTimers(); vi.setSystemTime(...)`; `vi.advanceTimersByTimeAsync(ms)` |
   | **Python** | `freezegun.freeze_time("2025-01-01")` or `time-machine`; inject a `clock` callable in product code |
   | **Go** | inject a `Clock` interface (`clock.Now()`), use `clockwork`/`benbjohnson/clock` fake in tests — never call `time.Now()` directly |
   | **JVM** | `Clock.fixed(instant, ZoneOffset.UTC)` injected; never `Instant.now()` inline |

   And **pin the timezone and locale for the whole suite**: `TZ=UTC LC_ALL=C` as a CI env var (and locally), so a runner in `America/Los_Angeles` and one in `Asia/Bangkok` agree. A test that asserts a formatted date/day-of-week without a pinned TZ is flaky by construction.

4. **Replace every `sleep` with an awaited condition.** A fixed delay is a race that "usually" wins; CI is slower and it loses. Poll for the actual state, with a timeout:
   - JS DOM/React → `await waitFor(() => expect(...).toBeInTheDocument())` / `findBy*` (Testing Library), `await expect(locator).toBeVisible()` (Playwright auto-waits — never `page.waitForTimeout`).
   - Backend → poll the condition (`await until(() => repo.get(id)?.status === 'done', {timeout: 2000})`); await the promise/job handle directly instead of guessing a duration.
   - Go → block on a channel/`WaitGroup`/`sync.Cond`, not `time.Sleep`.
   - If you fake timers (step 3), advance them explicitly and `await` the resulting microtasks — don't mix fake timers with real `await new Promise(setTimeout)`.

   Rule: **the test must wait on a signal that the work is done, not on the clock.**

5. **Seed all randomness and log the seed.** Determinism requires a fixed, *recorded* seed so a failure is reproducible:
   - Set a global seed (`pytest-randomly` prints `Using --randomly-seed=...`; Jest/Vitest `--sequence.seed`; Go `-shuffle.seed`) and **echo it on failure** so you can replay.
   - Stub non-deterministic generators: freeze `Math.random`/`crypto.randomUUID`, inject a deterministic id generator, or use a factory that produces stable values (→ test-data-factories). Don't assert on a real UUID; assert on shape or a seeded value.
   - For "any order is valid" results, assert on a **set/sorted** comparison, not list equality — the flake is often a legitimately unordered result the test over-specified.

6. **Isolate state per test — the #1 cause of order-dependent flakes.** Each test must start from a known, private state and leave nothing behind:

   | Resource | Isolation technique |
   |---|---|
   | **Database** | wrap each test in a transaction and **roll back** in teardown; or a fresh schema/database per worker (`pytest-xdist` `--dist=loadgroup`, `testcontainers` per suite); truncate-between only if no parallelism |
   | **Globals / singletons / module cache** | reset in `afterEach`; `jest.resetModules()`/`vi.resetModules()`; restore env vars; clear in-memory caches/registries |
   | **Filesystem / temp** | unique `mkdtemp()` per test, cleaned in teardown — never a hardcoded `/tmp/test.json` |
   | **Ports / servers** | bind to port `0` (OS-assigned) and read back the actual port; never hardcode `:3000` |
   | **Mocks / spies** | `restoreAllMocks()`/`vi.restoreAllMocks()` in teardown so a stub doesn't bleed into the next test |

   Forbid cross-test ordering dependencies: if test B needs data from test A, that's the bug — make B self-contained.

7. **Stub network and external IO; assert on a local boundary.** A test that hits a live URL, real DNS, or a third-party API is flaky by definition (timeouts, rate limits, data drift). Intercept at the HTTP layer (`msw`, `nock`, `responses`/`vcr.py`, `httptest.Server`), or inject a fake adapter. Set explicit per-request timeouts in the harness so a hung dependency fails fast and visibly instead of intermittently. Keep these stubbed deterministic responses in fixtures, not fetched at test time.

8. **Decide: is the flake in the test, or a real product race?** This is the senior call. Run the suspect test under `-race`/TSan and against the *real* concurrent path. If the non-determinism only exists because the test mis-waits or shares state → fix the test (steps 3–7). If two real operations genuinely race in product code (lost update, check-then-act, unsynchronized shared mutable state) → the flaky test is doing its job; hand the confirmed race to **async-concurrency-correctness** and keep a failing test that reproduces it. **Never delete a test that's exposing a real bug** because it's "flaky."

9. **Apply a quarantine policy — never a permanent retry.** When a flake can't be root-caused immediately, contain it without lying about green:
   - **Tag and track:** mark `@flaky`/`test.skip` (or `@Disabled`) **with a linked tracking issue and an owner + SLA** (e.g. fix or delete within 2 weeks). A quarantined test that never gets fixed is just deleted coverage.
   - **Quarantine ≠ retry:** moving it to a non-blocking lane is acceptable *temporarily*; auto-`retry(3)` on the whole suite as a standing policy is **forbidden** — it hides real product races and lets new flakes accumulate silently. If you must allow CI retries, scope them narrowly and **alert/count** them so flakiness is visible, not absorbed.
   - **Detect, don't ignore:** run a periodic "flaky detector" job that loops the suite and flags tests with a non-zero failure rate, so flakes surface before they erode trust in the suite.

## Common Errors

- **`sleep(n)` to "fix" a timing flake.** Wins on a fast laptop, loses on slow CI. Fix: await the condition/`waitFor`/promise (step 4); fake timers and advance them explicitly.
- **Real clock in code under test.** `Date.now()`/`time.Now()` makes tests fail at boundaries. Fix: inject and freeze a clock (step 3) + pin `TZ=UTC`.
- **Unpinned timezone/locale.** Date/format assertions pass in one TZ, fail in another. Fix: `TZ=UTC LC_ALL=C` for the whole suite.
- **Unseeded randomness.** `Math.random()`/`uuid()`/shuffle → ~1/N failures with no repro. Fix: seed it, log the seed, stub the generator (step 5).
- **Shared mutable state between tests.** Global/singleton/DB row/env mutated and not reset → order-dependent flake. Fix: per-test isolation + teardown reset (step 6).
- **Hardcoded port/temp path under parallelism.** "address in use"/"file exists" only in parallel. Fix: port `0`, `mkdtemp()` per test.
- **Live network/API in a unit/integration test.** Timeouts and data drift = flake. Fix: stub at the HTTP boundary with deterministic fixtures (step 7).
- **List-equality on an unordered result.** Asserting order the system doesn't guarantee. Fix: compare as a set or sort first.
- **Mocks/timers not restored.** A stub from test A leaks into B. Fix: `restoreAllMocks`/`useRealTimers`/`resetModules` in teardown.
- **Blanket `retry(3)` in CI.** Greens the dashboard, hides a real product race, normalizes flakiness. Fix: root-cause + quarantine-with-SLA (step 9), never standing retries.
- **Deleting a flaky test that exposes a real race.** You removed a true bug's only alarm. Fix: confirm via `-race`; if real, hand to async-concurrency-correctness and keep the reproducer (step 8).
- **Declaring it fixed after one green run.** A flake passes most of the time by definition. Fix: prove with the loop (step 2) — hundreds of runs, all green.

## Verify

1. **Reproduced first:** before the fix, the loop (`--count=500`/`for` loop, randomized order with a recorded seed) fails at a measurable rate; you can name the class (step 1) and point to the exact source of non-determinism.
2. **Order-independent:** the test passes both in isolation and in the full suite, and under shuffled order with multiple seeds — no dependency on what ran before it.
3. **Clock-pinned:** code under test takes an injected/frozen clock; suite runs with `TZ=UTC` and passes when the runner's local TZ is changed.
4. **No `sleep`:** grep the diff — zero fixed-delay waits (`sleep`/`waitForTimeout`); every wait is on a condition/signal with a timeout.
5. **Seeded:** randomness is seeded and the seed is logged on failure; rerunning with that seed reproduces or confirms the fix deterministically.
6. **Isolated:** each test starts from clean state (transaction-rollback / fresh schema / `mkdtemp` / port 0) and restores globals, mocks, timers, and env in teardown.
7. **No live IO:** no test hits real network/DNS/third-party endpoints; external calls are stubbed with deterministic fixtures and explicit timeouts.
8. **Race-checked:** ran under `-race`/TSan/`--detectOpenHandles`; either the flake was in the test (fixed here) or a real product race was confirmed and routed to async-concurrency-correctness with a reproducer kept.
9. **Stayed green under load:** the same loop that reproduced it now passes hundreds of runs, randomized, in parallel, with zero failures.
10. **No retry mask:** the fix is not a standing `retry()`; any quarantine is tagged with a tracking issue, owner, and SLA, and flaky-rate is monitored.

Done = the flake is reproduced and classified before any change, fixed at root cause (frozen clock + pinned TZ, awaited conditions not sleeps, seeded RNG, per-test isolation, stubbed IO), proven by hundreds of randomized parallel runs all green, with real product races routed to async-concurrency-correctness and any unavoidable quarantine tagged with an SLA — never masked by a blanket retry.
