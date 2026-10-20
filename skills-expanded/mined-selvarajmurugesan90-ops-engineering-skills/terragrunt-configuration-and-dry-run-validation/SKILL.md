---
name: terragrunt-configuration-and-dry-run-validation
description: >
  Structures Terragrunt configuration (terragrunt.hcl) as a DRY layer over
  Terraform modules across multiple environments/accounts/regions, using
  `include`, `generate`, and dependency blocks to avoid duplicated backend
  and provider boilerplate, and validates changes with a plan/dry-run
  workflow (`terragrunt plan`, `run-all plan`) before any apply touches a
  shared environment. Use when the user asks to "set up Terragrunt across
  environments," "avoid duplicating Terraform backend config," "run
  terragrunt plan across all our modules," "structure a Terragrunt
  live-config repo," or "dry-run a Terragrunt change before it hits prod."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: iac-and-automation-tooling
  maturity: stable
---

# Terragrunt Configuration and Dry-Run Validation

## Purpose

Terragrunt is a thin wrapper around Terraform that solves a problem
Terraform itself doesn't: keeping backend configuration, provider
version constraints, and common variables DRY across dozens of
environment/region/account combinations that would otherwise each need
their own near-duplicate `main.tf`. It does this by layering
`terragrunt.hcl` files that `include` a root configuration and
parameterize a shared Terraform module per environment, then generates
the actual Terraform backend/provider blocks at run time. The
operational risk this introduces is exactly the one Terraform's own
[infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md)
skill covers for state and plan review — plus a Terragrunt-specific one:
`run-all` commands operate across a whole dependency graph of modules at
once, so a `run-all apply` fanning out unreviewed across every
environment is a materially larger blast radius than a single
`terraform apply`. This skill covers Terragrunt's DRY layering and the
plan/dry-run discipline needed before that fan-out ever reaches `apply`.

## When to use

- A Terraform codebase has grown to the point where `dev/main.tf`,
  `staging/main.tf`, and `prod/main.tf` are near-identical copies
  differing only in backend key and a handful of variables.
- Standing up a new Terragrunt "live" repository (environment
  configuration) that consumes versioned Terraform modules from a
  separate module repository.
- Needing one environment's Terraform output as another's input (e.g. a
  shared VPC's subnet IDs consumed by an application-tier module) without
  hardcoding remote state data source blocks by hand in every module.
- Running a plan across many modules/environments at once
  (`run-all plan`) to validate a shared-module change before it's applied
  anywhere.
- Reviewing or troubleshooting why a `terragrunt.hcl` `include`/`generate`
  block isn't producing the Terraform configuration expected.

## Prerequisites & environment

- Terragrunt ≥ 0.55 paired with a compatible Terraform (or OpenTofu)
  binary ≥ 1.5 — check `terragrunt --version` output for its bundled
  compatibility notes, since Terragrunt's HCL functions and `run-all`
  behavior have changed across major versions (0.5x introduced the
  current `dependency`/`dependencies` block semantics that replaced older
  `dependencies { paths = [...] }` syntax).
- A separate **module repository** (versioned Terraform modules, tagged
  releases) distinct from the **live repository** (Terragrunt
  configuration that instantiates those modules per environment) — mixing
  the two defeats the DRY goal.
- The same remote backend/state-locking prerequisites as plain Terraform
  (S3+DynamoDB, GCS, Azure Storage, or Terraform Cloud) — Terragrunt
  generates backend config, it doesn't replace the need for one.
- Cloud provider credentials scoped per environment/account, since a
  `run-all` command will attempt to assume/use whatever credentials are
  configured for each module it touches in the dependency graph.
- `tflint`/`terraform validate` still apply to the underlying `.tf`
  module code; Terragrunt itself has no separate linter beyond
  `terragrunt hclfmt` for HCL formatting.

## Step-by-step guidance

1. **Put shared backend/provider config in a root `terragrunt.hcl`**,
   generated once and included everywhere rather than repeated:
   ```hcl
   # live/terragrunt.hcl (root)
   remote_state {
     backend = "s3"
     generate = { path = "backend.tf", if_exists = "overwrite_terragrunt" }
     config = {
       bucket         = "example-tfstate-<AWS_ACCOUNT_ID>"
       key            = "${path_relative_to_include()}/terraform.tfstate"
       region         = "us-east-1"
       dynamodb_table = "terraform-locks"
       encrypt        = true
     }
   }

   generate "provider" {
     path      = "provider.tf"
     if_exists = "overwrite_terragrunt"
     contents  = <<-EOF
       provider "aws" {
         region = "${local.region}"
       }
     EOF
   }

   locals {
     region = "us-east-1"
   }
   ```
   `path_relative_to_include()` derives a unique state key per environment
   automatically, so no environment's `terragrunt.hcl` needs to restate
   the backend block at all.

2. **Each environment/module directory `include`s the root and points at
   a versioned module source**, keeping the diff between environments
   down to just the inputs that actually differ:
   ```hcl
   # live/prod/vpc/terragrunt.hcl
   include "root" {
     path = find_in_parent_folders()
   }

   terraform {
     source = "git::https://github.com/example-org/tf-modules.git//vpc?ref=v3.2.0"
   }

   inputs = {
     cidr_block         = "10.20.0.0/16"
     environment        = "prod"
     enable_nat_gateway = true
   }
   ```
   ```hcl
   # live/dev/vpc/terragrunt.hcl
   include "root" {
     path = find_in_parent_folders()
   }

   terraform {
     source = "git::https://github.com/example-org/tf-modules.git//vpc?ref=v3.2.0"
   }

   inputs = {
     cidr_block         = "10.10.0.0/16"
     environment        = "dev"
     enable_nat_gateway = false
   }
   ```
   Pinning `?ref=v3.2.0` on the module source means a module change
   doesn't silently propagate to every environment on the next
   `terragrunt plan` — each environment upgrades its pinned ref
   deliberately.

3. **Wire cross-module data with `dependency` blocks instead of hand-
   written remote state data sources**, so Terragrunt resolves another
   module's outputs automatically and fails loudly if that module hasn't
   been applied yet:
   ```hcl
   # live/prod/app-tier/terragrunt.hcl
   include "root" {
     path = find_in_parent_folders()
   }

   dependency "vpc" {
     config_path = "../vpc"
     mock_outputs = {
       vpc_id     = "vpc-mock00000000000"
       subnet_ids = ["subnet-mock1", "subnet-mock2"]
     }
     mock_outputs_allowed_terraform_commands = ["validate", "plan"]
   }

   terraform {
     source = "git::https://github.com/example-org/tf-modules.git//app-tier?ref=v1.8.0"
   }

   inputs = {
     vpc_id     = dependency.vpc.outputs.vpc_id
     subnet_ids = dependency.vpc.outputs.subnet_ids
   }
   ```
   `mock_outputs` let `plan`/`validate` succeed even before the dependency
   has real outputs (useful in CI on a fresh environment), while
   restricting `mock_outputs_allowed_terraform_commands` ensures a real
   `apply` still fails fast if the actual dependency hasn't been applied.

4. **Dry-run a single module before touching anything shared:**
   ```bash
   cd live/prod/vpc
   terragrunt plan
   ```
   Read the plan exactly as you would a plain `terraform plan` — this is
   the same review discipline as
   [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md),
   just invoked through the Terragrunt wrapper.

5. **Validate a multi-module change with `run-all plan` before any
   `run-all apply`.** This walks the dependency graph and plans every
   affected module in the correct order:
   ```bash
   cd live/prod
   terragrunt run-all plan
   ```
   Review the aggregated output per module carefully — `run-all` prints
   each module's plan in sequence, and it is easy to skim past one
   module's unexpected destroy buried between two clean ones.

6. **Never run `run-all apply` unreviewed across a whole environment.**
   > **Warning:** `terragrunt run-all apply` (and especially
   > `run-all destroy`) fans out across every module in the current
   > directory's dependency graph. Run `run-all plan` first, review it in
   > full, and prefer scoping to the smallest actual change:
   ```bash
   # Prefer touching one module at a time when only one changed:
   cd live/prod/app-tier && terragrunt plan && terragrunt apply

   # Only use run-all when a genuinely cross-cutting change (e.g. a
   # shared module version bump) requires it, and always plan first:
   cd live/prod && terragrunt run-all plan
   # ...review every module's plan output...
   cd live/prod && terragrunt run-all apply --terragrunt-non-interactive=false
   ```
   Avoid `--terragrunt-non-interactive` (which skips Terragrunt's own
   per-module confirmation prompts) for any `run-all apply` against a
   shared or production environment.

7. **Use `terragrunt validate-inputs` and `hclfmt` in CI** to catch a
   `terragrunt.hcl` referencing an input the underlying module doesn't
   declare (or vice versa) before it reaches a human reviewer:
   ```bash
   terragrunt hclfmt --terragrunt-check
   terragrunt validate-inputs
   ```

## Best practices

- Keep the module repository and the live (environment) repository
  separate, each independently versioned — the live repo pins module
  refs; it never vendors module source inline.
- Default every environment's `terragrunt.hcl` to `include` the root
  config rather than partially duplicating it — if two environments'
  root includes diverge, DRY has already been lost.
- Pin module `ref=` tags explicitly (never a floating branch like `ref=main`)
  so `terragrunt plan` in `prod` can't unexpectedly pick up an
  in-flight change to the module still being tested in `dev`.
- Run `run-all plan` (never `run-all apply` directly) in CI on every PR
  touching shared module code or root config, and require a human to
  read the per-environment plan diffs before merge — mirroring the CI
  plan-review gate from
  [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md).
- Scope `run-all` commands to the narrowest directory that actually needs
  it (`cd live/staging/app-tier` rather than `cd live` from the repo
  root) to keep blast radius intentional.
- Treat `mock_outputs` as a CI/dry-run convenience only — never allow
  `apply` to proceed against mocked dependency outputs
  (`mock_outputs_allowed_terraform_commands` should exclude `apply`).

## Common pitfalls

- **Symptom:** `terragrunt plan` in one environment unexpectedly reflects
  a change someone else is still testing in a different environment.
  **Fix:** The module source `ref=` is likely unpinned (pointing at a
  branch, not a tag/commit) — pin every environment's module source to an
  explicit version and bump it deliberately per environment as changes
  are promoted.

- **Symptom:** `run-all plan` fails with a dependency error before it
  even reaches the module being changed.
  **Fix:** A `dependency` block's target module hasn't been applied yet
  in this environment (no state to read outputs from) and
  `mock_outputs`/`mock_outputs_allowed_terraform_commands` either isn't
  set or doesn't cover the command being run. Add mock outputs scoped to
  `plan`/`validate` only, and apply the dependency module for real before
  the dependent module's first real `apply`.

- **Symptom:** A generated `backend.tf`/`provider.tf` file conflicts with
  a hand-written one already in the module, causing a "duplicate backend
  configuration" error.
  **Fix:** Don't hand-write backend/provider blocks inside modules meant
  to be consumed via Terragrunt's `generate` block — the module should be
  backend/provider-agnostic, and only the live repo's root
  `terragrunt.hcl` generates those blocks. Set `if_exists =
  "overwrite_terragrunt"` deliberately if a transitional period requires
  both.

- **Symptom:** Someone runs `terragrunt run-all apply` from the repo root
  intending to apply one small change, and it fans out an apply across
  every environment's module in the tree, including production.
  **Fix:** This is a destructive/dangerous action if the working
  directory wasn't scoped correctly — always `cd` into the narrowest
  directory that contains only the modules actually intended to change,
  run `run-all plan` first and read every module's output, and never
  invoke `run-all apply` from a directory whose subtree spans more than
  one environment unless that cross-environment change is genuinely
  intended and reviewed.

- **Symptom:** CI's `run-all plan` output is thousands of lines and a
  reviewer can't tell which module actually has a meaningful diff.
  **Fix:** Use `terragrunt run-all plan --terragrunt-non-interactive
  2>&1 | tee plan.log` and post a summarized diff per module (grep for
  `Plan: N to add, N to change, N to destroy` per module block) as the
  PR comment, reserving full raw output as a linked artifact rather than
  the inline comment body.

## Worked example

**Scenario:** A platform team maintains a `vpc` module and an
`app-tier` module across `dev`, `staging`, and `prod`. They bump the
`app-tier` module from `v1.7.0` to `v1.8.0` (adds a new required input)
and need to validate the change across all three environments before
applying anywhere.

Root config (`live/terragrunt.hcl`), unchanged from the standard layout
in step 1.

`live/staging/app-tier/terragrunt.hcl` before the change:
```hcl
include "root" {
  path = find_in_parent_folders()
}

dependency "vpc" {
  config_path = "../vpc"
}

terraform {
  source = "git::https://github.com/example-org/tf-modules.git//app-tier?ref=v1.7.0"
}

inputs = {
  vpc_id     = dependency.vpc.outputs.vpc_id
  subnet_ids = dependency.vpc.outputs.subnet_ids
  instance_type = "t3.medium"
}
```

Change: bump the ref and add the new required input introduced by
`v1.8.0`:
```hcl
terraform {
  source = "git::https://github.com/example-org/tf-modules.git//app-tier?ref=v1.8.0"
}

inputs = {
  vpc_id           = dependency.vpc.outputs.vpc_id
  subnet_ids       = dependency.vpc.outputs.subnet_ids
  instance_type    = "t3.medium"
  enable_autoscaling = true  # new required input in v1.8.0
}
```

Dry-run validation, staging first:
```bash
cd live/staging/app-tier
terragrunt plan
# Plan: 1 to add, 1 to change, 0 to destroy
# (new autoscaling group resource, launch template updated in place)
```

Repeated identically in `dev`, then reviewed in a PR, then applied to
`staging` alone (`terragrunt apply`) and observed for a day before the
same two-line change is copied to `prod/app-tier/terragrunt.hcl` and its
own `terragrunt plan` is reviewed before that environment's `apply`. At
no point is `run-all apply` used, since only one module per environment
actually changed — `run-all` is reserved for the (separate) case of a
root-config change that legitimately affects every module at once.

## Cross-references

- [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md) — the underlying Terraform plan-review, state-locking, and module-design guidance Terragrunt wraps rather than replaces.
- [infrastructure-post-deployment-validation-and-smoke-testing](../infrastructure-post-deployment-validation-and-smoke-testing/SKILL.md) — verifying a `terragrunt apply` actually produced working infrastructure, beyond a clean plan/apply exit code.
- [environment-promotion-strategy](../../../devops/skills/environment-promotion-strategy/SKILL.md) — the dev/staging/prod promotion sequence this skill's worked example follows when bumping a module version.
