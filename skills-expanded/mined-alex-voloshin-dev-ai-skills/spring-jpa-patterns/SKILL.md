---
name: spring-jpa-patterns
description: Use this skill when the agent is implementing Java backend services in Spring Boot projects, reviewing JPA entity models, configuring connection pools or caches, designing REST endpoints, writing repository/service/controller layers, or onboarding to Spring conventions — for Spring Boot 3 + JPA backend patterns covering Java 21+ features, layered architecture, Spring Data JPA, Hibernate fetch strategies, Flyway migrations, HikariCP pool tuning, Redis caching with Spring Cache, Spring Security 6 filter chains, REST API design (RFC 7807, pagination, versioning), Testcontainers + JUnit 5 + Mockito testing, Micrometer + Actuator observability, and virtual threads and performance tuning.
disable-model-invocation: true
---

# Spring Boot + JPA Patterns

Backend knowledge base for Java 21+ services built on Spring Boot 3 with PostgreSQL and Redis. Covers layered architecture, persistence with Spring Data JPA + Hibernate, Flyway-managed schema, HikariCP tuning, Spring Security 6, REST design, the JUnit 5 + Mockito + Testcontainers test stack, and Micrometer-based observability. Designed to be auto-loaded by `java-engineer` and referenced by reviewers and architects working on Java services.

## Project Architecture (Spring Boot 3)

Use layered or hexagonal architecture consistently across the project:

- **Controller** (`@RestController`): HTTP mapping, request validation, response DTOs
- **Service** (`@Service`, `@Transactional`): business logic, orchestration, transaction boundaries
- **Repository** (`@Repository`, extends `JpaRepository`): data access, custom queries
- **Entity** (`@Entity`): JPA-managed domain objects, lifecycle callbacks
- **DTO / Record**: data transfer between layers — never expose entities in API responses
- **Mapper**: convert between entities and DTOs (MapStruct or manual)
- **Config** (`@Configuration`): bean definitions, property binding, infrastructure setup
- **Exception** (`@ControllerAdvice`): global error handling with `@ExceptionHandler`

Dependency injection rules:

- Constructor injection only. `final` fields with `@RequiredArgsConstructor` or explicit constructor.
- No field injection (`@Autowired` on fields).
- Java 21+ features: records, sealed classes, pattern matching, text blocks, virtual threads. No raw types or unchecked casts.

Configuration:

- Use `application.yml` over `.properties` — structured, profile-aware.
- Profile-based config: `application-dev.yml`, `application-prod.yml`, `application-test.yml`.
- Externalize environment values: `${DB_URL}`, `${REDIS_HOST}`, `${JWT_SECRET}`.
- `@ConfigurationProperties` + `@Validated` for type-safe binding.
- Virtual threads: `spring.threads.virtual.enabled=true` for I/O-bound workloads (Java 21+).

## Spring Data JPA + Hibernate

Entity design:

- `@Entity` with explicit `@Table(name = "...")` — never rely on naming strategy alone.
- Primary keys: `@GeneratedValue(strategy = IDENTITY)` for serial, `@UuidGenerator` for UUID.
- Auditing: `@CreatedDate`, `@LastModifiedDate` via `@EntityListeners(AuditingEntityListener.class)`.
- `@Column(nullable = false)` matches DB constraints.
- `equals()` / `hashCode()` based on business key or ID — never on all fields.
- `@Enumerated(EnumType.STRING)` — never `EnumType.ORDINAL`.

Query and fetch patterns:

- **N+1 prevention**: `@EntityGraph` or `JOIN FETCH` in JPQL for association loading.
- **Lazy by default**: all `@ManyToOne` and `@OneToMany` use `FetchType.LAZY`.
- **Projections**: interface/DTO projections for read-only queries — avoid loading full entities.
- **Batch ops**: `hibernate.jdbc.batch_size=25` for bulk inserts/updates.
- **Read-only transactions**: `@Transactional(readOnly = true)` enables Hibernate optimizations.
- **Indexes**: create for columns in WHERE, JOIN, ORDER BY via Flyway migration.
- Avoid native SQL except for performance-critical paths, with a comment explaining why.

## Flyway Migrations

- Location: `src/main/resources/db/migration/`.
- Versioned: `V{version}__{description}.sql` (e.g., `V1__create_users_table.sql`).
- Repeatable: `R__{description}.sql` for views, functions, seed data.
- Each migration is idempotent where possible (`CREATE INDEX IF NOT EXISTS`, `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`).
- Never modify or delete existing migrations.
- Never use `ddl-auto=update` in production — Flyway owns schema.
- CI test plan: run migrations against an empty DB and from the previous version.

## HikariCP Connection Pool

- Configure `maximum-pool-size`, `connection-timeout`, `max-lifetime`.
- Initial pool sizing heuristic: `(2 * CPU cores) + number_of_disks` — tune via load testing.
- Set `max-lifetime` below PostgreSQL's `idle_in_transaction_session_timeout`.
- Monitor via Micrometer: `hikaricp.connections.active`, `hikaricp.connections.pending`.
- Detect connection leaks via `leakDetectionThreshold` in non-prod profiles.

## Redis Caching

Declarative caching:

- `@EnableCaching` + `@Cacheable`, `@CachePut`, `@CacheEvict`.
- Spring Data Redis with Lettuce client (default in Spring Boot 3).
- Cache key design: `{entity}:{id}` or `{entity}:list:{hash_of_params}` — predictable, eviction-friendly.
- TTL: configured per cache in `RedisCacheConfiguration`.
- Eviction: `@CacheEvict` on mutations; `allEntries = true` for list caches.
- Serialization: `GenericJackson2JsonRedisSerializer` — human-readable, debuggable.

Patterns:

- **Cache-aside**: default `@Cacheable` flow — check cache, miss → load from DB → store.
- **Distributed locks**: `RedisTemplate` + Lua scripts, or Redisson.
- **Rate limiting**: Redis sliding-window counters.
- **Session storage**: Spring Session with Redis for stateless horizontal scaling.
- Never cache mutable state without an explicit invalidation strategy.
- Monitor hit/miss ratio, eviction rate, memory usage (Redis INFO + Micrometer).

## Spring Security

- Bean-based config via `SecurityFilterChain` — never extend `WebSecurityConfigurerAdapter` (removed in Spring Security 6).
- JWT auth: stateless sessions, token validation in `OncePerRequestFilter`.
- OAuth2 resource server: `spring-boot-starter-oauth2-resource-server` for JWT/opaque tokens.
- Method-level: `@PreAuthorize("hasRole('ADMIN')")`, `@Secured` for role-based access.
- CORS: configure explicitly in `SecurityFilterChain` — never `@CrossOrigin("*")`.
- CSRF: disable only for stateless REST (`csrf(csrf -> csrf.disable())`); keep enabled for session apps.
- Passwords: `BCryptPasswordEncoder`. Never store plaintext.
- Validate all inputs; rely on JPA's parameterized queries (no string concat into JPQL).

## REST API Design

- Resource-oriented URLs: `/api/v1/users`, `/api/v1/users/{id}/orders`.
- HTTP verbs: GET (read), POST (create), PUT (full update), PATCH (partial), DELETE (remove).
- Status codes: 200, 201, 204, 400, 401, 403, 404, 409, 422, 500 — precise, never generic 200 for errors.
- Pagination: `Pageable` parameter → `Page<T>` with `page`, `size`, `sort`.
- Versioning: URL-based (`/api/v1/...`).
- Validation: `@Valid` + Jakarta Bean Validation (`@NotNull`, `@Size`, `@Email`, `@Pattern`).
- Error responses: RFC 7807 problem-details shape — `{ timestamp, status, error, message, path, details[] }`.
- Custom exception hierarchy: `BusinessException` (4xx) → specific subclasses; `SystemException` (5xx).
- Global `@ControllerAdvice` with `@ExceptionHandler` per exception family.
- Never expose stack traces or internal details in API responses.
- Log exceptions with correlation IDs.
- OpenAPI: springdoc-openapi for generated docs; keep schemas in sync with DTOs.

## Testing

### JUnit 5

- Structure: Given → When → Then.
- AssertJ assertions; `@DisplayName` for readability.
- Skip tests for framework behavior, getters/setters, generated code.

### Mockito

- `@Mock` + `@InjectMocks`, `@ExtendWith(MockitoExtension.class)` for unit tests.
- Mock at architectural seams (services depend on repositories; controllers depend on services).
- Verify behavior with `verify(...)` only when interaction matters; otherwise assert state.

### Spring test slices

- `@WebMvcTest` + `MockMvc` for controllers.
- `@DataJpaTest` for repositories (paired with Testcontainers PostgreSQL).
- `@DataRedisTest` for Redis-only slices.
- `@SpringBootTest` + `MockMvc` for end-to-end request-response cycles.

### Testcontainers

- `@Testcontainers` + `@Container` for PostgreSQL and Redis to match production runtimes.
- Reuse containers across tests with `withReuse(true)` and `~/.testcontainers.properties` for local speed.
- Lifecycle: containers start before Spring context; use `@DynamicPropertySource` to inject JDBC URL and Redis host.

## Observability

- **Logging**: SLF4J + Logback. Structured JSON in production. MDC for correlation IDs.
- **Metrics**: Micrometer + Prometheus via `/actuator/prometheus`. Track latency, error rate, DB pool, cache hit ratio.
- **Health**: `/actuator/health` with custom indicators for PostgreSQL, Redis, external services.
- **Tracing**: Micrometer Tracing (Brave or OpenTelemetry bridge). Propagate trace/span IDs across services.
- **Actuator**: expose only necessary endpoints. Secure with a separate security config.

## Performance

- **Virtual threads** (Java 21+): enable for I/O-bound ops. Prefer `ReentrantLock` over `synchronized` to avoid pinning carriers.
- **Connection pool**: monitor HikariCP metrics and adjust pool size per throughput/latency.
- **Query optimization**: `EXPLAIN ANALYZE` on slow queries. Add indexes. Paginate large results.
- **Caching**: cache frequently read, rarely changed data. Measure before caching.
- **Async**: `@Async` + custom `TaskExecutor`. `CompletableFuture` for parallel calls.
- **GraalVM native**: consider for microservices needing fast startup.

## When this applies

| Workflow | Apply this knowledge |
|---|---|
| `Agent(java-engineer)` invocation | Auto-loaded |
| `/develop` with a Java work package | Spawned developer agent loads this |
| `/code-review` on Java PRs | Reviewer references these patterns |
| `/architecture-design` for a Java service | Architect references API + persistence patterns |
| `/bugfix` on a Spring/JPA defect | Developer + QA reference fetch + transaction patterns |

## Integration

- **Consumed by**: `java-engineer` (primary), `software-engineer` (when reviewing Java code), `db-engineer` (JPA model and migration review), `solution-architect` (REST + service-layer design).
- **Companion knowledge**: `owasp-coverage` skill for Spring Security threat coverage; `test-strategy` skill for layered test pyramid; `observability-methods` skill for Micrometer/OTel cross-stack patterns.
- **External references**: Spring Boot 3 reference docs, Spring Data JPA docs, Hibernate ORM docs, JUnit 5 user guide, Testcontainers docs, HikariCP wiki, Flyway docs.
