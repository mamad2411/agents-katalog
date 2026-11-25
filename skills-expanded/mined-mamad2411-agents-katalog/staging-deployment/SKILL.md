# Staging Deployment

## Purpose
Deploys the release candidate image to the Staging cluster and runs smoke tests.

## Role
DevOps Engineer

## Phase
Release

## Triggered By
Release Manager `staging-release-trigger` skill.

## Inputs
- Release candidate image tag in Harbor

## Process
1. Get release image tag from Harbor.
2. ArgoCD manual sync to Staging cluster.
3. Configure Traefik: `staging.{domain}`.
4. Wait for all pods healthy.
5. Run smoke tests from `test/smoke/`.
6. If smoke tests pass: notify Release Manager + QA + Security.
7. If smoke tests fail: notify Release Manager, block QA testing.

## Outputs
Staging deployment with smoke test results; notifications sent.

## Quality Gates
- [ ] Correct RC image tag deployed
- [ ] All pods confirmed healthy before smoke tests
- [ ] Smoke test results gate QA/Security notification
- [ ] Failures block QA testing and notify Release Manager

## References
- `.claude/skills/release-manager/staging-release-trigger/SKILL.md`
- `.claude/skills/devops-engineer/argocd-application-management/SKILL.md`
