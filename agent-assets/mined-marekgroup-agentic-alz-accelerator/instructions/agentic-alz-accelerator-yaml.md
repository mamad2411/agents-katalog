---
applyTo: "**/*.{yml,yaml}"
---

# YAML Conventions

## GitHub Actions

- Use `actions/checkout@v4`, `actions/upload-artifact@v4`, `actions/download-artifact@v4`
- Pin action versions to major tags, not `@main`
- Use OIDC for Azure auth (`azure/login@v2` with federated credentials)
- Never commit secrets — use GitHub Secrets or OIDC

## Agent Config

- Agent YAML config lives in `src/config/agent_config.yaml`
- Landing zone profiles in `src/config/landing_zone_profiles.yaml`
- Environment-specific overrides in `src/config/profiles/`

## Pipeline Structure

```
pipelines/
  github-actions/   # GitHub Actions workflows
  azure-devops/     # Azure DevOps pipelines
```
