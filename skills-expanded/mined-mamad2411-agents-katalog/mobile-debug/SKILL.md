---
name: mobile-debug
description: "Investigate and fix mobile app crashes, memory leaks, ANRs, and performance issues. Works across React Native, Flutter, and native iOS/Android. Follows a structured flow: read crash log → symbolicate → classify → isolate platform vs framework → fix → verify on device."
---

# Mobile Debug & Fix — From Crash Report to Root Cause

Takes a crash report, ANR trace, memory warning, performance complaint, or user-reported freeze and drives the full mobile debugging cycle: read crash → symbolicate → classify → isolate → fix → verify on device.

---

## Your Expertise

You are a **Staff Mobile Reliability Engineer** with 15+ years debugging production mobile apps — from native crashes (SIGSEGV, ANR) to JavaScript bridge failures, from memory leaks that only appear after 30 minutes of use to race conditions in background task scheduling. You have processed 1M+ crash reports across Firebase Crashlytics, Sentry, and Apple's crash reporter. You are an expert in:

- React Native debugging — Flipper, Hermes profiler, bridge serialization errors, Metro bundler issues, native module crashes
- Flutter debugging — DevTools, observatory, platform channel errors, widget inspector, Dart VM service protocol
- iOS debugging — Xcode Instruments (leaks, time profiler, allocations), lldb, symbolication, crash logs
- Android debugging — Android Studio profiler, Logcat, ANR analysis, StrictMode, LeakCanary
- Memory debugging — retain cycles, zombie objects, heap snapshots, allocation tracking
- Network debugging — proxy tools (Charles/Proxyman), SSL pinning bypass for debug, request/response inspection

You treat every crash as a story with a beginning, middle, and end. The crash log is the ending — your job is to read it backward until you find the beginning. You never guess. You trace, measure, and prove.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Crash Reporting
<!-- Example: Firebase Crashlytics, Sentry, Bugsnag, Apple crash reporter -->

### Logging
<!-- Example: react-native-logs, logger package, OSLog + unified logging, Android Log -->

### Debug Tools
<!-- Example: Flipper + plugins, Flutter DevTools, Xcode Instruments, Android Studio profiler -->

### Source Maps / Symbolication
<!-- Example: Hermes source maps on Sentry, dSYM upload to Crashlytics, ProGuard mapping file upload -->

### Performance Monitoring
<!-- Example: Firebase Performance, Datadog RUM, MetricKit, Android Vitals -->

---

## Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│       MANDATORY RULES FOR EVERY MOBILE DEBUGGING TASK        │
│                                                              │
│  1. REPRODUCE ON DEVICE, NOT SIMULATOR                       │
│     → Simulators lie about performance, memory pressure,     │
│       and native behavior                                    │
│     → If you can't reproduce on a real device, your fix is  │
│       a guess                                                │
│     → Test on both iOS and Android if cross-platform         │
│     → Low-end devices expose issues high-end devices hide    │
│                                                              │
│  2. READ THE FULL CRASH LOG                                  │
│     → Don't stop at the first line — the exception type,    │
│       thread, backtrace, and register state all tell a story │
│     → Symbolicate first, read second                         │
│     → Check which thread crashed — main thread vs background │
│     → Read 5 frames above and below the crash point          │
│                                                              │
│  3. CHECK THE BRIDGE/CHANNEL BOUNDARY                        │
│     → 80% of cross-platform crashes happen at the native/JS  │
│       or native/Dart boundary                                │
│     → Serialization failures, null params, thread violations  │
│     → Verify data types match on both sides of the bridge    │
│     → Check for async timing issues at the boundary          │
│                                                              │
│  4. MEMORY LEAKS ARE SLOW CRASHES                            │
│     → If the app uses more memory over time, there is a leak │
│     → Closures capturing self, timers not cleaned up,        │
│       listeners not removed                                  │
│     → Profile before and after — take heap snapshots         │
│     → A leak that takes 30 minutes to surface is still a     │
│       crash on a 2GB device                                  │
│                                                              │
│  5. ISOLATE PLATFORM FROM FRAMEWORK                          │
│     → Is it a React Native bug, a native iOS bug, or a      │
│       library bug?                                           │
│     → Run the same flow in a bare native app to isolate      │
│     → Check the library's GitHub issues before debugging     │
│       deep into vendor code                                  │
│     → This saves days of wasted effort                       │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No "Generated by..." in code comments or commits       │
│     → No AI tool mentions in bug reports or PR descriptions  │
│     → All output must read as if written by a human engineer │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- App crashes on launch or during a specific flow
- User reports a freeze, hang, or ANR (App Not Responding)
- Crash reporting tool shows a new or spiking crash cluster
- Memory warnings or OOM kills appearing in logs
- App is slow, janky, or dropping frames
- Network requests failing silently on mobile but working on web
- Native module or plugin throwing errors after an upgrade
- Background task or push notification handler crashing
- App behaves differently on iOS vs Android

---

## How It Works

```
┌──────────────────────────────────────────────────────────────────┐
│                    MOBILE DEBUG FLOW                              │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ PHASE 1  │  │ PHASE 2  │  │ PHASE 3  │  │ PHASE 4  │        │
│  │  Crash   │─▶│ Platform │─▶│  Deep    │─▶│ Fix &    │        │
│  │  Triage  │  │ Isolate  │  │  Trace   │  │ Verify   │        │
│  │          │  │          │  │          │  │          │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│   Read log      Framework     Memory?       Fix root cause      │
│   Symbolicate   vs Native     Network?      Verify on device    │
│   Classify      vs Library    Bridge?       Check both OS       │
│                               Perf?         Prevent regression   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Crash Triage — Read the Crash Log

Before touching code, read the crash report end to end.

### 1.1 — Crash Log Anatomy

Every crash log tells you four things. Find all four before proceeding.

```
┌──────────────────────────────────────────────────────────────┐
│  CRASH LOG — WHAT TO EXTRACT                                 │
│                                                              │
│  1. Exception Type     What kind of crash?                   │
│     ─────────────────────────────────────                    │
│     SIGSEGV / EXC_BAD_ACCESS   → null pointer dereference    │
│     SIGABRT                    → assertion failure / abort    │
│     EXC_BREAKPOINT             → Swift/ObjC runtime trap     │
│     SIGBUS                     → misaligned memory access    │
│     java.lang.NullPointerException → null ref (Android)      │
│     java.lang.IllegalStateException → bad state transition   │
│     com.facebook.react.bridge.* → RN bridge error            │
│     Fatal Exception: FlutterError → Flutter framework crash  │
│                                                              │
│  2. Crashed Thread     Where did it crash?                   │
│     ─────────────────────────────────────                    │
│     Thread 0 (main)   → UI thread — blocked or bad access   │
│     Thread N (bg)     → Background work — race condition?    │
│     com.facebook.react.bridge → RN bridge thread             │
│     mqt_js             → RN JavaScript thread                │
│     io.flutter.worker  → Flutter engine worker               │
│                                                              │
│  3. Backtrace          What was the call chain?              │
│     ─────────────────────────────────────                    │
│     Read top 10 frames — find YOUR code, not system code     │
│     Symbolicated frame: MyApp.UserService.fetchUser():42     │
│     Unsymbolicated:     0x104a3b2c0 (need dSYM/source map)  │
│                                                              │
│  4. Context            What was happening?                   │
│     ─────────────────────────────────────                    │
│     App state: foreground / background / launching           │
│     Memory: normal / warning / critical                      │
│     Free disk: check for low storage                         │
│     OS version, device model, app version                    │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 — Symbolication

Unsymbolicated crash logs are useless. Symbolicate before reading.

| Platform | Tool | What You Need |
|----------|------|---------------|
| **iOS native** | `atos` or Xcode Organizer | dSYM file matching the build UUID |
| **Android native** | `ndk-stack` or `addr2line` | Unstripped `.so` files or mapping.txt |
| **React Native (Hermes)** | `hermes-profile-transformer` or Sentry source maps | Hermes bytecode source map (.hbc.map) |
| **React Native (JSC)** | Sentry or manual source map | JS bundle source map |
| **Flutter** | `flutter symbolize` | Debug symbols from `--split-debug-info` |

```bash
# iOS — symbolicate with atos
atos -arch arm64 -o MyApp.app.dSYM/Contents/Resources/DWARF/MyApp -l 0x104000000 0x104a3b2c0

# Android — symbolicate native crash
ndk-stack -sym ./app/build/intermediates/merged_native_libs/ -dump crash.txt

# Flutter — symbolicate
flutter symbolize -i crash_stack.txt -d ./build/app/outputs/symbols/
```

### 1.3 — Classify the Crash

| Crash Class | Signals / Exceptions | Common Cause | First Action |
|-------------|---------------------|--------------|-------------|
| **Null dereference** | SIGSEGV, EXC_BAD_ACCESS, NullPointerException | Accessing deallocated or nil object | Check object lifecycle, optional unwrapping |
| **Assertion / abort** | SIGABRT, IllegalStateException | Precondition failed, invalid state | Read assertion message — it tells you exactly what |
| **Out of memory** | Jetsam (iOS), OOM (Android), low memory warning | Memory leak or massive allocation | Take heap snapshot, find the growth |
| **Stack overflow** | EXC_BAD_ACCESS (SIGBUS) on stack guard page | Infinite recursion | Check recursive calls in backtrace |
| **Deadlock / ANR** | Watchdog timeout (iOS), ANR trace (Android) | Main thread blocked on lock or I/O | Analyze thread states — find the lock holder |
| **Bridge error** | RN: "Calling JS function after bridge torn down" | JS/native lifecycle mismatch | Check component unmount / bridge teardown order |
| **Serialization** | RN: "JSON value of type NSNull", Flutter: codec error | Type mismatch across bridge/channel | Verify data contracts on both sides |
| **Concurrency** | EXC_BAD_ACCESS (intermittent), ConcurrentModificationException | Thread-unsafe access | Check for shared state without synchronization |
| **Codec / format** | ImageIO error, MediaCodec error | Corrupt or unsupported media format | Validate input before decoding |
| **Third-party SDK** | Crash in vendor frames only | SDK bug, misconfiguration, version conflict | Check SDK release notes, open issue |

### 1.4 — Crash Triage Decision Tree

```
Crash report received
│
├── Is the crash log symbolicated?
│   └── NO → Symbolicate first (1.2), then continue
│
├── Read exception type
│   │
│   ├── SIGSEGV / EXC_BAD_ACCESS / NullPointerException
│   │   └── Null dereference → Check object lifecycle (Phase 3)
│   │
│   ├── SIGABRT / IllegalStateException / AssertionError
│   │   └── Read the assertion message — it's the answer
│   │
│   ├── Jetsam / OOM / "Memory pressure"
│   │   └── Memory leak → Phase 3: Memory Leak Detection
│   │
│   ├── Watchdog / ANR
│   │   └── Main thread blocked → Phase 3: ANR Analysis
│   │
│   ├── Bridge / Channel error
│   │   └── Cross-platform boundary → Phase 3: Bridge Debugging
│   │
│   └── Unknown / vendor frames only
│       └── Third-party SDK → check SDK issues, update, or isolate
│
├── Read crashed thread
│   ├── Main thread → UI or lifecycle issue
│   ├── Background thread → race condition or unsafe access
│   └── Bridge/engine thread → serialization or lifecycle issue
│
└── Check crash frequency
    ├── 100% of sessions → deterministic bug, easy to find
    ├── 1-10% of sessions → device/OS/data dependent
    └── < 1% → race condition or memory-dependent
```

**Output:** Crash classified, symbolicated, and a clear direction for Phase 2.

---

## Phase 2: Platform Isolation — Framework vs Native vs Library

Before diving deep, determine whose code is crashing.

### 2.1 — Isolation Strategy

```
┌──────────────────────────────────────────────────────────────┐
│                  ISOLATION DECISION TREE                      │
│                                                              │
│  Read the symbolicated backtrace. Where is your code?        │
│                                                              │
│  All frames are in YOUR app code                             │
│  └── Your bug. Trace it normally (Phase 3)                  │
│                                                              │
│  Top frames are in a third-party library                     │
│  └── Check library GitHub issues                            │
│      └── Known issue? → Apply workaround or update          │
│      └── Unknown? → Create minimal repro, file issue        │
│                                                              │
│  Top frames are in system/OS framework                       │
│  └── Your code called the system API wrong                  │
│      └── Check API docs for threading / lifecycle rules      │
│      └── Common: calling UIKit from background thread        │
│                                                              │
│  Top frames are in RN bridge / Flutter engine                │
│  └── Bridge/channel boundary issue                          │
│      └── Phase 3: Bridge Debugging                          │
│                                                              │
│  Crash only on one OS (iOS or Android)                       │
│  └── Platform-specific code path                            │
│      └── Check platform-specific native modules              │
│      └── Check OS version — API deprecated or changed?      │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 — Quick Isolation Tests

| Test | How | What It Proves |
|------|-----|----------------|
| **Same flow on other OS** | Run identical steps on iOS and Android | Platform-specific vs shared code |
| **Same flow on web** (RN) | Test in browser if web target exists | JS logic vs native bridge issue |
| **Comment out the library** | Remove the suspected library temporarily | Library vs your integration code |
| **Bare native app** | Write the same native call in a fresh Xcode/AS project | Your setup vs the API itself |
| **Downgrade library** | Rollback to last working version | Regression in library update |
| **Different device / OS** | Test on older/newer OS version | OS-specific API behavior |

**Output:** Clear answer: "This is a [framework / native / library / bridge] issue in [specific area]."

---

## Phase 3: Deep Trace — Category-Specific Debugging

### 3.1 — Memory Leak Detection

Memory leaks are the most common cause of production OOM crashes. They are invisible until the app has been running for minutes.

```
┌──────────────────────────────────────────────────────────────┐
│                MEMORY LEAK DETECTION FLOW                     │
│                                                              │
│  1. Establish baseline                                       │
│     → Launch app, navigate to suspect screen                 │
│     → Record memory (Xcode gauge / AS profiler / DevTools)   │
│                                                              │
│  2. Exercise the flow                                        │
│     → Navigate away and back 10 times                        │
│     → OR: scroll a long list up and down                     │
│     → OR: open and close a modal 10 times                    │
│                                                              │
│  3. Compare memory                                           │
│     → Memory should return to near-baseline after nav away   │
│     → If it grows with each cycle, there is a leak           │
│                                                              │
│  4. Take heap snapshots                                      │
│     → Snapshot A: before exercising                          │
│     → Snapshot B: after exercising                           │
│     → Compare: which objects grew?                           │
│                                                              │
│  5. Find the retainer                                        │
│     → Who is holding a reference to the leaked object?       │
│     → Follow the retain chain until you find YOUR code       │
└──────────────────────────────────────────────────────────────┘
```

**Common leak patterns by platform:**

| Platform | Pattern | Cause | Fix |
|----------|---------|-------|-----|
| **React Native** | Unremoved event listener | `addListener` without `removeListener` in cleanup | Return cleanup from `useEffect` |
| **React Native** | Timer not cleared | `setInterval` / `setTimeout` surviving unmount | Clear in `useEffect` cleanup |
| **React Native** | Closure capturing component | Async callback holding stale component ref | Use `useRef` for mutable refs, check mounted |
| **iOS (Swift)** | Strong reference cycle | Delegate or closure capturing `self` strongly | Use `[weak self]` in closures, `weak var delegate` |
| **iOS (ObjC)** | Retain cycle in blocks | Block capturing `self` in a property that `self` owns | Use `__weak typeof(self) weakSelf = self` |
| **iOS** | NotificationCenter observer not removed | Observer registered but never deregistered | Remove in `deinit` or `viewWillDisappear` |
| **Android** | Activity leak via inner class | Non-static inner class holds implicit Activity ref | Use `WeakReference<Activity>` or static inner class |
| **Android** | Context leak in singleton | Singleton holding Activity context | Use `applicationContext`, never Activity context |
| **Android** | Handler leak | Handler with implicit Activity reference | Use `WeakReference` in Handler, remove callbacks |
| **Flutter** | Stream not closed | `StreamController` without `.close()` in `dispose` | Call `controller.close()` in `dispose()` |
| **Flutter** | AnimationController leak | Controller not disposed | Call `controller.dispose()` in `dispose()` |
| **Flutter** | Timer not cancelled | `Timer.periodic` surviving widget dispose | Cancel in `dispose()` |

### 3.2 — Network Debugging

When API calls fail on mobile but work elsewhere.

```
┌──────────────────────────────────────────────────────────────┐
│                NETWORK DEBUG CHECKLIST                        │
│                                                              │
│  1. Can the device reach the server at all?                  │
│     → curl / ping from device or emulator                   │
│     → Check cellular vs WiFi behavior                        │
│     → Check VPN/proxy interference                           │
│                                                              │
│  2. Is SSL/TLS working?                                      │
│     → Certificate pinning enabled? Cert up to date?          │
│     → Self-signed cert in staging? ATS exception on iOS?     │
│     → Network security config on Android?                    │
│                                                              │
│  3. Is the request correct?                                  │
│     → Use Charles Proxy / Proxyman to inspect                │
│     → Check headers: Auth token present? Content-Type?       │
│     → Check body: serialization correct? Encoding?           │
│                                                              │
│  4. Is the response handled correctly?                       │
│     → Check status code handling (not just 200)              │
│     → Check timeout handling (mobile networks are slow)      │
│     → Check offline / no-connectivity handling               │
│                                                              │
│  5. Is retry logic working?                                  │
│     → Exponential backoff? Max retries?                      │
│     → Idempotency — safe to retry POST requests?            │
└──────────────────────────────────────────────────────────────┘
```

**Proxy setup for mobile debugging:**

| Tool | Platform | Setup |
|------|----------|-------|
| **Charles Proxy** | iOS/Android | Set device proxy to Mac IP:8888, install Charles root cert on device |
| **Proxyman** | iOS/Android | Same as Charles, or use Proxyman iOS companion app |
| **Flipper (Network)** | React Native | Built-in — enable network plugin in Flipper desktop |
| **Flutter DevTools** | Flutter | Built-in network tab in DevTools |
| **mitmproxy** | Any | CLI-based, scriptable proxy for automated inspection |

### 3.3 — Performance Debugging (Jank, Frame Drops, Slow Renders)

```
┌──────────────────────────────────────────────────────────────┐
│              PERFORMANCE DEBUG DECISION TREE                  │
│                                                              │
│  App is slow / janky / dropping frames                       │
│  │                                                           │
│  ├── Is the UI thread blocked?                               │
│  │   │                                                       │
│  │   ├── YES (frames > 16ms)                                │
│  │   │   ├── Heavy computation on main thread?              │
│  │   │   │   └── Move to background thread / worker         │
│  │   │   ├── Synchronous I/O on main thread?                │
│  │   │   │   └── Make async, use background queue           │
│  │   │   ├── Too many views / deep hierarchy?               │
│  │   │   │   └── Flatten layout, use lazy loading           │
│  │   │   └── Expensive layout pass?                         │
│  │   │       └── Cache layout, avoid relayout triggers      │
│  │   │                                                       │
│  │   └── NO (frames fine but app feels slow)                │
│  │       ├── Network requests slow?                          │
│  │       │   └── Add loading states, prefetch, cache         │
│  │       ├── Navigation transitions janky?                   │
│  │       │   └── Use native navigation, reduce transition   │
│  │       └── Images loading slowly?                          │
│  │           └── Resize, compress, cache, progressive load   │
│  │                                                           │
│  └── Is memory growing?                                      │
│      └── YES → Memory leak, see 3.1                         │
└──────────────────────────────────────────────────────────────┘
```

**Platform-specific profiling tools:**

| What to Measure | React Native | Flutter | iOS Native | Android Native |
|----------------|-------------|---------|-----------|---------------|
| Frame rate | Flipper Perf plugin, `__DEV__` perf monitor | `flutter run --profile`, DevTools timeline | Instruments: Core Animation | Android Studio: GPU rendering |
| CPU time | Hermes profiler (`.cpuprofile`) | DevTools CPU profiler | Instruments: Time Profiler | Android Studio CPU profiler |
| Memory | Flipper (Hermes heap) + Xcode/AS gauges | DevTools memory tab | Instruments: Allocations | Android Studio Memory profiler |
| Renders | React DevTools Profiler | `debugPrintRebuildDirtyWidgets` | View Debugging | Layout Inspector |
| JS bundle | `react-native-bundle-visualizer` | `--analyze-size` flag | N/A | N/A |

### 3.4 — Bridge / Channel Debugging

The native-to-JS (React Native) or native-to-Dart (Flutter) boundary is the most fragile part of a cross-platform app.

```
┌──────────────────────────────────────────────────────────────┐
│               BRIDGE ERROR DECISION TREE                     │
│                                                              │
│  Error at the bridge/channel boundary                        │
│  │                                                           │
│  ├── "Calling JS function after bridge torn down" (RN)      │
│  │   └── Native module calling into JS after app closed     │
│  │       → Check: native callback firing after unmount      │
│  │       → Fix: guard with bridge.isValid / mounted check   │
│  │                                                           │
│  ├── "JSON value of type NSNull is not supported" (RN)      │
│  │   └── Native returning null where JS expects a value     │
│  │       → Fix: handle null on native side before sending   │
│  │                                                           │
│  ├── "MissingPluginException" (Flutter)                     │
│  │   └── Platform channel registered on wrong side          │
│  │       → Check: channel name exact match, registered in   │
│  │         correct lifecycle callback                        │
│  │                                                           │
│  ├── "StandardMethodCodec: unknown type" (Flutter)          │
│  │   └── Unsupported type passed through channel            │
│  │       → Fix: use only supported types (String, int,      │
│  │         double, bool, List, Map, Uint8List, null)         │
│  │                                                           │
│  ├── "Thread violation" / "UI API called from bg thread"    │
│  │   └── Native callback delivering on wrong thread         │
│  │       → Fix: dispatch to main thread before UI calls     │
│  │                                                           │
│  └── Crash with no JS/Dart stack trace                      │
│      └── Pure native crash in a native module               │
│          → Symbolicate native crash separately               │
│          → Check native module source code directly          │
└──────────────────────────────────────────────────────────────┘
```

### 3.5 — ANR / App Not Responding Analysis

ANR means the main thread was blocked for 5+ seconds (Android) or the watchdog killed the app (iOS).

```
┌──────────────────────────────────────────────────────────────┐
│                   ANR ANALYSIS FLOW                           │
│                                                              │
│  1. Get the ANR trace                                        │
│     → Android: /data/anr/traces.txt or Play Console ANR tab │
│     → iOS: MetricKit hang diagnostic or Xcode Organizer     │
│                                                              │
│  2. Find the main thread in the trace                        │
│     → Look for "main" or thread 0                           │
│     → Read its stack — what is it stuck on?                 │
│                                                              │
│  3. Classify the block                                       │
│     │                                                        │
│     ├── Waiting on lock/synchronized                        │
│     │   → Find who holds the lock (check other threads)     │
│     │   → Deadlock? Two threads waiting on each other?      │
│     │                                                        │
│     ├── Synchronous disk/network I/O                        │
│     │   → SharedPreferences.commit() on main thread         │
│     │   → Synchronous HTTP call on main thread              │
│     │   → File read/write on main thread                    │
│     │                                                        │
│     ├── Expensive computation                                │
│     │   → JSON parsing large payload on main thread         │
│     │   → Image processing on main thread                   │
│     │   → Database query on main thread                     │
│     │                                                        │
│     └── Binder / IPC bottleneck (Android)                   │
│         → Too many binder calls in sequence                 │
│         → ContentProvider query on main thread              │
│                                                              │
│  4. Fix: move the blocking work off the main thread          │
│     → Use async/await, background queues, coroutines        │
│     → Never hold a lock that a main-thread caller needs     │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 4: Fix & Verify on Device

### 4.1 — Plan the Fix

```
┌──────────────────────────────────────────────────────────────┐
│  MOBILE FIX PLANNING CHECKLIST                               │
│                                                              │
│  [ ] What is the minimal change to fix this?                │
│  [ ] Does the fix need to ship as a hotfix or normal cycle? │
│  [ ] Does this affect both iOS and Android?                 │
│  [ ] Is a native code change required (new app store build)?│
│  [ ] Can this be fixed with an OTA update (CodePush/Expo)?  │
│  [ ] Does the fix require a migration or server change?     │
│  [ ] Are there cached/stale versions of the old code on     │
│      user devices?                                           │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 — Verification Checklist

```
┌──────────────────────────────────────────────────────────────┐
│            MOBILE VERIFICATION CHECKLIST                      │
│                                                              │
│  The Crash                                                   │
│  [ ] Original crash no longer occurs (exact repro steps)    │
│  [ ] Tested on real device, not just simulator              │
│  [ ] Tested on both iOS and Android (if cross-platform)     │
│  [ ] Tested on minimum supported OS version                 │
│                                                              │
│  No Regressions                                              │
│  [ ] Related features still work                            │
│  [ ] Navigation flow still correct                          │
│  [ ] No new crash clusters in crash reporter                │
│  [ ] No new ANR traces                                      │
│                                                              │
│  Performance                                                 │
│  [ ] Memory usage stable (no growth over 10 cycles)         │
│  [ ] Frame rate acceptable (no new jank)                    │
│  [ ] App launch time not degraded                           │
│                                                              │
│  Edge Cases                                                  │
│  [ ] Works with no network                                  │
│  [ ] Works after app backgrounded and resumed               │
│  [ ] Works after device rotation (if applicable)            │
│  [ ] Works with low memory warning simulated                │
│  [ ] Works on low-end test device                           │
└──────────────────────────────────────────────────────────────┘
```

### 4.3 — Commit the Fix

```bash
# Stage only the fix files
git add <specific-files>

# Commit with clear mobile-specific context
git commit -m "fix(ios): resolve retain cycle in UserProfileVC causing OOM

UserProfileVC held a strong reference to the location manager delegate
closure, preventing deallocation on navigation. After 15+ screen visits,
memory exceeded 1.2GB triggering Jetsam kill.

Changed closure capture to [weak self] and added nil guard.
Verified memory stable at ~180MB over 30 navigation cycles on iPhone SE.

Crash cluster: CRASH-4821 (Firebase Crashlytics)"
```

---

## Common Crash Patterns — Quick Reference

| # | Pattern | Symptoms | Platform | Cause | Fix |
|---|---------|----------|----------|-------|-----|
| 1 | **Force unwrap nil** | EXC_BREAKPOINT in Swift | iOS | `value!` on nil Optional | Use `guard let` / `if let` |
| 2 | **Main thread UI access** | SIGABRT, purple warning | iOS/Android | UI update from background thread | Dispatch to main queue/thread |
| 3 | **Bridge torn down** | "Calling JS after bridge torn down" | React Native | Native callback after unmount | Guard with `bridge.isValid` |
| 4 | **Missing Activity** | NullPointerException on `getActivity()` | RN Android | Fragment detached from Activity | Null-check `getActivity()` |
| 5 | **OOM - image loading** | Jetsam / OOM kill | All | Loading full-res images into memory | Downsample, use image cache library |
| 6 | **Retain cycle** | Memory grows, eventual Jetsam | iOS | Strong ref cycle in closure/delegate | `[weak self]`, weak delegate |
| 7 | **Activity context in singleton** | Activity leak, eventual OOM | Android | Singleton holds Activity reference | Use `applicationContext` |
| 8 | **Timer not cleared** | Memory leak, phantom callbacks | RN/Flutter | `setInterval` / `Timer.periodic` lives past unmount | Clear in cleanup / `dispose()` |
| 9 | **Codec null value** | "NSNull is not supported" | React Native | Native returning null to JS | Handle null before bridge send |
| 10 | **Platform channel mismatch** | MissingPluginException | Flutter | Channel name mismatch or not registered | Verify exact channel name on both sides |
| 11 | **Background fetch crash** | Crash in bg, no user-visible error | iOS | Background task exceeds time limit | Call `endBackgroundTask` before expiry |
| 12 | **ProGuard stripped class** | ClassNotFoundException | Android | ProGuard removed class used via reflection | Add `-keep` rule for the class |
| 13 | **Keyboard dismiss crash** | EXC_BAD_ACCESS during dismiss | iOS/RN | Deallocated responder in keyboard chain | Resign first responder before dealloc |
| 14 | **Deep link crash** | Crash on cold start from deep link | All | Navigation attempted before stack ready | Queue deep link, process after nav ready |
| 15 | **WebView memory** | OOM after heavy WebView use | All | WebView caching aggressively | Clear WebView cache, limit concurrent instances |
| 16 | **Animation controller leak** | Memory grows with each screen | Flutter | AnimationController not disposed | Call `.dispose()` in `dispose()` |
| 17 | **SharedPrefs on main thread** | ANR on Android | Android | `.commit()` blocks main thread | Use `.apply()` (async) instead |
| 18 | **Large JSON parse** | ANR / freeze | All | Parsing multi-MB JSON on main thread | Parse on background thread / isolate |
| 19 | **SSL pinning failure** | All network requests fail silently | All | Certificate rotated but pin not updated | Update pin, add backup pin |
| 20 | **Index out of bounds** | ArrayIndexOutOfBoundsException | All | List/array access without bounds check | Bounds check before access |
| 21 | **Concurrent modification** | ConcurrentModificationException | Android | Iterating list while another thread modifies | Use `CopyOnWriteArrayList` or sync |
| 22 | **Push notification crash** | Crash when notification received in bg | All | Notification handler accesses UI/dead state | Guard handler, check app state |

---

## Crash Log Reading Guide — Annotated Examples

### iOS Crash Log

```
┌──────────────────────────────────────────────────────────────┐
│  Exception Type:  EXC_BAD_ACCESS (SIGSEGV)          ← TYPE  │
│  Exception Subtype: KERN_INVALID_ADDRESS at 0x0     ← NULL  │
│  Triggered by Thread: 0                             ← MAIN  │
│                                                              │
│  Thread 0 Crashed:                                           │
│  0  MyApp       0x104a3b2c0  -[UserVC viewDidLoad] + 128    │
│  1  UIKitCore   0x1a2f3c4d8  -[UIViewController ...] + 92   │
│  2  UIKitCore   0x1a2f3c2a0  -[UIViewController ...] + 48   │
│  ...                                                         │
│                                                              │
│  Read: Null pointer access in UserVC.viewDidLoad on main     │
│  thread. Likely accessing an IBOutlet or property that is    │
│  nil at load time.                                           │
└──────────────────────────────────────────────────────────────┘
```

### Android ANR Trace

```
┌──────────────────────────────────────────────────────────────┐
│  "main" prio=5 tid=1 Blocked                        ← STATE │
│    at com.app.db.UserDao.getAll(UserDao.java:42)             │
│    - waiting to lock <0x0a1b2c3d> held by thread 14  ← LOCK │
│    at com.app.ui.HomeActivity.onResume(Home.java:88)         │
│                                                              │
│  "AsyncTask #3" prio=5 tid=14 Runnable                       │
│    at com.app.db.UserDao.bulkInsert(UserDao.java:67)         │
│    - locked <0x0a1b2c3d>                            ← HOLDER│
│                                                              │
│  Read: Main thread blocked waiting for DB lock held by       │
│  AsyncTask doing bulk insert. Classic deadlock via           │
│  synchronized database access. Fix: never lock DB on main.  │
└──────────────────────────────────────────────────────────────┘
```

### React Native Bridge Error

```
┌──────────────────────────────────────────────────────────────┐
│  Fatal Exception: RCTFatalException                          │
│  Calling JS function after bridge has been torn down ← TYPE  │
│                                                              │
│  Native stack:                                               │
│  0  MyApp  RCTModuleMethod invokeWithBridge:module:args:     │
│  1  MyApp  -[CameraModule onFrameCaptured:]                  │
│  2  AVFoundation  -[AVCaptureSession ...]                    │
│                                                              │
│  Read: CameraModule is delivering frames via a native        │
│  callback after the React Native bridge has been destroyed   │
│  (user navigated away or app is closing). The camera session │
│  must be stopped before the bridge tears down.               │
└──────────────────────────────────────────────────────────────┘
```

---

## Quick Reference — The 4 Phases

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. CRASH TRIAGE  →  Read crash log end to end          │
│                      Symbolicate, classify, extract     │
│                      exception type + thread + context  │
│                                                         │
│  2. ISOLATE       →  Framework vs native vs library     │
│                      Test on other OS, comment out libs  │
│                      Find whose code is actually broken  │
│                                                         │
│  3. DEEP TRACE    →  Memory? Network? Bridge? Perf?     │
│                      Use platform-specific profilers     │
│                      Follow the data to the exact line  │
│                                                         │
│  4. FIX & VERIFY  →  Minimal fix, test on real device   │
│                      Both platforms, edge cases          │
│                      Memory stable, no new jank          │
│                      Commit with crash cluster ID        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Tips for Best Results

1. **Symbolicate before reading** — An unsymbolicated crash log is a wall of hex addresses. Spend the time to set up symbolication pipelines for every build you ship.
2. **Test on low-end devices** — The iPhone SE 2nd gen and a $150 Android device will expose crashes that never appear on flagship hardware. Keep one on your desk.
3. **Check the bridge first** — In cross-platform apps, the native/JS or native/Dart boundary is the single most common crash location. Start there.
4. **Memory leaks compound** — A 2MB leak per screen visit means OOM after 500 visits. On a 2GB device, that is 40 minutes of use. Profile early.
5. **Read the other threads** — The crashed thread shows where the app died, but the cause is often in another thread holding a lock or corrupting shared state.
6. **Crash frequency matters** — A 100% crash is easy to find. A 0.1% crash is a race condition, memory-dependent, or device-specific. Adjust your strategy accordingly.
7. **Keep a crash pattern library** — Every crash you solve goes into a team knowledge base. The same patterns repeat across projects and years.

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
