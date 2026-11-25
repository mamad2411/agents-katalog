---
name: security-secrets
description: "Locate exposed credentials without printing secret values. Use to locate possible exposed credentials; security-config inspects deployment settings, and security-fix repairs a confirmed exposure in code; vite-env checks client-bundle exposure through Vite env handling."
---

# security-secrets

Locate exposed credentials without printing secret values.

## Choose this workflow

Use to locate possible exposed credentials; security-config inspects deployment settings, and security-fix repairs a confirmed exposure in code; vite-env checks client-bundle exposure through Vite env handling.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Security methods](../../references/packs/security.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; repository/history/log scope and approved scanner capability.

**Pack prerequisites:** Defined application boundary, authorized code/environment, relevant trust/access rules, and evidence sources. Default to defensive inspection; active tests use owned or explicitly authorized isolated targets. Minimize sensitive evidence and never print usable credentials.

- **Infer from evidence:** Resolve the requested surface, source/runtime version, reachable callers and actual trust/access boundaries.
- **Reasonable default:** Start with source analysis and bounded owned fixtures; treat scanner output as leads and preserve legitimate controls.
- **Ask only when needed:** Ask when target authorization or necessary trust semantics are unresolved before active probing; source inspection need not wait for production access.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Locate likely exposed secrets and identify containment needs; no implicit credential rotation or history rewrite.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Run approved scanners with redacted output over the requested sources, copying no values into reports.
2. Distinguish placeholders from plausible secrets, and map exposure surfaces.
3. Propose owner- and provider-specific remediation.

## Technical method

- **Inspect:** Inspect scoped source, tracked history when requested, build outputs and redacted scanner locations.
- **Method:** Distinguish placeholders/public identifiers from secret material; report type/location without value and separate remediation from rotation/history changes.
- **Avoid misdiagnosis:** Testing a suspected credential against its provider exposes it and exceeds source review; deletion does not revoke an exposed credential.
- **Check the result:** Use fake canaries and benign placeholders to validate redaction and detection; identify unknown rotation status without trying live keys.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Security worked example](../../references/examples/security.md).
- Dependencies, builds, secrets, hooks or privileged execution cross a trust boundary: [Dependency and execution provenance](../../references/security/supply-chain.md).
- An available scanner or dependency advisory check can answer the scoped question: [Scanner selection and evidence](../../references/security/scanners.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).
- The task specifically involves bug bounty, authorized pentest, security proof; load only the matching method: [Authorized vulnerability research](../../references/methods/authorized-security-research.md).

## Decision branches

- **When a plausible credential is found:** Record location/type and rotation owner/provider steps; do not test it against a live service by default.
- **When the user asks to contain a confirmed exposure:** Plan the order: revoke or rotate first, because a pushed secret is already exposed; then remove it from the tree and move it to a secret store through security-fix; only then, if requested, purge history, coordinate the force-push and ask the Git host to drop cached views, and verify with a re-scan and the provider key-usage log. Revocation, rotation, force-push and host purge are separate external or destructive actions that each need an exact target.

## Deliver and verify

- Redacted locations and types with confidence, exposure context and scope, uncertainty, and a containment and remediation sequence.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A committed credential is reported without its value; test placeholders do not inflate findings blindly.

## Stop and recover

- Never test suspected credentials against live providers without authorization. Do not copy secrets into reports, shell history, or external scanners.

## Example requests

- **Normal (inspect):** Scan the requested repository scope with redacted findings only.
- **Edge (inspect):** Scan history containing both test placeholders and a plausible credential.
- **Blocked (inspect):** Assess secret handling without an approved scanner; do not upload the repository.
