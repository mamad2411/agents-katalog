---
name: terraform-conventions
description: Follow Terraform module structure and naming conventions.
---

# Terraform conventions

Local state in a shared environment causes conflicting applies that corrupt or destroy live infrastructure, and unpinned providers make `plan` non-reproducible across machines. Run `terraform validate` and `terraform fmt -check` in CI to keep structure and naming consistent.

## Structure

- One module per logical resource group (e.g. `modules/vpc/`, `modules/rds/`).
- Every module has `main.tf`, `variables.tf`, and `outputs.tf`.
- Root module composes child modules; avoid putting resources directly in root.

## Naming

- Use snake_case for all resource names, variables, and outputs.
- Prefix resources with their type when names would be ambiguous.
- Tag all resources with `environment`, `team`, and `managed_by = "terraform"`.

## State and safety

- Never store state locally in shared environments; use remote backends.
- Use `prevent_destroy` lifecycle rules on critical resources.
- Pin provider versions in `required_providers`.
- Run `terraform plan` before every apply and review the diff.

## Examples

```hcl
# BAD — resource in root module, camelCase name, no provider pin, no tags
resource "aws_s3Bucket" "myBucket" {
  bucket = "my-app-bucket"
}

# GOOD — in modules/storage/main.tf, snake_case, provider pinned, tagged
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.50" }
  }
}

resource "aws_s3_bucket" "app_assets" {
  bucket = var.bucket_name

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    environment = var.environment
    team        = var.team
    managed_by  = "terraform"
  }
}
```
