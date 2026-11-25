---
name: pre-commit-ci
description: Run ZeroAgent Studio quality gate (audit, lint, typecheck, coverage, build) before commit or merge. Use when committing, fixing CI, or finishing implementation.
paths:
  - package.json
  - package-lock.json
  - src/**/*
  - tests/**/*
  - vite.config.ts
---

# Pre-Commit CI

Run before commit or merge-ready sign-off. **Do not commit on red.**

## Install

```bash
npm ci
```

Use `npm ci` (not `npm install`) when lockfile must match — CI and releases.

## Gate

```bash
npm run ci
```

| Step | Pass criteria |
|------|----------------|
| audit | 0 vulnerabilities (moderate+) |
| lint | ESLint clean |
| typecheck | `tsc --noEmit` |
| test:coverage | 100% on included `src/` |
| build | Vite production build |

## Workflow

1. After `package.json` deps: `npm install` once → commit lockfile → verify `npm ci`
2. After `src/` / `tests/` edits: full `npm run ci` — not lint-only
3. Fix all failures; re-run until exit 0
4. Report briefly: command + pass/fail (token-efficient)

## Fallback (if `ci` script broken)

```bash
npm audit --audit-level=moderate && npm run lint && npm run typecheck && npm run test:coverage && npm run build
```

## Notes

- Coverage excludes pure UI shells — see `vite.config.ts` `coverage.exclude`
- Chunk size warnings on build are OK if exit 0
- Windows: run in repo root; no special CRLF handling for this repo

**Rule:** `.cursor/rules/pre-commit-quality-gate.mdc`
