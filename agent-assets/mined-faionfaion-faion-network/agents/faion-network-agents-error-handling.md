# Error Handling with RFC 7807 Problem Details

## Summary

**One-sentence:** Produces one application/problem+json envelope across every REST endpoint (RFC 7807 type/title/status/detail/instance/traceId + optional errors[]) with one framework handler and a JSON Schema gate.

**One-paragraph:** Every error returns `type` (URI), `title`, `status` (matching HTTP code), `detail`, `instance`, `traceId`, and an optional `errors[]` array for field-level validation failures. All endpoints share one shape, one content-type (`application/problem+json`), one framework-level exception handler. For 5xx errors, `detail` is a static string — never an exception message, stack trace, or SQL. `traceId` is populated from the W3C `traceparent` header or a generated UUID so on-call can correlate a customer's report with internal logs in one lookup.

**Ефективно для:** new REST APIs, refactors merging mixed error shapes into one, public-facing APIs where the error envelope is part of the contract, API-gateway/BFF setups translating downstream errors, multi-service architectures where clients must not memorise per-service formats.

## Applies If (ALL must hold)

- The API speaks JSON over HTTP (not gRPC, not GraphQL, not streaming).
- Clients are heterogeneous and benefit from a single error parser.
- You can register one global exception handler at the framework level.
- The team accepts `application/problem+json` as the response content-type.

## Skip If (ANY kills it)

- gRPC service — use `google.rpc.Status` + `error_details` instead.
- GraphQL — errors live in the response `errors[]` array per spec.
- Internal-only low-stability APIs where the envelope overhead outweighs benefit.
- Streaming endpoints (SSE, WebSocket) — error frames follow their own conventions.
- Static asset / file download endpoints — return raw HTTP status, no body.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Framework choice | string (fastapi / express / spring / django-rest) | tech stack ADR |
| List of HTTP status codes the API emits | YAML/Markdown table | OpenAPI spec or BA ticket |
| Trace-context header name | string (`traceparent` per W3C) | observability conventions |
| Domain of error-type URIs | string (`https://api.example.com/errors/`) | API governance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[language-framework-guide]]` | Stack choice determines which exception-handler API is used. |
| `[[go-http-handlers]]` or `[[nodejs-express-fastify]]` or `[[python-fastapi]]` | Framework-specific middleware wiring. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules: shape, content-type, status match, traceId, 5xx masking, errors[] usage, type URIs as contract, one handler | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for ProblemDetails + valid/invalid response examples | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: leaked exception text, wrong content-type, mismatched status, errors[] misuse, per-route shapes, missing traceId | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure: declare type URIs → write ProblemDetail model → register one handler → contract-test → wire trace-context | ~900 |
| `content/05-examples.xml` | medium | FastAPI + Express + Spring full worked examples | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "Is this a JSON-over-HTTP REST API where clients want generic error handling?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate ProblemDetail model + handler | sonnet | Mechanical, framework-templated. |
| Author error type URIs + titles | sonnet | Naming conventions, low ambiguity. |
| Contract-test schema authoring | sonnet | Schema mirrors the model. |
| Triage why a downstream returns a non-conforming error | opus | Multi-source diagnosis (network, framework, middleware order). |

## Templates

| File | Purpose |
|------|---------|
| `templates/problem-details.schema.yaml` | JSON Schema 2020-12 for the ProblemDetails body — drop-in for jsonschema/ajv/schemathesis. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-error-handling.py` | Validates a sample HTTP response body+headers against the ProblemDetails schema. | Contract test in CI; on-call debugging of a non-conforming endpoint. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[go-http-handlers]]` — Go middleware integration
- `[[python-fastapi]]` — FastAPI exception handler integration
- `[[nodejs-express-fastify]]` — Node middleware integration

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters protocol (JSON-over-HTTP only), framework support for one handler, and whether the team accepts `application/problem+json`. If any branch fails, defer to gRPC/GraphQL-specific conventions or skip the envelope.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/problem-details.schema.yaml`

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
$id: "https://api.example.com/schemas/problem-details"
type: object
required: [type, title, status]
properties:
  type:
    type: string
    format: uri
  title:
    type: string
  status:
    type: integer
    minimum: 100
    maximum: 599
  detail:
    type: string
  instance:
    type: string
  traceId:
    type: string
  errors:
    type: array
    items:
      type: object
      required: [field, code, message]
      properties:
        field:
          type: string
        code:
          type: string
        message:
          type: string
additionalProperties: true
```
