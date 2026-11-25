---
name: fabrico-preparing-applications-for-ai
description: "Prepares application architecture, data flows, operations, and quality gates for safe AI capabilities without coupling the product to one model provider. Use whenever building a new application, materially extending an existing application, adding LLM or agent features, or reviewing whether a system is AI-ready."
---

# Preparing Applications for AI

Make every application capable of adopting AI features safely without forcing speculative model integrations into the current scope. Build readiness into required application boundaries, data governance, asynchronous execution, and observability.

<readiness-boundary>

AI-ready does not mean adding a chatbot, vector database, model SDK, or paid provider to every product. Do not create unused abstractions. Preserve a clean adoption path in code already required by the application, and implement provider-specific machinery only when an AI use case is in scope.

</readiness-boundary>

## AI-Readiness Process

Track this checklist:

```text
Progress:
- [ ] Identify eligible use cases and risk level
- [ ] Define evaluation quality and cost-per-success budgets
- [ ] Expose reusable domain operations and context boundaries
- [ ] Add provider-neutral AI contracts when an AI feature is in scope
- [ ] Design safe synchronous, streaming, and queued execution
- [ ] Protect data and constrain model/tool authority
- [ ] Add observability, evaluation, and cost controls
- [ ] Verify deterministic fallbacks and failure behavior
```

### 1. Identify use cases and risks

- Add an AI-readiness section to the existing research or plan rather than creating a standalone document.
- For each plausible or requested capability, capture the user, business outcome, source data, required permission, latency target, acceptable failure mode, and whether human approval is required.
- Define a deterministic baseline for the workflow. Add AI only when a representative evaluation shows that it improves the required outcome enough to justify provider and operational cost.
- Classify the operation as assistive, generative, decision-support, or autonomous. Never grant autonomous write authority by default.
- Mark sensitive, regulated, tenant-owned, copyrighted, or retention-limited data before selecting a provider or persistence approach.

### 2. Preserve reusable application boundaries

- Keep domain operations out of UI components, controllers, prompts, and provider adapters. Expose them through typed application services with stable identifiers and explicit authorization context.
- Make relevant inputs and outputs serializable and schema-validatable so the same operation can be called by UI, API, queue job, or a future tool adapter.
- Propagate user, tenant, locale, timezone, correlation ID, and permission context across HTTP requests, events, and queue jobs.
- Emit structured domain and audit events for important operations. Do not rely on model transcripts as the system of record.

### 3. Add AI contracts only for in-scope AI features

- Put model calls behind a small provider-neutral gateway. Keep provider, model, temperature, timeout, and token limits in validated configuration rather than business code.
- Version prompts and tool schemas with the code that consumes them. Use `fabrico-engineering-prompts` for runtime prompt design.
- Prefer schema-constrained outputs and validate them before they reach domain logic. Reject or repair invalid output within bounded retry limits.
- Keep tools narrow and allowlisted. Give each tool typed arguments, server-side authorization, idempotency expectations, and an explicit read/write risk classification.
- Make provider replacement and a deterministic no-AI fallback possible without rewriting the domain layer.
- Do not add embeddings, retrieval infrastructure, or a vector database until a versioned retrieval evaluation shows that relational data, indexed search, and bounded context cannot meet the requirement.

### 4. Design execution paths

- Use synchronous calls only when bounded latency fits the request. Use Redis-backed queues for long-running, retryable, fan-out, or batch work.
- Support cancellation and disconnection for streaming responses. Persist only the minimum state required to resume or explain an operation.
- Add timeouts, bounded retries with backoff, idempotency keys, concurrency limits, rate limits, and circuit-breaking behavior around providers.
- Treat webhooks and asynchronous callbacks as untrusted input: authenticate, deduplicate, validate, and make processing replay-safe.

### 5. Protect data and users

- Minimize context before sending it to a model. Redact secrets and unnecessary personal data, and enforce tenant isolation before retrieval.
- Define consent, retention, deletion, export, residency, and training-use rules for prompts, outputs, embeddings, and traces.
- Defend against prompt injection by separating instructions from untrusted content and by enforcing tool authorization outside the model.
- Label AI-generated content where users could mistake it for authoritative human output. Require human review for high-impact writes or decisions.
- Never put secrets in prompts, source code, logs, fixtures, or client bundles.

### 6. Measure quality, reliability, and cost

- Record provider, model, prompt/tool version, latency, token or unit usage, estimated cost, outcome, error category, tenant, and correlation ID without logging prohibited content.
- Define task-specific evaluations before optimizing prompts. Maintain representative cases for normal, adversarial, multilingual, empty, oversized, and provider-failure inputs.
- Start with the least expensive model and reasoning level that passes the evaluation. Route only failed, ambiguous, or explicitly high-value cases to a stronger model and measure whether the fallback improves cost per successful task.
- Keep prompts and tool descriptions lean, place stable reusable content first, cap context and output, and measure provider caching rather than assuming it saves money.
- Deduplicate safe repeated work. Queue latency-insensitive bulk operations and use a provider batch facility only when its current price, retention, and completion window fit the product.
- Track quality, safety, latency, error rate, fallback rate, and cost per successful task. Set tenant-aware budgets and alerts when a paid AI feature exists.
- Keep model calls mockable. Unit and integration tests must not require paid or live model access by default. Run paid evaluation suites intentionally with an explicit budget and dataset version.

### 7. Verify readiness

```text
Validation:
- [ ] Domain operations are callable independently of the UI and any model provider
- [ ] User, tenant, authorization, and correlation context survives async boundaries
- [ ] Sensitive data rules cover prompts, outputs, embeddings, and traces
- [ ] AI outputs and tool arguments are validated before domain use
- [ ] Write-capable tools enforce authorization and human approval where required
- [ ] Timeouts, retries, idempotency, limits, and deterministic fallbacks are tested
- [ ] Model calls are observable, mockable, configurable, and disabled without credentials
- [ ] Representative evaluations cover quality and adversarial failure cases
```

## Connected Skills

- `fabrico-architecture-designing` - for placing AI boundaries in the overall system design
- `fabrico-building-lean-applications` - for AI admission gates, model escalation, total-cost decisions, and risk-based tests
- `fabrico-engineering-prompts` - for secure, versioned runtime prompts and evaluation strategy
- `fabrico-implementing-backend` - for APIs, queues, adapters, tests, and observability hooks
- `fabrico-managing-secrets` - for provider credentials and rotation
- `fabrico-implementing-observability` - for metrics, traces, SLOs, and alerting
- `fabrico-preparing-applications-for-saas` - for tenant-aware entitlements, metering, quotas, and billing boundaries
