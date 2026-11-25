---
name: review-before-merge
description: Pre-merge review for ZeroAgent Studio — CI, architecture, Bugbot, security. Use before PR, release, or when user asks for merge review.
disable-model-invocation: true
paths:
  - src/**/*
  - tests/**/*
  - package.json
---

# Review Before Merge

Structured review. Fix blockers before commit. **Findings only** unless user asks to fix.

## Order

1. **CI** — `.cursor/skills/pre-commit-ci/SKILL.md` (must pass first)
2. **Architecture** — static-only; layers intact; Prometheus fallback preserved
3. **Bugbot** — one `bugbot` subagent (`readonly: true`):

```text
Full Repository Path: <workspace root>
Diff: branch changes
```

Use `uncommitted changes` for dirty tree. `Base Branch: main` if branch not from main.

4. **Security** (keys, scraper, speech, fetch, deps) — `review-security` skill

## ZeroAgent checklist

- [ ] Brains: engine + `BrainType` + Settings + inspector + tests + `brainLabels`
- [ ] Tools: registry (`src/tools/registry.ts`) + tests — no hardcoded palette entries
- [ ] Keys via `keyStorage.ts` (session default); no hardcoded secrets
- [ ] `base: './'` in `vite.config.ts` unchanged or documented
- [ ] Heavy engines lazy-loaded
- [ ] Guide/README if user-facing behavior changed
- [ ] Coverage 100% on new logic

## Bugbot summary format

| Severity | Location (file:line) | Finding |

Sort highest severity first.

## After review

Blockers → fix → re-run CI + review. Clean → commit/PR per user request.

**Rule:** `.cursor/rules/zeroagent-reviewer.mdc`
