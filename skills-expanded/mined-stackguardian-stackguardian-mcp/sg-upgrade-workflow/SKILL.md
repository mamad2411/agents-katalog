---
name: sg-upgrade-workflow
description: Guided flow for upgrading (or downgrading) an existing StackGuardian workflow to a different template revision via the StackGuardian MCP update_workflow tool — pick the target revision, choose an upgrade mode (keep your settings vs reset to the template), preview the exact diff with a dry-run, review the four inputs, then apply. Use when the user wants to upgrade/move a workflow to a newer (or older) template version. For plain settings edits use the sg-update-workflow skill.
---

# Upgrade Workflow — Guided Flow

Move an existing workflow to a different template revision with the
StackGuardian MCP `update_workflow` tool (using its `upgradeMode` +
`dryRun`). This is a SEPARATE flow from a normal settings edit: an upgrade
changes the source template revision and lets the platform reconcile the
rest. For plain settings changes (Terraform version, approvals, connector,
env vars) use the `sg-update-workflow` skill instead.

Follow the steps IN ORDER. Never ask the user to type ids from memory — fetch
options with the listed tools and present choices.

## Step A — Locate the workflow

Find it with `search_workflows(searchQuery=<name>)`, confirm with the user, and
read `wfGrp` / `resourceName` (and `stack` if its `ResourceId` contains
`/stacks/<stack>/`) off the chosen result — exactly as in the `sg-update-workflow`
skill, including its rule for nested groups: `wfGrp` is everything between
`/wfgrps/` and the `/wfs/` (or `/stacks/`) marker, so `/wfgrps/platform/eu/wfs/api`
gives `wfGrp="platform/eu"`, not `"platform"`.

## Step B — Pick the target template revision

1. Find the template with `search_marketplace_templates(templateType='IAC')`
   (add `searchQuery`). Present revisions; let the user pick the target one.
   Label each revision **draft** or **published** from its `IsPublic`
   (`"0"` / `"1"`): moving a workflow onto a draft is allowed but must be
   said out loud — it is unpublished, can still change, and is not for
   production. Warn, don't block.
2. Note its pinned `/owner/name:rev` id (e.g. `/stackguardian/simple-ec2:12`) —
   this becomes `source.templateId`. Then call
   `get_marketplace_template_by_id` on it — not optional, since Step E has to
   show the user that revision's input defaults.

## Step C — Choose the upgrade mode

Explain the two modes plainly and let the user choose:
- **Keep my settings** (`upgradeMode="PRESERVE_SETTINGS"`) — upgrade the code but
  preserve the customizations the user made on this workflow (e.g. extra
  approvers, a pinned Terraform version). New env-var keys from the template are
  still added.
- **Reset to the template** (`upgradeMode="RESET_TO_TEMPLATE"`) — take the new
  template's defaults, discarding this workflow's overrides (the user can still
  review before applying).

## Step D — Preview the change (dry-run)

Call `update_workflow` with `dryRun=true`:
`update_workflow(wfGrp, resourceName, stack?, source={"type":"template",
"templateId":"<new rev>"}, upgradeMode=<mode>, dryRun=true)`.

This mutates nothing. Present the returned `preview` to the user:
- `summary` — how many settings are added / modified / removed.
- `changes` — the specific before/after per key.
- `reviewDimensions` — the four things worth reviewing: template **iacInputs**,
  **environmentVariables**, **connectors**, and **customStepParams**.

## Step E — Review the four inputs (MANDATORY — never skip)

This step ALWAYS runs on every upgrade, even when the dry-run reports no
required new inputs. Do NOT jump from the Step D preview straight to applying.
Present all four review dimensions explicitly and get the user's sign-off on
each one before Step F — the whole point of the upgrade flow is that the user
reviews these four things every time.

Walk the user through the four dimensions, showing the current/resolved value
for each from the Step D `reviewDimensions` (say "unchanged — keeping current"
when the dry-run shows no change, rather than silently omitting it):

1. **Template inputs** (`iacInputs`) — list the new revision's inputs, each
   with its effective value AND the new revision's own default, and ask the
   user to confirm or override. Present the defaults even when the dry-run
   reports no change: a new revision can add an input or move a default, and
   under `RESET_TO_TEMPLATE` the workflow adopts the new default silently.
   Read them from the revision's `InputSchemas` — the `FORM_JSONSCHEMA` entry's
   `encodedData` is a base64 JSON Schema whose `default` keys are the values
   that ship. Say plainly which ones you are accepting as-is.
2. **Environment variables** (`environmentVariables`) — show env vars the
   revision adds/changes; collect any values the user wants to set.
3. **Cloud connector** (`deployment`) — confirm the connector the workflow will
   deploy with; let the user change it.
4. **Custom-step params** — surface any from `reviewDimensions` for the user to
   review.

Gather anything the user wants to override as the matching `update_workflow`
param: template inputs -> `source.iacInputs`; environment variables ->
`environmentVariables`; cloud connector -> `deployment`.

Most other "advanced" settings (runner, Terraform options) follow the chosen
`upgradeMode` automatically; don't collect those here.

**Approvals are an exception — never send `approvers` without the count.**
`NumberOfApprovalsRequired` is one of the keys an upgrade reconciles, and if
your payload carries approvers but no count, `RESET_TO_TEMPLATE` resets the
count to its default of `0` — which means EVERY approver must approve. A
2-of-3 gate silently becomes all-of-2. If any approver is an SSO group the
same call instead hard-400s ("at least 1 when SSO Groups are selected"). So
whenever an upgrade touches approvers at all, read the stored count first and
pass it explicitly alongside them.

**Three exceptions an upgrade WIPES — carry them over yourself.** Cron
schedules (`userSchedules`) and run-container sizing (`userJobCPU` /
`userJobMemory`) are reset to the target template's values by an upgrade, and
templates rarely define any, so an upgrade silently drops a nightly schedule
or a raised memory limit. Read the workflow's current values first
(`get_orchestrator_resource_by_id`), tell the user what would be lost, and
pass the ones they want kept alongside the upgrade in Step F.

Conversely, `isActive`, `cacheConfig`, `parallelExecution` and `githubComSync`
are untouched by an upgrade — the tool REJECTS them combined with
`upgradeMode`. If the user wants one of those changed too, apply
the upgrade first, then make a second `update_workflow` call with just that
field.

`contextTags` and `miniSteps` sit in between: an upgrade accepts them and
merges them onto the stored values, so passing a partial is safe. Removal
works here too and uses the same idiom as a plain settings change — a key set
to `null` drops it (`contextTags={"eu": null}`), and `miniSteps={"wfChaining":
null}` clears just that group. Both paths merge against the stored workflow
identically, so you don't need to split a removal into a second call.

`tags`, by contrast, REPLACES on this path as on every other — send the
complete list the user wants to end up with, not just the ones they named.

Only proceed to Step F after the user has explicitly reviewed all four and
confirmed.

## Step F — Apply

On confirmation, re-call WITHOUT `dryRun` (same `source` + `upgradeMode`, plus
any overrides gathered in Step E):
`update_workflow(wfGrp, resourceName, stack?, source={"type":"template",
"templateId":"<new rev>", "iacInputs":{...}?}, upgradeMode=<mode>,
environmentVariables=[...]?, deployment={...}?, userSchedules=[...]?,
userJobCPU=...?, userJobMemory=...?)` — the last three only to carry over
values the upgrade would otherwise wipe (see Step E).

## Error handling

- `moved: true` with `movedTo` -> the workflow was relocated; re-target it.
- `status: 409` about runners -> active runs block the change; cancel or wait.
- `status: 400` -> often the target template isn't subscribed in the org, or an
  input/policy rejection — relay the platform's message; the user may need to
  subscribe the template first (`get_subscription` lists subscribed templates).
- `status: 404` -> wrong workflow path; re-locate via `search_workflows`.

## Success

The response is `{success, msg, data, source}`. Tell the user the workflow was
upgraded to the new revision and summarize what changed. It refreshes in
`search_workflows` once StackGuardian ingestion catches up (seconds).

Note: org is always derived server-side from the authenticated user — never ask
for or pass an organization. If the tool is missing, the server likely has
`SG_WRITE_TOOLS_ENABLED=false` (read-only mode).
