# JPA / Hibernate Patterns in Spring Boot

## Summary

**One-sentence:** JPA/Hibernate patterns — auditing timestamps, narrow repositories, justified cascade/fetch, optimistic locking, JOIN FETCH for eager loads, DTO projections for reads.

**One-paragraph:** JPA misuse — open-in-view enabled, `CascadeType.ALL` everywhere, lazy collections accessed outside transactions, N+1 from naive `findAll()` — produces "Hibernate is slow" complaints. This methodology pins five rules: every entity has audit timestamps + version where editable; cascade + fetch choices carry a written justification; repositories are narrow interfaces (no raw `JpaRepository` exposure); reads project to DTOs; eager loading uses explicit `JOIN FETCH`/`@EntityGraph`. Output: entity + narrow repository + transactional service spec conforming to `02-output-contract.xml`.

**Ефективно для:**

- Spring Boot 3.x + Hibernate 6.x services with non-trivial domain.
- High-throughput read paths needing DTO projection.
- Inventory / balance domains requiring optimistic locking.
- Teams that have suffered N+1 + open-in-view incidents.
- AI-generated code that defaults to `CascadeType.ALL`.

## Applies If (ALL must hold)

- Spring Boot 3.x project with JPA/Hibernate.
- Spring Data JPA repositories are in place.
- The team accepts narrow repository discipline (no raw `JpaRepository` in services).
- Flyway/Liquibase manage schema migrations.

## Skip If (ANY kills it)

- Reactive stack (Spring Data R2DBC) — different idioms.
- Plain JDBC / MyBatis — apply that stack's methodology.
- Single-table CRUD with no domain — Active Record on the entity is enough.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Entity sketch | Markdown / source | spec |
| Flyway migration baseline | SQL | repo |
| Performance budget | Markdown | spec |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-spring]] | Layered architecture + DI conventions this layers on. |
| [[ddd-repositories]] | Narrow-repository pattern referenced here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: audit-timestamps, justified-cascade-fetch, narrow-repo-interface, dto-projection-on-reads, joinfetch-for-eager | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for entity+repo+service spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: open-in-view, cascade-all, lazy-outside-tx, n-plus-1 | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on read/write shape → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-entity-mapping` | sonnet | Cascade + fetch judgment. |
| `write-narrow-repository` | sonnet | Interface naming + method set. |
| `audit-existing-queries` | sonnet | Look for N+1 + cascade misuse. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Entity.java` | Entity with audit + version + justified mappings |
| `templates/NarrowRepository.java` | Narrow read/write repository interfaces |
| `templates/Service.java` | Transactional service with JOIN FETCH + DTO projection |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-jpa-hibernate.py` | Validate entity+repo+service spec | Pre-commit on spec artefact |

## Related

- [[java-spring]]
- [[java-junit-testing]]
- [[ddd-repositories]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (read vs write, association depth, list vs single) to a rule from `01-core-rules.xml`. Use it whenever adding an entity, a repository method, or a slow query.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/Entity.java`

```java
package faion.domain.orders;

import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, length = 200)
    private String customerName;

    @Column(nullable = false, precision = 18, scale = 2)
    private BigDecimal total = BigDecimal.ZERO;

    /**
     * Items are wholly owned by Order. Cascade PERSIST + orphanRemoval so the
     * aggregate boundary matches persistence. Fetch LAZY by default; loaded
     * eagerly only via JOIN FETCH where required.
     */
    @OneToMany(mappedBy = "order", cascade = {CascadeType.PERSIST, CascadeType.MERGE}, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();

    @Version
    private Long version;

    @CreationTimestamp
    @Column(updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    private Instant updatedAt;

    protected Order() { }

    public Order(String customerName) {
        this.customerName = customerName;
    }

    public UUID getId() { return id; }
    public String getCustomerName() { return customerName; }
    public BigDecimal getTotal() { return total; }
    public List<OrderItem> getItems() { return List.copyOf(items); }
    public Long getVersion() { return version; }
}
```

### `templates/NarrowRepository.java`

```java
package faion.infra.orders;

import faion.domain.orders.Order;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.NoRepositoryBean;
import org.springframework.data.repository.query.Param;

import java.util.Optional;
import java.util.UUID;

@NoRepositoryBean
public interface OrderRepository {

    Optional<Order> findById(UUID id);

    @Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.id = :id")
    Optional<Order> findByIdWithItems(@Param("id") UUID id);

    Page<OrderSummaryDto> findAllSummaries(Pageable pageable);

    Order save(Order order);

    void delete(Order order);
}

interface OrderRepositoryJpa extends OrderRepository, JpaRepository<Order, UUID> {

    @Override
    @EntityGraph(attributePaths = {"items"})
    Optional<Order> findByIdWithItems(@Param("id") UUID id);

    @Override
    @Query("SELECT new faion.infra.orders.OrderSummaryDto(o.id, o.customerName, o.total) FROM Order o")
    Page<OrderSummaryDto> findAllSummaries(Pageable pageable);
}

record OrderSummaryDto(UUID id, String customerName, java.math.BigDecimal total) {}
```

### `templates/Service.java`

```java
package faion.app.orders;

import faion.domain.orders.Order;
import faion.infra.orders.OrderRepository;
import faion.infra.orders.OrderSummaryDto;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
@Transactional(readOnly = true)
public class OrderService {

    private final OrderRepository repository;

    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    public OrderResponse getById(UUID id) {
        Order order = repository.findByIdWithItems(id)
            .orElseThrow(() -> new OrderNotFoundException(id));
        return OrderResponse.from(order);
    }

    public Page<OrderSummaryDto> list(Pageable pageable) {
        return repository.findAllSummaries(pageable);
    }

    @Transactional
    public OrderResponse create(CreateOrderRequest req) {
        Order order = new Order(req.customerName());
        repository.save(order);
        return OrderResponse.from(order);
    }
}

record CreateOrderRequest(String customerName) {}
record OrderResponse(UUID id, String customerName, java.math.BigDecimal total) {
    static OrderResponse from(Order o) {
        return new OrderResponse(o.getId(), o.getCustomerName(), o.getTotal());
    }
}

class OrderNotFoundException extends RuntimeException {
    OrderNotFoundException(UUID id) { super("order not found: " + id); }
}
```
