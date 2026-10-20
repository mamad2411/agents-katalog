---
name: tailwind-canonicalize
description: >
  Install and wire tailwind-canonicalize into a JS/TS repo: detect package manager and
  favored lint/format stack (Biome, Ultracite, ESLint, Oxlint, Prettier), add the package
  as a devDependency, add package.json scripts, compose lint-staged/CI so canonicalize owns
  semantic Tailwind rewrites while the existing linter keeps format/lint, then verify the CLI
  runs and check/fix pipelines work. Use when the user runs /tailwind-canonicalize, or asks
  to "add tailwind-canonicalize", "setup tailwind canonicalize", "install tailwind-canonicalize",
  "wire canonicalize with biome/eslint/oxlint", "canonicalize tailwind classes in CI", or
  compose theme-safe arbitrary→named rewrites next to existing lint tools.
---

# tailwind-canonicalize setup (install + lint composition)

Agent playbook: install **tailwind-canonicalize** end-to-end in the **current repository**, compose it with whatever lint/format stack the repo already favors (Biome / Ultracite / ESLint / Oxlint / Prettier), and **verify** the CLI works. Prefer local project install over global.

**Ownership (non-negotiable):**

| Concern | Owner |
|---------|--------|
| Quote style, imports, unused vars, a11y | Biome / ESLint / Oxlint / Prettier |
| `w-[40px]` → `w-10`, migrations, tokens | **tailwind-canonicalize** |
| CSS generation | Tailwind CLI / Vite plugin |

Canonicalize is **standalone**. It does not replace Biome/ESLint/Oxlint. Integration is **orchestration**, not a plugin inside the linter.

Official docs (prefer Context7 / live site when versions drift):

- https://tailwind-canonicalize.xbp.app
- Repo guides (when working inside this monorepo): `docs/guides/integrations.md`, `biome.md`, `eslint.md`, `oxlint.md`, `cli.md`, `ci.md`

## Goals (definition of done)

1. Node.js **≥ 20** available
2. `tailwind-canonicalize` in root (or app) `devDependencies` — not only a one-off `dlx`
3. Scripts: `canonicalize`, `canonicalize:check`, and composed `fix` / `check` that run **canonicalize before** the favored linter
4. Favored stack detected and wired (Biome | Ultracite | ESLint | Oxlint | Prettier-only | none)
5. Optional but recommended: lint-staged / husky / lefthook runs canonicalize **before** format/lint on class-bearing files
6. Optional CI step: `--check` (or `--check --json`) as its **own** step
7. Verification:
   - `pnpm exec tailwind-canonicalize --version` (or npm/yarn/bun equivalent) succeeds
   - `… --help` succeeds
   - Dry run: `… . --check --safe` (or scoped path) exits 0 or 1 with a real report (not install/CLI crash)
   - Composed `check` / `fix` still invoke the favored linter
8. Short note in `AGENTS.md` / README only if those files are hand-maintained — **merge**, do not clobber project rules
9. Do **not** commit unless the user asks

## Step 0 — Detect package manager, Node, and lint favor

From repo root, read:

- `package.json`, lockfiles, workspace files (`pnpm-workspace.yaml`, `turbo.json`, `nx.json`)
- Lint configs and deps

### Package manager

| Signal | PM |
|--------|-----|
| `packageManager`: `pnpm@…` or `pnpm-lock.yaml` | `pnpm` |
| `yarn.lock` | `yarn` |
| `bun.lock` / `bun.lockb` | `bun` |
| else | `npm` |

Install command:

```bash
pnpm add -D tailwind-canonicalize
npm i -D tailwind-canonicalize
yarn add -D tailwind-canonicalize
bun add -d tailwind-canonicalize
```

### Lint / format favor (pick strongest match)

Inspect in order; first strong signal wins for **primary** composition:

| Priority | Signals | Primary stack |
|----------|---------|----------------|
| 1 | `ultracite` in deps / scripts | **Ultracite** (Biome backend) |
| 2 | `biome.json` / `biome.jsonc` or `@biomejs/biome` | **Biome** |
| 3 | `eslint.config.*` / `.eslintrc*` or `eslint` scripts | **ESLint** |
| 4 | `.oxlintrc*` or `oxlint` in deps/scripts | **Oxlint** |
| 5 | Prettier only (`.prettierrc*`, no Biome) | **Prettier** (format after canonicalize) |
| 6 | None of the above | **CLI-only** (scripts without lint composition) |

Secondary tools can still run in CI (e.g. Oxlint + Biome). Document multi-tool order in scripts:

```text
1. tailwind-canonicalize --write / --check
2. primary linter/formatter
3. optional second linter
4. tsc / tests
```

### Tailwind presence

- Prefer CSS-first v4 (`@import "tailwindcss"`, `@theme`) or `tailwind.config.*`
- Peer `tailwindcss` is optional; install only if the user wants `--strict-compile`
- If no Tailwind in the repo, still install canonicalize but **warn** that rewrites need a theme and skip aggressive full-tree `--write` until config exists

### Paths to scan

Default `.` at monorepo root may be fine. Prefer app/package roots with real UI if the monorepo is huge:

- `apps/web`, `apps/docs`, `packages/ui`, etc.
- Skip pure server crates with no class strings when wiring turbo/nx targets

## Step 1 — Prerequisites

```bash
node -v   # must be >= 20
```

If Node is too old, stop and tell the user to upgrade before installing.

Optional: confirm the published package resolves:

```bash
# pnpm
pnpm view tailwind-canonicalize version
```

## Step 2 — Install in the repository

From the appropriate package root (usually monorepo root):

```bash
pnpm add -D tailwind-canonicalize
```

Use the detected PM. Prefer **workspace root** `devDependencies` when scripts and CI run from root; for app-scoped tooling only, install in that package and use filter/exec.

**Do not** rely forever on `pnpm dlx tailwind-canonicalize` for hooks/CI after setup — local bin is the contract.

### Optional: system / global CLI

Only if the user explicitly wants a global binary for ad-hoc use outside projects:

```bash
npm i -g tailwind-canonicalize
tailwind-canonicalize --version
```

Still install the **project** dep for reproducible CI. Prefer project-local `pnpm exec` / `npx` in scripts.

## Step 3 — package.json scripts

Merge (do not delete unrelated scripts). Template — swap the lint half per favor:

### Shared canonicalize scripts

```json
{
  "scripts": {
    "canonicalize": "tailwind-canonicalize . --write --safe",
    "canonicalize:check": "tailwind-canonicalize . --check --json"
  }
}
```

Scope paths when needed: `tailwind-canonicalize src --write --safe` or multiple roots.

### Biome

```json
{
  "scripts": {
    "canonicalize": "tailwind-canonicalize . --write --safe",
    "canonicalize:check": "tailwind-canonicalize . --check --json",
    "lint": "biome check .",
    "lint:fix": "biome check --write .",
    "fix": "pnpm canonicalize && pnpm lint:fix",
    "check": "pnpm canonicalize:check && pnpm lint"
  }
}
```

### Ultracite

```json
{
  "scripts": {
    "canonicalize": "tailwind-canonicalize . --write --safe",
    "canonicalize:check": "tailwind-canonicalize . --check",
    "lint": "ultracite check",
    "fix": "tailwind-canonicalize . --write --safe && ultracite fix",
    "check": "tailwind-canonicalize . --check && ultracite check"
  }
}
```

### ESLint

```json
{
  "scripts": {
    "canonicalize": "tailwind-canonicalize . --write --safe",
    "canonicalize:check": "tailwind-canonicalize . --check",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "fix": "pnpm canonicalize && pnpm lint:fix",
    "check": "pnpm canonicalize:check && pnpm lint"
  }
}
```

If `eslint-plugin-tailwindcss` rewrites arbitrary values → scale keys, **disable** those rules. Keep sort/conflict rules if desired.

### Oxlint

```json
{
  "scripts": {
    "canonicalize": "tailwind-canonicalize . --write --safe",
    "canonicalize:check": "tailwind-canonicalize . --check",
    "lint": "oxlint .",
    "fix": "pnpm canonicalize",
    "check": "pnpm canonicalize:check && pnpm lint"
  }
}
```

Oxlint is mostly a reporter — rewrites stay on canonicalize.

### Oxlint + Biome

```json
{
  "scripts": {
    "fix": "tailwind-canonicalize . --write --safe && biome check --write .",
    "lint": "oxlint . && biome check .",
    "check": "tailwind-canonicalize . --check && oxlint . && biome ci ."
  }
}
```

### Prettier only

```json
{
  "scripts": {
    "canonicalize": "tailwind-canonicalize . --write --safe",
    "canonicalize:check": "tailwind-canonicalize . --check",
    "format": "prettier --write .",
    "fix": "pnpm canonicalize && pnpm format",
    "check": "pnpm canonicalize:check && prettier --check ."
  }
}
```

Preserve existing `typecheck` / `test` — append to `check` only when the repo already chains them.

## Step 4 — Optional config file

Only create if the project has a clear Tailwind entry and the user wants migrations/tokens. Minimal:

```ts
// tailwind-canonicalize.config.ts
import { defineConfig } from "tailwind-canonicalize";

export default defineConfig({
  tailwind: {
    version: 4,
    stylesheet: "./src/styles/globals.css", // adjust to real CSS entry
  },
  canonicalize: {
    arbitraryValues: true,
    deprecatedClasses: true,
    duplicateClasses: true,
  },
  migrations: {
    gradients: true,
    tailwindV4: true,
  },
});
```

For v3 configs, point at `tailwind.config.*` per package docs. Do **not** invent theme keys.

## Step 5 — lint-staged / husky / lefthook

If the repo already has lint-staged (or husky), **prepend** canonicalize so format runs on already-canonical classes.

### Single ordered entry (preferred)

```json
{
  "*.{js,jsx,ts,tsx,mjs,cjs,vue,astro,svelte,html,mdx}": [
    "tailwind-canonicalize --write",
    "biome check --write --no-errors-on-unmatched"
  ]
}
```

Swap the second command:

- Ultracite: `ultracite fix` (or biome under ultracite)
- ESLint: `eslint --fix --max-warnings=0`
- Oxlint: `oxlint` (no rewrite)
- Prettier: `prettier --write`

### Husky

`.husky/pre-commit` should stay thin:

```sh
#!/usr/bin/env sh
pnpm exec lint-staged
```

### Cache / ignore

Ignore `.tailwind-canonicalize-cache.json` in Biome/ESLint/Oxlint ignore lists if present. See [references/integrations.md](references/integrations.md).

## Step 6 — CI (optional but recommended)

Add a **separate** step — never hide canonicalize inside the linter binary:

```yaml
- name: Tailwind canonicalize
  run: pnpm exec tailwind-canonicalize . --check --json --safe

- name: Lint
  run: pnpm lint   # or biome ci / ultracite check / eslint / oxlint
```

Exit codes: `0` clean, `1` changes required under `--check`, `2` hard error.

Large monorepos: `--workers --incremental` on full-tree checks.

## Step 7 — Verify (required before claiming success)

Run with the project PM. From install root:

```bash
# 1. Binary resolves
pnpm exec tailwind-canonicalize --version
pnpm exec tailwind-canonicalize --help

# 2. Semantic dry-run (expect 0 or 1, not 2)
pnpm exec tailwind-canonicalize . --check --safe --json
# or scoped:
pnpm exec tailwind-canonicalize src --check --safe

# 3. Favored linter still works
pnpm exec biome --version     # or ultracite / eslint / oxlint
pnpm lint                     # if script exists

# 4. Composed scripts
pnpm canonicalize:check       # if added
pnpm check                    # only if safe to run full gate
```

### Pass criteria

| Check | Pass |
|-------|------|
| `--version` | Prints semver, exit 0 |
| `--help` | Help text, exit 0 |
| `--check` | Exit **0** or **1** with summary/JSON — not install failures or exit **2** from bad flags |
| Favored linter | Still invokable; scripts call it after canonicalize |
| No dual semantic rewrite | ESLint tailwind arbitrary→scale rules disabled if present |

If `--check` wants many rewrites on a dirty tree, **do not** mass `--write` the whole monorepo unless the user asked. Report counts from `--json` and offer a scoped write or review mode:

```bash
pnpm exec tailwind-canonicalize . --review --safe --verbose
pnpm exec tailwind-canonicalize path/to/file.tsx --write --safe
```

### Red→green smoke (when applying a sample rewrite)

1. Pick one known arbitrary (e.g. a fixture or a single file with `w-[40px]` if theme has `w-10`)
2. `--check` on that path → exit 1 if rewrite pending
3. `--write --safe` → exit 0
4. `--check` again → exit 0

Never guess unsafe theme matches; default is `--safe`.

## Step 8 — Docs for humans and agents

Merge into `AGENTS.md` only when the file exists and is project-owned:

```markdown
## Tailwind classes

Semantic rewrites: tailwind-canonicalize (not Biome/ESLint).

pnpm canonicalize        # --write --safe
pnpm canonicalize:check  # CI gate

Compose: canonicalize first, then biome/eslint/oxlint/ultracite.
```

## Step 9 — Report to user

Summarize:

- Package manager + install location (root vs package)
- Detected lint favor + scripts added
- Hooks / CI changes (if any)
- Verification: version, check exit code, sample JSON counts
- Whether global install was done
- Next steps (scoped `--write`, config file, migrations) if full-tree write was deferred

Do **not** commit unless asked.

## Anti-patterns

- Replacing Biome/ESLint with canonicalize
- Two tools rewriting the same class strings (e.g. ESLint arbitrary→scale + canonicalize)
- Claiming setup complete when `tailwind-canonicalize` is only available via one-off `dlx` and not in package.json
- Running full-repo `--write --aggressive` on first setup without user consent
- Hiding `--check` inside `biome check` so failures are mis-attributed
- Regex codemods for theme equivalence outside this tool
- `git add -A` of unrelated dirty work while only wiring canonicalize
- Overwriting rich `AGENTS.md` with a generic stub

## Quick command cheat sheet

```bash
# install
pnpm add -D tailwind-canonicalize

# verify
pnpm exec tailwind-canonicalize --version
pnpm exec tailwind-canonicalize . --check --safe --json

# apply safe rewrites
pnpm exec tailwind-canonicalize . --write --safe

# then format/lint (example: Biome)
pnpm exec biome check --write .

# CI
pnpm exec tailwind-canonicalize . --check --json --safe
```

## References

- [references/integrations.md](references/integrations.md) — scripts, lint-staged, conflict matrix by stack
- [references/verify.md](references/verify.md) — verification checklist and exit codes
