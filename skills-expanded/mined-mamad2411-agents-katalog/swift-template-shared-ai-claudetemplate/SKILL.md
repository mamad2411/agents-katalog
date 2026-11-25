# __APP_NAME__ — Claude Code Instructions

> You are an expert iOS developer working on **__APP_NAME__**. Write production-quality Swift code following the patterns established in this repo.

## Project Overview

**Tech Stack**: Swift __SWIFT_VERSION__ · iOS __DEPLOYMENT_TARGET__+ · **SwiftUI** · __ARCHITECTURE_NAME__ · __BUILD_SYSTEM__
**Bundle ID**: `__BUNDLE_ID__`
**Organization**: __ORG_NAME__
**Platforms**: __PLATFORMS__

> **SwiftUI only.** Do not introduce UIKit, Storyboards, or XIBs. ViewModels are `@Observable @MainActor`; views are SwiftUI structs. UIKit ↔ SwiftUI bridging via `UIViewRepresentable` / `UIHostingController` is acceptable when wrapping a specific component, but the app architecture stays SwiftUI.

## Architecture

This project uses **__ARCHITECTURE_NAME__**.

__ARCHITECTURE_DESCRIPTION__

### Dependency Rules

- Features depend on Core modules only
- Core modules depend on other Core modules (no cycles)
- Features NEVER depend on other Features
- Core modules NEVER depend on Features
- Direction: `Features → Core → External Dependencies`

## Code Standards

### Swift Patterns

```swift
// ViewModels: @Observable + @MainActor
@Observable
@MainActor
public final class ExampleViewModel {
    public init() {}
}

// Protocols: suffix with -Protocol when they're inverted-dependency boundaries
public protocol UserRepositoryProtocol: Sendable {}

// Concurrency: async/await only — no DispatchQueue
func fetchData() async throws -> [Item] { }
```

### Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Protocols (DI seams) | `{Name}Protocol` | `UserRepositoryProtocol` |
| ViewModels | `{Screen}ViewModel` | `HomeViewModel` |
| Views | `{Screen}View` | `HomeView` |
| Entities | Singular noun | `User`, `Item` |
| Services | `{Purpose}Service` | `NetworkService` |
| Mocks | `Mock{Name}` | `MockUserRepository` |

### Access Control

Always be explicit. Public for cross-module API, internal default, private for implementation detail.

### Indentation

**2 spaces** everywhere — Swift, YAML, Markdown.

## SwiftLint (Zero-Violation Policy)

All code must pass `swiftlint lint --config .swiftlint.yml` with zero warnings AND errors.

- No `print()` — use `Logger` from `os.log`
- No force unwrapping (`!`)
- No `fatalError()` / `preconditionFailure()` — degrade gracefully
- No hardcoded secrets — use Keychain or env vars
- Sorted imports

**NEVER use `// swiftlint:disable` comments.** Fix the root cause.

## Testing

| Code Type | Requirement |
|-----------|-------------|
| ViewModels | Mandatory — unit tests |
| Services / Repositories | Mandatory — unit tests with mocks |
| Domain models | Mandatory — property/init tests |
| Views | Optional — snapshot tests |

Use Given/When/Then in test bodies.

## Build & Setup

```bash
./setup.sh              # Full setup (install deps + generate project)
./setup.sh --quick      # Fast regenerate (skip dependency install)
./setup.sh --clean      # Clean rebuild
__GENERATE_COMMAND__    # Regenerate project only
```

## Verification (run after every change)

```bash
swiftlint lint --fix --config .swiftlint.yml
swiftlint lint --config .swiftlint.yml

__TEST_COMMAND__
```

A task is NOT complete until SwiftLint shows zero violations AND all tests pass.

## Git Workflow

- **Branching**: Gitflow — `main`, `develop`, `feature/*` from `develop`
- **Commits**: Conventional commits (`feat:`, `fix:`, `refactor:`, `test:`, `chore:`)
- **PRs**: Target `develop`. CI runs SwiftLint + unit tests.

## Guardrails

- File boundary: only edit files inside this repo
- Never modify generated `*.xcodeproj` / `*.xcworkspace` directly — regenerate from config
- Never introduce UIKit, Storyboards, or XIBs — SwiftUI only
- Don't run UI tests from CLI — only unit tests
- Confirm before destructive commands (`rm -rf`, `git reset --hard`, force push)
