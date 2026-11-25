---
name: file-refactor
description: >
  Keep source files under 500 lines. Split files that mix concerns — types,
  utils, hooks, sub-components, constants. Use when a file approaches the limit
  or when the user says refactor file, split file, too long, or file too big.
---

# File Refactor

Keep every source file under **500 lines**. Split before it crosses the limit.

## When to trigger

- A file exceeds 500 lines
- A module mixes types, utils, handlers, rendering, and constants
- A screen component contains inline sub-components that are extractable
- A service combines pure helpers, dataclasses, and orchestration in one file

## TypeScript / React splitting order

1. **Types** — interfaces, type aliases, enums → `types.ts`
2. **Pure utilities** — formatting, grouping, transforms → `utils.ts`
3. **Complex state logic** → `hooks/useXxx.ts`
4. **Sub-components** — UI pieces → `components/XxxYyy.tsx`
5. **Constants / config** — hardcoded arrays, config objects → `constants.ts`

## Python splitting order

1. **Data models** — `@dataclass`, `TypedDict`, `Protocol` → `models.py`
2. **Pure helpers** — side-effect-free formatting/parsing → `utils.py` or `*_format.py`
3. **Orchestration** — original file stays as coordinator (CLI entry, service facade)
4. **CLI groups** — subcommand handlers → dedicated modules
5. **Constants** — templates, frozensets → `constants.py`

## Rules

- **Single responsibility** — each file does one thing
- **Cohesion** — related code stays together
- **Preserve exports** — never break existing imports; re-export from original file if needed
- **Mirror neighbors** — follow existing package layout; don't invent new patterns
- After splitting: typecheck + lint must pass
