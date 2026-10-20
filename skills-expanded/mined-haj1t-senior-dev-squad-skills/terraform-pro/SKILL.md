---
name: terraform-pro
description: "Terraform modules, remote state, workspaces, CI/CD for IaC, security scanning. Use when writing or reviewing Terraform infrastructure code."
---

# Terraform Pro

## Purpose

Manage infrastructure as code at production scale. Covers module design, remote state, workspaces, CI/CD pipelines, policy as code, and security scanning.

## When to Use

**Use this when:**
- Designing or refactoring Terraform module structure for a multi-environment setup
- Setting up remote state with locking or migrating from local to remote backends
- Adding a Terraform CI/CD pipeline with plan-on-PR and apply-on-merge gates

**Use this ESPECIALLY when:**
- Multiple engineers are applying Terraform manually without state locking — state corruption is imminent
- A module has no documented inputs/outputs and callers are copy-pasting variable blocks
- Security scanning (tfsec, checkov) is absent from CI and the team is shipping IaC without policy checks

**Don't skip when:**
- Provisioning any production database or stateful resource — deletion protection and prevent_destroy must be set
- Adding a new environment — workspace isolation and backend key separation are required before first apply
- Handling secrets in Terraform — sensitive outputs, SSM/Secrets Manager references, and never-in-state patterns apply

## Core Patterns

### 1. Project Structure

A standard multi-environment layout separates per-environment entry points from reusable modules. See [REFERENCE.md](REFERENCE.md) for the full directory tree.

### 2. Module Design

Modules expose typed variables with descriptions and defaults, use `deletion_protection`, encrypt storage, export structured outputs, and tag every resource. See [REFERENCE.md](REFERENCE.md) for a complete annotated RDS module example.

### 3. Remote State

Remote state uses an S3 backend with DynamoDB locking, explicit `encrypt = true`, per-environment state keys, and pinned provider/Terraform versions. See [REFERENCE.md](REFERENCE.md) for the full `backend.tf` block.

### 4. Workspace Strategy

Use named workspaces (`dev`, `staging`, `prod`) and drive environment-specific values via `terraform.workspace` locals rather than duplicating variable files. See [REFERENCE.md](REFERENCE.md) for the workspace commands and conditional locals pattern.

### 5. CI/CD for Terraform

The pipeline runs `fmt -check`, `init`, `validate`, and a security scan on every push; posts a plan comment on every PR; and applies only on merge to main with environment approval gates. See [REFERENCE.md](REFERENCE.md) for the full GitHub Actions workflow YAML.

### 6. Policy as Code (Sentinel)

Sentinel rules enforce invariants (e.g. encryption on all resources) before apply. See [REFERENCE.md](REFERENCE.md) for a Sentinel policy example.

### 7. Security Scanning

Run `terrascan`, `tfsec`, `checkov`, and `infracost` in CI before every apply. See [REFERENCE.md](REFERENCE.md) for the exact commands.

### Checklist

- [ ] Remote state with locking (S3 + DynamoDB)
- [ ] State files never committed to git
- [ ] Modules follow semantic versioning
- [ ] Every module has documented inputs/outputs
- [ ] Sensitive outputs marked as `sensitive = true`
- [ ] Resource tags on every resource (Name, Environment, ManagedBy)
- [ ] prevent_destroy on critical resources (databases)
- [ ] CI/CD pipeline includes plan + apply stages
- [ ] Security scanning (tfsec/terrascan/checkov) in CI
- [ ] Cost estimation in CI (infracost)
- [ ] Workspace isolation (dev/staging/prod)
- [ ] Deletion protection on production databases

## Related Skills

- **devops-release-engineer** — Terraform provisions the infrastructure that release pipelines deploy to; coordinate when a new service requires both IaC changes and updated CI/CD configuration
- **cloud-security-auditor** — IAM policies, security group rules, and encryption settings provisioned by Terraform are the primary surface for cloud security review; use together when auditing or hardening infrastructure modules
- **docker-k8s-pro** — EKS, GKE, and AKS clusters are commonly provisioned with Terraform; coordinate when Terraform manages the Kubernetes control plane and node pools that docker-k8s-pro configures
- **security-reviewer** — sensitive variable handling, state file encryption, and least-privilege provider credentials are code-level security concerns; cross-reference when a module handles secrets or IAM
- **postgres-pro** — RDS and Cloud SQL instances provisioned in Terraform must align with the database configuration (instance class, parameter groups, backup windows) that postgres-pro recommends; coordinate on database module design
- **observability-pro** — CloudWatch, Grafana, and alerting infrastructure are often Terraform-managed; use together when building or extending the monitoring stack via IaC
