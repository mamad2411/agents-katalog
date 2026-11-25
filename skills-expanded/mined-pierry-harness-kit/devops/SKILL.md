---
name: devops
description: DevOps engineering conventions for team. CI/CD, infra-as-code, observability. Project conventions in .claude/conventions/devops.md override these defaults.
user_invocable: false
---

DevOps conventions, team default.

Project override: if `{repo}/.claude/conventions/devops.md` exists, overrides any rule here. See guides/conventions-override.md.

## Defaults

CI/CD:
- GitHub Actions for most repos. Workflows in `.github/workflows/`.
- Reusable workflows when steps repeat across repos.
- Secrets via GitHub Secrets, never inline.
- Pin actions to commit SHA, not branch.

Containers:
- Multi-stage Dockerfile. Slim base images (alpine, distroless).
- Non-root user in production stage.
- `.dockerignore` mirrors `.gitignore` essentials plus build artifacts.

Infra-as-code:
- Terraform for infra. State in remote backend (S3, etc).
- Modules in `terraform/modules/`. Stacks in `terraform/stacks/`.
- Variables via `terraform.tfvars`, never hardcoded.

Observability:
- Grafana dashboards JSON in repo when applicable.
- Alerts as code (Prometheus rules, Datadog monitors).
- Log structure: JSON, with `trace_id`, `service`, `level`, `msg`.

Secrets:
- Never commit secrets. Use secret manager.
- Pre-commit hook to scan for accidental secrets.

## Before writing code

Read at least 3 similar workflows or terraform modules in repo. Confirm:
- runner type (ubuntu-latest, self-hosted)
- secret naming convention
- environments (dev, staging, prod)
- approval gates for prod

## Forbidden in PR

- inline secrets
- actions pinned to `@main` or `@latest`
- terraform without state backend
- Dockerfile running as root in prod
- alerts without runbook links

## Mark gaps

```yaml
# TBD - verify with devops lead: {what is missing}
```
