---
name: spring-boot-data-jpa
description: Implement persistence with Spring Data JPA in Spring Boot using entity modeling, transactions, and migration-safe patterns. Use when building relational data layers for Spring Boot services.
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Spring Boot Data JPA

Design and implement maintainable, performant relational persistence in Spring Boot 3.x using Spring Data JPA + Hibernate 6.x: aggregate-driven entities, intent-named repositories, explicit fetch strategy, Flyway migrations, and Testcontainers verification.

## Context

You are building or reviewing a Spring Boot persistence layer. Output must avoid the well-known JPA traps (N+1, eager fetch, `OFFSET` pagination, schema drift), keep transactions short, and be verified against a real database engine.

## When to Use This Skill

- Adding RDBMS persistence to a new service.
- Migrating raw JDBC / MyBatis to Spring Data JPA, or Boot 2.x (Hibernate 5) to Boot 3.x (Hibernate 6).
- Investigating slow queries, deadlocks, or connection pool exhaustion.
- Preparing a service for multi-environment promotion (zero-downtime schema changes).

## Prerequisites

- `spring-boot-starter-data-jpa` + JDBC driver (`org.postgresql:postgresql`, `com.mysql:mysql-connector-j`, etc.).
- `flyway-core` (or Liquibase) for migrations.
- `testcontainers-junit-jupiter` + DB module for integration tests.
- Decision on database engine and version (e.g., PostgreSQL 16+).

## Instructions

### 1. Model Entities Around Aggregates

Design entities by business consistency boundary, not table-by-table. One aggregate root + child entities loaded together; cross-aggregate references by ID, not by association.

```java
@Entity
@Table(name = "orders", indexes = {
    @Index(name = "ix_orders_customer_created", columnList = "customer_id, created_at DESC"),
    @Index(name = "ix_orders_status",          columnList = "status")
})
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)   // Hibernate 6 native UUID gen
    private UUID id;

    @Column(name = "customer_id", nullable = false, updatable = false)
    private UUID customerId;                          // reference, not @ManyToOne

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private OrderStatus status;

    @Column(name = "total_amount", nullable = false, precision = 19, scale = 2)
    private BigDecimal totalAmount;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private final List<OrderLine> lines = new ArrayList<>();

    @Version
    private long version;                             // optimistic locking

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private OffsetDateTime createdAt;

    protected Order() {}                              // JPA
    // factory + intent-named methods (cancel, addLine, recalcTotal) ...
}
```

Rules:

- Always declare a JPA-required no-arg constructor (`protected`).
- Use `EnumType.STRING` (not `ORDINAL`) - ordinals break on enum reorder.
- Use `BigDecimal` with explicit `precision`/`scale` for money. Never `double`.
- Use `OffsetDateTime` / `Instant` over `Date`.
- Avoid bidirectional `@OneToMany` unless you actually traverse from both sides; if you do, manage both sides in helper methods.
- Don't `@ManyToOne` across aggregate boundaries - hold the foreign ID.

### 2. Identifier Strategy

| Strategy | When |
| --- | --- |
| `GenerationType.UUID` (Hibernate 6 native) | Distributed inserts, no central sequence; PG `uuid` column |
| `GenerationType.SEQUENCE` with allocationSize | High-throughput inserts, monotonic IDs needed |
| `GenerationType.IDENTITY` | Convenient but breaks JPA batch insert (one round-trip per row) |

Avoid `IDENTITY` on Postgres-heavy write paths.

### 3. Repositories Express Intent

```java
public interface OrderRepository extends JpaRepository<Order, UUID> {

    Optional<Order> findByIdAndCustomerId(UUID id, UUID customerId);

    boolean existsByOrderNumber(String orderNumber);

    @Query("""
        select o from Order o
        left join fetch o.lines
        where o.id = :id
        """)
    Optional<Order> findByIdWithLines(@Param("id") UUID id);

    // Keyset pagination (preferred for deep pages)
    @Query("""
        select o from Order o
        where o.customerId = :customerId
          and (:cursorCreatedAt is null
               or o.createdAt < :cursorCreatedAt
               or (o.createdAt = :cursorCreatedAt and o.id < :cursorId))
        order by o.createdAt desc, o.id desc
        """)
    List<Order> findPageAfter(@Param("customerId") UUID customerId,
                              @Param("cursorCreatedAt") OffsetDateTime cursorCreatedAt,
                              @Param("cursorId") UUID cursorId,
                              Limit limit);                // Spring Data 3.2+
}
```

Anti-patterns: exposing `findAll()` for unbounded data; methods named after columns instead of intent (`findByStatusAndCreatedAtGreaterThan` is fine for one filter, ugly for five - drop into `@Query` or Specifications).

### 4. Fetch Strategy: Lazy by Default, Explicit Eager via Joins

Default to `FetchType.LAZY` for `@ManyToOne` and `@OneToMany`. Solve N+1 with **deliberate** fetch joins or `@EntityGraph`.

```java
@EntityGraph(attributePaths = {"lines"})
@Query("select o from Order o where o.customerId = :customerId")
List<Order> findCustomerOrdersWithLines(@Param("customerId") UUID id);
```

Detect regressions in tests with **datasource-proxy** or `Hibernate.getSessionFactory().getStatistics()`:

```java
@Test
void noNPlusOneOnListOrders() {
    var stats = entityManagerFactory.unwrap(SessionFactory.class).getStatistics();
    stats.clear(); stats.setStatisticsEnabled(true);

    repo.findCustomerOrdersWithLines(customerId);

    assertThat(stats.getPrepareStatementCount()).isEqualTo(1);
}
```

Hibernate 6 also supports `@BatchSize` on collections to mitigate accidental N+1 (still, prefer explicit fetch).

### 5. Transactions: Service Layer, Read-Only When Possible

```java
@Service
class OrderService {

    @Transactional
    public OrderResponse place(CreateOrderRequest req) { ... }

    @Transactional(readOnly = true)
    public List<OrderResponse> list(UUID customerId, Cursor c) { ... }
}
```

Do NOT call remote APIs inside `@Transactional`. Do NOT call `@Transactional` methods on `this` (proxy bypassed - no transaction).

### 6. Avoid the Top JPA Performance Pitfalls

| Pitfall | Symptom | Fix |
| --- | --- | --- |
| N+1 SELECTs | 1+N queries per list call | Fetch join, `@EntityGraph`, or DTO projection |
| Eager `@OneToMany` | Cartesian explosion, slow even when collection unused | `LAZY` + on-demand fetch |
| Loading entities just to read 2 fields | Waste of mapping + dirty checking | DTO projection (`@Query("select new com.acme.OrderRow(o.id, o.total) from Order o ...")` or interface projection) |
| `OFFSET 100000` pagination | Linear scan, latency cliff | Keyset pagination (see above) |
| `IDENTITY` IDs + `saveAll(1000)` | One round-trip per row | `SEQUENCE` with `allocationSize=50` + `spring.jpa.properties.hibernate.jdbc.batch_size=50` + `order_inserts=true` |
| Open Session In View | Lazy access during JSON serialization, hidden queries | `spring.jpa.open-in-view=false` (set globally) |
| Long transactions | Connection pool exhaustion under load | Split work; do remote calls outside `@Transactional` |
| Missing index on filter/sort columns | Sequential scans | Add index in Flyway migration; verify with `EXPLAIN` |

Production-safe defaults:

```yaml
spring:
  jpa:
    open-in-view: false
    properties:
      hibernate:
        jdbc:
          batch_size: 50
          time_zone: UTC
        order_inserts: true
        order_updates: true
        query:
          fail_on_pagination_over_collection_fetch: true
          in_clause_parameter_padding: true
        generate_statistics: false   # enable in perf testing
  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 2000
      max-lifetime: 1800000
      leak-detection-threshold: 5000
```

### 7. Schema Migrations: Flyway, Forward-Only, Backward-Compatible

`spring.jpa.hibernate.ddl-auto=validate` in all environments above local. Never `update` or `create-drop` in shared envs.

```
src/main/resources/db/migration/
  V1__init_orders.sql
  V2__add_orders_status_index.sql
  V3__add_orders_payment_method.sql
```

Zero-downtime schema rule (expand/contract):

1. **Expand**: add nullable column / new table; deploy app code that writes to both old + new.
2. Backfill data.
3. Deploy app code that reads from new only.
4. **Contract**: drop old column / constraint in a later release.

Never combine "drop column" + "deploy code that stops using it" in the same release.

Verify migrations apply cleanly in CI (boot a Testcontainers DB, run Flyway, fail on out-of-order or checksum mismatch).

### 8. Tests: Slice + Integration with Testcontainers

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class OrderRepositoryTest {

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

Use the same engine + version as production. H2 hides Postgres-specific bugs (JSONB, arrays, locking semantics, ON CONFLICT).

### 9. Concurrency

- **Optimistic** (`@Version`) is the default. Catch `OptimisticLockException`, return 409 Conflict.
- **Pessimistic** (`@Lock(PESSIMISTIC_WRITE)`) only when you must serialize concurrent updates of the same row (rare). Always set a lock timeout.
- For idempotent writes, use a unique business key + `INSERT ... ON CONFLICT` (Postgres) via native query.

### 10. Auditing

Use `@CreatedDate`, `@LastModifiedDate`, `@CreatedBy`, `@LastModifiedBy` with `@EntityListeners(AuditingEntityListener.class)` and `@EnableJpaAuditing`. Provide an `AuditorAware` that pulls the current user from `SecurityContextHolder`.

## Common Pitfalls (Quick Reference)

| Anti-pattern | Fix |
| --- | --- |
| `@OneToMany(fetch = EAGER)` | LAZY + explicit fetch |
| `spring.jpa.open-in-view=true` (default!) | Set to `false` |
| `ddl-auto=update` in prod | Flyway/Liquibase, `ddl-auto=validate` |
| `findAll()` exposed to the API | Bounded query + pagination |
| H2 in tests, Postgres in prod | Testcontainers Postgres |
| Money as `double` | `BigDecimal` with `precision`/`scale` |
| Calling REST inside `@Transactional` | Move outside; persist intent + retry async |
| `EntityGraph` for everything | Use only where needed; dial in fetch shape |

## Output Format

When applying this skill, deliver:

1. Aggregate diagram + entity outline with annotations.
2. Repository method catalog (intent-named, with fetch strategy noted).
3. Transaction boundary table.
4. Identified N+1 / fetch issues + remediation per query.
5. Flyway migration plan (expand/contract steps if relevant).
6. Hikari + Hibernate properties block tuned for the workload.
7. Test plan: slice tests, Testcontainers integration tests, query-count assertions.

## Authoritative References

- Spring Data JPA reference: https://docs.spring.io/spring-data/jpa/reference/
- Spring Data Commons (paging, projections): https://docs.spring.io/spring-data/commons/reference/
- Hibernate 6 user guide: https://docs.jboss.org/hibernate/orm/6.6/userguide/html_single/Hibernate_User_Guide.html
- Hibernate Performance tuning: https://docs.jboss.org/hibernate/orm/6.6/userguide/html_single/Hibernate_User_Guide.html#performance
- Vlad Mihalcea's High-Performance Java Persistence (book + blog): https://vladmihalcea.com/tutorials/hibernate/
- Flyway: https://documentation.red-gate.com/fd
- Testcontainers Java: https://java.testcontainers.org/
- HikariCP: https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing
- PostgreSQL Indexes: https://www.postgresql.org/docs/current/indexes.html
