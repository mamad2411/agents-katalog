---
name: terraform-standards
description: "Sets house conventions for Terraform on AWS: module layout, typed variables, S3 backend with native locking, per-environment backends, pinning. Use when scaffolding a Terraform project, adding a backend or pinning versions. Not for plan review (use terraform-review) or IAM (use aws-iam-boundaries)."
license: MIT
---

# Terraform Standards

Every account id, bucket, key alias and role on this page is a placeholder (`111111111111`,
`<org>`, `<team>`). A wrong backend value does not error; it writes state somewhere else, so
copy real values from a project known to work, never from an example.

Without a checkout (web), apply these conventions to the HCL or backend files the user pastes.

## Module layout

| Kind | Contains | Has a backend? | Named |
| --- | --- | --- | --- |
| **Root module** | The composition for one environment of one component. Calls child modules, supplies environment values. | Yes — exactly one state file. | `infrastructure/terraform/`, or `environments/<env>/` |
| **Child module** | Reusable resource logic with no environment knowledge. | No. | `modules/<name>/` |

A child module that switches behaviour on an environment name is a root module wearing the
wrong hat. Pass the behaviour in as a variable; the caller knows which environment it is.

Inside a root module, split by file so a reader can find things without grep:

```
infrastructure/terraform/
├── versions.tf      # terraform { required_version, required_providers, backend "s3" {} }
├── providers.tf     # provider blocks, default_tags
├── variables.tf     # every input, typed and described
├── locals.tf        # derived names and tag maps
├── main.tf          # the resources and module calls
├── outputs.tf       # what other stacks consume
└── backends/
    ├── dev.s3.tfbackend
    ├── staging.s3.tfbackend
    └── production.s3.tfbackend
```

One state file per component per environment. A whole estate in one root module means every
plan touches everything, every apply holds one lock, and a typo in an unrelated resource
blocks the change you need.

## Variables

- **Type and describe every variable.** `any` defers the shape error from plan time to apply
  time. tflint's default ruleset already fails an untyped variable; `terraform_documented_variables`
  is off by default, so enable it in the repo's `.tflint.hcl`.
- **No default on anything that distinguishes environments** (`environment`, `account_id`,
  `vpc_id`, sizing). A default on `environment` means a forgotten `-var-file` plans cleanly
  against the wrong one.
- **Defaults are fine on genuinely optional inputs** — a retention period, an `enable_x` flag
  that is off, an empty tag map.
- **Use `validation` blocks for constraints you would otherwise write in a comment.**

```hcl
variable "environment" {
  type        = string
  description = "Deployment environment. Drives naming, sizing and tagging."

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "environment must be one of: dev, staging, production."
  }
}
```

Secrets: mark them `sensitive = true` and keep real values out of `tfvars`. Anything a data
source reads lands in state; where the provider offers them, prefer write-only arguments
(for example `password_wo`) fed from an ephemeral resource, which are never persisted. Each
pairs with a version argument (`password_wo_version`): Terraform cannot diff a value it never
stored, so bump the version to push a new one. Path
conventions and the state caveat are owned by `dev-standards:secrets-management`.

## Outputs

An output is an API: anything you export, something else can come to depend on.

- Export only what another stack or a human consumes, each with a `description`.
- `sensitive = true` redacts CLI output only; the value is still in state.
- Prefer publishing cross-stack values to a parameter store over having consumers read your
  remote state. A remote state read couples the consumer to your resource names and grants it
  every other value in your state file.

## State backend

State lives in S3: a private, versioned bucket, SSE-KMS with a customer-managed key, and
S3-native locking. Bucket versioning is the only undo for a corrupt or truncated state write.

```hcl
# backends/dev.s3.tfbackend
region       = "us-east-1"
bucket       = "<org>-tfstate-dev"
key          = "<org>/aws/<team>/dev/<project-name>/backend.tfstate"
encrypt      = true
use_lockfile = true
kms_key_id   = "alias/<org>-terraform-state"

assume_role = {
  role_arn = "arn:aws:iam::111111111111:role/<terraform-state-role>"
}
```

The backend block in `versions.tf` stays partial (`backend "s3" {}`), and each environment
initialises with its own file:

```
terraform init -input=false -reconfigure -backend-config=backends/dev.s3.tfbackend
```

- **`-input=false`**: `bucket` and `key` are required, so a missing `-backend-config` makes an
  interactive `init` prompt for them. In CI and scripts, fail instead of prompting.
- **`-reconfigure`** when switching environments in one working directory. Without it, `init`
  stops with "Backend configuration changed" and suggests `-migrate-state`; following that hint
  copies one environment's state into another's key.
- **The real quiet failure is a wrong `key`, not a missing one.** A key that points at an empty
  object gives you a plan that creates the whole environment again. A plan that is all
  creates for an environment that already exists is a stop, not a review comment.
- A root module with **no** `backend` block at all uses local state. `versions.tf` is where the
  backend block lives, so it is the first file to copy when scaffolding.

### The key path is the only thing that varies per project

Bucket, KMS alias, region and role are properties of the *environment*; the `key` belongs to
the *project*. When scaffolding, copy the backend files from a working project and change only
the `key`.

- **Spell each environment one way everywhere.** A key that says `prod` in one project and
  `production` in another creates a second, empty state file, not an error. Name the backend
  file with the same word the key uses.

### Locking

Use S3-native locking: `use_lockfile = true` writes a lock object beside the state. The
`dynamodb_table` argument is deprecated and `init` warns when it is set. Keep it only while
migrating an existing backend: with both set, Terraform takes both locks, so set
`use_lockfile = true`, apply once from every pipeline that uses the state, then remove
`dynamodb_table` and the table. Native locking needs a Terraform version that supports it;
see [references/versions.md](references/versions.md).

A lock that is never contended looks identical to no lock at all, so check it in review.

### State is sensitive

Everything the configuration touches is in state in plaintext. Grant read access to the state
bucket and its KMS key as seriously as read access to the secrets store, and remember that a
role that can *plan* can read state.

## Workspaces versus a directory per environment

Use one backend file per environment, as above, not `terraform workspace`, to separate dev
from production. Workspaces share one backend: one bucket, one KMS key and one assumed role.

- Anyone who can plan dev can read production state.
- The selected workspace lives in the working directory (`.terraform/environment`) or in
  `TF_WORKSPACE`, not in the command you typed; `terraform apply` is the same keystrokes for
  either environment.
- You cannot give the pipeline a production-only identity.

Workspaces fit **ephemeral copies of one environment** — a stack per feature branch or test
run — where every copy has the same blast radius and the same credential.

## Version pinning

- **Pin the exact Terraform CLI version in CI** (the setup action's version input, or a
  `.terraform-version` file read by the version manager). A newer 1.x may write a state format
  an older one cannot read; Terraform guarantees upgrades within 1.x, not downgrades. Upgrade
  the pinned CLI deliberately, in its own change.
- **`required_version`** states the oldest CLI the configuration works with. Set its floor to
  the version that introduced the newest feature you use (native locking, `removed` blocks,
  write-only arguments); it is a floor, not a pin.
- **Constrain every provider** with `~>` in `required_providers`, including data-source-only
  ones, and **commit `.terraform.lock.hcl`**: the constraint states intent, the lock file
  records what runs. Update with `terraform init -upgrade` in its own change, and read the
  provider changelog for the resources you use.
- tflint's default ruleset fails a missing `required_version` or provider constraint and an
  unpinned module source, so the review scan catches their absence. Whether the chosen range is
  sensible is still a human call.

Current version floors and example constraints: [references/versions.md](references/versions.md).

## fmt, validate, plan

```
terraform fmt -check -recursive
terraform init -input=false -backend=false
terraform validate
terraform init -input=false -reconfigure -backend-config=backends/dev.s3.tfbackend
terraform plan -input=false -out=tfplan
```

| Command | Answers | Needs credentials? |
| --- | --- | --- |
| `fmt -check` | Is it canonically formatted? | No |
| `validate` | Types, references, required arguments consistent? | No, after `init -backend=false` downloads providers |
| `plan` | What would change in *this* state, right now? | Yes |

`fmt` and `validate` (with `init -backend=false`) belong in pre-commit. `plan` does not: it
needs credentials and a backend, and a hook that authenticates is a hook people disable.

The saved plan file contains every value in the plan, sensitive ones included, in plaintext.
Treat `tfplan` like state: keep it out of git, and store it as a pipeline artifact with the
same access control as the state bucket. Apply that same file, so what was reviewed is what
runs. Reading a plan is `terraform-review`'s job.

## No applies to shared environments from a laptop

Make it impossible, not merely discouraged. A local apply ships an unreviewed working tree,
leaves no plan artifact, and attributes the change to a person's broad session. Enforce it in
IAM:

1. Shared-environment backends assume a **state role that trusts only the pipeline identity**.
   A personal session fails on `sts:AssumeRole` before any plan runs.
2. Personal identities reach the sandbox only, where a bad apply costs a rebuild.
3. Shared environments change through a **manual gate in the pipeline**: the saved plan is the
   artifact, the gate is the approval, the job log is the audit trail.
4. Read-only inspection of shared environments stays available, so nobody reaches for a
   bigger role just to look.

## Verify

After scaffolding or changing a backend, run and check:

1. `terraform fmt -check -recursive` and `terraform validate` pass.
2. `tflint` passes with the repo's config.
3. `terraform plan` against an existing environment shows only the intended changes; all
   creates means the `key` or backend file is wrong.
4. `init` prints no deprecation warning for `dynamodb_table` once migration is done.

If you cannot run these (no CLI, no credentials, web session), say which checks remain and
hand them to the user with the exact commands above.
