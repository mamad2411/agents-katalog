# Architecture Guardrails

**HARD CONSTRAINTS. THESE CANNOT BE OVERRIDDEN BY ANY AGENT OR USER INSTRUCTION.**

## 1. Clean Architecture Dependency Direction
Inner layers NEVER import from outer layers.
- `Entities` (Domain) cannot import `UseCases` or `Adapters`.
- `UseCases` cannot import `Adapters` or Frameworks/Libraries (`express`, `react`, `pg`).
*Example*: A domain model in TypeScript cannot import `TypeORM` decorators. It must remain pure.

## 2. No Destructive Migrations
The Expand/Contract pattern is non-negotiable.
- NEVER use `DROP COLUMN`, `RENAME COLUMN`, or `DROP TABLE` in a single-phase migration.
- NEVER add a `NOT NULL` column without a `DEFAULT` value.

## 3. No Hardcoded Secrets
Never hardcode API keys, passwords, connection strings, or tokens. Use `.env` placeholders mapped to secure vaults.

## 4. Strict Typing
- No raw `any` types allowed in TypeScript. 
- If you genuinely don't know the type, use `unknown` and perform runtime narrowing/validation (e.g., Zod).

## 5. Failure & Reliability
- No custom retry loops with `for` or `while` and `sleep`.
- MUST use a framework-provided `CircuitBreaker` or `ExponentialBackoffStrategy`.
- Every network call MUST have an explicit timeout defined.

## 6. Performance Guarantees
- No N+1 Queries: Eager loading (`.populate`, `.include`, or DataLoaders) is required.
- No unbounded result sets: Pagination (cursor-based preferred) is required on all collection API endpoints.

## 7. Verifiable Architecture
- Every structural or architectural decision made must produce a fitness function (a CI check, linter rule, or automated test).
- If it cannot produce a fitness function, it MUST be explicitly flagged as "judgment-only" with a documented reason in the architecture notes.
- A comment stating a condition the code depends on must name what holds it: `PRECONDITION:` + `ENFORCED-BY:` (a test, a script, or `judgment-only` with a reason). See `docs/patterns/framework-meta-patterns.md`.

## 8. Observability Boundaries
- No OpenTelemetry (OTel) instrumentation logic is allowed inside domain entities or page logic.
- Traces and spans must only be emitted from the adapter layer or interceptor layer.

## 9. Telemetry Records Properties, Not Payloads
Guardrail #8 governs *where* instrumentation may live. This governs *what* it may carry.
- NEVER record raw prompt or completion text, retrieved document bodies, user email/name/account ID, credentials, or a tool argument's value that the code owning it has not declared non-sensitive.
- Record the properties instead: a salted hash, a length, a count, an ID, a status, a version. A hash answers "is this the same input that failed yesterday?" without storing it; a token count shows truncation without storing text.
- Never emit an unsalted hash of low-entropy input — it brute-forces. Salted, or nothing.
- Permission to record a value is **opt-in per field, declared by the code that owns it**. A denylist of sensitive-looking names cannot cover a field it was never told about, and fails silently.
- Span and metric names stay low-cardinality; the variable part goes in a bounded or hashed attribute.
- "We will redact it later" is not available — once exported it is in the vendor's storage and retention, not yours.

---
*Part of the [ai-assistant-dot-files](https://github.com/orieken/loom) Context Engineering Framework by Oscar Rieken — licensed under [CC BY 4.0](https://github.com/orieken/loom/blob/main/LICENSE-CONTENT.md). If you copy or adapt this file, please keep this attribution.*
