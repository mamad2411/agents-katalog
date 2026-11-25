---
name: eng-validate
description: Run comprehensive project validation including syntax checks, linters, type checkers, unit tests, integration tests, and build verification. Use when validating project health or running quality gates.
---

# Validate Project

Execute multi-tiered validation to verify project health, code quality, test suite status, and build readiness.

## Process

### 1. Build & Tooling Discovery
Automatically detect the project environment and available validation tools:
- **Node.js / TS**: `npm`, `pnpm`, `yarn`, `bun`, `tsc`, `eslint`, `vitest`, `jest`
- **Python**: `pytest`, `ruff`, `mypy`, `black`, `uv run`
- **Rust**: `cargo check`, `cargo test`, `cargo clippy`
- **Go**: `go vet`, `go test ./...`, `golangci-lint`
- **Java / Kotlin**: `mvn test`, `gradle test`

### 2. Multi-Level Validation Execution
Execute checks in increasing order of cost:
1. **Level 1 - Syntax, Lint & Formatting**: Run static analysis and formatting checks.
2. **Level 2 - Type Checking**: Verify type safety (`tsc --noEmit`, `mypy`, `pyright`, etc.).
3. **Level 3 - Unit & Integration Tests**: Run test suites with summary reporting.
4. **Level 4 - Build & Package Verification**: Verify that the project builds or bundles without errors.

---

## Output Report Structure

```markdown
# Validation Report

- **Timestamp**: <ISO DateTime>
- **Project Root**: `<path>`
- **Overall Status**: PASSED | FAILED

## Summary Matrix
| Layer | Command | Status | Notes |
|---|---|---|---|
| Lint & Style | `<cmd>` | PASS/FAIL | X warnings |
| Type Check | `<cmd>` | PASS/FAIL | 0 errors |
| Test Suite | `<cmd>` | PASS/FAIL | X passed, Y failed |
| Build | `<cmd>` | PASS/FAIL | Artifacts verified |

## Detailed Diagnostics (If Failed)
<Log excerpts and actionable fix suggestions>
```

---

## Checkable Completion Criteria

- [ ] Validation executed across all four levels: lint, type check, test suite, build.
- [ ] Every layer reports an explicit PASS/FAIL status with the exact command used.
- [ ] Failures include log excerpts and actionable fix suggestions, never silent exits.
- [ ] Overall verdict (PASSED or FAILED) is stated unambiguously in the report header.
