---
name: spring-boot-exception-handling
description: Build consistent exception handling in Spring Boot with domain exceptions, global handlers, and stable error contracts. Use when implementing or reviewing API error behavior.
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Spring Boot Exception Handling

Build a unified, RFC 9457-compliant exception strategy in Spring Boot 3.x: domain exception taxonomy, single `@RestControllerAdvice`, stable error catalog, predictable rollback semantics, and clean separation between client-visible errors and internal diagnostics.

## Context

You are designing or reviewing error handling in a Spring Boot service. Output must be one consistent error contract across all endpoints, with no stack traces leaked to clients, no swallowed exceptions, and rollback behavior aligned with exception types.

## When to Use This Skill

- Defining the API error response standard.
- Eliminating scattered try/catch + `ResponseEntity.status(400).body(...)` from controllers.
- Implementing a global handler for the first time.
- Aligning transaction rollback with the exception model.

## Prerequisites

- Spring Boot 3.x (uses `org.springframework.http.ProblemDetail`).
- REST API patterns module reviewed (this module produces the contract that REST clients consume).
- Logging module reviewed (this module decides what gets logged at which level).
- Decision on error code namespace (per-domain prefix, e.g., `ORDER_*`, `PAYMENT_*`).

## Instructions

### 1. Exception Taxonomy

Group exceptions by intent, then map each group to an HTTP status. Three layers:

| Layer | Examples | Translates to |
| --- | --- | --- |
| Framework / validation | `MethodArgumentNotValidException`, `HttpMessageNotReadableException`, `ConstraintViolationException`, `MethodArgumentTypeMismatchException` | 400 |
| Spring Security | `AuthenticationException`, `AccessDeniedException` | 401 / 403 |
| Domain (your code) | `OrderNotFoundException`, `OrderAlreadyCancelledException`, `InsufficientStockException` | 404 / 409 / 422 |
| Infrastructure | `DataIntegrityViolationException`, `OptimisticLockingFailureException`, `ResourceAccessException` (RestClient timeout) | 409 / 502 / 504 |
| Unhandled | anything else | 500 |

### 2. Domain Exception Base Class

Domain exceptions carry a stable `code` and an HTTP status hint. Keep them framework-free (no Spring imports).

```java
public abstract class DomainException extends RuntimeException {
    private final String code;
    protected DomainException(String code, String message) { super(message); this.code = code; }
    protected DomainException(String code, String message, Throwable cause) { super(message, cause); this.code = code; }
    public String code() { return code; }
}

public class OrderNotFoundException extends DomainException {
    private final UUID orderId;
    public OrderNotFoundException(UUID orderId) {
        super("ORDER_NOT_FOUND", "Order " + orderId + " not found");
        this.orderId = orderId;
    }
    public UUID orderId() { return orderId; }
}

public class OrderAlreadyCancelledException extends DomainException {
    public OrderAlreadyCancelledException(UUID orderId) {
        super("ORDER_ALREADY_CANCELLED", "Order " + orderId + " is already cancelled");
    }
}
```

Anti-patterns: throwing generic `RuntimeException("not found")`, returning `null` to signal absence, returning `Optional` from a service for a "must exist" lookup (forces caller to invent the not-found story).

### 3. Single Global Handler with `@RestControllerAdvice`

Order matters: more specific exceptions first, fallback last. Extend `ResponseEntityExceptionHandler` to inherit Spring's framework-exception coverage in `application/problem+json`.

```java
@RestControllerAdvice
class GlobalErrorHandler extends ResponseEntityExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalErrorHandler.class);

    @ExceptionHandler(OrderNotFoundException.class)
    ProblemDetail handle(OrderNotFoundException e) {
        var pd = problem(HttpStatus.NOT_FOUND, "Order not found", e);
        pd.setProperty("orderId", e.orderId());
        return pd;
    }

    @ExceptionHandler(DomainException.class)              // catch-all for our domain
    ProblemDetail handleDomain(DomainException e) {
        var status = switch (e.code()) {
            case "ORDER_ALREADY_CANCELLED",
                 "INSUFFICIENT_STOCK"            -> HttpStatus.CONFLICT;
            case "INVALID_STATE_TRANSITION"      -> HttpStatus.UNPROCESSABLE_ENTITY;
            default                              -> HttpStatus.UNPROCESSABLE_ENTITY;
        };
        return problem(status, e.getMessage(), e);
    }

    @ExceptionHandler(OptimisticLockingFailureException.class)
    ProblemDetail handleOptimistic(OptimisticLockingFailureException e) {
        return problem(HttpStatus.CONFLICT, "Concurrent modification detected", "CONCURRENT_MODIFICATION", e);
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    ProblemDetail handleDataIntegrity(DataIntegrityViolationException e) {
        log.warn("data integrity violation", e);
        return problem(HttpStatus.CONFLICT, "Constraint violation", "DATA_INTEGRITY", e);
    }

    @ExceptionHandler(AccessDeniedException.class)
    ProblemDetail handleForbidden(AccessDeniedException e) {
        return problem(HttpStatus.FORBIDDEN, "Forbidden", "FORBIDDEN", e);
    }

    // Override Spring's hook for body-parse failures, validation, etc.
    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(
        MethodArgumentNotValidException ex, HttpHeaders h, HttpStatusCode s, WebRequest r) {
        var pd = problem(HttpStatus.BAD_REQUEST, "Validation failed", "VALIDATION_ERROR", ex);
        pd.setProperty("errors", ex.getBindingResult().getFieldErrors().stream()
            .map(fe -> Map.of("field", fe.getField(), "message", fe.getDefaultMessage(),
                              "rejectedValue", String.valueOf(fe.getRejectedValue())))
            .toList());
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(pd);
    }

    @ExceptionHandler(Exception.class)                    // last resort
    ProblemDetail handleUnhandled(Exception e) {
        log.error("unhandled exception", e);
        var pd = problem(HttpStatus.INTERNAL_SERVER_ERROR, "Internal server error", "INTERNAL_ERROR", e);
        // No detail leak: do NOT include e.getMessage() for unknown exceptions.
        pd.setDetail("An unexpected error occurred. Please contact support with traceId.");
        return pd;
    }

    private ProblemDetail problem(HttpStatus status, String title, Throwable e) {
        return problem(status, title, e instanceof DomainException de ? de.code() : "ERROR", e);
    }

    private ProblemDetail problem(HttpStatus status, String title, String code, Throwable e) {
        var pd = ProblemDetail.forStatusAndDetail(status, e.getMessage());
        pd.setTitle(title);
        pd.setType(URI.create("https://errors.acme.com/" + code.toLowerCase().replace('_','-')));
        pd.setProperty("code", code);
        pd.setProperty("traceId", currentTraceId());        // from Micrometer Tracing MDC
        pd.setProperty("timestamp", OffsetDateTime.now());
        return pd;
    }

    private static String currentTraceId() {
        return MDC.get("traceId");
    }
}
```

### 4. Logging Severity Aligned with Cause

| Cause | Level | Stack trace? |
| --- | --- | --- |
| Validation 400 | `debug` (or none) | No |
| Auth 401/403 | `info` (audit) | No |
| Domain 404/409/422 | `warn` (without trace) | No |
| Infra (DB down, timeout) | `error` | Yes |
| Unhandled 500 | `error` | Yes |

Never log expected user-input failures at `error`. They will drown real signals and break alerts.

### 5. Error Code Catalog (Stable, Documented)

Codes are public API. They never change once shipped.

| Code | HTTP | Meaning | Remediation hint |
| --- | --- | --- | --- |
| `VALIDATION_ERROR` | 400 | Request failed schema validation | Fix the offending fields |
| `ORDER_NOT_FOUND` | 404 | Order ID does not exist | Verify ID; may be deleted |
| `ORDER_ALREADY_CANCELLED` | 409 | Order is in a terminal state | Cannot cancel again |
| `INSUFFICIENT_STOCK` | 409 | Not enough inventory | Retry later or pick alternate |
| `CONCURRENT_MODIFICATION` | 409 | Optimistic lock failed | Re-fetch and retry |
| `FORBIDDEN` | 403 | Caller lacks permission | Request access |
| `INTERNAL_ERROR` | 500 | Unhandled fault | Contact support with traceId |

Keep the catalog in `docs/error-catalog.md` (or generate from a single source). Reserve namespaces per bounded context (`ORDER_*`, `PAYMENT_*`).

### 6. Transaction Rollback Alignment

`@Transactional` rolls back on `RuntimeException` and `Error` by default. Domain exceptions extend `RuntimeException`, so they roll back automatically. Verify in tests.

If you have checked exceptions and want rollback:

```java
@Transactional(rollbackFor = MyCheckedException.class)
public void doIt() throws MyCheckedException { ... }
```

If you intentionally do **not** want rollback for a specific exception:

```java
@Transactional(noRollbackFor = ReadOnlyAuditException.class)
```

Anti-pattern: catching the exception inside the transactional method and not rethrowing - the proxy never sees the throw, so the transaction commits.

### 7. Do Not Leak Internals

Never expose:

- Stack traces (`server.error.include-stacktrace=never` in prod).
- SQL fragments / DB error messages (translate `DataIntegrityViolationException`).
- Internal IDs unrelated to the resource.
- Class names from generic 500s.

Settings:

```yaml
server:
  error:
    include-message: never
    include-stacktrace: never
    include-binding-errors: never
    include-exception: false
```

### 8. Tests for Every Error Path

```java
@WebMvcTest(OrderController.class)
class OrderErrorTest {
    @Autowired MockMvc mvc;
    @MockBean OrderService svc;

    @Test
    void notFoundReturnsProblemDetail() throws Exception {
        var id = UUID.randomUUID();
        when(svc.findById(id)).thenThrow(new OrderNotFoundException(id));

        mvc.perform(get("/api/v1/orders/{id}", id))
            .andExpect(status().isNotFound())
            .andExpect(content().contentType(MediaType.APPLICATION_PROBLEM_JSON))
            .andExpect(jsonPath("$.code").value("ORDER_NOT_FOUND"))
            .andExpect(jsonPath("$.orderId").value(id.toString()))
            .andExpect(jsonPath("$.traceId").exists());
    }
}
```

Minimum suite: validation 400, auth 401/403, each domain code, optimistic lock 409, generic 500 fallback.

## Common Pitfalls

| Anti-pattern | Fix |
| --- | --- |
| `try { ... } catch (Exception e) { return ResponseEntity.status(500).body(...); }` in controller | Throw; let `@RestControllerAdvice` handle |
| Multiple `@RestControllerAdvice` with overlapping handlers | One advice; or scope each with `@Order` and `basePackages` |
| Returning `Map<String, String>` ad-hoc errors | `ProblemDetail` (RFC 9457) |
| Including `getMessage()` of unknown exceptions in 500 response | Generic message + traceId only |
| Logging validation 400s at `error` | Drop to `debug`/`warn`; alarms ignore |
| Throwing `RuntimeException("not found")` | Domain exception with code |
| Catching exception inside `@Transactional` and not rethrowing | Rethrow or translate; otherwise rollback won't fire |
| Exposing Hibernate exception messages | Translate `DataIntegrity*` to a clean code |

## Output Format

When applying this skill, deliver:

1. Exception taxonomy table (group -> example -> HTTP).
2. Domain exception class hierarchy.
3. Single `@RestControllerAdvice` implementation.
4. Error code catalog (markdown table) added to docs.
5. Logging-severity matrix.
6. Tests covering every documented code.
7. `application.yml` `server.error.*` lockdown.

## Authoritative References

- Spring MVC exception handling + ProblemDetail: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html
- Spring Boot error handling: https://docs.spring.io/spring-boot/reference/web/servlet.html#web.servlet.spring-mvc.error-handling
- RFC 9457 - Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc9457.html
- Spring Framework transaction rollback rules: https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/rolling-back.html
- Jakarta Bean Validation: https://jakarta.ee/specifications/bean-validation/3.0/
- OWASP - Improper Error Handling: https://owasp.org/www-community/Improper_Error_Handling
