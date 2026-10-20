# Vault Provisioning

## Purpose
Handles Vault init, unseal, and full credential/PKI provisioning via Kubernetes Jobs.

## Role
DevOps Engineer

## Phase
Cross-phase (infrastructure)

## Triggered By
Cluster bootstrap; new service needing Vault-issued credentials.

## Inputs
- Vault deployment (from `cluster-bootstrapping`)

## Process
Vault init, unseal, and full provisioning:
- `db-provision-job.yaml`: database credentials per service
- `k8s-auth-provision-job.yaml`: Kubernetes auth method
- `oidc-provision-job.yaml`: Authentik OIDC integration
- `pki-provision-job.yaml`: PKI for mTLS certificates

All provisioning runs as Kubernetes Jobs (not manual commands). Vault never provisioned manually in production.

## Outputs
Vault initialised, unsealed, and provisioned with DB/K8s-auth/OIDC/PKI configuration.

## Quality Gates
- [ ] All provisioning runs as Kubernetes Jobs (no manual commands)
- [ ] Database credentials provisioned per service
- [ ] Kubernetes auth method configured
- [ ] PKI configured for mTLS

## References
- `.claude/skills/devops-engineer/cluster-bootstrapping/SKILL.md`
- `.claude/skills/devops-engineer/terraform-cluster-provisioning/SKILL.md`
