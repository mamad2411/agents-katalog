# Exception Warden — Java Examples

**Framework basis:** All examples use **Spring Boot 3.x** (Spring Framework 6,
Spring Web MVC) on **Java 17+**, with **SLF4J 2.x / Logback MDC** for
request-ID logging (Rule 7), **Jakarta Bean Validation 3.x** (Hibernate
Validator 8) for field validation (Rule 10), and **Spring `@Transactional`**
for rollback (Rule 9). Version-sensitive details:
- Spring Boot 3 uses `jakarta.*` imports (`jakarta.servlet.http.HttpServletRequest`,
  `jakarta.validation.Valid`) — on Boot 2.x, substitute `javax.*`.
- `Map.of(...)` in Rule 6 requires Java 9+; the code shown assumes 17+.
- Spring Boot 3 supports RFC 9457 Problem Details natively
  (`spring.mvc.problemdetails.enabled=true`) — relevant when Rule 4 detects
  an existing Problem Details schema.

The rules themselves are framework-agnostic — when the repo uses Quarkus,
Micronaut, or plain JAX-RS, translate the idiom (e.g., Spring's
`@RestControllerAdvice` ↔ JAX-RS's `ExceptionMapper`); the rule still applies
unchanged.

## Rule 1 — Boundary handling only

```java
// VIOLATION — controller builds its own error response
@GetMapping("/orders/{id}")
public ResponseEntity<?> getOrder(@PathVariable String id) {
    try {
        return ResponseEntity.ok(repo.find(id));
    } catch (NotFoundException e) {
        return ResponseEntity.status(404).body(Map.of("error", "not found"));
    }
}

// CORRECT — throw typed exception; ONE @RestControllerAdvice formats all responses
@GetMapping("/orders/{id}")
public Order getOrder(@PathVariable String id) {
    return repo.find(id); // throws OrderNotFoundException
}

@RestControllerAdvice
class GlobalErrorHandler {
    @ExceptionHandler(AppException.class)
    ResponseEntity<ErrorBody> handle(AppException e, HttpServletRequest req) {
        return errorResponse(e, RequestId.from(req));
    }
}
```

## Rule 2 — Zero internal leakage

```json
// VIOLATION — leaks ORM, SQL, and internal host
{ "error": "org.hibernate.exception.JDBCConnectionException: could not connect to db-primary.internal:5432" }

// CORRECT — generic body; full detail in server logs under the same request_id
{ "code": "INTERNAL_ERROR", "message": "An unexpected error occurred.",
  "details": [], "request_id": "req_8f3a1c" }
```

## Rule 3 — Expected vs unexpected

```java
// Expected: typed exception → 409, message safe to show the client
throw new DuplicateEmailException("An account with this email already exists.");

// Unexpected: a NullPointerException bubbling up → global handler logs the
// stack trace, fires an alert, client sees only the generic INTERNAL_ERROR body.
```

## Rule 4 — One error schema

```json
{
  "code": "ORDER_NOT_FOUND",
  "message": "No order exists with the given ID.",
  "details": [],
  "request_id": "req_8f3a1c"
}
```

Violation: one endpoint returning `{"error": "..."}` while another returns
`{"code": ..., "message": ...}` — consolidate to one shape.

## Rule 5 — Codes for machines, messages for humans

```java
// VIOLATION — test parses human-readable message; breaks when copy changes
assertTrue(response.getMessage().contains("already exists"));

// CORRECT — assert on the stable code
assertEquals("DUPLICATE_EMAIL", response.getCode());
```

## Rule 6 — Deliberate status mapping

```java
// Explicit, exhaustive, in ONE place (Map.of requires Java 9+; assumes 17+)
Map<Class<? extends AppException>, HttpStatus> STATUS_MAP = Map.of(
    ValidationException.class,          HttpStatus.BAD_REQUEST,           // 400
    UnauthenticatedException.class,     HttpStatus.UNAUTHORIZED,          // 401
    ForbiddenException.class,           HttpStatus.FORBIDDEN,             // 403
    NotFoundException.class,            HttpStatus.NOT_FOUND,             // 404
    ConflictException.class,            HttpStatus.CONFLICT,              // 409
    RateLimitException.class,           HttpStatus.TOO_MANY_REQUESTS,     // 429
    UpstreamUnavailableException.class, HttpStatus.BAD_GATEWAY,           // 502
    UpstreamTimeoutException.class,     HttpStatus.GATEWAY_TIMEOUT        // 504
);  // anything unmapped → 500 + alert
```

Violation: `return ResponseEntity.ok(Map.of("success", false, "error", ...))`
— an error with HTTP 200.

## Rule 7 — Request ID everywhere

```
Client sees:  { "code": "INTERNAL_ERROR", ..., "request_id": "req_8f3a1c" }
Server log:   ERROR req_8f3a1c POST /orders — OrderRepoException: ...
              at com.acme.orders.OrderService.create(OrderService.java:42) ...
```

```java
// Filter (SLF4J MDC): generate/propagate the ID before anything else,
// so the ID appears in every log line for the request
public class RequestIdFilter extends OncePerRequestFilter {
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
            throws ServletException, IOException {
        String id = Optional.ofNullable(req.getHeader("X-Request-Id"))
                            .orElse("req_" + UUID.randomUUID().toString().substring(0, 6));
        MDC.put("requestId", id);
        try { chain.doFilter(req, res); } finally { MDC.remove("requestId"); }
    }
}
```

## Rule 8 — Catch only what you handle

```java
// VIOLATION — swallows everything, discards original cause
try {
    charge(order);
} catch (Exception e) {
    log.error(e.getMessage());
    throw new PaymentException("failed");
}

// CORRECT — typed catch, original passed as cause
try {
    charge(order);
} catch (GatewayTimeoutException e) {
    throw new UpstreamUnavailableException("payment gateway timeout", e);
}
```

Also forbidden: `catch (Throwable)`, empty catch blocks, and
`log.error(e.getMessage())` without the exception object (loses the stack trace —
use `log.error("...", e)`).

## Rule 9 — Fail fast, clean up always

```java
// VIOLATION — exception between writes leaves half-committed state; conn leaks
Connection conn = pool.acquire();
conn.execute(insertOrder);
conn.execute(insertPayment); // throws → order saved, payment not
pool.release(conn);

// CORRECT — validate first; try-with-resources + @Transactional guarantee cleanup
validate(order); // throws ValidationException before any write

// Spring-managed transaction — rolls back on any RuntimeException by default
@Transactional
public void createOrder(Order order) {
    orderRepo.insert(order);
    paymentRepo.insert(order.payment());
}
```

## Rule 10 — Exhaustive validation errors

```json
{
  "code": "VALIDATION_FAILED",
  "message": "Request validation failed.",
  "details": [
    { "field": "email",    "code": "INVALID_FORMAT", "message": "Must be a valid email address." },
    { "field": "quantity", "code": "OUT_OF_RANGE",   "message": "Must be between 1 and 100." }
  ],
  "request_id": "req_8f3a1c"
}
```

```java
// Spring MVC + Jakarta Bean Validation (@Valid on the request body).
// Bean Validation already collects all failures — map them all, don't stop at the first
@ExceptionHandler(MethodArgumentNotValidException.class)
ResponseEntity<ErrorBody> handleValidation(MethodArgumentNotValidException e, HttpServletRequest req) {
    List<FieldErrorDto> details = e.getBindingResult().getFieldErrors().stream()
        .map(f -> new FieldErrorDto(f.getField(), toCode(f), f.getDefaultMessage()))
        .toList();
    return errorResponse("VALIDATION_FAILED", details, RequestId.from(req));
}
```
