---
name: follow-tool-biome
description: Set up and use Biome for linting and formatting instead of ESLint/Prettier
argument-hint: "[scope]"
related:
  - follow-create-plugins
  - use-agent-browser
  - use-astgrep
  - follow-tool-usage
  - follow-best-practice
  - setup-cicd
  - follow-tool-dprint
  - follow-tool-eslint
  - run-lint
  - run-format

---

## Goal

Install and configure Biome for linting and formatting with Bun

## Scope

Use `follow-tool-biome` for the specified tasks and workflows only

- Boundary: Biome combines linter + formatter + assist for JS/TS/JSON/CSS in one tool — a replacement for ESLint+Prettier; if the project must format many languages (markdown, toml, yaml, python, php) use `/follow-tool-dprint` alongside or instead; if ESLint is required see `/follow-tool-eslint`; the Ultracite preset on Biome — see official docs via `/learn-from-web`

- Latest: `@biomejs/biome@2.5.14` (verified 2026-09-26)
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### 1. Setup

> Goal: install the Biome CLI in the project

1. Install the Biome CLI with `bun add -D @biomejs/biome`
2. Confirm a `package.json` already exists

### 2. Configure

> Goal: create `biome.jsonc` with scripts in `package.json`

1. Create `biome.jsonc` at the root with VCS integration and recommended rules

```json [biome.jsonc]
{
	"$schema": "./node_modules/@biomejs/biome/configuration_schema.json",
	"vcs": {
		"enabled": true,
		"clientKind": "git",
		"useIgnoreFile": true
	},
	"linter": {
		"enabled": true,
		"rules": {
			"correctness": {
				"noNodejsModules": "off"
			},
			"performance": {
				"noBarrelFile": "warn"
			}
		}
	},
	"formatter": {
		"enabled": true
	},
	"assist": {
		"enabled": true
	}
}
```

2. Add `lint`, `lint:fix`, and `format` scripts to `package.json`

```json [package.json]
{
    "scripts": {
       "lint" : "biome lint",
       "lint:fix" : "biome lint --write",
       "format" : "biome format --write"
    }
}
```

### 3. Monorepo

> Goal: set up Biome for monorepo workspaces
1. In each workspace create `biome.jsonc` with `root: false` and `extends: ["../../biome.jsonc"]`

```json [biome.jsonc]
{
	"root": false,
	"extends": ["../../biome.jsonc"]
}
```

### 4. Optional Domains

> Goal: add linter domains per tech stack
1. Pick the domains relevant to the project — see the list and each domain's triggering dependency at https://biomejs.dev/linter/domains/ (a domain activates automatically when its related dep is declared in `package.json`, e.g. `solid` when `solid-js` is present)
2. Add the domains in `biome.jsonc` under `linter.domains`
3. Validate the config with `bunx biome lint` — a key/rule placed in the wrong group raises a `deserialize` error listing known keys

```json [biome.jsonc]
{
	"linter": {
		"domains": {
			"drizzle": "recommended",
			"project": "recommended",
			"types": "recommended",
			"turborepo": "recommended",
			"vue": "recommended",
			"vitest": "recommended"
		}
	}
}
```

### 5. Verify

> Goal: confirm lint and format work
1. Run `bun run lint`
2. Run `bun run format`

### 6. GitHub Actions CI

> Goal: create a GitHub Actions workflow for Biome CI
1. Create `.github/workflows/biome.yml` for CI/CD

```yaml [.github/workflows/biome.yml]
name: Code quality

on:
  push:
  pull_request:

jobs:
  quality:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@v7
        with:
          persist-credentials: false
      - name: Setup Biome
        uses: biomejs/setup-biome@v2
        with:
          version: latest
      - name: Run Biome
        run: biome ci .
```

### Workflows

> Goal: dispatch specialized work to the right workflow

| Topic | Workflow |-------|----------| first-time setup (install, biome.json, editor, CLI) | `workflows/setup-biome/SKILL.md` | migrate from ESLint/Prettier | `workflows/migrate-from-eslint-prettier/SKILL.md` 
## Rules

### 1. Installation

- Use `bun add -D @biomejs/biome` only
- A `package.json` must already exist

### 2. Configuration

- Use `biome.jsonc` (with comments), not `.json`
- Enable VCS integration with git
- Root config uses `root: true`
- Workspace configs use `root: false` + `extends: "//"`

### 3. Scripts

- Must have a `lint` script: `biome lint` (check only)
- Must have a `lint:fix` script: `biome lint --write` (fix issues)
- Must have a `format` script: `biome format --write`

### 4. Optional Domains

- Domains use `recommended` only, never `all`
- Astro: for Astro projects
- Drizzle: for projects using Drizzle ORM
- Next: for Next.js projects
- Playwright: for Playwright test projects
- Project: for project-level analysis (affects performance)
- Qwik: for Qwik projects
- React: for React projects (conflicts with Solid)
- ReactNative: for React Native projects
- Solid: for Solid projects (conflicts with React)
- Svelte: for Svelte projects
- Tailwind: for Tailwind CSS projects
- Test: for test files
- Turborepo: for Turborepo projects
- Types: for type analysis (affects performance — scans the whole project + inference engine)
- Vue: for Vue projects
- Never use Tailwind with a project on a UnoCSS/Tailwind-free stack
- Example stack: Solid SPA/Start → `solid` + `project` + `types`
- A rule must sit under the group matching its diagnostic category (e.g. `useOptionalChain` → `complexity`, `noDescendingSpecificity` → `style`) — nursery rules go under the `nursery` group; check the group with `bunx biome explain <rule>`

- Use /follow-create-plugins (biome) if needed
- Use /use-agent-browser if needed
- Use /use-astgrep if needed
- Use /follow-tool-usage if needed
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /follow-tool-dprint if needed
- Use /follow-tool-eslint if needed
- Use /run-lint if needed
- Use /run-format if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Biome installed and working
- `lint`, `lint:fix`, and `format` scripts ready to use
- Config supports git ignore
- Monorepo workspaces extend the root config correctly

