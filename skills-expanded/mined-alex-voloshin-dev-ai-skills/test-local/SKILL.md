---
name: test-local
description: Local dev testing workflow — verify test environment, provision infrastructure (Docker, Testcontainers), run multi-level test suite (unit → integration → E2E), coverage analysis, quality gate. Applies QA Engineer role. Use for full local QA cycle before commit or PR.
context: fork
argument-hint: "service name or test scope"
---

# Test Local

Full QA cycle for local development environments. Verifies test infrastructure, provisions dependencies, runs tests at all levels (unit → integration → E2E), analyzes coverage, and applies quality gates. Orchestrated by `qa-engineer` role.

**Key difference from `run-tests` skill**: This workflow manages the full local test environment lifecycle (setup → test → report → cleanup). `run-tests` skill is a lightweight follow-up skill that only executes and analyzes tests.

## 1. Define Scope

Read `TESTING.md` at the project root (and per-service `TESTING.md` in monorepos) for test infrastructure, commands, credentials, and organization. This is the authoritative source for how to test the project.

Ask the user (or extract from context):

- **Test scope**: Full suite / specific module / specific test level (unit / integration / E2E)
- **What changed**: New feature / bug fix / refactor / pre-commit check / full regression
- **Known issues**: Any tests expected to fail? Any infra known to be down?

If invoked by another workflow — extract scope from parent context.

## 2. Apply Roles

**Primary**: `qa-engineer` role — owns test strategy, quality gates, and test infrastructure decisions.

**Secondary** (applied as needed during test execution):

| Need | Role |
|---|---|
| Fix failing unit/integration tests | Stack-specific: `java-engineer` role / `python-engineer` role / `frontend-engineer` role |
| Docker/compose/infra issues | `devops-engineer` role |
| Test data / database schema | `db-engineer` role |
| General debugging | `software-engineer` role |

## 3. Detect Project Stack

Read `AGENTS.md` and scan project files to determine:

| Signal | Stack | Test Runner | Container Tool |
|---|---|---|---|
| `package.json` + vitest/jest | TypeScript/JS | `npx vitest` / `npx jest` | Testcontainers-node |
| `package.json` + playwright | TypeScript/JS (E2E) | `npx playwright test` | Playwright containers |
| `pom.xml` / `build.gradle` | Java | `mvn test` / `gradle test` | Testcontainers-java |
| `pyproject.toml` / `pytest.ini` | Python | `pytest` | Testcontainers-python |
| `go.mod` | Go | `go test ./...` | Testcontainers-go |
| `*.csproj` | .NET | `dotnet test` | Testcontainers-dotnet |

Also detect:

- **Docker Compose**: `docker-compose.yml`, `docker-compose.test.yml`, `compose.yaml`
- **Test config files**: `.env.test`, `jest.config.*`, `vitest.config.*`, `playwright.config.*`, `pytest.ini`, `conftest.py`
- **CI config**: `.github/workflows/`, `Jenkinsfile`, `.gitlab-ci.yml` — extract test commands used in CI for parity

## 4. Verify Local Environment

Before running tests, verify the local environment is ready.

### 4a. Docker Daemon

```
// turbo
docker version --format "Client: {{.Client.Version}} | Server: {{.Server.Version}}"
```

If Docker is not running — notify user and stop. Tests requiring containers will fail.

### 4b. Port Conflicts

Check that ports needed by test services are available:

```
// turbo
netstat -ano | findstr ":<port>"
```

Common test ports: 5432 (PostgreSQL), 6379 (Redis), 27017 (MongoDB), 9092 (Kafka), 3306 (MySQL).

If conflicts found — report which process holds the port. Suggest resolution.

### 4c. Environment Variables

Check for test-specific environment configuration:

- Root `.env` — verify it exists and contains `test_` prefixed variables (e.g., `test_user`, `test_db_host`)
- Compare with `.env.example` — flag missing test variables
- Read only `.env.example` for reference — never log or output actual `.env` values

### 4d. Dependencies

Verify project dependencies are installed:

| Stack | Check Command |
|---|---|
| Node.js | `node_modules/` exists, `package-lock.json` up to date |
| Java | `mvn dependency:resolve -q` |
| Python | Virtual env active, `pip check` |
| Go | `go mod verify` |

If dependencies are stale — suggest `npm install` / `pip install -r requirements.txt` / etc.

## 5. Provision Test Infrastructure

Based on project config, set up test dependencies.

### 5a. Testcontainers (preferred)

If the project uses Testcontainers — no manual setup needed. Testcontainers starts/stops containers automatically per test suite. Verify:

- Docker daemon is running (Step 4a)
- Testcontainers config exists (`.testcontainers.properties` if needed)
- Required images are available (or will be pulled automatically)

### 5b. Docker Compose

If the project uses `docker-compose.test.yml` or similar:

```
docker compose -f docker-compose.test.yml up -d
```

Wait for services to be healthy:

```
docker compose -f docker-compose.test.yml ps
```

Check health status. If any service is unhealthy — collect logs and diagnose using `devops-engineer` role.

### 5c. Seed Data

If the project has seed scripts for test data:

1. Locate seed scripts (check `AGENTS.md`, `package.json` scripts, `Makefile`, `scripts/` directory)
2. Run seed scripts after infrastructure is ready
3. Verify seed completed successfully

### 5d. No Infrastructure Needed

If the project uses only mocks/stubs for unit tests — skip to Step 6.

## 6. Run Tests

Execute tests in pyramid order: unit → integration → E2E. Stop at first failing level unless user requested full suite.

### 6a. Unit Tests

```
// turbo
<unit-test-command>
```

**Expected**: Fast (< 2 min), high pass rate. If unit tests fail — fix before proceeding.

For failures — delegate to `run-tests` skill for analysis and auto-fix (Step 3-4 of that workflow).

### 6b. Integration Tests

Run only if unit tests pass (or user explicitly requested):

```
<integration-test-command>
```

**Expected**: Moderate speed (< 10 min). Tests interact with real dependencies (DB, APIs via containers).

Common integration test patterns by stack:

| Stack | Command | Notes |
|---|---|---|
| Vitest/Jest | `npx vitest run --project integration` | If workspace configured |
| pytest | `pytest tests/integration/ -v` | Or `pytest -m integration` |
| Maven | `mvn verify -pl <module>` | Failsafe plugin for ITs |
| Go | `go test -tags=integration ./...` | Build tag separation |

### 6c. E2E Tests

Run only if integration tests pass (or user explicitly requested):

```
<e2e-test-command>
```

**Prerequisites**:
- Application must be running locally (dev server or Docker)
- E2E test config must point to local URL
- Browser binaries installed (Playwright: `npx playwright install`)

Common E2E commands:

| Stack | Command |
|---|---|
| Playwright | `npx playwright test` |
| Cypress | `npx cypress run` |
| pytest + Selenium | `pytest tests/e2e/ -v` |

### 6d. Specialized Tests (optional)

If user requested or project has them:

| Type | When | Command Pattern |
|---|---|---|
| **Performance** | Pre-release, after optimization | `k6 run tests/load/script.js` |
| **Security** | Pre-release, after auth changes | `npm audit` / OWASP ZAP scan |
| **Accessibility** | UI changes | `npx playwright test --grep @a11y` or axe-core |

## 7. Coverage Analysis

After all tests pass, run coverage analysis:

| Stack | Command |
|---|---|
| Vitest | `npx vitest run --coverage` |
| Jest | `npx jest --coverage` |
| pytest | `pytest --cov=<package> --cov-report=term-missing` |
| Go | `go test -coverprofile=coverage.out ./... && go tool cover -func=coverage.out` |
| Maven | `mvn jacoco:report` |

Compare against `test-strategy` skill targets:

| Metric | Target | Hard Minimum | Status |
|---|---|---|---|
| Line coverage | ≥ 80% | ≥ 60% | [pass/fail] |
| Branch coverage | ≥ 75% | ≥ 50% | [pass/fail] |
| New code coverage | ≥ 90% | ≥ 80% | [pass/fail] |

Flag modules with coverage below hard minimum.

## 8. Quality Gate

Evaluate overall test quality:

| Gate | Criteria | Result |
|---|---|---|
| **Unit tests** | All pass | ✅ / ❌ |
| **Integration tests** | All pass (if run) | ✅ / ❌ / ⏭️ skipped |
| **E2E tests** | All pass (if run) | ✅ / ❌ / ⏭️ skipped |
| **Coverage** | Meets targets | ✅ / ⚠️ below target / ❌ below minimum |
| **No flaky tests** | Zero retried tests | ✅ / ⚠️ |
| **No new warnings** | Lint + type checks clean | ✅ / ❌ |

**Decision**:

| Result | Action |
|---|---|
| All gates pass | ✅ **PASS** — safe to commit/PR |
| Coverage warning only | ⚠️ **PASS with notes** — consider adding tests |
| Any test failure | ❌ **FAIL** — fix before commit |
| Flaky tests detected | ⚠️ **PASS with action** — file flaky test issue |

## 9. Cleanup

After testing completes:

1. **Stop test containers** (if Docker Compose was used):
   ```
   docker compose -f docker-compose.test.yml down -v
   ```
2. **Remove test data** (if seed scripts ran outside containers)
3. **Report leftover containers** (if any test containers weren't cleaned up)

Testcontainers handles its own cleanup automatically — verify no orphaned containers remain.

## 10. Summary

```
## Local Test Summary

### Environment
- **Stack**: [detected stack]
- **Docker**: [version] | Test infra: [Testcontainers / Docker Compose / none]
- **Env issues**: [none / list]

### Test Results
| Level | Total | Passed | Failed | Skipped | Duration |
|-------|-------|--------|--------|---------|----------|
| Unit | X | X | X | X | Xs |
| Integration | X | X | X | X | Xs |
| E2E | X | X | X | X | Xs |

### Coverage
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Line | X% | 80% | ✅/❌ |
| Branch | X% | 75% | ✅/❌ |
| New code | X% | 90% | ✅/❌ |

### Coverage Gaps
- [file/module] — [current%] — [uncovered areas]

### Quality Gate: ✅ PASS / ❌ FAIL
- [gate details]

### Failures Fixed (if any)
- [test] — [issue] — [fix]

### Remaining Issues
- [issue] — [action needed]

### Follow-up
- [recommendations]
```

## Integration

- **Roles**: `qa-engineer` role (primary), stack-specific roles (test fixes), `devops-engineer` role (infra issues)
- **Skills**: `test-strategy` skill (test patterns, coverage targets)
- **follow-up skills**: `run-tests` skill (test execution and auto-fix for failures)
- **Called by**: `feature-dev` skill (pre-commit testing), `bugfix` skill (verify fix)
- **Follow-up**: `pre-commit` skill (quality gate), `create-pr` skill (submit changes)
