---
name: follow-lib-tanstack-cli
description: Use the TanStack CLI — scaffold projects with add-ons (router, query, drizzle, auth)
argument-hint: "[template] [add-ons]"
related:
  - follow-lib-tanstack-ecosystem
  - run-dev
  - resolve-errors
---

## Goal

Use the TanStack CLI to scaffold a new project — an app starter with the chosen add-ons (Start/Router-based)

## Scope

Use when starting a new project that wants a complete default TanStack stack — not for adding a lib into an existing project (use the `setup-*` workflows instead)

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Scaffold

> Goal: scaffold a project with the add-ons the feature list needs

```bash
bunx @tanstack/cli create my-app
```

Key options (check the latest `--help`):

```bash
bunx @tanstack/cli create my-app --add-ons clerk,drizzle,tanstack-query
```

- Add-ons such as `tanstack-query`, `drizzle`, `clerk`, `tailwind`, `shadcn` — the current list is in `bunx @tanstack/cli create --help`
- Choose the package manager, framework (React/Solid), and toolchain per the prompts

### 2. Post-Scaffold

> Goal: the project actually runs

1. `cd my-app && bun install`
2. Set the env per the chosen add-ons (`.env` keys for clerk/drizzle etc.)
3. `/run-dev` — confirm the dev server starts
4. Check the generated structure — route tree, config files

### 3. Verify

> Goal: prove the scaffold builds and runs before finishing

1. Do `/run-typecheck` + a smoke test of the first page
2. On failure → `/resolve-errors` max 3 rounds

## Rules

- The CLI is a starting point — after scaffolding, keep customizing via the `setup-*` workflows
- Pick only the add-ons you really use — adding later is easier than removing
- Scaffold output may lag patch releases — check the versions in `package.json` after creation

## Expected Outcome

- A new project scaffolded successfully with the chosen add-ons
- The dev server runs with no errors
