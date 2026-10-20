---
applyTo: "packages/contracts/**"
---

# Contract instructions

- HTTP API specs: OpenAPI 3.x in `packages/contracts/openapi/`.
- Event/WebSocket specs: AsyncAPI in `packages/contracts/asyncapi/`.
- Config/manifest schemas: JSON Schema in `packages/contracts/schemas/`.
- Breaking changes require an ADR (`VE-PLAT-ADR-NNNN`) and version bump.
- Generated code goes in consuming apps/packages, not in contracts.
- No hand-written HTTP clients when generated SDKs exist.

See `docs/reference/contract-system.md` and `docs/reference/contract-policy.md`.
