---
name: terraform-cloud-and-spacelift-iac-orchestration-platforms
description: >
  Configures Terraform Cloud/HCP Terraform and Spacelift as state-management-
  as-a-service and run-orchestration platforms layered on top of raw
  Terraform — remote state with locking, VCS-driven runs, policy-as-code
  gates (Sentinel/OPA), and scheduled drift detection. Use when a user asks
  to "set up Terraform Cloud workspaces," "configure Spacelift stacks," "add
  a policy-as-code gate to Terraform runs," "set up VCS-driven Terraform
  runs," "schedule drift detection," or is deciding between Terraform
  Cloud, Spacelift, and a CLI-only/self-managed Terraform workflow.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devops
  maturity: stable
---

# Terraform Cloud and Spacelift: IaC Orchestration Platforms

## Purpose

[infrastructure-as-code-terraform](../infrastructure-as-code-terraform/SKILL.md)
covers the CLI-only workflow: a remote backend (S3+DynamoDB or equivalent)
for state, and `terraform plan`/`apply` run by hand or from a hand-rolled CI
job. **Terraform Cloud (rebranded HCP Terraform for HashiCorp's managed
offering)** and **Spacelift** are a different layer entirely: they are
run-orchestration platforms that sit on top of Terraform (or, for Spacelift,
also OpenTofu, Pulumi, and CloudFormation) and provide, as managed
capabilities, what a CLI-only workflow otherwise has to assemble by hand —
remote state storage with locking as a first-class hosted service (not just
a backend you configure), VCS-driven runs (a PR against your IaC repo
automatically triggers a plan, and merging triggers an apply, with no
custom CI YAML required), policy-as-code gates that block a run before
apply (Sentinel or OPA on Terraform Cloud; OPA on Spacelift) evaluated
against the plan's actual proposed changes, and scheduled drift detection
(a recurring job that runs `plan` against real infrastructure and reports
when it no longer matches state, independent of anyone actually running a
new apply). This skill covers configuring each platform's workspace/stack
model, VCS integration, policy gates, and drift-detection scheduling — it
assumes the underlying Terraform module/state concepts from
[infrastructure-as-code-terraform](../infrastructure-as-code-terraform/SKILL.md)
and doesn't repeat HCL authoring or module design.

## When to use

- Deciding whether a team's Terraform workflow should move from a
  hand-rolled CI pipeline (a GitHub Actions/GitLab CI job running
  `terraform plan`/`apply` against an S3+DynamoDB backend) to a managed
  orchestration platform, and which one.
- Setting up Terraform Cloud/HCP Terraform workspaces or Spacelift stacks
  with VCS-driven runs, so a PR against the IaC repo automatically produces
  a reviewable plan without custom pipeline YAML.
- Writing or debugging a Sentinel or OPA policy that should block a
  non-compliant plan (e.g. an unencrypted resource, a disallowed region)
  before it can be applied.
- Configuring scheduled drift detection so manual/out-of-band changes to
  cloud resources are surfaced automatically instead of only being
  discovered at the next intentional apply.
- Comparing Terraform Cloud, Spacelift, and a self-managed CI-driven
  workflow on cost, policy-gate model, and multi-IaC-tool support
  (Spacelift's Pulumi/CloudFormation/OpenTofu support vs. Terraform Cloud's
  Terraform/OpenTofu-only scope).
- Migrating an existing CLI-only Terraform setup (S3+DynamoDB backend, CI
  pipeline running plan/apply) onto one of these platforms without losing
  existing state.

## Prerequisites & environment

- An existing Terraform (or OpenTofu; Spacelift also supports Pulumi and
  CloudFormation) codebase already structured into modules/environments,
  per [infrastructure-as-code-terraform](../infrastructure-as-code-terraform/SKILL.md)
  — these platforms orchestrate runs against your existing code, they
  don't replace the need for well-structured HCL.
- A Terraform Cloud/HCP Terraform organization and account, or a Spacelift
  account — both offer a free tier with usage limits; confirm current tier
  boundaries (run/user/workspace counts, which policy engine is available
  on which tier) against each vendor's own pricing page before assuming
  parity, since both have changed their tiering over time.
- A VCS provider (GitHub, GitLab, Bitbucket, Azure DevOps) connected via an
  OAuth app or VCS integration so the platform can receive webhook events
  for PR-triggered plans and merge-triggered applies.
- Cloud provider credentials the platform's run environment will use to
  execute `plan`/`apply` — scoped least-privilege to what the specific
  workspace/stack manages, injected as the platform's own encrypted
  variable/credential store rather than committed anywhere in the repo.
- A decision on policy engine: **Sentinel** (Terraform Cloud/Enterprise's
  native policy-as-code language, paid tiers only) or **OPA/Rego**
  (supported on Terraform Cloud's newer OPA integration and natively by
  Spacelift) — confirm which is available on your tier/platform before
  writing policy in a language the platform can't actually enforce with.

## Step-by-step guidance

1. **Migrate existing state into the platform's managed state storage**
   rather than keeping a separate S3+DynamoDB backend alongside it — both
   platforms provide state storage as part of the workspace/stack, with
   locking handled automatically:
   ```hcl
   # Terraform Cloud backend config (replaces an S3+DynamoDB backend block)
   terraform {
     cloud {
       organization = "example-org"
       workspaces {
         name = "payments-api-prod"
       }
     }
   }
   ```
   ```bash
   terraform login                 # authenticates the CLI to Terraform Cloud
   terraform init                  # migrates existing local/S3 state on first run, with a confirmation prompt
   ```
   For Spacelift, state is managed per-stack in Spacelift's own backend by
   default, or you can point a stack at an existing external backend during
   a transitional migration period — check current Spacelift docs for the
   supported migration path before assuming a specific mechanism.

2. **Create one workspace (Terraform Cloud) or stack (Spacelift) per
   deployable unit/environment**, mirroring the state-isolation-per-
   blast-radius principle from
   [infrastructure-as-code-terraform](../infrastructure-as-code-terraform/SKILL.md) —
   a workspace/stack is the platform's unit of state, variables, and run
   history, so conflating environments into one workspace defeats blast-
   radius isolation the same way sharing one state file would:
   ```
   Terraform Cloud workspaces:
     payments-api-dev
     payments-api-staging
     payments-api-prod

   Spacelift stacks (equivalent):
     payments-api-dev
     payments-api-staging
     payments-api-prod
   ```

3. **Connect each workspace/stack to a VCS repository and branch**, so a PR
   automatically triggers a `plan` (posted as a check/comment on the PR)
   and a merge automatically triggers an `apply` — no custom CI YAML
   needed for the plan/apply mechanics themselves:
   ```
   Terraform Cloud workspace settings:
     VCS repo: github.com/example-org/infra
     Working directory: environments/prod
     Trigger: only when files in "environments/prod/**" change (path-based trigger)
     Apply method: Manual apply (require a human to confirm after plan)
   ```
   ```yaml
   # Spacelift stack config (spacelift.yaml, conceptual)
   stack:
     name: payments-api-prod
     repository: infra
     branch: main
     project_root: environments/prod
     autodeploy: false   # require manual confirmation before apply, same intent as Terraform Cloud's manual apply
   ```
   Keep `autodeploy`/apply method set to manual confirmation for production
   workspaces/stacks — automatic apply-on-merge is reasonable for a
   low-risk dev environment but removes the human review step that
   [infrastructure-as-code-terraform](../infrastructure-as-code-terraform/SKILL.md)
   treats as essential before a production apply.

4. **Write a policy-as-code check that evaluates the plan itself**, not
   just the HCL source, so it can catch issues that only exist in the
   proposed change (a plan that would remove encryption, widen an IAM
   policy, or touch a disallowed region) — Sentinel example (Terraform
   Cloud/Enterprise):
   ```python
   import "tfplan/v2" as tfplan

   s3_buckets = filter tfplan.resource_changes as _, rc {
       rc.type is "aws_s3_bucket" and
       (rc.change.actions contains "create" or rc.change.actions contains "update")
   }

   main = rule {
       all s3_buckets as _, bucket {
           bucket.change.after.server_side_encryption_configuration is not null
       }
   }
   ```
   OPA/Rego equivalent (Spacelift or Terraform Cloud's OPA integration),
   evaluated against the plan JSON:
   ```rego
   package terraform.policies.s3_encryption

   deny[msg] {
       resource := input.resource_changes[_]
       resource.type == "aws_s3_bucket"
       not resource.change.after.server_side_encryption_configuration
       msg := sprintf("S3 bucket %v must have encryption configured", [resource.address])
   }
   ```
   Attach the policy in **advisory** (warn, don't block) mode first against
   real runs to gauge false-positive rate, then switch to **mandatory**
   (block the run) once tuned — this is the IaC-orchestration-platform
   equivalent of the phased-rollout discipline used for any new blocking
   scan gate.

5. **Schedule drift detection** so out-of-band changes (a console edit, a
   change made by another tool) are surfaced without waiting for the next
   intentional apply:
   ```
   Terraform Cloud workspace settings → Drift Detection
     Schedule: Daily at 02:00 UTC
     Notify: Slack webhook / email on detected drift
   ```
   ```yaml
   # Spacelift scheduled drift detection (conceptual)
   scheduling:
     drift_detection:
       schedule: "0 2 * * *"
       reconcile: false   # detect and notify only; don't auto-apply to "fix" drift
   ```
   Keep drift detection in detect-and-notify mode, not auto-reconcile, by
   default — automatically applying to correct drift can itself be a
   surprising, unreviewed production change if the drift was actually an
   intentional out-of-band fix (e.g. an emergency console change during an
   incident) rather than unwanted deviation.

   > **Warning:** enabling `reconcile: true` (Spacelift) or an equivalent
   > auto-apply-on-drift setting means the platform will run `apply`
   > against production infrastructure with no human review, purely
   > because observed state diverged from code — including cases where the
   > divergence was an intentional emergency fix. Treat this the same as
   > any other unreviewed production apply: enable it only after explicit,
   > deliberate sign-off per workspace/stack, never as a default.

6. **Store sensitive input variables in the platform's own encrypted
   variable store**, marked sensitive/write-only, rather than in `.tfvars`
   committed to the VCS repo the platform reads from:
   ```
   Terraform Cloud workspace variables:
     db_password  (Terraform variable, category: terraform, Sensitive: true)
   ```
   This is the same "keep secrets out of `.tf`/`.tfvars`" discipline from
   [infrastructure-as-code-terraform](../infrastructure-as-code-terraform/SKILL.md),
   applied to the platform's own variable store instead of CI secrets.

7. **Use run tasks/policy checks as a place to wire in existing scanners**
   rather than duplicating them — both platforms support hooking external
   checks (e.g. a Checkov/tfsec run, per
   [checkov-and-tfsec-iac-security-scanning](../../../devsecops/skills/checkov-and-tfsec-iac-security-scanning/SKILL.md))
   into the run pipeline as a required check before apply, so IaC security
   scanning and orchestration-platform policy gates compose instead of
   running as two disconnected systems.

8. **Review run history and state versions before assuming reproducibility**
   — both platforms retain a full run/state-version history per
   workspace/stack, which is useful for auditing exactly what plan was
   approved and applied for any past change, distinct from and
   complementary to Git history of the HCL source itself.

## Best practices

- Require manual apply confirmation for any production workspace/stack;
  reserve auto-apply-on-merge for genuinely low-risk environments (a
  scratch/dev workspace) where an unreviewed apply is an acceptable risk.
- Roll out a new policy-as-code check in advisory/warn mode before
  switching it to mandatory/blocking — an under-tuned policy blocking every
  run has the same organization-wide blast radius as an under-tuned
  security scanner suddenly gating merges.
- Keep drift detection in notify-only mode by default; treat
  auto-reconciliation as a deliberate, reviewed choice per workspace, not a
  default behavior, since some drift is an intentional emergency fix that
  shouldn't be silently reverted.
- Scope cloud credentials per workspace/stack to exactly what that
  workspace manages, using the platform's own credential/variable store —
  don't reuse one broad, account-wide credential across every
  workspace/stack for convenience.
- Use path-based VCS triggers (only run a workspace when files under its
  specific directory change) in a monorepo layout, so an unrelated change
  elsewhere in the repo doesn't trigger every workspace's plan.
- Treat the platform's policy engine as complementary to, not a
  replacement for, static IaC scanning that runs earlier in the PR
  lifecycle — a Checkov/tfsec check on the PR catches misconfigurations at
  review time; a Sentinel/OPA policy on the plan is a second, plan-aware
  gate that can catch issues only visible once Terraform has computed the
  actual proposed changes.

## Common pitfalls

- **Symptom:** A workspace/stack's automatic VCS-triggered plan runs (and
  posts a comment) for every PR in a monorepo, even ones that don't touch
  that workspace's infrastructure at all.
  **Fix:** Configure a path-based trigger scoped to the workspace's working
  directory, rather than the default "any change in the connected repo"
  behavior — an unscoped trigger produces noisy, irrelevant plan comments
  and wastes run minutes.

- **Symptom:** A newly-added Sentinel/OPA policy blocks every run across an
  entire organization the moment it's enabled, including runs unrelated to
  what the policy was meant to catch.
  **Fix:** Attach the policy in advisory mode first, review a representative
  sample of real runs against it, and only switch to mandatory/blocking
  once the false-positive rate is understood and accepted — the same
  phased-rollout discipline as any new blocking gate.

- **Symptom:** Scheduled drift detection reports drift on a resource that
  was intentionally changed out-of-band during an incident, and the
  reconciliation setting automatically applies a "fix" that reverts the
  emergency change.
  **Fix:** Keep drift detection in detect-and-notify mode, not
  auto-reconcile, by default; when drift is genuinely intentional (an
  emergency fix), update the Terraform source to match reality (or apply
  deliberately) rather than letting an automated reconciliation job revert
  it silently.

- **Symptom:** A team migrates from an S3+DynamoDB backend to Terraform
  Cloud/Spacelift-managed state and can no longer run `terraform plan`
  locally the way they used to.
  **Fix:** This is often intentional (the platform is meant to be the
  primary/only place runs execute for shared environments), but if local
  plans are still needed for development, use `terraform login` /
  Spacelift's CLI to authenticate the local CLI against the platform's
  remote backend rather than trying to point back at the old S3 backend,
  which would create two divergent sources of truth for the same state.

- **Symptom:** A sensitive variable (a database password) was set as a
  plain (non-sensitive) workspace variable and is now visible in run logs
  or the UI to anyone with workspace read access.
  **Fix:** Mark the variable sensitive (or write-only, on platforms that
  support it) at creation time — sensitivity is not retroactively
  fixable for past run logs that may have already displayed the value, so
  rotate the credential immediately upon discovering this, then recreate
  the variable correctly marked sensitive.

## Worked example

**Scenario:** A team migrates `payments-api`'s production Terraform from a
hand-rolled GitHub Actions pipeline (S3+DynamoDB backend, manual `apply`
approval via a protected environment) to Terraform Cloud, adding a Sentinel
policy requiring encryption on all S3 buckets and daily drift detection.

Backend migration:
```hcl
terraform {
  cloud {
    organization = "example-org"
    workspaces {
      name = "payments-api-prod"
    }
  }
}
```
```bash
terraform login
terraform init   # prompts to migrate existing S3-backed state into Terraform Cloud
```

Workspace configuration:
```
VCS repo: github.com/example-org/infra, branch: main
Working directory: environments/prod
Trigger: only on changes under environments/prod/**
Apply method: Manual apply
```

Sentinel policy (mandatory, after a 2-week advisory period showed zero
false positives):
```python
import "tfplan/v2" as tfplan

s3_buckets = filter tfplan.resource_changes as _, rc {
    rc.type is "aws_s3_bucket" and
    (rc.change.actions contains "create" or rc.change.actions contains "update")
}

main = rule {
    all s3_buckets as _, bucket {
        bucket.change.after.server_side_encryption_configuration is not null
    }
}
```

Drift detection: scheduled daily at 02:00 UTC, notify-only, posting to the
team's on-call Slack channel on detected drift rather than auto-applying.

Result: a PR touching `environments/prod/main.tf` now automatically
produces a plan comment on the PR (no custom CI YAML maintaining the
plan/apply mechanics), a merge requires a human to click "Confirm & Apply"
in the Terraform Cloud UI after the Sentinel policy passes, and any manual
console change to a payments-api-prod resource is surfaced by the next
day's drift-detection run instead of silently persisting until the next
intentional deploy.

## Cross-references

- [infrastructure-as-code-terraform](../infrastructure-as-code-terraform/SKILL.md) — the underlying CLI-only Terraform workflow (module design, state, plan review) this skill's platforms orchestrate; read that skill first for HCL/state fundamentals not repeated here.
- [checkov-and-tfsec-iac-security-scanning](../../../devsecops/skills/checkov-and-tfsec-iac-security-scanning/SKILL.md) — static IaC misconfiguration scanning that composes with, rather than duplicates, a Sentinel/OPA plan-time policy gate configured here.
- [gitops-workflow](../gitops-workflow/SKILL.md) — a comparable git-driven-reconciliation pattern for Kubernetes/application deployments; VCS-driven Terraform runs here are the IaC-provisioning analogue.
- [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md) — the general pipeline-gate concepts (required checks, manual approval) that these platforms implement as native features instead of hand-rolled CI YAML.
