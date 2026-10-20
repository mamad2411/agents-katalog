# Outbound-Integration Rules — Java Examples

**Framework basis:** Java 17+, Spring Boot 3.x, Spring's `RestClient`/`WebClient`,
Resilience4j for retry/circuit-breaking. The rules themselves are
framework-agnostic — these examples only show one concrete stack.
**Translation hints:** OkHttp/Apache HttpClient → set `connectTimeout`/`callTimeout`
on the builder; Feign → `Request.Options` + a Resilience4j decorator. **Version-
sensitive:** `RestClient` is Boot 3.2+; earlier code uses `RestTemplate` with a
`ClientHttpRequestFactory` timeout, or `WebClient` with an `HttpClient` timeout.

## Rule 1 — Every outbound call is time-bounded
Violation:
```java
RestClient client = RestClient.create();           // no timeouts → can hang forever
```
Correct:
```java
var factory = new SimpleClientHttpRequestFactory();
factory.setConnectTimeout(2_000);
factory.setReadTimeout(5_000);
RestClient client = RestClient.builder().requestFactory(factory).build();
```

## Rule 2 — Retry only what is safe, with capped jittered backoff
Violation:
```java
for (int i = 0; i < 10; i++) {                     // fixed delay, unbounded intent
    try { return client.get()...; } catch (Exception e) { Thread.sleep(1000); }
}
```
Correct:
```java
RetryConfig cfg = RetryConfig.custom()
    .maxAttempts(3)
    .intervalFunction(IntervalFunction.ofExponentialRandomBackoff(200, 2.0))
    .retryOnException(this::isTransient)           // 5xx/429/IO only, GET is idempotent
    .build();
```

## Rule 3 — Break the circuit on a failing dependency
Violation:
```java
// every call hits a dead dependency, waits for the full timeout, piles up threads
RateDto d = client.get().uri("/rate").retrieve().body(RateDto.class);
```
Correct:
```java
CircuitBreaker cb = registry.circuitBreaker("rates");
RateDto d = cb.executeSupplier(() ->
    client.get().uri("/rate").retrieve().body(RateDto.class));  // fails fast when open
```

## Rule 4 — Check the status before trusting the body
Violation:
```java
RateDto d = client.get().uri("/rate").retrieve().body(RateDto.class);  // 500 body parsed as success
```
Correct:
```java
RateDto d = client.get().uri("/rate")
    .retrieve()
    .onStatus(HttpStatusCode::isError,
        (req, res) -> { throw new RatesUnavailableException(res.getStatusCode()); })
    .body(RateDto.class);
```

## Rule 5 — Validate and map the response at the boundary
Violation:
```java
JsonNode json = client.get()...body(JsonNode.class);
domain.setRate(json.get("rate").decimalValue());   // raw external schema leaks inward
```
Correct:
```java
public record RateDto(BigDecimal rate, String currency) {}
RateDto dto = client.get()...body(RateDto.class);
if (dto.rate() == null) throw new RatesUnavailableException("missing rate");
```

## Rule 6 — Convert remote failures into typed local errors
Violation:
```java
public RateDto fetch() { return client.get()...body(RateDto.class); }  // raw ResourceAccessException escapes
```
Correct:
```java
public RateDto fetch() {
    try { return client.get()...body(RateDto.class); }
    catch (ResourceAccessException e) { throw new RatesUnavailableException(e); }  // typed
}
```

## Rule 7 — Make writes idempotent where the protocol allows
Violation:
```java
// retried POST with no idempotency key → double charge
client.post().uri("/charges").body(charge).retrieve();
```
Correct:
```java
client.post().uri("/charges")
    .header("Idempotency-Key", chargeId.toString())   // retry-safe
    .body(charge).retrieve();
```

## Rule 8 — Isolate the client behind an interface
Violation:
```java
@Service
class InvoiceService {
    void bill() { RestClient.create().post()...; }   // HTTP call inside business logic
}
```
Correct:
```java
interface RatesPort { RateDto fetchRate(); }         // seam; fakeable in tests
@Service class InvoiceService {
    private final RatesPort rates;                    // injected
}
```

## Rule 9 — Propagate context outward; never leak secrets
Violation:
```java
log.info("calling rates with key {} full response {}", apiKey, body);  // secret + full body
```
Correct:
```java
client.get().uri("/rate")
    .header("X-Correlation-Id", MDC.get("correlationId"))   // propagate trace
    .header("Authorization", "Bearer " + token)             // not logged
    .retrieve();
```

## Rule 10 — Bound concurrency and payload size
Violation:
```java
RateDto d = RestClient.create().get()...;   // new client + connection per call
```
Correct:
```java
// one shared, pooled client bean, connection pool capped
@Bean RestClient ratesClient(RestClient.Builder b) { return b.requestFactory(pooled()).build(); }
```
