---
name: follow-lang-swift
description: Swift application guidelines with Clean Architecture and SwiftUI
argument-hint: "[scope|setup-project]"
related:
  - follow-lang-kotlin
  - follow-architecture
  - follow-best-practice
  - refactor
  - setup-cicd
  - use-scripts
  - run-test
  - deep-test
  - deep-research

---

## Goal

Develop Swift applications with Clean Architecture and SwiftUI per best practices

## Scope

For Swift tasks and workflows (iOS/macOS/visionOS apps and Swift packages). Package: `SKILL.md` entry + `references/toolchain.md` (ecosystem-tool table) + `workflows/setup-project/SKILL.md` (argument `setup-project` — first-time SPM/app scaffold); verify the current Swift/Xcode toolchain and API changes via `/deep-research` at use time (official docs: https://developer.apple.com/documentation/swift, https://www.swift.org/documentation/)

## Execute

### 1. Check Version And Setup

> Goal: set up Swift Package Manager and dependencies with live-checked versions

1. Run `/deep-research` + `/follow-best-practice` to confirm the current Swift language mode, practices, and Observation-framework availability for the deployment targets before choosing APIs
2. New project → run the workflow `workflows/setup-project/SKILL.md` (argument `setup-project`): `swift package init` or Xcode app skeleton, `Package.swift`, layered targets, first test, verify
3. Core stack: SPM, Swift Concurrency (`async/await`), DI via Factory (or protocol-based manual DI)
4. Tool inventory (build, test, lint, format, profiling) → `references/toolchain.md`

### 2. Project Structure

> Goal: organize the project per Clean Architecture

1. `Application/` — entry point (`@main struct MyApp: App`), app/scene delegates when required
2. `Core/` — DI registry, extensions, shared utils
3. `Data/` — data sources, DTO models, repository implementations
4. `Domain/` — entities (immutable `struct`, `Identifiable, Hashable`), repository protocols, use cases
5. `Presentation/` — reusable components, screens, view models
6. `Resources/` — assets, color sets
7. Run `/follow-architecture` for the pattern decision; detail: structures + layer tables in `follow-architecture/SKILL.md` (`## Clean Pattern` / `## Layered Pattern`)

### 3. Layer Dependencies (Import Rules)

> Goal: enforce the dependency direction

1. `Presentation -> Domain`, `Data -> Domain`, `Domain -> (nothing)`, `Core -> shared only`, `Application -> Presentation/Domain/Data`
2. Repository protocol lives in Domain, implementation in Data; DTOs are converted to domain entities at the data boundary

### 4. Core Principles

> Goal: apply key SwiftUI and concurrency practices

1. SwiftUI data flow: `@State` (local), `@StateObject` (owned), `@ObservedObject` (passed in), `@EnvironmentObject` (hierarchy-shared) — prefer the `@Observable` macro when the deployment target supports it (live-check)
2. `ObservableObject` view models with `@Published` properties; derived values as computed properties
3. Swift Concurrency: `async/await` and `async throws` APIs for I/O; avoid completion-handler mixes across layers
4. MVVM: the view model mediates view and use cases; views are `struct`s conforming to `View`, small, single-responsibility, with `private` internal state
5. DI via Factory registrations to keep layers decoupled and testable

### 5. Testing

> Goal: test the project effectively

1. Domain use cases and view models are unit-tested through injected protocol mocks (`swift test` / Xcode test targets)
2. Separate UI/network integration tests from pure unit tests; no live network in unit tests
3. Run `/run-test` until green; `/deep-test coverage` for gaps

## Rules

### 1. Component Structure

- SwiftUI views are `struct`s, one file per component, small and single-responsibility; `private` for internal state; order members: state → derived → body → helpers

### 2. Data Flow

- Correct property-wrapper choice per ownership; `@Published`/`@Observable` for view-model notification; async/await for I/O; never reach across layer boundaries directly

### 3. Code Quality

- `struct` for data models (immutable by default); protocols for interfaces; consistent naming; value semantics preferred over reference types except view models/DI

### 4. Build Commands

- `swift build`, `swift run`, `swift test`, `swift package update|resolve`; on Xcode projects use `xcodebuild` with the project scheme

- Use /follow-lang-kotlin if needed
- Use /follow-best-practice if needed
- Use /refactor if needed
- Use /setup-cicd if needed
- Use /use-scripts if needed

## Expected Outcome

- Swift application structured with Clean Architecture and enforced dependency direction
- Correct SwiftUI usage and clear, maintainable data flow
- Decoupled, testable code with DI and protocol boundaries
- Tests covering domain and view models, passing locally and in CI
