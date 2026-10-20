---
name: spring-endpoint
description: Add or change a Spring Boot HTTP endpoint end-to-end, following the conventions already present in this codebase — controller, request/response DTOs, Bean Validation, application service with an explicit transaction boundary, repository, RFC 9457 error mapping, Testcontainers integration test and OpenAPI entry. Use whenever a new REST operation is requested, or an existing one gains a field, a status code or a validation rule.
user-invocable: true
argument-hint: "<HTTP method> <path> [--module <name>]"
agent: foundry-dev:spring-engineer
model: sonnet
effort: medium
metadata:
  foundry.vertical: dev
  foundry.io: "requirement.v1 -> review.v1"
license: Apache-2.0
---

# Add a Spring Boot endpoint

An endpoint is not a controller method. It is eight artefacts that must agree: route, request
DTO, validation, use case, transaction boundary, persistence, error model, contract document —
plus the tests that prove they agree. Ship all of them or ship nothing.

This skill produces a **complete vertical slice** in the project's existing style. It never
introduces a new architectural pattern; if the required pattern is missing, it stops and says so.

## When not to use this

- The change is a pure read optimisation of an existing endpoint → `optimise-query`.
- The endpoint requires a schema change → run `write-migration` first; this skill assumes the
  column exists.
- The API shape itself is undecided (resource naming, pagination, idempotency semantics) →
  `design-api-contract` first. This skill implements a decided contract; it does not design one.
- Removing or breaking an existing endpoint → `api-deprecation`.
- The application is WebFlux/reactive. The steps below assume Spring MVC. Detect first
  (step 1); if reactive, stop and report, because `MockMvc`, `@Transactional` semantics and
  blocking repositories all differ.

## Step 1 — Detect conventions (never skip)

Run these before writing a line. The output decides where files go and how they are named.

```bash
# module layout and architectural style
find src/main/java -maxdepth 4 -type d | sed 's|src/main/java/||' | sort | head -40
# MVC or WebFlux?
grep -rn 'spring-boot-starter-web\b\|spring-boot-starter-webflux' pom.xml build.gradle build.gradle.kts 2>/dev/null
# an existing endpoint to copy the shape from (pick the most recently modified)
grep -rln '@RestController' src/main/java --include=*.java | xargs ls -t 2>/dev/null | head -3
# DTO style: records? separate request/response? a mapper?
grep -rn 'public record .*Request\|public record .*Response' src/main/java --include=*.java | head -10
grep -rln 'MapStruct\|@Mapper' src/main/java --include=*.java | head -3
# error model already wired?
grep -rn '@RestControllerAdvice\|ProblemDetail\|ErrorResponseException' src/main/java --include=*.java | head
# OpenAPI: generated from code, or a committed spec?
grep -rn 'springdoc\|swagger\|openapi' pom.xml build.gradle build.gradle.kts 2>/dev/null
ls -1 **/openapi*.y*ml api/*.y*ml 2>/dev/null
# test conventions
grep -rln '@WebMvcTest\|@SpringBootTest\|Testcontainers' src/test/java --include=*.java | head -5
```

Write the answers down in one short block before proceeding. If two conventions coexist (some
DTOs are records, some are classes), follow the **newest** file's convention and say which you
picked. Do not average them.

`references/detection-matrix.md` maps each command's output to a concrete decision.

## Step 2 — Write the failing test first

If `superpowers` is installed, invoke `superpowers:test-driven-development` and follow it.
If it is absent, apply this reduced rule: the first artefact you write is a test that fails
because the endpoint does not exist, and you run it and read the failure.

Two tests, minimum:

**a. Slice test** (`@WebMvcTest`) — routing, deserialisation, validation, status codes, and
the error body. Service mocked. Fast.

**b. Integration test** (`@SpringBootTest` + Testcontainers) — the real path through the
service, the real repository, the production database engine, the real migrations.

Never use H2 for (b). H2's "PostgreSQL mode" accepts SQL PostgreSQL rejects and locks
differently; a green H2 test is not evidence.

Assert, at minimum:
- the happy-path status code and body;
- one validation failure: status 400, `Content-Type: application/problem+json`, and the stable
  `type` URI;
- authorisation: an unauthenticated call and a call by a user who must not see the resource;
- for a collection: pagination boundaries (page 0, past-the-end, an oversized `size`);
- for an unsafe method: idempotency or conflict behaviour.

Templates: `references/test-templates.md`.

## Step 3 — Request and response DTOs

- Java `record`s in the module's DTO package. Never expose a JPA entity — it leaks the schema,
  turns every column rename into a breaking API change, and invites
  `LazyInitializationException` at serialisation time.
- **Separate request and response types**, even when the fields match today. They diverge the
  moment you add a server-computed field.
- Never accept a client-controlled `id`, `createdAt`, `version`, `tenantId` or role field on a
  create request. Mass assignment through a shared DTO is the most common privilege-escalation
  bug in this shape of code.
- Money is `BigDecimal` with an explicit currency; timestamps are `Instant`/`OffsetDateTime`
  serialised as ISO-8601 with an offset. Never a bare local date-time.
- Nullability is part of the contract. An `Optional` field in a request means "absent";
  distinguish absent from explicit null if the API supports partial update (`PATCH`), and say
  which semantics you chose in the OpenAPI description.

## Step 4 — Validation

- Jakarta Bean Validation on the request record components; `@Valid` on the controller
  parameter. Add `@Validated` on the controller class if you constrain `@RequestParam` or
  `@PathVariable`.
- Cross-field rules go in a `ConstraintValidator`, not an `if` at the top of the service.
- Bound every collection and string: `@Size(max = ...)` on lists and text. An unbounded list
  parameter is a denial-of-service vector.
- Validation checks **format**. Domain invariants ("the order must be open") stay in the
  domain and produce a 409, not a 400. Do not delete the domain check because the DTO is
  annotated.

## Step 5 — Controller

- Thin. Map HTTP to a use-case call and back. No conditional on domain state, no repository
  access, no transaction annotation.
- Return `ResponseEntity` only where you need to set headers or a non-default status;
  otherwise return the body and annotate the status.
- Status codes, applied honestly:
  `201 Created` with a `Location` header for creation; `204 No Content` for a delete or a
  command with no body; `200` for a read; `409 Conflict` for an invariant or optimistic-lock
  failure; `422` only if the project already distinguishes it from 400 — pick one and be
  consistent; `404` rather than `403` when revealing existence is itself a leak.
- Use `@RequestBody @Valid`. Use `@PageableDefault` with a **maximum** page size — a caller
  asking for `size=100000` must be clamped, not served.
- For unsafe methods on a versioned aggregate, require `If-Match` with the ETag (RFC 9110
  §13); respond 428 when absent, 412 when stale.

## Step 6 — Application service and transaction boundary

- The transaction boundary is here, on the method that represents one unit of work.
  `@Transactional` on the service; `@Transactional(readOnly = true)` for reads.
- **Decide and state the propagation.** Default `REQUIRED` unless you can justify otherwise.
  `REQUIRES_NEW` takes a second connection for the duration — see `persistence-engineer`
  before using it.
- **No remote call inside the transaction.** Holding a database connection across someone
  else's timeout is how a pool exhausts. Move the call out, or write an outbox row in the same
  transaction and relay it after commit.
- Publish domain events after commit (`@TransactionalEventListener(phase = AFTER_COMMIT)`),
  never inside — an event emitted for a transaction that then rolls back is a lie other
  services will act on.
- A `private @Transactional` method is always a bug: the proxy cannot advise it and the
  annotation silently does nothing.

## Step 7 — Repository

- Spring Data interface method, `@Query`, or an explicit projection. Prefer a **projection or
  DTO query** when the endpoint returns a flat view — do not load managed entities to copy
  three fields.
- Every `*ToOne` association on any entity you touch must be `FetchType.LAZY`.
- After the integration test passes, count the statements the endpoint issues. If it scales
  with the number of returned rows, stop and hand off to `optimise-query`.
  ```bash
  ./mvnw -q test -Dtest=<YourIT> -Dspring.profiles.active=sql 2>&1 | grep -c '^Hibernate: '
  ```

## Step 8 — Error model

Wire the endpoint into the existing `@RestControllerAdvice`. If the project has none, create
exactly one, extending `ResponseEntityExceptionHandler`, and say so in the report — it is an
architectural addition, not a detail.

- Every failure mode of this endpoint maps to a `ProblemDetail` (RFC 9457) with a **stable,
  dereferenceable `type` URI** you own. `about:blank` for a domain error is a defect.
- `title` is stable per `type`; `detail` is human-readable.
- **Never** put an exception message, stack frame, SQL fragment, internal hostname or another
  user's data in the response. Log those with a correlation id and return the id.
- Field errors go into a documented extension property, not concatenated into `detail`.
- Assert `Content-Type: application/problem+json` in the test — a test that checks only the
  status code passes while the body is wrong.

`references/error-catalogue.md` holds the `type` URI naming scheme and the standard mappings.

## Step 9 — OpenAPI

- If the spec is generated (springdoc-style), annotate so the generated document is correct:
  operation summary, every response status including the error ones, and the `ProblemDetail`
  schema for each.
- If the spec is committed and hand-maintained (design-first), update it in the **same commit**
  and regenerate whatever is generated from it.
- Regenerate and diff against the base branch. An additive diff is fine; anything that removes
  or narrows must go through `api-deprecation` instead.

```bash
./mvnw -q verify   # or ./gradlew build — whichever generates the spec
git diff --stat -- '*openapi*.json' '*openapi*.yaml' '*openapi*.yml'
```

## Step 10 — Verify, then report

If `superpowers` is installed, invoke `superpowers:verification-before-completion`. Otherwise
run every command below and read the output — do not infer.

```bash
./mvnw -q verify            # or ./gradlew build
grep -rn '@Autowired' <files you touched>          # must be empty
grep -rn 'FetchType.EAGER' <entities you touched>  # must be empty
```

Then record the result. Write a `review.v1` artifact to
`.foundry/blackboard/<wave>/spring-endpoint.json` with `blackboard_write`, listing anything you
found but did not fix as a `finding.v1` with a `failureScenario`. Return ≤ 300 tokens to the
caller: the artifact path, the route added, and the statement count per request.

## Exit criteria

- [ ] Build and the full test suite are green, run by you, output read.
- [ ] Slice test asserts status, body, and the error `type` URI for at least one 4xx.
- [ ] Integration test runs against the production database engine via Testcontainers, with
      the project's real migrations applied.
- [ ] No JPA entity appears in a controller signature.
- [ ] No client-settable `id`, `tenantId`, `version` or role field on any request DTO.
- [ ] Exactly one transaction boundary, on the application service, with the propagation
      chosen deliberately; no remote call inside it.
- [ ] Statement count per request does not scale with the number of rows returned.
- [ ] Every declared response status has a documented `ProblemDetail` `type`.
- [ ] OpenAPI regenerated; the diff is additive.
- [ ] Page size is clamped to a documented maximum.
- [ ] `review.v1` written; caller summary ≤ 300 tokens.

## Deliberately not covered

Authentication and authorisation **design** (this skill only enforces that the endpoint is
protected and tested for the negative case); rate limiting and quota policy; caching headers
and CDN behaviour; API versioning and deprecation (`service-versioning-engineer`); schema
changes (`write-migration`); query tuning (`optimise-query`); WebFlux; Kotlin idioms;
GraphQL and gRPC surfaces.

## Degradation

No Docker → the integration test cannot run. Report the integration criterion **unverified**;
do not substitute H2. No springdoc or committed spec → say the API is undocumented and emit it
as a `finding.v1` rather than inventing a document format. No `superpowers` → follow the
reduced rules stated inline at steps 2 and 10. No `foundry` MCP server → write the artifact
file directly and note that it was not schema-validated.
