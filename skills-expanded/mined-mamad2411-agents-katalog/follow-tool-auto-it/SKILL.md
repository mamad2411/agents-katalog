---
name: follow-tool-auto-it
description: Set up Auto for automated releases with conventional commits
argument-hint: "[scope]"
related:
  - follow-secret-manager
  - follow-tool-release-it
  - follow-tool-changelogen
  - follow-tool-changesets
  - follow-tool-semantic-release
  - follow-tool-github-actions
  - open-web-for-config-secret
---

## Goal

Set up Auto for automated releases with conventional commits, semantic versioning, and automatic changelog generation

## Scope

Set up Auto for packages and workspaces that need automated releases

- Boundary: Auto computes the semver bump from PR labels (not commit messages directly) — for changelogs from conventional commits use `/follow-tool-changelogen`, for monorepo multi-package versioning use `/follow-tool-changesets`, for alternatives see `/follow-tool-release-it` and `/follow-tool-semantic-release`
- Latest: `auto@11.3.6` / `@auto-it/core@11.3.6` (verified 2026-09-13)
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### 1. Install Auto

> Goal: install the Auto CLI in the project

1. Run `bun add -D auto`
2. Verify the installation succeeded

### 2. Configure Auto

> Goal: set up the Auto config with the released plugin

1. Add config in `package.json`

```json
{
  "scripts": {
    "release": "auto shipit"
  },
  "author": "your-name <your-email>",
  "auto": {
    "plugins": [
      "released"
    ],
    "baseBranch": "main"
  }
}
```

2. Or create a `.autorc` file

```json
{
  "plugins": [
    "released"
  ],
  "baseBranch": "main",
  "author": "your-name <your-email>"
}
```

3. Released plugin options

```json
{
  "plugins": [
    [
      "released",
      {
        "label": ":shipit:",
        "prereleaseLabel": "🚧",
        "message": "%TYPE went out with version: %VERSION",
        "lockIssues": true,
        "includeBotPrs": false
      }
    ]
  ]
}
```

Important: `author` must be set in package.json or .autorc so Auto can commit

### 3. Setup GitHub Token

> Goal: set up the GitHub token for release automation

1. Use `/follow-secret-manager` to manage `GH_TOKEN`, or `/open-web-for-config-secret` to open the GitHub Personal Access Token creation page
2. Add it as `GH_TOKEN` in repository secrets
3. Or use `GITHUB_TOKEN` (when using GitHub Actions)

### 4. Setup NPM Token

> Goal: set up the NPM token for package publishing

1. Use `/follow-secret-manager` to manage `NPM_TOKEN`, or `/open-web-for-config-secret` to open the NPM token page at `https://www.npmjs.com/settings/~/tokens` (Automation token)
2. Add NPM_TOKEN to GitHub secrets with:
   ```bash
   gh secret set NPM_TOKEN
   ```
3. For scoped packages (@scope/package):
   - Check whether the scope exists on npm
   - If the scope is new: publish the first time locally with `bun publish --access public`
   - Verify NPM_TOKEN has publish rights for that scope

### 5. Create GitHub Workflow

> Goal: create the GitHub workflow for automated release
1. Create `.github/workflows/release.yml`

```yml
name: Release

on:
  push:
    branches:
      - main

permissions:
  contents: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0
      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - name: Release
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: bun run release
```

Important: `permissions` must be added so the workflow can push tags and create releases

### 6. Run Release

> Goal: run the release and verify the result
1. Run `bun run release` (local)
2. Or push to the main branch (CI/CD)
3. Auto detects commits and creates the release/tag automatically

## Rules

### 1. Installation

- Always use bun instead of npm
- The released plugin ships included with the auto CLI by default
- No need to install @auto-it/released separately

### 2. Configuration

- `author` is required in the config
- Specify the base branch (main/master)
- Use conventional commits (feat:, fix:, etc.)

### 3. Authentication

- Use `/follow-secret-manager` to manage `GH_TOKEN` or `NPM_TOKEN`
- Use `/open-web-for-config-secret` to open the token-creation URLs
- `GH_TOKEN` or `GITHUB_TOKEN` is required in CI
- `NPM_TOKEN` is required for npm publish

### 4. Released Plugin Options

- `label`: customize the label on merged PRs
- `prereleaseLabel`: label for prerelease branches
- `message`: custom message with %TYPE and %VERSION
- `lockIssues`: lock issues merged in PRs
- `includeBotPrs`: comment on PRs from bots

- Use /follow-tool-release-it if needed
- Use /follow-tool-github-actions if needed (tool auto it)

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Auto installed and working
- Config set correctly
- GitHub token ready
- Releases created automatically per conventional commits
- Released plugin comments on PRs and issues
