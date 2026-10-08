---
name: ios-performance
description: >
  iOS performance optimization expert skill covering memory management (ARC, retain cycles, weak/unowned,
  value vs reference types, copy-on-write), SwiftUI performance (view identity, @Observable vs ObservableObject,
  lazy containers, EquatableView, image caching), Instruments profiling (Time Profiler, Allocations, Leaks,
  Energy Log, Core Animation, SwiftUI instrument), app launch optimization, network performance, battery
  optimization, build performance, and common anti-patterns. Use this skill whenever the user optimizes
  iOS app performance, investigates memory leaks, profiles with Instruments, improves launch time, or
  fixes frame drops. Triggers on: performance, memory leak, retain cycle, ARC, weak self, profiling,
  Instruments, Time Profiler, Allocations, frame rate, FPS, launch time, battery, energy, optimization,
  slow, lag, freeze, hang, jank, memory pressure, CPU usage, build time, compile time, app size,
  or any iOS performance question.
---

# iOS Performance Optimization Skill

## Core Rules

1. **Use `[weak self]` in escaping closures by default** — use `[unowned self]` only when the closure's lifetime is strictly shorter than the captured object (e.g., parent owns child, child's closure references parent).
2. **Non-escaping closures do NOT need `[weak self]`** — `map`, `filter`, `forEach`, `reduce`, `compactMap`, `sorted(by:)` are non-escaping. The closure executes synchronously and releases captures immediately.
3. **Delegates must be `weak var`** — the delegate protocol must conform to `AnyObject` (or be marked `@objc`). Strong delegates create retain cycles between owner and delegate.
4. **Use `@Observable` over `ObservableObject`** (iOS 17+) — `@Observable` tracks property access per-view, so only views reading a changed property re-evaluate. `ObservableObject` with `@Published` invalidates ALL observing views on ANY published property change.
5. **Break SwiftUI views into small subviews** — each subview localizes its state dependency, so changes only re-evaluate the subview, not the entire parent body.
6. **Use `LazyVStack`/`LazyHStack` inside `ScrollView` for large collections** — `VStack` evaluates ALL children upfront. Use `List` for very large datasets (10,000+) since it reuses cells.
7. **Use `.task` modifier instead of `.onAppear` + `Task {}`** — `.task` automatically cancels when the view disappears. Use `.task(id:)` to restart when a dependency changes.
8. **Profile with Instruments BEFORE optimizing** — measure first, optimize second. Never guess where the bottleneck is.
9. **Never block the main thread** — all file I/O, network calls, JSON decoding of large payloads, image processing, and database queries must run off the main thread.
10. **Reuse expensive objects** — `URLSession`, `DateFormatter`, `JSONDecoder`, `NumberFormatter`, `NSRegularExpression` are expensive to create. Use shared instances or caches.

## Performance Targets

| Metric | Target | Critical Threshold |
|--------|--------|--------------------|
| Cold launch | <400ms to first frame | >2s triggers watchdog kill |
| Warm launch | <200ms | >1s feels broken |
| Frame rate | 60 FPS (120 on ProMotion) | <45 FPS is noticeable jank |
| Frame budget | 16.67ms (8.33ms at 120Hz) | >33ms = visible dropped frame |
| Memory (typical) | <100MB resident | >500MB risks jetsam on older devices |
| Memory (spike) | <200MB peak | Varies by device class |
| CPU idle | <3% | >5% drains battery |
| CPU active task | <80% sustained | 100% = thermal throttling |
| API response (perceived) | <200ms | >1s needs loading indicator |
| App size (download) | <50MB (OTA limit: 200MB) | >200MB requires Wi-Fi |
| Disk writes | <1MB/min sustained | Excessive writes degrade flash |

## Quick Diagnosis Guide

| Symptom | Instrument / Tool | Likely Cause | First Action |
|---------|-------------------|-------------|--------------|
| UI freezes / hangs | Time Profiler | Main thread blocking (sync I/O, heavy computation) | Check main thread call stack |
| Memory grows over time | Allocations + Memory Graph | Retain cycle or unbounded cache | Take heap snapshots, compare generations |
| Sudden memory spike | Allocations (VM Tracker) | Large image decode, bulk data load | Check transient allocations |
| Purple "memory" warning | Memory Graph Debugger | Retain cycle between objects | Trace reference chains |
| Dropped frames | Core Animation instrument | Offscreen rendering, layer blending | Enable "Color Blended Layers" |
| Battery drain | Energy Log | Excessive CPU, location, network polling | Check CPU/network wake frequency |
| Slow cold launch | App Launch instrument | Too many dylibs, heavy `+load`/`init`, sync main | Profile pre-main vs post-main |
| Slow scrolling (SwiftUI) | SwiftUI instrument | Non-lazy stacks, excessive redraws | Check body evaluation count |
| Slow scrolling (UIKit) | Time Profiler + Core Animation | Cell height calculation, offscreen rendering | Profile `cellForRow` time |
| Network slow | Network instrument | No HTTP/2 reuse, large payloads, no compression | Check connection count and sizes |
| Build slow | Xcode build timeline | Type inference, large files, no parallelism | Add `-warn-long-function-bodies` |

## Memory Management Quick Reference

```swift
// CORRECT: [weak self] in escaping closure
func fetchData() {
    networkService.fetch { [weak self] result in
        guard let self else { return }
        self.update(with: result)
    }
}

// CORRECT: [unowned self] ONLY when lifetime is guaranteed
class Parent {
    lazy var handler: () -> Void = { [unowned self] in
        self.doSomething()  // Parent always outlives its own lazy property
    }
}

// NOT NEEDED: Non-escaping closure — no capture cycle possible
let names = users.map { $0.name }          // map is non-escaping
let adults = users.filter { $0.age >= 18 } // filter is non-escaping
items.forEach { print($0) }                // forEach is non-escaping

// CORRECT: Weak delegate
protocol DataServiceDelegate: AnyObject {
    func didUpdate(_ data: Data)
}

class DataService {
    weak var delegate: DataServiceDelegate?
}
```

## SwiftUI Performance Quick Reference

```swift
// BAD: One large view — any state change re-evaluates entire body
struct ProfileView: View {
    @State private var name = ""
    @State private var bio = ""
    @State private var avatarURL: URL?
    @State private var posts: [Post] = []

    var body: some View {
        ScrollView {
            avatarSection     // Change to name re-evaluates avatar too
            bioSection
            postsSection      // All 500 post cells re-evaluated
        }
    }
}

// GOOD: Extracted subviews — state changes localized
struct ProfileView: View {
    var body: some View {
        ScrollView {
            AvatarSection()   // Only re-evaluates when avatar changes
            BioSection()      // Only re-evaluates when bio changes
            PostsSection()    // Only re-evaluates when posts change
        }
    }
}

// GOOD: LazyVStack for scrollable content
struct PostsSection: View {
    let posts: [Post]

    var body: some View {
        LazyVStack {  // Only creates visible cells + prefetch buffer
            ForEach(posts) { post in
                PostRow(post: post)
            }
        }
    }
}

// GOOD: .task with auto-cancellation
struct UserDetailView: View {
    let userID: String
    @State private var user: User?

    var body: some View {
        content
            .task(id: userID) {  // Cancels & restarts if userID changes
                user = try? await api.fetchUser(userID)
            }
    }
}
```

## @Observable vs ObservableObject

```swift
// OLD (iOS 14+): ObservableObject — ALL views re-evaluate on ANY change
class UserViewModel: ObservableObject {
    @Published var name = ""       // Change triggers ALL observers
    @Published var email = ""      // Change triggers ALL observers
    @Published var avatarURL: URL? // Change triggers ALL observers
}

// NEW (iOS 17+): @Observable — only views reading changed property re-evaluate
@Observable
class UserViewModel {
    var name = ""       // Only views reading `name` re-evaluate
    var email = ""      // Only views reading `email` re-evaluate
    var avatarURL: URL? // Only views reading `avatarURL` re-evaluate
}
```

## Instruments Workflow

### Step 1: Profile, Don't Debug
Always profile on a **real device** (not Simulator). Use **Release** configuration for accurate measurements.

### Step 2: Choose the Right Instrument
- **Time Profiler** — CPU bottlenecks, main thread blocking
- **Allocations** — memory growth, leaks, allocation hotspots
- **Leaks** — automatic retain cycle detection (periodic snapshots)
- **Memory Graph Debugger** (Xcode, not Instruments) — visual reference chains
- **Core Animation** — rendering performance, blended layers, offscreen rendering
- **Energy Log** — battery drain causes (CPU, network, GPS, Bluetooth)
- **Network** — HTTP request/response analysis
- **App Launch** — cold/warm launch breakdown
- **SwiftUI** (Xcode 16+) — view body evaluations, cause & effect graph

### Step 3: Time Profiler Settings (Always Set These)
1. **Invert Call Tree** — shows heaviest leaf functions first
2. **Separate by Thread** — isolates main thread work
3. **Hide System Libraries** — focuses on your code
4. **Separate by State** — shows running vs blocked time

### Step 4: Record, Reproduce, Analyze
1. Record for 10-30 seconds covering the problematic interaction
2. Select the time range of interest
3. Look at the heaviest stack traces
4. Focus on main thread first (Thread 1)

## App Launch Optimization Checklist

### Pre-main Phase (<200ms target)
- [ ] Max 6 non-system dynamic frameworks (each adds ~10-20ms)
- [ ] No `+load` methods in ObjC code (move to `+initialize` or lazy init)
- [ ] Minimize static initializers (C++ globals, `__attribute__((constructor))`)
- [ ] Use static linking where possible (SPM default)

### Post-main Phase (<200ms target)
- [ ] Defer non-essential initialization (analytics, logging, feature flags)
- [ ] Use `lazy var` for expensive properties
- [ ] Load first screen data from cache, then refresh from network
- [ ] Avoid synchronous network calls at launch
- [ ] Minimize work in `application(_:didFinishLaunchingWithOptions:)`
- [ ] Use `Scene` phase detection instead of heavy AppDelegate setup

## Common Anti-Patterns

### 1. Main Thread Blocking
```swift
// BAD: Synchronous file read on main thread
let data = try! Data(contentsOf: largeFileURL)

// GOOD: Async file read
let data = try await Task.detached {
    try Data(contentsOf: largeFileURL)
}.value
```

### 2. Excessive Allocations in Loops
```swift
// BAD: Creates new DateFormatter per iteration (expensive!)
for event in events {
    let formatter = DateFormatter()
    formatter.dateFormat = "yyyy-MM-dd"
    labels.append(formatter.string(from: event.date))
}

// GOOD: Reuse formatter
let formatter = DateFormatter()
formatter.dateFormat = "yyyy-MM-dd"
for event in events {
    labels.append(formatter.string(from: event.date))
}
```

### 3. VStack for Large Collections
```swift
// BAD: Creates ALL 10,000 views upfront
ScrollView {
    VStack {
        ForEach(items) { item in  // 10,000 items = 10,000 views in memory
            ItemRow(item: item)
        }
    }
}

// GOOD: Only creates visible views
ScrollView {
    LazyVStack {
        ForEach(items) { item in  // ~20 views in memory at a time
            ItemRow(item: item)
        }
    }
}
```

### 4. Retaining Self in Timers
```swift
// BAD: Timer retains self, self retains timer → cycle
class PollingService {
    var timer: Timer?

    func start() {
        timer = Timer.scheduledTimer(withTimeInterval: 5, repeats: true) { _ in
            self.poll()  // Strong capture → retain cycle
        }
    }
}

// GOOD: Weak capture
func start() {
    timer = Timer.scheduledTimer(withTimeInterval: 5, repeats: true) { [weak self] _ in
        self?.poll()
    }
}
```

### 5. Not Cancelling Tasks
```swift
// BAD: Task keeps running after view disappears
.onAppear {
    Task {
        while !Task.isCancelled {
            await refresh()
            try await Task.sleep(for: .seconds(30))
        }
    }
}

// GOOD: .task auto-cancels on disappear
.task {
    while !Task.isCancelled {
        await refresh()
        try? await Task.sleep(for: .seconds(30))
    }
}
```

## Reference Files

For deep dives, see:
- `references/memory.md` — ARC, retain cycles, value vs reference types, copy-on-write, debugging
- `references/swiftui-perf.md` — View identity, @Observable, lazy containers, images, .task
- `references/instruments.md` — Time Profiler, Allocations, Leaks, Energy, Core Animation, SwiftUI instrument
- `references/optimization.md` — App launch, network, battery, build performance, anti-patterns
