---
name: sg-create-stack
description: Guided flow for creating a StackGuardian STACK (a bundle of workflows deployed together in a defined order) from a stack template via the StackGuardian MCP create_stack tool — walks the user through picking a stack template (IAC_GROUP) and revision, workflow group, stack name/description/tags/context tags, a cloud connector and environment variables (stack-wide or per workflow), then the template inputs of EACH workflow in the stack (always presenting each workflow template's defaults and the stack template's pre-wired values for review), then creates the stack. Stacks are template-only (no git mode). Use when the user wants to create/deploy a stack, deploy a stack template / template group from the StackGuardian library, or stand up a multi-workflow environment (e.g. VPC + security group + EC2 + Ansible) in one go. For a single workflow use the sg-create-workflow skill.
---

# Create Stack — Guided Flow

Create a StackGuardian stack with the `create_stack` tool on the
StackGuardian MCP server. A stack is a set of workflows created together from
a **stack template** (library templateType `IAC_GROUP`), plus the template's
**Actions** (apply / plan / destroy…) that fix the order they run in. Follow
the steps IN ORDER. Never ask the user to type IDs from memory — fetch
options with the listed tools and present choices. In user-facing messages
use plain language; never surface internal parameter names like `wfGrp`,
`templateGroupId`, `workflows[].workflow` or `iacInputs`.

There is **no git mode** for stacks: the stack template already names the
workflow templates it is made of. If the user wants to deploy their own repo
they want a workflow, not a stack — hand over to the `sg-create-workflow` skill.

**Nothing is deployed by creating a stack.** Say so. Running it is a separate
step (Step F).

## Step A — Pick the stack template and revision

1. Call `search_marketplace_templates(templateType='IAC_GROUP')` (add
   `searchQuery` if the user described what they want). Present the results;
   let the user pick one.
2. Note the chosen template's `TemplateId` in pinned `/owner/name:rev` form
   (e.g. `/acme/three-tier-web:2`) — this becomes `templateGroupId`. Always
   pin the revision; the tool refuses an unpinned id.
3. **Draft vs published.** `IsPublic` `"1"` is published, `"0"` is a
   **draft**. A draft is allowed (it is how an author tests one) but tell the
   user plainly it is unpublished, can still change, and is not for
   production; never silently pick one. (The tool repeats this as a
   `warnings` entry.)
4. Immediately call `get_marketplace_template_by_id(templateType='IAC_GROUP',
   templateId=<pinned id>)` and read `WorkflowsConfig.workflows` (a JSON
   string in search results — parse it). Each entry has an `id` (a UUID —
   this is how you address the workflow later) and
   `VCSConfig.iacVCSConfig.iacTemplateId`, the workflow template it runs.
   Some entries also carry stored `iacInputData.data` and
   `EnvironmentVariables` — the stack template's own pre-set values. Keep
   all of this for Step D.
5. Tell the user what the stack is made of: one line per workflow (template
   name + revision, and TERRAFORM/OPENTOFU vs a custom step pipeline if
   visible). The search result does NOT carry the template's `Actions`; the
   tool reads those itself at create time, so don't try to show the run
   order from search results — say the order comes from the template.

## Step B — Workflow group and naming

1. Offer exactly three ways to pick the target group — never dump or
   "recommend" arbitrary groups:
   - **Name or keyword**: resolve via
     `search_orchestrator_resources(resourceTypes=['WORKFLOW_GROUP'],
     searchQuery=<keyword>)`; on a near-miss suggest the closest match. The
     confirmed pick becomes `wfGrp` — pass EVERYTHING AFTER `/wfgrps/` in its
     `ResourceId` (the id can differ from the display name; the tool accepts
     either and translates a name, but carry the id forward — every later
     tool takes it). Nested groups (`PROD/eu-central-1`) are accepted as the
     whole path.
   - **Create a new group**: pass `createNewWorkflowGroup=true` ONLY when the
     user explicitly asks for a brand-new group. Note the platform would
     silently create a mistyped group on stack create — that is why the tool
     refuses an unknown group unless this flag is set.
   - **Browse in the dev portal**: share the workflow-groups page —
     `https://<dashboard>/orchestrator/orgs/<org>?tab=workflowGroups`
     (`<dashboard>` and `<org>` as in **No connector yet**).
   This step is mandatory — never call `create_stack` without a
   user-confirmed group.
2. Ask the user for:
   - stack name (`resourceName`, 1–100 chars; its id is the slugified name)
   - optional description (max 512 chars)
   - optional tags (max 10) and context tags (key:value pairs)
3. Optionally check for duplicates first with
   `search_stacks(searchQuery=<name>)`.

## Step C — Cloud connection and environment variables

The dashboard offers these **stack-wide** (applied to every workflow) or
**per workflow**. Ask which the user wants; default to stack-wide.

1. Cloud connector: skip if none is needed (omit `deployment`). Otherwise
   find connectors via
   `search_orchestrator_resources(resourceTypes=['INTEGRATION.CLOUD'])` (if
   none fits, see **No connector yet**) and build `deployment = {"connectorId": "/integrations/<id>"}` — only
   `connectorId` is required; the kind is resolved live. A per-workflow
   connector goes in that workflow's entry as `workflows[].deployment` and
   overrides the stack-wide one for that workflow only. Omitting both keeps
   whatever each workflow template declares.
2. Environment variables: collect each as `{varName, textValue}` or
   `{varName, secretId}` (`/secrets/<name>`), exactly one of the two.
   Stack-wide ones go in `environmentVariables`; per-workflow ones in
   `workflows[].environmentVariables`. Merge order is: the workflow
   template's own variables, then stack-wide, then per-workflow — a
   same-named variable replaces, everything else is kept (the tool carries
   the template's own variables forward; the platform would drop them).
   A stack template may already set variables on a workflow (visible in
   Step A's `EnvironmentVariables`) — show those so the user knows what they
   inherit.

## Step D — Template parameters, per workflow

This is the step that differs from a single workflow: **walk the workflows
one at a time**, in the template's order, and for EACH:

1. Call `get_marketplace_template_by_id(templateType='IAC', templateId=<that
   workflow's iacTemplateId>)` and decode `InputSchemas` (a LIST; the
   `FORM_JSONSCHEMA` entry's `encodedData` is base64 JSON Schema; walk
   `properties` — each `default` is what ships if the user says nothing).
2. Overlay the stack template's stored `iacInputData.data` for that workflow
   (from Step A) — those values win over the schema defaults, and that is
   what the tool sends too.
3. **Pre-wired inputs.** Any stored value that is a `${reference::…}` or
   `${workflow::…}` string is wired to ANOTHER workflow's output at run time
   (e.g. the security group's `vpc_id` comes from the VPC workflow). Show
   them as "filled in automatically from <workflow>" and do NOT ask for a
   value. The tool refuses to replace one with a literal; only another
   reference string is accepted, and only if the user asks for that
   deliberately.
4. **ALWAYS present every remaining input with the value that will be used
   before creating — never let one apply unseen.** Name, what it does, the
   default, whether it is required (no default = needs a value). Ask the
   user to confirm or override; collect the overrides ONLY (untouched inputs
   may be omitted — the tool merges them over the defaults) as that
   workflow's `iacInputs`.
5. Unknown keys are refused by the tool with `availableInputs` — the
   platform itself would deploy a typo silently, so take names from the
   schema, never from memory.
6. If `InputSchemas` is empty, tell the user "no parameters for
   <workflow>" and move on.

Optionally let the user rename a workflow (`workflows[].resourceName`);
the platform's default is `<template-name>-<index>`. Names must be unique
within the stack.

Build one `workflows` entry per workflow the user changed:
`{"workflow": "<id from Step A>", "iacInputs": {...}, "resourceName": ...,
"deployment": {...}, "environmentVariables": [...]}` — every field but
`workflow` optional. Workflows with nothing to change need NO entry (the tool
still creates them, with the template's defaults). `workflow` can also be the
workflow template's pinned id when only one workflow in the stack uses it.

## Step E — Confirm and create

Confirm a plain-language summary: stack name and group, the workflows and
their run order comes from the template, connector(s), variables, and per
workflow the inputs being overridden and the ones accepted as-is. Then call
`create_stack` with everything.

## Step F — After creation

The response is `{success, msg, stackId, data: {stack, workflows}, link?,
warnings?, note}`. Tell the user the stack was created and where
(`stackId`, and `link` if present) and that **nothing has run yet**. To
deploy: run the stack's *apply* action from the dashboard link, or run each
workflow with `create_workflow_run` in the order the stack's Actions define
(each `data.workflows[].SubResourceId` is the id those tools take; ask
before running — `action` is required there and always a user decision).

## No connector yet

Connectors can't be created with the MCP tools. When a connector search returns
nothing, or nothing for the cloud account or git host the user needs, stop and
give the user the settings page as a markdown link, so they can click through,
then wait until they say the connector is added:

- Cloud: `[Add a cloud connector](https://<dashboard>/orchestrator/orgs/<org>/settings/cloud-providers)`
- Git: `[Add a git connector](https://<dashboard>/orchestrator/orgs/<org>/settings/vcs-providers)`

`<org>` is what follows `/orgs/` in `source.filters.orgId` of any search
response (`/orgs/acme` → `acme`). `<dashboard>` is `app.stackguardian.io` for
Europe or `us.stackguardian.io` for the United States: match the region of the
StackGuardian MCP server URL (`api.app.stackguardian.io` or
`api.us.stackguardian.io`), and give both links if you can't tell. When the
user confirms, search again.

Never work around a missing connector by switching to another StackGuardian
organization or MCP server, even one that has a matching connector. A
different organization has different credentials, policies and people; switch
only when the user explicitly asks for that organization.

## Error handling (teaching errors)

On error, present the offered options and re-call — do not guess:
- `availableWorkflowGroups` / `availableWorkflowGroupNames` /
  `devPortalWorkflowGroupsUrl` → unknown group (see Step B)
- `candidateWorkflowGroups` → the name is ambiguous; re-call with the id
- `stackTemplateWorkflows` → a `workflows[].workflow` value is not one of
  the template's workflows; the list carries each `id`, `templateId` and
  `defaultName`
- `availableInputs` → an `iacInputs` key is not an input of that workflow
  template
- `wiredInputs` → an `iacInputs` key is pre-wired to another workflow's
  output; drop it
- `availableConnectors` / `candidates` / `availableSecrets` → as in
  sg-create-workflow
- "Could not read stack template" / "does not exist" → the template read
  is required (it supplies the run order); fix the id or retry
- HTTP 409 = stack id taken; 403 = not permitted or a policy denied;
  404 = template not found; 400 = payload rejected — relay the message.
  A 5xx or a "failed to create workflow" message may have left a
  **partial stack** (the platform writes the stack before its workflows and
  does not roll back): check `search_stacks` before retrying, and tell the
  user what exists.

Note: org is always derived server-side from the authenticated user — never
ask for or pass an organization. If the tool is missing, the server likely
has `SG_WRITE_TOOLS_ENABLED=false` (read-only mode).
