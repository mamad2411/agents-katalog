---
name: follow-tool-changesets-setup-changesets
description: Install Changesets, init `.changeset/`, and set up the version/publish flow first time
argument-hint: "[scope]"
related:
  - setup-cicd
  - run-release
  - follow-secret-manager
---

## Goal

Install `@changesets/cli`, init the `.changeset/` directory, and set up the changeset → version → publish workflow until it is ready to use — first-time setup

## Scope

Use for monorepos/workspaces that want to start using Changesets — install, init, changeset flow, release workflow. Config key details live in `workflows/config-changesets/SKILL.md`

- If `.changeset/` already exists → verify only

## Execute

### 1. Check Prerequisites

> Goal: check state before setup

1. Check whether the `.changeset/` directory and `@changesets/cli` in devDependencies already exist — if present → skip to verify
2. Check whether the project is a monorepo (workspaces in the root `package.json`) or a single package — Changesets supports both
3. Identify the package manager from the lockfile

### 2. Install And Init

> Goal: install the CLI and init config

1. Run `bun add -D @changesets/cli` (or the project's package manager)
2. Run `bunx changeset init` — creates `.changeset/` with `config.json` and `README.md`
3. Confirm with `bunx changeset --version`

### 3. Changeset Flow

> Goal: set up the changeset creation flow

1. Run `bunx changeset` to create a changeset file — pick packages, bump type (`major`/`minor`/`patch`), and write the description for the changelog
2. Commit the changeset files (`.changeset/*.md`) into the repo alongside the code changes
3. Confirm contributors understand the flow — document it in CONTRIBUTING/README if needed

### 4. Version And Publish Commands

> Goal: set up release scripts

1. Add scripts to the root `package.json`: `"version-packages": "changeset version"`, `"release": "changeset publish"`
2. `changeset version` — consumes changesets → bumps versions + updates CHANGELOGs + deletes the changeset files
3. `changeset publish` — publishes packages to the registry per the new versions
4. Set up the GitHub Actions release workflow with `changesets/action` — use the action version pinned by the parent skill, paired with the correct CLI major version
5. Use `/follow-secret-manager` to set `GITHUB_TOKEN` and `NPM_TOKEN` as secrets — never hard-code

### 5. Verify

> Goal: confirm the flow works

1. Create a test changeset → run `bunx changeset status` to check pending changesets
2. Run `bunx changeset version` on a test branch to see the version bumps (revert after checking)
3. If verification fails → run `/resolve-errors` for max 3 rounds, then stop and report

## Rules

### 1. Idempotent

- If `.changeset/` already exists → verify only, never re-run `init`

### 2. Flow Discipline

- Every PR that changes a published package must carry a changeset file
- `version` → review the generated CHANGELOGs before committing; run `publish` in CI only after merge

### 3. Secrets

- `NPM_TOKEN`/`GITHUB_TOKEN` via secrets only

- Use /setup-cicd if needed
- Use /follow-secret-manager if needed

## Expected Outcome

- `@changesets/cli` installed and `.changeset/` initialized
- Changeset → version → publish flow ready to use
- Release workflow secrets configured correctly
