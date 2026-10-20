---
name: spring-boot-coding-conventions
description: Apply consistent Spring Boot coding conventions for layering, naming, dependency injection, transactions, Redis usage, and configuration management. Use when writing or reviewing Java service code in Spring Boot projects.
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Spring Boot Coding Conventions

Apply consistent, team-wide Spring Boot 3.x conventions for layering, naming, dependency injection, transactions, configuration, and shared infrastructure (Redis, clients) so the codebase stays readable and reviewable as it grows.

## Context

You are writing or reviewing Java service code in a Spring Boot 3.x project. The output must read predictably to anyone on the team: a reviewer should be able to find a class by name, infer its responsibility from the package, and trust the transaction and DI rules without re-reading config.

## When to Use This Skill

- Creating new modules in a Spring Boot backend.
- Reviewing PRs for consistency.
- Refactoring inconsistent service boundaries (god services, controller-to-repo shortcuts).
- Authoring or updating a team coding standard.

## Prerequisites

- Layered package structure exists (see foundation module).
- Common API response and error contract are defined (see rest-api-patterns + exception-handling).
- Redis / cache strategy and TTL policy decided.
- Build pipeline runs Checkstyle / Spotless / ErrorProne or equivalent.

## Instructions

### 1. Layer Responsibilities (One-Way Dependencies)

| Layer | Allowed depends on | Owns |
| --- | --- | --- |
| `api` (controllers, DTOs) | application, domain (read-only) | HTTP shape, validation triggers, status codes |
| `application` (use cases) | domain, infrastructure ports | Orchestration, transaction boundaries |
| `domain` (entities, services, value objects) | nothing Spring-specific | Business rules, invariants |
| `infrastructure` (JPA, HTTP clients, brokers) | domain ports | Adapters; implements interfaces declared in domain |

Hard rule: `domain.*` must not import `org.springframework.*`, `jakarta.persistence.*`, `jakarta.servlet.*`, or any external SDK. Enforce with **ArchUnit**:

```java
@AnalyzeClasses(packages = "com.acme.orders")
class ArchitectureTest {
    @ArchTest static final ArchRule domainHasNoFramework =
        noClasses().that().resideInAPackage("..domain..")
            .should().dependOnClassesThat().resideInAnyPackage(
                "org.springframework..", "jakarta.persistence..", "jakarta.servlet..");

    @ArchTest static final ArchRule controllersDoNotCallRepositories =
        noClasses().that().resideInAPackage("..api..")
            .should().dependOnClassesThat().resideInAPackage("..infrastructure.persistence..");
}
```

### 2. Naming

Pick stable suffixes. Apply across the whole codebase.

| Type | Suffix | Example |
| --- | --- | --- |
| Controller | `Controller` | `OrderController` |
| Use case service | `Service` or `UseCase` | `PlaceOrderService`, `CancelOrderUseCase` |
| Domain service | `DomainService` (when ambiguous) | `PricingDomainService` |
| Repository (port) | `Repository` | `OrderRepository` |
| Repository impl | `*Adapter` or `*JpaRepository` | `OrderJpaRepository` |
| Request DTO | `*Request` | `CreateOrderRequest` |
| Response DTO | `*Response` | `OrderResponse` |
| Domain exception | `*Exception` | `OrderNotFoundException` |
| Config props | `*Properties` | `PaymentProperties` |
| Mapper | `*Mapper` | `OrderMapper` |

Anti-pattern: mixing `OrderManager`, `OrderHelper`, `OrderHandler`, `OrderUtil` for similar concepts.

### 3. Dependency Injection: Constructor Only

Use constructor injection on `final` fields. Never field injection (`@Autowired` on a field) - it breaks unit testability and hides required deps.

```java
@Service
class PlaceOrderService {
    private final OrderRepository orders;
    private final PaymentClient payments;
    private final ApplicationEventPublisher events;

    PlaceOrderService(OrderRepository orders, PaymentClient payments,
                      ApplicationEventPublisher events) {
        this.orders = orders;
        this.payments = payments;
        this.events = events;
    }
}
```

Single constructor: Spring auto-wires it without `@Autowired` (since Spring 4.3). Use Lombok `@RequiredArgsConstructor` only if the team standardizes on Lombok.

Anti-patterns: `@Autowired` on a field; `@Autowired` setter for a required dep; `@Resource` (name-based) without a clear reason.

### 4. Transactions: Explicit, at the Service Layer

`@Transactional` belongs on application/use-case methods, not controllers and not repositories.

```java
@Service
class PlaceOrderService {
    @Transactional
    public OrderResponse place(CreateOrderRequest req) { ... }

    @Transactional(readOnly = true)
    public OrderResponse get(UUID id) { ... }
}
```

Rules:

- **Always** use `readOnly = true` on read paths - allows Hibernate read-only optimizations and DB read-replica routing.
- Default rollback: any `RuntimeException` rolls back, checked exceptions do not. If you throw checked domain exceptions and want rollback, use `@Transactional(rollbackFor = MyCheckedException.class)`.
- Keep transactions short. Do **not** call remote APIs inside `@Transactional` (holds a DB connection while waiting on network).
- Do not catch and swallow exceptions inside `@Transactional` - the proxy needs the throw to roll back.
- `@Transactional` self-invocation (calling another method on `this`) bypasses the proxy. Split into two beans, or use `TransactionTemplate`.

### 5. Redis / Cache Key Discipline

Centralize key construction. Always set TTL.

```java
public final class CacheKeys {
    private CacheKeys() {}
    public static final String NS = "orders";
    public static String order(UUID id)         { return NS + ":order:" + id; }
    public static String customerOrders(UUID c) { return NS + ":customer:" + c + ":orders"; }
}
```

```yaml
spring:
  cache:
    type: redis
  data:
    redis:
      host: ${REDIS_HOST}
      timeout: 200ms
      lettuce:
        pool:
          max-active: 16
```

Spring Cache TTL config:

```java
@Bean
RedisCacheManager cacheManager(RedisConnectionFactory cf) {
    var defaults = RedisCacheConfiguration.defaultCacheConfig()
        .entryTtl(Duration.ofMinutes(5))
        .disableCachingNullValues()
        .serializeValuesWith(SerializationPair.fromSerializer(new GenericJackson2JsonRedisSerializer()));
    return RedisCacheManager.builder(cf)
        .cacheDefaults(defaults)
        .withCacheConfiguration("order",
            defaults.entryTtl(Duration.ofMinutes(15)))
        .build();
}
```

Anti-patterns: anonymous keys built inline (`"order:" + id`), missing TTL (silent memory leak), caching mutable objects without invalidation strategy.

### 6. Configuration: `@ConfigurationProperties`, Not `@Value` Soup

Group related settings; validate them on bind.

```java
@Validated
@ConfigurationProperties(prefix = "orders.payment")
public record PaymentProperties(
    @NotBlank String baseUrl,
    @NotNull @DurationMin(seconds = 1) Duration timeout,
    @Min(0) @Max(10) int maxRetries) {}
```

Use `@Value` only for one-off scalars. Keep secrets out of source.

### 7. Immutability and Records by Default

- DTOs: `record`.
- Value objects in domain: `record` (or final classes).
- Collections returned from query methods: `List.copyOf(...)` or unmodifiable views.
- Mutable JPA entities are unavoidable, but keep setters package-private and expose intent-named methods (`order.cancel()`, not `order.setStatus(CANCELLED)`).

### 8. Null Handling

- Public APIs: `Optional<T>` for "may be absent" return types; never `Optional` parameters or fields.
- Use **JSpecify** `@Nullable` / `@NonNull` annotations (Spring 6.2 supports JSpecify) and enforce with NullAway/ErrorProne.
- Never return `null` collections - return empty.

### 9. Exceptions

- Throw domain exceptions from service/domain code (`OrderNotFoundException`), not generic `RuntimeException`.
- Don't use exceptions for control flow.
- Catch the narrowest type, log with context, rethrow or translate.

### 10. Logging Inside Services

Use SLF4J parameterized logging (no string concatenation):

```java
private static final Logger log = LoggerFactory.getLogger(PlaceOrderService.class);
log.info("order placed orderId={} customerId={} total={}", id, customerId, total);
```

Never log secrets, tokens, or full PII. See logging-monitoring module.

## Common Pitfalls

| Anti-pattern | Why it hurts | Fix |
| --- | --- | --- |
| `@Autowired` field injection | Hidden deps, no constructor for tests, can't be `final` | Constructor injection |
| `@Transactional` on controller | DB connection held during HTTP serialization | Move to service |
| `@Transactional` on `private` / `this`-invoked method | Proxy bypassed, no transaction | Split bean or use `TransactionTemplate` |
| `@Transactional` wrapping a remote HTTP call | Connection pool exhaustion, long-held locks | Call client outside the transaction |
| Catching `Exception` and logging at error level inside try blocks | Hides root cause, breaks rollback | Catch narrowly; let it propagate or translate |
| `Optional<T>` as a field/parameter | Misuse of API; serialization issues | Use as return type only |
| `@Value("${...}")` everywhere | No validation, no grouping, no IDE help | `@ConfigurationProperties` records |
| Cyclic dep between two beans | Hard to reason about init order | Extract a third bean or invert dep |
| Returning JPA entity from service to controller | Lazy init / leak / coupling | Return DTO record |

## Output Format

When applying this skill, deliver:

1. Layer dependency map + ArchUnit rules.
2. Naming convention table (filled in for the project).
3. DI policy (constructor only) with a diff against current violations.
4. Transaction policy summary + list of `@Transactional` placements reviewed.
5. Cache key + TTL policy.
6. Configuration properties classes inventory.
7. Refactor plan if violations exist (prioritized).

## Authoritative References

- Spring Framework reference - DI: https://docs.spring.io/spring-framework/reference/core/beans.html
- Spring Framework reference - Transactions: https://docs.spring.io/spring-framework/reference/data-access/transaction.html
- Spring Boot configuration properties: https://docs.spring.io/spring-boot/reference/features/external-config.html#features.external-config.typesafe-configuration-properties
- ArchUnit: https://www.archunit.org/
- JSpecify nullness: https://jspecify.dev/
- Spring Cache abstraction: https://docs.spring.io/spring-framework/reference/integration/cache.html
- Effective Java (Bloch) item summary (community): https://github.com/HugoMatilla/Effective-JAVA-Summary
- Google Java Style Guide: https://google.github.io/styleguide/javaguide.html
