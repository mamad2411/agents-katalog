---
name: follow-tool-github-actions
description: Set up GitHub Actions for complete CI/CD
argument-hint: "[scope]"
related:
  - follow-tool-lighthouse
  - follow-secret-manager
  - open-web-for-config-secret
  - follow-dot-github
  - follow-deploy
  - run-deploy
  - follow-tool-renovate
  - follow-tool-release-it
---

## Goal

Set up GitHub Actions for complete CI/CD with security, testing, deployment, monitoring

## Scope

Configure GitHub Actions for projects and repositories

- Boundary: GitHub Actions is a hosted platform (not an installable package) — companion tools are the `gh` CLI (`gh workflow`/`gh run`) and `actionlint` for local validation; secrets go through `/follow-secret-manager`
- Latest: `gh@2.101.0`, `actionlint@1.7.12`, `actions/checkout@v7` (v7.0.1), `actions/setup-node@v7`, `actions/cache@v6` (v6.1.0), `actions/upload-artifact@v7` (v7.0.1) (verified 2026-09-26)
- References: [cli](references/cli.md) | [apis](references/apis.md) 
## Execute

### 1. Pick Workflow

> Goal: dispatch specialized work to the appropriate workflow

| Topic | Workflow |-------|----------| workflow file structure, triggers, jobs, permissions | `workflows/setup-workflows/SKILL.md` | caching, matrix, concurrency groups, artifact reuse | `workflows/optimize-ci/SKILL.md` 
### 2. Select Workflows

> Goal: pick the fitting workflows

Select workflows by the project's needs:

- Base CI/CD: `ci.yml` (lint, typecheck, test) - every project must have
- Security: `codeql.yml`, `dependabot.yml`, `license-check.yml` - production projects needing security
- Testing: `coverage.yml`, `e2e.yml`, `mutation.yml`, `sonarqube.yml` - projects needing quality assurance
- Performance: `lighthouse.yml`, `bundle-size.yml`, `performance-budget.yml` - web applications needing performance
- Deployment: `deploy-staging.yml`, `deploy-production.yml`, `docker.yml`, `cloudflare-workers.yml`, `cloudflare-pages.yml` - projects needing automated deployment
- Monitoring: `slack-notify.yml`, `discord-notify.yml`, `artifacts.yml` - projects needing notifications
- Advanced: `matrix.yml`, `parallel.yml`, `cache.yml` - projects needing optimization
- Documentation: `deploy-docs.yml`, `changelog.yml`, `docusaurus.yml` - projects with documentation
- Git Ops: `commitlint.yml`, `dependency-review.yml`, `auto-merge.yml` - team projects needing governance

### 3. Basic Setup

> Goal: set up secrets, dependency updates, and the base CI workflow

1. Run `/follow-secret-manager` to set up CI/CD secrets with OIDC or machine identity
2. Run `/follow-tool-renovate` to set up dependency updates
3. Run `/follow-tool-release-it` to set up automated releases (if a monorepo)
4. Create `.github/workflows/ci.yml` for lint, typecheck, test

### 4. Add Workflows As Needed

> Goal: add workflows by need

- Security: add `codeql.yml`, `dependabot.yml` for production
- Testing: add `coverage.yml`, `e2e.yml` for quality assurance
- Performance: add `lighthouse.yml` for web applications
- Deployment: add workflows per platform in use (Docker, Cloudflare, Vercel)
- Monitoring: add `slack-notify.yml` for team notifications
- Git Ops: add `commitlint.yml`, `dependency-review.yml` for team collaboration

### 5. Write Workflows

> Goal: write workflow YAML per best practices

1. Run `/deep-analyze` to analyze structure and dependencies
2. Read the `.github/workflows/` directory and analyze existing workflows
3. Identify missing or duplicated workflows
4. Write workflow YAML using `actions/checkout@v7`, caching, and safe permissions
5. Separate CI and CD workflows
6. Use matrix strategy for multiple configurations
7. Set up monitoring and notifications for failures
8. Test syntax with `actionlint` (`mise use -g actionlint` then run `actionlint`) and verify permissions

## Rules

- Follow the project conventions and global rules (tool github actions)
- Use the allowed tools only when needed

- Use `/open-web-for-config-secret` when secrets must be created via the web
- Use `/follow-dot-github` for other `.github/` repo config
- Use `/follow-deploy` when deployment guidance is needed
- Use `/run-deploy` to trigger deployment

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Workflows fitted to the project are selected
- GitHub Actions fully configured per the requirements
- CI/CD runs automatically
