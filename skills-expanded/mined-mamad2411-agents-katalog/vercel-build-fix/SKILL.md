---
name: vercel-build-fix
description: "Reproduce and repair failed deployment builds. Use for a failed Vercel build; vite-bundle handles size and splitting of a successful build."
---

# vercel-build-fix

Reproduce and repair failed deployment builds.

## Choose this workflow

Use for a failed Vercel build; vite-bundle handles size and splitting of a successful build.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vercel methods](../../references/packs/vercel.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; failed deployment, branch/revision, and build logs.

**Pack prerequisites:** Exact team/project/environment and deployment/revision when applicable; read access to relevant configuration/logs. Verify installed CLI/API support and framework behavior during implementation. Never print environment values or infer promotion authorization from a preview request.

- **Infer from evidence:** Read the linked project, team, framework, environment and deployment SHA from local config and supplied deployment evidence.
- **Reasonable default:** Diagnose locally with existing build scripts when deployment access is missing; do not infer a production target from a preview URL.
- **Ask only when needed:** Resolve a missing deployment/team/environment before the dependent remote operation; names and scope suffice without exposing environment values.

Declared evidence requirements: `vercel.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Repository/build configuration causing the failure; project settings changes require explicit target scope.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Identify the failing deployment, SHA, environment and first causal build error. Compare repository/install root, build package, output path, runtime/package manager and resolved dependencies with the successful environment.
2. Reproduce the failing boundary locally when possible using the same workspace command and versions. Check case sensitivity, hoisted undeclared dependencies, build-time environment names and generated-file assumptions before patching application behavior.
3. Apply a focused fix and verify the corresponding build path. Keep local success separate from remote deployment verification; reuse the existing deployment/project identity and create a new deployment only when requested.
4. Report the causal evidence, changed configuration/code, local result and the deployment/revision actually observed remotely. Redact values and do not download secrets as incidental diagnosis.
5. Use the matching bundled evidence collector when available; read its result and limitations rather than treating exit zero as readiness. Revalidate identity before a dependent action.

## Technical method

- **Inspect:** Capture the first causal build error, deployed SHA, working directory, lockfile, Node version and variable names/scopes.
- **Method:** Reproduce the failed build conditions locally where possible; test whether the failure is dependency resolution, compilation or missing configuration.
- **Avoid misdiagnosis:** A later wrapper exit hides the initial cause; supplying a production secret locally can conceal a missing preview scope.
- **Check the result:** Run the matching build and inspect the new deployment's build result at the changed SHA, keeping local and remote evidence distinct.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vercel worked example](../../references/examples/vercel.md).
- Resolving check, deployment or migration identity: [Delivery evidence](../../references/scenarios/delivery-evidence.md).

## Decision branches

- **When local build succeeds but deployment fails:** Reproduce the specific environment difference before changing application code or adding dependencies.

## Deliver and verify

- Fix, root-cause explanation, local check results, and deployment verification if authorized.
- Causal build boundary, environment comparison, patch and reproduction outcome.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A missing runtime dependency is resolved correctly; environment differences are not masked by hard-coded secret values.

## Stop and recover

- Do not deploy or alter production settings merely to test. Inaccessible logs limit the diagnosis explicitly.

## Example requests

- **Normal (apply):** Repair the preview build failure using the supplied deployment logs.
- **Edge (apply):** Fix a deployment where an omitted runtime dependency exists only through workspace hoisting.
- **Blocked (inspect):** Diagnose from a build log without a valid Vercel token; do not deploy to test.
