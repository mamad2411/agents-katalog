---
name: solution-pipelines
description: Deploy Dataverse solutions across environments via Power Platform Pipelines (deploymentpipeline / deploymentstagerun). Includes pipeline-host discovery, the 3-call Maker-UI workflow, stage-run status code mapping, permission pitfalls, and trade-offs between Pipeline deployment and direct solution export/import. Use when the user wants to promote a solution from dev → staging → prod, or when troubleshooting pipeline runs.
version: 1.0
---

# Solution Deployment via Power Platform Pipelines

Expert reference for deploying Dataverse solutions through Power Platform Pipelines via the dataverse-modelling-mcp server.

## Hard prerequisites

- **Pipeline-Host environment is separate.** The `deploymentpipeline`, `deploymentstage`, and `deploymentstagerun` entities live in a dedicated Pipeline-Host env (often hidden from non-admin users in the BAP environments list). The source/Dev env (where the solution actually lives) does NOT have these entities. All pipeline calls go against the Pipeline-Host URL — never against the source/target.
- **Permission** (on the TARGET env, not the Pipeline-Host): the deploying user must have `prvImportCustomization` on each target environment the pipeline imports into. Without it, **validation itself fails** — the run goes to `stagerunstatus = Fehlgeschlagen` and `validationresults` contains `SecLib::CheckPrivilege failed … PrivilegeName: prvImportCustomization` with the user/BU GUID of the *target* env. Granting the user a Pipeline-Host group/role does NOT help — it must be a role carrying `prvImportCustomization` (e.g. System Customizer) on the target. Verified `2026-06-02`: the same failure occurs identically in the Maker UI, confirming it is purely a target-env permission, not an MCP issue. After a role change allow for security-cache propagation / re-login.
- **Environment write policy** (per project memory): `contoso-dev` writable without confirmation, `contoso-staging` and `contoso-prod` need explicit user confirmation before triggering a pipeline that writes there.
- **⚠️ Token-AppId blocker — headless pipeline deploy via the direct API does NOT currently work** (empirically established `2026-06-02`). The Pipeline-Backend's validation workflow only fires for runs created by the **Power Apps Maker portal** AppId `a8f7a65c-f5ba-4859-b2d6-df772c264e9d`. A run created with any other appid returns HTTP 201 but stays in `Nicht gestartet` forever (validation never starts). The problem: a headless MCP **cannot mint an `a8f7a65c` token** —
  - Device Code Flow directly with `a8f7a65c` → token redemption fails with `AADSTS7000218` (requires a client_secret; not a public client for device-code).
  - FOCI refresh-token exchange to `a8f7a65c` (from Azure CLI `04b07795` or PAC `9cee029c`) → `AADSTS70000` (not in the same client family).
  - The current code authenticates as PAC CLI (`9cee029c`) — that token IS obtainable headlessly but is NOT accepted by the backend → runs hang at `Nicht gestartet`.
  
  So `solution_deploy_pipeline` / `pipeline_auth_init` are effectively non-functional for committing a deploy. The create-payload, sequence, and `DeployPackageAsync` call are otherwise correct (verified call-for-call against a Maker-UI HAR capture). **Recommended deployment path for MCP: the file-based `solution_export` + `solution_import`** (normal Dataverse token, no appid gate). Pipelines remain a Maker-UI (or PAC CLI) operation. Read-only Pipeline calls (`pipeline_list`/`pipeline_stages`/`pipeline_environments`/`pipeline_run_status`) work fine — they are not appid-gated. The Auth-Code + PKCE avenue was also tested (`2026-06-02`) and **fails**: `a8f7a65c` has no manually-capturable redirect URI registered — both `http://localhost` and `https://login.microsoftonline.com/common/oauth2/nativeclient` return `AADSTS50011` (redirect mismatch); only the Maker portal's own web origins are registered, which can't be captured from a CLI. **Conclusion: there is no headless way to obtain an `a8f7a65c` token — `solution_deploy_pipeline` cannot be made to work from a headless MCP. Use file-based export/import instead.**

## Tool map

| User intent | MCP tool |
|---|---|
| List pipelines on a host | `pipeline_list(pipelineHostOrgUrl)` |
| List stages of a pipeline | `pipeline_stages(pipelineHostOrgUrl, pipelineId)` |
| Map Power-Platform env GUID → pipeline-internal `deploymentenvironmentid` | `pipeline_environments(pipelineHostOrgUrl)` |
| Poll a run's status | `pipeline_run_status(pipelineHostOrgUrl, stageRunId)` |
| Check, on the target, that a deployed ribbon change can take effect — before and after the run | `ribbon_scan_unmanaged_layers`, then `ribbon_diagnose(table)` (connected to the target) |
| **Commit a deploy** | *No tool* — removed (see below). Use `solution_export` + `solution_import`, or the Maker UI / PAC CLI. |

> **Note:** the deploy tools `solution_deploy_pipeline`, `pipeline_auth_init` and
> `pipeline_auth_complete` were **removed**. A headless MCP cannot mint the Power-Apps-Maker
> (`a8f7a65c`) token the pipeline backend requires, so a committed deploy never starts. The
> investigation below is kept as background; only the read-only `pipeline_*` calls above are live.
> The `deploymentsettingsjson` / version-bump payloads are documented for anyone re-implementing the
> deploy path outside this server.

## The 3-/4-call Maker-UI workflow

When a user clicks "Bereitstellung" (Deploy) on a stage card in the Maker UI, the browser makes three or four sequential calls (depending on whether the solution has mandatory environment variables / connection references on the target). Our `solution_deploy_pipeline` mirrors them when `autoConfirm=true`. Documented here for the case the tool needs extending.

### Step 1 — POST: create stage run, kick off validation
```http
POST {pipelineHostOrgUrl}/api/data/v9.0/deploymentstageruns?$select=deploymentstagerunid

{
  "artifactname": "<solution-unique-name>",
  "devdeploymentenvironment@odata.bind": "/deploymentenvironments(<devDeploymentEnvironmentId>)",
  "deploymentstageid@odata.bind": "/deploymentstages(<targetStageId>)",
  "makerainoteslanguagecode": "de-DE",
  "solutionid": "<solution-guid-from-source-env>"
}
→ 201 Created
{ "deploymentstagerunid": "<new-run-guid>" }
```

Validation now runs server-side; the row's `stagerunstatus` walks through Nicht gestartet → Überprüfen → Überprüfung erfolgreich. **Skipping steps 2+3 leaves the run hanging at "Nicht gestartet" forever** — this is the trap that the older deprecated `pipelines({id})/Deploy` endpoint never explained.

### Step 2a (optional) — PATCH: set environment variables & connection-reference overrides

Only sent if the solution has any mandatory EnvVars or ConnRefs on the target. The UI shows this as the "Umgebungsvariablen" (environment variables) step in the dialog. Skip when there are none.

```http
PATCH {pipelineHostOrgUrl}/api/data/v9.0/deploymentstageruns({runId})

{
  "deploymentsettingsjson": "{\"EnvironmentVariables\":[{\"SchemaName\":\"sample_my_var\",\"Value\":\"42\"}],\"ConnectionReferences\":[]}"
}
→ 204 No Content
```

The `deploymentsettingsjson` field is a stringified inner JSON. Schema name comes from the env-var's logical name in Dataverse; value is a string regardless of the env-var's actual type (decimal/boolean/etc — Pipeline coerces server-side).

### Step 2b — PATCH: set version + notes
```http
PATCH {pipelineHostOrgUrl}/api/data/v9.0/deploymentstageruns({runId})

{
  "artifactdevcurrentversion": "1.10.0",
  "artifactversion":           "1.11.0",
  "deploymentnotes":           "what changed"
}
→ 204 No Content
```

`artifactversion` is the new version the solution will carry after deploy. Maker UI typically auto-increments the second segment (`1.10.0 → 1.11.0`); we expose it as a required parameter for explicit control.

### Step 3 — POST: actually start the deploy
```http
POST {pipelineHostOrgUrl}/api/data/v9.0/DeployPackageAsync

{ "StageRunId": "<runId>" }
→ 204 No Content
```

The Pipeline-System workflow then takes over: solution gets exported from Dev, imported into the target stage's env. Total runtime observed: ~5–15 min depending on solution size and dependency tree.

## Stage-run status codes

The `stagerunstatus` and `operationstatus` fields use a shared option-set. Always read the `@OData.Community.Display.V1.FormattedValue` annotation for the localized label, but know the codes for code-side logic:

| Code | Label (DE) | Meaning |
|---|---|---|
| 200000000 | Nicht gestartet | Run row created, validation queue not yet entered |
| 200000001 | Wird ausgeführt | Currently active (validation or deploy) |
| 200000002 | Erfolgreich | Terminal — completed without errors |
| 200000003 | Fehlgeschlagen | Terminal — see `validationresults` or `errormessage` |
| 200000004 | Abgebrochen / Cancelled | Terminal — user/system cancelled |
| 200000007 | Überprüfung erfolgreich | Validation OK, awaiting commit (steps 2+3) |
| 200000010 | Bereitstellung wird ausgeführt | Deploy in progress (after step 3) |

`operation` discriminates which sub-phase:
- 200000200 = Kein Wert (initial)
- 200000201 = Überprüfen
- 200000202 = Bereitstellen

## Validation duration & polling

Empirically: validation completes in 5–10 min on solutions with 10–100 components, can climb past 15 min on larger ones. Our service uses a default `validationTimeoutSeconds=600` (10 min) and polls every 10 s; raise both for big solutions. `solution_deploy_pipeline` polls server-side so the MCP call blocks until step 3 fires (or validation fails or times out).

## Permission pitfall — fast diagnosis

Symptom: validation completes but `validationresults` shows:
```
SecLib::CheckPrivilege failed.
User: <systemuserid>,
PrivilegeName: prvImportCustomization
```

The user-GUID in the error message is the **calling user on the target env**. Cross-check against an admin account. The error is fatal for the run — start a new one with the admin token.

## Pipeline vs. direct export/import — trade-offs

| Aspect | Pipeline | `solution_export` + `solution_import` |
|---|---|---|
| Audit / history | Auto-logged in `deploymentstagerun` | Manual notes only |
| Stage enforcement (Dev → Stage → Prod order) | Yes | No |
| Approval gates | Configurable per stage | None |
| Version bumping | Mandatory new `artifactversion` | Solution version is whatever the export says |
| Speed for ad-hoc | Slow (5–15 min) | Fast (1–3 min) |
| Works without Pipelines installed | No | Yes |
| Solution stays managed-only on target | Yes by default | Configurable |
| Auth | Maker-AppId token (Device Code Flow, `pipeline_auth_init`) | Regular Dataverse token — no extra login |

**Default to Pipeline** when staging/prod targets are involved. Use direct export/import for throwaway envs (`service-test`), bulk migrations, or — importantly — **as the robust fallback when host-managed Pipelines misbehave** (validation/auth/deploy issues).

### Direct export/import — capabilities (since 2026-06-01)

- **`solution_export(uniqueName, managed, filePath?)`** — with `filePath` the zip is written to local disk and only the path + byte size come back; without it the base64 is returned inline. Use `filePath` for large solutions to avoid pumping megabytes of base64 through the MCP channel.
- **`solution_import(filePath? | zipBase64?, overwriteUnmanaged, timeoutSeconds=600)`** — runs the **async** `ImportSolutionAsync` action (not the timeout-prone sync `ImportSolution`), polls the `asyncoperation` until terminal, and returns `Success` (driven by async statuscode 30) plus `ComponentErrors[]` parsed from the ImportJob's `data` XML. Provide `filePath` to read the zip from disk (preferred) or `zipBase64` inline.
- Architecture note: the **PAC CLI was deliberately NOT used** as the engine (own auth store, external-process dependency). If deeper SDK features are ever needed, the **`ServiceClient` SDK with `tokenProviderFunction`** (reuses `DataverseTokenProvider`) is the preferred next step — not the CLI. See memory `project_solution_import_export_architecture`.

## Environment reference values (example)

Illustrative placeholders showing the shape of a pipeline setup. All IDs are tenant-specific — resolve the real values for your own environment with `pipeline_environments(...)` before relying on them.

| Item | Value |
|---|---|
| **Pipeline-Host org URL** | `https://orgexample.crm4.dynamics.com` |
| Pipeline "Example" `deploymentpipelineid` | `10000000-0000-0000-0000-000000000001` |
| Stage "contoso-staging" `deploymentstageid` | `20000000-0000-0000-0000-000000000002` (first stage, `previous=null`) |
| Stage "contoso-prod" (Prod) `deploymentstageid` | `20000000-0000-0000-0000-000000000003` (`previous=contoso-staging`) |
| Dev-env mapping (contoso-dev) `deploymentenvironmentid` | `30000000-0000-0000-0000-000000000004` |
| contoso-dev Power-Platform `environmentid` | `40000000-0000-0000-0000-000000000005` |
| Admin account with `prvImportCustomization` | `admin@contoso.com` |

The `deploymentenvironmentid` (pipeline-internal mapping row id) is NOT the Power-Platform env GUID. Resolve via `pipeline_environments(pipelineHostOrgUrl)` and filter by `EnvironmentId` if you only know the PP env GUID.

## Typical workflows

### "Deploy ContosoSales from contoso-dev → contoso-staging"
1. Capture current solution version: `mcp__dataverse-modelling-mcp__solution_get(uniqueName='ContosoSales')` → `version` (e.g. `1.10.0`).
2. Compute target version (typically bump second segment: `1.10.0 → 1.11.0`).
3. Confirm contoso-staging write with the user (per project memory).
4. `solution_deploy_pipeline(pipelineHostOrgUrl, solutionId, artifactName='ContosoSales', devDeploymentEnvironmentId, targetStageId=<contoso-staging>, currentVersion='1.10.0', newVersion='1.11.0', deploymentNotes='<reason>', autoConfirm=true)` — blocks ~6–10 min, returns `stageRunId`.
5. Poll `pipeline_run_status(pipelineHostOrgUrl, stageRunId)` until `stagerunstatus = Erfolgreich` (or Fehlgeschlagen).
6. On success: solution and its components (cloud flows, tables, etc.) are now in contoso-staging as managed.

### "Validate without deploying"
Same as above but `autoConfirm=false`. Tool returns immediately after step 1 with the runId. Inspect `pipeline_run_status` until `stagerunstatus = Überprüfung erfolgreich` and read `validationresults` JSON — useful to preview which components will be imported and to catch missing dependencies before committing.

### "Diagnose a failed run"
1. `pipeline_run_status(pipelineHostOrgUrl, stageRunId)` → look at `stagerunstatus@…FormattedValue` and `operationstatus@…FormattedValue`.
2. Parse `validationresults` JSON: `SolutionValidationResults[].Message`. For permission errors the user-GUID is in that string. For missing dependencies, `MissingDependencies` lists what's not in the target.
3. Common causes: missing `prvImportCustomization`, connection references not yet present on target, dependent solutions not yet deployed, target env not "managed-environment-enabled" (Pipeline UI shows a banner about this).

### "Roll back a deployed solution"
Pipelines do **not** offer one-click rollback. Options:
- Trigger a new pipeline deploy with an older `solutionid` snapshot (requires keeping snapshots in dev).
- Use solution layers (`solution_remove_active_layer`) to peel off the most recent unmanaged layer if the previous managed solution is still intact.
- Direct import of an older managed solution file (bypasses Pipeline audit but is fastest).

## Reverse-engineered endpoints (Maker UI parity)

Documented for the rare case the wrappers need extending.

| Call | URL | Method |
|---|---|---|
| List pipelines | `/api/data/v9.2/deploymentpipelines` | GET |
| List stages of a pipeline | `/api/data/v9.2/deploymentstages?$filter=_deploymentpipelineid_value eq {id}` | GET |
| Env mapping rows | `/api/data/v9.2/deploymentenvironments` | GET |
| Create stage run + start validation | `/api/data/v9.0/deploymentstageruns?$select=deploymentstagerunid` | POST |
| Set version + notes | `/api/data/v9.0/deploymentstageruns({runId})` | PATCH |
| Kick off actual deploy | `/api/data/v9.0/DeployPackageAsync` | POST |
| Poll a run's status | `/api/data/v9.0/deploymentstageruns({runId})?$select=stagerunstatus,errormessage,operation,operationdetails,operationstatus,validationresults,...` | GET |

API-version inconsistency (v9.2 for read, v9.0 for the run-creation + deploy actions) is intentional Microsoft-side — keep both.

## Pitfalls

- **Run hangs at "Nicht gestartet" forever** if you only do step 1. Always follow with PATCH + DeployPackageAsync (or use `autoConfirm=true`). The deprecated `pipelines({id})/Deploy` endpoint that older MCP code used is dead; do not call it.
- **`DeployPackageAsync` is unbound**, despite naming. Don't try `/deploymentstageruns({id})/DeployPackageAsync` — fails. It takes `StageRunId` in the body.
- **`api-version=2016-11-01` is wrong**. Pipelines use Dataverse Web API (`/api/data/v9.0` or `/api/data/v9.2`), not the PA Flow API.
- **outputsLink-style retrieval doesn't apply**. Stage-run details come back directly on GET — no SAS-signed URL juggling like flow run actions need.
- **A green run does not mean a changed ribbon button reaches the users.** Two things can stop it, and
  neither shows in the run:
  - An unmanaged ribbon layer on the target overrides the managed deployment. It cannot be removed,
    only overwritten (`ribbon_sync_unmanaged_layer`).
  - The server keeps delivering the old client ribbon until the table's metadata changes
    (`ribbon_refresh_client_metadata`).

  After deploying a ribbon change, run `ribbon_diagnose` for the table on the target. The command-bar-buttons skill
  has the details.
- **`0x80071151 "Cannot start another [Import]"`** while Microsoft updates its own `msdyn_*` solutions
  on the environment — a chain that can run for ten minutes and more. Every import and publish is
  refused meanwhile; wait and retry. To see what runs, read `msdyn_solutionhistories` with
  `$orderby=msdyn_starttime desc&$top=10`: a filter on `msdyn_starttime` is silently ignored, and
  thousands of old rows have no `msdyn_endtime`, so "no end time" is no sign of a running operation.

## Related memories

- See [[feedback_environment_write_policy]] for contoso-dev vs contoso-staging/contoso-prod write confirmations.
- See `cloud-flows` skill for editing the cloud-flow content (FetchXML, action inputs) before deploying.
