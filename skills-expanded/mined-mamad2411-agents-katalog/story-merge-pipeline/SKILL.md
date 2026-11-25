# Story Merge Pipeline

## Purpose
Builds, tags, scans, and auto-deploys images to SIT when task/feat branches merge.

## Role
DevOps Engineer

## Phase
Development

## Triggered By
`task/` PR merged to `feat/`, `feat/` merged to `us/`.

## Inputs
- Merged branch commit

## Process
1. Secrets scan (GitLeaks/TruffleHog).
2. Build Docker image.
3. Tag: `{service}-{branch-slug}-{short-commit-hash}`.
4. Push to Harbor registry.
5. Harbor Trivy scan auto-runs on push.
6. ArgoCD image updater detects new tag → auto-deploys to SIT.
7. Kanban card description updated with image tag.

Fully automated. SIT: Option A (latest per service, no manual control).

## Outputs
Built, scanned, deployed SIT image; kanban card updated.

## Quality Gates
- [ ] Secrets scan passes before build
- [ ] Image tagged per convention
- [ ] Trivy scan runs automatically on push
- [ ] Kanban card description reflects deployed image tag

## References
- `.claude/skills/devops-engineer/harbor-registry-management/SKILL.md`
- `.claude/skills/devops-engineer/argocd-application-management/SKILL.md`
