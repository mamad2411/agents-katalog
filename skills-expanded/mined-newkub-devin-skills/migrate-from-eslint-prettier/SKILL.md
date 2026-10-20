---
name: follow-tool-biome-migrate-from-eslint-prettier
description: Migrate ESLint/Prettier → Biome — rules mapping, incremental, verify
argument-hint: "[project-path]"
related:
  - follow-tool-biome
  - follow-tool-eslint
  - deep-impact
  - run-lint
  - report-before-after
---

## Goal

Move ESLint (+ Prettier) to Biome incrementally — `biome migrate` converts rules automatically, verify equivalent coverage, with rollback available

## Scope

- For projects with `.eslintrc*`/`eslint.config.*` and/or `.prettierrc*`
- Covers `biome migrate eslint`, `biome migrate prettier`, rules mapping, incremental adoption
- If ESLint must run alongside Biome temporarily → plan the overlap in step 4

## Execute

### 1. Baseline

> Goal: know the original coverage before migrating

1. Run `eslint .` recording error/warning counts per rule (use `--format json` for a detailed diff)
2. Run `prettier --check .` recording the original formatting state
3. List all ESLint configs + plugins — do `/deep-impact` for a monorepo
4. Commit the state before starting — the rollback path must be ready

### 2. Install Biome And Migrate

> Goal: use the official migrate commands

1. `bun add -D @biomejs/biome` then `bunx biome init` if no config exists
2. Run `bunx biome migrate eslint --write` — converts the ESLint config → Biome rules
3. Run `bunx biome migrate prettier --write` — converts the Prettier config → formatter options
4. Review the generated diff — the tool converts only rules with equivalents; the rest need a manual decision

### 3. Map Remaining Rules

> Goal: handle rules without an equivalent

1. List ESLint rules that couldn't migrate — check the Biome rules docs for an equivalent
2. Plugin rules (react, import, etc.) → check which Biome linter rules/domains cover them
3. Rules missing in Biome → decide: accept lower coverage, keep ESLint for just those rules, or use a Biome plugin — see official docs
4. Write the mapping table into the report

### 4. Incremental Adoption

> Goal: switch step by step, no big-bang

1. Enable `biome check` on file/folder subsets via `files.includes`/`overrides` in `biome.jsonc`
2. Transition period: ESLint can still run alongside in CI — disable rules Biome already covers in the ESLint config to prevent double-reporting
3. Formatter: switch Prettier → Biome format in one go (the format diff is large — prepare a separate format commit)
4. Update editor settings: disable ESLint/Prettier extensions for scopes Biome already owns

### 5. Verify And Clean Up

> Goal: Biome covers equivalently, then remove the old tools

1. Run `bunx biome check .` → diagnostics sensible versus the ESLint baseline
2. Run the test suite — auto-fix may change code, so tests are required
3. All passing → remove `eslint`/`prettier` deps + configs, switch CI to `biome ci` — in a separate commit
4. Not passing → keep ESLint for the still-needed rules, report what remains

## Rules

### 1. Safety

- Always use `biome migrate` commands before manual edits
- Keep the format commit separate from logic changes
- Never delete ESLint until the coverage verification passes

### 2. Coverage

- The report must clearly list dropped rules — never claim a "complete migration" while unmapped rules remain
- Biome auto-fix may differ from ESLint — review fix diffs before committing

## Expected Outcome

- `biome.jsonc` covers lint+format equivalent to the old ESLint/Prettier setup
- Clear rules mapping — knowing what was lost and why
- CI runs `biome ci`; old deps removed (or kept with a stated reason)
