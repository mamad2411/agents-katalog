---
name: follow-tool-pkg-new
description: Set up pkg.pr.new for continuous preview releases
argument-hint: "[scope]"
related:
  - follow-tool-github-actions
  - follow-tool-release-it
  - follow-tool-semantic-release
  - follow-tool-renovate
  - follow-tool-node-modules-inspector
---

## Goal

Set up pkg.pr.new for continuous (preview) releases of libraries by auto-publishing every commit and pull request

## Scope

For GitHub libraries that want preview packages for every commit and pull request

- Use this skill for ephemeral preview releases only — for real releases use `/follow-tool-release-it` or `/follow-tool-semantic-release`
- Requires GitHub Actions — if there's no workflow yet, do `/follow-tool-github-actions` first

- Latest: `pkg-pr-new@0.0.88` (verified 2026-09-13)

## Execute

### 1. Install GitHub Application

> Goal: install the GitHub Application on the repository

1. Go to `https://github.com/apps/pkg-pr-new`
2. Install the application on the repository
3. Verify the required permissions
4. See details in 

### 2. Install Package

> Goal: install the pkg-pr-new package in the project

1. Run `bun add -D pkg-pr-new`
2. In CI, run from the lockfile (`bun run pkg-pr-new publish` or `pnpm exec pkg-pr-new publish`) instead of `bunx`/`npx`
3. See details in 

### 3. Configure Workflow

> Goal: create the GitHub Actions workflow for publishing

1. Create `.github/workflows/publish.yml`
2. Trigger on `push` and `pull_request`
3. Run `bun install`, `bun run build`, then `bunx pkg-pr-new publish`
4. For monorepos, specify package paths such as `'./packages/*'`
5. See details in 

### 4. Configure Options

> Goal: set options for templates, CLI, and comments

1. Use `--template './examples/*'` for StackBlitz templates
2. Use `--bin` for CLI applications
3. Use `--comment=update` for custom comments
4. Use `--packageManager=bun` for the package manager in comments
5. Use `--commentWithSha` when commit SHA URLs are wanted in comments instead of PR number URLs
6. See details in 

### 5. Verify Preview Publish

> Goal: confirm preview packages publish successfully

1. Open a pull request and check the bot comment appears with install commands
2. Test the install with an npm-compatible URL: `bun add https://pkg.pr.new/<owner>/<repo>/<package>@<commit>`
3. Use the `sha`, `urls`, `packages` step outputs from `pkg-pr-new publish` to chain E2E jobs (`needs.<job>.outputs.urls`)
4. If no publish happens → check the GitHub Application is installed on the repo and the workflow has correct permissions
5. See details in 

## Rules

### 1. Installation

- The GitHub Application must be installed before use
- Always use `bun` instead of `npm`
- Run the command only once per workflow

### 2. Configuration

- Specify package paths for monorepos
- Use patterns like `./packages/*` instead of running multiple times
- Set permissions in the workflow

### 3. Options

- `--template`: creates Stackblitz instances for examples
- `--bin`: shows `bunx` instead of `npm i` in comments
- `--comment`: `update`, `create`, or `off`
- `--packageManager`: `npm`, `pnpm`, `yarn`, or `bun`
- `--only-templates`: shows only templates in comments
- `--previewVersion`: rewrites the version to `0.0.0-preview-<sha>` before packing, avoiding lockfile collisions
- `--pnpm` / `--yarn` / `--bun`: use `pnpm pack`/`yarn pack`/`bun pm pack` instead of `npm pack` (required with pnpm catalogs)
- `--json <file>`: writes publish metadata to JSON for custom comments

### 4. Best Practices

- Publish approved pull requests only, for security
- Use the outputs for E2E tests
- Avoid publishing on tags

- Use /follow-tool-github-actions if needed (tool pkg new)
- Use /follow-tool-release-it if needed
- Use /follow-tool-semantic-release if needed (tool pkg new)
- Use /follow-tool-renovate if needed
- Use /follow-tool-node-modules-inspector if needed

## References

- [CLI reference](references/cli.md)


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- pkg.pr.new installed and working
- GitHub Application installed successfully
- Workflow configured correctly
- Preview packages published automatically
- Comments appear on pull requests

