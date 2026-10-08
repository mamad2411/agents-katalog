---
name: test-quality-review
description: Evaluate whether tests cover changed behavior, edge cases, regressions, external integrations, and deterministic validation paths. Use for all non-trivial code changes and especially bug fixes, validators, parsers, adapters, and workflows.
license: Apache-2.0
compatibility: "Go testing package, local fake adapters, HTTP test servers, deterministic fixtures"
allowed-tools: filesystem scm-api diff-analyzer corpus-selector validator
metadata:
  version: "2.0.0"
  owner: "7review"
  review-domain: "test-quality"
  risk-tier: "high"
---

# Test Quality Review Skill

## Activation Contract

Use this skill for any non-trivial code change and always for bug fixes, parsers, validators, provider adapters, SCM integrations, HIL state changes, publishing, memory/headroom bridges, streaming, config loading, Docker wiring, and security checks.

Do not demand tests for pure formatting or text-only copy changes unless they affect runtime behavior, generated artifacts, or documented contracts.

## Review Algorithm

1. Identify the user-visible or contract behavior changed by the diff.
2. Check whether tests fail before the fix and pass after it.
3. Look for missing negative, edge, and integration-adapter cases.
4. Reject brittle tests that assert implementation details without behavior value.
5. Suggest the smallest useful test that would catch the risk.
6. Check whether the test isolates external systems with fakes, fixtures, local HTTP servers, or container health checks.
7. Check whether regression tests encode the actual bug or production risk, not only the happy path.
8. Verify deterministic behavior: no real network, no wall-clock race, no provider dependency, no order-sensitive flake.

## Technical Patterns

### Agent Pipeline Tests

- Pipeline tests should prove lifecycle order: event normalization, SCM enrichment, diff normalization, corpus/skill selection, model review, validation, report render, publish/HIL, memory proposal.
- Fake SCM, fake LLM, fake publisher, fake memory, and fake headroom adapters should expose what was called and with which normalized state.
- Disabled or unavailable adapters should fail clearly when required by production config.

### SCM Adapter Tests

- Webhook tests must cover valid signatures/secrets, missing secrets, invalid signatures, unsupported events, malformed payloads, and minimal payloads that require enrichment.
- Pagination tests must use HTTP test servers or fake clients with multiple pages.
- Publishing tests must cover prior bot marker detection, update vs supersede behavior, and concurrent retry safety.

### Validation and Policy Tests

- Validators need positive and negative cases. A validator with only accept-path tests is incomplete.
- HIL tests should cover illegal transitions, approval-required final publish, rejected findings excluded from memory, and explicit auto-final policy.
- Redaction tests should include representative token/header/key patterns.

### Streaming and Operator UI Tests

- Streaming tests should exercise chunk boundaries, cancellation, provider errors after partial output, and final completion state.
- TUI/CLI/config wizard tests should focus on config parsing, validation,
  generated file shape, and command behavior instead of terminal screenshots
  where practical.

### Docker and Bridge Tests

- Docker config tests should validate required services, health checks, networks, volumes, and environment variables.
- Python bridge code should have explicit health and request-shape checks when it is part of production deployment.

## Review Areas

- Validation rejection paths
- Provider adapter normalization and pagination
- Webhook signature or secret failures
- Idempotent publishing and duplicate detection
- Parser malformed input
- Boundary values and empty/nil cases
- Concurrency or retry behavior with fake dependencies

## Coverage Contract

The goal is production confidence, not vanity coverage. A change is well-tested when the tests would fail for the realistic bug the change is meant to prevent.

- For deterministic code, prefer table-driven branch tests that name the business case.
- For adapters, use local HTTP servers or fake interfaces; never require live
  external SCM, memory, compression, sidecar, or model calls.
- For parsers, include malformed input, unsupported shape, minimal valid payload, and representative real-world variants.
- For side effects, assert idempotency, stored state, and retry behavior.
- For goroutines, queues, streaming, or cancellation, assert shutdown and error propagation, not just happy-path output.

## Conditional Integration Test Map

Use these rows only when the changed repository has the matching integration
surface. Do not infer that the target repository is an agent just because this
skill mentions one:

| Area | Required Tests |
| --- | --- |
| Webhooks or external events | signature/token rejection, event filtering, delivery IDs, payload variants |
| External API clients | pagination, malformed provider responses, auth errors, normalization |
| Automated workflow pipeline | lifecycle order, validation before side effects, required dependency paths |
| Approval gate | approval before final side effects, rejected items excluded from durable output |
| Operator UI/API | auth headers, command parsing, streaming chunks, operator error messages |
| Runtime packaging | required services/env, network/volume health expectations |
| Skill/procedure packages | metadata validation, activation content, selection, enriched body instructions |

## Test Smells

- A test only proves a mock was called but not the normalized behavior.
- A parser test uses only one ideal payload shape.
- A concurrency test sleeps instead of using channels, contexts, or deterministic synchronization.
- A Docker/config test validates file existence but not required services or env contracts.
- A prompt/model test asserts exact prose instead of structured findings or report sections.

## Execution Rules

Test findings must connect a changed behavior to a missing or weak executable
check. File when a production branch, parser, validator, adapter, state
transition, or side effect changed without a test that would fail on regression.
Suppress when coverage is provided by a more focused integration test or when
the change is mechanical and already guarded by compile/lint behavior.

Choose the test shape:

- unit test for deterministic parsing, validation, selection, and rendering
- local HTTP server test for SCM, LLM, memory, compression, or sidecar adapters
- integration-style pipeline test for lifecycle state and publishing
- Docker/compose check for runtime wiring
- golden/structured assertion only when output format is the contract

## Tool Routing

| Step | Tool Surface | Required Use |
| --- | --- | --- |
| Changed behavior map | `diff-analyzer`, `scm-api` | Identify newly changed branches, parsers, adapters, validators, state transitions, error paths, and integration boundaries. |
| Existing test lookup | `filesystem`, `corpus-selector` | Locate adjacent tests, fixtures, fake providers, HTTP test servers, golden reports, and documented test commands. |
| Coverage validation | `validator` | Report missing tests only when a behavior, regression, branch, or production risk is untested. |

## Escalation Signals

- A parser, validator, external adapter, publisher, memory/compression bridge, or state machine changes without rejection and edge-case tests.
- A bug fix lacks a regression test that would fail before the change.
- Tests use real external APIs or credentials where local fakes should be used.

## Evidence Standard

Test-quality findings should name the behavior at risk, the missing case, and the test seam that can cover it without real external dependencies. Prefer concrete test names such as `TestPublisher_UpdatesExistingDraftMarker` over broad demands like "add more tests".

## Runtime Integration Checks

- For every production behavior, identify the cheapest deterministic test layer: parser, adapter with HTTP server, pipeline fake, run-store filesystem, CLI command, or runtime packaging config.
- Required external dependency paths must have positive, failure, and readiness
  tests without depending on live external services.
- Streaming and operator commands need tests for auth, partial output, terminal events, error events, and bounded timeouts.
- Skills themselves require validation tests for frontmatter, activation content, selection, and sufficient execution guidance.

## Review Output Contract

Missing-test findings must name a specific behavior and a specific test to add. Include why existing tests would not fail for the regression and what fake, fixture, or local server should be used.

## False Positive Checks

- Do not require 100% line coverage when branch/behavior coverage is stronger and more maintainable.
- Do not require expensive end-to-end tests for behavior that a focused unit or adapter test can cover.
- Do not object to table-driven tests because they are compact; object only when cases hide important behavior.
- Do not demand tests for generated code unless the generator or generated contract changed.

## Finding Template

```md
### [severity] Missing or weak test coverage

- Behavior at risk: `<contract or user-visible behavior>`
- Missing case: `<negative/edge/integration/regression path>`
- Existing tests: `<what is present or absent>`
- Evidence: `<changed lines and test files>`
- Suggested test: `<specific test name, fake/fixture, and assertion>`
- Production risk: `<what could regress unnoticed>`
```
