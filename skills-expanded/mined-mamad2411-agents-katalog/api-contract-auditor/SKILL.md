---
name: "api-contract-auditor"
description: "Audit backend, client, SDK, schema, fixture, and serialization contracts for drift and compatibility problems. Use when a user asks to review API or SDK compatibility, validate contract fixtures, inspect decoding mismatches, audit schema drift, or as part of $full-test-suite."
---

# API Contract Auditor

Review contract surfaces end to end and promote only verified mismatches or unsafe assumptions.

## Workflow

1. Inventory contract sources: routes, DTOs, schema files, generated clients, fixtures, decode models, and integration tests.
2. Trace request and response shapes across producer and consumer boundaries.
3. Confirm mismatches with schema proof, decode failures, integration tests, or strong static evidence.
4. Record confirmed findings in `project-audit-findings.md`.
5. Prefer shared fixtures and contract tests when proposing fixes.

## Focus Areas

- response or request shape drift
- incompatible naming, casing, or required fields
- stale fixtures or OpenAPI or GraphQL specs
- missing compatibility fields during migrations
- decode assumptions not enforced by upstream schemas
- backend-first fixture exports and SDK fixture copies that have drifted
- SDK decode failures, hash mismatches, or missing supported error shapes
- provider or adapter interfaces whose implementations normalize data
  inconsistently across platforms

## Rules

- Prefer one canonical finding per root contract mismatch.
- When possible, recommend the smallest producer or consumer change that restores a stable shared contract.
- Treat producer schemas, OpenAPI/GraphQL specs, and generated fixture manifests
  as stronger evidence than hand-maintained client assumptions.
- When SDKs consume checked-in fixtures, verify both manifest hashes and real
  model decoding before declaring compatibility.
- If a provider adapter contract is language-agnostic, audit semantics rather
  than exact method names: authentication behavior, pagination/cursors,
  normalization idempotency, supported cost/detail flags, and error categories.

## Fixture Drift Checks

When a repo uses backend-exported SDK fixtures:

1. Find the producer export/check command and generated fixture manifest.
2. Confirm every SDK copy was refreshed from the producer source of truth.
3. Validate fixture hashes or timestamps when the repo provides a manifest.
4. Decode fixtures through the actual SDK/client models, not just JSON parsing.
5. Check supported error responses are machine-readable and stable.

For same-release-train changes, require producer route/schema updates,
fixture regeneration, SDK fixture sync, and decoder updates to land together or
be explicitly staged with compatibility shims.

## References

- Finding format: `../_shared-project-ops/references/finding-format.md`
- Verification template: `../_shared-project-ops/references/verification-template.md`
- Dedupe rules: `../_shared-project-ops/references/dedupe-rules.md`
