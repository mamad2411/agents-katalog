# API Contract Testing

## Purpose
Verify REST, GraphQL, and gRPC contracts with schema validation, Pact consumer-driven tests, oasdiff breaking-change detection, Prism mock servers, and can-i-deploy gates so providers and consumers evolve without silent breakage.

## Use when
- Adding or changing endpoints, fields, error codes, or pagination that consumers depend on.
- Setting up Pact consumer-driven contracts between a web frontend and a backend provider.
- Detecting breaking changes with oasdiff or buf breaking before a provider release.
- Building mock servers for frontend or partner development against an unverified spec.

## Do not use when
- Implementing endpoint business logic or handlers from scratch (use `backend-api`).
- Testing browser rendering, accessibility, or user flows (use `frontend-web`).
- Tuning database schemas or query plans without contract impact (use `database-review`).

## Required context
- Provider spec: OpenAPI 3.1 document, GraphQL SDL, or .proto files with version and changelog.
- Consumer inventory: named consumers (AcmeWeb, PartnerSync), their Pact versions, and supported contract ranges.
- Compatibility policy: additive-only within major versions, 90-day sunset for removals.
- CI topology: where verifier, mock, and can-i-deploy gate run in the pipeline.

## Procedure
1. **Validate the spec statically**: lint with Spectral (ruleset: operation ids, no trailing slashes, problem-details errors), verify examples against schemas with openapi-examples-validator, and confirm every response has an explicit schema and error catalog entry.
2. **Diff for breaking changes**: run oasdiff breaking against the last released spec (or buf breaking for Protobuf); classify findings as breaking (removed field, tightened type), dangerous (new required request field), or safe (new optional field, new endpoint) and block the pipeline on breaking.
3. **Author Pact consumer tests**: consumers declare expected interactions (given order ord_9f31 exists, upon get order, with path /v1/orders/ord_9f31, will respond 200 with matching body); publish pacts to the broker with consumer version tags such as web-2.14.0.
4. **Verify the provider and gate deployment**: run the provider verification suite against a real staging deployment, publish results to the broker, and run pact-broker can-i-deploy for the deployable pair; red verification blocks promotion.
5. **Serve and test mocks**: run Prism mock servers from the same spec for frontend and partner testing, assert mock responses validate against the spec, and fail any test that passes against the mock but is not covered by a Pact interaction.
6. **Record evidence and run scripts/verify.sh** from the repo root with diff reports, broker badges, and can-i-deploy output attached.

## Decision rules
- **Spec is executable truth**: unverified examples, undocumented errors, and mock-only behavior are defects, not conveniences.
- **Breaking changes never slip**: any oasdiff breaking finding blocks merge until reclassified with consumer sign-off or moved to a new major version.
- **Consumer-driven over provider-assumed**: provider tests derive from published Pact files, never from guessed consumer behavior.
- **Mock fidelity enforced**: Prism serves only spec-valid responses; drift between mock and provider verification fails the build.
- **can-i-deploy gates promotion**: no provider or consumer ships to production with a red broker matrix cell.

## Evidence required
- oasdiff or buf breaking report with zero untriaged breaking changes.
- Pact broker verification results and can-i-deploy green output for the release pair.
- Prism mock validation log plus contract test suite results.
- Passing execution log from scripts/verify.sh.

## Output contract
- Verified contract matrix: spec version, consumer versions, verification badges, deployment clearance.
- Pact interactions and provider states committed alongside the specs.
- Mock server configuration reproducible in CI and local development.

## Stop conditions
- All interactions verified, can-i-deploy green, mocks spec-valid, zero untriaged breaking changes.
- Breaking change found requiring consumer negotiation or major-version planning.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to Lead Architect if provider and consumer teams disagree on breaking versus safe classification.
- Escalate to the owning consumer team lead if a required Pact interaction is missing or the broker matrix stays red past one business day.
