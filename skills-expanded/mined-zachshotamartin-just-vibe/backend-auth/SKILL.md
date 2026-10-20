---
name: backend-auth
description: "Build or audit authentication and session behavior. Use for identity/session lifecycle; backend-permissions handles what an identity may do."
---

# backend-auth

Build or audit authentication and session behavior.

## Choose this workflow

Use for identity/session lifecycle; backend-permissions handles what an identity may do.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Backend methods](../../references/packs/backend.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect for audits; apply for a specified implementation. Requires identity provider, session model, and recovery/logout requirements.

**Pack prerequisites:** Service source, data/interface contracts, framework/runtime versions, and test environment. Default apply operations target local code and isolated tests; live infrastructure/data mutations require their own requested scope.

- **Infer from evidence:** Trace service callers, request contracts, authorization, transactions, retries and existing test infrastructure.
- **Reasonable default:** Use the existing persistence and framework; isolate local tests from live services.
- **Ask only when needed:** Resolve ambiguous durability, duplication or consistency requirements before encoding them; absent production access does not prevent local implementation.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Authentication and session lifecycle; resource authorization is separately checked by `backend-permissions`.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: edit the requested local implementation and perform relevant bounded checks while preserving unrelated work. Live data changes, remote actions and paid jobs require their resolved target and existing session authorization.

## Execute

1. Identify the provider, session owner, trust boundaries and the actual request: audit or implementation. Trace login, refresh, logout and recovery across browser and server.
2. Read only the matching cookie-session, OAuth callback, refresh-race or recovery scenario. Use the supported provider mechanism, implement the requested boundary and verify the relevant transitions.

## Technical method

- **Inspect:** Resolve provider/version, session storage, cookie topology and token refresh/revocation semantics.
- **Method:** Load the matching authentication scenario and identity security guide; trace browser binding, token verification, rotation, recovery and account linking.
- **Avoid misdiagnosis:** Decoding a JWT is not signature/issuer/audience validation; accepting an access token as identity can cross protocol boundaries.
- **Check the result:** Test invalid/expired credentials, wrong flow state, session fixation, concurrent refresh and logout followed by a late refresh result.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Backend worked example](../../references/examples/backend.md).
- Working on cookie sessions, callbacks, refresh or recovery: [Authentication scenarios](../../references/scenarios/auth.md).
- Identity, ownership, tenant isolation, replay or privilege changes affect the task: [Identity and authorization](../../references/security/identity.md).
- The task depends on framework defaults, middleware, RLS, server/client or deployment behavior: [Framework-specific review branches](../../references/security/frameworks.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).
- The task specifically involves kubernetes, readiness probe, rolling update; load only the matching method: [Kubernetes release and failure recovery](../../references/methods/kubernetes-release.md).
- The task specifically involves flox, uncloud, dev environment, reproducible environment; load only the matching method: [Flox, containers and reproducible development](../../references/methods/reproducible-environments.md).
- The task specifically involves tail latency, latency critical, p99, benchmark optimization; load only the matching method: [Latency budgets and performance experiments](../../references/methods/latency-systems.md).

## Decision branches

- **When browser cookie sessions carry authentication:** Resolve cookie scope, proxy/HTTPS behavior, CSRF protection, session rotation and logout semantics.
- **When OAuth/OIDC callbacks establish a session:** Bind the flow to the initiating browser, enforce the supported state/PKCE/nonce contract, and validate identity through the provider client.
- **When refresh and logout can overlap across tabs or workers:** Choose the session owner and stale-result rule; test rotation/reuse, expired credentials and late refresh after logout.
- **When recovery or account linking changes access:** Verify single-use/expiry, ownership proof, abuse controls and the intended existing-session invalidation.

## Deliver and verify

- Authentication findings or implementation with the auth lifecycle, trust assumptions and expired/revoked/invalid-credential checks.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Logout/revocation invalidates the intended session; untrusted or expired tokens fail closed.

## Stop and recover

- Do not invent cryptography, log credentials, or mistake authentication for permission to access every resource.

## Example requests

- **Normal (inspect):** Audit session refresh, logout, and expired-token behavior.
- **Edge (apply):** Repair refresh behavior across concurrent browser tabs and expired sessions.
- **Blocked (inspect):** Review auth configuration without credentials or live login attempts.
