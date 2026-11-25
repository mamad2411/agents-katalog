---
name: follow-lib-tanstack-intent
description: Use TanStack Intent — ship agent skills with npm packages
argument-hint: "[package-name]"
related:
  - follow-lib-tanstack-ecosystem
  - resolve-errors
---

## Goal

Use TanStack Intent — the standard way to pack **agent skills** into an npm package so consumers can install that lib's skills into their agent tooling

## Scope

Use when maintaining an npm package and you want to ship skills (e.g. Devin/Claude/Cursor-compatible skills) with the package — for package authors, not app developers — **0.x**: check `https://tanstack.com/intent/latest` before implementing

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install And Layout

> Goal: install the package and lay out the skill files in the npm package

```bash
bun add -D @tanstack/intent
```

1. Place skill files per the convention the package defines (generally a `skills/` directory in the package root — check the latest docs)
2. Each skill = a dir with a `SKILL.md` like this repo — frontmatter `name`/`description`/`related`

### 2. Publish And Consume

> Goal: consumers can install skills from the package

1. Publish the package normally — `skills/` must be in the published files (check the `files` field in `package.json`)
2. Consumers run the intent CLI/MCP to discover + install skills from installed deps into their own agent config dir
3. Sync skill versions with the package version — skill content must match that release's API

### 3. Verify

> Goal: prove the skill resolves from the published package before finishing

1. `npm pack --dry-run` — confirm `skills/` is in the tarball
2. Install in a test project, then discover the skill through intent tooling
3. On failure → `/resolve-errors` max 3 rounds

## Rules

- Skills in the package must match the code version — no stale examples
- `files` in `package.json` must cover the skills dir — otherwise they aren't published
- For library authors only — app projects don't need it

## Expected Outcome

- The package publishes with skills in the tarball
- Consumers discover and install skills via intent tooling
