---
name: flaky-test-stabilizer
description: Diagnose and stabilize flaky Android tests — coroutine dispatcher issues, idling resource gaps, time/clock control, network mocking, Robolectric vs instrumented mismatches, and Compose `mainClock` problems. Use whenever the user mentions a "flaky test", "intermittent failure", "passes locally fails in CI", "test sometimes hangs", "racy", or wants to investigate a test that fails 5–30% of the time. Also use when reviewing a test suite that's been disabled or quarantined because of flakiness.
---

# Flaky Test Stabilizer

Flaky tests are almost never random. They're races, time bugs, or environment differences. This skill walks through the categories in the order they're worth checking.

## When to use

Triggers: "flaky", "intermittent", "passes locally", "sometimes fails", "@Ignore", "retry", "test hangs", "JUnit timeout".

For tests that fail 100% of the time — that's a normal failing test. Use this when the failure rate is between 1% and 99%.

## Process

### Phase 1: Reproduce the flake

You can't fix what you can't observe. Get the flake to fail somewhat reliably first:

- Run the test 50–200 times in a loop. In Android Studio, "Run Until Failure" or use `--rerun-tasks` with a count.
- For instrumented tests: `./gradlew connectedDebugAndroidTest --rerun-tasks` in a loop.
- Note the failure rate. A 5% flake needs more runs to confirm a fix than a 50% one.

If it only flakes in CI, look at differences: device emulator vs. local, parallel test execution, time zone, locale.

### Phase 2: Read the failure

For each failure, capture:

- The assertion that failed and the actual vs expected.
- Logcat (instrumented) or stdout (unit).
- Thread dump if it hung.
- Whether failures cluster on the same assertion or vary.

Different assertions failing = the test is in a bad state by the time it gets there (look earlier in the test). Same assertion = the timing of one specific operation is racing.

### Phase 3: Match the flake to a category

**Coroutine dispatcher / `runTest` misuse**
- ViewModel test uses real `Dispatchers.Main` instead of a test dispatcher.
- `runBlocking` instead of `runTest`.
- `Dispatchers.IO` work that isn't awaited.
- **Fix**: Inject a `CoroutineDispatcher` (Hilt or constructor). In tests, swap to `UnconfinedTestDispatcher()` or `StandardTestDispatcher()`. Use `Dispatchers.setMain(testDispatcher)` in `@Before`. Use `Turbine` for Flow assertions instead of `take(1).toList()`.

**Time / clock dependency**
- Tests use `System.currentTimeMillis()` or `Instant.now()` directly.
- Animations or `delay()` calls not advanced.
- **Fix**: Inject a `Clock`. In `runTest`, use `testScheduler.advanceTimeBy(...)` or `advanceUntilIdle()`. For Compose, `composeTestRule.mainClock.autoAdvance = false` and `advanceTimeBy(...)` explicitly.

**Idling / synchronization gaps (instrumented)**
- Espresso test races against a background task because there's no `IdlingResource`.
- `Thread.sleep()` used as a synchronization primitive.
- **Fix**: Register an `IdlingResource` for OkHttp, WorkManager, or custom async work. For Compose, the test rule auto-syncs — don't add sleeps.

**Network non-determinism**
- Tests hit real endpoints.
- `MockWebServer` enqueues are missing for some test paths.
- **Fix**: Always mock. Verify every test enqueues exactly the responses it needs. Reset the mock between tests.

**Shared state across tests**
- A static field, singleton, or DataStore persists between tests.
- Tests pass in isolation but fail when run after others.
- **Fix**: Reset state in `@After`. Use Hilt's `@TestInstallIn` to swap dependencies per test. Avoid `object` singletons that hold mutable state.

**Robolectric vs instrumented mismatch**
- Test passes on JVM (Robolectric) but fails on device, or vice versa.
- **Fix**: Identify the API behaving differently. Robolectric shadows some Android APIs imperfectly. Consider moving the test to the layer where the behavior is real (instrumented for framework-heavy code, unit for pure logic).

**Compose test clock issues**
- `composeTestRule.waitForIdle()` returns but animations are mid-flight.
- `onNodeWithText` fails because the text just appeared.
- **Fix**: `waitUntil { ... }` with a timeout, or control the clock manually with `mainClock.autoAdvance = false`.

**Order-dependent assertions**
- Assertions assume a specific order of events from a `Flow` or callback.
- **Fix**: Use `Turbine`'s `awaitItem()` (not `expectMostRecentItem()` unless that's the intent). For sets, assert on set membership, not list order.

### Phase 4: Apply the fix and prove it

- Re-run the test in a loop, same count as Phase 1.
- A fix that took the flake from 30% to 0% over 200 runs is real. From 30% to 2% over 50 runs is probably noise.
- Roll the pattern out: if the same flake-shape appears across many tests (e.g. missing test dispatcher), fix them all.

### Phase 5: Prevent

- Add a CI job that runs the suite N times on PRs to critical paths.
- Lint or detekt rule banning `Thread.sleep` in tests.
- Code review: any test using `runBlocking`, `System.currentTimeMillis`, or `Dispatchers.Main` directly should get pushback.

## Output

Per flaky test:

1. **Failure rate** observed.
2. **Category** from Phase 3.
3. **Root cause** — the specific race or assumption.
4. **Fix** — code change.
5. **Verification** — new failure rate after fix.

## Common pitfalls

- **Adding retries instead of fixing.** Hides the flake, lets it spread. Reserve `@Retry` for tests against truly external systems.
- **`Thread.sleep(500)` to "stabilize" timing.** Doesn't fix the race; makes the suite slow.
- **Marking flakes `@Ignore`.** They never come back. Quarantine with a ticket and a deadline.
- **Trusting one green run as proof of fix.** Re-run 100x. Flakes lie.
