---
name: vercel-runtime
description: "Investigate function errors, timeouts, and runtime differences. Use for failures after a successful build; vercel-build-fix handles build-time errors."
---

# vercel-runtime

Investigate function errors, timeouts, and runtime differences.

## Choose this workflow

Use for failures after a successful build; vercel-build-fix handles build-time errors.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vercel methods](../../references/packs/vercel.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; deployment, route/function, error window, and correlation IDs. Apply for requested remediation.

**Pack prerequisites:** Exact team/project/environment and deployment/revision when applicable; read access to relevant configuration/logs. Verify installed CLI/API support and framework behavior during implementation. Never print environment values or infer promotion authorization from a preview request.

- **Infer from evidence:** Read the linked project, team, framework, environment and deployment SHA from local config and supplied deployment evidence.
- **Reasonable default:** Diagnose locally with existing build scripts when deployment access is missing; do not infer a production target from a preview URL.
- **Ask only when needed:** Resolve a missing deployment/team/environment before the dependent remote operation; names and scope suffice without exposing environment values.

Declared evidence requirements: `vercel.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Runtime exceptions, timeouts, resource limits, and local/deployed behavior differences.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: edit the requested local implementation and perform relevant bounded checks while preserving unrelated work. Live data changes, remote actions and paid jobs require their resolved target and existing session authorization.

## Execute

1. The bundled Vercel collector covers build logs only, so its result is not runtime evidence. For runtime or function logs use the host Vercel connector or observability tools, or the installed CLI vercel logs after reading vercel logs --help: confirm whether that version supports a time window and which deployment it defaults to, since older releases only stream live logs briefly.
2. Correlate deployment, revision, request and time window, and inspect handler entry, environment presence, dependency waits and runtime-specific API support.
3. Separate cold-start, resource and network causes, and propose a focused reproduction or fix. Revalidate identity before a dependent action.

## Technical method

- **Inspect:** Inspect function logs and request IDs with region, runtime, payload size, duration and dependency timing.
- **Method:** Separate cold start, handler CPU, downstream wait and connection acquisition; compare runtime APIs to the deployed function type.
- **Avoid misdiagnosis:** A successful build proves no request health; an Edge/Node API mismatch needs a supported runtime choice, not suppressed errors.
- **Check the result:** Exercise the original failing route with a controlled request and observe success/error/timeout behavior on the same deployment.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vercel worked example](../../references/examples/vercel.md).
- Resolving check, deployment or migration identity: [Delivery evidence](../../references/scenarios/delivery-evidence.md).

## Decision branches

- **When timeout logs contain no downstream completion:** Treat the waiting boundary as evidence, not proof of which dependency caused the delay.

## Deliver and verify

- Request/deployment identity, a supported diagnosis with log references and causal hypotheses, the discriminating probe, and repair, verification and recovery limits.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Build success is not mistaken for runtime health; a timeout has evidence identifying the waiting boundary.

## Stop and recover

- Do not trigger billable/high-volume traffic or expose request data. Change code or configuration only in apply mode for requested remediation.

## Example requests

- **Normal (inspect):** Investigate function timeouts for this deployment and time window.
- **Edge (inspect):** Diagnose a function that builds but times out awaiting a database connection.
- **Blocked (inspect):** Analyze redacted runtime logs without generating live traffic.
