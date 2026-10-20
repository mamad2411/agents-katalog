# Kubernetes Security Hardening

## Purpose
Maintains cluster-level security posture across network policy, pod security, and secret handling.

## Role
DevOps Engineer

## Phase
Cross-phase (infrastructure)

## Triggered By
Cluster bootstrap; quarterly review; new service onboarding.

## Inputs
- Cluster configuration

## Process
- Network policies: services only communicate with permitted peers.
- Default-deny: all ingress blocked except explicitly allowed.
- Pod security standards: no privileged containers where avoidable.
- Service accounts: minimal permissions (no cluster-admin for apps).
- Secret encryption at rest: Kubernetes etcd encryption configured.
- Read-only root filesystem: where possible (stateless services).
- Container resource limits: always set (prevents resource starvation).
- CIS Kubernetes benchmark: review quarterly.

## Outputs
Hardened cluster configuration; quarterly CIS review record.

## Quality Gates
- [ ] Default-deny network policy in place
- [ ] No privileged containers without justification
- [ ] Service accounts scoped minimally
- [ ] etcd encryption at rest confirmed
- [ ] Resource limits set on all containers
- [ ] CIS benchmark reviewed on schedule

## References
- `.claude/skills/devops-engineer/cluster-bootstrapping/SKILL.md`
- `.claude/skills/security-engineer/zap-full-scan/SKILL.md`
