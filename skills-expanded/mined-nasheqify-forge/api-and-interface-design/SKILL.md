---
name: api-and-interface-design
description: >
  API and interface design discipline (Hyrum's law, contract-first, validate at
  boundaries, prefer addition over modification). Use when designing a new API,
  module boundary, type contract between modules, REST/SSE endpoint, or schema
  pipeline boundary.
status: active
invocation:
  primary: user-facing
  secondary: [workflow-step, sub-skill]
  trigger_patterns:
    - "design API"
    - "interface design"
    - "module boundary"
    - "API contract"
    - "endpoint design"
    - "schema pipeline"
disable-model-invocation: false
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: api-and-interface-design

## Purpose

Design stable, well-documented interfaces that are
hard-to-misuse. Good interfaces make the right thing easy and
the wrong thing hard. Applies to REST APIs, SSE streams,
module boundaries, Pydantic models, component props, and any
surface where one piece of code talks to another.

Complementary to `agents/code-api-contract.md` (persona
reviewer for existing APIs) — this skill is the **authoring
discipline** for new interfaces; the persona is the review
counterpart.

Absorbs the existing schema-pipeline reality (Pydantic →
OpenAPI → Zod) as a concrete pattern.

## Source

agent-skills at `eb07f19` (MIT License, © 2025 Addy Osmani); Forge's register of adopted methods.

## Standalone

Distinct from:
- `agents/code-api-contract.md` (persona) — review role for
  existing APIs in code_review_board L2. This skill is the
  authoring stage.
- `skills/spec_authoring/SKILL.md` — general spec writing.
  This skill specializes in interface design within the
  spec.
- `skills/code_review_board/SKILL.md` — the whole code
  review board. This skill feeds the board with consistently
  designed APIs.

What only this skill delivers:
- Hyrum's law as an explicit authoring requirement (hidden
  behaviour as a de-facto contract).
- One-version rule (diamond-dependency avoidance).
- 5 authoring requirements (contract-first / consistent
  errors / validate-at-boundaries / prefer-addition /
  predictable-naming).
- REST + SSE patterns specifically.
- Discriminated unions / input-output separation /
  branded types for Pydantic.

## When to call

- Designing new API endpoints (REST or SSE).
- Defining module boundaries or contracts between teams.
- Creating Pydantic model schemas.
- Designing a database schema that informs the API shape.
- Changing existing public interfaces (Hyrum's-law
  obligation).

### Do not call for

- Internal function signatures that are not a public API →
  `code-quality` (naming axis).
- DB schema without API implication →
  `agents/code-data.md` persona.
- Pre-existing endpoint bug fix → `fix` workflow + L1
  review.
- General spec writing → `spec_authoring`.

## Process

Before designing a new interface or changing an existing public one, and before writing its contract: read and
follow `skills/api_and_interface_design/authoring.md` (phases 1–7: Hyrum's law, the one-version rule, contract-first,
consistent error semantics with the status-code mapping, validate-at-boundaries, prefer addition over modification,
predictable naming).

## REST, SSE and Pydantic patterns

When defining REST endpoints, an SSE event stream or Pydantic models, and before changing a model that feeds the
schema pipeline: read and follow `skills/api_and_interface_design/patterns.md` (REST API patterns: resource design,
pagination, filtering, PATCH; SSE patterns and obligations; Pydantic patterns: discriminated unions, input / output
separation, branded IDs, schema pipeline Pydantic → OpenAPI → Zod).

## Red flags

- Endpoints that return different shapes depending on
  conditions.
- Inconsistent error formats across endpoints (some
  `raise HTTPException`, some AppError, some return None).
- Validation scattered in the internal code instead of at
  boundaries.
- Breaking changes to existing fields (type changes,
  removals).
- List endpoints without pagination.
- Verbs in REST URLs (`/api/createTask`, `/api/getUsers`).
- Third-party API responses without validation.
- `extra="ignore"` (default) instead of `extra="forbid"` on
  public request models.
- SSE events without an explicit event schema.
- StreamingResponse errors thrown as HTTPException (too
  late).

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "We document the API later" | The Pydantic models ARE the documentation. Define them first. |
| "We don't need pagination yet" | As soon as someone has 100+ items you'll need it. Add it from the start. |
| "PATCH is complicated, let's use PUT" | PUT requires the full object every time. PATCH is what clients actually want. |
| "We version the API when needed" | Breaking changes without versioning break consumers. Design for extension from the start. |
| "Nobody uses the undocumented behaviour" | Hyrum's law: if it's observable, somebody depends on it. Treat every public behaviour as a commitment. |
| "We can just maintain two versions" | Multi-version maintenance multiplies cost and creates diamond dependencies. Cross-ref the one-version rule (`authoring.md` phase 2). |
| "Internal APIs don't need contracts" | Internal consumers are also consumers. Contracts prevent coupling and enable parallel work. |
| "extra=ignore is the default; that's fine" | Silent pass-through. Unknown fields are NOT recognized → drift. **extra=forbid** on public request models. |

## Contract

### INPUT
- **Required:** use case described (which resource, which
  operations).
- **Required:** consumer identified (frontend React,
  internal module, external API).
- **Optional:** existing schema-pipeline context (Pydantic
  models present?).
- **Context:** `framework/spec-engineering.md` 5 primitives,
  `agents/code-api-contract.md` persona,
  `skills/code_review_board/SKILL.md` (downstream review).

### OUTPUT
**DELIVERS:**
- Pydantic model schemas (input + output + error).
- REST / SSE endpoint definitions with status-code mapping.
- Pagination schema for list endpoints.
- Discriminated union for variants.
- Naming convention applied.
- Hyrum's-law considerations documented (which behaviours
  expose? which internal?).

**DOES NOT DELIVER:**
- No implementation logic — contract-first; implementation
  follows separately.
- No database schema — `agents/code-data.md` persona /
  spec authoring.
- No frontend code — the schema pipeline produces Zod;
  frontend code follows separately.

**ENABLES:**
- A stable public API with clear boundaries.
- A backward-compatible extension path.
- Schema-pipeline consistency (Pydantic → OpenAPI → Zod).
- code-api-contract persona can review consistently.

### DONE
- Every endpoint has typed input + output schemas.
- Error responses follow one consistent form (AppError +
  ErrorResponse).
- Validation only at system boundaries.
- List endpoints support pagination.
- New fields are additive + optional (backward compatible).
- Naming follows consistent conventions across every
  endpoint.
- API doc or types committed with the implementation.
- SSE events explicitly defined (when applicable).

### FAIL
- **Retry:** schema inconsistency detected → fix, then
  re-review.
- **Escalate:** Hyrum's-law consequence unclear →
  solution-expert or council for an architectural decision.
- **Abort:** replacement not designed but the old API
  should be deprecated → build the replacement first, then
  deprecate (cross-ref `deprecation_and_migration`).

## See also

- `agents/code-api-contract.md` — persona reviewer
  (counterpart to this skill).
- `skills/deprecation_and_migration/SKILL.md` — when a
  breaking change is needed.
- `skills/code_review_board/SKILL.md` — downstream review
  of the API implementation.
- `framework/spec-engineering.md` — 5 primitives (spec
  writing); applies to API specs.
- `skills/spec_authoring/SKILL.md` — when an API is part
  of a larger spec.
