---
name: sg-create-workflow
description: Guided flow for creating a StackGuardian workflow via the StackGuardian MCP create_workflow tool — first asks whether to deploy from a marketplace template or a git repository, then walks the user through template selection (or repo, branch, directory and public/private + VCS connector), workflow group, cloud connector, environment variables, custom step pipelines (CUSTOM/WfStepsConfig), template inputs (always presenting the template's defaults for review before creating), cron schedules, post-run notifications/chaining/webhooks, runner caching and job sizing, then creates the workflow. Covers TERRAFORM, OPENTOFU and CUSTOM workflow types and both template and git sources. Use when the user wants to create/deploy a workflow, deploy a template from the StackGuardian library, deploy IaC from their own git repo, or set up an Ansible/Helm/Kubernetes/CloudFormation step pipeline.
---

# Create Workflow — Guided Flow

Create a StackGuardian IaC workflow with the `create_workflow` tool on the
StackGuardian MCP server. Follow the steps IN ORDER. Never ask the user to
type IDs or names from memory — always fetch options with the listed tools
and present choices. In user-facing messages use plain language; never
surface internal parameter names like `wfGrp`, `source`,
`deployment.connectorId`, or `iacInputs`.

Parameters are grouped to match the tool's own shape: `source` (one object,
template XOR git — never both), `deployment`,
`terraformConfig`, `approvals`, `runnerConstraints` are each a single nested
object, not flat siblings. Build each group's object as you collect its
fields in the steps below, then pass the assembled objects in the final
`create_workflow` call.

## Step A — Pick the IaC source mode

**First question, before anything else**: does the user want to deploy from
the **StackGuardian template library** or from **their own git repository**?
Ask — don't infer it from a stray URL or template name. Build exactly one of
these two shapes for `source` — never both, and never mix fields from one
into the other:
- `{"type": "template", "templateId": ..., "iacInputs": {...}}`
- `{"type": "git", "repo": ..., "ref": ..., "workingDir": ...,
  "isPrivateRepo": ..., "gitAuthRef": ..., "includeSubModule": ...,
  "iacInputs": {...}}`

### Template mode

1. Call `search_marketplace_templates(templateType='IAC')` (add `searchQuery`
   if the user described what they want). Present the results; let the user
   pick one.
2. Note the chosen template's `ResourceId` in pinned `/owner/name:rev` form
   (e.g. `/stackguardian/simple-ec2:3`) — this becomes `source.templateId`.
   Always pin the revision; never pass an unpinned template id.
3. Immediately call `get_marketplace_template_by_id` with that id and keep the
   `InputSchemas` for Step D.
4. **Draft vs published.** Each revision's `IsPublic` says whether it is
   published (`"1"`) or still a **draft** (`"0"`). When presenting revisions,
   label each one. A draft is allowed — it is how a template author tests
   one — but tell the user plainly that it is unpublished, can still change
   under the workflow, and is not for production; let them continue if they
   want. Never block on it, and never silently pick a draft. (The tool
   repeats this as a `warnings` entry in its response.)

### Git mode

1. Collect the clone URL (`source.repo` — HTTPS or SSH form both work),
   optional branch/tag/commit (`source.ref`, repo default branch when
   omitted) and optional subdirectory holding the IaC root
   (`source.workingDir`, repo root when omitted). Ask about submodules only
   if the code vendors modules that way (`source.includeSubModule=true`).
2. **Ask whether the repository is public or private — never assume.** The
   tool has no default and refuses the call until it knows:
   - **Public**: pass `source.isPrivateRepo=false` explicitly.
   - **Private**: the platform needs credentials to clone. List the org's
     VCS connectors with
     `search_orchestrator_resources(resourceTypes=['INTEGRATION.VCS'])`,
     present them (name + provider kind; if there is none, see **No
     connector yet**), and pass the pick as
     `source.gitAuthRef="/integrations/<id>"` (use the full
     `/integrationgroups/<group>/integrations/<id>` form if the connector is
     group-managed or the tool reports an ambiguity with `candidates`).
     Setting `gitAuthRef` implies private — no need to also send
     `isPrivateRepo`. For a plain git host with no connector, a
     `/secrets/<name>` token is the alternative (GIT_OTHER hosts accept
     ONLY that form).
3. The VCS provider kind is inferred from the repo host (github.com,
   gitlab.com, bitbucket.org, dev.azure.com; anything else is GIT_OTHER) and,
   when a connector is given, taken from the connector itself. Do NOT pass
   `source.vcsProvider` unless the user explicitly needs an override such as
   GITHUB_APP_CUSTOM or AZURE_DEVOPS_SP.
4. There is no `InputSchemas` for a git source — Step D is different there
   (see below).

## Step B — Workflow group and naming

1. Offer the user exactly three ways to pick the target group — never dump
   or "recommend" arbitrary groups:
   - **Name or keyword**: resolve it via
     `search_orchestrator_resources(resourceTypes=['WORKFLOW_GROUP'],
     searchQuery=<keyword>)`; on a near-miss suggest the closest match
     ("no `production` — did you mean `prod`?"). The confirmed pick becomes
     `wfGrp` — pass EVERYTHING AFTER `/wfgrps/` IN ITS `ResourceId` (e.g.
     `mcp-test-qypm75mb` from `/wfgrps/mcp-test-qypm75mb`, and the whole
     `PROD/eu-central-1` from `/wfgrps/PROD/eu-central-1`), which is how
     the platform addresses the group; the `ResourceName` shown to the user
     can differ from it, and a clean-looking name is NO guarantee they
     match (`gitops` may be `gitops-y8pf2mb1`) — never assume, always read
     the `ResourceId`. The tool accepts either and translates a name, but
     the id is what every later call (update/run/delete) needs, so carry
     the id forward. Never invent a group name.
   - **Create a new group**: pass `createNewWorkflowGroup=true` ONLY when the
     user explicitly asks for a brand-new group.
   - **Browse in the dev portal**: share the workflow-groups page —
     `https://<dashboard>/orchestrator/orgs/<org>?tab=workflowGroups`
     (`<dashboard>` and `<org>` as in **No connector yet**).
   This step is mandatory — never call `create_workflow` without a
   user-confirmed `wfGrp`.
   **Nested groups are accepted** — `PROD/eu-central-1` is a real group that
   holds workflows. Pass the whole path exactly as it appears; the last
   segment alone is a different group. A full resource id is not a group
   path — drop any `/wfs/...` or `/stacks/...` part.
2. Ask the user for:
   - workflow name (`resourceName`, 1–100 chars)
   - optional description (max 512 chars)
   - optional tags (max 10) and context tags (key:value pairs)
3. Optionally check for duplicates first with
   `search_workflows(searchQuery=<name>)`.

## Step C — Cloud connection and environment variables

1. Ask whether a cloud deployment connector is needed (skip if no cloud
   deployment — then omit `deployment` entirely). Build
   `deployment = {"connectorId": "/integrations/<id>"}` — only `connectorId`
   is required; its kind is resolved live server-side; do NOT pass
   `deployment.connectorKind` unless a returned error asks for it. Find
   connectors via
   `search_orchestrator_resources(resourceTypes=['INTEGRATION.CLOUD'])`.
   If none fits, see **No connector yet**.
2. Ask whether to add environment variables. Collect each as
   `{varName, textValue}` (plain text) or `{varName, secretId}` where
   `secretId` is a `/secrets/<name>` vault reference — exactly one of the
   two per variable. Repeat until done. (`environmentVariables` stays a flat
   list param, not nested under another object.)

## Step C2 — Custom steps (CUSTOM workflows only)

Skip this entirely unless the user wants a **custom step pipeline** rather
than a Terraform/OpenTofu run. Signals: they describe running an Ansible
playbook, a Helm chart, a Kubernetes manifest, a CloudFormation stack, or
their own container/script rather than Terraform.

1. Set `wfType: "CUSTOM"`.
2. Decide where the steps come from — ask if unclear:
   - **From the template** (template mode only): if the library template
     chosen in Step A is itself a CUSTOM template, it already carries its
     own steps. Omit `wfStepsConfig` entirely and the platform uses the
     template's. Supplying your own **replaces** the template's steps
     outright — there is no merge — so only do so when the user wants
     different steps.
   - **Git mode**: a git source carries no steps, so `wfStepsConfig` is
     REQUIRED for a CUSTOM workflow — the tool refuses the call without it.
   - **Explicit steps**: build `wfStepsConfig`, a list of up to 10 steps run
     in list order.
3. For each explicit step, find the step template with
   `search_marketplace_templates(templateType='WORKFLOW_STEP')` (or
   `get_subscription`) and present the choices — never invent an id. Then
   call `get_marketplace_template_by_id` on the chosen revision to read its
   `InputSchemas`. Present that step's defaults and collect values the same
   way as Step D — a step template's defaults ship unseen just as readily as
   the workflow's own.
   Each step is:
   `{"name": "<slug>", "wfStepTemplateId": "/owner/name:rev",
     "wfStepInputData": {"schemaType": "FORM_JSONSCHEMA", "data": {...}},
     "approval": false, "timeout": 5400, "environmentVariables": [...],
     "mountPoints": [...]}`
   Only `name` and `wfStepTemplateId` are required.
4. Rules worth knowing before you call:
   - `approval: true` pauses the run for manual approval BEFORE that step —
     a per-step gate, set per step. For a CUSTOM workflow this is the ONLY
     approval gate available: `approvalPreApply` lives in `terraformConfig`,
     which the platform rejects for CUSTOM outright. `approvals` still
     controls WHO may approve and how many of them.
   - `name` is letters/digits/`_`/`-` only, unique within the workflow. It is
     part of the run's status identity (`on_<index>_<name>`), not a label.
   - `mountPoints` need a **private** runner — set `runnerConstraints` to
     `{"type": "private", "names": ["<group>"]}` or drop the mounts.
   - `wfStepInputData.data` is **not** validated against the step template's
     schema by the platform; a wrong key reaches the container silently, so
     check `InputSchemas` rather than guessing.
   - `wfStepTemplateId` is **not** verified at create time either — a bad id
     creates a workflow that fails at every run. Always take it from a
     search result.
   - A `/secrets/<name>` reference inside a step's environment variables
     fails **silently** at run time if it can't be resolved (unlike
     workflow-level variables). Confirm the secret exists.

## Step D — Template parameters

For a CUSTOM workflow the per-step inputs were already collected in Step C2;
this step covers the workflow's own IaC template inputs.

**Git mode**: there is no template schema to read. Ask the user whether the
IaC needs variable values (Terraform variables without defaults); collect any
as a plain `source.iacInputs` dict of `{name: value}`, or omit it. Nothing is
validated here — a missing required variable surfaces at plan time — so
prompt for the ones the user knows are required. Then go to Step E.

**Template mode**:

**ALWAYS present the template's defaults to the user before creating — never
let one apply unseen.** Omitting an input does not leave it unset; the value
the template declares is what gets deployed. Show every input and its default
even when nothing is strictly required and the call would succeed untouched:
the user is agreeing to those values whether or not they were shown them, so
show them.

Read the defaults out of the `InputSchemas` fetched in Step A. It is a LIST;
the entry with `type: "FORM_JSONSCHEMA"` carries `encodedData`, a base64
JSON Schema. Decode it and walk `properties` recursively — each `default` key
is the value that ships if the user says nothing, and nested objects carry
nested defaults. An input with no `default` has none: it needs a value or it
falls through to whatever the template's own IaC code defaults to.

Present each input as: name, what it does, **the default that will be used**,
and whether it is required. Ask the user to confirm the set or override
individual values, and say plainly which ones you are about to accept as-is.
Collect their answers as `source.iacInputs`; inputs they left alone may be
omitted or passed explicitly — both behave the same.

If `InputSchemas` is empty or has no `FORM_JSONSCHEMA` entry, tell the user
"No template parameters needed" and skip.

## Step E — Options and create

Defaults are agent-safe; only surface these if the user asks or they matter.
Each bullet below is a top-level `create_workflow` parameter — build the
nested object only if you have something to put in it, and omit the
parameter entirely otherwise (its defaults still apply omitted):
- `wfType`: TERRAFORM (default), OPENTOFU, or CUSTOM (see Step C2 below).
  Note ANSIBLE / HELM / KUBERNETES / CLOUDFORMATION are NOT workflow types —
  they are search filters for CUSTOM workflows whose step template matches
  that keyword. To build one, use `wfType: CUSTOM` with the matching step
  template.
- `terraformConfig`: `{"approvalPreApply": true, "managedTerraformState": true,
  "driftCheck": false, "terraformVersion": ..., "driftCron": ...}` — these
  three booleans already match this tool's agent-safe defaults, so omit the
  whole object unless something needs to differ. `driftCron` (AWS cron) is
  stored independently of `driftCheck` — a schedule set while `driftCheck` is
  false sits inert until drift checking is enabled. `approvalPreApply` (default
  false) pauses after `plan` and waits before `apply` — it's the Terraform
  approval gate; a no-change plan finishes without asking.
  **Never send `terraformConfig` for a CUSTOM workflow** — the platform
  rejects the
  combination outright, so drift check, `approvalPreApply` and the Terraform
  hooks are simply unavailable there.
- `approvals`: `{"approvers": [...], "numberOfApprovalsRequired": N}` — WHO
  may approve. Two settings, and both are needed for a real gate:
  `approvalPreApply` (above) decides whether a run stops; `approvals` decides
  who releases it. A pause with no approvers can be released by ANYONE.
  The count reads backwards, so get it right: **`0` = every approver must
  approve** (the strictest setting, not "none"), **`1` = any one of them**,
  `N` = that many. Keep `N` <= the number of approvers — nothing validates it,
  and a larger N is a gate no run can satisfy. `>=1` is required when any
  approver is an SSO group. ALWAYS send both: approvers with no count leaves
  the platform's default of `0`, silently creating a UNANIMOUS gate; an empty
  list with a count mints a workflow needing approvals from nobody.
  Read the result back in plain words before creating ("anyone from X or Y can
  approve" / "both must approve").
- `runnerConstraints`: `{"type": "shared"}` default (StackGuardian-managed
  infra), or `{"type": "private", "names": ["<runner-group-name>"]}` to run on
  your own runner group. `names` is a single-item list of the group's NAME
  (not an id or path) — find it via
  `search_orchestrator_resources(resourceTypes=['RUNNER'])` and use the
  ResourceName.
- `miniSteps`: post-run actions keyed by run outcome (COMPLETED / ERRORED /
  ...) — chain other workflows or stacks, send email notifications, fire
  webhooks:
  `{"wfChaining": {"COMPLETED": [{"workflowGroupId": ..., "workflowId": ...}]},
  "notifications": {"email": {"COMPLETED": [{"recipients": [...]}]}},
  "webhooks": {"COMPLETED": [{"webhookName": ..., "webhookUrl": ...}]}}`.
  All three groups and every event key are optional. A `stackId` can stand in
  for `workflowId` when chaining to a stack. `DRIFT_DETECTED` only ever fires
  when `terraformConfig.driftCheck` is enabled — don't offer it otherwise.
- `userSchedules`: up to 10 cron schedules for automated runs —
  `[{"cron": "0 2 * * ? *", "state": "ENABLED", "desc": ..., "inputs": {...}}]`.
  `cron` is AWS EventBridge syntax (note the `?` day-of-week field) and
  `state` is ENABLED/DISABLED — a DISABLED schedule is kept but doesn't fire,
  which is how you park one during a freeze. `inputs` overrides settings for
  THAT schedule's runs only (env vars, Terraform action/config, job sizing,
  chaining) — omit it and scheduled runs use the workflow's own settings.
- `cacheConfig`: persist runner directories between runs so repeats
  warm-start — `{"enabled": true, "paths": [".terraform"], "key":
  "tf-plugins-v1", "policy": "PULL_PUSH"}`. If you pass it at all, all four of
  `enabled`/`paths`/`key`/`policy` are REQUIRED. `key` is slug format
  (letters, digits, `_`, `-`); runs sharing a key share the cache, so change
  it to force a fresh one. `policy` is PULL_PUSH (restore + save, typical),
  PULL (restore only), or PUSH (save only — a cache-warming workflow).
  Optional `fallback_keys` restores from older keys after a rotation.
- `userJobCPU` / `userJobMemory`: run-container sizing — CPU in ECS units
  (1024 = 1 vCPU; platform default 512) and memory in MB (default 1024).
  Raise memory when runs fail out-of-memory, common with large Terraform
  states; raise CPU for very large plans.
- `parallelExecution`: **CUSTOM workflows only** — true lets runs of this
  workflow execute simultaneously, false (platform default) queues them
  serially. Rejected outright for TERRAFORM/OPENTOFU.
- `isActive`: true (default) = active. false parks the workflow so it doesn't
  count toward the plan's active-workflow quota, but its run history, logs and
  outputs return 402 until it's re-activated (triggering a run re-activates it
  automatically). Rarely worth setting at create time.
- `githubComSync`: advanced GitHub PR-trigger behavior, e.g.
  `{"pull_request_opened": {"createWfRun": {"enabled": true}}}`. Free-form and
  NOT validated by the platform, so a wrong key fails silently — most
  workflows omit it entirely.

Confirm a plain-language summary of everything collected with the user, then
call `create_workflow` with all parameters.

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

The tool validates live and returns actionable errors instead of opaque 400s.
On error, present the offered options and re-call — do not guess:
- `availableWorkflowGroups` → unknown group; a list of group IDS (capped
  at 50) — re-call with one verbatim; `availableWorkflowGroupNames`
  maps any id whose display name differs, show those to the user; plus
  the `devPortalWorkflowGroupsUrl` link for browsing
- `availableConnectors` → unknown `deployment.connectorId`; present list,
  re-call
- `availableVcsConnectors` → either the public/private question hasn't been
  answered (the error text asks it — put it to the user, then re-call with
  `isPrivateRepo=false` or a chosen connector as `gitAuthRef`) or the given
  `gitAuthRef` connector is unknown; present the list, re-call
- `candidates` → the bare `/integrations/<id>` exists in several integration
  groups; re-call with the full `/integrationgroups/...` id from the list
- `availableSecrets` → a referenced `/secrets/<name>` doesn't exist; present
  list or create the secret first
- HTTP 409 = workflow name taken; 403 = not permitted; 400 = payload/policy
  rejection — relay the platform's message

## Success

The response is `{success, msg, data, source}`; `data.SubResourceId` is the
new `/wfgrps/<group>/wfs/<name>` path. Tell the user the workflow was created
and where. It appears in `search_workflows` once StackGuardian ingestion
catches up (seconds) — no need to re-query, the response already carries the
resource.

Note: org is always derived server-side from the authenticated user — never
ask for or pass an organization. If the tool is missing, the server likely has
`SG_WRITE_TOOLS_ENABLED=false` (read-only mode).
