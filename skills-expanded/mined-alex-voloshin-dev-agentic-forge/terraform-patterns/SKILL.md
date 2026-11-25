---
name: terraform-patterns
description: Terraform / IaC conventions agentic-forge applies when the detected stack is Terraform — the toolchain (terraform fmt / init -backend=false + validate / terraform test / tflint), offline checks only (the human plans and applies), mock-provider tests, validation blocks, secret and state hygiene, rendered-plan review, and the high-value Terraform pitfalls. Loaded on demand by develop / code-review and the software-engineer / qa-engineer roles after stack detection; kept off the always-on listing.
disable-model-invocation: true
---

# Terraform patterns

The Terraform stack pack: loaded by the `software-engineer` / `qa-engineer` roles (and the
`code-review` lint aspect) when `stacks.detect` reports Terraform. It carries only what is
**Terraform-specific** on top of [`engineering-standards`](../engineering-standards/SKILL.md) —
Claude already knows HCL; this encodes the conventions and gates agentic-forge holds
infrastructure changes to. (Mechanism: ADR 0015, by-stack detection + reference packs.)

## Toolchain

**Prefer the repo's own commands** — read the `Makefile` / CI workflow (and any pre-commit or
policy-as-code config) and run *those*. Defaults (the commands `stack-detect` reports as
fallbacks):

| Job | Conventional command | Gate |
| --- | --- | --- |
| format | `terraform fmt -recursive` | applied (canonical) |
| types | `terraform init -backend=false && terraform validate` | valid |
| test | `terraform test` — listed only when `*.tftest.hcl` exists | green; new behaviour covered |
| lint | `tflint --recursive` — listed only when `.tflint.hcl` sits beside the root module | clean (no new ignores) |

`init -backend=false` touches no state, but it is not read-only: it downloads providers and
modules into `.terraform/` and may rewrite `.terraform.lock.hcl`. Commit the lock file and review
its diff; use `terraform init -lockfile=readonly` when the change must not move a provider.

## Offline checks only; the human plans and applies

- **The agent runs only the offline gate:** `terraform fmt`, `terraform init -backend=false`,
  `terraform validate`, `terraform test` on mock providers (and `tflint` when configured). None
  of these reads state or reaches a cloud API. "Offline" is about the cloud, not about trust:
  `init` downloads providers and `tflint` runs the ruleset plugins the repo's `.tflint.hcl` names
  (`tflint --init` downloads them), so in an untrusted repo they are the same class of risk as
  running its tests.
- **Anything against a real backend is the human's step**, named in the hand-off, never run:
  `terraform init` with the backend, `terraform plan -out=plan.out`, `terraform show -json
  plan.out`, and above all `terraform apply`, `terraform destroy`, `import`, `state rm/mv/push`
  and `force-unlock` — not even "just to check". A real plan runs on whatever credentials the
  shell happens to hold, takes the state lock, and writes `plan.out` with every secret in
  plaintext.
- **The hand-off says what to review in the rendered plan**, not only in the HCL, whenever the
  change builds a document: `jsonencode(...)`, policy definitions and assignments, IAM / bucket
  policies, templated config. `terraform show -json plan.out` shows what the provider will send;
  the HCL can read right while the rendered JSON is wrong — the field case was Azure Policy rules
  that looked correct in HCL and that Azure would have refused at assignment. Name the commands,
  the addresses that should change (and how: update, move, replace), and the documents to read.

## Idioms

- **Validate inputs where they enter.** A `validation` block on the variable (emptiness,
  length or range, shape, allowed values — `type` already enforces the type) rejects a bad value at plan time with a clear error; a resource
  `lifecycle { precondition { ... } }` / `postcondition` guards assumptions about other
  objects. Prefer both to a runtime failure inside the provider, or a comment.
- **Pin versions.** `required_version` plus `required_providers` with `source` and a version
  constraint (`~> 4.0`); modules from a registry or git by version / tag, never a moving branch.
- **`for_each` over `count`** for anything with an identity: keyed addresses
  (`aws_s3_bucket.team["data"]`) survive removing an element; `count` re-indexes and replaces
  everything after it. `count` is for 0-or-1 toggles.
- **Refactor with `moved` / `removed` / `import` blocks**, not state surgery: a rename or
  `count -> for_each` change ships a `moved` block per object (`from = aws_s3_bucket.team[0]`,
  `to = aws_s3_bucket.team["data"]`) so the plan shows a move, not a destroy/create; `removed`
  (1.7+, `lifecycle { destroy = false }`) drops an object from state without destroying it.
- **Secrets never live in code, tfvars or plain outputs.** Mark secret variables and outputs
  `sensitive = true`, give them no default, and source them from a secret store data source or
  `TF_VAR_*` in the environment. `sensitive` only redacts CLI output — the value is still in
  state in plaintext, so the backend must be encrypted and access-controlled (prefer ephemeral
  values / write-only arguments where the Terraform and provider versions support them).
- **A module's inputs and outputs are its public contract.** Tightening a validation, renaming
  or retyping a variable, or dropping an output breaks callers you cannot see in this diff: grep
  the module's `source` across the repo and check open PRs (`gh pr list`) for consumers of the
  old shape — no textual conflict is not no semantic conflict (code-review's concurrent-change
  step).

## Testing

- **`terraform test` with mocked providers**, so tests need no cloud credentials and create
  nothing: `mock_provider "azurerm" {}` (1.7+), with `override_resource` / `override_data` /
  `override_module` to pin the computed values an assertion depends on.
- **Prefer `command = plan` runs** for logic and rendering — on mock providers, these are the only
  plans the agent makes; a test that applies must use mocks only. Assert on the **rendered** values — `jsondecode(azurerm_policy_definition.x.policy_rule)`
  — not on echoes of the input variables.
- **Every validation gets a failing run**: `expect_failures = [var.name]` (or the resource's
  check) proves a bad value is refused. Cover the happy path, a boundary and an error case.
- Never weaken, skip, or delete a run or assertion to go green.

## Layout

- A root or module: `versions.tf` (terraform + providers), `variables.tf`, `main.tf` (or files
  by concern), `outputs.tf`, `tests/*.tftest.hcl`; every variable and output has a
  `description` and a `type`.
- Environments are separate roots (or workspaces the repo already uses) calling shared modules.
- Never commit `.terraform/`, `*.tfstate`, `*.tfstate.*`, crash logs, saved plans, or a
  `*.tfvars` that holds a secret; **do** commit `.terraform.lock.hcl`. Check `.gitignore`.

## Pitfalls (Terraform-specific, high-value)

- **HCL that renders a different document than it reads**: `jsonencode` of a value that is
  `null` or an empty list, string-vs-list fields, interpolated JSON strings — check the plan JSON.
- **`count` keyed by a list** (reorder = replace); `for_each` over a value unknown until apply.
- **A plan that destroys or replaces** what the task meant to change — the hand-off names the
  addresses that should change so the human can check every `-/+` and `forces replacement`.
- **Unpinned providers / modules** and an uncommitted or hand-edited lock file.
- **Secrets in state, outputs, `*.tfvars` or logs** (`TF_LOG` dumps request bodies).
- **`depends_on` papering over a missing reference**; provider configuration inside a
  reusable module (pass providers from the root instead).

## Definition of done (Terraform)

`terraform fmt -recursive` applied, `init -backend=false && validate` clean, `terraform test`
green with mock providers and a failing run per validation (plus `tflint` when configured),
versions pinned and the lock file committed, no secret in code / tfvars / non-sensitive outputs,
refactors via `moved` blocks — using the repo's own commands where declared. **Nothing against a
real backend**: no plan, apply or destroy; the hand-off names the human's `terraform plan
-out=plan.out` / `terraform show -json plan.out`, the expected changes, and the rendered
documents to review.
