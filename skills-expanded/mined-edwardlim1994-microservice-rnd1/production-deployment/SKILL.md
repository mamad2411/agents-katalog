# Production Deployment

## Purpose
Deploys the staging-verified image to Production and opens the post-deploy monitoring window.

## Role
DevOps Engineer

## Phase
Release

## Triggered By
Release Manager `production-release-trigger` (after Edward's approval).

## Inputs
- Exact image tag deployed to Staging

## Rule
SAME image tag as Staging — NEVER rebuild for production.

## Process
1. Get exact image tag that was deployed to Staging (from Harbor).
2. ArgoCD manual sync to Production cluster.
3. Wait for all pods healthy (rolling update).
4. Run smoke tests from `test/smoke/`.
5. Open 30-minute monitoring window.
6. Notify Release Manager: deployment complete or failed.

## Outputs
Production deployment completed with smoke test results; Release Manager notified.

## Quality Gates
- [ ] Same image tag as Staging used (no rebuild)
- [ ] Rolling update completed with all pods healthy
- [ ] Smoke tests run against production
- [ ] Release Manager notified of outcome

## References
- `.claude/skills/release-manager/production-release-trigger/SKILL.md`
- `.claude/skills/release-manager/post-release-monitoring/SKILL.md`
