---
name: infrastructure-as-code
description: Writes and changes cloud infrastructure safely with Terraform/OpenTofu, Bicep, Pulumi, or CloudFormation/CDK - remote state, pinned modules and providers, plan review before apply, replacement and data-loss checks, drift, imports, policy scanning and CI. Use when editing .tf, .bicep, Pulumi or CDK code, reviewing a plan or what-if output, setting up state backends, importing existing resources, or building an IaC pipeline. Not for Kubernetes manifests (use kubernetes-deployments).
license: MIT
---

# Infrastructure as Code

Infrastructure code deletes real things. The plan (or what-if / preview / diff) is the source of truth for what will happen, so read it every time, and **never apply, destroy or change state without the user's explicit confirmation.**

## When to use

- Writing or modifying Terraform/OpenTofu, Bicep/ARM, Pulumi, CloudFormation or CDK code.
- Reviewing a plan before it is applied.
- Setting up state, environments, modules or an IaC CI pipeline.
- Importing hand-made resources into code, or fixing drift.

## Safety rules (read first)

The agent **may** run without asking: formatting, validation, linting, scanning, and plan/preview commands that do not change infrastructure (`terraform fmt`, `validate`, `plan`; `az deployment group what-if`; `pulumi preview`; `cdk diff`, `cdk synth`).

The agent **must stop and get explicit confirmation** before:

- `terraform apply` / `tofu apply` / `destroy`, any `-auto-approve`
- `terraform state rm`, `state mv`, `import` (CLI), `force-unlock`, `taint`/`-replace`
- `az deployment ... create` (and never `--mode Complete` without a separate, explicit OK: it deletes resources not in the template)
- `az stack ... create` / `set` / `delete` (deployment stacks), especially with `--action-on-unmanage deleteResources` or `deleteAll`, which delete resources
- `pulumi up`, `pulumi destroy`, `pulumi state delete`
- `cdk deploy`, `cdk destroy`, executing a CloudFormation change set
- Any command against a production account, subscription or project, including read-only `plan` / `what-if`, unless the user has already said the agent may use production credentials for previews

Before asking, show the user a summary of the plan: counts of add/change/destroy and every replacement or deletion by name.

## Choose the tool

| Tool | Clouds | Language | State | Preview command |
| --- | --- | --- | --- | --- |
| Terraform | Any (large provider ecosystem) | HCL | State file in a backend | `terraform plan` |
| OpenTofu | Same as Terraform (open-source fork, MPL license) | HCL | State file; supports client-side state encryption | `tofu plan` |
| Bicep (compiles to ARM) | Azure | Bicep DSL | Azure itself (no state file) | `az deployment group what-if` |
| Pulumi | Any | TypeScript, Python, Go, C#, Java, YAML | Pulumi Cloud or self-managed backend | `pulumi preview --diff` |
| CloudFormation / CDK | AWS | YAML/JSON / TS, Python, Java, C#, Go | AWS (stacks) | Change sets / `cdk diff` |

Default: follow what the repository already uses. For a new multi-cloud or multi-vendor setup choose Terraform or OpenTofu; for Azure-only teams Bicep is a strong option; for AWS-only teams that want a general-purpose language, CDK.

## Workflow for a change

1. **Find the root module / stack and environment** you are changing, and which backend and account it targets. Confirm the target with the user if it could be production.
2. **Make the smallest change.** Follow existing module structure and naming. Add tags/labels the repo requires (owner, environment, cost center).
3. **Format and validate**: `terraform fmt -recursive` and `terraform validate` (or `tofu`), `az bicep build --file main.bicep`, `pulumi preview`, `cdk synth`.
4. **Lint and scan** (see Policy and scanning).
5. **Produce a plan and save it**: `terraform plan -out=tfplan`, then read it with `terraform show tfplan` (or `terraform show -json tfplan` for tooling).
6. **Review the plan** with [references/plan-review-checklist.md](references/plan-review-checklist.md). Look first for `destroy`, `must be replaced` and `# forces replacement`.
7. **Summarize for the user**: what changes, every deletion/replacement, data-loss risk, downtime risk, cost impact if known.
8. **Apply only the reviewed plan, only after confirmation**: `terraform apply tfplan`. Applying a saved plan guarantees you apply what was reviewed.
9. **Verify** the resources and the application after apply, and that a fresh plan shows no changes.

## State

- Use a **remote backend with locking**: S3 (Terraform 1.10+ supports S3-native lock files with `use_lockfile = true`; older setups use a DynamoDB lock table, now deprecated, so check the version), `azurerm` (Blob Storage lease locking), `gcs`, or HCP Terraform / Terraform Enterprise. Pulumi: Pulumi Cloud or an object-storage backend.
- **State contains secrets in plain text** (passwords, keys, connection strings). Encrypt the bucket/container, restrict access to the pipeline and a few admins, enable versioning for recovery.
- `sensitive = true` only hides values from CLI output. They are still in state.
- **Never commit** `*.tfstate`, `*.tfstate.backup`, `.terraform/`, or tfvars files that contain secrets. **Do commit** `.terraform.lock.hcl`.
- One state per environment and per blast radius. A single giant state makes every plan slow and every mistake big.

## Environments

| Approach | Good for | Watch out |
| --- | --- | --- |
| Separate root directories (or stacks) per environment, sharing modules | Production isolation, different backends and credentials per env | Some duplication of root config |
| Terraform CLI workspaces | Short-lived or identical copies (feature environments) | Same backend and credentials; easy to run in the wrong workspace; not strong isolation |
| Separate accounts / subscriptions / projects per environment | Strongest isolation (recommended for prod) | More setup; needs automation |

Always confirm the selected workspace/stack and cloud account before planning.

## Versions and modules

- Pin Terraform/OpenTofu with `required_version` and providers with `required_providers` (`version = "~> 5.0"` style constraints). Upgrade providers deliberately (see `dependency-upgrades`), regenerating the lock file with `terraform init -upgrade` and reviewing the diff.
- Pin modules: registry modules with `version`, git modules with `?ref=` a tag or commit SHA. Never track a moving branch.
- Keep modules small and purposeful (a network, a database, a service). Expose variables with types, descriptions and `validation` blocks; output only what callers need.
- Don't wrap a single resource in a module just to rename its arguments.

## Refactoring without destroying

- Renaming or moving resources changes their address, which plans as destroy + create. Use `moved` blocks (Terraform) or aliases (Pulumi) so state follows the code.
- Bring existing resources under management with `import` blocks (Terraform 1.5+) or `pulumi import`, then iterate until the plan shows no changes.
- Stop managing a resource without deleting it with a `removed` block or `terraform state rm` (confirm first).
- Protect critical resources: `lifecycle { prevent_destroy = true }`, CloudFormation `DeletionPolicy: Retain` or `Snapshot`, Azure resource locks, deletion protection flags on databases.

## Drift

- Detect: `terraform plan -refresh-only`, or a scheduled `terraform plan -detailed-exitcode` in CI (exit code 2 means changes are pending). `pulumi refresh --preview-only`; CloudFormation drift detection; Bicep what-if.
- Decide per difference: update code to match reality, or re-apply code to undo the manual change. Ask the user which; manual changes are sometimes emergency fixes.
- Reduce drift by removing console write access for managed resources.

## Secrets

- No secrets in code or committed variable files. Read them from a secret manager (data sources), or pass via the pipeline's secret store.
- Prefer resources that generate and store secrets inside the cloud (managed identities, generated DB passwords stored in a vault) over passing values through IaC.

## Policy and scanning

| Purpose | Tools |
| --- | --- |
| Lint | `tflint` (provider rule sets), `az bicep lint`, `cfn-lint` |
| Security misconfiguration | Checkov, Trivy (`trivy config .`; tfsec's checks now live in Trivy), KICS |
| Policy as code | OPA/Conftest on plan JSON, Sentinel (HCP Terraform), Azure Policy, AWS Config rules |
| Cost diff in PRs | Infracost (see `cloud-cost-optimization`) |

## CI/CD flow

1. On pull request: `fmt -check`, `validate`, lint, scan, `plan` for each affected environment; post a plan summary on the PR.
2. Require review of the plan, not just the code.
3. On merge: apply the **saved plan** from the same commit, with a manual approval gate for production.
4. Authenticate the pipeline to the cloud with OIDC federation, not long-lived keys (see `ci-cd-pipelines`).
5. Allow only one apply per state at a time (pipeline concurrency group plus state locking).

## Anti-patterns

- **Applying without reading the plan**, or running `apply` that re-plans instead of applying the reviewed plan.
- **Ignoring `forces replacement`** on databases, disks, DNS zones or networks. Replacement can mean data loss and downtime.
- **Hand-editing state** or using `state rm` to "fix" errors without understanding why.
- **Click-ops on managed resources**, which then get reverted on the next apply.
- **One state for everything**, so a typo in a tag plan touches the production database.
- **Unpinned providers and modules**, so the same code plans differently next week.
- **Secrets in tfvars committed to git.**
- **`--mode Complete` / `destroy` used as cleanup** without listing what will be deleted.

## Done when

- Code is formatted, validates, and passes lint and security scans (or findings are explained).
- A saved plan has been reviewed; every delete and replacement is listed and approved by the user.
- Apply ran only after explicit confirmation, and a follow-up plan shows no changes.
- State is remote, locked, encrypted and not in git; versions are pinned and the lock file is committed.

## References

- [references/plan-review-checklist.md](references/plan-review-checklist.md) — read before summarizing any plan, what-if, preview or diff for the user.
