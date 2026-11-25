---
name: terraform-patterns
description: Module composition, state management, workspace strategy, provider versioning, and infrastructure-as-code best practices. Grok-native with Production Contract.
when-to-use: When writing or reviewing Terraform, Bicep-equivalent IaC, or any cloud provisioning code. Pair with devops, terraform-expert, azure/gcp/aws-expert.
---

# Terraform Patterns (Grok Port)

Maintainable, reviewable, safe IaC patterns. Focus on modules, state, workspaces, drift prevention, and Grok Production Contract (ledger for every infra change, preflight cost/security checks, compound from real outages caused by bad IaC).

## Module Composition (reusable, versioned)
```hcl
# modules/vpc/main.tf
variable "name" { type = string }
variable "cidr" { type = string default = "10.0.0.0/16" }
variable "azs" { type = list(string) default = ["us-east-1a", "us-east-1b"] }

resource "aws_vpc" "main" {
  cidr_block = var.cidr
  tags = {
    Name        = var.name
    ManagedBy   = "terraform"
    Environment = terraform.workspace
  }
}
# ... subnets, igw, etc.
```

Usage:
```hcl
module "vpc" {
  source = "../../modules/vpc"
  name   = "prod-vpc"
  cidr   = "10.1.0.0/16"
}
```

- One module per logical component (never giant monolith root).
- Version modules via git tags or Terraform Registry.
- Expose only what consumers need; sensible defaults + validation.

## State Management (remote + locking)
- Never local state in prod/CI.
- Remote backend (S3 + DynamoDB lock, or equivalent GCS/Cloud Storage + lock).
- State encryption at rest + in transit.
- Separate state files per environment / blast radius (prod vs staging vs shared).
- Never `terraform state mv` without review + backup.

## Workspace Strategy (not for everything)
- Workspaces good for: same infra, different env (dev/stage/prod) with light differences.
- Separate roots / state better for: radically different regions, accounts, or when blast radius must be isolated.
- Never use workspace for "prod vs prod-dr" if they are truly separate accounts.

## Provider Versioning & Drift
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.5.0"
}
```

- Pin major/minor; allow patch in CI.
- `terraform plan` in CI on every PR that touches .tf.
- Regular `terraform refresh` or use drift detection tools.
- Tag all resources with `ManagedBy=terraform`, `Environment`, `CostCenter`.

## Safety & Review Guardrails
- Never commit .tfstate or backend config with keys.
- Use `terraform plan -out=plan.tfplan` + `show -json` for machine-readable review.
- Policy-as-code (OPA / Sentinel / Checkov) for: no public S3, no * in IAM, required tags, approved regions.
- Destroy protection on critical resources (`prevent_destroy = true` in lifecycle for prod databases).

## Grok Integration (Production Contract)
- Primary: devops + terraform-expert + (aws-expert | gcp-expert | azure-expert).
- Fire on_infra_change hook for any .tf, module, or backend change.
- Pre-Flight (mandatory for infra PRs): "State remote + locked? Workspace or separate root correct? Cost estimate attached? IAM least-privilege? Public exposure risk? Drift detection plan? Rollback = previous commit + apply?"
- Ledger: every apply (plan hash, resources added/changed/destroyed, PR link, approver, cost delta if available).
- Handoff: plan output (or json), module diff, cost impact, secret surface (none in state), drift runbook, destroy/rollback commands.
- Friction + compound: every "prod DB was destroyed because workspace selected wrong" or "public bucket because no policy check" → compound to preflight + CI job templates.
- Palace: "Chose separate state roots for prod vs non-prod because blast radius of a mistaken workspace switch was unacceptable; rejected single root + workspaces after the 2025-03 incident".
- Claim-verification: Two-pass. Grep "resource \"aws_" → read_file actual .tf + run `terraform plan` in the context → "aws_s3_bucket 'prod-data' with prevent_destroy exists at infra/s3.tf:18 and plan shows 0 destroy ✓VERIFIED". Never claim "safe to apply" without seeing the real plan output.
- Pair with: aws-patterns / gcp-patterns / azure-patterns / kubernetes-patterns, sast-patterns (IaC secret scanning + misconfig), security-review, preflight, compound-learnings.

## When to Activate
- Any .tf change, new module, backend migration, or workspace change.
- Swarm Phase 2 (infra) + Phase 3 (review + policy).
- Before any terraform apply in shared/prod.
- PRs touching IaC.
- Cost, security, or compliance reviews (shipper + verifier).

See .grok/skills/aws-patterns/SKILL.md (and gcp/azure), kubernetes-patterns, preflight, memory-palace (store "why separate state" decisions). Always require plan review. Production Contract: ledger entry + handoff + preflight + friction for every infra mutation.

IaC is the source of truth. A bad apply is the fastest way to have a very bad day. Plan, review, policy, and rollback plan are non-negotiable.
