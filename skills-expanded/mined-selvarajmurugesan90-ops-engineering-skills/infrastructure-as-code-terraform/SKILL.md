---
name: infrastructure-as-code-terraform
description: >
  Authors, structures, and safely applies Terraform infrastructure-as-code,
  including module design, remote state, workspaces, plan review, and
  importing existing resources. Use when the user asks to "write Terraform
  for X," "structure a Terraform repo/modules," "manage remote state,"
  "import existing infrastructure into Terraform," "review a Terraform
  plan," or "safely apply/destroy infrastructure changes."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devops
  maturity: stable
---

# Infrastructure as Code (Terraform)

## Purpose

Terraform lets infrastructure be declared as versioned, reviewable code
rather than configured by hand through cloud consoles, which is what makes
infrastructure changes auditable, repeatable across environments, and safe
to change collaboratively. The operational risk it manages is drift and
irreversibility: a `terraform apply` can create, modify, or destroy real
cloud resources, so the workflow around *how* Terraform is run (plan
review, state locking, blast-radius scoping) matters as much as the HCL
itself.

## When to use

- Provisioning new cloud infrastructure (VPCs, compute, managed databases,
  Kubernetes clusters, IAM) that should be reproducible across
  environments.
- Structuring a Terraform codebase into reusable modules instead of one
  large monolithic configuration.
- Setting up or migrating remote state (e.g., to an S3 + DynamoDB or
  Terraform Cloud/Enterprise backend) with locking.
- Bringing existing, manually-created cloud resources under Terraform
  management (`import`).
- Reviewing a `terraform plan` output before an apply to a shared or
  production environment.
- Safely decommissioning infrastructure (`terraform destroy` or resource
  removal) without unintended blast radius.

## Prerequisites & environment

- Terraform ≥ 1.5 is recommended: it introduced `import` blocks (config-driven
  imports, reviewable in a plan) and `moved`/`check` blocks matured around
  this line; Terraform ≥ 1.7 added `terraform test`. Terraform 0.12–0.14 
  used different HCL2 syntax nuances — confirm the version before assuming
  syntax compatibility, especially for `for_each`/`dynamic` blocks.
- A configured cloud provider credential with least-privilege permissions
  scoped to what the configuration actually manages (not account-owner/
  root credentials).
- A remote backend for state (S3+DynamoDB, Azure Storage, GCS, or
  Terraform Cloud) — local state files are unsafe for anything beyond a
  single-person experiment because they aren't locked or shared.
- `tflint` and/or `terraform validate`, plus a policy tool if enforcing
  guardrails (OPA/Conftest, Sentinel on Terraform Cloud/Enterprise, or
  Checkov) — recommended, not optional, for any team-shared repo.
- Version pinning for both Terraform itself (`required_version`) and every
  provider (`required_providers` with version constraints) to avoid
  unannounced behavior changes on `terraform init`.

## Step-by-step guidance

1. **Pin versions and configure a remote backend first.**
   ```hcl
   terraform {
     required_version = ">= 1.7, < 2.0"
     required_providers {
       aws = {
         source  = "hashicorp/aws"
         version = "~> 5.0"
       }
     }
     backend "s3" {
       bucket         = "example-tfstate-<AWS_ACCOUNT_ID>"
       key            = "payments-api/prod/terraform.tfstate"
       region         = "us-east-1"
       dynamodb_table = "terraform-locks"
       encrypt        = true
     }
   }
   ```
   The DynamoDB table provides state locking so two people/pipelines
   can't `apply` concurrently and corrupt state.

2. **Structure reusable modules** with a clear input/output contract
   rather than copy-pasting resource blocks per environment:
   ```
   modules/
     vpc/
       main.tf
       variables.tf
       outputs.tf
   environments/
     dev/main.tf     # module "vpc" { source = "../../modules/vpc" ... }
     staging/main.tf
     prod/main.tf
   ```
   Each environment directory has its own state file/backend key, keeping
   blast radius scoped — a bad plan in `dev` cannot touch `prod` state.

3. **Always review the plan before applying**, especially to shared
   environments:
   ```bash
   terraform plan -out=tfplan
   terraform show -json tfplan | <policy-checker>   # optional automated gate
   terraform apply tfplan
   ```
   Applying a saved plan file (rather than re-running `apply` bare)
   guarantees what gets applied is exactly what was reviewed — state
   can't have drifted in between in a way that silently changes the
   outcome.

4. **Import existing resources instead of recreating them.** With
   Terraform ≥ 1.5, prefer a declarative `import` block (plannable,
   reviewable, and removable after the import is committed) over the
   imperative `terraform import` CLI command:
   ```hcl
   import {
     to = aws_s3_bucket.logs
     id = "example-logs-bucket"
   }

   resource "aws_s3_bucket" "logs" {
     bucket = "example-logs-bucket"
   }
   ```
   Run `terraform plan` to confirm the generated plan shows the resource
   being *adopted*, not recreated, then `terraform apply`. On Terraform
   < 1.5, use `terraform import aws_s3_bucket.logs example-logs-bucket`
   and hand-write the matching resource block so `plan` shows no diff.

5. **Use `moved` blocks when refactoring**, not delete-and-recreate, to
   avoid Terraform planning a destroy+create for a resource that only
   changed its address in code:
   ```hcl
   moved {
     from = aws_instance.web
     to   = module.web_server.aws_instance.this
   }
   ```

6. **Isolate state per environment/blast-radius**, using either separate
   state files (recommended default) or Terraform workspaces
   (`terraform workspace new staging`) for lighter-weight variants of the
   same config. Workspaces share backend config and code, which is
   convenient but makes it easier to accidentally apply against the wrong
   workspace — separate state files per environment directory are safer
   for anything production-facing.

7. **Never treat `terraform destroy` as a routine command.**
   > **Warning:** `terraform destroy` (or removing a resource block, which
   > plans a destroy) is irreversible for stateful resources (databases,
   > buckets with data, volumes) unless backups/snapshots exist
   > independently. Before running it against anything beyond a scratch/dev
   > environment: confirm via `terraform plan -destroy` exactly what will
   > be removed, confirm backups exist for stateful resources, and prefer
   > `terraform state rm` + manual deletion, or scoping `-target` narrowly,
   > over a blanket destroy when only part of the stack should go away.
   ```bash
   terraform plan -destroy -out=tfplan.destroy   # review first, always
   # terraform apply tfplan.destroy              # only after explicit sign-off
   ```

## Best practices

- Keep provider and Terraform version constraints explicit
  (`~> 5.0`, not unpinned) so `terraform init` doesn't silently pick up a
  new major provider version with breaking changes.
- Run `terraform fmt -check` and `terraform validate` in CI so malformed
  or unformatted HCL never reaches review.
- Use `for_each` over `count` for collections of similar resources when
  membership can change by key (e.g., a map of subnets) — `count`-indexed
  resources shift indices and trigger spurious replace/destroy plans when
  an item is removed from the middle of a list.
- Keep secrets out of `.tf`/`.tfvars` files entirely; source them from the
  provider's native secret manager or environment variables
  (`TF_VAR_db_password`) injected at apply time, and mark corresponding
  variables `sensitive = true` so they're redacted from plan/apply output.
- Store `.tfvars` per environment (`dev.tfvars`, `prod.tfvars`) so the
  same module code is reused with different inputs — this is the
  foundation for a clean
  [environment-promotion-strategy](../environment-promotion-strategy/SKILL.md).
- Run `terraform plan` in CI on every PR touching `.tf` files and post the
  plan output as a PR comment for human review before merge/apply — this
  is the IaC equivalent of a code review gate in
  [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md).
- Prefer many small, single-purpose state files over one giant state file
  — smaller blast radius, faster plans, and less contention on the state
  lock.

## Common pitfalls

- **Symptom:** `terraform plan` shows a resource being destroyed and
  recreated when only an unrelated attribute changed.
  **Fix:** Check whether the changed attribute forces replacement
  (`terraform plan` marks these with `# forces replacement`); if so,
  confirm that's actually intended (some attributes are immutable
  cloud-side) or restructure to avoid the forced replace, e.g. via
  `lifecycle { create_before_destroy = true }` for zero-downtime swaps.

- **Symptom:** Two people run `apply` around the same time and state gets
  corrupted or one person's changes silently disappear.
  **Fix:** This means state locking isn't in place or isn't being
  respected — configure a locking backend (S3+DynamoDB, GCS with native
  locking, Terraform Cloud) and never run `apply` with
  `-lock=false` outside a documented break-glass procedure.

- **Symptom:** A resource that already exists in the cloud (created by
  hand or by a previous tool) causes `terraform apply` to error with
  "already exists" instead of adopting it.
  **Fix:** Import it first (via an `import` block on Terraform ≥ 1.5, or
  `terraform import` on older versions) so Terraform's state matches
  reality before it tries to manage the resource going forward.

- **Symptom:** `terraform plan` output is hundreds of lines of unrelated
  changes on an otherwise small PR.
  **Fix:** This usually indicates state drift (manual console changes
  since the last apply) or a provider version bump changing a default —
  run `terraform plan` on `main` first to see the baseline drift
  separately from your intended change, and reconcile drift in its own
  PR before layering new changes on top.

- **Symptom:** Someone runs `terraform destroy` against what they thought
  was a dev workspace but it was actually pointed at prod state.
  **Fix:** Use separate state files/backends per environment (not just
  workspaces sharing one backend config) with distinct backend `key`
  values, and require `terraform workspace show`/an explicit
  `-var-file=prod.tfvars` confirmation step in any destroy runbook.

## Worked example

**Scenario:** Add a new S3 bucket for application logs in the `staging`
environment, reusing a shared module, with the plan reviewed in CI before
apply.

`modules/logging-bucket/main.tf`:
```hcl
variable "bucket_name" {
  type = string
}

variable "retention_days" {
  type    = number
  default = 90
}

resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_lifecycle_configuration" "this" {
  bucket = aws_s3_bucket.this.id
  rule {
    id     = "expire-logs"
    status = "Enabled"
    expiration { days = var.retention_days }
  }
}

output "bucket_arn" { value = aws_s3_bucket.this.arn }
```

`environments/staging/main.tf`:
```hcl
module "app_logs" {
  source         = "../../modules/logging-bucket"
  bucket_name    = "example-app-logs-staging"
  retention_days = 30
}
```

CI workflow step (GitHub Actions):
```yaml
- name: Terraform Plan
  working-directory: environments/staging
  run: |
    terraform init
    terraform plan -no-color -out=tfplan | tee plan_output.txt
- name: Post plan to PR
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      const plan = fs.readFileSync('environments/staging/plan_output.txt', 'utf8');
      github.rest.issues.createComment({
        ...context.repo, issue_number: context.issue.number,
        body: "```\n" + plan.slice(-60000) + "\n```"
      });
```
A reviewer reads the posted plan (confirms it's an additive `+ create`,
no unexpected deletes), approves the PR, and a separate `deploy` job
(gated behind the `staging` environment) runs `terraform apply tfplan`
using the exact plan artifact that was reviewed.

## Cross-references

- [gitops-workflow](../gitops-workflow/SKILL.md)
- [environment-promotion-strategy](../environment-promotion-strategy/SKILL.md)
- [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md)
