---
name: follow-tool-renovate-setup-renovate
description: Install Renovate — GitHub App or self-hosted workflow — with a token
argument-hint: "[scope]"
related:
  - follow-secret-manager
  - follow-tool-github-actions
  - open-web-for-config-secret
---

## Goal

Install and enable Renovate on a repository — choose the hosted GitHub App or a self-hosted runner — with correct authentication

## Scope

Use for a repo without Renovate yet — install method, token, workflow trigger. `renovate.json` details are in `workflows/config-renovate/SKILL.md`

- If Renovate already runs (config + PRs from the renovate bot) → verify only

## Execute

### 1. Choose Install Method

> Goal: pick how to deploy Renovate

1. **Mend Renovate GitHub App** — install the app from GitHub Marketplace on the repo/org — no self-hosting, config via `renovate.json` only
2. **Self-hosted via GitHub Actions** — create `.github/workflows/renovate.yml` running `renovatebot/github-action` — fits when you need control of the schedule/runner (check the parent skill or official docs for versions)
3. Other self-hosted modes (docker, npm cli) — see official docs

### 2. Setup Token (Self-hosted)

> Goal: configure `RENOVATE_TOKEN`

1. Use `/follow-secret-manager` or `/open-web-for-config-secret` to create a GitHub PAT with `repo` scope (for private repos)
2. Set it as a repository secret: `gh secret set RENOVATE_TOKEN` or via the GitHub UI
3. Verify with `gh secret list`
4. Skip this step for the GitHub App method — the app authenticates itself

### 3. Create Workflow (Self-hosted)

> Goal: create the workflow that runs Renovate

1. Create `.github/workflows/renovate.yml` with `schedule` triggers (cron, e.g. `0 2 * * *`) + `workflow_dispatch`
2. Set permissions `contents: write`, `pull-requests: write`, `issues: write`
3. Use `renovatebot/github-action` with `RENOVATE_TOKEN` — when running multiple repos, specify `repositories` in config or env
4. Don't set `RENOVATE_AUTODISCOVER`/`RENOVATE_AUTODISCOVER_FILTER` once `repositories` is specified

### 4. Minimal Config

> Goal: create a minimal config so Renovate works

1. Create `.github/renovate.json` (or `renovate.json` at the root) with `$schema` and `extends: ["config:base"]`
2. Presets/packageRules/automerge details continue in `workflows/config-renovate/SKILL.md`

### 5. Verify

> Goal: confirm Renovate works

1. Validate the config: `bunx -- renovate-config-validator .github/renovate.json`
2. Self-hosted: trigger `workflow_dispatch` and watch the run logs — the repo scan must succeed
3. GitHub App: wait for the onboarding PR (`Configure Renovate`) — merge it to activate
4. If it fails from token/permissions → fix and rerun (max 3 rounds), then report

## Rules

### 1. Method Choice

- Prefer the GitHub App unless there's a reason to self-host — less maintenance
- Self-hosted must always have a schedule + `workflow_dispatch`

### 2. Token

- `RENOVATE_TOKEN` as a repository secret only, never committed
- PAT with `repo` scope for private repos

### 3. Common Pitfalls

- Forgetting `RENOVATE_TOKEN` → the workflow fails
- Forgetting permissions `contents/pull-requests/issues: write`
- Never use `--frozen-lockfile` in the install step — Renovate must be able to update the lockfile

- Use /follow-tool-github-actions if needed
- Use /follow-secret-manager if needed

## Expected Outcome

- Renovate active on the repo (app or self-hosted workflow)
- Token/permissions correct — the run doesn't fail
- Config passes `renovate-config-validator`
