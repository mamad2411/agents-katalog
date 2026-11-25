---
name: spring-boot-rest-api-patterns
description: Design and implement robust REST APIs in Spring Boot with validation, error handling, and pagination patterns. Use when building or reviewing Spring Boot HTTP services.
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Spring Boot REST API Patterns

Build predictable, versionable, observable REST APIs in Spring Boot 3.x using Jakarta Validation, RFC 9457 ProblemDetail, keyset pagination, content negotiation, and OpenAPI 3.1.

## Context

You are designing or reviewing a Spring Boot HTTP API. The output must be consistent across endpoints (request shape, status codes, error contract, pagination), safe to evolve, and friendly to both human and machine consumers.

## When to Use This Skill

- New REST API in Spring Boot 3.x.
- Refactoring inconsistent controllers (mixed envelopes, ad-hoc errors, leaked entities).
- Defining team-wide API standards.
- Preparing an API for external/public consumers.

## Prerequisites

- `spring-boot-starter-web` and `spring-boot-starter-validation`.
- `springdoc-openapi-starter-webmvc-ui` (or equivalent) for OpenAPI 3.1 generation.
- Agreed versioning strategy (URI vs. header).
- DTO mapping tool (MapStruct, manual mappers, or Java records as DTOs).

## Instructions

### 1. Contract-First, Resource-Oriented Design

For each endpoint specify route, method, request DTO, response DTO, success status, and error statuses **before** writing code. Generate or hand-write OpenAPI; review the contract in PR.

Resource conventions:

- Plural nouns: `/orders`, `/orders/{id}/items`.
- HTTP verb expresses intent (`GET`, `POST`, `PUT` for full replace, `PATCH` for partial, `DELETE`).
- Avoid RPC verbs in path (`/getOrders`, `/createOrder` are anti-patterns).
- Sub-resources for ownership: `/customers/{id}/orders`.

Status codes:

| Outcome | Status |
| --- | --- |
| Resource created (with `Location` header) | 201 Created |
| Successful read | 200 OK |
| Async accepted | 202 Accepted |
| No body to return | 204 No Content |
| Conditional request not modified | 304 Not Modified |
| Validation failure | 400 Bad Request |
| Unauthenticated | 401 Unauthorized |
| Forbidden | 403 Forbidden |
| Resource not found | 404 Not Found |
| State conflict (duplicate, optimistic lock) | 409 Conflict |
| Business rule violated | 422 Unprocessable Entity |
| Rate limited | 429 Too Many Requests |
| Unhandled fault | 500 Internal Server Error |

### 2. Separate Transport DTOs from Domain/JPA Entities

Never serialize JPA entities directly. Use Java `record`s as immutable DTOs.

```java
public record CreateOrderRequest(
    @NotNull UUID customerId,
    @NotEmpty @Size(max = 100) List<@Valid OrderLine> lines,
    @Size(max = 500) String note) {

    public record OrderLine(
        @NotNull UUID productId,
        @Min(1) @Max(999) int quantity) {}
}

public record OrderResponse(
    UUID id,
    UUID customerId,
    OrderStatus status,
    BigDecimal totalAmount,
    OffsetDateTime createdAt) {}
```

Why: prevents lazy-loading exceptions during serialization, accidental PII leaks, and forced-evolution coupling between persistence and API.

### 3. Validate at the Boundary

Add `@Valid` on every `@RequestBody` and `@PathVariable`/`@RequestParam` constraints at the controller level. Enable `@Validated` on the controller class for parameter constraints.

```java
@RestController
@RequestMapping("/api/v1/orders")
@Validated
class OrderController {

    private final OrderService orders;
    OrderController(OrderService orders) { this.orders = orders; }

    @PostMapping
    ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest req) {
        var created = orders.create(req);
        return ResponseEntity
            .created(URI.create("/api/v1/orders/" + created.id()))
            .body(created);
    }

    @GetMapping("/{id}")
    OrderResponse get(@PathVariable UUID id) {
        return orders.findById(id);
    }
}
```

Validation failures are converted to `MethodArgumentNotValidException` and `ConstraintViolationException`. Map both to `ProblemDetail` (see exception-handling module).

### 4. Use RFC 9457 `ProblemDetail` for Errors

Spring Framework 6 ships `org.springframework.http.ProblemDetail`. Always return `application/problem+json` for non-2xx.

```java
@RestControllerAdvice
class GlobalErrorHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler(OrderNotFoundException.class)
    ProblemDetail handleNotFound(OrderNotFoundException e) {
        var pd = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
        pd.setType(URI.create("https://errors.acme.com/order-not-found"));
        pd.setTitle("Order not found");
        pd.setProperty("code", "ORDER_NOT_FOUND");
        pd.setProperty("orderId", e.getOrderId());
        return pd;
    }

    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(
        MethodArgumentNotValidException ex, HttpHeaders h, HttpStatusCode s, WebRequest r) {
        var pd = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        pd.setTitle("Validation failed");
        pd.setProperty("code", "VALIDATION_ERROR");
        pd.setProperty("errors", ex.getBindingResult().getFieldErrors().stream()
            .map(fe -> Map.of("field", fe.getField(), "message", fe.getDefaultMessage()))
            .toList());
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(pd);
    }
}
```

The `code` property is what clients should branch on. The `type` URI is dereferenceable docs. Never put stack traces, SQL, or internal IDs in the response.

### 5. Pagination, Filtering, Sorting

Enforce a hard cap on page size. Prefer **keyset (cursor) pagination** for sorted, large, or deep-page collections.

Page-based (Spring Data `Pageable`):

```java
@GetMapping
Page<OrderResponse> list(
    @RequestParam(defaultValue = "0") @Min(0) int page,
    @RequestParam(defaultValue = "20") @Min(1) @Max(100) int size,
    @RequestParam(required = false) OrderStatus status) {
    return orders.list(status, PageRequest.of(page, size, Sort.by("createdAt").descending()));
}
```

Keyset (preferred for large datasets):

```java
public record CursorPage<T>(List<T> items, String nextCursor) {}

@GetMapping("/orders")
CursorPage<OrderResponse> list(
    @RequestParam(required = false) String cursor,
    @RequestParam(defaultValue = "50") @Min(1) @Max(100) int size) {
    return orders.listAfter(cursor, size);
}
```

Encode the cursor as opaque base64 of `(createdAt, id)`. Document that clients must treat it as opaque. Never expose `OFFSET` for unbounded datasets - `OFFSET 1000000` scans 1M rows.

### 6. Versioning Strategy

Pick **one** and apply consistently:

| Strategy | Pros | Cons | Use when |
| --- | --- | --- | --- |
| URI: `/api/v1/...` | Visible, cacheable, simple | Breaks pure REST orthodoxy | **Default for most teams** |
| Custom header `X-API-Version: 2` | Clean URLs | Harder to test, cache | Internal-only APIs |
| Media type `Accept: application/vnd.acme.v2+json` | Per-resource versioning | Heavy for clients | Public APIs needing fine-grained evolution |

Define deprecation policy **before** v1 ships: `Deprecation:` and `Sunset:` headers (RFC 8594, RFC 9745), changelog, minimum support window (e.g., 12 months).

### 7. Content Negotiation, Caching, Idempotency

- Serve `application/json`; reject unknown `Content-Type` with 415.
- For cacheable GETs, support `ETag` (Spring's `ShallowEtagHeaderFilter` or compute weak ETags) and honor `If-None-Match`.
- For unsafe operations that may be retried, accept `Idempotency-Key` header and persist a request hash + response for replay (RFC draft, common in payments).

### 8. Document with OpenAPI 3.1 (Live, Not Maintained-by-Hand)

Use `springdoc-openapi`. Annotate intent only when generation cannot infer:

```java
@Operation(summary = "Create order", responses = {
    @ApiResponse(responseCode = "201", description = "Created"),
    @ApiResponse(responseCode = "422", description = "Business rule violated",
        content = @Content(schema = @Schema(implementation = ProblemDetail.class)))
})
@PostMapping
ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest req) { ... }
```

Publish the spec on `/v3/api-docs`. Lint with Spectral in CI. Generate client SDKs from the spec; never hand-write them.

### 9. Tests at the API Boundary

Minimum coverage per controller:

- `@WebMvcTest` happy path with `MockMvc` + JSONPath asserts.
- Validation failure -> 400 + ProblemDetail shape.
- Domain error -> mapped status + `code` property.
- Authorization denied -> 401/403.
- Serialization snapshot for any breaking-change-risk endpoint.

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {
    @Autowired MockMvc mvc;
    @MockBean OrderService orders;

    @Test
    void rejectsEmptyLines() throws Exception {
        mvc.perform(post("/api/v1/orders").contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {"customerId":"%s","lines":[]}
                    """.formatted(UUID.randomUUID())))
            .andExpect(status().isBadRequest())
            .andExpect(content().contentType(MediaType.APPLICATION_PROBLEM_JSON))
            .andExpect(jsonPath("$.code").value("VALIDATION_ERROR"));
    }
}
```

## Common Pitfalls

| Anti-pattern | Why it hurts | Fix |
| --- | --- | --- |
| Returning JPA entities from controllers | Lazy-init exceptions, PII leaks, locked schema | Dedicated DTO records + mapper |
| Custom `{ "success": false, "data": null, "msg": "..." }` envelope | Reinvents HTTP, breaks tooling | Use HTTP status + `ProblemDetail` |
| `@RequestParam` without bounds (`size=100000`) | DoS vector | `@Max(100)` cap |
| Deep `OFFSET` pagination on large tables | Linear scan, latency cliff | Keyset/cursor pagination |
| Different error shapes per controller | Clients code per-endpoint hacks | One `@RestControllerAdvice` |
| Verbs in URLs (`/api/createOrder`) | Not REST, harder to cache, harder to evolve | Resource + method |
| Bumping URI version for additive changes | Forces client churn | Add fields (non-breaking); only bump for breaking changes |
| Storing OpenAPI by hand | Drifts from code immediately | Generate with springdoc + lint with Spectral |

## Output Format

When applying this skill, deliver:

1. Endpoint contract table (route, method, request, response, statuses, auth).
2. DTO records with validation annotations.
3. Controller code following the patterns above.
4. ProblemDetail mapping table (exception -> status + code).
5. Pagination decision per endpoint (page vs. keyset, cap).
6. Versioning + deprecation plan.
7. OpenAPI spec snippet or link to generated `/v3/api-docs`.
8. Test matrix (happy, validation, domain error, auth, serialization).

## Authoritative References

- Spring MVC reference: https://docs.spring.io/spring-framework/reference/web/webmvc.html
- ProblemDetail (Spring Framework 6): https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html
- Jakarta Bean Validation 3.0: https://jakarta.ee/specifications/bean-validation/3.0/
- RFC 9457 - Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc9457.html
- RFC 9110 - HTTP Semantics: https://www.rfc-editor.org/rfc/rfc9110.html
- RFC 8594 / 9745 - Deprecation & Sunset headers: https://www.rfc-editor.org/rfc/rfc8594.html
- OpenAPI 3.1 specification: https://spec.openapis.org/oas/v3.1.0
- springdoc-openapi: https://springdoc.org/
- OWASP API Security Top 10 (2023): https://owasp.org/API-Security/editions/2023/en/0x00-header/
- Microsoft REST API guidelines: https://github.com/microsoft/api-guidelines
- Zalando RESTful API guidelines: https://opensource.zalando.com/restful-api-guidelines/
