---
name: aevatar-scheduled-agent-key-canary
description: Use when an authenticated Aevatar user asks whether scheduled Studio Team member workflows can run with a dedicated NyxID Agent Key, especially for production checks involving cron origin, credential use, or cleanup readiness.
version: "1.0"
metadata:
  category: tool-based
  tool-list:
    - aevatar_create_team
    - aevatar_create_member
    - aevatar_bind_member_workflow
    - aevatar_schedule_member_workflow
    - aevatar_get_member
    - aevatar_get_schedule
    - aevatar_list_schedules
    - nyxid_services
    - nyxid_api_keys
    - nyxid_proxy
    - code_execute
  tag:
    - aevatar
    - nyxid
    - agent-key
    - cron
    - schedule
    - canary
    - diagnostics
---

# Verify scheduled Agent Key execution

## Outcome contract

Treat this canary as an account-scoped check of the current authenticated user, owner LLM selection, and production configuration. Do not describe it as platform-wide health.

CLEANUP_INCOMPLETE if any created resource is not terminal or terminal state is unknown.
PASS only if authorization, real cron, marker, exact-key-use, and cleanup are all true.
FAIL otherwise, with featureConclusion=not_evaluated for pre-mutation prerequisites and featureConclusion=failed for an executed canary failure.

Start the final response with exactly one verdict. Use `featureConclusion=passed` only with `PASS`. Give `CLEANUP_INCOMPLETE` precedence over a feature result whenever cleanup is incomplete or unknown.
For `CLEANUP_INCOMPLETE`, set `featureConclusion=not_evaluated` if feature evidence was never collected, `featureConclusion=failed` if executed feature evidence failed, or `featureConclusion=passed` if all feature evidence passed but cleanup remains incomplete.

## Stop conditions

- Stop before mutation with `FAIL` and `featureConclusion=not_evaluated` when authentication, trusted `scopeId`, an exact active Aevatar UserService, an explicit active owner LLM selection, or a required tool is unavailable.
- Stop before mutation when the fixed clock probe fails, an allowlisted route or typed field differs from the connected service contract, the exact Team/member/draft absence checks are inconclusive, or canonical credential-aware deletion is unavailable. Require `DELETE /api/schedules/{scheduleId}` to accept the exact owner plus both `operationId` and `idempotencyKey`, and require exact-body replay to be the retry contract. Use `PREREQUISITE_CREDENTIAL_REVOCATION_SURFACE_UNAVAILABLE` when that lifecycle surface is absent or incompatible.
- Stop without mutation when the caller declines the single confirmation. Return `FAIL`, `featureConclusion=not_evaluated`, and `errorCode=CONFIRMATION_DECLINED`.
- Fail closed when an identity is missing, owner scope is ambiguous, or Agent Key correlation returns zero or multiple candidates.
- Finish every response before the eighth local tool round and before 300 seconds. Return a completed resumable response before either limit.
- Never call `run-now`, an unowned or generic schedule mutation, `aevatar_provision_workflow_schedule`, the legacy `scheduled_agent_creator`, or direct NyxID Agent Key create/update/delete operations.
- Begin cleanup after executed evidence collection whether the feature succeeds or fails. Preserve the member, draft, and Team while automation revocation remains pending.

## Confirmation and phased continuation

Perform read-only prerequisite inspection first. Then request one concise confirmation covering all effects: create a temporary Team, workflow member, workflow draft/binding, and annual schedule; allow one owner LLM call; wait for a real cron fire; revoke the dedicated Agent Key; retire the revision; delete the member and draft; and archive the Team.

Treat a line-leading `::aevatar-scheduled-agent-key-canary confirm/start` continuation as confirmation. If the caller declines, end without mutation with `FAIL`, `featureConclusion=not_evaluated`, and `errorCode=CONFIRMATION_DECLINED`. Use the returned `previous_response_id` from the immediately preceding completed response and require the same authenticated caller and response session.
Until the caller explicitly confirms or declines, emit only the confirmation request plus `confirmationStatus=pending`. Do not emit `PASS`, `FAIL`, `CLEANUP_INCOMPLETE`, `featureConclusion`, an error code, or a checkpoint. Silence or an unanswered confirmation is pending, not a decline.

Advance through these completed checkpoints:

| Checkpoint | Required condition | Next line-leading command |
| --- | --- | --- |
| `PREREQUISITES_CONFIRMED` | Read-only prerequisites passed and the caller confirmed | `::aevatar-scheduled-agent-key-canary continue` |
| `BINDING_READY` | Exact member binding is read-model visible | `::aevatar-scheduled-agent-key-canary continue` |
| `CANARY_ARMED` | Exact automation and one unique unused key candidate are ready | `::aevatar-scheduled-agent-key-canary continue` no earlier than 15 seconds after the target minute starts |
| `REVOCATION_STARTED` | Evidence was collected and exact automation deletion was accepted | `::aevatar-scheduled-agent-key-canary continue` |

Emit each checkpoint only after its condition is true. End the response immediately after the checkpoint and continuation instruction. If binding, fire evidence, or revocation needs more observation than the current response safely permits, return a completed progress response with the last achieved checkpoint and exact next command; reread exact identities on continuation and never duplicate a mutation.

Compute `targetFireAtUtc` only after `BINDING_READY`. Make it at least eight full minutes ahead. In `CANARY_ARMED`, tell the caller the exact earliest continuation time: 15 seconds after the target minute begins.

## Exact identities and checkpoint ledger

Keep `scopeId`, `teamId`, `memberId`, `draftWorkflowId`, `publishedServiceId`, `revisionId`, `bindingRunId`, `scheduleId`, `runId`, and `agentKeyId` semantically distinct. Never infer one from another, assume equality, use display-name similarity, or put `draftWorkflowId` into a member API.

Derive visibly distinct caller-supplied IDs from the fixed random suffix:

- `teamId=team-canary-<suffix>`
- `memberId=m-canary-<suffix>`
- `draftWorkflowId=wf-canary-<suffix>`

Derive unique Team, member, and schedule display names and the workflow marker from the same suffix. Before the first cleanup DELETE, derive one fresh `deleteOperationId` and `deleteIdempotencyKey`, record them, and reuse the unchanged pair, owner tuple, and reason for the first canonical DELETE and every replay.

Carry only these labelled, non-secret checkpoint fields when known:

```text
scopeId
teamId
memberId
draftWorkflowId
publishedServiceId
revisionId
bindingRunId
scheduleId
runId
agentKeyId
targetFireAtUtc
deleteOperationId
deleteIdempotencyKey
lastUsedAtBeforeShape=null|timestamp
lastUsedAtAfterShape=null|timestamp
```

The schedule-create tool's internal operation and idempotency identities are not public. Never reconstruct, output, or checkpoint them. Do not place the suffix, marker, raw key, bearer token, Vault reference, credential ciphertext, refresh token, permission digest, complete inventory, or raw tool response in a checkpoint.

Resume a lost-context continuation only from this labelled ledger plus owner-correct reads. If missing non-ledger context prevents marker or before-state proof, fail the feature closed, perform all cleanup supported by exact ledger identities, and never rediscover by display name.

## Allowed tools and routes

Use only the tools declared in frontmatter. Use `nyxid_services` to resolve exact active UserServices, `nyxid_api_keys` only for bounded inventory reads, and `code_execute` only for the three fixed snippets in this skill.

Use these typed calls exactly:

```text
aevatar_create_team:
  display_name, description, caller-supplied team_id=team-canary-<suffix>

aevatar_create_member:
  display_name, implementation_kind=workflow, team_id=<teamId>,
  description, caller-supplied member_id=m-canary-<suffix>

aevatar_bind_member_workflow:
  member_id=<memberId>, workflow_yaml=<exact YAML>,
  workflow_id=wf-canary-<suffix>

aevatar_schedule_member_workflow:
  member_id=<memberId>, schedule_cron=<annual cron>,
  schedule_timezone=UTC, prompt=<marker>, display_name=<unique schedule name>
```

Use `aevatar_get_member` with only the exact `member_id`. Use `aevatar_list_schedules` and `aevatar_get_schedule` with the exact `team_id`, `member_id`, and, for detail, `schedule_id`.

For every `nyxid_proxy` call, supply the exact active Aevatar `service_id` and `slug=aevatar`. Permit only these method/path pairs:

```text
GET    /api/user-config/llm
GET    /api/scopes/{scopeId}/teams/{teamId}
GET    /api/workspace/workflow-drafts/{draftWorkflowId}?scopeId={scopeId}
GET    /api/schedules?ownerKind=studio_member_automation&ownerScopeId={scopeId}&ownerTeamId={teamId}&ownerMemberId={memberId}
GET    /api/schedules/{scheduleId}?ownerKind=studio_member_automation&ownerScopeId={scopeId}&ownerTeamId={teamId}&ownerMemberId={memberId}
GET    /api/scopes/{scopeId}/members/{memberId}/runs?take=10&scheduleId={scheduleId}&updatedFrom={utc}
DELETE /api/schedules/{scheduleId}
POST   /api/scopes/{scopeId}/members/{memberId}/binding/revisions/{revisionId}:retire
DELETE /api/scopes/{scopeId}/members/{memberId}
DELETE /api/workspace/workflow-drafts/{draftWorkflowId}?scopeId={scopeId}
POST   /api/scopes/{scopeId}/teams/{teamId}/archive
```

`/api/schedules` is the canonical schedule lifecycle surface. Nested Team automation HTTP is preflight-only and is not a list, detail, delete, or retry surface. Never use the rejected legacy `scopeId/teamId/memberId` schedule query shape and never call a second fire-diagnostic route.

Treat the two read shapes as separate contracts:

| Surface | Exact shape |
| --- | --- |
| `aevatar_get_schedule` | Flat snake_case fields with string lifecycle values, including `authorization_status`, `credential_source_kind`, `next_fire_at`, `last_fire_at`, `revocation_pending`, and `state_version`. |
| Canonical owner detail through `nyxid_proxy` | Raw camelCase `{ "schedule": { ... }, "recentFires": [ ... ] }`. `schedule.teamAutomationLifecycleStatus` is numeric (`Active=2`, `RevocationPending=6`), `schedule.credentialSourceKind` is numeric (`ScheduledInvocationAgentKey=6`), and owner LLM, recurrence, revocation-track, and fire fields remain beneath `schedule` or `recentFires`. |

Use the flattened tool fields for string lifecycle assertions. Use canonical raw detail for exact owner fields, owner LLM fields, `scheduleMode`, `oneShotFireAt`, `completed`, NyxID/Vault revocation tracks, and `recentFires`. Never apply a flattened field name to the raw response or a raw numeric enum rule to the flattened tool response.

## Phase 1 — inspect prerequisites and confirm

1. Resolve the trusted current `scopeId`. Require authenticated Aevatar and NyxID access.
2. Resolve one exact active Aevatar UserService with `nyxid_services`. If several candidates remain and the connected context does not designate one, stop and ask the caller to select the exact service.
3. Call `GET /api/user-config/llm` through that exact Aevatar UserService. Require an explicit owner LLM route, model, and `UserService.id`; require the selected owner LLM UserService to be active and exact in `nyxid_services`.
4. Confirm the connected tool schemas, canonical owner-aware list/detail paths, raw `{schedule,recentFires}` shape, flattened `aevatar_get_schedule` shape, canonical DELETE body, replay semantics, receipt fields, and expected status codes match this skill. The DELETE body must accept only `reason`, `operationId`, `idempotencyKey`, and the typed owner object for this branch; the receipt must expose only non-secret admission facts. Fail closed on drift and do not probe a mutation to discover the contract.
5. Run this exact pre-mutation `code_execute` probe:

```python
from datetime import datetime, timezone
import secrets

now = datetime.now(timezone.utc)
suffix = secrets.token_hex(4)
marker = f"AEVATAR_AGENT_KEY_CANARY_{suffix}"
print(now.isoformat(), suffix, marker)
```

6. Derive the distinct IDs and non-secret labels. Require owner-correct absence of the exact `teamId`, `memberId`, and `draftWorkflowId`: Team GET must be 404, `aevatar_get_member` must report not found, and draft GET must be 404. Do not accept a name search.
7. Read a baseline with `nyxid_api_keys`. Retain only the fields needed for ID-delta correlation; never copy the complete inventory into output.
8. Present the one confirmation with `confirmationStatus=pending` and end the response without a verdict, `featureConclusion`, error code, or checkpoint. After the caller continues with `confirm/start`, emit `PREREQUISITES_CONFIRMED` without performing a mutation in that response.

Use stable prerequisite codes such as `PREREQUISITE_AUTH_UNAVAILABLE`, `PREREQUISITE_SCOPE_UNAVAILABLE`, `PREREQUISITE_CODE_EXECUTE_UNAVAILABLE`, `PREREQUISITE_OWNER_LLM_UNAVAILABLE`, `PREREQUISITE_CONTRACT_DRIFT`, and `PREREQUISITE_CREDENTIAL_REVOCATION_SURFACE_UNAVAILABLE`.

## Phase 2 — create and bind the canary

1. Call `aevatar_create_team` with the exact caller-supplied `team_id`.
2. Call `aevatar_create_member` with `implementation_kind=workflow`, the exact `team_id`, and the exact caller-supplied `member_id`.
3. Call `aevatar_bind_member_workflow` with the exact `member_id`, exact `workflow_id`, and this exact YAML:

```yaml
name: scheduled_agent_key_canary
description: Harmless one-call scheduled Agent Key canary.
roles:
  - id: canary
    name: Canary
    system_prompt: |
      Return the exact marker supplied in the user prompt and nothing else.
steps:
  - id: prove_agent_key
    type: llm_call
    target_role: canary
    allowed_tools: []
```

4. Treat every create or bind receipt, including `202 Accepted`, as admission only. Read the exact Team/member/draft identities until the member reports the expected distinct `draftWorkflowId`, `publishedServiceId`, active `revisionId`, and completed binding facts. Preserve `bindingRunId` when returned.
5. Allow at most two minutes for binding visibility. Between reads, use only the fixed pacing snippet below. Stop before the response budget and continue from exact identities if needed.
6. If a Team, member, or bind response is ambiguous, reread only the exact caller-supplied ID. Never mint a replacement ID or repeat a mutation merely because its response was lost.
7. Emit `BINDING_READY` only after canonical binding readiness is visible.

## Phase 3 — arm the real cron

1. After `BINDING_READY`, run this exact target calculation:

```python
from datetime import datetime, timedelta, timezone

now = datetime.now(timezone.utc)
target = now.replace(second=0, microsecond=0) + timedelta(minutes=9)
cron = f"{target.minute} {target.hour} {target.day} {target.month} *"
print(target.isoformat(), cron)
```

2. Require the target to remain at least eight full minutes ahead. Treat the five-field expression as an annual cron; require its next occurrence to equal the selected target minute and the following occurrence to be at least 300 days later.
3. Immediately before schedule creation, call `aevatar_list_schedules` with the exact `team_id` and `member_id` and require an empty schedule list for this newly created member. Record `createAttemptUtc` from the trusted tool-call timestamp. Call `aevatar_schedule_member_workflow` exactly once with the member, annual cron, `UTC`, marker prompt, and unique schedule display name. Let the typed tool own credential provisioning and create idempotency.
4. On a normal result, record the returned `schedule_id` and verify that exact row. If the result is ambiguous or lost, never repeat the mutation and never invent its internal operation identities. Re-read only the exact member schedule list and recover only when exactly one post-baseline row has all of: the exact `published_service_id`, exact display name, exact marker prompt, exact annual cron, `schedule_timezone=UTC`, `enabled=true`, and `updated_at >= createAttemptUtc - 30s`. Record that row's `schedule_id`. If zero, multiple, or mismatched rows remain at the response budget, return `CLEANUP_INCOMPLETE`, `featureConclusion=not_evaluated`, and `cleanupStage=schedule_create_ambiguous`; preserve the member, draft, and Team and do not create a replacement.
5. Read `nyxid_api_keys` after creation and record `postCreateObservationUtc` from the trusted observation timestamp. Select exactly one post-create candidate satisfying every condition:

```text
id absent from baseline
created_at within [createAttemptUtc - 30s, postCreateObservationUtc + 30s]
name starts with studio-schedule-
is_active=true
allow_all_services=false
allow_all_nodes=false
allowed_service_ids equals [ownerLlmUserServiceId]
last_used_at is null
```

6. Label the key a unique correlated candidate, not a direct schedule-key reference. Fail closed on zero or multiple candidates.
7. Read `aevatar_get_schedule` for the exact owner and `schedule_id`. Require `authorization_status=active`, `credential_source_kind=scheduled_invocation_agent_key`, `enabled=true`, `next_fire_at=target`, `last_fire_at=null`, `revocation_pending=false`, and a positive authoritative `state_version`. Read the canonical owner detail and require `schedule.teamOwned=true`, the exact `schedule.teamOwnerScopeId`, `schedule.teamId`, and `schedule.teamOwnerMemberId`, `schedule.scheduleMode=0`, `schedule.oneShotFireAt=null`, `schedule.completed=false`, the exact owner LLM route/model/UserService, and empty pre-fire `recentFires`. Recheck the same Agent Key constraints and `last_used_at=null`.
8. If any recurring-readiness field differs, or the target minute is missed before activation becomes visible, begin cleanup. Never call `run-now`, reinterpret a one-shot schedule as recurring, or reinterpret the next annual occurrence as this canary.
9. Emit `CANARY_ARMED` with `targetFireAtUtc`, exact identities, and `lastUsedAtBeforeShape=null`. Tell the caller to continue no earlier than 15 seconds after the target minute begins.

## Phase 4 — prove the fire and begin revocation

1. If the caller resumes too early, end a completed response with `CANARY_ARMED` and the same earliest continuation time.
2. After the target, perform bounded owner-correct reads until all evidence is terminal or two minutes after the target minute. Between reads, use only:

```python
import time

time.sleep(30)
print("continue")
```

3. Require the flattened `last_fire_at` and authoritative `state_version` to advance from their pre-fire values. Re-read the same canonical owner detail; do not call a separate diagnostic endpoint.
4. Call the exact run route with `updatedFrom={targetFireAtUtc}`. Require exactly one run for `scheduleId`, preserve its `runId`, and require `completionStatus=1` (`Completed`), `lastSuccess=true`, empty `lastError`, and `lastOutput` containing the exact marker.
5. In the same canonical owner detail, require exactly one matching `recentFires` entry with `scheduledFireAt=target`, empty `error`, and `manual=false`.
6. Read the same exact `agentKeyId`. Require it to remain constrained and active, and require `last_used_at` to change from null to a timestamp at or after `targetFireAtUtc`.
7. Record the four evidence booleans independently. Do not let one observation substitute for another.
8. Begin cleanup whether evidence passed or failed. Send exactly one credential-aware request:

```json
{
  "reason": "scheduled_agent_key_canary_cleanup",
  "operationId": "<deleteOperationId>",
  "idempotencyKey": "<deleteIdempotencyKey>",
  "owner": {
    "kind": "studio_member_automation",
    "scopeId": "<scopeId>",
    "teamId": "<teamId>",
    "memberId": "<memberId>"
  }
}
```

Call `DELETE /api/schedules/{scheduleId}` with that body. Do not put a bearer, credential owner, binding identity, key ID, Vault reference, or secret material in the body. Treat `202 Accepted` and its `accepted/status/scheduleId/operationId/commandId` fields as admission only.
9. Emit `REVOCATION_STARTED` only after deletion is accepted and the first exact owner-correct post-delete detail or terminal 404 observation is recorded.

## Phase 5 — finish cleanup and report

Complete cleanup in this exact order:

1. Observe the exact canonical owner detail. While it exists, if `schedule.revocationPending=true` and either `schedule.nyxIdRevocationStatus` or `schedule.vaultRevocationStatus` is `Pending` or `Failed`, replay the byte-equivalent semantic DELETE body: unchanged path `scheduleId`, owner kind/scope/team/member, `deleteOperationId`, `deleteIdempotencyKey`, and reason. Only the transient authenticated request and Host-derived bearer may be fresh. Never mint replacement delete identities and never call a separate retry route. If both tracks are terminal but the row remains visible, observe projection; do not start another operation.
2. Require automation detail 404, absence from the exact owner automation list, and the exact `agentKeyId` inactive or absent.
3. Only after step 2, retire the exact `revisionId`.
4. Delete the exact `memberId` and require `aevatar_get_member` to report not found.
5. Delete the exact `draftWorkflowId` and require the owner-correct draft GET to return 404. Treat an empty DELETE result as provisional HTTP 204 only.
6. Archive the exact `teamId` and require the Team GET to report `lifecycleStage=archived`.

Allow at most three minutes for cleanup observation and still stop before the per-response budget. If revocation remains pending or any terminal observation is missing, preserve the remaining authority resources and return `CLEANUP_INCOMPLETE` with the exact cleanup stage and only the labelled recovery identities needed.

Report only the verdict, `featureConclusion`, target and observed UTC timestamps, the five evidence booleans, schedule/run status counts, redacted `last_used_at` null/timestamp shapes, stable error codes, and cleanup stage. Show final resource IDs only for `CLEANUP_INCOMPLETE`. Never print raw responses, full inventories, permission digests, tokens, key material, or Vault references.

## Evidence matrix

Require all four independent facts before declaring the executed feature successful:

| Evidence | Required fact |
| --- | --- |
| canonical authorization | Flattened `authorization_status=active` and `credential_source_kind=scheduled_invocation_agent_key`; canonical raw detail has the exact owner LLM route/model/UserService; the exact correlated Agent Key has false wildcard flags and the exact service grant. |
| real cron | Flattened `last_fire_at` and authoritative `state_version` advance; the same canonical raw detail has one `recentFires` entry with `scheduledFireAt=target`, empty `error`, and `manual=false`. |
| workflow execution | exactly one member run for `scheduleId`, `completionStatus=1` (`Completed`), `lastSuccess=true`, empty `lastError`, and `lastOutput` contains the marker |
| exact key use | the same unique post-create Agent Key candidate has `last_used_at=null` before fire and a timestamp at or after target after fire |

Set `cleanup=true` only after automation detail 404, owner-list absence, exact key inactive/absent, revision retirement, member 404, draft 404, and Team `lifecycleStage=archived`.

## Failure and recovery rules

| Condition | Required action |
| --- | --- |
| Caller declines | Stop without mutation and return `FAIL`, `featureConclusion=not_evaluated`, and `errorCode=CONFIRMATION_DECLINED`. |
| Clock or pacing probe unavailable before mutation | Return `FAIL`, `featureConclusion=not_evaluated`, and a harness prerequisite code. |
| Route, wire shape, or credential-aware DELETE contract missing | Stop before mutation with `FAIL`, `featureConclusion=not_evaluated`, and `errorCode=PREREQUISITE_CREDENTIAL_REVOCATION_SURFACE_UNAVAILABLE`; do not substitute nested CRUD or direct key deletion. |
| Team/member/bind response ambiguous | Read only the exact caller-supplied identity; never create a replacement. |
| Bind never becomes visible | Clean only resources actually created; do not schedule. |
| Schedule response ambiguous | Never repeat the schedule mutation and never invent create identities. Recover only from one exact post-baseline owner-list row matching the full create tuple; otherwise preserve owner resources and return `CLEANUP_INCOMPLETE` at `schedule_create_ambiguous`. |
| Target minute missed | Delete the exact automation; never use `run-now`. |
| Run fails or marker mismatches | Collect the exact key state, mark the executed feature failed, then clean up. |
| Exact key `last_used_at` is unchanged | Fail the feature even when the workflow reports success, then clean up. |
| Candidate count is zero or multiple | Fail closed; clean exact known resources and use `CLEANUP_INCOMPLETE` if exact key cleanup cannot be established. |
| Revocation remains pending or a track failed | Replay the unchanged canonical DELETE body through a fresh authenticated request. Preserve member/draft/Team and return `CLEANUP_INCOMPLETE` if terminal cleanup is not observed within the response budget. |
| Member, draft, Team, or terminal read fails during cleanup | Return `CLEANUP_INCOMPLETE`; never claim cleanup from an accepted receipt. |
| Continuation context is missing | Use only the labelled ledger and exact owner reads; never reconstruct identities or rediscover by display name. |

Never use imagined logs, generic command-observation APIs, automatic expiry, one-shot scheduler semantics, reference counts, or operator-only audit logs as substitutes for the public canonical facts.

## Common mistakes

| Rationalization | Required response |
| --- | --- |
| `202 means it worked` | Admission is not completion; read canonical state and independent key facts. |
| `run-now is faster` | It invalidates the cron proof and is forbidden. |
| `the marker proves the key` | Marker proves execution only; require the same key's `last_used_at` transition. |
| `similar names are enough` | Use exact caller-supplied IDs and full owner tuple; zero/multiple candidates fail closed. |
| `one long response is simpler` | It exceeds the 300-second/eight-round contract; complete a resumable checkpoint first. |
| `cleanup can happen later` | Verdict is `CLEANUP_INCOMPLETE` until terminal cleanup is observed. |
| `raw and flattened schedule fields are interchangeable` | They are separate contracts: use flat snake_case strings from `aevatar_get_schedule` and nested camelCase/numeric enums from canonical raw detail. |
| `retry-revocation should be a separate POST` | The public retry contract is exact replay of the same credential-aware canonical DELETE body with fresh authenticated transport authority. |

Do not add IDs, tool results, user text, environment reads, network calls, or dynamically generated code to any `code_execute` snippet. Use the two calculation snippets once at their specified phases and use only the fixed pacing snippet between bounded reads.
