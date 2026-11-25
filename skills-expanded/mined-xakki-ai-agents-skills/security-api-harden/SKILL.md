---
name: security-api-harden
description: 'Secure or review API ingress, transport, identity and response failure boundaries, plus resource, tenant and workspace authorization. Use when input, external calls or responses cross a trust boundary, or a caller selects stored resources. RU: безопасность API, авторизация ресурсов.'
license: MIT
disable-model-invocation: true
---

# API security boundaries and resource authorization

Use when API input, external calls, generic protocol methods or responses cross a trust boundary, or when a caller selects durable or live resources, a project/workspace, tenant, session, account or credential-bearing connection. Trace real authentication, resource scope, validation, planning, transport, parsing, output and state effects. Separate a read-only review from an authorized implementation; neither implies live provider calls or deployment.

## Boundaries

Validate at each relevant boundary before the associated side effect. Treat injected transport results and their inspection as untrusted where the contract requires it. Preserve stable, bounded and non-sensitive failure behavior; an error helper can leak a body before a later sanitizer runs. Select [ingress and raw APIs](references/ingress-and-raw.md), [transport and response validation](references/transport-and-response.md) or [generated and identity acceptance](references/generated-and-identity.md) for the active mode. Test actual consumer seams, observe forbidden downstream calls with valid positive controls, and report missing coverage and live-runtime evidence separately.

## Resource authorization and isolation

Authentication establishes caller identity; a supplied identifier or path is a selector, not proof of authority. Trace each operation from the request or transport to trusted server-owned context, durable ownership, query or mutation, worker and response, including list and detail, resume, search, counts, aggregates, exports, imports, live actions, cleanup and equivalent endpoints. Resolve and verify the caller's grant and resource scope **before** sensitive reads, credential access, effects or mutations. Scope queries and captures at their source: filtering a global inventory afterwards has already accessed foreign data. Fail closed when trusted context or ownership is unavailable.

Match identity comparison and canonicalization to the actual contract. Preserve durable ownership on an existing resource; never silently reassign missing ownership or trust a request-supplied workspace. Keep scope attached through internal projections, caching, multi-profile aggregation and fallback paths. Unknown or foreign resources use the documented non-disclosing denial without hiding required operational errors. Exercise the real authorization seam with an authorized positive control and foreign, missing and spoofed negative cases, and verify forbidden history reads, credentials and effects do not occur. Preserve the project's authorization and compatibility policy.

References: [scope and isolation checks](references/scope-isolation.md) for implementation and regression tests, [credential and capability checks](references/credential-capabilities.md) for selectors, idempotent replay and one-time download capabilities, [acceptance evidence](references/acceptance-evidence.md) for an independent read-only review, and [browser session boundaries](references/browser-session-boundaries.md) for browser-owned sessions and request-context bridges.
