# service-core

The Core service owns operational state: health/readiness diagnostics, approval
records, audit events, artifact references, scoped config, secret references,
ordered events, policy decisions, workspace mutation plans, schedules, and
evaluations.

## Agent Rules

1. Use `core_EvaluatePolicy` before risky work when the policy outcome is not
   obvious.
2. Use `core_RequestApproval` for risky actions and do not proceed until an
   approval decision is recorded.
3. Use `core_CreateWorkspaceMutationPlan` before renaming, deleting,
   restructuring, or writing sidecars in a user directory.
4. Never ask Core for raw secret values. `core_GetSecretRef` returns only a
   reference.
5. Persist artifacts with redaction metadata through `core_PutArtifact`.
6. Preserve event ordering through `core_PublishEvent` and `core_ListEvents`.
7. Treat `core_RecordApprovalDecision` denial as a hard stop.

## Service Functions

- `core_CheckHealth`
- `core_CheckReadiness`
- `core_RecordAuditEvent`
- `core_ListAuditEvents`
- `core_PutArtifact`
- `core_GetArtifact`
- `core_RequestApproval`
- `core_RecordApprovalDecision`
- `core_GetConfig`
- `core_SetConfig`
- `core_GetSecretRef`
- `core_PublishEvent`
- `core_ListEvents`
- `core_EvaluatePolicy`
- `core_CreateWorkspaceMutationPlan`
- `core_ApproveWorkspaceMutationPlan`
- `core_ScheduleRun`
- `core_ListSchedules`
- `core_RecordEvaluation`
- `core_GetEvaluation`
