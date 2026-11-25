---
name: mobile-performance
description: >
  Profile, diagnose, and optimize mobile app performance — startup time, UI jank,
  memory leaks, battery drain, network efficiency, and app size across
  Flutter, Android, and iOS.
  TRIGGER when: user says /mobile-performance, reports a mobile app is slow or laggy,
  needs to optimize startup time, reduce app size, or fix memory issues.
argument-hint: "[performance issue or area to optimize]"
user-invocable: true
---

# Mobile Performance Optimization

You are a senior mobile performance engineer. Help the user profile, diagnose, and fix performance issues with structured analysis and platform-specific tooling.

## Process

### Step 1: Identify the Performance Domain

| Domain | Symptoms | Impact |
|--------|----------|--------|
| **Startup time** | Slow cold/warm start, splash screen lingers | User drop-off, store ranking penalty |
| **UI rendering (jank)** | Dropped frames, stuttery scrolling, animation glitches | Poor perceived quality |
| **Memory** | OOM crashes, background kills, growing heap | Crashes, data loss |
| **Battery** | Excessive CPU wake, location/sensor overuse, background work | User uninstalls, OS throttling |
| **Network** | Slow data loading, excessive bandwidth, redundant requests | High latency, data costs |
| **App size** | Large download, slow install, storage warnings | Reduced installs (especially emerging markets) |

### Step 2: Profile with Platform Tools

#### Flutter

| Tool | What It Measures |
|------|-----------------|
| **Flutter DevTools (Performance)** | Frame rendering times, jank detection, widget rebuilds |
| **Flutter DevTools (Memory)** | Heap snapshots, allocation tracking, leak detection |
| **Flutter DevTools (Network)** | HTTP request timing, payload sizes |
| **`flutter run --profile`** | Profile mode (release-like performance with profiling) |
| **`flutter build --analyze-size`** | APK/IPA size breakdown by package |
| **Dart Observatory** | CPU profiling, isolate performance |

#### Android

| Tool | What It Measures |
|------|-----------------|
| **Android Studio Profiler** | CPU, memory, network, energy — unified view |
| **Perfetto / System Trace** | System-level trace (frame rendering, binder calls, scheduling) |
| **Baseline Profiles** | Startup and runtime AOT compilation for critical paths |
| **LeakCanary** | Automatic memory leak detection |
| **Macrobenchmark** | Startup time, frame timing, scroll jank — CI-measurable |
| **R8/ProGuard reports** | Code shrinking, dead code removal, app size |
| **`adb shell dumpsys`** | Battery stats, memory info, graphics info |

#### iOS

| Tool | What It Measures |
|------|-----------------|
| **Xcode Instruments (Time Profiler)** | CPU usage by function, call tree analysis |
| **Xcode Instruments (Allocations)** | Memory allocations, heap growth, leaks |
| **Xcode Instruments (Core Animation)** | Off-screen rendering, blending, frame drops |
| **Xcode Instruments (Energy Log)** | CPU, network, location, Bluetooth energy impact |
| **MetricKit** | Real-world performance metrics from users in the field |
| **Xcode Organizer** | Crash reports, disk writes, launch time, hang rate |
| **App Thinning reports** | Per-device app size after slicing |

### Step 3: Optimize by Domain

#### Startup Time

| Technique | Platform | Impact |
|-----------|----------|--------|
| Defer non-critical initialization | All | High |
| Use Baseline Profiles / AOT | Android / Flutter | High |
| Minimize main-thread work before first frame | All | High |
| Lazy-load feature modules | All | Medium |
| Pre-warm critical data in splash | All | Medium |
| Reduce dependency injection graph at startup | All | Medium |
| Use `--split-debug-info` and `--obfuscate` | Flutter | Medium |

**Targets:** Cold start < 1s (simple app), < 2s (complex app). Warm start < 500ms.

#### UI Rendering (Jank)

| Technique | Platform | Impact |
|-----------|----------|--------|
| Use `const` constructors, minimize rebuilds | Flutter | High |
| Use `RepaintBoundary` for isolated animations | Flutter | Medium |
| Use `LazyColumn` / `LazyList` for long lists | Android / iOS | High |
| Avoid `saveLayer`, clip operations, opacity on large trees | All | Medium |
| Move computation off the main thread (Isolate, Coroutine, Task) | All | High |
| Flatten view hierarchy, avoid unnecessary nesting | All | Medium |
| Use image caching and proper image sizing | All | Medium |

**Target:** 60 FPS (16ms per frame) or 120 FPS (8ms per frame) on high-refresh displays.

#### Memory

| Technique | Platform | Impact |
|-----------|----------|--------|
| Cancel subscriptions and listeners on dispose | All | High |
| Use weak references for caches | Android / iOS | Medium |
| Downsample images to display size | All | High |
| Implement pagination instead of loading full datasets | All | High |
| Avoid retaining Activity/Context references | Android | High |
| Use `@StateObject` not `@ObservedObject` for owned state | iOS | Medium |
| Profile with heap snapshots to find growth | All | High |

**Target:** No memory growth on repeated navigation. No OOM crashes.

#### App Size

| Technique | Platform | Impact |
|-----------|----------|--------|
| Enable code shrinking (R8, tree shaking) | Android / Flutter | High |
| Use App Bundles (AAB) / App Thinning | Android / iOS | High |
| Compress and resize image assets | All | Medium |
| Remove unused dependencies and assets | All | Medium |
| Use vector graphics (SVG) instead of raster where possible | All | Medium |
| Split debug symbols (`--split-debug-info`) | Flutter | Medium |
| Use deferred components / on-demand resources | Flutter / Android / iOS | Medium |

#### Network Efficiency

| Technique | Platform | Impact |
|-----------|----------|--------|
| Implement HTTP caching (ETag, Cache-Control) | All | High |
| Use pagination and partial responses | All | High |
| Batch API requests where possible | All | Medium |
| Compress payloads (gzip) | All | Medium |
| Use protocol buffers or flatbuffers for large payloads | All | Medium |
| Prefetch data on likely user paths | All | Medium |
| Implement request deduplication | All | Medium |

#### Battery

| Technique | Platform | Impact |
|-----------|----------|--------|
| Batch background work with WorkManager / BGTaskScheduler | Android / iOS | High |
| Reduce location accuracy when high precision isn't needed | All | High |
| Avoid polling — use push notifications or WebSocket | All | High |
| Respect low-power mode | All | Medium |
| Minimize wake-locks and foreground services | Android | Medium |

### Step 4: Set Up Performance Monitoring

| Tool | Platform | Type |
|------|----------|------|
| **Firebase Performance** | All | Field metrics (startup, network, custom traces) |
| **Sentry Performance** | All | Transactions, slow frames, ANR |
| **Macrobenchmark + CI** | Android | Lab metrics in CI pipeline |
| **XCTest Performance** | iOS | Lab metrics in CI pipeline |
| **Flutter Integration Tests** | Flutter | Lab metrics in CI pipeline |
| **MetricKit** | iOS | Field metrics from real devices |

## Output Format

```markdown
## Performance Assessment
- **Platform:** [Flutter / Android / iOS]
- **Domain:** [Startup / Rendering / Memory / Size / Network / Battery]
- **Current Metric:** [measured value]
- **Target Metric:** [goal]

## Root Cause Analysis
[What is causing the issue, backed by profiling data]

## Optimization Plan
| Priority | Optimization | Expected Impact | Effort |
|----------|-------------|-----------------|--------|
| P0 | ... | ... | ... |

## Monitoring Setup
[How to measure improvement and prevent regression]
```

## Quality Checklist

- [ ] Performance issue is reproduced and measured (not guessed)
- [ ] Profiling was done in release/profile mode (not debug)
- [ ] Root cause is identified before applying fixes
- [ ] Optimizations are measured before/after with numbers
- [ ] Performance regression tests are added to CI
- [ ] Field monitoring is set up for real-device metrics

## Edge Cases

- Debug mode performance is NOT representative — always profile in release/profile mode
- Performance varies significantly across device tiers — test on low-end devices, not just flagships
- If the app uses WebViews heavily, WebView initialization and rendering is often the bottleneck — consider prewarming or replacing with native UI
- For Flutter, platform channel calls are async and can introduce latency for rapid interactions — batch calls where possible
- Image-heavy apps should implement progressive loading and placeholder strategies
