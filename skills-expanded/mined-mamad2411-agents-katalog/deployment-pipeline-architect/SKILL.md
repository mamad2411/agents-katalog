---
name: "Deployment Pipeline Architect"
version: "1.0.0"
description: "Designs CI/CD pipelines with build, test, and deploy stages. Supports GitHub Actions, GitLab CI with environment promotion and rollback."
author: "workspace"
activated: false
---

# Deployment Pipeline Architect

Designs CI/CD pipelines with build, test, and deploy stages. Supports GitHub Actions, GitLab CI with environment promotion and rollback.

## Decision Framework

### When to Apply
Use when: Setting up CI/CD, automating deployments, managing environments, implementing rollback strategies

### When NOT to Apply
Don't use when: Manual deployment is intentional requirement, single-developer prototype

## Anti-Patterns

### 1. Deploying Directly to Production
Always use staging/preview environments first.

### 2. Secrets in Code
```yaml
# BAD
env:
  API_KEY: "sk-abc123"

# GOOD
env:
  API_KEY: ${{ secrets.API_KEY }}
```

### 3. No Rollback Strategy
Always have a way to revert to previous version within minutes.


## Trigger Phrases

- "Setup CI/CD"
- "Deployment pipeline"
- "GitHub Actions"
- "Automated deploy"
- "Rollback strategy"

## Patterns

### GitHub Actions Pipeline
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
  deploy-staging:
    needs: test
    environment: staging
    steps:
      - run: deploy-to-staging.sh
  deploy-production:
    needs: deploy-staging
    environment: production
    steps:
      - run: deploy-to-production.sh
```

### Rollback Script
```bash
#!/bin/bash
PREVIOUS_VERSION=$(git describe --tags --abbrev=0 HEAD^)
kubectl set image deployment/app app=$REGISTRY/app:$PREVIOUS_VERSION
kubectl rollout status deployment/app
```


## Escalation Chain

1. **Retry** - Retry failed step
2. **Rollback** - Revert to previous version
3. **Notify** - Alert team via notification channel
4. **Block** - Prevent further deployments
5. **Manual** - Human intervention required

## Error Classification

| Error Type | Severity | Recovery |
|-----------|----------|----------|
| Test failure | Error | Block deploy |
| Deploy timeout | Critical | Auto-rollback |
| Health check fail | Critical | Auto-rollback |
| Config error | Warning | Fix + retry |

## Integration
- Works with: feature-flag-system, performance-budget-enforcer, error-recovery-orchestrator

