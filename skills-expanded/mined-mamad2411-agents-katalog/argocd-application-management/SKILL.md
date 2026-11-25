# ArgoCD Application Management

## Purpose
Manages ArgoCD Application definitions and sync policies per environment.

## Role
DevOps Engineer

## Phase
Cross-phase (infrastructure)

## Triggered By
New service scaffolded; sync policy change needed.

## Inputs
- Service Helm chart

## Process
ArgoCD Application definitions per environment:
- SIT: auto-sync enabled (deploys automatically on image tag update)
- Staging: manual sync (Release Manager triggers)
- Production: manual sync (Edward's approval required)

Health check configuration per application. Sync policies: SIT=automated, others=manual. RBAC: developers can view, not sync production.

## Outputs
ArgoCD Application definitions with correct sync policy per environment.

## Quality Gates
- [ ] SIT auto-sync confirmed enabled
- [ ] Staging and Production sync set to manual
- [ ] Health checks configured per application
- [ ] RBAC restricts production sync to authorized approval flow

## References
- `.claude/skills/devops-engineer/story-merge-pipeline/SKILL.md`
- `.claude/skills/devops-engineer/staging-deployment/SKILL.md`
- `.claude/skills/devops-engineer/production-deployment/SKILL.md`
