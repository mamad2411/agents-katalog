---
name: kmp-coverage-grower
description: Incrementally grow unit-test coverage on a Kotlin Multiplatform project (Android + iOS) — find untested branches and edge cases, prefer `commonTest` so one test serves both platforms, add tests where they're missing, and harden existing tests with edge cases that current coverage misses. Use whenever the user asks to "add tests", "improve coverage", "find uncovered code", "what's not tested", "edge cases", mentions Kover/JaCoCo, or wants to ratchet coverage up over time. Works even when there are zero tests today.
---

# KMP Coverage Grower

The goal isn't 100% coverage — it's confidence that the logic does what it says, especially at the edges. This skill walks through measuring what's tested, finding what isn't, and adding the smallest set of tests that closes the highest-value gaps.

## When to use

Triggers: "add unit tests", "raise coverage", "find untested code", "edge cases", "Kover", "JaCoCo", "what should I test", "no tests yet", "coverage report".

For instrumented/UI tests, use a different skill. This one focuses on **unit tests** — `commonTest`, `androidUnitTest`, `iosTest`.

## Process

### Phase 1: Inventory what's there

Don't write a single test until you know the baseline. Run:

```
find . -path '*/commonTest/*.kt' | wc -l
find . -path '*/androidUnitTest/*.kt' -o -path '*/androidTest/*.kt' | wc -l
find . -path '*/iosTest/*.kt' | wc -l
```

And check what's set up:

- `kotlin.test` in `commonTest` dependencies?
- `kotlinx-coroutines-test`, `turbine`, `Ktor MockEngine` available in `commonTest`?
- Kover or JaCoCo plugin applied?

Tell the dev what you found in one paragraph before doing anything else. Cases:

- **Zero tests, no tooling** → start at Phase 2 (set up), then Phase 3 picks the first target.
- **Some tests, no coverage tool** → Phase 2 (just the tooling), then Phase 3.
- **Tests + coverage tool** → skip to Phase 3.

### Phase 2: Set up measurement

Use **Kover** for KMP — it aggregates across platforms and is the modern default.

Root `build.gradle.kts`:

```kotlin
plugins {
    id("org.jetbrains.kotlinx.kover") version "..." apply false
}
```

In each module that should report coverage:

```kotlin
plugins {
    id("org.jetbrains.kotlinx.kover")
}

kover {
    reports {
        filters {
            excludes {
                classes("*.di.*", "*.generated.*", "*BuildConfig*")
                annotatedBy("*Generated*")
            }
        }
    }
}
```

Run:

```
./gradlew :shared:koverHtmlReport
```

Report lands in `build/reports/kover/html/index.html`. Open it.

If the project is Android-only, JaCoCo works too — but Kover handles `commonMain` source-set coverage correctly, which JaCoCo doesn't.

### Phase 3: Pick targets, don't chase percentages

Open the coverage report and sort by file. **Don't aim for high overall percentage** — aim for high coverage on files that matter. Use this filter:

| Priority | What |
|---|---|
| **High** | Repositories, use cases, ViewModels/Presenters, parsers, validators, state reducers |
| **Medium** | Mappers, formatters, non-trivial extensions |
| **Skip** | DTOs, `data class` with only `val`s, DI modules, generated code, `expect class` declarations |

Pick the highest-priority file with the lowest coverage. That's your target.

### Phase 4: Read the file before writing tests

Open the target file and identify:

1. **Public entry points** — what callers actually invoke. These are the test surface.
2. **Branches** — every `if`, `when`, `try/catch`, `?:`, `?.let`. Each branch is at least one test.
3. **Error paths** — what happens on null inputs, empty collections, network failures, cancellation.
4. **State** — for stateful classes (ViewModels), what's the state graph? Each transition is a test.

Then look at any existing tests for this file. Note what's covered (happy path usually) and what isn't (almost always: errors, edges, concurrency).

### Phase 5: Write tests in `commonTest` when possible

Every test you can put in `commonTest` runs on both platforms — one test, double the value. Push tests up:

| Code lives in | Test lives in |
|---|---|
| `commonMain` | `commonTest` |
| `androidMain` only (e.g. uses `Context`) | `androidUnitTest` |
| `iosMain` only | `iosTest` |
| `expect`/`actual` | Test the contract in `commonTest`; test platform quirks in platform tests |

**Test skeleton for `commonTest`:**

```kotlin
class UserRepositoryTest {
    private val testDispatcher = StandardTestDispatcher()
    private lateinit var api: FakeUserApi
    private lateinit var repo: UserRepository

    @BeforeTest fun setup() {
        api = FakeUserApi()
        repo = UserRepository(api, testDispatcher)
    }

    @Test fun returnsUser_whenApiSucceeds() = runTest(testDispatcher) {
        api.userResponse = User(id = "1", name = "Bam")
        val result = repo.getUser("1")
        assertEquals(User("1", "Bam"), (result as Outcome.Success).value)
    }
}
```

Prefer **fakes** (hand-written stub implementations of interfaces) over mocking libraries. MockK has KMP support but it's friction; fakes are clearer and work everywhere.

### Phase 6: Hunt edge cases the current tests miss

This is the part most teams skip. For each function, run through this checklist:

**Inputs**
- Empty string, empty list, empty map.
- Null where nullable.
- Single-element collection (often handled differently than many).
- Boundary values: `0`, `-1`, `Int.MAX_VALUE`, `Long.MIN_VALUE`.
- Unicode, whitespace, very long strings.
- Duplicates in a list that's expected to be unique.

**State**
- Method called twice in a row.
- Method called before init / after close.
- Concurrent calls from multiple coroutines.

**Errors**
- Network throws `IOException`.
- Server returns 4xx, 5xx, malformed JSON.
- Database returns empty result.
- Cancellation: `runTest { val job = launch { ... }; job.cancel(); ... }`.

**Time and async**
- `delay()` and timeouts — use `testScheduler.advanceTimeBy(...)`.
- Flow emissions: empty flow, single emission, many, error mid-stream. Use `Turbine`:

```kotlin
repo.observeUser("1").test {
    assertEquals(Loading, awaitItem())
    assertEquals(Success(User(...)), awaitItem())
    awaitComplete()
}
```

**Platform quirks (for `expect`/`actual`)**
- Date/time: locale, timezone edge (DST switch).
- Numbers: locale-dependent formatting.
- Strings: different default encodings.
- Filesystem paths: Android `/data/...` vs. iOS sandbox.

For each gap you find, write one focused test. Name it after the case: `returnsEmptyList_whenInputIsEmpty`, not `test3`.

### Phase 7: Verify coverage actually moved

After adding tests, rerun:

```
./gradlew :shared:koverHtmlReport
```

Check the specific file you targeted. Coverage should jump. If it didn't:

- Tests may not run on both platforms — verify by running `./gradlew :shared:allTests` (or `:iosX64Test` and `:testDebugUnitTest` separately).
- Branches you thought were tested might be excluded by Kover filters.
- The test might pass without exercising the branch (assertion is too loose).

### Phase 8: Lock in the gain

Set a coverage floor so the new tests don't get deleted and uncovered code doesn't grow back:

```kotlin
kover {
    reports {
        verify {
            rule {
                minBound(60)  // raise as coverage grows
            }
        }
    }
}
```

Run `./gradlew :shared:koverVerify` in CI. When you add tests next round, ratchet the number up by 5-10 points. The ratchet is the whole point — coverage that goes up and never comes down.

## Output

Each pass produces:

1. **Inventory** — current test counts, current coverage % per priority file.
2. **Targets picked** — 1–3 files with reasoning.
3. **Edge case list** — the specific cases you found uncovered.
4. **Tests added** — file paths, brief description, where they live (commonTest preferred).
5. **New coverage numbers** — per file and overall.
6. **New floor** — Kover verify rule, ratcheted.

Don't dump 50 tests in one PR. Group by file or by feature so review stays sane.

## Common pitfalls

- **Chasing percentage instead of quality.** A test that calls a function with happy-path inputs and no assertions adds coverage but no confidence. Each test must assert the right thing happened.
- **Writing tests in `androidUnitTest` when `commonTest` would work.** Halves the value — iOS gets nothing.
- **Mocking everything.** Heavy mocking ties tests to implementation. Fakes for collaborators, real instances for value types and pure logic.
- **One giant test per function.** Hard to read, hard to debug a failure. Prefer many small named tests.
- **Skipping cancellation tests for coroutine code.** Cancellation bugs are some of the nastiest in production. Test them explicitly.
- **Setting a coverage floor that fails the build forever.** Start at the current number minus a small buffer; raise on every coverage-improving PR.
- **Testing `data class` equals/hashCode.** The compiler generates these. Don't.
