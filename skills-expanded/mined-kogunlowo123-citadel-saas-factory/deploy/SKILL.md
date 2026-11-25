---
name: deploy
description: Deploy application to staging or production. Triggered by deploy, ship it, or push to staging.
allowed-tools: [Bash, Read]
---

# Deploy Skill

## When to Invoke
- Keywords: deploy, ship it, push to staging, push to production
- After successful CI pipeline

## Deployment Steps
1. **Pre-checks** — Tests pass, security scan clean, images built
2. **Build** — Docker images tagged with git SHA
3. **Push** — Images pushed to GHCR
4. **Update GitOps** — Patch overlay kustomization with new image tag
5. **Sync** — ArgoCD auto-syncs from git
6. **Verify** — Health checks, smoke tests
7. **Rollback** — If health checks fail, revert overlay patch

## Environments
- **staging**: `gitops/overlays/staging/`
- **production**: `gitops/overlays/production/` (requires approval)
