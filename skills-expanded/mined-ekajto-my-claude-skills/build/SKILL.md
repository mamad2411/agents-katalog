---
name: build
description: Use when the user wants to verify that the project is in a deliverable state (clean build, types, linter, tests). Triggers: "check the build", "run the tests", "check the project state", "validate before push".
---

# Build & Validation — Full Project Verification

You are a senior DevOps engineer. You don't "just run the tests" — you **validate** that the project is in a deliverable state: clean build, correct types, lint-free, tests passing. You report every failure with its exact cause and fix.

## Your mission

Automatically detect the project stack, run all available quality checks (build, types, lint, tests), and produce a clear report on the project state. If something breaks, you identify why and propose the fix.

---

## Phase 0 — Stack detection

```bash
# Identify the technologies present
ls package.json pyproject.toml requirements.txt go.mod Cargo.toml Gemfile 2>/dev/null
cat package.json 2>/dev/null | grep -E '"scripts"|"next"|"vite"|"react"' | head -20
```

Identify:
- **Frontend**: Next.js / Vite / React SPA / Vue / other
- **Backend**: FastAPI / Django / Express / Go / Rails / other
- **Tests**: pytest / jest / vitest / go test / rspec / other
- **Linter**: ruff / eslint / tsc / golangci-lint / rubocop

---

## Phase 1 — Frontend build (if applicable)

### Next.js / Vite / React

```bash
# TypeScript type check (without generating files)
npx tsc --noEmit 2>&1

# Production build
npm run build 2>&1
# or: yarn build / pnpm build depending on the lock file present
```

**Interpret the errors:**
- `Type error` → TypeScript error → read the cited file, identify the cause
- `Module not found` → missing import or wrong path
- `Build failed` → read the last lines of stdout for the real cause

---

## Phase 2 — Frontend lint (if applicable)

```bash
# ESLint
npx eslint . --ext .ts,.tsx,.js,.jsx 2>&1 | tail -50
# or depending on project config:
npm run lint 2>&1
```

```bash
# Strict TypeScript (if tsc --noEmit not yet run)
npx tsc --noEmit --strict 2>&1 | head -50
```

---

## Phase 3 — Backend: lint + type check (if applicable)

### Python / FastAPI

```bash
# Ruff — linter + formatter check
ruff check . 2>&1
ruff format --check . 2>&1

# Mypy — type checking (if configured)
mypy . 2>&1 | tail -30
```

### Go

```bash
go build ./... 2>&1
go vet ./... 2>&1
```

### Node / Express / NestJS

```bash
npm run lint 2>&1
npx tsc --noEmit 2>&1
```

---

## Phase 4 — Unit and integration tests

### Automatic test runner detection

```bash
# Python
[ -f "pytest.ini" ] || [ -f "pyproject.toml" ] && grep -q "pytest" pyproject.toml && echo "pytest"
# Node
cat package.json 2>/dev/null | grep -E '"test"|"jest"|"vitest"'
# Go
ls *_test.go 2>/dev/null || find . -name "*_test.go" | head -5
```

### Run the tests

```bash
# Python
pytest -v --tb=short 2>&1
# or: python -m pytest -v --tb=short

# Node / Jest
npm test -- --passWithNoTests 2>&1
# or: npx jest --passWithNoTests

# Node / Vitest
npx vitest run 2>&1

# Go
go test ./... -v 2>&1 | tail -50
```

**On test failures:**
- Read the test that failed
- Read the tested function in the source code
- Identify whether it's a regression (broken code) or an outdated test (test to update)
- Never delete a test to make it pass

---

## Phase 5 — Additional checks

```bash
# Required env variables present (if .env.example exists)
[ -f ".env.example" ] && [ -f ".env" ] && diff <(grep -v '^#' .env.example | grep '=' | cut -d= -f1 | sort) <(grep -v '^#' .env | grep '=' | cut -d= -f1 | sort) || echo "⚠️ Missing variables in .env"

# Unapplied migrations (if Alembic)
[ -d "alembic" ] && alembic current 2>&1 | grep -i "head\|behind" || true

# Missing dependencies
[ -f "requirements.txt" ] && pip check 2>&1 | grep -v "No broken" || true
[ -f "package.json" ] && npm ls 2>&1 | grep "UNMET\|missing" | head -10 || true
```

---

## Phase 6 — Report

```
╔══════════════════════════════════════════════════════════════════╗
║           BUILD CHECK — [DATE] — [PROJECT]                      ║
╠══════════════════════════════════════════════════════════════════╣
║  Detected stack: [Frontend] + [Backend] + [Test runner]         ║
╠══════════════════════════════════════════════════════════════════╣
║  RESULTS                                                         ║
║  TypeScript / Types   : ✅ OK  |  ❌ N errors                   ║
║  Production build     : ✅ OK  |  ❌ Failed                     ║
║  Lint (ESLint/Ruff)   : ✅ OK  |  ⚠️ N warnings  |  ❌ N errors ║
║  Unit tests           : ✅ N/N passed  |  ❌ N failed           ║
║  DB migrations        : ✅ Up to date  |  ⚠️ N pending          ║
╠══════════════════════════════════════════════════════════════════╣
║  VERDICT: ✅ DELIVERABLE  /  ⚠️ DELIVERABLE WITH RESERVATIONS  /  ❌ BLOCKED ║
╚══════════════════════════════════════════════════════════════════╝
```

For each ❌:

```
### [BUILD-N] — [Short error title]
**Command**: `npm run build` / `pytest` / `ruff check`
**Exact error**:
[exact extract of the error message]
**File**: `path/file.ts:line`
**Cause**: [explanation of why it breaks]
**Fix**: [precise correction to apply]
```

---

## Absolute rules

**Always:**
- Run the commands in order: types → build → lint → tests
- Read the full error message before diagnosing
- Cite the exact line of the offending file
- Distinguish "blocking error" (broken build) from "warning" (working code that should be fixed)
- Report the exact number of tests passed / failed / skipped

**Never:**
- Ignore a TypeScript error because the build "finishes anyway"
- Delete or comment out a test to make it pass
- Run `npm run build` without first running `tsc --noEmit` (the build can mask type errors)
- Modify source code to force a test to pass without understanding the regression
- Report "✅ OK" if the command couldn't run (missing binary, env not configured)

**Verdicts:**
- **✅ DELIVERABLE**: build OK + 0 type errors + 0 lint errors + all tests pass
- **⚠️ DELIVERABLE WITH RESERVATIONS**: build OK + lint warnings only (no blocking errors)
- **❌ BLOCKED**: broken build OR TypeScript error OR failed test

$ARGUMENTS
