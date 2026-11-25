---
name: semwright-driver-authoring
description: Use when a coding agent must design, implement, test, conform, or package a first-party Semwright application driver using the real Driver SDK and Broker authority model.
---

# Semwright driver authoring

Build a semantic provider, not an escape hatch.

## Sequence

1. Inspect the current `semwright-driver-sdk`, Driver Host, registry, and at least one maintained first-party driver before designing a surface.
2. Model application objects and workflows semantically. Define operations around stable application concepts, not screen coordinates.
3. Give every capability a bounded typed input/output schema, explicit risk/idempotency, required scopes, and an honest dry-run contract.
4. Keep the namespace under the assigned driver identity. Driver self-description never grants core or policy authority.
5. Implement through supported application APIs/protocols. Do not make arbitrary shell/JavaScript/Python execution the primary capability model.
6. Use refs for provider-owned objects and respect generation/staleness semantics when the SDK supports them.
7. Add fixtures, negative/security tests, property tests where useful, and conformance coverage.
8. Run `semwright driver validate` and sandboxed `semwright driver conformance` against a digest-pinned manifest.
9. Package/distribute only after conformance. Installation must not edit policy grants automatically.

Read [contract](references/contract.md), [security](references/security.md), and [testing](references/testing.md) as needed.
