---
name: operator
description: Run automations, monitor jobs, diagnose and retry failures, handle manual approval tasks, and manage triggers on the Itential Platform. Use when you need to find or start a workflow, check job status, see why jobs failed, retry a failed task, approve a waiting manual task, or set up endpoint, manual or scheduled triggers.
argument-hint: "[action or workflow-name]"
---

# Itential Operator — Run, Monitor and Fix Automations

This skill is for **operating** the Itential Platform: finding and running automations, monitoring jobs, handling manual tasks, managing triggers, and responding to failures. To build or change workflows — or to test and sign off a delivery, which Itential's builder skills do by running jobs themselves — use the builder skills (`itential-builder` plugin: `builder-agent`, `qa-agent`). Platform health, adapters and access are Itential's admin skills (`itential-admin-skills`).

## Org, team & personal rules

Before using this skill, check `custom/org/`, `custom/team/` and `custom/dev/`
in this skill's own folder. Read every `.md` file found — any folder may be
empty or absent. Apply them on top of everything below; where a file overrides a
specific rule here, follow the override. More specific wins: dev > team > org >
this document. No customization may weaken this skill's safety
rules or put credentials in committed files.

---

## Connecting to the Platform

Read `PLATFORM_URL`, `AUTH_METHOD` and the credentials from the `.env` in the folder you're working in. Ask the user only if there's no `.env`. Never print secrets or tokens back to the user.

**OAuth (`AUTH_METHOD=oauth`, `CLIENT_ID`, `CLIENT_SECRET`)** — the usual case, and the only option on SSO-enabled platforms. The request **must** be `application/x-www-form-urlencoded`, not JSON:

```bash
curl -s -X POST "{PLATFORM_URL}/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials"
```

Returns `{"access_token": "...", "token_type": "bearer", "expires_in": 3600}`. Send `Authorization: Bearer {access_token}` on every call.

**Username/password (`AUTH_METHOD=password`, `USERNAME`, `PASSWORD`)** — local or dev platforms: `POST /login` with `{"username": "...", "password": "..."}` (JSON) returns a token string; pass it as a `?token=` query parameter instead of a header.

Re-authenticate on a 401, or when calls start returning empty responses mid-session — tokens expire (OAuth: `expires_in` seconds).

## Concepts

- **Automation** — a runnable workflow registered in Operations Manager: a name, a `componentId` (the workflow), and optional triggers.
- **Job** — one run of a workflow: status, variables, tasks, errors and metrics.
- **Trigger** — a way to start a job automatically: `endpoint` (API call), `manual` (a form in the UI), `schedule` (a repeating interval), `eventSystem` (a platform event).
- **Manual task** — a human-in-the-loop step in a running job. An operator claims it, reviews it, and finishes it before the job continues.

## Gotchas

- Operations Manager responses are `{message, data, metadata}`; lists put paging in `metadata: {total, skip, limit}`.
- **Filters differ by endpoint — a wrong filter is silently ignored and returns everything:**
  - Jobs and tasks: brackets — `equals[status]=error`, `contains[name]=Backup`, `starts-with[name]=AWS`.
  - Automations and triggers: field name separately — `contains=Backup&containsField=name`, `equals=schedule&equalsField=type`, `startsWith=AWS&startsWithField=name` (brackets return an error).
  - Automation Studio workflows: brackets too — `equals[_id]={id}`, `equals[name]={name}`. The colon form (`equals=_id:{id}`) is ignored and returns unrelated workflows.
- **Automations ≠ workflows.** An automation holds the name, triggers and access; the workflow (tasks, `inputSchema`) lives in Automation Studio. Look up inputs by the automation's `componentId`.
- **Start jobs by workflow name** — `POST /operations-manager/jobs/start` takes `workflow` (the name), not the automation ID, and variables go in `options.variables`, never at the top level (they're ignored there).
- **Check `data.error`, not just `data.status`** — the error array says which task failed and why.
- **Retry the failed task, don't restart the job** — `POST /operations-manager/jobs/{jobId}/tasks/{taskId}/retry` keeps the job's variables and completed work; a new job loses them.
- **A manual task waiting for someone shows `status: running`** with `type: manual` — there is no `paused` status for these.
- **Finishing a manual task:** `{"taskData": {"finish_state": "success", "variables": {...}}}` — claim it first.
- **Scheduled triggers have no cron syntax** — they run every `repeatInterval` milliseconds from `firstRunAt`.
- `contains` can match too broadly ("Request Change" also matches other names) — use an exact match when you know the name. But automation names with characters like `(` `)` never match `equals`/`startsWith` (e.g. "(LCM) Certificate Discovery") — use `contains` on a plain part of the name and pick from the results.
- A workflow in a project your account can't see returns no results (or `{}` from `/workflows/detailed/{name}`) — that's access, not a missing workflow; ask the project owner to add your account.

## Find and Understand Automations

### List automations

```
GET /operations-manager/automations?contains=Backup&containsField=name
```

Query parameters: `limit`, `skip`, `sort`, `order`, and the filter pairs `equals`/`equalsField`, `contains`/`containsField`, `startsWith`/`startsWithField`.

```json
{
  "message": "Successfully retrieved automations",
  "data": [
    {
      "_id": "68af8ad9b7a68a68f9dcb435",
      "name": "(LCM) VIP Management Operations",
      "description": "",
      "componentName": "@688a1319: VIP LCM Ops Mgr",
      "componentType": "workflows",
      "componentId": "ceca87c0-3f45-4a52-9e54-80771ccff8bb"
    }
  ],
  "metadata": {"total": 57, "skip": 0, "limit": 25}
}
```

- `componentId` — the workflow's `_id` in Automation Studio
- `componentName` — the workflow's name (project workflows are prefixed `@<projectId>: `) — this is the name to pass when starting a job

### Get a workflow's inputs

```
GET /automation-studio/workflows?equals[_id]={componentId}&include=name,inputSchema
```

Returns `{items: [{_id, name, inputSchema}], total}`. Or by name:

```
GET /automation-studio/workflows/detailed/{urlEncodedWorkflowName}
```

`inputSchema.properties` lists the variables to pass when starting a job; `inputSchema.required` says which can't be left out.

## Start and Monitor Jobs

### Start a job

```
POST /operations-manager/jobs/start
```
```json
{
  "workflow": "Workflow Name Here",
  "options": {
    "description": "Why this job is being run",
    "type": "automation",
    "variables": {
      "device_name": "IOS-CAT8KV-1",
      "vlan_id": 100
    }
  }
}
```

- `workflow` — the workflow **name**, not the automation ID
- `options.variables` — must match the workflow's `inputSchema`
- `options.type` — `"automation"` for normal jobs, `"resource:action"` for Lifecycle Manager actions
- `options.description` — optional, shown in the UI

The response's `data._id` is the job ID.

### Check a job

```
GET /operations-manager/jobs/{jobId}
```

```json
{
  "data": {
    "_id": "job-id",
    "name": "Workflow Name Here",
    "status": "error",
    "variables": {"device_name": "IOS-CAT8KV-1"},
    "error": [
      {"task": "c3d4", "message": "…what went wrong…", "timestamp": 1791391389640}
    ],
    "tasks": {
      "a1b2": {"name": "getDevice", "status": "complete", "metrics": {"finish_state": "success"}},
      "c3d4": {"name": "backUpDevice", "status": "error", "metrics": {"finish_state": "error"}}
    },
    "metrics": {"start_time": 1791391380000, "progress": 0.5, "user": "..."}
  }
}
```

- `data.status` — `running`, `complete`, `error`, `canceled`, `paused`
- `data.error` — array of `{task, message, timestamp}`; `message` is often the failing system's own response
- `data.variables` — all job variables, including outputs
- `data.tasks` — every task's `status` and `metrics.finish_state` (`success`, `error`, `failure`)

### List jobs

```
GET /operations-manager/jobs?limit=10&sort=metrics.start_time&order=-1
```

Filter: `equals[status]=error`, `contains[name]=Backup`.

### Bulk operations

```
POST /operations-manager/jobs/pause    {"jobIds": ["id1", "id2"]}
POST /operations-manager/jobs/resume   {"jobIds": ["id1", "id2"]}
POST /operations-manager/jobs/cancel   {"jobIds": ["id1", "id2"]}
```

### Watch a job

Get notified when a job's status changes:
```
POST /operations-manager/jobs/{jobId}/watch
POST /operations-manager/jobs/{jobId}/unwatch
```

## Handle Failures

### Find what went wrong

`GET /operations-manager/jobs/{jobId}`, then:
1. `data.error` — which task failed, and the message
2. `data.tasks.{taskId}` — the failing task's name and `finish_state`
3. Read the message before retrying — a bad input or an unreachable system will fail again

### Retry a failed task

```
POST /operations-manager/jobs/{jobId}/tasks/{taskId}/retry
```
```json
{"variables": {}}
```

Pass changed variables in `variables` to retry with different inputs.

### Continue from a task

```
POST /operations-manager/jobs/{jobId}/continue
{"fromTask": "c3d4"}
```

Resumes the job from that task, skipping the ones before it.

### Revert

```
POST /operations-manager/jobs/{jobId}/revert
{"fromTask": "e5f6", "toTask": "a1b2"}
```

Runs the workflow backward from `fromTask` to `toTask`, following its revert transitions.

## Manual Tasks

Manual tasks are approval or review steps that pause a job until someone acts.

### Find waiting tasks

```
GET /operations-manager/tasks?equals[type]=manual&equals[status]=running
```

Each task has:
- `_id` — the task's ID (use it to claim, assign or release)
- `job._id` — the job it belongs to; `job.task` — its ID within the workflow (use it to finish)
- `name` — e.g. `ViewData`; `view` — the UI page for it
- `metrics.owner` — who has claimed it (empty if nobody)

### Claim → review → finish

**1. Claim it:**
```
POST /operations-manager/tasks/{taskId}/claim
```

**2. See what it shows and collects:**
```
GET /operations-manager/jobs/{jobId}/tasks/{taskId}/manual-controller
```

**3. Finish it:**
```
POST /operations-manager/jobs/{jobId}/tasks/{taskId}/finish
```
```json
{
  "taskData": {
    "finish_state": "success",
    "variables": {"approved": true, "notes": "Reviewed and approved"}
  }
}
```

- `finish_state` — the path the workflow takes next: usually `success`, or `failure` to reject
- `variables` — the values the task's form collects (see the manual-controller response for their names)

### Assign or release

```
POST /operations-manager/tasks/{taskId}/assign    {"userId": "user-id"}
POST /operations-manager/tasks/{taskId}/release
```

## Triggers

### List triggers

```
GET /operations-manager/triggers?equals=schedule&equalsField=type
```

Other filters work the same way: `contains=Backup&containsField=name`, `enabled=true`, `actionId={automationId}`.

| Type | Starts a job when… | Key fields |
|------|-------------------|------------|
| `endpoint` | something calls `/operations-manager/triggers/endpoint/{routeName}` | `routeName`, `verb`, `schema` |
| `manual` | someone submits its form in the UI (or via the API) | `formId`, `legacyWrapper` |
| `schedule` | the interval comes round | `firstRunAt`, `repeatInterval`, `processMissedRuns` |
| `eventSystem` | a platform event fires | `source`, `topic`, `schema` |

Every trigger also has `name`, `enabled`, `actionType: "automations"` and `actionId` (the automation's `_id`).

### Create a trigger

```
POST /operations-manager/triggers
```

**Endpoint** (start a job from another system):
```json
{
  "name": "Start Backup via API",
  "type": "endpoint",
  "enabled": true,
  "actionType": "automations",
  "actionId": "automation-id-here",
  "routeName": "start-backup",
  "verb": "POST",
  "schema": {
    "type": "object",
    "properties": {"device_name": {"type": "string"}},
    "required": ["device_name"]
  }
}
```

Call it with `POST /operations-manager/triggers/endpoint/start-backup` and `{"device_name": "IOS-CAT8KV-1"}`.

**Manual** (a form in the UI):
```json
{
  "name": "Run Backup Manually",
  "type": "manual",
  "enabled": true,
  "actionType": "automations",
  "actionId": "automation-id-here",
  "formId": "json-form-id-here",
  "legacyWrapper": false
}
```

`formId` is a JSON form's ID. With `legacyWrapper: false`, each form field becomes a job variable of the same name. Run it from the API with `POST /operations-manager/triggers/manual/{triggerId}/run` and `{"formData": {"device_name": "IOS-CAT8KV-1"}}`.

**Schedule** (every 24 hours):
```json
{
  "name": "Nightly Backup",
  "type": "schedule",
  "enabled": true,
  "actionType": "automations",
  "actionId": "automation-id-here",
  "firstRunAt": 1791424800000,
  "repeatInterval": 86400000,
  "processMissedRuns": "none"
}
```

- `firstRunAt` — first run, as epoch **milliseconds** (UTC)
- `repeatInterval` — milliseconds between runs: 3600000 hourly, 86400000 daily, 604800000 weekly
- `processMissedRuns` — `none` skips runs missed while the platform was down; `last` runs the most recent one

### Enable or disable a trigger

```
PATCH /operations-manager/triggers/{triggerId}
{"enabled": false}
```

## Operator Workflows

### Daily check
```
1. GET /operations-manager/tasks?equals[type]=manual&equals[status]=running   → approvals waiting
2. GET /operations-manager/jobs?equals[status]=error                            → failed jobs
3. For each: GET /operations-manager/jobs/{id} → read data.error
4. Retry, fix the input, or escalate
5. GET /operations-manager/jobs?equals[status]=running                          → what's still running
```

### Run a workflow you haven't run before
```
1. GET /operations-manager/automations?contains=keyword&containsField=name   → find it; note componentId and componentName
2. GET /automation-studio/workflows?equals[_id]={componentId}&include=name,inputSchema  → required inputs
3. POST /operations-manager/jobs/start  {workflow: componentName, options: {variables}}
4. GET /operations-manager/jobs/{id}    → poll until it isn't running
5. If status is error: read data.error
```

### Schedule an automation
```
1. GET /operations-manager/automations?contains=...&containsField=name   → its _id
2. POST /operations-manager/triggers                      → type schedule, firstRunAt, repeatInterval
3. GET /operations-manager/triggers/{id}                  → confirm it's enabled and when it runs next (nextRunAt)
```
