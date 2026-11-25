---
name: follow-tool-renovate
description: Set up Renovate for auto dependency updates via GitHub Actions
argument-hint: "[scope]"
related:
  - follow-secret-manager
  - open-web-for-config-secret
  - follow-tool-github-actions
  - follow-tool-pkg-new
  - follow-tool-release-it
  - follow-tool-semantic-release
  - run-install
---


## Goal

Set up Renovate to update dependencies automatically via GitHub Actions

## Scope

Use for GitHub repositories that want dependency updates, schedule, automerge, and PR management

- Renovate only creates dependency update PRs — no version bump or publish; for releases use `follow-tool-release-it` or `follow-tool-semantic-release`
- If you already use the Mend-hosted Renovate GitHub App, no self-hosted workflow is needed — this skill covers self-hosted via `renovatebot/github-action`

- Latest: `renovate@44.115.10` (npm; requires Node.js `^24.11.0`) / `renovatebot/github-action@v46.3.4` (verified 2026-09-26)

## Execute

### Workflows

| Topic | Workflow |-------|----------| GitHub App / self-hosted install, `RENOVATE_TOKEN`, workflow | `workflows/setup-renovate/SKILL.md` | `renovate.json` presets, `packageRules`, automerge | `workflows/config-renovate/SKILL.md` 
### 1. Configure Renovate

> Goal: create the renovate config in the project

1. Create `.github/renovate.json`
2. Use `"$schema": "https://docs.renovatebot.com/renovate-schema.json"`
3. Set `extends` to `["config:base"]`
4. Set `schedule`, e.g. `["every day"]`
5. Set `automerge: true` for `dependencies` and `devDependencies` via `packageRules`
6. Set `docker: false` and `"platform": "github"` when self-hosted
7. See details in 

### 2. Create Workflow

> Goal: create the GitHub Actions workflow to run Renovate

1. Create `.github/workflows/renovate.yml`
2. Set the `cron` to run at `0 2 * * *`
3. Add `workflow_dispatch` for a manual trigger
4. Grant permissions `contents: write`, `pull-requests: write`, `issues: write`
5. Use `renovatebot/github-action@v46` (latest `v46.3.4`) or pin the full version
6. See details in 

### 3. Setup Token

> Goal: configure `RENOVATE_TOKEN` for authentication

1. Use `/follow-secret-manager` to manage `RENOVATE_TOKEN`, or `/open-web-for-config-secret` to open the GitHub PAT creation page with `repo` scope
2. Set the secret in the repository yourself, or use `gh secret set RENOVATE_TOKEN -b "token"`
3. Verify the secret with `gh secret list` or the secret manager dashboard
4. See details in 

### 4. Validate Config

> Goal: verify the renovate config is correct

1. Run `bunx -- renovate-config-validator .github/renovate.json`
2. Check `extends` — the presets must actually exist
3. Check the `packageRules` matchers are correct
4. See details in 

### 5. Monitor Pull Requests

> Goal: follow the PRs Renovate creates

1. Check the PRs created per the schedule
2. Verify `automerge` — whether it merges or needs review
3. Adjust `packageRules` for deps you don't want auto-updated
4. See details in 

## Rules

### 1. Config

- Use `config:base` as the base config
- Set `docker: false` to disable Docker updates
- Use `"platform": "github"` for GitHub repositories
- Specify `repositories: ["owner/repo"]` when self-hosted
- Use an explicit `schedule`

### 2. Workflow

- Use `cron: "0 2 * * *"` to run daily
- Set permissions `contents`, `pull-requests`, `issues` to `write`
- Use `bun install --ignore-scripts` or the project's package manager
- Don't set `RENOVATE_AUTODISCOVER` or `RENOVATE_AUTODISCOVER_FILTER` when `repositories` is specified

### 3. Token

- Use a PAT with `repo` scope for private repos
- Set `RENOVATE_TOKEN` as a repository secret
- Use `/follow-secret-manager` to manage `RENOVATE_TOKEN`, or `/open-web-for-config-secret` to open the token-creation page
- Use `gh secret set` or the GitHub UI to configure

### 4. Common Mistakes

- Missing `RENOVATE_TOKEN` makes the workflow fail
- Using `config:recommended` can trigger unwanted Node.js version checks
- Forgetting permissions in the workflow
- Using `--frozen-lockfile` prevents Renovate from updating the lockfile

- Use /follow-tool-github-actions if needed (tool renovate)
- Use /follow-tool-pkg-new if needed
- Use /follow-tool-release-it if needed
- Use /follow-tool-semantic-release if needed (tool renovate)

## References

- [CLI reference](references/cli.md)

- Use /run-install if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Renovate runs daily or on manual trigger
- Dependencies update automatically and automerge per rules
- PRs are created for dependency updates
- Lock files are updated automatically
- The workflow doesn't fail from token or permissions issues
