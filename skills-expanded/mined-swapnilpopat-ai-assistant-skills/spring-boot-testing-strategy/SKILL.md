---
name: spring-boot-testing-strategy
description: Build a balanced Spring Boot test strategy using slice tests, integration tests, and containerized dependencies. Use when defining or improving quality gates for Spring Boot services.
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Spring Boot Testing Strategy

Build a balanced, fast, deterministic test suite for Spring Boot 3.x using JUnit 5, MockMvc, slice tests, Testcontainers, and contract tests. Optimize for confidence per second of CI time.

## Context

You are designing or refactoring tests for a Spring Boot service. Output must catch real regressions, run fast on every PR, stay deterministic (no flakes), and be cheap enough that engineers run them locally.

## When to Use This Skill

- New project test setup.
- Existing service with slow / flaky tests.
- Low confidence in refactors due to weak coverage.
- Defining CI quality gates for release.

## Prerequisites

- JUnit 5 (`spring-boot-starter-test` brings JUnit Jupiter, Mockito, AssertJ, JsonPath).
- Mockito 5 / AssertJ.
- Testcontainers (`testcontainers-junit-jupiter` + DB module).
- CI runner with Docker (or Testcontainers Cloud) for integration tests.

## Instructions

### 1. Test Pyramid by Intent

| Tier | Tooling | Speed | Use for |
| --- | --- | --- | --- |
| Unit | JUnit 5 + Mockito + AssertJ, no Spring context | <50ms each | Pure business logic, value objects, mappers, domain rules |
| Slice | `@WebMvcTest`, `@DataJpaTest`, `@JsonTest`, `@RestClientTest` | 1-3s | Controller wiring, validation, repository queries, JSON shape |
| Integration | `@SpringBootTest` + Testcontainers | 5-30s | Cross-layer flows, real DB, real broker, real auth |
| Contract | Spring Cloud Contract / Pact | 1-5s | Producer/consumer compatibility |
| E2E (optional) | Postman/RestAssured against deployed env | minutes | Smoke after deploy |

Most tests should be unit + slice. Reserve `@SpringBootTest` for cross-cutting flows that genuinely need full wiring.

### 2. Unit Test (No Spring)

```java
class PricingDomainServiceTest {
    private final PricingDomainService pricing = new PricingDomainService();

    @Test
    void appliesDiscountWhenLoyaltyTierIsGold() {
        var total = pricing.compute(money("100.00"), Customer.gold());
        assertThat(total).isEqualByComparingTo("90.00");
    }
}
```

If a test needs a Spring context, ask whether the unit test is testing logic or framework wiring. Pure logic should not need Spring.

### 3. Controller Slice (`@WebMvcTest`)

```java
@WebMvcTest(OrderController.class)
@Import({SecurityConfig.class, GlobalErrorHandler.class})
class OrderControllerTest {
    @Autowired MockMvc mvc;
    @MockBean OrderService service;

    @Test
    @WithMockUser(roles = "order.write")
    void createsOrder() throws Exception {
        var resp = new OrderResponse(UUID.randomUUID(), UUID.randomUUID(),
            OrderStatus.PLACED, new BigDecimal("19.99"), OffsetDateTime.now());
        when(service.place(any())).thenReturn(resp);

        mvc.perform(post("/api/v1/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                  {"customerId":"%s","lines":[{"productId":"%s","quantity":1}]}
                  """.formatted(UUID.randomUUID(), UUID.randomUUID())))
            .andExpect(status().isCreated())
            .andExpect(header().exists("Location"))
            .andExpect(jsonPath("$.status").value("PLACED"));
    }
}
```

Don't use `@SpringBootTest` to test a controller. The slice is faster and more focused.

### 4. Repository Slice (`@DataJpaTest` + Testcontainers)

Avoid H2 - it hides Postgres-specific behavior (UUID, JSONB, locking, ON CONFLICT, fractional seconds).

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class OrderRepositoryIT {
    @Container
    static final PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16-alpine");

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry r) {
        r.add("spring.datasource.url",      pg::getJdbcUrl);
        r.add("spring.datasource.username", pg::getUsername);
        r.add("spring.datasource.password", pg::getPassword);
    }

    @Autowired OrderRepository repo;

    @Test
    void findByIdWithLinesUsesSingleQuery() { ... }
}
```

Use `@ServiceConnection` (Spring Boot 3.1+) to reduce boilerplate:

```java
@Container @ServiceConnection
static final PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16-alpine");
```

Reuse containers across tests with the singleton pattern or `withReuse(true)` + `~/.testcontainers.properties` `testcontainers.reuse.enable=true`.

### 5. HTTP Client Slice (`@RestClientTest`)

```java
@RestClientTest(PaymentClient.class)
class PaymentClientTest {
    @Autowired PaymentClient client;
    @Autowired MockRestServiceServer server;

    @Test
    void deserializesAuthorizationResponse() {
        server.expect(requestTo("/v1/authorize"))
              .andRespond(withSuccess("""
                {"id":"a-1","status":"AUTHORIZED"}""", MediaType.APPLICATION_JSON));

        var auth = client.authorize(new AuthRequest("o-1", BigDecimal.TEN));

        assertThat(auth.status()).isEqualTo("AUTHORIZED");
    }
}
```

### 6. Full Integration (`@SpringBootTest`)

Use sparingly for the small set of cross-cutting flows (place-order end-to-end with DB + outbound payment + outbox).

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@Testcontainers
@AutoConfigureMockMvc
class PlaceOrderFlowIT {
    @Container @ServiceConnection
    static final PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16-alpine");
    @Container @ServiceConnection
    static final KafkaContainer kafka = new KafkaContainer("apache/kafka:3.8.0");

    @Autowired MockMvc mvc;
    @Autowired OrderRepository repo;

    @Test
    void placedOrderIsPersistedAndEmitted() { ... }
}
```

### 7. Test Data: Builders, Faker, Fixtures

Hand-rolled data factories beat Spring `@Sql` files for readability.

```java
public final class Orders {
    public static Order.Builder anOrder() {
        return Order.builder()
            .id(UUID.randomUUID())
            .customerId(UUID.randomUUID())
            .status(OrderStatus.PLACED)
            .total(new BigDecimal("9.99"));
    }
}
// usage:  var o = anOrder().status(OrderStatus.CANCELLED).build();
```

Control time and randomness:

```java
@TestConfiguration
class TimeConfig {
    @Bean Clock testClock() {
        return Clock.fixed(Instant.parse("2026-01-15T10:00:00Z"), ZoneOffset.UTC);
    }
}
```

Inject `Clock` everywhere instead of `Instant.now()`.

### 8. Determinism Rules

- No `Thread.sleep`. Use Awaitility for async waits with explicit timeout + polling.
- No relying on iteration order (`HashMap` -> `LinkedHashMap`/sorted assertions).
- No tests dependent on each other (`@TestMethodOrder` smell unless intentional).
- Reset external state between tests: `@DirtiesContext` only when truly needed (it kills speed). Prefer per-test data isolation by random IDs.
- Quarantine flaky tests in a `@Tag("flaky")` group, fix within an SLA, don't disable silently.

### 9. Performance and Footprint

- Spring `@SpringBootTest` context is cached across tests with the same configuration. Don't randomize properties in `@DynamicPropertySource` that don't need to be (it busts the cache).
- Parallelize unit/slice tests:

```properties
# junit-platform.properties
junit.jupiter.execution.parallel.enabled = true
junit.jupiter.execution.parallel.mode.default = same_thread
junit.jupiter.execution.parallel.mode.classes.default = concurrent
```

- Run `@SpringBootTest` serially (broker/DB containers).
- Track context cache hit rate. Aim to keep total distinct contexts <= 5 per module.

### 10. Contract Testing for Service Boundaries

For provider/consumer relationships, use Spring Cloud Contract or Pact. Provider verifies a contract checked in by the consumer; CI fails if the provider breaks an existing consumer.

### 11. Coverage as a Signal

Track line + branch coverage with JaCoCo. Treat thresholds as smoke alarms, not goals. The right test asks "does this catch a regression a user would care about?", not "did I touch every line?".

### 12. CI Quality Gates

Per PR (must pass):

- Compile + SpotBugs/ErrorProne/Checkstyle.
- Unit + slice suite.
- ArchUnit rules.
- Dependency vulnerability scan.

Pre-merge / nightly:

- Full integration suite (Testcontainers).
- Mutation testing on critical packages (PIT) for high-risk modules.
- Contract verification.

## Common Pitfalls

| Anti-pattern | Fix |
| --- | --- |
| `@SpringBootTest` for everything | Slice tests + targeted integration |
| H2 in tests, Postgres in prod | Testcontainers Postgres |
| `Thread.sleep(2000)` to "wait for async" | Awaitility with deadline + condition |
| Reusing the same DB rows across tests | Random IDs per test, isolation by data not order |
| Asserting on `toString()` of a DTO | Field-by-field with AssertJ; resilient to changes |
| `@DirtiesContext` everywhere | Fix the root cause (mutating bean state in tests) |
| Mocking value objects | Don't mock what you own and is data |
| Mocking the JPA repository in service tests AND not having an integration test | Add at least one Testcontainers test that exercises the real query |
| Coverage threshold = 100% as the goal | Test risk, not lines |

## Output Format

When applying this skill, deliver:

1. Pyramid allocation table for the project (rough %).
2. Per-module test type recommendations.
3. Critical integration scenarios list.
4. Test data + Clock injection plan.
5. CI gate definition (per-PR vs pre-merge).
6. Flake budget + remediation owner.
7. Initial baseline tests added (one per layer).

## Authoritative References

- Spring Boot testing: https://docs.spring.io/spring-boot/reference/testing/index.html
- Spring Framework testing: https://docs.spring.io/spring-framework/reference/testing.html
- JUnit 5 user guide: https://junit.org/junit5/docs/current/user-guide/
- AssertJ: https://assertj.github.io/doc/
- Mockito: https://site.mockito.org/
- Testcontainers Java: https://java.testcontainers.org/
- Spring Boot Testcontainers support: https://docs.spring.io/spring-boot/reference/testing/testcontainers.html
- Awaitility: https://github.com/awaitility/awaitility
- Spring Cloud Contract: https://docs.spring.io/spring-cloud-contract/reference/
- Pact JVM: https://docs.pact.io/implementation_guides/jvm
- PIT mutation testing: https://pitest.org/
- ArchUnit: https://www.archunit.org/
