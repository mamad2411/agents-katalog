---
name: api-contract-define
description: 'Implement, repair or independently review API operations and cross-layer contracts, tracing producer to consumer wire behavior end to end. Use for a new or repaired API operation, a consumer validator, or a feature spanning several layers. RU: контракт API, сквозная проверка.'
license: MIT
disable-model-invocation: true
---

# API and cross-layer contracts

Use for a new or repaired API operation, a consumer validator, a feature or repair that spans several production layers, or an independent review of producer-to-consumer wire behavior. Establish which of implementation and read-only review the request authorizes (review does not authorize edits, deployment or live probes), the requested scope and each acceptance criterion before choosing tests.

Trace the actual route, composition, request schema, validation, authorization/entitlement, client, serializer and response consumer. For cross-layer work map the real input → authority → implementation → serialization → persistence → output path, plus production composition, configuration, asynchronous effects and any other surface the task requires. Resolve the documented contract from the authoritative source and the implemented producer; do not infer it from an example, a generic standard name, a stale review or a convenient fake. A passing helper, mocked producer or static declaration proves only that seam. Build a positive/negative evidence matrix, define behavior for each outcome, identify preserved behavior and explicitly excluded fallbacks, and preserve existing security and compatibility rules. Keep project-specific route names, framework and toolchain choices in the project's own instructions.

Test through supported project interfaces with deterministic inputs and the minimum external dependencies. Distinguish a candidate, a delivered local change, activation and live acceptance; report verified, blocked and untested surfaces separately. Use the project's sanctioned schema generation only when the affected source requires it; a generated artifact is not the canonical source by default. Run proportionate focused gates and report actual results and limits. Never infer publication, deployment or remote authority from a local check.

References: [integration and offline verification](references/integration-and-tests.md), [producer and consumer validation](references/response-validation.md) for structured responses and pagination, [health evidence](references/health-api.md) for health-backed APIs, [boundary verification](references/boundary-verification.md), and [lifecycle and failure contracts](references/lifecycle-and-failure.md) for deactivation or fail-closed changes.
