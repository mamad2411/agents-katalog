---
name: swift-language
description: Comprehensive modern Swift (6.x) language expertise — concurrency, generics, ownership/performance, macros, API design, error handling, SwiftPM, C/C++/ObjC interop, cross-platform (Linux/Android/embedded/server), and Swift Testing. Use this skill whenever writing, reviewing, refactoring, or debugging ANY Swift code — even a single function — and whenever the user mentions Swift, .swift files, Xcode projects, Swift packages, actors, Sendable, swiftc, or compiler errors from a Swift build. Also use it when choosing between Swift language features or migrating code to a newer Swift version. Not needed for pure SwiftUI layout questions (a dedicated SwiftUI skill may fit better), but DO use it when SwiftUI code involves concurrency, performance, or general language questions.
---

# Swift to the Max

Expert-level guidance for modern Swift. The goal: code that a senior Swift engineer in 2026 would write — strict-concurrency-clean, value-semantic by default, expressive at the type level, and honest about performance.

## Version landscape (mid-2026)

| Version | Status | Headline features |
|---|---|---|
| Swift 5.10 | legacy | last 5.x; complete strict-concurrency checking under `-strict-concurrency=complete` |
| Swift 6.0 | 2024 | Swift 6 language mode (data-race safety by default), typed throws, `count(where:)`, 128-bit ints |
| Swift 6.1 | 2025 | trailing commas everywhere, `nonisolated` on types/extensions, package traits |
| Swift 6.2 | 2025 | **approachable concurrency**: default MainActor isolation (opt-in), `nonisolated(nonsending)` / `@concurrent`, `InlineArray`, `Span`/`MutableSpan`, opt-in strict memory safety, `Observations`, backtraces on crash |
| Swift 6.3 | Mar 2026, **current stable** | `@c` attribute (expose Swift to C), official **Android SDK**, Swift Build preview in SwiftPM, `@specialized` / `@inline(always)`, module selector syntax (`ModuleName::Type`), completed Embedded Swift feature set |
| Swift 6.4 | WWDC26 beta | `await` in `defer`, `Iterable` protocol (borrowing iteration), `anyAppleOS` availability shorthand, `@diagnose`, Swift Testing ↔ XCTest interop, unified URL implementation |

Default to Swift 6 language mode semantics unless the project's `Package.swift` / build settings say otherwise. Check `// swift-tools-version:` and `swiftLanguageModes:` before assuming. Never emit code using a beta-only (6.4) feature without flagging it as such.

## Non-negotiable defaults

These apply to essentially all new Swift code; deviate only when the surrounding codebase clearly does otherwise, and say so.

- **Value types first.** `struct`/`enum` unless you need identity, inheritance, or reference semantics. If you reach for `class`, ask whether it should be an `actor` or `final class`.
- **Strict concurrency clean.** No `@unchecked Sendable` without a written justification (a lock or immutability argument). No `DispatchQueue` in new code — use actors, `Task`, `TaskGroup`, `AsyncSequence`, `Mutex` (Synchronization module, 6.0+).
- **`some` before `any`.** Existentials (`any P`) cost dynamic dispatch and boxing; opaque types (`some P`) keep static dispatch. Use `any` only when you genuinely need heterogeneity.
- **Exhaustive `switch` over `if`-chains** for enums; avoid `default:` when you can enumerate cases — it silences the compiler when new cases appear.
- **No force unwraps / force try in production paths.** `!` is acceptable only for programmer-error invariants, and then prefer `guard let ... else { preconditionFailure("why") }` so the invariant is documented.
- **Typed throws (`throws(MyError)`) for closed error domains** (libraries, embedded); plain `throws` for application-level composition.
- **`guard` for early exit, one happy path** at low indentation.
- **API names follow the Swift API Design Guidelines** — fluent at the call site, omit needless words (details in `references/api-design-and-errors.md`).

## Idiom translation table

When reviewing or migrating, rewrite the left column on sight:

| Legacy | Modern |
|---|---|
| `DispatchQueue.global().async { ... }` | `Task { ... }` / `Task.detached` (rare) / `@concurrent` func |
| `DispatchQueue.main.async { ... }` | `@MainActor` function or `MainActor.run` |
| completion handlers `(Result<T, Error>) -> Void` | `async throws -> T` (bridge with `withCheckedThrowingContinuation`) |
| `NSLock` / `os_unfair_lock` | `Mutex<State>` (Synchronization) or an `actor` |
| `class Foo: NSObject` + KVO | `@Observable` (Observation framework) |
| `Array` fixed-size hot buffers | `InlineArray<N, T>` (6.2+) |
| `UnsafeBufferPointer` parameters | `Span<T>` / `RawSpan` (6.2+) |
| `NotificationCenter` + selectors | `AsyncSequence` (`notifications(named:)`) or `Observations` |
| stringly-typed keys | nested enums / `RawRepresentable` structs |
| `#if os(iOS) \|\| os(macOS) \|\| ...` across all Apple OSes | `anyAppleOS` (6.4+, flag as beta) |

## Workflow

1. **Detect the project's Swift version and language mode** first (`Package.swift`, `.xcodeproj` settings, `swift --version`). Guidance shifts meaningfully between 5.x, 6.0/6.1, and 6.2+ (default MainActor isolation may be on).
2. **Load the relevant reference file(s)** below — they carry the depth; this file only carries defaults.
3. **Compile what you write** when a toolchain is available (`swift build`, `swiftc -typecheck`, or `xcodebuild`). Swift's type checker is the cheapest reviewer you have. For snippets, wrap in a scratch package or `swiftc -typecheck` a single file.
4. **Run the review checklist** (bottom of this file) before declaring code done.

## Reference routing

Read the file whose domain the task touches. Multiple may apply; read all that do.

| Topic | File | Read when… |
|---|---|---|
| Concurrency | `references/concurrency.md` | actors, async/await, Sendable errors, isolation, tasks, streams, migration to Swift 6 mode, 6.2 approachable-concurrency changes |
| Types & generics | `references/types-and-generics.md` | protocols, `some`/`any`, associated types, parameter packs, noncopyable (`~Copyable`) & `~Escapable` types, phantom types, result builders |
| Memory & performance | `references/memory-and-performance.md` | ARC, retain cycles, COW, `consuming`/`borrowing`, `InlineArray`/`Span`, `@specialized`/`@inline(always)`, allocation profiling, Instruments |
| API design & errors | `references/api-design-and-errors.md` | naming, library ergonomics, typed throws, error architecture, availability, documentation comments |
| Macros | `references/macros.md` | writing or debugging `@attached`/`@freestanding` macros, SwiftSyntax, macro testing |
| SwiftPM & tooling | `references/swiftpm-and-tooling.md` | Package.swift authoring, traits, plugins, Swift Build, swiftly, CI setup, pinning toolchains |
| Interop & platforms | `references/interop-and-platforms.md` | C/C++/ObjC bridging, `@c`, Android SDK, Linux/server, Embedded Swift, WASM |
| Testing | `references/testing.md` | Swift Testing (`@Test`, `#expect`), parameterized tests, XCTest migration/interop, async testing |

## Review checklist

Run through this before presenting any nontrivial Swift code:

1. Does it compile under the project's language mode? (Actually check when possible.)
2. Any data-race-safety diagnostics it would trip in Swift 6 mode? Any `@unchecked Sendable`, `nonisolated(unsafe)`, or `@preconcurrency` without justification?
3. Retain cycles: every escaping closure stored on a class/actor audited for `[weak self]` need — and no cargo-cult `[weak self]` where the closure is short-lived (task bodies that finish quickly are fine holding `self` strongly, if that lifetime is intended).
4. Force unwraps, `try!`, `as!` — each one justified or removed.
5. Public API: names read as English phrases at the call site; parameters have sensible defaults; types are `Sendable` where users will need them to be.
6. Errors: can callers distinguish the failures they need to handle? Is anything swallowed silently (`try?` discarding actionable errors)?
7. Performance red flags in hot paths: unnecessary existentials, repeated `Array` reallocation without `reserveCapacity`, string concatenation in loops, O(n) `count` checks on lazy sequences.
8. Availability: does the code use symbols newer than the stated deployment target without `@available` guards?

## When NOT to over-apply this skill

- Small scripts and prototypes: correctness and clarity beat architecture. Don't wrap a 30-line script in actors and protocols.
- Existing codebases: match local conventions first; propose modernization separately rather than mixing it into a feature diff.
- Beta features (6.4 as of mid-2026): mention, don't silently use.

## Companions & orchestration

Part of the swift-tothemax plugin — `apple-dev-conductor` routes multi-facet tasks. Siblings: `swiftui-max` owns the view layer; hand UI questions there. This skill owns everything beneath it.
Ecosystem companions (delegate the sub-task if installed, keep this skill's 2026 version facts): `swift-concurrency` / `swift-concurrency-pro` for concurrency-correctness review of diffs; `swift-testing-pro` / `swift-testing-expert` for test-suite review; `swiftdata` / `swiftdata-pro` for persistence layers. If both this skill and a companion produce a checklist, merge and run once.
