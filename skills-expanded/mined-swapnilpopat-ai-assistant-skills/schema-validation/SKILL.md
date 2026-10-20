---
name: schema-validation
description: Validate API requests/responses against OpenAPI 3.1 / JSON Schema 2020-12 / Protobuf, gate CI on breaking changes, and fuzz with property-based generators. Use to catch contract drift before consumers do.
source: self
date_added: 2026-04-30
---

# Schema Validation

Make the schema the single source of truth and assert it everywhere — at the edge, in tests, and in CI gates.

## Stack Baseline (2026)

| Layer | Tool |
| --- | --- |
| Spec | OpenAPI 3.1 (JSON Schema 2020-12 aligned) |
| Linting | Spectral 6, Redocly CLI |
| Diff/breaking-change | `oasdiff` 1.x, Buf for Protobuf |
| Runtime validation | express-openapi-validator, FastAPI, Connexion, Spring `springdoc` |
| Property/fuzz | Schemathesis, Hypothesis-jsonschema, fast-check |
| Contract assertions | Pact 4.x, Dredd |

## When to Use

- Any HTTP/JSON, gRPC, or event-driven API.
- When clients rely on response shape for codegen.
- Before publishing a public API or partner API.

## Instructions

1. **Single source of truth** — store `openapi.yaml` (or `.proto`) in the service repo; generate types/clients/server stubs from it.
2. **Lint on every PR** — Spectral ruleset enforcing operationId, examples, error schemas, security definitions.
3. **Validate at runtime** — middleware rejects malformed requests with a structured 400 and asserts response shape in dev/staging.
4. **Fuzz with Schemathesis** — generates valid + boundary requests from spec; finds 5xx, schema mismatches, status-code violations.
   ```bash
   schemathesis run --checks all --hypothesis-max-examples=200 \
     --base-url=https://staging.example.com http://staging.example.com/openapi.json
   ```
5. **Diff for breaking changes** — `oasdiff breaking old.yaml new.yaml --fail-on ERR` in CI; a breaking change requires a MAJOR bump or explicit waiver.
6. **Property tests for hand-written code** — Hypothesis (Python) / fast-check (TS) round-trip serialization invariants.
7. **Snapshot examples** — every endpoint has a recorded example; CI fails when example no longer validates.

## JSON Schema 2020-12 Notes

- Use `$dynamicRef` sparingly; many tools still lag.
- Prefer `unevaluatedProperties: false` over `additionalProperties: false` when composing with `allOf`.
- Always model error responses with a `Problem` schema (RFC 9457 — Problem Details).

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Spec lives in Confluence, code drifts | Spec in repo; codegen in CI |
| `additionalProperties` left default | Explicitly set false on response objects |
| Examples never validated | `spectral lint` + JSON Schema check on examples |
| Breaking change shipped silently | `oasdiff` gate on PRs |
| Only happy-path validated | Fuzz with Schemathesis; assert error schemas |

## Output

- Spec in repo, linted, versioned semver.
- CI: lint → diff → fuzz (on changed paths) → publish artifact.
- Runtime: 400 with `Problem+JSON` on bad input; 500 logged + traced on bad output.

## References

- OpenAPI 3.1 spec — https://spec.openapis.org/oas/v3.1.0
- JSON Schema 2020-12 — https://json-schema.org/specification
- Spectral — https://stoplight.io/open-source/spectral
- oasdiff — https://github.com/Tufin/oasdiff
- Schemathesis — https://schemathesis.readthedocs.io/
- RFC 9457 Problem Details — https://www.rfc-editor.org/rfc/rfc9457
