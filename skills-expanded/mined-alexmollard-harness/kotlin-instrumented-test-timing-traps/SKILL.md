---
name: kotlin-instrumented-test-timing-traps
description: "Fix Kotlin/Android instrumented tests that pass alone but fail in the suite, or that abort the whole run with \"Failed to instantiate test runner class\" — covers runTest's virtual delay never waiting, an expression-bodied @Before returning non-Unit, awaiting a ViewModel StateFlow deterministically, and proving a fix by running the full suite twice. Use when an androidTest is flaky, when a wait races an async load, or when the runner fails before any test executes."
---

# Instrumented test timing traps (Kotlin / Android)

Three failures that look like device, dependency, or product problems and are
none of them. Each cost a full diagnostic cycle.

## 1. `runTest`'s `delay` is virtual — a polling loop never waits

```kotlin
@Before fun setUp() = runTest {          // WRONG for waiting on real work
    var waited = 0
    while (vm.ui.value.items.isEmpty() && waited < 100) { delay(50); waited++ }
}
```

Inside `runTest` the scheduler *skips* `delay`, so 100 iterations complete in
microseconds. The test then passes only when the awaited work happened to be
warm — green alone, red in the suite. Symptom: an assertion like
`"must load its catalogue" expected:<true> but was:<false>` that nobody can
reproduce in isolation.

`runBlocking` makes the delay real, but a fixed sleep still races the load.

## 2. Await the state, never a duration

```kotlin
val loaded = withTimeout(10_000) { vm.ui.first { it.items.isNotEmpty() } }
assertTrue("the editor must load its catalogue", loaded.items.isNotEmpty())
```

There is no duration to tune wrong. Use for anything a `ViewModel` loads in
`init`, or any `StateFlow` fed asynchronously.

## 3. An expression-bodied `@Before` returning a value kills the entire run

```kotlin
@Before fun setUp() = runBlocking {
    withTimeout(10_000) { vm.ui.first { it.items.isNotEmpty() } }   // returns the value
}
```

JUnit requires `@Before` to return `void`. A non-`Unit` tail fails **class
validation**, so nothing runs and the error names the runner, not your code:

```
RuntimeException: Failed to instantiate test runner class
androidx.test.internal.runner.junit4.AndroidJUnit4ClassRunner
  Caused by: java.lang.reflect.InvocationTargetException
```

This reads like a missing `kotlinx-coroutines-test` dependency or a broken
emulator. It is a signature. Confirm the classpath theory cheaply — if
`assembleDebugAndroidTest` compiles clean, it is not the classpath.

Fix: bind the value and assert on it (keeps `Unit`, documents the premise), or
add an explicit trailing `Unit`.

## Verifying a fix

A flake fix is unproven until the **full suite** runs green **twice
consecutively** — not the single test, which is what passed before.

```bash
rm -rf app/build/outputs/androidTest-results     # stale XML reads as green
./gradlew :app:connectedDebugAndroidTest
```

Always print the result-file count alongside the totals; `0 files` means the run
never happened and any "pass" is last run's XML.

## Constructing a ViewModel in an instrumented test

Needs a real `Repository`, so build it on an isolated database and on `Main`:

```kotlin
context.deleteDatabase(TEST_DB)
db = MonarchDatabase.create(context, TEST_DB)      // never the live file
vm = withContext(Dispatchers.Main) { PresetEditorViewModel(Repository(db), presetId = null) }
```

Do not fake the repository to force a JVM unit test. Either use the instrumented
suite, or extract the pure logic into a top-level function and test that.
