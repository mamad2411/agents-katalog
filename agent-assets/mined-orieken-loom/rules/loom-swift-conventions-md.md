# Swift Conventions

Conventions for iOS / macOS apps built with SwiftUI and Swift Concurrency. Applies to any feature
the framework targets at a native Apple platform.

## Architecture
ALWAYS follow Clean Architecture layers: Domain → UseCase → Repository → Adapter.
NEVER let domain entities import UIKit, SwiftUI, or any framework layer.
ALWAYS define repository protocols in the use-case layer, implement in adapters.
ALWAYS use constructor injection for dependencies — avoid singletons as primary state holders.
Use `@Environment` for SwiftUI-scoped dependencies only (theme, locale, navigation containers).
ALWAYS use `async`/`await` and Swift Concurrency — no callback pyramids or manual DispatchQueue juggling.
NEVER use `@Published` inside domain entities — keep Combine bindings in the ViewModel layer.

## Project Tooling
- **Build system**: Xcode (primary) or Swift Package Manager for command-line / multiplatform targets.
- **Complexity enforcement**: [`SwiftLint`](https://github.com/realm/SwiftLint) — `cyclomatic_complexity`
  rule capped at `6` (enforces the framework-wide `< 7` budget). Add a `.swiftlint.yml` at the repo
  root; treat SwiftLint warnings as CI failures.
- **Formatter**: [`SwiftFormat`](https://github.com/nicklockwood/SwiftFormat) — run as a build phase
  or pre-commit hook.
- **Static analysis**: Xcode's built-in Analyze action (`⌘⇧B`) plus SwiftLint; no custom
  analysis framework required.

## File Naming
PascalCase for all Swift source files; one public type per file; filename matches the public type name.

| Purpose | Suffix | Example |
|---|---|---|
| Domain model | `Model.swift` | `UserModel.swift` |
| ViewModel | `ViewModel.swift` | `UserProfileViewModel.swift` |
| Repository protocol | `Repository.swift` | `UserRepository.swift` |
| Repository impl | `RepositoryImpl.swift` | `UserRepositoryImpl.swift` |
| Use case | `UseCase.swift` | `FetchUserUseCase.swift` |
| SwiftUI view | `View.swift` | `UserProfileView.swift` |
| Unit test | `Tests.swift` | `UserProfileViewModelTests.swift` |
| UI test | `UITests.swift` | `UserProfileUITests.swift` |

## Frameworks
- **UI layer**: SwiftUI — primary and modern default. UIKit only for components not yet expressible
  in SwiftUI or for legacy feature areas; never mix them in the same view hierarchy without a
  clear `UIViewRepresentable` boundary.
- **Reactive / async**: Swift Concurrency (`async`/`await`, `Task`, `Actor`) for all async work.
  Combine is acceptable for multi-value streams and SwiftUI bindings (`@Published`, `PassthroughSubject`);
  avoid Combine for one-shot async calls (use `async/await` instead).
- **Dependency injection**: constructor injection; [`Factory`](https://github.com/hmlongco/Factory)
  is the recommended lightweight DI container for projects that need container-based registration —
  not required for small apps.
- **Networking**: `URLSession` with `async`/`await` — no third-party HTTP library required.

## Testing & QA Tooling
- **Unit testing framework**: XCTest — standard library, no extra dependency.
- **Expressive matchers**: [`Nimble`](https://github.com/Quick/Nimble) (optional) for readable
  assertions (`expect(result).to(equal(42))`). [`Quick`](https://github.com/Quick/Quick) for
  BDD-style `describe`/`it` grouping (optional; use when BDD phrasing aids stakeholder readability).
- **Mocking**: Swift has no runtime reflection, so prefer **hand-rolled protocol-based test doubles**
  (`MockUserRepository: UserRepository { ... }`). For large suites,
  [`Mockingbird`](https://github.com/birdrides/mockingbird) can generate mocks from source at build
  time — verify it tracks your Swift/Xcode version before adoption.
- **Snapshot testing**: [`swift-snapshot-testing`](https://github.com/pointfreeco/swift-snapshot-testing)
  — records and diffs SwiftUI / UIKit view snapshots. Pair with visual-qa-engineer when enabled.
- **UI / integration**: XCUITest (Xcode's built-in UI automation) for acceptance flows.
- **Fake / synthetic data**: hand-built `Builder` structs or `static func make(...)` factory methods
  per domain type (the same builder pattern recommended in `go-conventions.md`). No faker library
  equivalent dominates the Swift ecosystem yet.
- **Mutation testing** (ADR-008 clause 2): `muter` — a candidate, **not yet verified** against a
  real project. Verify before relying on its score: a mutant that did not compile, or timed out,
  must never be counted as killed.
- **Performance testing**: XCTest's `measure {}` block for microbenchmarks; k6 for any backend
  service the iOS app calls.
- **Reporting**: XCTest's built-in `.xcresult` bundle; convert to JUnit XML via
  [`xcresulttool`](https://developer.apple.com/documentation/xctest) for CI reporting aggregators.

## Quick Reference

```swift
// Complexity: < 7 — enforce with SwiftLint cyclomatic_complexity: 6
// File naming: PascalCase, one public type per file, suffix-typed
// Architecture: Domain / UseCase / Repository / Adapter — no framework imports in domain
// Models: struct (value semantics), final class only when reference semantics needed
// Async: async/await + Actor — no callbacks or manual DispatchQueue
// Dependency injection: constructor injection; @Environment for SwiftUI-scoped deps
// Tests: XCTest (primary), Nimble matchers, hand-rolled protocol fakes
// Snapshot testing: swift-snapshot-testing
// Complexity tool: SwiftLint cyclomatic_complexity rule capped at 6
```

---
*Part of the [ai-assistant-dot-files](https://github.com/orieken/loom) Context Engineering Framework by Oscar Rieken — licensed under [CC BY 4.0](https://github.com/orieken/loom/blob/main/LICENSE-CONTENT.md). If you copy or adapt this file, please keep this attribution.*
