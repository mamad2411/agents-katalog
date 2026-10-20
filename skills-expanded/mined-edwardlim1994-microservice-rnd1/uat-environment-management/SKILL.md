# UAT Environment Management

## Purpose
Creates and tears down per-story UAT environments automatically based on kanban label state.

## Role
DevOps Engineer

## Phase
UAT

## Triggered By
PM adds `uat-ready` label to story PR; PM removes it.

## Inputs
- Story PR with `uat-ready` label

## Process
ArgoCD ApplicationSet with PullRequest generator configuration.

Trigger: PM adds `uat-ready` label to story PR.
- Creates namespace: `uat-{branch-slug}`
- Traefik IngressRoute: `uat-{KAN-N}.uat.internal`
- Resource limits per UAT namespace (lean — not production-sized): CPU: 500m per pod, Memory: 512Mi per pod

Auto-teardown: PM removes `uat-ready` label → ArgoCD tears down. PVC cleanup: automated after namespace teardown (critical — PVCs persist otherwise).

Monitors: UAT cluster resource usage, alerts at 80% capacity.

## Outputs
Per-story UAT namespace, auto-torn-down on label removal.

## Quality Gates
- [ ] Namespace and IngressRoute created on uat-ready label
- [ ] Resource limits applied (lean, not production-sized)
- [ ] Auto-teardown confirmed on label removal
- [ ] PVC cleanup automated after teardown
- [ ] 80% capacity alert configured

## References
- `.claude/skills/qa-engineer/uat-deployment-verification/SKILL.md`
- `.claude/skills/devops-engineer/resource-monitoring/SKILL.md`
