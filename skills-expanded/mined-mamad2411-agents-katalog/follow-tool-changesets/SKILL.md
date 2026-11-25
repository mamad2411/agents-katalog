---
name: follow-tool-changesets
description: Set up Changesets for monorepo versioning and changelog management
argument-hint: "[scope]"
related:
  - use-agent-browser
  - use-astgrep
  - follow-tool-aube
  - follow-tool-usage
  - follow-best-practice
  - setup-cicd
  - follow-tool-changelogen
  - follow-tool-auto-it
  - follow-tool-release-it
  - follow-tool-semantic-release
---

## Goal

Set up Changesets to manage versioning, changelogs, and package publishing in a monorepo systematically

## Scope

Set up Changesets for monorepos and workspaces

- Boundary: Changesets uses changeset files (`.changeset/*.md`) for multi-package versioning + a release PR flow — best for monorepos; for single-package changelogs from conventional commits use `/follow-tool-changelogen`; for PR-label releases see `/follow-tool-auto-it`; alternatives: `/follow-tool-release-it`, `/follow-tool-semantic-release`
- Latest: `@changesets/cli@3.0.3` (verified 2026-09-26) — `changesets/action@v2` (v2.1.2), `actions/checkout@v7`, `oven-sh/setup-bun@v2`
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### Workflows

| Topic | Workflow |-------|----------| Init, `.changeset/` flow, version/publish commands | `workflows/setup-changesets/SKILL.md` | `config.json`, `fixed`/`linked` packages, access | `workflows/config-changesets/SKILL.md` 
### 1. Install Changesets

> Goal: install the Changesets CLI and init config

1. Run `bun add -D @changesets/cli`
2. Run `bunx changeset init`

### 2. Configure Changesets

> Goal: tune `.changeset/config.json` appropriately

1. Edit `.changeset/config.json`
2. Set the base branch, access, and updateInternalDependencies
3. Configure the access token for publishing

```json [.changeset/config.json]
{
  "$schema": "https://unpkg.com/@changesets/config@4.0.1/schema.json",
  "changelog": "@changesets/cli/changelog",
  "commit": false,
  "fixed": [],
  "linked": [],
  "access": "restricted",
  "baseBranch": "main",
  "updateInternalDependencies": "patch",
  "ignore": []
}
```

### 3. Setup GitHub Actions

> Goal: create the GitHub Actions release workflow
1. Create `.github/workflows/release.yml`
2. Configure GITHUB_TOKEN and NPM_TOKEN
3. Set the version and publish commands

```yml [.github/workflows/release.yml]
name: Release

on:
  push:
    branches:
      - main

concurrency: ${{ github.workflow }}-${{ github.ref }}

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - name: Create Release Pull Request or Publish
        uses: changesets/action@v2
        with:
          version-script: bun changeset version
          publish-script: bun changeset publish
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### 4. Create Changesets

> Goal: create changeset files for changes
1. Run `bunx changeset` to create a changeset file
2. Select the packages and the changeset type (major, minor, patch)
3. Write the description for the changelog

### 5. Publish

> Goal: publish packages through Changesets
1. Merge the release PR created by GitHub Actions
2. Or run `bunx changeset publish` manually
3. Changesets versions and publishes the packages automatically

## Rules

### 1. Installation

- Use `bun add -D @changesets/cli` to install
- Run `bunx changeset init` to initialize

### 2. Configuration

- A base branch is required (default: main)
- Set access (restricted for scoped packages)
- Set updateInternalDependencies to patch

### 3. Authentication

- GITHUB_TOKEN is required for GitHub operations
- NPM_TOKEN is required for npm publishing

### 4. Workflow

- Use changesets/action@v2 for GitHub Actions — v2 must pair with Changesets CLI v3 (CLI v2 uses action@v1)
- Use the `version-script` and `publish-script` inputs (v2 renamed them from `version`/`publish`)
- Use concurrency to prevent conflicts

- Use /use-agent-browser if needed
- Use /use-astgrep if needed
- Use /follow-tool-aube if needed
- Use /follow-tool-usage if needed
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /follow-tool-changelogen if needed
- Use /follow-tool-auto-it if needed
- Use /follow-tool-release-it if needed
- Use /follow-tool-semantic-release if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Changesets installed and working
- Config set correctly
- GitHub Actions workflow ready to use
- Versioning and publishing fully automated

