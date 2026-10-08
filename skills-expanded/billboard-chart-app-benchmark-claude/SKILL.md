# :benchmark Module

## Responsibility
Macrobenchmark and Baseline Profile generation. Measures app startup time and scroll performance using `benchmark-macro-junit4`. Generates Baseline Profile artifacts consumed by `:app`.

## Key Files
| File | Role |
|------|------|
| `benchmark/StartupBenchmark.kt` | Measures cold/warm startup metrics |
| `benchmark/ScrollChartBenchmark.kt` | Measures chart list scroll performance |
| `baselineprofile/StartupBaselineProfile.kt` | Generates startup Baseline Profile |
| `BaselineProfileMetrics.kt` | Shared metric configuration |
| `GenerlAction.kt` | Reusable UI automation actions (scroll, click) |
| `Utils.kt` | Helper utilities for benchmark setup |

## Baseline Profile Generation
```bash
# Generate baseline profile (requires connected device or managed device)
./gradlew :app:generateBaselineProfile
```
- Runs on Pixel 6 API 32 and API 36 (configured in `:benchmark/build.gradle.kts`).
- Only the `demo` flavor is enabled for baseline profile generation (`beforeVariants` filter).
- `dexLayoutOptimization = true` in `:app` uses the generated profile.

## Build Flavor
This module targets the `demo` flavor only. The `benchmark` build type extends `release` with debug signing. Do **not** run benchmarks on `debug` builds — results will be inaccurate.

## Rules
- Benchmark classes must extend `MacrobenchmarkRule`.
- Use `UiAutomator` for UI interactions — `testTagsAsResourceId = true` is set in `MainActivity`.
- Run `ScrollChartBenchmark` before any significant change to the chart list UI.
- Never include this module in the release APK — it is `android.test` only.

## Build Configuration
Plugins: `baselineprofile`, `billboard.android.test`.
Target: `:app`.
Managed devices: `pixel6Api32`, `pixel6Api36` grouped as `baselineProfileDevices`.
`experimentalProperties["android.experimental.self-instrumenting"] = true` — required for Baseline Profile generation.
