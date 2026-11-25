---
name: vercel-release-check
description: "Verify a deployment and prepare promotion or rollback steps. Use to verify a named deployment's release gates; deploy executes authorized transition."
---

# vercel-release-check

Verify a deployment and prepare promotion or rollback steps.

## Choose this workflow

Use to verify a named deployment's release gates; deploy executes authorized transition.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vercel methods](../../references/packs/vercel.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; candidate deployment, intended production target, health criteria, and previous stable deployment.

**Pack prerequisites:** Exact team/project/environment and deployment/revision when applicable; read access to relevant configuration/logs. Verify installed CLI/API support and framework behavior during implementation. Never print environment values or infer promotion authorization from a preview request.

- **Infer from evidence:** Read the linked project, team, framework, environment and deployment SHA from local config and supplied deployment evidence.
- **Reasonable default:** Diagnose locally with existing build scripts when deployment access is missing; do not infer a production target from a preview URL.
- **Ask only when needed:** Resolve a missing deployment/team/environment before the dependent remote operation; names and scope suffice without exposing environment values.

Declared evidence requirements: `vercel.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Readiness and promotion/rollback preparation; actual promotion is a separate authorized action.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Resolve team/project, candidate deployment ID, immutable Git SHA and intended environment from observed metadata. Compare that identity with the tested commit, build output and required configuration names/scopes.
2. Check build completion, representative route/API health, asset content types, access protection and environment-specific behavior. Distinguish a protected preview from an unhealthy deployment; do not use a generic successful homepage as proof of the application journey.
3. Identify the previous known-good deployment and test the proposed recovery against schema/data and external effects. Reverting code may not restore data compatibility or undo published messages.
4. Produce a gate table tied to this candidate: criterion, evidence identity/time, pass/fail/unknown and blocking consequence. Re-read candidate identity before readiness is reported. Promotion, alias/DNS changes and rollback require their own authorized action/target.

## Technical method

- **Inspect:** Verify immutable candidate SHA, health evidence, environment requirements, compatible schema and previous deployment identity.
- **Method:** State promotion gates and a recovery sequence that accounts for data changes and in-flight work.
- **Avoid misdiagnosis:** Code rollback may fail once the schema or external effects have changed.
- **Check the result:** Check the actual promoted alias/deployment after authorized action and preserve pending gates when protected or live evidence is unavailable.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vercel worked example](../../references/examples/vercel.md).


## Decision branches

- **When rollback would restore code but not reverse a schema/data change:** Mark that recovery gap and require an explicit compatible recovery plan.

## Deliver and verify

- Candidate identity, evidence-linked release gates, concrete blockers or unknowns, recovery target/limits and readiness for the exact requested action.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- All readiness evidence applies to the named deployment and revision; unknown health or incompatible recovery is not converted to a pass. No deployment or promotion is implied by an audit.

## Stop and recover

- Do not promote or change aliases from a check request. Missing required health evidence means not yet verified.

## Example requests

- **Normal (inspect):** Check the candidate deployment before promotion; do not promote it.
- **Edge (inspect):** Check readiness for a deployment that removes a database column.
- **Blocked (inspect):** Assess readiness without current health evidence; do not promote aliases.
