---
name: bootstrap-ts-project
description: Bootstrap a new TypeScript project with pnpm, oxc (oxlint + oxfmt), prek git hooks, proper git setup, AGENTS.md, and CI. Use this skill whenever the user wants to create a new TypeScript project, scaffold a TS repo, set up a TypeScript monorepo, bootstrap a Node.js/TypeScript project, or asks for project setup with linting/formatting. Also trigger when the user mentions "new project", "init project", "scaffold", or "bootstrap" in a TypeScript/JavaScript context.
---

# Bootstrap TypeScript Project

This skill sets up a production-ready TypeScript project with modern tooling: pnpm, oxc (oxlint + oxfmt), prek pre-commit hooks, and GitHub Actions CI.

## Before you start

Read the reference docs in `references/` alongside this skill — they contain exact config formats, CLI commands, and options you'll need:

- `references/oxc.md` — oxlint + oxfmt installation, config, and CLI
- `references/prek.md` — prek installation, prek.toml format, local hooks
- `references/pnpm-catalogs.md` — catalog protocol for monorepos

## Workflow

Execute these steps in order. Each step after the initial commit gets its own git commit.

### Step 1: Ensure pnpm

Check if the project already has a `package.json`. If not, run `pnpm init`. Verify `pnpm-lock.yaml` exists or will be created.

If the project has a `pnpm-workspace.yaml`, it's a monorepo — you'll use catalogs (Step 5).

### Step 2: Git init + .gitignore + initial commit

If `.git/` doesn't exist, run `git init`.

Create/update `.gitignore` with a comprehensive TypeScript/.gitignore:

```
node_modules/
dist/
build/
.tsbuildinfo
*.tsbuildinfo
coverage/
.env
.env.local
.env.*.local
*.log
.DS_Store
Thumbs.db
```

Stage everything and commit:

```bash
git add -A
git commit -m "feat: initial commit"
```

### Step 3: Add oxc (oxlint + oxfmt)

Install the oxc toolchain:

```bash
pnpm add -D oxlint oxfmt
```

Add scripts to `package.json`:

```json
{
  "scripts": {
    "lint": "oxlint",
    "lint:fix": "oxlint --fix",
    "fmt": "oxfmt",
    "fmt:check": "oxfmt --check"
  }
}
```

Create `.oxlintrc.json`:

```json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "categories": {
    "correctness": "error",
    "suspicious": "warn"
  },
  "rules": {
    "eslint/no-unused-vars": "warn"
  }
}
```

Create `.oxfmtrc.json`:

```json
{
  "$schema": "./node_modules/oxfmt/configuration_schema.json",
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "singleQuote": false,
  "trailingComma": "all"
}
```

Run the formatter on all existing files to ensure a clean baseline:

```bash
pnpm fmt
```

Commit:

```bash
git add -A
git commit -m "feat: add oxc toolchain (oxlint + oxfmt)"
```

### Step 4: Add prek pre-commit hooks

Install prek:

```bash
pnpm add -D @j178/prek
```

Create `prek.toml` at the project root:

```toml
[[repos]]
repo = "local"

[[repos.hooks]]
id = "oxfmt"
name = "oxfmt"
language = "system"
entry = "npx oxfmt --write"
files = "\\.(js|jsx|ts|tsx|mjs|cjs|mts|cts|json|css|md|yaml|yml|html|vue|svelte)$"

[[repos.hooks]]
id = "oxlint"
name = "oxlint"
language = "system"
entry = "npx oxlint"
files = "\\.(js|jsx|ts|tsx|mjs|cjs|mts|cts|vue|svelte|astro)$"
```

Install the hooks:

```bash
npx prek install
```

Verify by running:

```bash
npx prek run --all-files
```

Commit:

```bash
git add -A
git commit -m "feat: add prek pre-commit hooks (oxlint + oxfmt)"
```

### Step 5: Monorepo catalogs (conditional)

**Only do this if** `pnpm-workspace.yaml` exists (the project is a monorepo).

Read `references/pnpm-catalogs.md` for the full pattern.

Add a `catalog` section to `pnpm-workspace.yaml` with the dev dependencies:

```yaml
catalog:
  oxlint: ^1.0.0
  oxfmt: ^0.10.0
  "@j178/prek": ^0.3.0
  # ... plus any other shared deps already in the workspace
```

Then update each package's `package.json` to use `catalog:` instead of hardcoded versions for those deps:

```json
{
  "devDependencies": {
    "oxlint": "catalog:",
    "oxfmt": "catalog:",
    "@j178/prek": "catalog:"
  }
}
```

Run `pnpm install` to reconcile.

Commit:

```bash
git add -A
git commit -m "feat: adopt pnpm catalogs for shared dependencies"
```

### Step 6: AGENTS.md via init skill

Run the `/init` skill (or equivalent) to generate a pre-populated `CLAUDE.md` for the project.

Then rename and symlink:

```bash
mv CLAUDE.md AGENTS.md
ln -s AGENTS.md CLAUDE.md
```

This way both `CLAUDE.md` and `AGENTS.md` point to the same file, and `AGENTS.md` is the canonical name.

Commit:

```bash
git add -A
git commit -m "feat: add AGENTS.md with project conventions"
```

### Step 7: GitHub Actions lint workflow

Create `.github/workflows/lint.yml`:

```yaml
name: Lint

on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - uses: pnpm/action-setup@v5

      - uses: actions/setup-node@v6
        with:
          node-version-file: .node-version
          cache: pnpm

      - run: pnpm install --frozen-lockfile

      - name: oxlint
        run: pnpm lint

      - name: oxfmt check
        run: pnpm fmt:check
```

If there's no `.node-version` file, either create one (e.g. `22`) or replace `node-version-file` with a hardcoded `node-version: 22`.

Commit:

```bash
git add -A
git commit -m "ci: add lint workflow for oxlint + oxfmt"
```

## Monorepo considerations

For monorepos, the lint workflow should lint all packages. If packages have their own `lint` scripts, use:

```yaml
- run: pnpm -r lint
- run: pnpm -r fmt:check
```

Or if the root package.json has the scripts, the default `pnpm lint` / `pnpm fmt:check` will work since oxlint and oxfmt both recurse into subdirectories by default.

## Checklist

Before finishing, verify:
- [ ] `pnpm install` succeeds
- [ ] `pnpm lint` runs without errors (or only expected warnings)
- [ ] `pnpm fmt:check` passes
- [ ] `npx prek run --all-files` passes
- [ ] `.github/workflows/lint.yml` exists
- [ ] `AGENTS.md` exists and `CLAUDE.md` is a symlink to it
- [ ] All steps have proper git commits
