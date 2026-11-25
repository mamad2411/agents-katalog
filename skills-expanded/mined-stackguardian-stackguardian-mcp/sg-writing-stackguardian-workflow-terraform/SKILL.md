---
name: sg-writing-stackguardian-workflow-terraform
description: Use when writing, reviewing or debugging Terraform/OpenTofu HCL for StackGuardian workflows (stackguardian_workflow_git, stackguardian_workflow_from_template, workflow templates/revisions, CUSTOM Ansible/Helm/kubectl/CloudFormation steps) — vcs_config, terraform_config, connectors, secrets in env vars, runners and stackguardian_runner_group, schedules, VCS triggers, notifications, chaining, workflow outputs — or when a workflow applies but every run fails, or when migrating old `stackguardian_workflow` + `data = jsonencode(...)` code. Also covers looking up the org's connectors, secrets, runner groups and templates via the StackGuardian MCP server.
---

# Writing StackGuardian workflow Terraform

## Overview

Provider `StackGuardian/stackguardian` **1.12.3** (Terraform Plugin Framework). Every nested
structure is an **attribute** (`x = {...}` / `x = [{...}]`), never a block. Facts were verified on
1.12.3; on a newer provider re-check rules 11 and 12 first (they are provider bugs). The provider
validates almost nothing, so mistakes show up as: a 400 at apply, *"Provider produced
inconsistent result after apply"* (the resource is tainted when this happens on create), or a
workflow that is created and then
fails every run. Everything below was checked against provider, api, core, run-controller
and step-template source, and the traps marked **(live)** were reproduced against a real org.

Groups: **sg-writing-stackguardian-workflow-group-terraform**. Guardrails/approvals on plans:
**sg-writing-stackguardian-policy-terraform**.

## Setup

```terraform
terraform {
  required_providers {
    stackguardian = {
      source  = "registry.terraform.io/StackGuardian/stackguardian" # full address: the OpenTofu registry has no copy
      version = "~> 1.12.3"
    }
  }
}
provider "stackguardian" {} # STACKGUARDIAN_API_KEY, STACKGUARDIAN_ORG_NAME, STACKGUARDIAN_API_URI
```

`api_uri` has **no default** (live): set `https://api.app.stackguardian.io` (EU) or
`https://api.us.stackguardian.io` (US). A key from the other region returns 401 (per the provider
docs).

## Which resource

| Want | Resource |
|---|---|
| Workflow whose IaC is in your git repo | `stackguardian_workflow_git` (`wf_type` TERRAFORM / OPENTOFU / CUSTOM) |
| Workflow from a template revision **owned by your org** | `stackguardian_workflow_from_template` (templates of other orgs, incl. the marketplace, fail — rule 11) |
| Reusable definition many workflows share | `stackguardian_workflow_template` + `stackguardian_workflow_template_revision` |
| Ansible / Helm / kubectl / CloudFormation / Terragrunt | `wf_type = "CUSTOM"` + `wf_steps_config` (there is no ANSIBLE/HELM wf_type) |
| Read a workflow's Terraform outputs | `data "stackguardian_workflow_outputs"` |

`stackguardian_workflow`, `wfgrp`, `data = jsonencode({...})`, `GitHubComSync`, `is_active`,
`cache_config`, `tfvars_file_path` and `enforced_policies` do not exist in this provider.

## Discover dependencies first (StackGuardian MCP)

Connectors, secrets, runner groups, groups and other workflows must already exist, and wrong ids
only fail at run time. **If the StackGuardian MCP server is connected, look every one up before
writing HCL** and offer the user the real options (full mapping: `references/discovery.md`):

| Dependency | MCP call | Value to use |
|---|---|---|
| cloud / VCS connector | `search_orchestrator_resources(resourceTypes=["INTEGRATION.CLOUD"])` / `["INTEGRATION.VCS"]` | `ResourceId` (`/integrations/<id>`) → `integration_id` / `auth`; `ResourceType` minus `INTEGRATION.` → `kind` / `source_config_dest_kind`. Never the `ResourceName` |
| secret | `search_orchestrator_resources(resourceTypes=["SECRET"])` | `/secrets/<name>` → `"$${secret::<name>}"`; missing ones must be created first (`sg-manage-secrets` skill) |
| private runner group | `search_orchestrator_resources(resourceTypes=["RUNNER"])` | last segment of `/runnergroups/<id>` → `runner_constraints.names` |
| workflow group | `search_orchestrator_resources(resourceTypes=["WORKFLOW_GROUP"])` | `SubResourceId` minus `/wfgrps/` → `workflow_group_id` (`ResourceId` is only the leaf) |
| other workflows, their outputs | `search_workflows`, `get_workflow_outputs` | `SubResourceId` `/wfgrps/<g>/wfs/<w>` → chaining, `${workflow::…}`, import id |
| own / step templates | `search_marketplace_templates`, `get_marketplace_template_by_id`, `get_subscription` | `/<org>/<name>:<n>`, input schema defaults, draft status |

Rows must carry `OrgId = "/orgs/<STACKGUARDIAN_ORG_NAME>"`; use read tools only (don't create via
MCP what Terraform should own); keep the data sources in the HCL as the plan-time check. Without
MCP: data sources + ask the user — never invent ids.

## Core template

```terraform
data "stackguardian_connector" "github" { id = "github_com" } # GITHUB_COM connector id is always github_com
data "stackguardian_connector" "aws"    { id = "aws-prod-oidc" }

resource "stackguardian_workflow_git" "payments_api" {
  id                = "payments-api"                           # REQUIRED slug; changing it replaces the workflow (new state!)
  resource_name     = "Payments API"                           # display name; omit it and the server invents a random one
  workflow_group_id = stackguardian_workflow_group.prod.id    # bare id, "payments/prod" when nested; never change in place
  wf_type           = "TERRAFORM"                              # TERRAFORM | OPENTOFU | CUSTOM — immutable
  description       = "Payments API infrastructure"            # "" fails validate; omit instead

  vcs_config = {
    iac_vcs_config = {
      custom_source = {
        source_config_dest_kind = "GITHUB_COM"                 # must equal the auth connector's kind
        config = {
          repo        = "https://github.com/acme/payments-infra"
          ref         = "main"
          working_dir = "envs/prod"
          is_private  = true
          auth        = "/integrations/${data.stackguardian_connector.github.id}"
        }
      }
    }
    iac_input_data = {                                         # becomes a .tfvars.json passed to plan
      schema_type = "RAW_JSON"
      data        = jsonencode({ region = "eu-central-1", instance_count = 3 })
    }
  }

  deployment_platform_config = [{
    kind   = "AWS_OIDC"                                        # = the connector's kind
    config = { integration_id = "/integrations/${data.stackguardian_connector.aws.id}" }
  }]

  environment_variables = [
    { kind = "PLAIN_TEXT", config = { var_name = "TF_LOG", text_value = "WARN" } },
    { kind = "PLAIN_TEXT", config = { var_name = "DB_PASSWORD", text_value = "$${secret::payments-db-pass}" } }, # $$ = literal ${
  ]

  terraform_config = {
    terraform_version       = "1.5.7"                          # always set; Terraform <= 1.5.7, OpenTofu e.g. "1.11.x"
    managed_terraform_state = true                             # server default is FALSE; true requires NO backend block in the repo
    approval_pre_apply      = true
    drift_check             = true
    drift_cron              = "0 2 * * ? *"                    # 6-field EventBridge cron, UTC
  }

  approvers                    = ["alice@acme.com", "bob@acme.com", "carol@acme.com"] # lowercase
  number_of_approvals_required = 2                                                    # 0 = ALL approvers

  runner_constraints = { type = "shared" }
  tags               = ["payments", "prod"]
}
```

## Rules that bite

1. **Path vs bare ids.** `integration_id`, `auth`: `/integrations/<id>` (or `/secrets/<name>`).
   `workflow_group_id`, `runner_constraints.names`, `wf_chaining.*`: bare ids. A bare connector id
   applies fine and every run fails with `Connector <id> does not exist`. Kinds must match the
   connector: `kind = data.stackguardian_connector.aws.settings.kind` guarantees it.
2. **Secrets:** `PLAIN_TEXT` + `text_value = "$${secret::<name>}"` (the dashboard's form;
   `VAULT_SECRET` + `secret_id = "/secrets/<name>"` also works at run, although the 1.12.3 docs
   call `secret_id` "Not used"; `SECRET_VALUE` from older docs is a 400). The whole value must be the
   reference. Nothing checks the secret at apply — a missing one fails the run. The provider has
   no secret resource; create secrets out of band.
3. **Terraform > 1.5.7** is rejected on create and update (`Terraform 1.9.0 is above the highest
   managed version (1.5.7)`, live). OpenTofu has no cap. See `references/execution.md` for escape hatches.
4. **Write every value the server normalizes** or you get *inconsistent result* (live):
   `terraform_config = {}` (server stamps `1.5.7`), mixed-case approver emails (lowercased).
   Nested typos (`is_privte`, `terraform_verison`) pass `terraform validate` and are silently
   dropped (live) — copy attribute names from `references/schema.md`.
5. **Workflows start inactive** and activate on their first run — including a drift or schedule
   tick (billed). Outputs are unavailable until then. Creating a workflow never runs it.
6. **Schedules auto-apply.** `user_schedules` cannot carry run inputs in this provider, so each
   tick on a TERRAFORM/OPENTOFU workflow is a full `apply` unless `approval_pre_apply = true`.
7. **Approvals:** `approval_pre_apply` with `approvers = []` lets *anyone* approve; `0` with a list
   means *everyone*; a plan with no changes completes without asking; any rejection cancels the run.
8. **Destroying the resource does not destroy infrastructure.** It deletes the workflow, its runs,
   schedules and SG-managed state. Run a destroy run first (see `references/lifecycle.md`).
9. **Clearing values on `workflow_git`:** removing `tags`/`approvers` *keeps* them (`[]` clears);
   removing `description`, `environment_variables`, `mini_steps`, … clears them. **Never just delete
   `user_schedules`** — the schedules keep firing: set it to `[]` and apply (server deletes them,
   provider reports a one-time *inconsistent result*, live), then remove the attribute.
10. **CUSTOM** needs a non-empty `wf_steps_config` (else 201 then every run: `Workflow Steps not set`)
    and must not have `terraform_config`.
11. **Provider 1.12.3 bug:** `workflow_from_template` with a template owned by *another* org (every
    `/stackguardian/...` marketplace template) fails at apply with `Could not read template
    revision … 401 Unauthorized` (live). Use an own-org copy of the template
    (`examples/own_template.tf`) or `workflow_git` on the template's repo.
12. **Template upgrades take two applies** when the new revision is created in the same config:
    publish the revision first, then point `iac_template_id` at it (same apply → *inconsistent
    final plan*, live).

## Quick reference

| Topic | Rule / value |
|---|---|
| Template id | `iac_template_id = "/<your-org>/<template>:<rev>"`; bare `name:rev` 404s, other orgs' templates 401 (live). The `stackguardian_workflow_template_revision` **data source** is the opposite: bare `<template>:<rev>` (a `/<org>/` prefix returns a misleading 403) |
| Inherit from template | Omit the attribute. Suppress with top-level `[]`/`{}`; nested `terraform_config` lists/strings **cannot** be suppressed (live) |
| VCS kinds | `GITHUB_COM`, `GITHUB_APP_CUSTOM`, `GITLAB_COM`, `BITBUCKET_ORG`, `AZURE_DEVOPS`, `AZURE_DEVOPS_SP`, `GIT_OTHER` (auth = `/secrets/<n>` only) |
| Cloud kinds | `AWS_STATIC`, `AWS_RBAC`, `AWS_OIDC`, `AZURE_STATIC`, `AZURE_OIDC`, `GCP_STATIC`, `GCP_OIDC` — max 1 entry |
| Private runner | `runner_constraints = { type = "private", names = ["<runner group id>"] }` (exactly one, no `/runnergroups/`) |
| Step template ids | `/stackguardian/ansible:18`, `kubernetes:13`, `cloudformation:2`, `terragrunt:1`, `terraform:22` |
| Cron | `min hour dom month dow year`, `?` in dom or dow, UTC. 5-field → 400 |
| Engine | Terraform ≤ 1.5.7 → `wf_type = "TERRAFORM"`; newer → `wf_type = "OPENTOFU"` with an OpenTofu version ≥ 1.6 (`"1.10.x"`) — a bare version < 1.6 selects the Terraform binary whatever the `wf_type` |
| Import | `terraform import stackguardian_workflow_git.x <group-id>/<workflow-id>` (nested group ok) |
| Limits | tags 10, env vars 20, steps 10, lifecycle step lists 5 each, schedules 10, description 512 |
| Outputs | `jsondecode(data.stackguardian_workflow_outputs.x.data["vpc_id"]).value` |

## Common mistakes

| Mistake | What happens |
|---|---|
| `stackguardian_workflow` + `data = jsonencode(...)` | Resource does not exist in 1.x |
| `wf_group = "web"` / no `id` | Validate error: `workflow_group_id` and `id` are required |
| `vcs_config { ... }` block syntax | Syntax error — attributes only |
| `iac_vcs_config.use_marketplace_template` | Not an attribute; the resource type decides |
| `iac_template_id = "my-tpl:1"` | 404 `Template my-tpl:1 of type IAC does not exist` |
| `iac_template_id = "/stackguardian/aws-s3-demo-website:16"` | 401 at apply (provider bug, rule 11) |
| `integration_id = data.stackguardian_connector.aws.id` | Applies; every run fails `Connector aws does not exist` |
| `terraform_version = "1.9.0"` with `wf_type = "TERRAFORM"` | 400 `… above the highest managed version (1.5.7)` on create and on update |
| Repo has `backend "s3"` and `managed_terraform_state = true` | Every plan fails `Found more than 1 terraform state backend blocks` |
| `pre_plan_hooks = ["tflint"]` | No tflint/jq/cloud CLIs in the image (busybox `sh`), and hooks start outside the repo: `cd "$MOUNTED_IAC_SOURCE_CODE_DIR" && …`, install tools via curl or use a step |
| Changing `workflow_group_id` of a `workflow_git` | Inconsistent result; workflow stays in the old group (live). Use `-replace` |
| `terraform_config = {}` / `approvers = ["Bob@X.com"]` | Inconsistent result, resource tainted on create (live) |
| Typo in a nested attribute (`is_privte = true`) | Passes validate, silently dropped → 400 `isPrivate required` or a server default (live) |
| Deleting the `user_schedules` attribute | Schedules keep firing applies; set `[]` first (rule 9) |
| `cmd_override` on a shared runner | The string is passed as the ECS container command, which expects a list — the run is expected to fail (unverified); use it on private runners |
| `user_schedules` on a prod TERRAFORM workflow without approval | Unattended `apply` every tick |
| `email.completed` / `email.cancelled` recipients | Stored, but the run controller only emails on errored, approval_required, drift_detected |
| Step-level `environment_variables` in `wf_steps_config` | Stored, never injected — put variables at workflow level |
| `terraform destroy` to tear down infra | Infra orphaned, state deleted |
| Destroying a published (`is_public = "1"`) template revision | Refused until an applied `deprecation` has an `effective_date` in the past — epoch **milliseconds** as a string (live; `references/sources-and-templates.md` §3) |

## References (read when needed)

- `references/sources-and-templates.md` — VCS kinds/auth matrix, templates, inheritance, upgrades, own templates/revisions, custom runtime images.
- `references/execution.md` — wf_type rules, versions, managed state, inputs, hooks, lifecycle steps, CUSTOM steps and their inputs, env vars and runtime references, connectors, runners (incl. managing connector / runner group resources), sizing, approvals.
- `references/automation-and-outputs.md` — schedules, drift, VCS triggers, notifications, webhooks, chaining, outputs.
- `references/lifecycle.md` — create/update/clear semantics, replacement, import, destroy, error catalog.
- `references/schema.md` — exact attribute tree of every workflow-side resource and the runner group (provider 1.12.3).
- `examples/*.tf` — validated with `terraform validate` and `tofu validate`; see `examples/README.md`.
