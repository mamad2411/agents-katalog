---
name: test-runners-by-stack
description: Use this skill when running tests in a specific stack, wiring CI test steps, or designing test infrastructure — per-stack test runner commands and conventions for TypeScript/JavaScript, Java, Python, Go, and .NET covering unit, integration, E2E, and coverage commands plus Testcontainers conventions and quality-gate signals, a reference table for picking the right command after stack detection. Knowledge skill — loaded as context by `/test-local` and `/test-strategy`, never invoked directly.
disable-model-invocation: true
---

# Test Runners by Stack

Per-stack tooling lookup for unit, integration, E2E, and coverage commands plus Testcontainers conventions. Used by `/test-local` (provision + run) and `/test-strategy` (design). Knowledge skill — loaded as context, never invoked directly.

Detection signals and Testcontainers mapping (high-level):

| Signal | Stack | Unit Runner | Container Tool |
|---|---|---|---|
| `package.json` + vitest/jest | TypeScript/JS | `npx vitest` / `npx jest` | Testcontainers-node |
| `package.json` + playwright | TypeScript/JS (E2E) | `npx playwright test` | Playwright containers |
| `pom.xml` / `build.gradle` | Java | `mvn test` / `gradle test` | Testcontainers-java |
| `pyproject.toml` / `pytest.ini` | Python | `pytest` | Testcontainers-python |
| `go.mod` | Go | `go test ./...` | Testcontainers-go |
| `*.csproj` | .NET | `dotnet test` | Testcontainers-dotnet |

## TypeScript / JavaScript

| Level | Command | Notes |
|---|---|---|
| Unit (Vitest) | `npx vitest run` | Fast, isolated; use `--project unit` if workspace configured |
| Unit (Jest) | `npx jest` | Same role as Vitest |
| Integration | `npx vitest run --project integration` | If workspace configured; otherwise filter by path/tag |
| E2E (Playwright) | `npx playwright test` | Requires `npx playwright install` for browser binaries |
| E2E (Cypress) | `npx cypress run` | App must be running locally; config points to local URL |
| Coverage (Vitest) | `npx vitest run --coverage` | Emits line/branch coverage |
| Coverage (Jest) | `npx jest --coverage` | Same shape |

**Dependency check**: `node_modules/` exists; `package-lock.json` up to date. If stale, suggest `npm install`.

**Testcontainers (Node)**: containers start/stop automatically per suite — only requirement is a running Docker daemon and that needed images can be pulled.

**Config files commonly present**: `jest.config.*`, `vitest.config.*`, `playwright.config.*`, `.env.test`.

**Quality-gate signals**: unit suite under ~2 min; flaky tests = any retried test; lint + type check must be clean alongside test pass.

## Java

| Level | Command | Notes |
|---|---|---|
| Unit | `mvn test` or `gradle test` | Surefire (Maven) runs `*Test.java` by default |
| Integration | `mvn verify -pl <module>` | Failsafe plugin runs `*IT.java` integration tests |
| Coverage | `mvn jacoco:report` | JaCoCo plugin emits line/branch report |

**Dependency check**: `mvn dependency:resolve -q` to ensure resolution before running tests.

**Testcontainers (Java)**: declared as a test-scope dependency; containers spin up per suite via JUnit extension or `@Testcontainers`. Requires Docker daemon.

**Config files commonly present**: `pom.xml` / `build.gradle`, optional `src/test/resources/` test config.

**Quality-gate signals**: integration suite under ~10 min; Failsafe report distinguishes unit vs IT failures; JaCoCo line/branch report compared against coverage targets.

## Python

| Level | Command | Notes |
|---|---|---|
| Unit | `pytest` | Discovers `test_*.py` / `*_test.py` |
| Integration | `pytest tests/integration/ -v` or `pytest -m integration` | Marker-based separation also common |
| E2E (Selenium) | `pytest tests/e2e/ -v` | App must be running locally; webdriver installed |
| Coverage | `pytest --cov=<package> --cov-report=term-missing` | `pytest-cov` plugin; report shows uncovered lines |

**Dependency check**: virtualenv active; `pip check` confirms no broken/conflicting dependencies. If stale, suggest `pip install -r requirements.txt`.

**Testcontainers (Python)**: `testcontainers` package; same lifecycle model as other stacks. Requires Docker daemon.

**Config files commonly present**: `pyproject.toml`, `pytest.ini`, `conftest.py`, `.env.test`.

**Quality-gate signals**: unit suite under ~2 min; coverage line/branch reported via `term-missing` per module; `-v` recommended when failures need diagnosis.

## Go

| Level | Command | Notes |
|---|---|---|
| Unit | `go test ./...` | Discovers `*_test.go` across the module |
| Integration | `go test -tags=integration ./...` | Build-tag separation isolates IT files |
| Coverage | `go test -coverprofile=coverage.out ./... && go tool cover -func=coverage.out` | Per-function coverage summary |

**Dependency check**: `go mod verify` confirms module checksums.

**Testcontainers (Go)**: `testcontainers-go` library; same lifecycle model. Requires Docker daemon.

**Config files commonly present**: `go.mod`, build-tag headers (e.g. `//go:build integration`) on integration files.

**Quality-gate signals**: unit suite typically very fast; coverage emitted as `.out` file, suitable for CI artifact upload; build tags must match between local and CI runs.

## .NET

| Level | Command | Notes |
|---|---|---|
| Unit | `dotnet test` | Runs all test projects in solution by default |
| Integration | `dotnet test` with category filter | E.g. `--filter Category=Integration` |
| Coverage | `dotnet test --collect:"XPlat Code Coverage"` | Emits coverage.cobertura.xml |

**Testcontainers (.NET)**: `Testcontainers` NuGet package; same lifecycle model. Requires Docker daemon.

**Config files commonly present**: `*.csproj`, `*.sln`, optional `appsettings.Test.json`.

**Quality-gate signals**: category filter (`Category=Integration`) is the standard separator between unit and integration; coverage emitted in Cobertura format for CI parsing.

## Specialized tests (cross-stack)

| Type | When | Command Pattern |
|---|---|---|
| Performance | Pre-release, after optimization | `k6 run tests/load/script.js` |
| Security | Pre-release, after auth changes | `npm audit` / OWASP ZAP scan |
| Accessibility | UI changes | `npx playwright test --grep @a11y` or axe-core |

## Coverage targets (cross-stack)

| Metric | Target | Hard Minimum |
|---|---|---|
| Line coverage | ≥ 80% | ≥ 60% |
| Branch coverage | ≥ 75% | ≥ 50% |
| New code coverage | ≥ 90% | ≥ 80% |

Flag modules with coverage below the hard minimum. Targets sourced from `test-strategy`.

## When this applies

| Phase | Apply this knowledge |
|---|---|
| `/test-local` Step 3 (detect stack) | Map detection signal to stack + runner |
| `/test-local` Step 4d (dependencies) | Pick the per-stack dependency check command |
| `/test-local` Step 6a (run unit) | Pick the unit-test command for the detected stack |
| `/test-local` Step 6b (run integration) | Pick the integration command (Vitest project / pytest marker / Maven Failsafe / Go build tag / dotnet filter) |
| `/test-local` Step 6c (run E2E) | Pick the E2E runner (Playwright / Cypress / pytest+Selenium) and ensure prerequisites |
| `/test-local` Step 7 (coverage) | Pick the coverage command and compare against targets |
| `/test-strategy` (design phase) | Reference for what runners exist per stack when authoring `TESTING.md` |

## Integration

- **Used by**: `/test-local` (running tests across all levels), `/test-strategy` (designing test plans and authoring `TESTING.md`)
- **Companion knowledge**: `test-strategy` skill (test pyramid, design principles, coverage targets)
- **Project context**: `TESTING.md` (root + per-service) — authoritative source for the actual commands the project uses
