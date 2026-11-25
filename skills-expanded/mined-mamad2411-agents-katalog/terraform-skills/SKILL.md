---
name: terraform-skills
description: Terraform IaC patterns, modules, and best practices
category: stacks/infrastructure/terraform
applies_to: terraform
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# Terraform Skills

Infrastructure as Code tool for building, changing, and versioning infrastructure.

## Sub-Skills

### Core Concepts
- [resources.md](core/resources.md) - Resource patterns
- [data-sources.md](core/data-sources.md) - Data sources
- [providers.md](core/providers.md) - Provider configuration
- [state.md](core/state.md) - State management

### Modules
- [module-structure.md](modules/module-structure.md) - Module patterns
- [composition.md](modules/composition.md) - Module composition
- [versioning.md](modules/versioning.md) - Module versioning
- [registry.md](modules/registry.md) - Terraform Registry

### Variables
- [input-variables.md](variables/input-variables.md) - Input variables
- [output-values.md](variables/output-values.md) - Output values
- [locals.md](variables/locals.md) - Local values
- [validation.md](variables/validation.md) - Variable validation

### State Management
- [remote-state.md](state/remote-state.md) - Remote state
- [workspaces.md](state/workspaces.md) - Workspaces
- [state-locking.md](state/state-locking.md) - State locking
- [import.md](state/import.md) - Resource import

### AWS Patterns
- [vpc.md](aws/vpc.md) - VPC configuration
- [ec2.md](aws/ec2.md) - EC2 patterns
- [rds.md](aws/rds.md) - RDS patterns
- [iam.md](aws/iam.md) - IAM patterns
- [s3.md](aws/s3.md) - S3 patterns
- [lambda.md](aws/lambda.md) - Lambda patterns

### Azure Patterns
- [resource-groups.md](azure/resource-groups.md) - Resource groups
- [networking.md](azure/networking.md) - Azure networking
- [app-service.md](azure/app-service.md) - App Service

### GCP Patterns
- [compute.md](gcp/compute.md) - Compute Engine
- [networking.md](gcp/networking.md) - GCP networking
- [cloud-run.md](gcp/cloud-run.md) - Cloud Run

### CI/CD
- [github-actions.md](cicd/github-actions.md) - GitHub Actions
- [atlantis.md](cicd/atlantis.md) - Atlantis patterns
- [terraform-cloud.md](cicd/terraform-cloud.md) - Terraform Cloud

## Detection
Auto-detected when project contains:
- `*.tf` files
- `terraform.tfvars`
- `resource ` or `provider ` patterns
