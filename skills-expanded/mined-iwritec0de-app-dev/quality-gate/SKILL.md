---
name: quality-gate
description: >-
  This skill should be used when the user asks to "run a quality gate", "check
  code quality", "run lint checks", "run pre-push security scan", "check for
  dead code", or mentions "quality gate", "quality check", "lint check", "run
  checks", "code quality", "pre-push scan", "security scan". Provides automated
  JavaScript/TypeScript code quality enforcement including type checking, linting,
  formatting, dead code detection, type coverage, circular dependency detection,
  tests, and security scanning before git push.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# Quality Gate

Automated quality enforcement with two hooks:

## Stop Hook — Code Quality

Fires on every session stop. Runs JavaScript/TypeScript checks on changed files:

| Check | Tool | Severity |
|-------|------|----------|
| Types | `tsc --noEmit` | BLOCK |
| Lint | `eslint` | BLOCK on errors, WARN on warnings |
| Format | `prettier --check` | WARN |
| Tests | `jest` | BLOCK |
| Dead code | `knip` (unused exports, deps, files) | WARN |
| Type coverage | `type-coverage` (>80% threshold) | WARN |
| Circular deps | `madge --circular` | WARN |
| TODO/FIXME | grep scanner | WARN |

**Behavior:**
- Missing required tools (tsc, eslint, prettier, jest) = FAIL with install command
- Missing optional tools (knip, type-coverage, madge) = WARN with install suggestion
- Retry limiter: allows stop after 3 consecutive failures

## PreToolUse Hook — Security Scan

Intercepts `git push` commands. Runs 4 scanners in sequence:

1. **semgrep** — SAST scan on changed files with `--config=auto`
   - Critical/High findings = BLOCK push
   - Medium findings = WARN
   - Claude should auto-fix findings before retrying

2. **gitleaks** — scans commits being pushed for leaked secrets
   - Any secret found = BLOCK push

3. **trivy** — filesystem vulnerability, secret, and misconfig scan
   - Critical vulns = BLOCK push
   - High vulns = WARN

4. **SonarQube** (optional) — checks quality gate status if configured
   - Requires `SONARQUBE_URL` and `SONARQUBE_TOKEN` env vars, plus `sonar-project.properties`
   - Skipped silently if `SONARQUBE_TOKEN` is not set
   - Failed quality gate = BLOCK push

## Configuration

| Env Var | Default | Purpose |
|---------|---------|---------|
| `CLAUDE_QUALITY_GATE` | `1` | Enable/disable quality gate |
| `CLAUDE_QUALITY_GATE_MAX_RETRIES` | `3` | Max retry attempts before allowing stop |
| `SONARQUBE_URL` | `https://sonarqube.internal` | SonarQube server URL |
| `SONARQUBE_TOKEN` | (none) | SonarQube auth token |
| `CLAUDE_NOTIFY_DISCORD` | `0` | Send Discord notifications |
| `DISCORD_WEBHOOK_URL` | (none) | Discord webhook for notifications |

## Commands

- `/quality run` — Run checks manually
- `/quality status` — View gate status and recent results
- `/quality config` — See active checks and tool availability
