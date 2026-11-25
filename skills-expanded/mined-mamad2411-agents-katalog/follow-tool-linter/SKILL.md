---
name: follow-tool-linter
description: Use a linter in the project
argument-hint: "[scope]"
related:
  - follow-tool-biome
  - follow-tool-eslint
  - follow-tool-formatter
  - follow-tool-hk
  - follow-tool-moonrepo
  - resolve-errors
  - run-lint
  - run-format
  - run-verify
---

## Goal

Use a linter in the project per tech stack

## Scope

Use linters for projects per tech stack

- Boundary: this skill helps pick and wire a linter into the repo/CI — after picking a tool, use the dedicated skill (`/follow-tool-eslint`, `/follow-tool-biome`) for detailed config; formatting lives in `/follow-tool-formatter`
- Latest: oxlint `1.85.0`, biome `2.5.14`, eslint `10.11.0`, ruff `0.16.7`, golangci-lint `2.13.2` (verified 2026-09-26)
- References: [cli](references/cli.md) | [apis](references/apis.md) 
## Execute

### 1. Select Linter

> Goal: pick the linter by project tech stack

1. Check the project's tech stack
2. Pick a suitable linter:
   - TypeScript/JavaScript: oxlint or biome
   - Rust: clippy
   - Go: golangci-lint
   - Python: ruff

### 2. Setup Linter

> Goal: install and configure the linter

1. Run `/follow-tool-biome` for TypeScript/JavaScript
2. Run `/follow-tool-eslint` for TypeScript/JavaScript
3. For oxlint: `bun add -D oxlint` then `bunx oxlint` — for type-aware rules, install `oxlint-tsgolint` as well
4. Run `clippy` for Rust (`rustup component add clippy` then `cargo clippy`)
5. For Python: `pipx install ruff` then `ruff check` (+ `ruff format` for the formatter)
6. For Go: `mise use -g golangci-lint` then `golangci-lint run`

### 3. Validate

> Goal: test the linter and check the configuration

1. Run the linter as a test (e.g. `bun run lint` or `bunx <linter> .`)
2. Check the configuration — effective rules match the intent, files that should be ignored aren't linted
3. Do `/run-verify` for a combined lint + typecheck check

### 4. Integrate With CI And Hooks

> Goal: the linter runs in CI and pre-commit

1. Add a lint step in CI (`/follow-tool-github-actions` for GitHub Actions) — use check mode, not fix
2. git hooks for linting staged files: a repo with `.moon/workspace.yml` → moon's `vcs.hooks`, e.g. `moon run :lint --affected --status=staged` (see `/follow-tool-moonrepo`); other repos or parallel staged-file linting → `/follow-tool-hk`
3. Use `--max-warnings 0` or the equivalent in CI when a zero-warning gate is wanted
4. On failing lint findings → do `/resolve-errors` before committing

## Rules

### 1. Linter Selection

- Pick the linter by tech stack — if the project already has one, keep it
- Separate lint (code quality) from format (style) — see `/follow-tool-formatter`
- In CI run check mode only; auto-fix (`--fix`) happens in local/hooks

### 2. Error Handling

- Use `/resolve-errors` when errors are found

- Use `/follow-tool-biome` for detailed Biome config
- Use `/follow-tool-eslint` for detailed ESLint config
- Use `/follow-tool-formatter` for the formatter (separate from lint)
- Use `/follow-tool-hk` for hooks in repos that don't use moon
- Use `/follow-tool-moonrepo` for `vcs.hooks` in a moon repo
- Use /resolve-errors if needed
- Use /run-lint if needed
- Use /run-format if needed
- Use /run-verify if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The linter is fully configured
- The linter works correctly
