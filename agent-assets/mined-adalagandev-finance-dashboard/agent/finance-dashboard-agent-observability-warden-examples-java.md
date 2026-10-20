# Observability Rules — Java Examples

**Framework basis:** Java 17+, Spring Boot 3.x, SLF4J + Logback with MDC,
Micrometer for metrics. The rules themselves are framework-agnostic — these
examples only show one concrete stack.
**Translation hints:** Log4j2 → `ThreadContext` in place of MDC; OpenTelemetry →
`Span.current().setAttribute(...)`. **Version-sensitive:** Boot 3 ships
Micrometer Observation + Micrometer Tracing; Boot 2 uses Spring Cloud Sleuth for
correlation ids.

## Rule 1 — Log structured, not concatenated
Violation:
```java
log.info("processed order " + id + " for user " + user);   // unqueryable prose
```
Correct:
```java
log.atInfo().addKeyValue("orderId", id).addKeyValue("userId", user)
   .log("order processed");                                 // filterable fields
```

## Rule 2 — One correlation id per request, threaded everywhere
Violation:
```java
log.info("import started");                 // no way to join this to the request
```
Correct:
```java
MDC.put("correlationId", req.getHeader("X-Correlation-Id") != null
    ? req.getHeader("X-Correlation-Id") : UUID.randomUUID().toString());
try { log.info("import started"); } finally { MDC.clear(); }   // set at boundary filter
```

## Rule 3 — Never log sensitive data
Violation:
```java
log.info("auth user={} password={} token={}", email, password, token);
```
Correct:
```java
log.atInfo().addKeyValue("userId", userId).log("authentication succeeded");  // no secrets
```

## Rule 4 — Use the right level, and mean it
Violation:
```java
log.error("user opened dashboard");         // routine event at ERROR → alert noise
log.debug("payment gateway rejected charge");   // real failure hidden at DEBUG
```
Correct:
```java
log.info("dashboard opened");
log.error("payment rejected: {}", reason);  // failure needing attention
```

## Rule 5 — Log an exception once, with cause and context
Violation:
```java
catch (IOException e) { log.error("import failed", e); throw e; }
// ...and again logged at ERROR by every outer layer
```
Correct:
```java
catch (IOException e) {
    log.atError().addKeyValue("file", name).setCause(e).log("import failed");
    throw new ImportFailedException(name, e);   // exception-warden maps the response
}
```

## Rule 6 — Instrument key operations deliberately
Violation:
```java
public ImportResult importCsv(...) { ... }   // no signal that it ran or how it went
```
Correct:
```java
Timer.Sample s = Timer.start(registry);
ImportResult r = doImport(...);
s.stop(registry.timer("import.duration", "outcome", r.outcome()));
registry.counter("import.rows", "outcome", r.outcome()).increment(r.count());
```

## Rule 7 — Metric and label cardinality is bounded
Violation:
```java
registry.counter("http.requests", "path", request.getURI().toString()).increment();  // unbounded ids in path
```
Correct:
```java
registry.counter("http.requests", "route", "/accounts/{id}", "status", "200").increment();  // templated
```

## Rule 8 — Instrumentation is side-effect-free and cheap
Violation:
```java
log.debug("state = " + expensiveToJson(hugeObject));   // serialized even when DEBUG off
```
Correct:
```java
if (log.isDebugEnabled()) log.debug("state = {}", expensiveToJson(hugeObject));
// or: log.atDebug().addArgument(() -> expensiveToJson(hugeObject)).log("state = {}");
```

## Rule 9 — Log at the boundary, not in a loop
Violation:
```java
for (Row r : rows) { save(r); log.info("saved row {}", r.id()); }   // N log lines
```
Correct:
```java
for (Row r : rows) save(r);
log.atInfo().addKeyValue("count", rows.size()).log("batch saved");   // one summary
```

## Rule 10 — No System.out for application logging
Violation:
```java
System.out.println("import done " + count);   // bypasses structure/level/routing
```
Correct:
```java
private static final Logger log = LoggerFactory.getLogger(ImportService.class);
log.atInfo().addKeyValue("count", count).log("import done");
```
