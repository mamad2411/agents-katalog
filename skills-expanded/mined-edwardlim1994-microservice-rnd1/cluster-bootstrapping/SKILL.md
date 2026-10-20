# Cluster Bootstrapping

## Purpose
Defines the ordered, non-parallelisable sequence for bootstrapping a brand new cluster.

## Role
DevOps Engineer

## Phase
Cross-phase (infrastructure)

## Triggered By
New cluster needed.

## Inputs
- Terraform configuration
- Repo credentials for ArgoCD
- Harbor pull secret

## Process
Ordered sequence for NEW cluster — never skip or parallelise steps:
1. Terraform provisions nodes + networking.
2. cert-manager installed (needs to exist before Traefik).
3. CA distribution configured (for internal TLS).
4. Traefik installed (needs certs from cert-manager).
5. Vault installed → `vault-provisioning` skill runs.
6. ArgoCD installed → configured with repo credentials.
7. Harbor credentials configured as pull secret in cluster.
8. Observability stack deployed (OTEL + Alloy + Loki + Tempo + Prometheus + Grafana).
9. Apicurio Registry deployed.
10. Application services deployed via ArgoCD.

Each step depends on the previous — strict ordering required.

## Outputs
Fully bootstrapped cluster ready for application deployment.

## Quality Gates
- [ ] All 10 steps completed in strict order
- [ ] No step skipped or parallelised
- [ ] Each dependent step confirmed healthy before proceeding

## References
- `.claude/skills/devops-engineer/terraform-cluster-provisioning/SKILL.md`
- `.claude/skills/devops-engineer/vault-provisioning/SKILL.md`
- `.claude/skills/devops-engineer/argocd-application-management/SKILL.md`
- `.claude/skills/devops-engineer/observability-stack-management/SKILL.md`
