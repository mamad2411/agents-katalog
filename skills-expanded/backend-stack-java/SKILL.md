---
name: backend-stack-java
description: "A Java backend with Spring Boot 3 on Java 21: project layout, REST controllers and validation, services and transactions, Spring Data JPA without N+1 and with open-in-view off, Flyway migrations, ProblemDetail errors, Spring Security configuration, configuration properties, Actuator and Micrometer, virtual threads, and tests with JUnit 5, MockMvc and Testcontainers. Read when the project is a Java or Kotlin Spring backend."
---

# Java with Spring Boot

The generated Spring app returns JPA entities from controllers (with lazy
loading errors, password hashes and endless JSON recursion), puts
`@Transactional` on the controller, loads each order's items one query at a
time behind open-in-view, lets Hibernate create the tables, and catches
`Exception` to answer `200` with a message. The backend rules are in the
`backend` skill; these are Spring's own.

## 1. Setup

- Keep the project's versions. A new service: the current Spring Boot from
  start.spring.io, Java 21 or 25 (both LTS) through a build toolchain,
  Gradle with the Kotlin DSL (or Maven), the wrapper committed.
- Boot 3 is on Jakarta EE (`jakarta.*`, never `javax.*`). Boot 4 (Spring
  Framework 7, November 2025) is the newer line: a planned upgrade with its
  migration guide (Jackson 3 among the changes), never a side effect.
- Starters `web`, `validation`, `data-jpa`, `security`,
  `oauth2-resource-server`, `actuator`; Flyway as `flyway-core` plus
  `flyway-database-postgresql` (a module per database since Flyway 10).
  WebFlux only for an all-reactive stack; with virtual threads MVC scales.
- Package by feature (`orders/` with its controller, service, repository,
  entities and DTO records; `common/` for configuration, errors, security),
  classes package-private unless another feature needs them.
- Kotlin: the `kotlin("plugin.spring")` and `kotlin("plugin.jpa")` plugins,
  `jackson-module-kotlin`, `-Xjsr305=strict`; entities as plain classes with
  `var` properties (never `data class`), DTOs as data classes.

## 2. Controllers and validation

```java
@RestController
class OrderController {
    private final OrderService orders;
    OrderController(OrderService orders) { this.orders = orders; }

    @PostMapping("/api/orders")
    ResponseEntity<OrderResponse> place(@Valid @RequestBody PlaceOrderRequest req,
                                        @AuthenticationPrincipal Jwt jwt) {
        OrderResponse created = orders.place(jwt.getSubject(), req);
        return ResponseEntity.created(URI.create("/api/orders/" + created.id())).body(created);
    }
}

record PlaceOrderRequest(@NotEmpty @Size(max = 50) List<@Valid Line> lines,
                         @Size(max = 500) String note) {
    record Line(@NotBlank String productId, @Positive @Max(100) int quantity) {}
}
```

- Constructor injection into `final` fields, never field injection. DTOs are
  records; entities never leave the service (map there, or with MapStruct):
  a serialised entity leaks columns, fires lazy loads and recurses through
  two-way relations.
- `@Valid` on bodies; constraints on `@RequestParam` and `@PathVariable` are
  checked too (Spring 6.1+, `HandlerMethodValidationException`). Boot's
  Jackson ignores unknown fields; refuse them, as `backend-api` asks, with
  `spring.jackson.deserialization.fail-on-unknown-properties=true`.
- Lists take a `Pageable` (`@PageableDefault(size = 25)`,
  `spring.data.web.pageable.max-page-size=100`) and return your own DTO; a
  serialised `Page` is no stable contract (Spring Data 3.3 warns about it).

## 3. Services and transactions

- `@Transactional(readOnly = true)` on the service class, `@Transactional`
  on each writing method; never on controllers.
- It works through a proxy: a call from the same class (`this.place(...)`)
  runs without it. Checked exceptions do not roll back by default: domain
  exceptions are unchecked, or set `rollbackFor`.
- Race-free writes (`backend-data`): `@Version` on entities two people edit
  (a stale write throws `ObjectOptimisticLockingFailureException`), and
  conditional updates for stock:

```java
@Modifying
@Query("update Product p set p.stock = p.stock - :qty where p.id = :id and p.stock >= :qty")
int reserve(@Param("id") long id, @Param("qty") int qty); // 0 rows: not enough stock
```

  A bulk update bypasses the persistence context: a `Product` loaded before
  it in the same transaction is stale afterwards. `@Lock(PESSIMISTIC_WRITE)`
  only when you must read, decide, then write.
- Side effects after commit: `@TransactionalEventListener` (after commit by
  default) queues emails and webhooks (`backend-jobs`); Spring Modulith's
  event publication registry when they must not be lost.

## 4. Spring Data JPA without surprises

- `spring.jpa.open-in-view=false`. On (the default, with a warning at
  start), every lazy access during serialisation is a hidden query; off, it
  fails loudly and loading becomes a decision.
- `spring.jpa.hibernate.ddl-auto=validate`: the schema comes from Flyway.
- `@ManyToOne(fetch = FetchType.LAZY)` and `@OneToOne(fetch = FetchType.LAZY)`
  written out, since both are eager by default. Each use case loads what it
  needs in its query:

```java
@EntityGraph(attributePaths = {"items", "customer"})
Optional<Order> findWithItemsById(long id);
```

- A fetch join on a collection with paging makes Hibernate page in memory
  (warning `HHH90003004`): page the ids, then fetch those rows with their
  collections, or set `hibernate.default_batch_fetch_size` (32 to 100) so
  lazy collections load in batches. Make the warning fatal with
  `spring.jpa.properties.hibernate.query.fail_on_pagination_over_collection_fetch=true`.
- Read-only responses use DTO or interface projections (only the columns,
  no dirty checking); reports, window functions and upserts go through
  `JdbcClient` (Spring 6.1) or jOOQ.
- Entities: no Lombok `@Data` (its `equals`, `hashCode` and `toString` walk
  lazy relations); `equals` on the id with a constant `hashCode`. Ids from a
  sequence (`GenerationType.SEQUENCE`, `allocationSize` equal to the
  sequence's increment), since `IDENTITY` turns off insert batching.
- Money as `BigDecimal` or a `long` in minor units; times as `Instant` on
  `timestamptz`, with `spring.jpa.properties.hibernate.jdbc.time_zone=UTC`.
- HikariCP's `maximum-pool-size` (10 by default) sized against the
  database's limit across all instances; `connection-timeout` about 5 s
  instead of 30 s, so a starved pool fails fast.

## 5. Flyway

- `src/main/resources/db/migration/V7__add_status_to_orders.sql`: plain SQL,
  never edited once it ran anywhere (the checksum check fails the start).
- Migrations run at start, fine for one instance. With several, run them as
  a release step (the Flyway CLI, or the app once with the web server off):
  Flyway's lock makes the other instances wait through a long migration.
- `CREATE INDEX CONCURRENTLY` in a migration of its own (it cannot run in a
  transaction); other large-table changes in `database-postgres`.

## 6. Errors as ProblemDetail

```java
@RestControllerAdvice
class ApiExceptionHandler extends ResponseEntityExceptionHandler {
    @ExceptionHandler(DomainException.class)
    ProblemDetail domain(DomainException e) {
        HttpStatus status = switch (e) {
            case NotFoundException nf -> HttpStatus.NOT_FOUND;
            case ConflictException c -> HttpStatus.CONFLICT;
            default -> HttpStatus.UNPROCESSABLE_ENTITY;
        };
        ProblemDetail p = ProblemDetail.forStatus(status);
        p.setProperty("code", e.code());
        return p;
    }
}
```

- Extending `ResponseEntityExceptionHandler` gives Spring MVC's own errors
  (bad JSON, validation, wrong method) the RFC 9457 shape; override
  `handleMethodArgumentNotValid` to list every field and code
  (`backend-errors`). A stale `@Version` write maps to `409` `stale_version`.
- Domain exceptions are unchecked, carry a stable code, know nothing of
  HTTP. The last-resort handler logs with the request id and answers a
  generic `500`; `server.error.include-stacktrace` and `include-message`
  stay `never` (the defaults).

## 7. Spring Security

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(auth -> auth
            .requestMatchers(HttpMethod.GET, "/api/products/**").permitAll()
            .anyRequest().authenticated())
        .oauth2ResourceServer(oauth -> oauth.jwt(Customizer.withDefaults()))
        .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .csrf(csrf -> csrf.disable()) // bearer tokens only; keep CSRF with cookies
        .build();
}
```

- The chain lives in a `@Configuration` class with `@EnableMethodSecurity`;
  `anyRequest().authenticated()` last closes every new route by default.
- JWTs: `spring.security.oauth2.resourceserver.jwt.issuer-uri` (keys from its
  JWKS) and `.audiences`; scopes become `SCOPE_` authorities. A same-site
  browser app uses session cookies with CSRF on (`backend-auth`).
- `@PreAuthorize("hasAuthority('SCOPE_orders:refund')")` on service methods;
  ownership in the query (`findByIdAndCustomerId`), so another user's id is
  a `404`. Passwords with `createDelegatingPasswordEncoder()` (bcrypt) from
  `PasswordEncoderFactories`, or `Argon2PasswordEncoder`.

## 8. Configuration and outbound calls

- Settings as `@ConfigurationProperties(prefix = "payments")` records with
  `@Validated` and constraints (`@NotNull URI baseUrl`,
  `@NotBlank String apiKey`), registered by `@ConfigurationPropertiesScan`:
  a missing value stops the start and names the property.
- Secrets from the environment (`PAYMENTS_APIKEY` binds to
  `payments.api-key`: dots become underscores, dashes are dropped) or the
  platform's secret store, never a committed `application-prod.yml`.
  Profiles only for what really differs.
- Outbound HTTP through `RestClient` built from the injected
  `RestClient.Builder` (it carries tracing), with both timeouts set: a
  `JdkClientHttpRequestFactory` over an `HttpClient` with
  `connectTimeout(Duration.ofSeconds(3))`, and `setReadTimeout(...)` on it.

## 9. Actuator, logs and metrics

- `management.endpoints.web.exposure.include=health,info,prometheus`, on a
  port that is not public (`management.server.port=8081`);
  `management.endpoint.health.probes.enabled=true` serves
  `/actuator/health/liveness` and `/readiness`, the database included with
  `management.endpoint.health.group.readiness.include=readinessState,db`.
- Logs through SLF4J and Logback, JSON with Boot's structured logging
  (`logging.structured.format.console=ecs`, Boot 3.4+); Micrometer Tracing
  puts `traceId` and `spanId` in the MDC.
- Metrics with `micrometer-registry-prometheus` or `-otlp`; traces with
  `micrometer-tracing-bridge-otel` and an OTLP exporter, sampled by
  `management.tracing.sampling.probability` (0.1 by default).
- `server.shutdown=graceful` (the default since Boot 3.4) and
  `spring.lifecycle.timeout-per-shutdown-phase=20s`.

## 10. Virtual threads

- `spring.threads.virtual.enabled=true` (Boot 3.2+, Java 21+) runs requests,
  `@Async` and scheduled tasks on virtual threads: blocking JDBC and HTTP
  calls no longer need a big pool, but the Hikari pool still caps queries.
- On Java 21, blocking inside `synchronized` pins the carrier thread (fixed
  in Java 24 by JEP 491): `ReentrantLock` around blocking calls in hot code,
  and watch the JFR event `jdk.VirtualThreadPinned`. Never pool virtual
  threads; CPU-bound work gains nothing.

## 11. Tests

- JUnit 5 and AssertJ. `@WebMvcTest(OrderController.class)` with MockMvc
  (or `MockMvcTester`, Spring 6.2+), services replaced with `@MockitoBean`
  (Boot 3.4+; `@MockBean` before).
- `@SpringBootTest` and `@DataJpaTest` (with
  `@AutoConfigureTestDatabase(replace = Replace.NONE)`) against Postgres
  from Testcontainers, wired by `@ServiceConnection`; never H2 in its place:

```java
@TestConfiguration(proxyBeanMethods = false)
class TestcontainersConfig {
    @Bean
    @ServiceConnection
    PostgreSQLContainer<?> postgres() {
        return new PostgreSQLContainer<>("postgres:17-alpine");
    }
}
```

  Testcontainers 2 moves the class to `org.testcontainers.postgresql`
  without the type parameter: follow the build's version.
- `jwt()` from `SecurityMockMvcRequestPostProcessors` for the caller, and a
  test per rule that another user's order is a `404`; an injected `Clock`;
  WireMock or `MockRestServiceServer` for outbound HTTP.

## Check it

`./gradlew build` (or `./mvnw verify`); one class with
`./gradlew test --tests '*OrderControllerTest'`. Run `./gradlew bootRun` and
`curl` the endpoints: a bad body gives a `400` problem listing every field,
another user's id a `404`, and `/actuator/health/readiness` on port 8081
answers. The start log has no open-in-view warning; with
`logging.level.org.hibernate.SQL=debug` in a test, a list runs as many
queries for 50 rows as for 5.

## Avoid

Entities returned from controllers; `javax.*` imports on Boot 3; field
injection; `@Transactional` on controllers or on methods called from the
same class; open-in-view left on; `ddl-auto=update` on a real database;
eager `@ManyToOne` defaults; `join fetch` with paging over a collection;
Lombok `@Data` on entities; `double` for money; H2 in tests of a Postgres
app; `catch (Exception e)` answering `200`; secrets in committed YAML; HTTP
clients without timeouts; virtual threads expected to speed up ten pooled
connections.
