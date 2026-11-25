---
name: terraform-procedures
description: Use this skill when authoring or running a Terraform plan/apply, refactoring modules, performing state surgery, importing existing cloud resources, or working in repos that use OpenTofu instead of HashiCorp Terraform — Terraform and OpenTofu procedures covering state operations (state list/show/mv/rm/pull/push), plan/apply lifecycle, OpenTofu fork compatibility, state-surgery safety warnings, and workspace handling. Loaded by `/infra-change` and other infrastructure workflows; not a workflow itself.
disable-model-invocation: true
---

# Terraform Procedures — State, plan/apply, and OpenTofu compatibility

Knowledge reference for Terraform/OpenTofu operations used by infrastructure-change workflows. Covers the plan/apply lifecycle, state-management commands, refactoring patterns, and fork-compatibility notes. Designed to be loaded as background context when a workflow encounters Terraform configs.

## Terraform fork detection — OpenTofu

If `.terraform-version` or `tofu.lock.hcl` indicates [OpenTofu](https://opentofu.org) (HashiCorp BSL fork, 2023+), substitute `tofu` for `terraform` in all commands below. Flag semantics are identical for the operations covered in this skill.

Other indicators of an OpenTofu repo:
- `tofu` binary referenced in CI configs instead of `terraform`
- `.tofu/` directory or `tofu.tf` files

## Plan / apply lifecycle

### Pre-plan validation

```
terraform validate
terraform fmt -check -recursive
```

Modern pre-plan suite (run when configs are present):

```
tflint                              # if .tflint.hcl present
tfsec . --soft-fail                 # if tfsec.yml or .tfsec/ present
checkov -d . --soft-fail            # if .checkov.yml present
terraform-docs markdown table .     # regenerate docs if terraform-docs.yml present
```

### Plan with detailed exit codes

```
terraform plan -out=tfplan -detailed-exitcode
# Exit codes:
#   0 = no changes
#   1 = error
#   2 = changes proposed
```

The `-detailed-exitcode` form is the standard oracle for iterative reconciliation loops (RALF): success = `0` (no diff).

### Apply

```
terraform apply tfplan
```

Always apply a saved plan file, never re-plan during apply. Re-planning at apply time can introduce drift between what was reviewed and what is executed.

### Plan summary format

When presenting a plan for review, summarise as:

```
## Terraform Plan Summary
| Action  | Count | Resources |
|---------|-------|-----------|
| Add     | X     | [list]    |
| Change  | X     | [list]    |
| Destroy | X     | [list]    |

WARNING — DESTROY/REPLACE resources:
- [resource] — [reason]

Data loss risk: [yes/no]
Estimated cost impact: [if applicable]
```

## State operations — use with extreme caution

State surgery is the second-most-fragile area after `destroy`. Always back up state before any of these operations (`terraform state pull > backup.tfstate`).

```
terraform state list                                # enumerate resources
terraform state show <addr>                         # inspect a resource
terraform state mv <src> <dst>                      # rename / refactor
terraform state rm <addr>                           # remove from state (resource still exists in cloud)
terraform import <addr> <id>                        # adopt an existing cloud resource
terraform state pull > backup.tfstate               # snapshot state
terraform state push backup.tfstate                 # restore (DANGEROUS)
```

### Refactor without state surgery

For module refactoring, prefer `moved {}` blocks (TF v1.1+) and `removed {}` blocks (TF v1.7+) — they encode the rename inside `.tf` files instead of imperative state ops, which means:

- Changes are reviewable in PRs
- The refactor is reproducible across workspaces
- No risk of half-applied state on operator error

Example `moved` block:

```
moved {
  from = aws_instance.old_name
  to   = aws_instance.new_name
}
```

### Partial-apply anti-pattern

`-target=<resource>` for partial-apply is an anti-pattern except in emergencies. State drift between resources causes surprising future plans and breaks the invariant that the state file matches the configuration.

If `-target` becomes necessary (e.g., breaking a cyclic dependency during initial bootstrap), follow up immediately with a full plan/apply to reconcile.

## Workspaces

Terraform workspaces partition state within a single backend:

```
terraform workspace list
terraform workspace new <name>
terraform workspace select <name>
terraform workspace show
```

Workspaces are appropriate for per-environment state (dev/staging/prod) when the configuration is identical and only variable values differ. For divergent configurations, prefer separate root modules.

## Policy-as-code gate

If `.conftest/` (Conftest), `.opa/` (raw OPA Rego), `.tflint.hcl` (TFLint), or `tfsec.yml` (tfsec) / `.checkov.yml` (Checkov) configs are present, run them as a **pre-plan** gate. A plan that violates policy never advances to apply.

## Rollback

```
# Revert the .tf file changes and re-apply
terraform plan -out=tfplan-rollback
terraform apply tfplan-rollback
```

For state-only rollback (after a botched `state mv` or `state rm`):

```
terraform state push backup.tfstate
```

State rollback overwrites the backend state and should be coordinated with whoever holds the workspace lock.

## When this applies

| Phase | Apply this knowledge |
|---|---|
| Step 3 — Review current state | `terraform validate`, `fmt -check`, `plan -detailed-exitcode` |
| Step 3a-bis — State operations | `state list/show/mv/rm/import`, `moved {}` / `removed {}` blocks |
| Step 4 — Implement | `terraform fmt -recursive`, `terraform validate` |
| Step 5 — Plan review | `terraform plan -out=tfplan` and plan-summary format |
| Step 6 — Apply | `terraform apply tfplan` |
| Step 8 — Rollback | Revert `.tf` files and re-apply, or push backup state |

## Integration

- **Used by**: `/infra-change` (Steps 3, 4, 5, 6, 8 — Terraform plan/apply lifecycle)
- **Companion knowledge**: `@gitops-detection` (HCP Terraform / Terraform Cloud / Atlantis / Spacelift / env0 controllers that own the apply gate)
- **External references**: [Terraform docs](https://developer.hashicorp.com/terraform/docs), [OpenTofu docs](https://opentofu.org/docs/), [moved block](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring), [removed block](https://developer.hashicorp.com/terraform/language/resources/syntax#removing-resources)
