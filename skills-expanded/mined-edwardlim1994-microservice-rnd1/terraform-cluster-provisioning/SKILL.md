# Terraform Cluster Provisioning

## Purpose
Provisions cluster infrastructure and core infra services via Terraform.

## Role
DevOps Engineer

## Phase
Cross-phase (infrastructure)

## Triggered By
New cluster needed, or infra service change.

## Inputs
- Terraform configuration in `services/terraform` / `apps/terraform`

## Process
Provisions cluster infrastructure (nodes, networking, storage). Provisions infra services (Kafka, Apicurio, Authentik, Vault) via Terraform.

Does NOT provision app Helm releases — that is ArgoCD's job.

State backend: remote state (not local `.tfstate` files).

Run: `scripts/services-terraform-up.sh` for infra provisioning.

## Outputs
Provisioned cluster nodes, networking, and infra services.

## Quality Gates
- [ ] Remote state backend used (never local .tfstate)
- [ ] App Helm releases NOT provisioned here (ArgoCD's responsibility)
- [ ] Provisioning script run rather than manual terraform apply where applicable

## References
- `.claude/skills/devops-engineer/cluster-bootstrapping/SKILL.md`
- `.claude/skills/devops-engineer/vault-provisioning/SKILL.md`
