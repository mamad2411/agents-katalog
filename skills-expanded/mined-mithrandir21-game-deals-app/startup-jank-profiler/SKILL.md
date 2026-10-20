---
name: startup-jank-profiler
description: Analyze Android startup time and frame drops — cold/warm/hot start, time-to-initial-display, Baseline Profile setup, Macrobenchmark scaffolding, Strong Skipping Mode wins, lazy-list jank, and image loader tuning. Use whenever the user mentions "slow startup", "cold start", "TTID", "jank", "frame drops", "Baseline Profile", "Macrobenchmark", or wants to make the app launch or scroll smoother. Especially relevant for release-build performance work.
---

# Startup & Jank Profiler

Startup is dominated by class loading, dependency graph construction, and synchronous I/O. Jank is dominated by main-thread work per frame. The fixes are different, and you need different tools to confirm them.

## When to use

Triggers: "slow startup", "cold start", "TTID", "time to interactive", "Baseline Profile", "Macrobenchmark", "jank", "frame drops", "scrolling stutter".

For "ANR / hang for many seconds" use `anr-deadlock-detective`. For "Compose screen is slow but no startup issue" use `compose-recomposition-optimizer`.

## Process

### Phase 1: Identify the symptom

Push the dev to name one specific thing:

- **Cold start time** (from icon tap to first frame) — measured by `am start -W`, Macrobenchmark `StartupTimingMetric`, or Play Console vitals.
- **Time to initial display (TTID)** — first frame visible.
- **Time to fully drawn (TTFD)** — when the app reports `reportFullyDrawn()`.
- **Frame jank during scrolling** — `FrameTimingMetric`, or Layout Inspector recomposition counts.

If they just say "slow", pick startup first (more impactful, easier to measure).

### Phase 2: Set up measurement

Don't optimize blindly. Get a number you can defend.

For startup, write a Macrobenchmark:

```kotlin
@RunWith(AndroidJUnit4::class)
class StartupBenchmark {
    @get:Rule val benchmarkRule = MacrobenchmarkRule()

    @Test
    fun startup() = benchmarkRule.measureRepeated(
        packageName = "com.app",
        metrics = listOf(StartupTimingMetric()),
        iterations = 10,
        startupMode = StartupMode.COLD,
        setupBlock = { pressHome() }
    ) {
        startActivityAndWait()
    }
}
```

Run on a real device, not an emulator. Run on the **release build** with R8 enabled — debug builds are not representative.

Record the baseline number. Every change gets compared to it.

### Phase 3: Trace what startup actually does

Use Android Studio's CPU Profiler (System Trace) or Perfetto.

Look for these on the main thread before first frame:

- **`Application.onCreate`** — every dependency in here adds to cold start. List what's initialized.
- **Synchronous content provider initialization** — third-party SDKs love these. WorkManager, Firebase, etc.
- **Dependency graph construction** — Dagger/Hilt component creation. Usually fast; check if any provider does heavy work eagerly.
- **`Activity.onCreate`** — same checks.
- **First frame rendering** — composition + layout + draw. If this dominates, see Phase 5.

### Phase 4: Common startup fixes

**Move eager work to lazy / background**
- Anything in `Application.onCreate` that isn't needed before first frame: defer with `androidx.startup` (`Initializer` chains) or a coroutine on `Dispatchers.Default`.
- Firebase, analytics SDKs, crash reporters that aren't needed for the first screen: initialize after first frame, behind a `Dispatchers.Default` launch.

**Cut content providers**
- Each ContentProvider declared by a library runs at app start. Audit with `dumpsys package <pkg>`. Disable ones you don't need (some libs let you opt-out in the manifest).

**Lazy DI**
- Hilt/Dagger create eagerly only what's reached. If a provider does heavy work in `init`, defer.
- Use `Lazy<Foo>` or `Provider<Foo>` instead of `Foo` where the value isn't needed until later.

**Baseline Profile**
- Single biggest win for cold start once other fixes are in. Add the `androidx.baselineprofile` plugin, write a profile generator that exercises startup + key user paths, ship the generated profile with the app. Realistic improvement: 15–30% on cold start.

```kotlin
// In :baselineprofile module
@OptIn(ExperimentalBaselineProfilesApi::class)
@RunWith(AndroidJUnit4::class)
class BaselineProfileGenerator {
    @get:Rule val rule = BaselineProfileRule()

    @Test
    fun generate() = rule.collect("com.app") {
        startActivityAndWait()
        // exercise key paths
    }
}
```

**Strong Skipping Mode (Compose)**
- Confirm Kotlin 2.0+ and Strong Skipping enabled. Reduces unnecessary recomposition broadly, including on first composition of complex screens.

**Splash screen API**
- Use `androidx.core.splashscreen`. Keep it on screen until the first useful content is rendered, not until the app is "ready". Misuse here is a common cause of perceived slowness.

### Phase 5: Jank fixes (per-frame)

If the symptom is dropped frames rather than slow startup:

- **Compose recomposition** — see `compose-recomposition-optimizer`.
- **LazyColumn / LazyRow without keys** — every item recomposes on data change. Add `items(list, key = { it.id })`.
- **Image loading on main thread** — use Coil or Glide. Don't decode in `onBindViewHolder` or in Composables.
- **Heavy synchronous parsing** — JSON, large lists, computed properties recalculated per scroll. Cache, move to background, or use `derivedStateOf`.
- **Overdraw** — debug GPU overdraw in developer options. Pure white screens with 3x overdraw waste a lot of frame budget.

### Phase 6: Verify

- Re-run the Macrobenchmark from Phase 2. Compare numbers, not vibes.
- Run on a slow device (ideally the cheapest device in your supported range) — that's where wins matter most.
- Add the benchmark to CI so regressions get caught.

## Output

Per investigation:

1. **Baseline measurement** — number + device + build type.
2. **Trace summary** — where the time goes.
3. **Fixes** — ordered by impact / effort.
4. **Post-fix measurement** — same conditions as baseline.
5. **Ongoing check** — Macrobenchmark in CI, Baseline Profile maintained.

## Common pitfalls

- **Profiling debug builds.** R8 changes startup significantly. Always profile release builds (with `debuggable=false` if needed for tracing, use a profileable manifest entry).
- **One-shot measurement.** Cold start has high variance. Run 5–10 iterations.
- **Skipping Baseline Profiles.** Single largest startup win available with relatively little work.
- **Optimizing the wrong start mode.** Most users see warm starts, not cold. Make sure you're measuring the one that matters.
- **"Just initialize on a background thread"** for something that has to run before first frame. That's a race, not a fix.
