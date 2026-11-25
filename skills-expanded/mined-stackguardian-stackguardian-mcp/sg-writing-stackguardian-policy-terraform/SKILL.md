---
name: sg-writing-stackguardian-policy-terraform
description: Use when writing, reviewing or debugging Terraform/OpenTofu HCL for StackGuardian policies (stackguardian_policy, policies_config, enforced_on, Tirith JSON, OPA/Rego, marketplace policy templates, cost limits, approval gates, config-time workflow rules), attaching a policy to a workflow, group or connector — or when a policy applies but never blocks, blocks every plan, never asks for approval, or its scope silently disappears. Also covers resolving scopes and dependencies via the StackGuardian MCP server.
---

# Writing StackGuardian policy Terraform

## Overview

A `stackguardian_policy` is a list of rules (`policies_config`) plus a scope (`enforced_on`).
**Attachment lives only on the policy** — workflows, groups and templates have no policy
attribute. Rules are evaluated at two different moments:

| `meta.required_provider` | Evaluated | Verdict effect |
|---|---|---|
| `stackguardian/terraform_plan`, `stackguardian/infracost`, OPA (`OPA_REGO`) | in the plan step of TERRAFORM/OPENTOFU runs (also CloudFormation/Pulumi steps), before `apply`; not on drift or `plan-without-policy` runs, not in Ansible/Kubernetes steps | FAIL errors the run; APPROVAL_REQUIRED pauses before the next step |
| `stackguardian/json` (config rule) | when a workflow in scope is **created/updated** (also via Terraform) and when a run is **built** | FAIL = `403 Workflow policy (<policy>:<rule>) failed …` on create/update (live); at run build the run is refused or gated at step 0 |

The provider validates nothing and the Tirith engine fails *open* on many mistakes, so a wrong
rule usually applies cleanly and then passes everything. Provider **1.12.3**, Tirith **1.0.5**
(core; the terraform step on `main` pins 1.0.7 with the same semantics). "(live)" = reproduced against a real org. Setup (source address,
`api_uri`): **sg-writing-stackguardian-workflow-terraform**.

## Discover scope and dependencies first (StackGuardian MCP)

`enforced_on` entries are never validated, so a typo silently attaches nothing. **If the
StackGuardian MCP server is connected, take scope strings and ids from it** (rows must carry
`OrgId = "/orgs/<STACKGUARDIAN_ORG_NAME>"`; read tools only):

| Need | MCP call | Value to use |
|---|---|---|
| group scope | `search_orchestrator_resources(resourceTypes=["WORKFLOW_GROUP"], searchQuery=…)` | `SubResourceId` as-is (`/wfgrps/PROD/GCP-4jc2fd3k`) — not `ResourceId` (leaf only) |
| workflow / stack scope | `search_workflows(searchQuery=…)`, `search_stacks` | `SubResourceId` as-is (`/wfgrps/<g>/wfs/<w>`, `/wfgrps/<g>/stacks/<s>`) |
| connector scope | `search_orchestrator_resources(resourceTypes=["INTEGRATION.CLOUD"])` | `ResourceId` (`/integrations/<id>`) |
| blast radius before applying | `search_workflows(parentId="/orgs/<org>/wfgrps/<g>", count=true)`, `search_workflows(cloudIntegrationIds=[…])`, `cross_reference(targetKind="cloud_integration", targetId=…, count=true)` | how many workflows the policy will judge |
| existing policies | `search_policies(searchQuery=…)`, `get_orchestrator_resource_by_id(parentId="/orgs/<org>", resourceId="/policies/<id>")` | name collisions, current rules and `Scope` |
| marketplace policy template | `get_subscription(subscriptionTypes=["IAC_POLICY"])` | `/<owner>/<name>` + a revision that exists |
| git repo auth (OPA / git Tirith) | `search_orchestrator_resources(resourceTypes=["INTEGRATION.VCS"])`, `["SECRET"]` | `auth` = `ResourceId` / `/secrets/<name>` |
| config-rule key paths | `get_orchestrator_resource_by_id` on a real workflow | exact field names (`TerraformConfig`, `DeploymentPlatformConfig`, `RunnerConstraints`, …) |

Without MCP: literal paths from the user plus data-source existence checks — never guessed.

## Core template (runtime rule on the Terraform plan)

```terraform
resource "stackguardian_policy" "no_public_s3" {
  resource_name = "no-public-s3"  # slug: it is the id, and approvals match on it
  policy_type   = "GENERAL"       # the only value the provider can write
  description   = "Block public S3 ACLs"
  tags          = ["security"]
  enforced_on   = ["/wfgrps/${stackguardian_workflow_group.payments.id}"] # ALWAYS declare (see rule 1)
  approvers     = []                # declare, even when empty
  number_of_approvals_required = 0

  policies_config = [{
    name    = "s3_acl_not_public"   # slug, unique in the policy
    skip    = false
    on_fail = "FAIL"                # FAIL | WARN | PASS | APPROVAL_REQUIRED
    on_pass = "PASS"                # REQUIRED too: omitted -> 400 `onPass: "" is not a valid choice` (live)

    policy_vcs_config = {
      use_marketplace_template = false
      custom_source = { source_config_kind = "SG_POLICY_FRAMEWORK", source_config_dest_kind = "INLINE" }
    }

    policy_input_data = {
      schema_type = "TIRITH_JSON"
      data = jsonencode({            # only meta, evaluators, eval_expression at the top level
        meta = { version = "v1", required_provider = "stackguardian/terraform_plan" }
        evaluators = [{
          id = "acl_not_public"      # snake_case; never a prefix of another id
          provider_args = {
            operation_type               = "attribute"
            terraform_resource_type      = "aws_s3_bucket_acl"
            terraform_resource_attribute = "acl"
          }
          condition = {
            type            = "NotContainedIn"   # found value must NOT be in this list
            value           = ["public-read", "public-read-write", "authenticated-read"]
            error_tolerance = 1                  # skip plans without aws_s3_bucket_acl (0 = FAIL them)
          }
        }]
        eval_expression = "acl_not_public"       # && || ! ( ) only
      })
    }
  }]
}
```

## Rules that bite

1. **Declare `enforced_on`, `tags`, `approvers`, `number_of_approvals_required`, `description` and
   `policies_config` every time.** They are Optional+Computed without state carry-over: omit one
   while changing anything else and the provider sends `null` (the live test wiped `enforced_on` to
   `[]`, silently detaching the policy); an omitted `number_of_approvals_required` is sent as `0` —
   *all* approvers. `enforced_on = []` or no attribute = attached to **nothing**; org-wide is `["*"]`.
2. **Scope paths** are exact strings, never validated: `"*"`, `/wfgrps/<group-id>` (includes nested
   groups, stacks, workflows), `/wfgrps/<g>/wfs/<wf>`, `/wfgrps/<g>/stacks/<s>[/wfs/<wf>]`,
   `/integrations/<connector>` (every workflow deploying through it),
   `/integrationgroups/<g>[/integrations/<c>]`. Nested group: `/wfgrps/parent/child`. No trailing `/`.
3. **Condition direction:** `Contains` = found value contains yours; `ContainedIn` = found value is
   in your list (allow-list); `NotContainedIn` = deny-list. Types are case-sensitive; an unknown
   type (`In`, `Exists`, `StartsWith`, `NotRegexMatch`) fails every input.
4. **`error_tolerance`** (inside `condition`): 0 fails plans that lack the resource type, 1 skips
   them, 2 also skips resources missing the attribute. A fully skipped rule **passes**.
5. **Terraform plan actions are `create`, `update`, `delete`, `no-op`, `read`** — never `apply` or
   `destroy`. The provider docs' `NotEquals "apply"` approval example never fires.
6. **APPROVAL_REQUIRED** needs `approvers` + `number_of_approvals_required` on the policy (`0` =
   all approvers). A runtime approval pauses before the *next* step, so plan-only runs never pause.
   Approvals match on the policy's id: keep `resource_name` a slug, don't set a different `id`, and
   never rename a policy that uses APPROVAL_REQUIRED (the id stays, the match breaks).
7. **Config rules** must be `stackguardian/json` + `operation_type = "get_value"` + a `key_path`
   rooted at a workflow field (`TerraformConfig.managedTerraformState`, `Tags`, `WfType`,
   `DeploymentPlatformConfig.*.config.integrationId`, …). Any other `required_provider`
   (`sg_workflow`, `sg_stack`, `kubernetes`, none) ends in "Tirith run errored" → `on_fail` in the
   terraform step — it **blocks every Terraform/OpenTofu run in scope**. `sg_workflow`/`sg_stack`
   with a workflow `key_path` are also picked up at config time and always fail there (Tirith has no
   `sg_stack` provider; `sg_workflow` ignores `key_path`): with `FAIL`, every workflow create/update gets 403.
8. **OPA** needs `additional_config = jsonencode({ opaQuery = "<package>.<bool_rule>" })` (no `data.`
   prefix) — without it every Rego policy passes. The provider cannot read it back: the first apply
   ends in *inconsistent result* (tainted); `terraform untaint`, then use
   `lifecycle { ignore_changes = all }` and change the policy only with `-replace`.
   **Not** `ignore_changes = [policies_config]`: any later update then re-sends the rules from state
   and wipes `opaQuery` server-side (live).
9. **Only three top-level keys** in a Tirith document (`meta`, `evaluators`, `eval_expression`),
   integers rather than floats, `jsonencode` for `data`, `schema_type = "TIRITH_JSON"` for inline Tirith.
10. **A policy in scope also blocks Terraform:** a failing config rule makes `terraform apply` of
    the affected `stackguardian_workflow_*` resources fail with 403.

## Quick reference

| Need | Use |
|---|---|
| Block a resource setting | `terraform_plan` / `attribute` + `NotContainedIn` / `NotEquals`, tolerance 1 |
| Required tags | `attribute` on `tags` (or `tags_all`) + `Contains "<key>"` (key) or `Contains { K = "v" }` (pair) |
| Restrict region | `provider_config`, `attribute = "region"`, `ContainedIn [...]` — one evaluator per registry (`registry.terraform.io/hashicorp/aws` for Terraform, `registry.opentofu.org/hashicorp/aws` for OpenTofu), tolerance 2, joined with `&&`; only literal regions are checked |
| Count cap | `count` + `LessThanEqualTo N` |
| Monthly cost cap | `stackguardian/infracost`, `total_monthly_cost`, `resource_type = ["*"]`, `LessThanEqualTo 500` |
| Approval on deletes | `action`, type `"*"`, `NotContainedIn ["delete"]`, `on_fail = "APPROVAL_REQUIRED"` |
| Config guardrail | `stackguardian/json`, `get_value`, `key_path`; e.g. managed state = `is_custom \|\| uses_managed_state` (tolerance 1 on the managed key — see `examples/config_rules.tf`) |
| Scope an existing group/workflow | a literal/local path (`local.net = "platform/networking"` → `"/wfgrps/${local.net}"`), with `data "stackguardian_workflow_group" { id = local.net }` as a plan-time existence check. Don't use `data.<group>.id` in the path: it is only the leaf for nested groups (live) |
| Marketplace rule | `policy_vcs_config = { use_marketplace_template = true, policy_template_id = "/<owner-org>/<name>:<n>" }` |
| Git Tirith | `SG_POLICY_FRAMEWORK` + git kind; the file must be `<working_dir>/tirith.json`; runtime only |
| Warn-only rollout / disable | `on_fail = "WARN"` / `skip = true` (there is no active flag) |
| Import | `terraform import stackguardian_policy.x <policy-id>` |

## Common mistakes

| Mistake | What happens |
|---|---|
| `schema_type = "TIRITH_FORMAT"` / other invented enums | Apply error: `… is not a valid …` |
| Org-wide by listing groups | Misses new groups; use `["*"]` |
| `eval_expression = "a and b"` | Becomes an undefined symbol → **silent pass** |
| Ids `acl-ok` and `acl-ok-2` | Prefix collision → `final_result = -1`, treated as a pass: the longer id's evaluator is silently ignored |
| `error_tolerance = 0` on a type-specific rule, group-wide | Every plan without that type FAILS |
| `on_fail = "APPROVAL_REQUIRED"` without approvers | The run pauses and anyone with approve permission can release it |
| `required_provider = "stackguardian/sg_workflow"` (or `sg_stack`, `kubernetes`) | FAILs the terraform step of every run in scope; with a workflow `key_path` also 403s every workflow create/update (rule 7) |
| Required tag as `terraform_resource_attribute = "tags.CostCenter"` with tolerance 2, or with type `"*"` | A missing key is "attribute not found" (severity 2): tolerance 2 skips it, so the rule never fails; with `"*"` and tolerance 1 every untaggable resource fails. Use one type per evaluator with tolerance 1, or `tags` + `Contains "CostCenter"` |
| `policies_config { ... }` block, or a raw HCL object as `data` | Syntax / type error: `policies_config = [{ ... }]`, `data = jsonencode({ ... })` |
| `stackguardian_policy { data = jsonencode({...}) }` (pre-1.x form, still in the provider's onboarding guide asset) | Unsupported argument; use the typed attributes |
| `severity`, a stage (`PRE_PLAN`, `PRE_APPLY`), per-rule approvers, nested `all_of`/`any_of` | Not part of a policy: severity/stage keys are ignored, nested shapes are not read. Enforcement is only `on_fail`/`on_pass`; approvers are policy-level |
| `{{ var.x }}` placeholders in the document | Never filled; the plan step crashes (even with `on_fail = "WARN"`) |
| OPA `opaQuery = "data.main.allow"` or `main.deny` | KeyError / non-boolean → on_fail |
| `policy_template_id = "/stackguardian/x:latest"` | Resolved per run; pin a number |
| `policy_type = "FILTER.INSIGHT"` | Provider always writes GENERAL → inconsistent result |
| `policies_config = []` (a policy without rules) | Inconsistent result, tainted (live) — a policy needs at least one rule; disable with `skip = true` |
| `resource_name` of a policy that already exists | `409 Policy ID not unique` (from code) — `terraform import` it instead |
| Floats like `value = 99.5` in the document | The create stores raw floats and can 409 (unverified); use integers |

## References

- `references/tirith.md` — Tirith 1.0.5: providers, operation types, conditions, tolerance and skip
  semantics (incl. the skip-erasure bug), `eval_expression`, config-time key paths, verified recipes.
- `references/sources-and-lifecycle.md` — inline / git / OPA / marketplace sources, scope
  resolution, approvals, provider round-trip behaviour, import, destroy, error catalog.
- `references/schema.md` — exact `stackguardian_policy` schema (provider 1.12.3).
- `examples/*.tf` — validated with `terraform`/`tofu validate`, applied live, and every Tirith
  document executed against Tirith 1.0.5 with passing and failing sample plans (`examples/README.md`).
