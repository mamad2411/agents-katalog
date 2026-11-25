---
name: ship-patch
description: End-to-end patch workflow for ZeroAgent Studio — implement, test, review, version, commit. Use when shipping a fix or feature branch.
paths:
  - src/**/*
  - tests/**/*
  - package.json
  - CHANGELOG.md
---

# Ship Patch

Focused branch → green gate → optional review → version/docs → commit (user request only).

## Steps

1. **Branch** — from `main`; one concern per branch
2. **Implement** — `.cursor/rules/zeroagent-engineer.mdc`; minimal diff; no backend
3. **Test** — `npm ci` + `npm run ci` (`.cursor/skills/pre-commit-ci/SKILL.md`)
4. **Review** (optional) — `.cursor/skills/review-before-merge/SKILL.md`
5. **Document** — user-visible → `CHANGELOG.md` + `#/guide` if behavior changed
6. **Version** — `.cursor/skills/release-versioning/SKILL.md` when shipping
7. **Commit** — only after green gate; **user must ask**
8. **Deploy** — push to `main` (GitHub Actions) or `npm run deploy` when user asks

## Do not

- Commit on red CI
- Add server deps or repo-stored secrets
- Store API keys outside `src/lib/keyStorage.ts` / Settings panel

## Final reply (token-efficient)

Execution plan with `[x]` · files touched · gate result · version bump (if any)
