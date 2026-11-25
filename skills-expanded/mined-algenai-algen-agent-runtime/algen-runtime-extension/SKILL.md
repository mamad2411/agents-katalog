---
name: algen-runtime-extension
description: Add or review an Algen Agent Runtime extension such as a model provider, tool adapter, retrieval backend, persistence store, telemetry integration, or external-framework adapter.
---

# Extend Algen Agent Runtime

First identify the extension point and inspect its Protocol, registry, existing adapter, contract
tests, optional extra, and documentation. Read only the matching section of
`references/extension-points.md`.

Implement against Runtime contracts rather than leaking a vendor SDK into orchestration or public
state. Normalize vendor inputs, outputs, usage, errors, streaming behavior, and cancellation at the
adapter boundary. Keep the dependency optional and fail with an actionable installation message
when its extra is absent.

Treat all extension inputs as untrusted. Carry tenant and identity context, enforce permissions,
validate outbound destinations, classify side effects and idempotency, bound time and result size,
and prevent secrets from entering logs or persisted events.

Add deterministic contract tests without credentials. Put live integration tests behind the `live`
marker. Update the optional dependency extra, compatibility documentation, an importable example
when useful, and `CHANGELOG.md` for user-visible support.

