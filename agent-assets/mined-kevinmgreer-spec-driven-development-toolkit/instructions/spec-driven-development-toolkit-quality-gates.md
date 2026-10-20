---
description: "Use when running quality gates, checking code quality, or preparing for PR. Covers lint, format, typecheck, build, and test gates with auto-detection and iteration. Trigger phrases: quality gates, lint, format, build, typecheck, run checks, CI, code quality."
---

# Quality Gates

Automated checks that must pass before proceeding to the next phase of the ATDD cycle.

## When Gates Run

- **After test stubs (Red)**: All stubs fail for "not implemented" reasons (not import/syntax errors)
- **After each scenario**: Target scenario green, no regressions
- **After all scenarios**: Full test suite green
- **Before refactor**: lint + format + typecheck + build + test
- **After each refactor step**: Full test suite green
- **Before PR**: All gates pass

## Gate Detection

Detect available gates from the project's configuration files:

- **Tests**: `package.json`, `pyproject.toml`, `*.csproj`, `go.mod`, `Cargo.toml`, etc.
- **Lint**: ESLint, Biome, Ruff, Flake8, RuboCop, golangci-lint, Clippy
- **Format**: Prettier, Biome, Black, Ruff, rustfmt, gofmt
- **Type check**: TypeScript, mypy, pyright, .NET, Go
- **Build**: npm/yarn build, dotnet build, go build, cargo build, make, gradle, maven

## Gate Execution

1. Run lint, format, type check, and build (can be parallel)
2. Auto-fix lint and format issues where tools support it
3. Fix type and build errors manually
4. Run tests after all other gates pass
5. If any gate fails, fix and re-run (max 3 attempts per gate)
6. After fixing, re-run ALL gates to check for regressions

## Rules

- Never modify tests to pass a gate
- Auto-fix when possible (lint --fix, format --write)
- Skip gates the project doesn't have (note as N/A)
- Match CI/CD checks — read `.github/workflows/` etc. to see what CI requires

Full reference: `docs/atdd/quality-gates.md`
