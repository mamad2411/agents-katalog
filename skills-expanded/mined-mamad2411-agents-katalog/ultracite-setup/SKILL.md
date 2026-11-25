---
name: ultracite-setup
description: >
  Fully install and wire Ultracite (Biome-first lint/format) into a JS/TS repo or monorepo:
  non-interactive init, package scripts, husky + lint-staged, VS Code/editor settings,
  Prettier/ESLint cleanup, biome.jsonc presets and pragmatic rule overrides, green check,
  and AGENTS.md notes. Use when the user runs /ultracite-setup, or asks to "add ultracite",
  "setup ultracite", "init ultracite", "wire biome/ultracite", "replace prettier with ultracite",
  "lint-staged ultracite", or fully configure monorepo lint/format with Ultracite.
---

# Ultracite setup (full project wiring)

Agent playbook: install Ultracite end-to-end so `check`/`fix`, editor format-on-save, and pre-commit all work. Prefer **Biome** backend unless the user asks for ESLint or Oxlint.

Companion skill: general day-to-day Ultracite usage may also exist as `ultracite`. This skill owns **first-time and full re-setup**.

## Goals (definition of done)

1. `ultracite` + linter package in root `devDependencies`
2. Config extends Ultracite presets (`biome.jsonc` / eslint / oxlint)
3. Root scripts: `check`, `fix`, `lint`, `format` (and `prepare` if husky)
4. Editor: Biome as default formatter (no leftover Prettier default)
5. Optional: husky pre-commit runs lint-staged, which runs `ultracite fix`
6. Conflicting tools removed (Prettier when using Biome; legacy eslintrc)
7. `ultracite doctor` all pass
8. `ultracite check` (or `pnpm check`) exits 0 — use auto-fix + **pragmatic overrides** on existing codebases rather than rewriting the universe in one PR
9. AGENTS.md / contributing notes mention the commands (merge; do not clobber project non-negotiables)

## Step 0 — Detect package manager and stack

Read root `package.json`, workspace files (`pnpm-workspace.yaml`, `turbo.json`, `nx.json`), and frameworks:

| Signal | Framework / preset flag |
|--------|-------------------------|
| `next` | `--frameworks next` (and usually `react`) |
| `react` / `react-dom` | `react` |
| `vitest` | `vitest` |
| `jest` | `jest` |
| Vue / Svelte / Solid / etc. | matching preset |

Package manager from `packageManager` field or lockfile:

- `pnpm-lock.yaml` → `pnpm`
- `yarn.lock` → `yarn`
- `bun.lock` / `bun.lockb` → `bun`
- else `npm`

Detect existing lint/format: `biome.json(c)`, `eslint.config.*`, `.prettierrc*`, `prettier` in deps, husky, lint-staged.

## Step 1 — Non-interactive init

Run from repo root (use the project PM's dlx):

```bash
# pnpm (common in Xylex monorepos)
pnpm dlx ultracite init \
  --pm pnpm \
  --linter biome \
  --editors universal \
  --frameworks react next vitest \
  --integrations husky lint-staged \
  --type-aware \
  --quiet
```

Adjust flags:

- Drop frameworks that do not apply
- Omit `--integrations husky lint-staged` if the user does not want hooks
- Prefer **not** passing `--agents universal` when `AGENTS.md` already has project rules — merge Ultracite notes by hand instead of overwriting
- Use `--type-aware` for Biome on TypeScript-heavy apps unless the user declines

If init is interactive only, pass the same choices via flags + `--quiet` / `CI=true`.

## Step 2 — Harden package.json scripts

Ensure root scripts (names can alias):

```json
{
  "scripts": {
    "lint": "ultracite check",
    "format": "ultracite fix",
    "check": "ultracite check",
    "fix": "ultracite fix",
    "prepare": "husky"
  }
}
```

- Remove `prettier --write` / eslint-only `lint` that would fight Ultracite
- Keep `typecheck` as `tsc` (or monorepo `-r typecheck`) — Ultracite does not replace typecheck
- Workspace packages: prefer root-owned lint. If packages need a script, use  
  `pnpm -w exec ultracite check <path>` (pnpm) rather than fragile `cd ../..`

Remove `prettier` from `devDependencies` when Biome is the formatter. Run install to refresh the lockfile.

## Step 3 — Editor + extensions

`.vscode/settings.json`:

- `editor.defaultFormatter`: **`biomejs.biome`** (not `esbenp.prettier-vscode`)
- Per-language formatters for js/ts/json/css/md/etc. → Biome
- `editor.formatOnSave`: true
- `editor.codeActionsOnSave`: `source.fixAll.biome` + `source.organizeImports.biome` as `explicit`

`.vscode/extensions.json`:

```json
{
  "recommendations": ["biomejs.biome"]
}
```

Init's "universal" editors may leave Prettier as the top-level default — **always fix that**.

## Step 4 — Husky + lint-staged

`.husky/pre-commit` should be only:

```sh
pnpm exec lint-staged
```

(or `npx` / `yarn` / `bunx` equivalent). Do **not** leave a mid-file `#!/bin/sh`, do not force full `pnpm test` on every commit unless the user asks.

`.lintstagedrc.json` (prefer local bin, not forever-dlx):

```json
{
  "*.{js,jsx,ts,tsx,json,jsonc,css,scss,md,mdx}": [
    "pnpm exec ultracite fix"
  ]
}
```

## Step 5 — biome.jsonc files + monorepo ignores

Start from init's `extends`. Add exclusions (Biome: list `!` patterns only when the extended preset already includes `**` — **do not add a second `"**"`** or Biome errors):

```jsonc
{
  "$schema": "./node_modules/@biomejs/biome/configuration_schema.json",
  "extends": [
    "ultracite/biome/core",
    "ultracite/biome/type-aware",
    "ultracite/biome/react",
    "ultracite/biome/next",
    "ultracite/biome/vitest"
  ],
  "files": {
    "includes": [
      "!**/node_modules",
      "!**/dist",
      "!**/.next",
      "!**/coverage",
      "!**/.turbo",
      "!**/pnpm-lock.yaml"
      // plus generated seeds, SPEC.json dumps, etc.
    ]
  }
}
```

See [references/monorepo-wiring.md](references/monorepo-wiring.md).

## Step 6 — Green `check` on existing codebases

1. Run `pnpm exec ultracite doctor` — fix failures first.
2. Run `pnpm fix` / `ultracite fix` (optionally `biome check --write --unsafe` for remaining safe churn).
3. Aggregate remaining rules:

```bash
pnpm exec biome check --max-diagnostics=5000
# group by rule id; fix real bugs; turn off or defer pure style noise
```

4. Apply **pragmatic overrides** in `biome.jsonc` for adoption (document *why* in comments). Common NodeNext / monorepo sets:

| Rule | Often off when… |
|------|------------------|
| `correctness/useImportExtensions` | TS ESM uses `.js` specifiers that resolve to `.ts` |
| `correctness/noUnresolvedImports` | pnpm workspace packages Biome cannot resolve |
| `assist/source/useSortedKeys` (+ interface/attributes) | Mass churn on domain types |
| `performance/noBarrelFile` | Intentional package entry barrels |
| `performance/noJsxPropsBind` | Existing React renderers |
| `style/noNonNullAssertion` | Gradual strictness |
| `suspicious/noUnnecessaryConditions` | Type-aware false positives on unions |
| `performance/noAwaitInLoops` | Sequential migrate/seed scripts |
| a11y click/label rules | Complex builder shells; tighten later |

Default stance: **format + correctness green first**; re-enable strict style in later PRs. Full override catalog: [references/rule-overrides.md](references/rule-overrides.md).

5. Re-run until:

```bash
pnpm exec ultracite doctor   # all pass
pnpm check                   # exit 0
```

6. Smoke existing unit tests if the auto-fix touched many files.

## Step 7 — Docs for humans and agents

Merge into `AGENTS.md` (preserve project non-negotiables):

```markdown
## Lint / format

Ultracite (Biome) is the monorepo linter and formatter.

pnpm check   # ultracite check
pnpm fix     # ultracite fix

Pre-commit: lint-staged runs ultracite fix on staged files.
```

Update README/contributing only if those files are hand-maintained (not pure generated docs).

## Step 8 — Report to user

Summarize:

- Backend + version (`ultracite`, `@biomejs/biome`)
- Scripts, hooks, editor
- What was removed (Prettier/ESLint)
- Override rationale (if any)
- Doctor + check results
- Files reformatted by first `fix` (scope of diff)

Do **not** commit unless asked.

## Anti-patterns

- Leaving Prettier as default formatter while Biome owns format
- `pnpm dlx ultracite` in lint-staged forever when the package is installed locally
- Overwriting a rich `AGENTS.md` with generic agent stubs
- Adding `"**"` to `files.includes` when Ultracite core already catch-alls
- Claiming "setup complete" while `check` still fails thousands of style nits with no plan
- `git add -A` of unrelated dirty work while only wiring Ultracite

## Quick command cheat sheet

```bash
pnpm dlx ultracite init --pm pnpm --linter biome --editors universal \
  --frameworks react next vitest --integrations husky lint-staged --type-aware --quiet
pnpm exec ultracite doctor
pnpm check
pnpm fix
pnpm exec biome check --write --unsafe   # optional broader autofix
```
