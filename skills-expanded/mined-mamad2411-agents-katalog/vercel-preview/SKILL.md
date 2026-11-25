---
name: vercel-preview
description: "Prepare and validate a branch or PR preview deployment. Use for a specifically requested preview deployment; vercel-release-check assesses production readiness."
---

# vercel-preview

Prepare and validate a branch or PR preview deployment.

## Choose this workflow

Use for a specifically requested preview deployment; vercel-release-check assesses production readiness.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vercel methods](../../references/packs/vercel.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Inspect an existing preview or plan a proposed one; apply for requested preview configuration or creation.

**Pack prerequisites:** Exact team/project/environment and deployment/revision when applicable; read access to relevant configuration/logs. Verify installed CLI/API support and framework behavior during implementation. Never print environment values or infer promotion authorization from a preview request.

- **Infer from evidence:** Read the linked project, team, framework, environment and deployment SHA from local config and supplied deployment evidence.
- **Reasonable default:** Diagnose locally with existing build scripts when deployment access is missing; do not infer a production target from a preview URL.
- **Ask only when needed:** Resolve a missing deployment/team/environment before the dependent remote operation; names and scope suffice without exposing environment values.

Declared evidence requirements: `vercel.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Preview environment only, including authorized smoke checks.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: make the requested changes or execute the requested operation within its resolved target and limits. Local preparation does not authorize live, remote, destructive or paid actions; existing explicit session authorization still applies.

## Execute

1. Resolve the intended project and commit, and inspect prerequisites.
2. Reuse a matching deployment where suitable; create one only when requested.
3. Verify identity, URL, access protection, routes and representative behavior.

## Technical method

- **Inspect:** Resolve branch/head SHA, existing matching deployments and access-protection expectations.
- **Method:** Reuse an appropriate existing preview or create the requested one; check nested routes, APIs and assets at its immutable deployment identity.
- **Avoid misdiagnosis:** Anonymous 401/403 from protection is not necessarily app failure; a branch alias may advance while checks run.
- **Check the result:** Record deployment ID, SHA, URL and actual route observations, including unavailable protected checks.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vercel worked example](../../references/examples/vercel.md).


## Decision branches

- **When a deployment request times out:** Query for the intended revision before retrying; distinguish a protected URL from an unhealthy app.
- **When the request is for local preparation or implementation:** Prepare requested preview configuration locally; submitting a preview requires the intended project/account and source revision, with no implicit production promotion.

## Deliver and verify

- Preview plan or actual URL and deployment ID with the exact revision, access requirements and observed smoke-check results.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- The preview serves the intended commit; a protected preview is reported as access-restricted rather than broken without evidence.

## Stop and recover

- No promotion, production-domain changes, or unsolicited sharing. Check for existing deployment after uncertain creation.

## Example requests

- **Normal (plan):** Prepare a preview for this branch and project; identify prerequisites first.
- **Edge (apply):** Create a preview after an earlier request returned no deployment ID.
- **Blocked (inspect):** Plan a preview without provider access; do not invent a URL.
