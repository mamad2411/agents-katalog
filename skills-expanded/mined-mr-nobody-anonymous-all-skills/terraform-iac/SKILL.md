---
name: terraform-iac
description: "Write production Terraform: module boundaries, state and locking, plan review discipline, drift detection, and safe multi-environment layouts."
type: procedural
category: cloud
domain: cloud
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: high
level: advanced
triggers:
  - terraform module design
  - terraform state drift
  - terraform plan review
  - terraform workspace environments
  - terraform remote state
keywords:
  - terraform
  - iac
  - hcl
  - state
  - plan
  - drift
source: custom
enabled: true
---

# Terraform Infrastructure as Code

## Purpose

Write production Terraform: module boundaries, state and locking, plan review discipline, drift detection, and safe multi-environment layouts.

## When to Use

- Infrastructure must be declared as reviewable code.
- A plan shows unexpected destroys or drift from the real environment.
- Multiple environments must share modules without sharing state.

## When NOT to Use

- The infrastructure is a one-off local experiment.
- The platform is declarative elsewhere (Kubernetes manifests, Pulumi code) and mixing adds risk.
- You lack permissions to read the actual provider state.

## Capabilities

- Structure root modules, environments and reusable child modules.
- Configure remote state with locking and least-privilege access.
- Review plans for destructive changes and explain them.
- Detect and reconcile drift with targeted imports.

## Inputs

- The provider and its credential scope (account, project, subscription).
- Existing state location and whether imports are required.
- The environment topology (dev/stage/prod isolation strategy).

## Workflow

1. Read the plan end to end; treat any `-/+` or destroy of stateful resources as a stop sign.
2. Keep environments isolated by directory or workspace with separate state.
3. Use modules with small, explicit variable surfaces and no hidden provider defaults.
4. Import existing resources instead of recreating them.
5. Run `terraform fmt`, `validate` and a policy/plan check in CI.

## Tools

- terraform / opentofu
- terraform plan -out and show
- policy-as-code (OPA, checkov)

## Examples

- `terraform fmt -recursive && terraform validate`
- `terraform plan -out plan.tfplan && terraform show -no-color plan.tfplan`
- `terraform import aws_s3_bucket.logs logs-bucket`

## Safety

- Destroying stateful resources (databases, buckets, DNS zones) may be irreversible.
- Never commit state or plan files; they contain secrets and resource metadata.
- Force-unlocking state risks concurrent writers corrupting it.

## Source

All-Skills canonical library (`skills/cloud/terraform-iac`). First-party skill, maintained in this repository.

## Notes

- `terraform plan` in CI on every PR is the cheapest drift and blast-radius control.
- Modules should not create providers; pass them in explicitly.
- Pairs with: `cloud/aws-compute`, `cloud/pulumi-iac`.
