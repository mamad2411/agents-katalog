---
name: domino-governance
description: Manage model risk governance in Domino using policies, bundles, evidence, findings and approvals through the Governance API (/api/governance/v1). Covers creating bundles, attaching evidence (registered model versions, project files and reports, dataset snapshot files, endpoints, NetApp Volume snapshot files, Flow artifacts), answering policy evidence questions, progressing through policy stages, approvals, findings, audit export and policy lifecycle. Use when the user mentions governance, compliance, bundles, policies, model risk management, SR 11-7, NIST AI RMF, approvals, findings, or audit trails.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token or service account token.
---

# Domino Governance Skill

Applies to Domino 6.3 and Domino Cloud.

## Configuration

Auth: [domino-api-intro](../domino-api-intro/SKILL.md#authentication). In a run use `DOMINO_API_PROXY` (no header) or a bearer from `http://localhost:8899/access-token`; outside a run a Personal Access Token or service account token as `Authorization: Bearer`. Legacy user API keys (`X-Domino-Api-Key`, `DOMINO_USER_API_KEY`) are deprecated; never use them.

Governance REST lives at `/api/governance/v1/*`. Pick the base where `GET $BASE/policy-overviews` returns **HTTP 200** (try the table rows in order):

| Context | Base | Authorization |
|---------|------|----------------|
| In-run, `DOMINO_API_PROXY` set (JWT credential propagation) | `$DOMINO_API_PROXY/api/governance/v1` | None (proxy adds starting-user JWT) |
| In-run, no proxy, governance on platform API gateway | `$DOMINO_USER_HOST` or `$DOMINO_API_HOST` + `/api/governance/v1` | Bearer from `GET http://localhost:8899/access-token` |
| In-run but proxy or sidecar returns **404** on `/api/governance/v1/*` (the in-run base does not route governance) | public deployment URL + `/api/governance/v1` | Bearer PAT or service account token |
| Outside any run | public deployment URL + `/api/governance/v1` | Bearer PAT or service account token |

Do **not** scrape the JWT `iss` claim to derive the cluster URL. Prefer `DOMINO_API_PROXY` in-run when step 1 succeeds; otherwise step 2 or 3.

Shell setup for the rows: [API-GOVERNANCE.md](./API-GOVERNANCE.md#base-url-discovery).

**Examples in the reference files:** send `Authorization: Bearer $TOKEN` only when `TOKEN` is set (rows 2 to 4); on the proxy path leave it unset. The curl blocks use a shell conditional for that.

## Key Concepts

Definitions of policy (template), bundle (living document), evidence (proof) and finding (issue): [STANDARD-WORKFLOW.md](./STANDARD-WORKFLOW.md#key-concepts).

## Reference files

When automating a specific flow, open the matching workflow file first instead of re-deriving from the 8-step section below.

- [STANDARD-WORKFLOW.md](./STANDARD-WORKFLOW.md) - Full request bodies for the 8-step workflow, and where bundles appear in the Domino UI
- [API-GOVERNANCE.md](./API-GOVERNANCE.md) - Endpoint table, bundle fields, base-URL shell setup, compute-policy polling
- [BUNDLE-LIFECYCLE.md](./BUNDLE-LIFECYCLE.md) - Stage sequences, creating bundles, progressing stages
- [EVIDENCE-WORKFLOW.md](./EVIDENCE-WORKFLOW.md) - Attachment types, evidence submission, findings
- [ONBOARD-MODEL.md](./ONBOARD-MODEL.md) - Onboard a model into governance
- [EVIDENCE-ROUND-TRIP.md](./EVIDENCE-ROUND-TRIP.md) - Evidence round-trip with findings
- [APPROVAL-GATE.md](./APPROVAL-GATE.md) - Approval gate automation
- [MONITORING-REREVIEW.md](./MONITORING-REREVIEW.md) - Monitoring-driven re-review
- [RECERTIFICATION-BULK.md](./RECERTIFICATION-BULK.md) - Periodic recertification (bulk)
- [AUDIT-EXPORT.md](./AUDIT-EXPORT.md) - Regulatory audit export
- [POLICY-LIFECYCLE.md](./POLICY-LIFECYCLE.md) - Policy lifecycle and rollout
- [MODEL-RETIREMENT.md](./MODEL-RETIREMENT.md) - Model retirement
- [WAIVER-EXCEPTION.md](./WAIVER-EXCEPTION.md) - Exception or waiver
- [READ-CONTEXT.md](./READ-CONTEXT.md) - Read governance context for downstream use

## Standard 8-Step Governance Workflow

All endpoints are under `$BASE` (`/api/governance/v1`); endpoint table and bundle field semantics: [API-GOVERNANCE.md](./API-GOVERNANCE.md#endpoints). Full request bodies for each step: [STANDARD-WORKFLOW.md](./STANDARD-WORKFLOW.md).

1. **Discover policies** — `GET $BASE/policy-overviews`; note the `id` of the policy you want to use.
2. **Get the project ID** — `DOMINO_PROJECT_ID` inside Domino, or look it up through the Projects API.
3. **Create a bundle** — `POST $BASE/bundles` with `projectId`, `name`, `policyId` (attachments may be inline). Save the returned `id` as `BUNDLE_ID`.
4. **Inspect the bundle** — `GET $BASE/bundles/$BUNDLE_ID` for stages, attachments and approval status.
5. **Attach evidence** — `POST $BASE/bundles/$BUNDLE_ID/attachments` with `type` one of `ModelVersion`, `Report`, `DatasetSnapshotFile`, `Endpoint`, `NetAppVolumeSnapshotFile`, `FlowArtifact`, `FlowArtifactFile` and a type-specific `identifier` object (shapes in [EVIDENCE-WORKFLOW.md](./EVIDENCE-WORKFLOW.md#attachment-types)). MLflow runs are not an attachment type: attach the registered model version or a report file instead.
6. **Answer evidence questions** — evidenceSet and artifact UUIDs come from `GET $BASE/policies/$POLICY_ID`; submit with `POST $BASE/rpc/submit-result-to-policy` using `policyId` (NOT `policyVersionId`) and `content` as `{artifactId: value}`. Only results with `isLatest: true` count as submitted evidence; drafts do not.
7. **Progress stages** — `POST $BASE/rpc/publish-approval-event`, then `PATCH $BASE/bundles/$BUNDLE_ID` with `{"stage": ...}` when the policy requires it. `PATCH .../stages/{stageId}` updates **assignee** only. Re-fetch and verify `stage` or `currentStageInfo.status` changed. Do not advance while findings on the stage are open.
8. **Document findings** — `POST $BASE/findings`; close with **PUT** `/findings/{id}` and `"status": "Done"` after the new evidence is submitted and recomputed ([API-GOVERNANCE.md](./API-GOVERNANCE.md#after-compute-policy-polling)).

## Documentation Reference

OpenAPI and route discovery: [API-SPECS.md](../domino-api-intro/API-SPECS.md) (public routes section). Published specs: `https://docs.domino.ai/api-specs/6.3/public-api.json` and `https://docs.domino.ai/api-specs/cloud/public-api.json`.

**Product docs:**
- Governance overview: https://docs.domino.ai/cloud/platform-capabilities/features/governance (6.3: replace `cloud` with `6.3`)
- Attachments: https://docs.domino.ai/cloud/platform-capabilities/features/governance/work-with-bundles/attachments
- Governance API: https://docs.domino.ai/cloud/reference/api/governance-api
