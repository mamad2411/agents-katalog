---
name: vercel-routing
description: "Diagnose redirects, rewrites, headers, domains, and route behavior. Use for platform/framework route interaction; vite-assets diagnoses emitted asset paths."
---

# vercel-routing

Diagnose redirects, rewrites, headers, domains, and route behavior.

## Choose this workflow

Use for platform/framework route interaction; vite-assets diagnoses emitted asset paths.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vercel methods](../../references/packs/vercel.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; URL/path, expected response, project, and deployment configuration. Apply for a requested routing configuration fix.

**Pack prerequisites:** Exact team/project/environment and deployment/revision when applicable; read access to relevant configuration/logs. Verify installed CLI/API support and framework behavior during implementation. Never print environment values or infer promotion authorization from a preview request.

- **Infer from evidence:** Read the linked project, team, framework, environment and deployment SHA from local config and supplied deployment evidence.
- **Reasonable default:** Diagnose locally with existing build scripts when deployment access is missing; do not infer a production target from a preview URL.
- **Ask only when needed:** Resolve a missing deployment/team/environment before the dependent remote operation; names and scope suffice without exposing environment values.

Declared evidence requirements: `vercel.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Redirects, rewrites, headers, domains, and framework routing interactions.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: edit the requested local implementation and perform relevant bounded checks while preserving unrelated work. Live data changes, remote actions and paid jobs require their resolved target and existing session authorization.

## Execute

1. Build a request table with host, path, method and expected handler, and inspect base paths.
2. Trace redirects, rewrites, filesystem and framework routing in effective precedence order with bounded read-only requests, comparing preview and production assumptions.
3. Identify loops, unmatched paths and the responsible rule.

## Technical method

- **Inspect:** Inspect framework routes, platform rewrites/redirects, domain target, base path and effective response headers.
- **Method:** Follow one URL through each routing layer; check precedence and loops with redirect following bounded.
- **Avoid misdiagnosis:** An SPA fallback returning HTML for JavaScript or API URLs can look like HTTP success while breaking clients.
- **Check the result:** Test direct nested navigation, asset MIME types, API errors, query preservation and the intended redirect status/method behavior.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vercel worked example](../../references/examples/vercel.md).


## Decision branches

- **When a catch-all rewrite returns HTML for API or asset paths:** Narrow the rule and verify reserved paths plus direct nested navigation.

## Deliver and verify

- Route matrix with observed status, location and content type, the responsible rule and cause, and a proposed configuration patch; apply mode makes a requested fix.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Redirect loops are identified; API routes are not swallowed by a catch-all SPA rewrite.

## Stop and recover

- No DNS or custom-domain mutation implicitly. Distinguish framework behavior from platform configuration and unavailable network evidence.

## Example requests

- **Normal (inspect):** Explain why nested API routes receive the SPA page instead of JSON.
- **Edge (apply):** Fix preview deep links without swallowing API requests.
- **Blocked (inspect):** Inspect routing configuration without DNS access or live request evidence.
