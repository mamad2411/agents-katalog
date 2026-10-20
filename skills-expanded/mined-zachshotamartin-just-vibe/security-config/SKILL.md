---
name: security-config
description: "Review application, container, and deployment configuration. Use for effective security-relevant settings; vercel-audit is a deployment-specific configuration comparison, and security-fix repairs a confirmed misconfiguration."
---

# security-config

Review application, container, and deployment configuration.

## Choose this workflow

Use for effective security-relevant settings; vercel-audit is a deployment-specific configuration comparison, and security-fix repairs a confirmed misconfiguration.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Security methods](../../references/packs/security.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; app/container/deployment configuration and exact environment.

**Pack prerequisites:** Defined application boundary, authorized code/environment, relevant trust/access rules, and evidence sources. Default to defensive inspection; active tests use owned or explicitly authorized isolated targets. Minimize sensitive evidence and never print usable credentials.

- **Infer from evidence:** Resolve the requested surface, source/runtime version, reachable callers and actual trust/access boundaries.
- **Reasonable default:** Start with source analysis and bounded owned fixtures; treat scanner output as leads and preserve legitimate controls.
- **Ask only when needed:** Ask when target authorization or necessary trust semantics are unresolved before active probing; source inspection need not wait for production access.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Debug settings, permissions, network exposure, cookies/headers, transport assumptions, and default credentials.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Compare declared and effective settings for the exact environment with the intended boundaries.
2. Trace high-impact settings and trust boundaries, distinguishing local development exceptions from public production exposure, and verify available deployment evidence.

## Technical method

- **Inspect:** Inspect effective production settings, network exposure, cookie/CORS/proxy rules, container privileges and CI trust paths.
- **Method:** Load only the matching framework and deployment branches; compare actual deployed behavior to configuration intent.
- **Avoid misdiagnosis:** Debug defaults, broad proxy trust or client-visible secrets can invalidate otherwise safe code; development settings are not production evidence.
- **Check the result:** Check a trusted and untrusted origin/host/identity where relevant and report inaccessible effective settings as unknown.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Security worked example](../../references/examples/security.md).
- Dependencies, builds, secrets, hooks or privileged execution cross a trust boundary: [Dependency and execution provenance](../../references/security/supply-chain.md).
- The task depends on framework defaults, middleware, RLS, server/client or deployment behavior: [Framework-specific review branches](../../references/security/frameworks.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).
- The request needs proactive context warnings, detected checks, native editor events, GitHub epic coordination or configuration audit reports: [Context health, check presets, editor events and shared work](../../references/runtime-depth.md).
- The task specifically involves bug bounty, authorized pentest, security proof; load only the matching method: [Authorized vulnerability research](../../references/methods/authorized-security-research.md).

## Decision branches

- **When effective deployment configuration is unavailable:** Report source-established risks conditionally instead of asserting the live setting.

## Deliver and verify

- Setting/environment/evidence/impact table with target-specific fixes and validation steps.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Public debug exposure is identified; intentionally local development settings are not mislabeled as production incidents.

## Stop and recover

- No infrastructure edits or broad hardening that breaks required behavior. Unknown effective settings remain unknown.

## Example requests

- **Normal (inspect):** Audit production configuration without changing infrastructure settings.
- **Edge (inspect):** Review debug exposure and cross-origin settings in separate dev and production configurations.
- **Blocked (inspect):** Audit configuration files without infrastructure access or changing live settings.
