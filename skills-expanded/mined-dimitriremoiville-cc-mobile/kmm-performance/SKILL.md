---
name: kmm-performance
description: Performance patterns for the shared Kotlin Multiplatform module — Darwin dispatcher choice, ObjC interop allocation costs, Flow/StateFlow bridging into SwiftUI, framework-link size, kotlinx.serialization cost, Ktor engine overhead. Load when investigating shared-module latency, iOS bridging regressions, or shrinking the iOS framework.
---

# KMM performance

The shared module's performance story is not the same on the two platforms. JVM/Android perf advice is in `android-performance`; this skill covers what is *specifically* a KMP / Darwin concern.

## Measure first

Every optimization here needs a number from the *consuming* side:

- **Android:** Macrobenchmark + Perfetto from the app module — same as `android-performance`. The shared module's cost shows up as time inside repository/use-case frames.
- **iOS:** Instruments (Time Profiler + Allocations). The shared module appears as `libshared.dylib` frames; Kotlin function names are demangled when the framework ships debug symbols.

Numbers from a JVM benchmark in `commonTest` do **not** predict iOS performance — the Darwin runtime, GC model, and bridging cost are all different. Run on a device, not a simulator.

## Dispatcher choice on Darwin

`Dispatchers.IO` on Darwin is backed by a `kotlinx.coroutines` worker pool, **not** the platform GCD. For most repository work this is fine, but:

- **UI work** must hop to `Dispatchers.Main`, which on Darwin is the main `NSRunLoop`. Failing to do so will silently break SwiftUI updates.
- **Heavy CPU work** (parsing, crypto) on `Dispatchers.Default` is fine; don't reach for GCD via cinterop just to "be native."
- **Avoid `runBlocking` in iOS-facing APIs.** It blocks the main thread when called from Swift unless you've explicitly hopped off it. Use suspend functions and let Swift `await` them.

## ObjC interop allocation costs

Every Kotlin object crossing the boundary into Swift incurs a wrapper allocation. Hot paths to watch:

- **Per-frame conversions.** A `StateFlow<List<Item>>` emitting 60 times/sec creates 60 list wrappers + N item wrappers each. Either throttle on the Kotlin side (`sample(16.milliseconds)`) or expose a coarser API.
- **Sealed-class hierarchies as enums.** Each Kotlin sealed subclass becomes a separate ObjC class — pattern-matching in Swift requires `is`/`as?` casts that allocate. For tight loops, prefer a plain `enum class` with a single payload field.
- **`Long` and `Int` boxing.** `Int` (32-bit) on iOS maps to `KotlinInt` (boxed) when crossing the boundary, not `Int32`. For numeric-heavy APIs, expose `IntArray`/`LongArray` or use cinterop, not `List<Int>`.

Measure with Instruments → Allocations, filter by `Kotlin*` class names.

## Flow / StateFlow bridging into SwiftUI

The shared ViewModel exposes `StateFlow<UiState>`; SwiftUI doesn't speak `Flow` natively. Two patterns:

1. **`SKIE` / Touchlab `KMP-NativeCoroutines`** — generates `AsyncSequence` wrappers. Pay the codegen cost once, get idiomatic Swift.
2. **Hand-rolled `@Published` bridge** — a small Swift `ObservableObject` that subscribes to the `StateFlow` via a `Cancellable`. Cheaper, no plugin, but you write the wrapper per ViewModel.

Whichever you pick, **do not** call `collect { }` from Swift in a `Task { }` without storing the `Task` — leaked tasks compound and the main thread will eventually stutter.

For one-shot events (`Channel<UiEvent>` exposed as `receiveAsFlow`), prefer a single `subscribe(onEach:)` Swift extension that takes ownership of the cancellation; don't bridge through `@Published` (events get coalesced).

## Framework link size

Every Kotlin dependency you add ships in the iOS framework binary. Three levers:

- **Audit transitively.** `./gradlew :shared:linkReleaseFrameworkIosArm64` then `du -sh shared/build/bin/iosArm64/releaseFramework/shared.framework/shared`. Compare before/after when adding a dep.
- **`isStatic = false`** when the framework is consumed via SPM/CocoaPods *and* the app embeds a Swift wrapper that itself links transitive deps — saves duplicated symbols.
- **Strip unused targets.** If you don't ship `iosX64` or `iosSimulatorArm64`, don't build them on release CI.

Targets to watch: anything pulling JVM reflection (`kotlin-reflect`), JSON libraries other than `kotlinx.serialization`, logging frameworks that include their own coroutine support.

## kotlinx.serialization cost

JSON parsing on Darwin is consistently 2-4× slower than on a comparable Android device for the same payload, because the Darwin Kotlin runtime has no equivalent of ART's JIT. Mitigations:

- **Lazy fields.** `@Transient` + manual decode for fields you rarely read.
- **Streaming for large payloads.** `Json.decodeToSequence` over `decodeFromString` for arrays > 1 MB.
- **Cache the `Json { }` instance.** Constructing it allocates and configures a non-trivial graph.

## Ktor engine overhead

- **Android engine:** `OkHttp`. Same characteristics as `retrofit-networking` — connection pooling, HTTP/2 multiplexing for free.
- **Darwin engine:** `NSURLSession`. Defaults are fine, but the per-request `URLSessionConfiguration` allocation isn't free. Reuse a single `HttpClient` instance for the app lifetime; don't create one per repository.

`HttpClient` is thread-safe by design; inject the same instance via Koin everywhere.

## Cold-start cost on iOS

The shared framework's first invocation pays for:

1. Kotlin runtime initialization (`kotlin.native.runtime.GC` warmup, class table setup).
2. Koin module graph construction (if your `startKoin { }` is on the main thread of `application(_:didFinishLaunchingWithOptions:)`).
3. First `HttpClient` instantiation (TLS setup, NSURLSession config).

If you see >100 ms in `application:didFinishLaunching:` traceable to Kotlin frames, the fix is almost always **lazy DI** — wrap heavy singletons in `factory` or `single { ... }` with `createdAtStart = false`, and let them resolve on first use.

## What's *not* in this skill

- **Per-platform UI perf** — Compose recomposition, SwiftUI view tree thrash. Those live in `compose-ui` / `swiftui-views` and the native `*-performance` skills.
- **Benchmark infrastructure** — Macrobenchmark setup is in `android-performance`. There is no equivalent benchmark harness for the shared module itself; if you need one, write a JVM `kotlinx.benchmark` suite in `commonTest`-adjacent source — and don't trust the numbers for iOS.
