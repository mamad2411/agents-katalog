---
name: setup-ts-project-config
version: 4
description: >-
  Plan — don't execute — TypeScript project quality gates: Husky hooks, lint-staged, commitlint, linter/formatter (ESLint+Prettier or Biome), Vitest, and Knip dead-code detection. Writes a resumable plan to `<cwd>/.plans/setup-ts-project-config/plan.md`; re-runs reconcile against live state. Trigger on "plan precommit setup", "plan husky and lint-staged", "plan eslint/prettier/biome config", "add Knip", "set up code quality gates", "configure pre-commit hooks", or /setup-ts-project-config.
---

# Setup TS Project Config (planning)

Plan — don't build. This skill inspects a TypeScript project, asks the toolchain decisions once, and writes an **ordered, resumable plan** for wiring the standard quality gates: a Husky `pre-commit` hook driven by `lint-staged`, a `commit-msg` hook driven by commitlint, a linter and formatter (ESLint flat config + Prettier, or Biome for both), and a unit-test runner (Vitest by default; an existing Jest or `node:test` setup is kept). The plan lands at `<cwd>/.plans/setup-ts-project-config/plan.md`. **No project files are created or modified by this skill** — executing the plan is a separate step, done by hand or with whatever implementation workflow you use.

Use this when bootstrapping a fresh TS repo or retrofitting tooling onto one with none. Re-run any time: the skill re-reads an existing plan, reconciles it against the project's current state, and reports what's still outstanding.

## Core rules

1. **Plan only — never touch the project.** The single file this skill writes is `<cwd>/.plans/setup-ts-project-config/plan.md` (creating `.plans/setup-ts-project-config/` if needed). It never installs dependencies and never writes `eslint.config.*`, `package.json`, `.husky/`, `tsconfig.json`, etc. Those are *steps in the plan*, for someone else to run.
2. **Detect before planning.** Run `scripts/detect-stack.sh` first. Never assume the package manager — use the one the lockfile implies (pnpm / yarn / npm / bun); the plan's commands are written for that manager.
3. **Resumable.** On every invocation, check for an existing `plan.md`. If it exists, read it, re-run detection, mark steps the project now satisfies as `- [x]` with an "(already present)" note, refresh the detected-state table, and report the outstanding steps — never blow the file away, never delete a step the user has annotated. Only rewrite sections that changed.
4. **Never clobber — in the plan too.** If a config file already exists (`eslint.config.*`, `.prettierrc*`, `biome.json*`, `knip.config.*`, `commitlint.config.*`, `vitest.config.*`, `.husky/`), the plan records it as *present — leave as-is* instead of emitting an overwrite step, unless the user explicitly asked to replace it.
5. **One toolchain for lint+format.** Either ESLint+Prettier *or* Biome — never both. If the project already has one, the plan keeps it; otherwise the choice is asked and recorded in the plan.
6. **Keep the existing test runner.** The plan scaffolds Vitest only when no Jest / Vitest / `node:test` setup is detected.
7. **The plan is self-sufficient.** Every step is concrete: exact install command, exact file path plus the [REFERENCE.md](references/REFERENCE.md) section to copy from, exact `package.json` keys, exact hook contents. A reader should not have to re-derive anything.
8. **Verification is a planned step, not something this skill runs.** The final plan steps are "run lint / format:check / type-check / test, report results" and "exercise the hooks with a trivial commit" — instructions for the executor, not actions for this skill.

## Plan file format

`<cwd>/.plans/setup-ts-project-config/plan.md`:

- **Header** — date, target project root, detected package manager, `type: module` (yes/no), `tsconfig` style (`none` / `plain` / `references`).
- **Decisions** — lint+format toolchain; test runner (and Vitest DOM env if relevant); commitlint preset plus any custom header rule. Each with the value chosen and a one-line why.
- **Detected state** — a table: each tool/config marked present or absent; present ones tagged "leave as-is".
- **Steps** — a numbered `- [ ]` / `- [x]` checklist, each step ending with the REFERENCE.md section it draws from. Order: `git init` (if no repo) → `npm init -y` equivalent (if no `package.json`) → install deps → write linter config → write formatter config + ignore file → write `knip.config.ts` → write `vitest.config.ts` + sample `*.test.ts` (only if scaffolding Vitest) → write `commitlint.config.*` → create minimal `tsconfig.json` (only if none) → wire `package.json` scripts + `lint-staged` block → `husky init` → write `.husky/pre-commit` → write `.husky/commit-msg` → `chmod +x` the hooks → verify (lint, format:check, type-check, test) → exercise hooks via a trivial commit.
- **Notes** — project-specific gotchas for the executor: e.g. `type-check` = `tsc -b` when the tsconfig uses project references; add root configs like `vitest.config.ts` to a tsconfig `include`; the first `prettier --write` will reformat pre-existing source — confirm with the user before running it.

## Workflow

### 1. Locate / resume

If `<cwd>/.plans/setup-ts-project-config/plan.md` exists, read it; otherwise this is a fresh plan. Either way, continue to detection — the plan is always reconciled against the live project.

### 2. Detect

Run `scripts/detect-stack.sh [project-dir]` (defaults to cwd; ensure it is executable: `chmod +x scripts/detect-stack.sh`). It prints `key<TAB>value` lines: `root`, `pkg_manager`, `has_package_json`, `typescript`, `type_module`, `tsconfig`, `eslint`, `prettier`, `biome`, `vitest`, `jest`, `husky`, `lint_staged`, `commitlint`, `knip`, `tailwindcss`, `tailwind_v4`, `git_repo`. `tsconfig` is `none` (plan creates the minimal one), `plain` (`type-check` = `tsc --noEmit`), or `references` (`type-check` = `tsc -b`). If `git_repo` is `no`, the plan's first step is `git init` (hooks need a repo). If `typescript` is `no`, the plan includes installing it. If the script exits 65 (no `package.json`), the plan starts with `npm init -y` (or the detected manager's equivalent).

### 3. Decide

If a plan exists, confirm its recorded decisions still hold; otherwise ask — bundle into one round:
- **Lint+format toolchain** — `ESLint + Prettier` or `Biome`. Skip the question if one is already present; use that.
- **Test runner** — confirm planning Vitest if none detected; for browser/DOM code, ask whether a `jsdom` / `happy-dom` env is wanted.
- **commitlint preset** — default `@commitlint/config-conventional`; ask whether they want extra header rules (the custom `header-format` example in [REFERENCE.md](REFERENCE.md#commitlint)).

### 4. Write the plan

Write (or update) `<cwd>/.plans/setup-ts-project-config/plan.md` in the format above, pulling dependency lists and templates from [REFERENCE.md](references/REFERENCE.md) by reference. When updating an existing plan: mark now-satisfied steps `- [x] (already present)`, refresh the detected-state table, leave everything else — including any user annotations — intact.

### 5. Hand off

Tell the user the plan path, summarise the outstanding steps, and note that executing them is up to the user — by hand, or with whatever implementation workflow they use. Remind them that re-running this skill re-reads the plan and reports status. **Do not execute any step.**

## Companion files

- [REFERENCE.md](references/REFERENCE.md) — the template library the plan's steps cite: copy-paste config templates (ESLint flat config, Prettier, Biome, Knip, commitlint, Vitest, lint-staged, Husky hooks), per-toolchain dependency lists, and the package.json script sets. Consulted when writing the plan, not on every run.

## Scripts

- `scripts/detect-stack.sh [project-dir]` — inspects the project (nearest `package.json` upward from the given dir; default cwd) and prints `key<TAB>value` lines describing the package manager and which tools/configs are already present. Exit `0` ok, `64` usage error, `65` no `package.json` found.
