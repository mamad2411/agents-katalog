---
name: sg-update-workflow
description: Guided flow for changing an existing StackGuardian workflow's settings via the StackGuardian MCP update_workflow tool — locate the workflow, then change any of description/tags, cloud connector, environment variables, Terraform options, custom step pipelines (CUSTOM workflows), approvals, runner placement, cron schedules, post-run notifications/chaining/webhooks, runner cache, job sizing, activation, or template inputs. Only the fields you change are touched. Use when the user wants to edit/modify/reconfigure an existing workflow's settings (NOT to upgrade its template revision — that's the sg-upgrade-workflow skill).
---
# Update Workflow — Guided Flow

Change an existing workflow's settings with the StackGuardian MCP
`update_workflow` tool. This is for editing a workflow that already exists —
to CREATE one use the `sg-create-workflow` skill; to UPGRADE its template
revision use the `sg-upgrade-workflow` skill.

Follow the steps IN ORDER. Never ask the user to type ids or names from memory —
fetch options with the listed tools and present choices. In user-facing messages
use plain language; never surface internal parameter names like `wfGrp`,
`terraformConfig`, or `DeploymentPlatformConfig`.

**Golden rule:** pass ONLY the fields the user wants to change. Everything you
omit is preserved automatically — the tool reads the current workflow and merges
your change in. You never need to restate unchanged settings.

**Exceptions that REPLACE rather than merge** — `wfStepsConfig`,
`userSchedules`, `cacheConfig`, `githubComSync`, `tags`, `approvals` and
`runnerConstraints`. For these, whatever you send becomes the stored value
outright, so read the current one first and re-send every part the user wants
to keep. Tell the user this before applying.

Why these and not the others: a field can only MERGE if it has a key to address
its parts by. Maps do (`contextTags` by tag name, `environmentVariables` by
`varName`, `terraformConfig` by option name), so a partial is safe and removal
is expressed explicitly. Lists and all-or-nothing objects don't, so a merge
could never express removal — replace is the only semantics that can drop an
element, and the price is that you must send the complete set every time.

Every merging field is merged by the TOOL, not by StackGuardian — it reads the
workflow first and merges your partial in. So a merging field can fail with
"couldn't read the current workflow" and apply nothing; that is the tool
refusing to send a partial that would drop the keys you didn't name. Report it
and stop, don't rebuild the payload by hand.

## Step A — Locate the workflow

1. Find it with `search_workflows(searchQuery=<name>)`. Present matches; let the
   user confirm the one they mean. Never invent a workflow name.
2. From the chosen result's `ResourceId`, read off:
   - the workflow group -> `wfGrp` — EVERYTHING between `/wfgrps/` and the
     `/wfs/` (or `/stacks/`) marker, slashes included. Don't stop at the first
     segment.
   - the workflow name -> `resourceName`
   - if the id contains `/stacks/<stack>/`, the stack -> `stack` (omit
     otherwise)
     A path like `/wfgrps/dev/wfs/api` gives `wfGrp="dev"`, `resourceName="api"`.
     A path like `/wfgrps/dev/stacks/net/wfs/api` adds `stack="net"`.
   **Nested workflow groups** are real and `update_workflow` accepts them: in
   `/wfgrps/platform/eu/wfs/api` the group is the whole `"platform/eu"`, NOT
   `"platform"`. Taking only the first segment silently targets a different
   group — usually a 404, or the wrong workflow if a same-named one exists
   there. Keep the inner slashes exactly as they appear; don't URL-encode them
   and don't collapse them. (Only `..` and backslashes are rejected.)

## Step B — Decide what to change

Ask the user what they want to change, then build ONLY those parameters:

- **description / tags / contextTags** — these three do NOT behave alike.
  - `description` is a scalar: it replaces.
  - `contextTags` is a map, so it MERGES key-by-key — tags the user doesn't
    mention are kept. Because omitting a key means "keep it", REMOVING a tag
    needs an explicit `null` for that key: to drop `eu`, pass
    `contextTags={"eu": null}`. This works on a plain settings change and
    alongside a template upgrade — both paths merge identically.
  - `tags` is a LIST, so it REPLACES wholesale. There's no key to null out, so
    sending the survivors is the only way to remove one: to drop `eu` from
    `["prod","eu","team-a"]`, pass `tags=["prod","team-a"]`.
    **This is the trap:** passing `tags=["prod"]` to "add prod" silently
    deletes the other two and reports success. Whenever the user wants to ADD
    a tag, read the current list first (it's on the `search_workflows` result
    you already have from Step A) and send the full intended set.
  (The `contextTags` merge is the tool's doing — it reads the current workflow
  and merges before sending, because the platform overwrites the whole map
  either way.)
- **Cloud connector** (`deployment`) — `{"connectorId": "/integrations/<id>"}`.
  Find connectors via
  `search_orchestrator_resources(resourceTypes=['INTEGRATION.CLOUD'])`; if
  none fits, see **No connector yet**. The connector's kind is resolved live;
  the workflow's existing deploy-profile name is kept unless you pass
  `deployment.profileName`.
- **Environment variables** (`environmentVariables`) — a list of
  `{varName, textValue}` or `{varName, secretId}` entries. These are UPSERTED by
  name: entries you pass add or replace matching vars; every existing var you
  DON'T mention is kept. (Removing a var isn't supported here yet — tell the user
  to remove it in the dev portal if asked.) A `/secrets/<name>` `secretId` is
  verified live; an unknown one returns `availableSecrets`.
- **Terraform/OpenTofu options** (`terraformConfig`) — pass only the keys to
  change, e.g. `{"terraformVersion": "1.6.2"}` or `{"driftCheck": true,
  "driftCron": "0 */6 * * ? *"}`. Keys you omit are kept, and a key set to
  `null` is removed. That preservation is the tool's, not the platform's: it
  reads the workflow and merges your partial into the stored options before
  sending. So if the read fails the update is refused outright rather than
  applied partially — surface that to the user, don't retry with a fuller
  payload.
  Two things the merge does NOT cover:
  - **Only the flat options merge.** The list-valued ones REPLACE wholesale:
    the lifecycle step lists (`prePlanWfStepsConfig`, `postPlanWfStepsConfig`,
    `preApplyWfStepsConfig`, `postApplyWfStepsConfig`), the hook lists
    (`preInitHooks`, `prePlanHooks`, `postPlanHooks`, `preApplyHooks`,
    `postApplyHooks`) and `terraformBinPath`. This is the `tags` trap one level
    down: to ADD one hook, read the current list
    (`get_orchestrator_resource_by_id`) and send the full intended list.
  - **Alongside a template upgrade the omitted keys come from the template,
    not the workflow.** With `upgradeMode` set, your partial is applied on top
    of the current options under `PRESERVE_SETTINGS` but on top of the TARGET
    TEMPLATE's options under `RESET_TO_TEMPLATE` — so on a reset, anything you
    don't name lands on the template's value rather than the one the workflow
    has today. Preview it with the `sg-upgrade-workflow` skill's dry run before
    applying, and tell the user which values are about to change.
- **Custom step pipeline** (`wfStepsConfig`) — CUSTOM workflows ONLY. Up to 10
  steps, run in list order. **This field does NOT merge** (see the
  replace-wholesale list under the golden rule): the
  list you send REPLACES the stored pipeline entirely, so always read the
  workflow's current steps first (`get_orchestrator_resource_by_id`) and
  re-send every step the user wants to keep, not just the changed one. State
  this to the user before applying. The tool refuses if the workflow isn't
  CUSTOM — a workflow's type is fixed at creation, so a Terraform workflow can
  never be converted into a step pipeline; the only route is a new workflow.
  Steps can't be emptied either (a CUSTOM workflow with no steps fails every
  run). Step shape and its gotchas are documented in the `sg-create-workflow`
  skill's Step C2 — the same rules apply here (unique slug names,
  `mountPoints` need a private runner, `wfStepTemplateId` and
  `wfStepInputData.data` are NOT verified by the platform). Cannot be combined
  with a template upgrade: upgrade first, then adjust the steps.
- **Approvals** (`approvals`) — `{"approvers": [...],
  "numberOfApprovalsRequired": N}`. REPLACES the stored approval settings, so
  send the full intended state. Two settings make a gate: whether a run stops
  is `terraformConfig.approvalPreApply` (TERRAFORM/OPENTOFU) or a step's own
  `approval: true` (CUSTOM); `approvals` only says who may release it, and a
  pause with NO approvers can be released by anyone. So "I added approvers but
  nothing asks" means the gate is off, and clearing `approvers` doesn't remove
  the pause — it opens it to everyone. To drop the gate itself, set
  `approvalPreApply` false.
  The count reads backwards: **`0` = every approver must approve** (strictest,
  not "none"), **`1` = any one of them**, `N` = that many, and `N` must be <=
  the number of approvers or no run can satisfy it. `>=1` when any approver is
  an SSO group. Emptying `approvers` zeroes the count for you, so you can't
  strand the workflow. The tool does NOT do the reverse: sending approvers
  without a count leaves the stored count, whose MEANING changes with the list
  — adding approvers to a workflow sitting at count `0` turns it from "anyone"
  into "unanimous". So read the current count first
  (`get_orchestrator_resource_by_id`) and always send both together.
- **Runner placement** (`runnerConstraints`) — `{"type": "shared"}` or
  `{"type": "private", "names": ["<runner-group-name>"]}` (find the runner group
  via `search_orchestrator_resources(resourceTypes=['RUNNER'])`, use its
  ResourceName).
- **Template / variable inputs only** (`iacInputs`) — a dict of new input values
  applied to the CURRENT source without changing the template, e.g.
  `{"region": "eu-west-1"}`. (To also change the source template/repo, pass
  `source` instead — see below.)
  Changing inputs on the current template does not pull in new defaults, so
  only the values the user names change.
- **Change the source** (`source`) — a full `{"type": "template", ...}` or
  `{"type": "git", ...}` object (same shape as `create_workflow`). This
  re-points the workflow's IaC. WARNING: changing the source of a live workflow
  keeps its existing state file but points it at different code — surface this
  to the user before doing it, and prefer the `sg-upgrade-workflow` skill when the
  intent is "move to a newer template revision." Don't pass both `source` and
  `iacInputs`. Whenever you point a workflow at a different template or
  revision, call `get_marketplace_template_by_id` on it first and present that
  template's input defaults to the user before applying — the new template's
  values are what the workflow will run with, and the user should see them
  rather than inherit them unseen. Same rule as the sg-create-workflow skill's
  Step D.
- **Post-run actions** (`miniSteps`) — workflow/stack chaining, email
  notifications and webhooks keyed by run outcome; same shape as in the
  `sg-create-workflow` skill's Step E. This one MERGES onto the stored config, so
  a partial like `{"webhooks": {...}}` keeps the existing chaining and
  notifications untouched.
- **Cron schedules** (`userSchedules`) — REPLACES the stored list wholesale
  (up to 10). Send every schedule the user wants kept plus the change; an
  empty list clears them all. Schedules have no caller-facing id — the tool
  pairs your list positionally with the stored ones, so entry 1 edits the
  first stored schedule, entry 2 the second, and anything past the stored
  count is created. Read the current schedules first
  (`get_orchestrator_resource_by_id`) so the positions line up.
- **Runner cache** (`cacheConfig`) — REPLACES wholesale; it's all-or-nothing
  (`enabled`/`paths`/`key`/`policy` are required together), so there's nothing
  to merge. Shape and `policy` values are in the `sg-create-workflow` skill's
  Step E.
- **Run-container sizing** (`userJobCPU` / `userJobMemory`) — CPU in ECS units
  (1024 = 1 vCPU) and memory in MB. Raise memory for out-of-memory runs.
- **Concurrent runs** (`parallelExecution`) — CUSTOM workflows only, verified
  against the workflow's stored type; true allows simultaneous runs, false
  queues them.
- **Activate / deactivate** (`isActive`) — true activates, false deactivates
  (frees the plan's active-workflow quota, but run history, logs and outputs
  return 402 until re-activated). Rejected for a workflow inside a stack —
  stacks manage activity through the stack itself. Cannot be combined with a
  template upgrade.
- **GitHub PR triggers** (`githubComSync`) — REPLACES wholesale. Free-form and
  not validated by the platform, so confirm the exact shape with the user
  rather than guessing keys.

## Step C — Confirm and update

Summarize, in plain language, exactly what will change (and note that everything
else stays the same). On confirmation, call `update_workflow` with `wfGrp`,
`resourceName`, the optional `stack`, and only the fields being changed.

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

Present the offered options and re-call — don't guess:
- `availableConnectors` -> unknown `deployment` connector; present list, re-call.
- `availableSecrets` -> a referenced `/secrets/<name>` doesn't exist; present
  list or create the secret first.
- `availableVcsConnectors` -> unknown git `source.gitAuthRef`; present, re-call.
- `status: 404` / "not found" -> the workflow path was wrong; re-locate with
  `search_workflows` and re-read `wfGrp`/`resourceName`/`stack`.
- `moved: true` with `movedTo` -> the workflow was renamed/relocated; tell the
  user its new path and re-target it.
- `status: 409` about runners -> the workflow has active runs (queued / running /
  awaiting approval); a runner-placement change is blocked until those finish.
  Tell the user to cancel or wait, then retry.
- `status: 403` -> not permitted; `status: 400` -> payload/policy rejection —
  relay the platform's message.

## Success

The response is `{success, msg, data, source}`. Tell the user the workflow was
updated and what changed. The change shows up in `search_workflows` once
StackGuardian ingestion catches up (seconds) — no need to re-query.

Note: org is always derived server-side from the authenticated user — never ask
for or pass an organization. If the tool is missing, the server likely has
`SG_WRITE_TOOLS_ENABLED=false` (read-only mode).
