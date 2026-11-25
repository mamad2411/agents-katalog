---
name: test-harness-verify
description: 'Verify that a test runner, fixture, isolated runtime or generated artifact really ran what it claims, at the consumer boundary. Use when a gate, wrapper or isolation claim may misrepresent the run. RU: проверка тестового окружения, изоляция тестов.'
disable-model-invocation: true
---

# Test harness verification

Use when a test runner, wrapper, fixture, isolated runtime or report gate might misrepresent what actually ran or how it was isolated, or when correctness depends on a generated artifact. Identify the requested test, selected inputs, runner and consumer, allowed effects, expected evidence and real completion status. Inspect actual selector and collection behavior; source test presence, a wrapper's zero exit or a printed summary alone may not establish that the intended test ran.

## Runners and evidence

For artifact-gated runners, distinguish child failure, valid evidence and a zero-exit child with missing or malformed evidence. Bind the producer's final artifact to the real consumer, preserve child and wrapper statuses separately, and do not let cleanup replace a primary failure. Test both valid controls and causally rejected negative cases where authorized. When primary work succeeded but mandatory cleanup failed, report a failed lifecycle; when both failed, retain both outcomes and the primary failure.

## Isolated integration and end-to-end runtime

Identify the real runner, supported infrastructure, scope, data stores, credentials, network and the exact authorized lifecycle first; a particular container system is not universally required. Use uniquely owned test resources and test-only configuration, fail closed when configuration is absent or ambiguous, never inherit production secrets or reuse shared databases, caches or project names. Limit network exposure to the intended test interfaces and prove the actual process, mounts and endpoints honor the boundary; fake tools must be used by every downstream helper. Bootstrap schemas and fixtures idempotently and verify the functional readiness the test needs (a generic health check can be narrower). Serialize tests that share mutable state unless isolation is established. Distinguish setup, runner, assertion, cleanup and environment failures. Clean up only exact resources the authorized test created, with bounded operations, preserving the original failure; never prune shared resources by broad names.

## Generated artifacts

When correctness depends on a generated script, query, document or schema rather than only its builder, identify the producer, input, artifact, consumer and supported execution environment. Exercise the production generation path with controlled inputs and validate the emitted artifact with the intended consumer where practical; do not duplicate the builder as the only oracle. Test syntax, shape, behavior and negative cases, and report what is static, mocked, executed or untested. Use test-only data and isolated outputs for side-effecting artifacts.

For mutable state or cleanup claims inspect [fixture isolation](references/fixture-isolation.md); for complex fake tooling or result pipelines [harness oracles](references/harness-oracles.md); for persisted state, rollback or ownership fences [persistence evidence](references/persistence-evidence.md). Run checks through the project's supported interface and report selected scope, counts, errors, unrun checks and limits. A synthetic fake or parser proves only the boundary it models; it is not independent review or real-runtime acceptance. For validation reporting see `quality-change-verify`.
