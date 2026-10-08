---
name: project-diagnosis
description: Structured gap analysis that identifies what a project is missing — not what's done poorly (that's /audit), but what's absent entirely. Checks for tests, CI, security basics, linting, type safety, deployment readiness, and dependency health. Each finding has a severity and a concrete fix action.
invoke_when: Use when starting a session (lightweight via hook), running /diagnose for full gap analysis, or when the project-doctor agent needs a gap inventory before fixing things.
---

# Project Diagnosis

## Purpose

Most projects don't fail because their code is bad — they fail because things are missing. No tests, no CI, no input validation, no error handling, no logging. This skill systematically checks for what's absent and surfaces concrete, actionable findings.

**This is NOT a code review.** The `/audit` command reviews code quality. This skill checks project infrastructure completeness.

## Diagnosis Checklist

Run through each category. For each check, record: present (pass), absent (finding), or not applicable (skip).

### 1. Testing Infrastructure
| Check | How to Verify | Severity if Missing |
|-------|--------------|-------------------|
| Test directory exists | Look for `tests/`, `__tests__/`, `test/`, `spec/`, or test file patterns (`*.test.*`, `*.spec.*`, `test_*.py`, `*_test.go`) | **High** |
| Test runner configured | `package.json` has `test` script, OR `pytest.ini`/`pyproject.toml` has pytest config, OR `go test` works | **High** |
| Coverage configured | `@vitest/coverage-v8`, `pytest-cov`, `go test -cover`, or equivalent is installed | **Medium** |
| At least 1 test exists | At least one test file has actual test cases (not just empty files) | **High** |

### 2. CI/CD Configuration
| Check | How to Verify | Severity if Missing |
|-------|--------------|-------------------|
| CI config exists | `.github/workflows/`, `.gitlab-ci.yml`, `.circleci/config.yml`, `Jenkinsfile`, `.travis.yml` | **Medium** |
| CI runs tests | CI config includes a test step | **Medium** |
| CI runs linter | CI config includes a lint step | **Low** |

### 3. Security Basics
| Check | How to Verify | Severity if Missing |
|-------|--------------|-------------------|
| `.env` in `.gitignore` | `.gitignore` exists and contains `.env` | **Critical** |
| No hardcoded secrets | Quick scan for patterns: `password = "`, `apiKey = "`, `secret = "`, `token = "` in source files | **Critical** |
| Input validation present | If API routes exist, check for Zod/Pydantic/validator imports near route handlers | **High** |
| Dependency audit clean | `npm audit` / `pip audit` / `go vuln` shows no critical vulnerabilities | **Medium** |

### 4. Code Quality Tools
| Check | How to Verify | Severity if Missing |
|-------|--------------|-------------------|
| Linter configured | ESLint config (`.eslintrc*`, `eslint.config.*`), Ruff config (`ruff.toml`, `pyproject.toml` with `[tool.ruff]`), or `golangci-lint` config | **Medium** |
| Formatter configured | Prettier config, Black/Ruff format config, or `gofmt` (built-in) | **Low** |
| Type checking | `tsconfig.json` with `strict: true`, or `mypy`/`pyright` configured, or Go (built-in) | **Medium** |

### 5. Architecture & Documentation
| Check | How to Verify | Severity if Missing |
|-------|--------------|-------------------|
| Architecture spec | `.shipworthy/architecture.md` exists | **Medium** |
| README exists | `README.md` in project root | **Low** |
| `.gitignore` exists | `.gitignore` in project root | **Medium** |

### 6. Deployment Readiness
| Check | How to Verify | Severity if Missing |
|-------|--------------|-------------------|
| Health endpoint | Scan for `/health`, `/healthz`, `/ping`, or `health_check` route | **Low** |
| Structured logging | Check for `pino`, `winston`, `logging` (Python), `slog` (Go) imports — not `console.log` | **Medium** |
| Error tracking | Check for Sentry, Bugsnag, Datadog, or similar error tracking setup | **Low** |
| Environment config | `.env.example` or environment variables documented somewhere | **Low** |

## Output Format

### For Session-Start Hook (Lightweight)
A single line injected into context:
```
Project health: [X] gaps found — [highest severity] priority: [top 1-2 findings]
```
Example: `Project health: 4 gaps found — Critical priority: .env not in .gitignore, no input validation`

If no gaps found: `Project health: All checks passed`

### For /diagnose Command (Full)
Organized by severity:

```
## Project Diagnosis Report

### Critical (fix immediately)
- [ ] .env not listed in .gitignore — secrets may be committed
- [ ] Hardcoded API key found in src/config.ts:14

### High (fix soon)
- [ ] No test files found — add a tests/ directory and at least one test
- [ ] No input validation — install Zod and validate route inputs

### Medium (improve when convenient)
- [ ] No CI configuration — add .github/workflows/ci.yml
- [ ] No linter configured — install ESLint with strict config

### Low (nice to have)
- [ ] No health endpoint — add GET /health for monitoring
- [ ] No .env.example — document required environment variables

### Passed
- [x] .gitignore exists
- [x] README exists
- [x] TypeScript strict mode enabled
```

## Tier-Adapted Presentation

- **Builder**: Show only Critical findings. Frame them as helpful: "I noticed a couple things I should fix before we go further."
- **Maker**: Show Critical and High. Frame as recommendations: "Here are some gaps I'd recommend addressing."
- **Engineer**: Show everything. Frame as a report: "Full diagnosis results below."

## Auto-Fix Capability

When invoked via `/diagnose --fix` or when the project-doctor agent runs:
- **Can auto-fix**: `.gitignore` creation/updates, linter config, test runner setup, CI workflow generation, health endpoint, `.env.example`
- **Cannot auto-fix**: Removing hardcoded secrets (needs human judgment on replacement), adding input validation to existing routes (needs understanding of expected inputs), configuring error tracking (needs account credentials)
- **Always ask before fixing**: Never silently modify existing files. Create new files freely, but modification requires user approval.
