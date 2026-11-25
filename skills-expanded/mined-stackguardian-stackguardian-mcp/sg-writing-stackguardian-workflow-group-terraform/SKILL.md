---
name: sg-writing-stackguardian-workflow-group-terraform
description: Use when writing, reviewing or debugging Terraform/OpenTofu HCL for StackGuardian workflow groups (stackguardian_workflow_group) — nested groups, group ids vs display names, referencing a group from workflows, policies, chaining or runtime references, importing existing groups — or when a group create fails with "Workflow Group ID not unique", a nested group fails to create, a group has a random suffix, or destroy fails with "Workflow Group not empty".
---

# Writing StackGuardian workflow group Terraform

## Overview

A workflow group is a folder for workflows and stacks and the usual unit of access control.
Groups nest with `/`. Provider `StackGuardian/stackguardian` **1.12.3**; setup (source address,
`api_uri`) is in **sg-writing-stackguardian-workflow-terraform**. Facts marked **(live)** were
reproduced against a real org.

## Core pattern

```terraform
resource "stackguardian_workflow_group" "platform" {
  id            = "platform"                 # set it: the route id everything else uses
  resource_name = "Platform"                 # display name, free text
  description   = "Shared platform infrastructure" # <= 255
  tags          = ["platform"]               # <= 10; never tags = [] on a group (inconsistent result)
}

resource "stackguardian_workflow_group" "networking" {
  id            = "${stackguardian_workflow_group.platform.id}/networking" # nested: "platform/networking"
  resource_name = "Networking"               # leaf display name (live)
}

resource "stackguardian_workflow_git" "vpc" {
  workflow_group_id = stackguardian_workflow_group.networking.id # bare id, full path when nested
  # ...
}
```

## Discover existing groups first (StackGuardian MCP)

If the StackGuardian MCP server is connected, list groups before creating or referencing one:
`search_orchestrator_resources(resourceTypes=["WORKFLOW_GROUP"], searchQuery="<name>",
fields=["ResourceId","ResourceName","SubResourceId","ParentId","OrgId"])`.

- **`SubResourceId`** is the full path: `/wfgrps/PROD/GCP-4jc2fd3k` → `workflow_group_id =
  "PROD/GCP-4jc2fd3k"`, import id `PROD/GCP-4jc2fd3k`, policy scope as-is. `ResourceId` is only the
  leaf; `ResourceName` is the display name (ids often carry random suffixes).
- An id you plan to create that already exists → import it instead (create would 409).
- `search_workflows(parentId="/orgs/<org>/wfgrps/<path>")` shows what lives in a group before you
  delete or re-scope it.
- Check `OrgId = "/orgs/<STACKGUARDIAN_ORG_NAME>"`; use read tools only. Without MCP: ask for the id and
  add a `data "stackguardian_workflow_group"` existence check.

## Ids

- `id` set → used verbatim (slug `^[A-Za-z0-9_-]+$`; a nested id is `parent/child`). Changing it
  replaces the group **and every workflow referencing it**: `workflow_from_template` workflows are
  destroyed and recreated (SG-managed state and run history lost), `workflow_git` ones end in
  *inconsistent result* and keep the old group non-empty. Treat group ids as permanent.
- `id` omitted → derived from `resource_name`: kept as-is when slug-shaped, otherwise lowercased
  with a random suffix (`"Platform Team"` → `platform-team-x7k2lm9q4n1d`). Always set `id` when the
  name is not a slug.
- Nested without `id`: `resource_name = "${parent.id}/networking"` also works, but the full path
  becomes the display name (live). Prefer the `id` + leaf `resource_name` form above. Without `id`,
  any `/` in `resource_name` means nesting (`"Dev/Test"` looks for a parent `Dev` → 409); with `id`
  set, the display name may contain `/`.
- The parent must exist first; referencing `parent.id` orders creation. The dashboard stops at a
  depth of 10.
- Groups created in the dashboard often have ids like `gitops-y8pf2mb1` (name + random suffix):
  look them up by id, never assume id = name.

## How other resources reference a group

| Where | Form |
|---|---|
| `workflow_group_id` on workflows | `stackguardian_workflow_group.x.id` → `platform/networking` (resource, or a literal/local full path — never `data.<group>.id` for a nested group, see below) |
| `stackguardian_policy.enforced_on` | `"/wfgrps/${stackguardian_workflow_group.x.id}"` — covers nested groups, stacks and workflows below; no trailing slash |
| `mini_steps.wf_chaining.*.workflow_group_id` | bare id (`platform/networking`) |
| `${workflow::<group>.<wf>.outputs...}` run-time reference | bare id, `/` kept; in HCL escape the `$`: `"$${workflow::platform/networking.vpc.outputs.vpc_id.value}"` |
| `data "stackguardian_workflow_outputs"` | `workflow_group = stackguardian_workflow_group.x.id` |
| role `allowed_permissions` paths | group **ids** (full path when nested), not `/wfgrps/...` and not display names; the values are regexes full-matched against the group path, so `["platform"]` does not cover `platform/networking`: grant both `platform` and `platform/.*` (the form StackGuardian's own Terraform modules use, from code), or list the children. The lists are positional: `<wf>`, `<wfRun>` … lists in the same permission need one entry per `<wfGrp>` entry (pad with `".*"`) |
| import id | `platform/networking` |

A workflow whose `workflow_group_id` names a group that does not exist is **still created**: the
server auto-creates a *top-level* group named after the last path segment (description
`Automatically created by SG when creating a workflow`, tags `sg-created`, `workflow`), and for a
nested path the workflow is stored under a parent path that has no group. If a top-level group of
that name already exists, the create fails with 500 `Workflow Group does not exist and cannot be
created.` Always reference the group resource (or a literal full path you know exists).

## Lifecycle

| Action | Behaviour |
|---|---|
| Create with an id that already exists | 409 `Workflow Group ID not unique` (live). The provider docs claim it adopts the group — it does not. Import it instead |
| Create that fails with a **400** (description > 255, 11 tags, non-slug `id`, reserved name) | the provider reads the group named by `resource_name` and, if one exists, silently **adopts** it into state — a later destroy deletes a group you never created. Fix the 400 cause; check the plan when names may collide |
| Reusing the id of a group moved in the dashboard | 409 `A resource used to exist with the same id but was moved to …` — the provider cannot pass `replace-moved-resource`; pick another id |
| Change `resource_name` | in-place rename |
| Change `id` | replace (the old group must be empty to delete) |
| Omit `description`/`tags` while changing anything else | they are **cleared** (Optional+Computed without state carry-over; live plan) — removing them alone shows no diff until some other attribute changes. Keep them declared when the group has values; to clear tags, omit them and change another attribute in the same apply |
| `tags = []` | *Provider produced inconsistent result after apply*, group tainted (live) — omit `tags` for a group without tags. `description = ""` is fine |
| Delete | only when empty: `Workflow Group not empty` (400) while any workflow, stack or child group remains. Terraform orders children first within one config (live); workflows created outside Terraform block it. Right after deleting the children the check is eventually consistent — retry |
| Move a workflow between groups | no in-place move: `terraform apply -replace` (new workflow, managed state lost) or move it in the dashboard and re-import at the new address (workflow skill, lifecycle §4) |
| Group deleted outside Terraform | dropped from state on refresh and silently re-created on the next apply |
| Import | `terraform import stackguardian_workflow_group.networking platform/networking`, or an `import` block + `terraform plan -generate-config-out=generated.tf` to get its current name/description/tags written for you |
| Read an existing group | `data "stackguardian_workflow_group" "x" { id = "platform/networking" }` fails at plan with `Unable to read workflow group.` when it does not exist — use it as an **existence check**. It returns `description` and `tags`, but its `id` is only the **leaf** (`networking`) for nested groups and `resource_name` is null (live). Build references from the path you looked up (`local.net = "platform/networking"`), not from `data.x.id` |

Limits: `resource_name` ≤100 (reserved names such as `wfgrps`, `policies`, `secrets`, `logs`,
`outputs` are rejected; the check skips `id`, so `id = "listall"` is created but unreachable at
its own route — from code), description ≤255, tags ≤10 (the dashboard strips every non-word character — `-`, `.`, `:` — from tags it edits;
Terraform keeps them). The server has no nesting-depth limit; the dashboard stops at 10.

## Common mistakes

| Mistake | What happens |
|---|---|
| `resource_name = "Platform Team"` and no `id` | Random-suffixed id; every reference by name breaks |
| `workflow_group_id = "/wfgrps/platform"` | Wrong: bare id only (`/wfgrps/` is the policy form) |
| `enforced_on = ["/wfgrps/platform/"]` | Trailing slash: matches nothing |
| `enforced_on = ["/wfgrps/platform/wfgrps/networking"]` | Not a scope (that shape is only the child-create URL / dashboard tree key): use `/wfgrps/platform/networking` |
| `workflow_group_id = data.stackguardian_workflow_group.net.id` (nested) | Resolves to the leaf `networking`: wrong/auto-created top-level group (live data-source behaviour) |
| Hard-coding `workflow_group_id = "platfrom"` | Server auto-creates a junk group `platfrom` |
| Nested group before its parent exists | 409 `Workflow Group does not exist` — reference `parent.id` |
| Deleting a group that still has dashboard-created workflows | 400 `Workflow Group not empty` |

Worked example (validated with `terraform validate` and `tofu validate`, applied live):
`examples/groups.tf`.
