---
name: cloud-flows
description: Work with Power Automate solution-aware Cloud Flows on Dataverse — inspect, save draft, publish, restore versions, trigger runs, debug action outputs, and patch FetchXML / action inputs surgically. Includes a compact iteration workflow for safe edit-test-publish cycles, and FetchXML guidance (rollup trade-offs, comment pitfalls, aggregate limits) for classification flows. Use when the user asks about Power Automate cloud flows in a Dataverse environment.
version: 1.1
---

# Cloud Flows on Dataverse

Expert reference for managing **solution-aware** Power Automate cloud flows via the dataverse-modelling-mcp server.

## Hard prerequisites

- **Only solution-aware flows have version history.** Flows in the default solution get no `componentversion` rows. If a flow is missing from version-history queries, check that it belongs to a non-default solution (`solutioncomponents` filtered on `objectid eq <flowid>`).
- **Environment write policy:** `contoso-dev` is the safe write target. `contoso-prod` (production) and `contoso-staging` need explicit user confirmation before any mutating call.
- **The `componentversion` virtual entity refuses direct Create.** The Microsoft Learn doc lists Create as supported, but every POST/PATCH against `/componentversions` or the elastic backing table `/componentversionnrddatasourceset` fails. The bound actions documented below are the only working write path.

## Tool map

| User intent | MCP tool | Underlying call |
|---|---|---|
| List flows | `flow_list` | Power Automate Flow API |
| Inspect single flow | `flow_get`, `flow_describe` | Power Automate Flow API |
| **Get raw clientdata (with `connectionReferences` wrapper)** | `flow_get_clientdata` | Dataverse `GET /workflows({id})?$select=clientdata` |
| **Create solution-aware flow (version history + draft/publish)** | `flow_create(…, solutionUniqueName=…)` | Dataverse `POST /workflows` (category=5, type=1) |
| Create personal flow (no versioning) | `flow_create(…)` without `solutionUniqueName` | Power Automate Flow API |
| List version history | `flow_list_versions` | Dataverse `GET /workflows({id})/componentversions` |
| Inspect single version | `flow_get_version` | Filtered list (direct GET-by-key is blocked) |
| **Save a draft (Op=1 Update version)** | `flow_save_draft` | `PATCH /workflows({id})` + header `mscrm.AsUnpublished: true` |
| **Publish current draft (Op=2 Publish version)** | `flow_publish` | `POST /PublishComponent?ActivateFlowOnPublish=<bool>` |
| **Save draft + publish in one call** | `flow_save_draft_and_publish` | combined PATCH + PublishComponent |
| **Surgical update of one action input** | `flow_patch_action_input` | GET clientdata → mutate one key under `actions.<X>.inputs.parameters` → save draft (optional publish) |
| **Validate a FetchXML against Dataverse** | `fetchxml_validate` | `GET /{entitySet}?fetchXml=<xml>` read-only |
| Activate/deactivate at runtime (no snapshot) | `flow_set_state` | Power Automate `/start` or `/stop` |
| **Restore a prior published version (Op=3 Restore)** | `flow_restore_version` | `POST /workflows({id})/Microsoft.Dynamics.CRM.RestoreComponentVersion` |
| Get run history | `flow_get_runs` | Power Automate Flow API |
| **Trigger a flow run** | `flow_trigger_run` | `POST .../triggers/{triggerName}/run` |
| **Wait until a run reaches a terminal state** | `flow_wait_for_run` | Polls `GET .../runs/{runId}` until status != Running |
| **List actions of a single run (status + outputsLink)** | `flow_get_run_actions` | `GET .../runs/{runId}/actions` |
| **Fetch the raw outputs of one action** | `flow_get_action_outputs` | resolves SAS-signed outputsLink — no Bearer header |

## Conceptual model

The `workflow` row carries the **live** flow. Alongside it, the virtual `componentversion` view exposes snapshots. Each snapshot has an `Operation` discriminator:

| Operation | Label | Triggered by |
|---|---|---|
| 0 | Create | Initial flow creation |
| 1 | Update | `flow_save_draft` (PATCH with `mscrm.AsUnpublished: true`) |
| 2 | Publish | `flow_publish` (POST `PublishComponent`) |
| 3 | Restore | `flow_restore_version` |
| 4 | Solution Import | Solution-import pipeline |

**Restore semantics:** `RestoreComponentVersion` only acts on **Publish-typed (Op=2)** versions. Calls against Create/Update IDs return HTTP 204 but produce no observable change.

**Publish vs. Activate:** independent. `flow_publish` snapshots the draft as the new published version but leaves the runtime state unchanged. `ActivateFlowOnPublish=true` combines both. `flow_set_state` toggles runtime alone without touching version history.

## Solution-flow patch & test workflow

The full iteration cycle for a safe edit on `contoso-dev`, with MCP tools alone (no PowerShell escape hatches required for the common path):

1. **Inspect** — `flow_get` to confirm the action name and current shape. For full `clientdata` (incl. `connectionReferences`), `flow_get_clientdata`. `flow_list_versions(flowId)` to note the last good Op=2 version-id as rollback anchor.
2. **Edit** — choose the smallest path that fits:
   - One parameter on one action (most edits): `flow_patch_action_input(flowId, actionName, parameterName, valueJson, publish=false)`. Avoids round-tripping the full clientdata.
   - Multi-action / structural change: `flow_get_clientdata` → mutate locally → `flow_save_draft` (or `flow_save_draft_and_publish`).
3. **Pre-flight FetchXML changes** — `fetchxml_validate(entitySet, fetchXml, sampleSize)` against the active org before patching it into a List action. Catches well-formedness errors (e.g. `--` in comments) and reports the row count to be classified.
4. **Publish** — `flow_publish(flowId, activateFlow=false)` (or pass `publish=true` directly to `flow_patch_action_input`). Confirm via `flow_list_versions` that a new Op=2 row landed and `connectionReferences` is still populated.
5. **Trigger** — `flow_trigger_run(flowId, triggerName)`. For Recurrence-triggered flows, `triggerName="Recurrence"` is the canonical name.
6. **Wait** — `flow_wait_for_run(flowId, runId, timeoutSeconds=300)`. Blocks server-side until terminal state.
7. **Validate the run** — `flow_get_run_actions(flowId, runId)` lists every action's status; for any `Failed` row, follow its `OutputsLink` via `flow_get_action_outputs(flowId, runId, actionName)` to get the error body (Dataverse error code, BadRequest message, etc.). For Compose-style telemetry actions, fetch the same way and inspect the produced JSON / HTML.
8. **Rollback if needed** — `flow_restore_version(flowId, <lastGoodOp2Id>)` then `flow_publish`. Restore produces an Op=3 row pointing at the source for audit.

Single-action edits commonly compress to two tool calls: `fetchxml_validate` (read-only) followed by `flow_patch_action_input(..., publish=true)`.

## FetchXML inside classification / lifecycle flows

When a flow drives lifecycle decisions via FetchXML against `accounts` / `contacts` etc., a handful of dataverse-specific traps recur. Each carries a trade-off — none of these is a hard ban, but the consequences should be conscious.

### Rollup-field reliance — convenient but lagged

Dataverse rollup fields like `sample_open_opportunities` or `sample_number_orders` are **asynchronously recomputed**. Real lag observed: minutes to hours, sometimes longer for cold accounts. They can be stale in either direction:
- A new opportunity exists but `sample_open_opportunities` still shows `0`.
- A record's rollup was never computed → the field is **`null`**, not `0`. `condition operator='eq' value='0'` then matches nothing.

**Trade-off**: rollups are cheap (single attribute, no join), and for thresholds like `eq 1` or `ge 2` they are essentially the only practical option (see below). For *existence* checks they can quietly mis-classify records.

**When to prefer an outer-join existence check** (`<link-entity ... link-type='outer' alias='X'>` + `condition entityname='X' attribute='<id>' operator='null'/'not-null'`):
- The check is the *only thing* gating a destructive / overwriting classification (e.g. „has zero open opps" used to mark `Verlorener Potentialkunde`).
- The records are recent / volatile (frequently changing leads, opps, orders).
- A wrong classification has measurable downstream cost.

**When the rollup is fine**:
- Threshold semantics that an existence-check cannot express (`exactly 1`, `>= 2`).
- A higher-priority phase in the same flow will overwrite an incorrect classification anyway (e.g. `A` after `N` covers stale `sample_number_orders eq 1` for accounts that actually have 2+ orders).

### Aggregate FetchXML — no cross-entity HAVING

FetchXML supports `aggregate='true'` with `groupby` and `aggregate='countcolumn'` on a linked entity. Documentation suggests aggregate aliases can be used as filters. **In practice, an aggregate-alias condition on a cross-entity outer-join is rejected** by Dataverse:

```xml
<!-- This is "Attribute not found in XNode" or value-coerced-to-GUID error -->
<filter><condition alias='ordercount' operator='ge' value='2' /></filter>
```

What works:
- Boolean existence on the outer-join: `<condition entityname='oa' attribute='salesorderid' operator='not-null' />` (≥1) or `'null'` (=0).
- Numeric threshold via the rollup field on the parent entity itself (`<condition attribute='sample_number_orders' operator='ge' value='2' />`) — same trade-off as above.
- Aggregate-alias HAVING on the **same entity** (no joins) — that case works as documented.

For „exactly N" or „at least N≥2" cross-entity, you either accept the rollup-field dependency or accept a structural workaround (e.g. two outer-joins with disjoint filters to prove ≥2 distinct rows, at the cost of edge cases that match neither).

### XML-comment pitfall: `--` is invalid

Per W3C, an XML comment may not contain `--`. Dataverse parses FetchXML strictly:

```xml
<!-- Verlorener Potentialkunde (772600007)  -- NEU -->  <!-- ❌ rejected: "Invalid XML." -->
```

Easy to overlook in dash-separated section headers. `fetchxml_validate` catches this pre-flight.

### Sending emails from a flow (Dataverse connector)

The Dataverse connector supports inline activity parties on email creation — via a specific op/parameter combination:

- Use `operationId: CreateRecordWithOrganization` (**not** `CreateRecord`) and pass `organization: "current"` in parameters.
- The parameter is named `item/activitypointer_activity_parties` (**not** `item/email_activity_parties`). The latter triggers `InvalidOpenApiFlow / WorkflowOperationParametersExtraParameter`.
- Inline array shape:
  ```jsonc
  "item/activitypointer_activity_parties": [
    { "participationtypemask": 1, "partyid@odata.bind": "/systemusers(<sender-guid>)" },
    { "participationtypemask": 2, "partyid@odata.bind": "/systemusers(<recipient-guid>)" },
    { "participationtypemask": 2, "addressused": "team@example.com" }
  ]
  ```
  `addressused` works for distribution lists / shared mailboxes without resolving a systemuser.
- Send via `PerformBoundAction`, `actionName: Microsoft.Dynamics.CRM.SendEmail`, `item/IssueSend: true` (false = mark sent in CRM without SMTP delivery).
- Reference flow (example): a scheduled nightly cloud flow, workflowid `50000000-0000-0000-0000-000000000006`.

## Reverse-engineered endpoints (Maker UI parity)

These came from Playwright network traces of `make.powerautomate.com` and are now wrapped by the MCP tools. Documented here for the rare case the wrapper needs extending — most work belongs in the service layer, not in tool callers.

### Restore (bound action on workflow)
```http
POST /api/data/v9.2/workflows({flowId})/Microsoft.Dynamics.CRM.RestoreComponentVersion
Content-Type: application/json

{"RestoringVersionId": "componentversions(<componentversionId>)"}
```
- Parameter name is **PascalCase**. A C# anonymous object `new { RestoringVersionId = ... }` gets serialized as `restoringVersionId` by the shared `JsonSerializerOptions` (CamelCase policy) and rejected. Use a `Dictionary<string, object?>`.
- Returns 204 even when the snapshot wasn't actually applied — verify via re-list.

### Publish (unbound action)
```http
POST /api/data/v9.2/PublishComponent?ActivateFlowOnPublish=false
Content-Type: application/json

{"Target": "/workflows({flowId})"}
```

### Save draft (direct PATCH with special header)
```http
PATCH /api/data/v9.2/workflows({flowId})
Content-Type: application/json
mscrm.AsUnpublished: true
If-Match: *

{"clientdata": "<stringified-logic-apps-json>", "name": "..."}
```
- Without `mscrm.AsUnpublished`, the PATCH may try to validate/publish immediately and fail.
- A second header `mscrm.SkipComponentVersioning: true` is what the Maker UI uses in the publish-batch's first PATCH to avoid double-versioning; do **not** add it to plain Save-draft calls — it would suppress the Update version row entirely.

### Manual run (PA Flow API)
```http
POST https://{region}.api.flow.microsoft.com/providers/Microsoft.ProcessSimple/environments/{envId}/flows/{flowId}/triggers/{triggerName}/run?api-version=2016-11-01
```
- Returns 200 with no usable body. Read the new RunId by listing runs (`/runs?$top=1`) right after.

### Action outputs (per-action endpoint — stable)
```http
GET .../flows/{flowId}/runs/{runId}/actions/{actionName}?api-version=2016-11-01
```
- Returns `properties.outputsLink.uri` — a SAS-signed URL. Download it **without** a Bearer header; otherwise `DirectApiRequestHasMoreThanOneAuthorization`.
- Prefer this over `GET .../runs/{runId}?$expand=properties/actions`, which intermittently returns ASP.NET runtime-error HTML.

## General pitfalls

- **`clientdata` is a stringified JSON**, not nested JSON. When constructing it manually, the inner `properties.definition` block must use Logic Apps keys `$schema`, `$connections`, `$authentication` — verbatim with dollar signs. Don't try to coerce them via `string.Replace`; build the JSON literal directly (raw string interpolation in C# works well).
- **Manual trigger schema:** the Request trigger's `inputs.schema` must be a JSON-schema object (`{"type":"object","properties":{},"required":[]}`), not an empty `{}`.
- **Direct OData PATCH on `clientdata` bypasses versioning.** It modifies the live flow without creating a `componentversion` row. To get a proper Update snapshot, go through `flow_save_draft` (or any wrapper that includes the `mscrm.AsUnpublished: true` header).
- **Composite key lookups are blocked:** `GET /componentversions({id})` and `GET /workflows({wfid})/componentversions({verId})` both fail with "Get with NavigationKey is allowed only on Metadata Entities." Resolve a single version by listing and filtering client-side.
- **`RestoreComponentVersion` is async.** After calling it, give Dataverse 1–2 seconds before re-listing versions to assert the Op=3 row exists.
- **External PA-MCP `update_flow` corrupts solution-aware flows.** It transforms `connectionReferences` into the flat Flow-API shape and loses `connectionReferenceLogicalName`, leaving every `OpenApiConnection` action broken. Always use the dataverse-modelling-mcp save-draft path for solution-aware flows.

## Typical workflows

### "Roll a flow back to yesterday's published version"
1. `flow_list_versions(flowId)` → identify the target row where `Operation == 2` and `CreatedOn` matches.
2. `flow_restore_version(flowId, versionId)` — produces a new Op=3 row and a fresh Draft on the workflow.
3. (Optional) `flow_publish(flowId, activateFlow=true)` to re-publish-and-activate immediately.

### "Replace the FetchXML of one List action"
1. `fetchxml_validate(entitySet="accounts", fetchXml=<new>, sampleSize=3)` — well-formed? row count plausible?
2. `flow_patch_action_input(flowId, actionName="List_Lost_Customers", parameterName="fetchXml", valueJson="\"<the new xml>\"", publish=true)` — saves draft and publishes in one go.
3. `flow_trigger_run(flowId, "Recurrence")` → `flow_wait_for_run(flowId, runId)` → `flow_get_run_actions(flowId, runId)`.

### "Apply a small edit safely without breaking the active flow"
1. `flow_get(flowId)` to confirm structure (or `flow_get_clientdata` for the full wrapper).
2. `flow_patch_action_input(...)` (no publish) — creates Op=1 Update version, runtime unaffected.
3. Inspect & test via run, then `flow_publish(flowId)` when ready.

### "Disable a noisy flow temporarily"
- `flow_set_state(flowId, enable=false)` — stops runs without changing version history. Re-enable later with `enable=true`.

### "Audit who changed what"
- `flow_list_versions(flowId)` returns each row with `CreatedByName`, `Operation`, `CreatedOn`.

## Related memories

- See [[feedback_environment_write_policy]] for the contoso-dev vs contoso-prod/contoso-staging write rules.
