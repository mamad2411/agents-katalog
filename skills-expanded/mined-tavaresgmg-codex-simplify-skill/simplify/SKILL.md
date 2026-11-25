---
name: simplify
description: >
  Code refactoring engine that improves clarity, consistency, and maintainability while
  preserving exact functionality. Triggers on: "simplify", "refactor", "clean up",
  "improve readability", "code quality", "find problems", "audit code", "review module".
  Do NOT use for: adding features, writing tests, formatting, or architecture changes.
---

# Code Simplifier

Senior refactoring engineer. Goal: make code **obvious** — where the next developer
reads it and thinks "of course."

## Iron Laws

1. **FUNCTIONALITY IS SACRED** — Zero behavior changes. Tests that passed before must pass after.
2. **CLARITY OVER BREVITY** — Explicit beats clever. A 5-line `if/else` beats a nested ternary.
3. **CONSISTENCY OVER PERFECTION** — Follow project patterns. Migrate ALL or NONE.
4. **ATOMIC CHANGES** — One concern per edit. Each change independently reviewable.
5. **EVIDENCE OVER OPINION** — "It's cleaner" is NOT valid. "Reduces nesting 5→2 via guard clauses" IS.

## Mode Detection

- **Refactor** (default) — find problems AND fix them.
- **Audit** — find and report WITHOUT editing. Triggers: "find problems", "audit", "scan", "what's wrong with".

## Process

### Phase 1 — Scope

1. User specified files → use exact scope.
2. User specified directory/module → recurse all source files.
3. "Entire repo" → `git ls-files` filtered to source extensions, warn about context cost, batch.
4. No arguments → `git diff --name-only HEAD` + `git diff --name-only --cached` for recent changes.
5. No files found → ask user.

### Phase 2 — Context Loading

Batch all reads in parallel:
1. Project standards — CLAUDE.md, AGENTS.md, .editorconfig, linter configs.
2. ALL target files completely.
3. Adjacent files — imports, importers, shared types.

Identify project conventions from what you read (naming, import style, error handling, patterns).

### Phase 3 — Analysis

Analyze across three dimensions simultaneously:
1. **Structural** — long functions, deep nesting, high cyclomatic complexity, large param lists.
2. **Smells** — DRY violations (3+ identical blocks), dead code, magic values, feature envy.
3. **Consistency** — naming deviations, import ordering, type annotation gaps, stale comments.

Return findings as: `[file:line] — issue — confidence (0-100)`.

### Phase 4 — Prioritized Plan

Score each finding (0-100):
- **76-100:** Must fix — complexity bomb, bug risk, convention violation.
- **51-75:** Apply — clear improvement with concrete benefit.
- **26-50:** Apply only if zero-risk and obvious.
- **0-25:** Skip — subjective preference.

**Audit mode →** present report and STOP.

**Refactor mode — decision gate:**
- < 10 low-risk edits → proceed autonomously.
- \> 10 edits OR structural changes → present summary, ask user.
- Public API changes → ALWAYS ask first.

### Phase 5 — Refactoring

1. Work in priority order (Critical → Improvement → Minor).
2. Re-read current file state before each edit.
3. Group related changes in same file.
4. Never edit a file not read in this session.

**Stop-loss:** Same edit fails twice → STOP. Log as "attempted, reverted — reason" and move on.

### Phase 6 — Verification

**Mandatory. No exceptions.**

Discover project commands (package.json, Makefile, pyproject.toml, Cargo.toml) then run in parallel:
1. Lint (`npm run lint`, `ruff check .`, `cargo clippy`, etc.)
2. Typecheck (`tsc --noEmit`, `mypy .`, `cargo check`, etc.)
3. Tests covering modified code.

Zero new errors. If verification fails: revert the failing change, report, move on.

### Phase 7 — Report

```
## Simplification Report

### Execution
- Mode: refactor | audit
- Scope: N files (recent changes | directory: X | entire repo)

### Changes Applied (N total)
- [file:line] — What changed — Why (confidence: N)

### Verification
- Lint: PASS/FAIL | TypeCheck: PASS/FAIL | Tests: PASS/FAIL (N passed, M total)

### Metrics
- Lines: +N / -M (net: ±K) | Files touched: N

### Flagged for Future
- [file:line] — What could improve — Why not now
```

## Parallelism Strategy

| Scope | Strategy |
|-------|----------|
| 1-5 files | Single agent, sequential analysis |
| 6-20 files | Spawn 3 explorer agents for Phase 3 (one per analysis dimension) |
| 20+ files | Explorers per module for Phase 3 + worker agents per independent module for Phase 5 |

Module independence: no mutual imports, no shared mutable state, no cross-module findings.
If unsure → sequential. Safety > speed.

## Anti-Rationalization Checklist

Before ANY change, verify:

- [ ] Can you name the SPECIFIC metric improved? ("cleaner" is not a metric)
- [ ] Did you search ALL references before removing code?
- [ ] Does the abstraction have 3+ usages? (2 similar → tolerate, 3 identical → extract)
- [ ] Are you migrating ALL instances of a pattern, not creating inconsistency?
- [ ] Is your diff smaller than the original code that triggered the review?
- [ ] Are you staying in declared scope? ("while I'm here..." = scope creep)
- [ ] Would a senior engineer unfamiliar with the task understand WHY each change was made?

If any check fails → **STOP. Re-read Iron Laws. Stay in scope.**

## Boundaries

Does NOT: add features, write tests, change architecture, format code, upgrade dependencies,
or touch code outside scope.

## Adaptation

Project docs > codebase patterns > textbook rules. Follow what the team does, not what's ideal.
