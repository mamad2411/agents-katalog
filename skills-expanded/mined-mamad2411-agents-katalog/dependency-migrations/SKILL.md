---
name: dependency-migrations
description: Major version upgrades for React Next and toolchain - ordered steps rollback and test gates
tags:
  - dependencies
  - migration
  - nextjs
version: 1.0.1
category: development
outcomes:
  - Ordered checklist per package with codemod or manual notes
  - Test gate commands after each mergeable step
  - Rollback branch or tag suggestion
stack:
  - pnpm
  - next
  - react
last_reviewed: 2026-05-19
risk_level: medium
tools_allowed: suggest-shell
requires_user_approval: false
compatibility:
  - generic-markdown
  - skills-sh
  - cursor
  - claude-code
  - antigravity
  - codex
  - github-copilot
  - windsurf
  - gemini-cli
  - cline
  - amp
  - opencode
  - roo
  - goose
  - kilo
  - kiro-cli
  - droid
  - openclaw
  - trae
references:
  - references/stack-nextjs.md
  - references/skill-safety.md
  - references/dependency-security.md
---

# Instructions

## When to Use

- Use for ordered major upgrades (React/Next/toolchain) with rollback.
- Prefer `secure-dependencies` for audit/lockfile policy alone.
- Prefer `testing-agent` to define regression gates before bumping.

Plan **major upgrades** (Next, React, TypeScript, ESLint flat config, Vitest) with **small steps**.

1. **Baseline security:** run `pnpm audit` (or org equivalent); resolve or document allowlisted CVEs before bumping majors - pair with **`secure-dependencies`**.
2. Inventory current versions from lockfile and `package.json`.
3. Order upgrades: tooling that does not change runtime first, then framework, then breaking libs.
4. For each step: codemod link or manual file list; **tests to run** (`pnpm test`, `pnpm lint`, `pnpm build`).
5. **Next major:** read official upgrade guide for that jump only - do not merge multiple majors blindly.
6. Rollback: git branch or tag before step; document `pnpm install` restore.
## Outcomes

- Markdown checklist with gates; no 500-line single PR unless user insists.

## Output Rules

Numbered phases; each phase ends with verification commands.

## Scope and boundaries

- **In scope:** JS/TS dependency upgrades in one repo.
- **Out of scope:** database migrations, production cutover scheduling.

## Safety

- suggest-shell: user runs commands; warn on peer dependency overrides.

## Troubleshooting

- **Peer dependency hell:** prefer `pnpm.overrides` only with comment and owner approval.
- **Type explosion:** enable `skipLibCheck` temporarily only as documented bridge.

## Related skills

- [`secure-dependencies`](../secure-dependencies/SKILL.md) - audit policy during upgrades
- [`github-actions-ci`](../github-actions-ci/SKILL.md) - CI gates for majors
- [`testing-agent`](../testing-agent/SKILL.md) - regression tests before bump

**GitHub:** https://github.com/bh611627/skillcodex/tree/main/skills/dependency-migrations/SKILL.md  
**npm:** https://www.npmjs.com/package/@skillcodex/skills
