---
name: follow-tool-github-actions-setup-workflows
description: Create workflow files in `.github/workflows/` — structure, triggers, jobs, permissions
argument-hint: "[scope]"
related:
  - follow-secret-manager
  - follow-dot-github
  - run-verify
---

## Goal

Create correct workflow YAML files in `.github/workflows/` — file structure, triggers, jobs, steps, permissions per best practices

## Scope

Use when adding new workflows or changing workflow structure — caching/matrix/performance tuning lives in `workflows/optimize-ci/SKILL.md`

## Execute

### 1. Inventory Existing Workflows

> Goal: know which workflows already exist

1. Read everything in `.github/workflows/` — identify existing workflows, triggers, and gaps
2. Check whether the CI base (`ci.yml` — lint, typecheck, test) exists yet — every project needs it
3. Run `/follow-dot-github` if the whole `.github/` directory needs auditing

### 2. Choose Workflows

> Goal: pick workflows based on needs

- Base CI/CD: `ci.yml` (lint, typecheck, test) — every project
- Security: `codeql.yml`, `dependabot.yml` — production
- Testing: `coverage.yml`, `e2e.yml` — quality assurance
- Deployment: workflows per the platform actually used
- Monitoring: notify workflows — team notifications

### 3. Write Workflow Files

> Goal: write workflow YAML per best practices

1. Define clear `name` and `on` triggers — `push`/`pull_request` on the right branches, `workflow_dispatch` for manual runs
2. Set least-privilege `permissions` — `contents: read` as default, add only what's needed
3. Use `actions/checkout` and setup actions pinned by the parent skill — check the latest version stated in the parent `SKILL.md` or official docs, never guess
4. Use a `concurrency` group to cancel in-progress runs on the same ref
5. Separate CI and CD workflows — never run deploy on a pull request
6. Organize jobs: set `runs-on`, `steps`, `needs` for job dependencies, and clear `if` conditions

### 4. Secrets And Tokens

> Goal: configure secrets safely

1. Run `/follow-secret-manager` for secrets the workflows need (`NPM_TOKEN`, deploy keys)
2. Reference secrets only through `${{ secrets.* }}` — never hard-code
3. Prefer OIDC/trusted publishing over long-lived tokens when the provider supports it

### 5. Validate

> Goal: check syntax and permissions before committing

1. Run `actionlint` against every workflow file (`mise use -g actionlint` if missing)
2. Verify triggers — a push to an unintended branch should not trigger
3. If syntax fails → fix, then re-lint until it passes

## Rules

### 1. Structure

- One workflow per file with a descriptive name (`ci.yml`, `release.yml`)
- Always least-privilege `permissions`
- Pin action versions per the parent skill or official docs — no `master`/`latest` floating refs

### 2. Triggers

- CI triggers on `push`/`pull_request` for main branches
- deploy/release triggers only on `push` to the release branch or tags — never run on PRs

### 3. Secrets

- Secrets go through `${{ secrets.* }}` and `/follow-secret-manager` only

- Use /follow-secret-manager if needed
- Use /follow-dot-github if needed

## Expected Outcome

- Workflow files in `.github/workflows/` pass `actionlint`
- Triggers and permissions follow least-privilege
- CI base covers lint, typecheck, test
