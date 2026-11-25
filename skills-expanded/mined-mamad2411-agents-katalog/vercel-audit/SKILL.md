---
name: vercel-audit
description: "Inspect project configuration, build settings, and deployment assumptions. Use to compare repository configuration with a specific Vercel project; vercel-runtime investigates a particular runtime failure."
---

# vercel-audit

Inspect project configuration, build settings, and deployment assumptions.

## Choose this workflow

Use to compare repository configuration with a specific Vercel project; vercel-runtime investigates a particular runtime failure.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vercel methods](../../references/packs/vercel.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; project and repository plus reported deployment concerns.

**Pack prerequisites:** Exact team/project/environment and deployment/revision when applicable; read access to relevant configuration/logs. Verify installed CLI/API support and framework behavior during implementation. Never print environment values or infer promotion authorization from a preview request.

- **Infer from evidence:** Read the linked project, team, framework, environment and deployment SHA from local config and supplied deployment evidence.
- **Reasonable default:** Diagnose locally with existing build scripts when deployment access is missing; do not infer a production target from a preview URL.
- **Ask only when needed:** Resolve a missing deployment/team/environment before the dependent remote operation; names and scope suffice without exposing environment values.

Declared evidence requirements: `vercel.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Framework detection, root/build/output settings, runtime assumptions, and deployment configuration.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Record team, project and revision, and inspect recent deployment metadata.
2. Compare root directory, build/install command, output directory, framework preset and runtime against the relevant package's scripts and configuration, and identify drift or unsupported assumptions.

## Technical method

- **Inspect:** Read team/project identity, root directory, framework preset, package manager, build/output settings and deployment SHA.
- **Method:** Compare each setting to the workspace actually owning the app; distinguish monorepo install root from build root.
- **Avoid misdiagnosis:** Relinking to inspect settings mutates project state; local hoisting can conceal undeclared dependencies.
- **Check the result:** Produce an evidence-backed mismatch list and mark unavailable remote settings unknown instead of assuming local config is authoritative.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vercel worked example](../../references/examples/vercel.md).
- The task depends on framework defaults, middleware, RLS, server/client or deployment behavior: [Framework-specific review branches](../../references/security/frameworks.md).

## Decision branches

- **When a monorepo's deployed root differs from the package under review:** Trace install/build working directories and workspace dependency resolution before changing settings.

## Deliver and verify

- Setting/source/effective-value comparison with drift findings, unavailable observations and ordered fixes.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A wrong monorepo root is identified; missing settings access is reported rather than assumed to match local defaults.

## Stop and recover

- No settings edits or new deployment. Do not treat a successful old deployment as evidence the current revision is healthy.

## Example requests

- **Normal (inspect):** Audit the linked project's build settings against this monorepo configuration.
- **Edge (inspect):** Audit a monorepo deploying the wrong workspace package.
- **Blocked (inspect):** Audit supplied settings and logs without live Vercel access.
