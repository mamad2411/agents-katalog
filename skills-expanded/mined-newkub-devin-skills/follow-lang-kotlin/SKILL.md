---
name: follow-lang-kotlin
description: Develop Kotlin applications with Clean Architecture and Compose
argument-hint: "[scope|setup-project]"
related:
  - follow-lang-javascript
  - follow-architecture
  - follow-best-practice
  - refactor
  - setup-cicd
  - use-scripts
  - run-test
  - deep-research
---

## Goal

Develop Kotlin projects with Clean Architecture, Compose, Coroutines, Koin, and Arrow

## Scope

For projects developed in Kotlin (Compose Multiplatform/Desktop, KMP). Package: `SKILL.md` entry + `references/toolchain.md` (ecosystem-tool table) + `workflows/setup-project/SKILL.md` (argument `setup-project` — first-time Gradle/Compose scaffold); verify current versions/practices via `/deep-research` at use time

## Execute

### 1. Check Version And Setup

> Goal: install dependencies and configure the project with live-checked versions

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest stable Kotlin, Compose Multiplatform, Coroutines, Koin, Ktor, and Arrow versions before pinning anything
2. New project → run the workflow `workflows/setup-project/SKILL.md` (argument `setup-project`): JDK pin, Gradle wrapper + version catalog, Kotlin DSL config, Clean Architecture skeleton, ktlint/detekt gates, verify
3. Optional deps (Ktor, Arrow, Koin) → confirm with the user before adding
4. Tool inventory (JDK, Gradle, lints, test stack) → `references/toolchain.md`

### 2. Project Structure

> Goal: organize code per Clean Architecture

1. Split into `core/`, `data/`, `domain/`, `presentation/` — domain never depends on framework/UI
2. `data/` owns I/O (remote/local datasources, DTOs, repository implementations, DTO → domain mapping); `domain/` owns entities, repository interfaces, use cases; `presentation/` owns Compose screens, ViewModels, Koin DI modules
3. Recommended layout:

```text
src/main/kotlin/com/mycompany/app/
├── core/error/            # Failure sealed class, exceptions
├── data/datasource/       # Remote/Local data sources
├── data/model/            # DTOs
├── data/repository/       # Domain repository implementations
├── domain/model/          # Business entities
├── domain/repository/     # Repository interfaces (contracts)
├── domain/usecase/        # Single-responsibility use cases
├── presentation/di/       # Koin modules
├── presentation/screen/   # Composable screens
├── presentation/viewmodel/# StateFlow ViewModels
└── Main.kt
```

4. Run `/follow-architecture` to pick the pattern for the app shape

### 3. Core Principles

> Goal: write Kotlin per best practices

1. Use Coroutines (+ Flow/StateFlow) for async operations, never blocking threads
2. Use Koin for dependency injection; one `module { }` per layer boundary
3. Use Ktor for the HTTP client
4. Use Arrow `Either<Failure, Success>` for functional error handling; `data class` for immutable models
5. Side effects live in the data layer; use cases have a single clear responsibility (`suspend operator fun invoke`)

### 4. Error Handling

> Goal: handle errors with the Arrow Either pattern

1. Define a `sealed class Failure` (`ServerFailure`, `CacheFailure`, ...) in `core/error/`
2. Repository interfaces return `Either<Failure, T>`; wrap exceptions with `Either.catch { }.mapLeft { ServerFailure(it.message ?: "...") }`
3. ViewModels render state by `fold(ifLeft = ..., ifRight = ...)` into a `StateFlow<UiState>`; avoid throwing exceptions across layers

### 5. Testing

> Goal: write tests for every layer

1. Use `kotlin.test`/JUnit 5 with `runTest` for coroutines; MockK (`mockk`, `coEvery`) for repository mocks
2. Unit test domain use cases (pure functions), data layer (mock API), presentation (ViewModel state transitions)
3. Run `/run-test` until green

## Rules

### 1. Architecture

- Clean Architecture layers `data/`/`domain/`/`presentation/`; domain is framework-free; data maps DTO → domain as the single source of truth
- Use Compose Multiplatform for UI

### 2. Async And DI

- Coroutines for async; Koin for DI; Ktor for HTTP

### 3. Error Handling

- Arrow `Either<Failure, Success>` everywhere a call can fail; `data class` for immutable models

### 4. No Stale Pins

- Never pin Kotlin/library versions in this skill or in code comments; live-check at use time via `/deep-research`

- Use /follow-lang-javascript if needed
- Use /follow-best-practice if needed
- Use /refactor if needed
- Use /setup-cicd if needed
- Use /use-scripts if needed

## Expected Outcome

- Kotlin project with Clean Architecture and clear layer boundaries
- Compose Multiplatform UI, Coroutines async, Koin DI, Arrow Either error handling
- Unit tests covering domain, data, and presentation
