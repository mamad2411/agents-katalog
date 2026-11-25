---
name: "db-arch-patterns"
description: "Data access patterns with code: repositories with Specification queries, Unit of Work transaction boundaries, DTO projections against N+1 queries, HikariCP pool sizing, and a consistent-hashing shard router. Use when designing or reviewing a data access layer."
---

# Database Architecture Patterns

> Named patterns with code for Repository interface, Unit of Work, Specification pattern, N+1 prevention, read replica routing, connection pool sizing, and sharding strategies.

## Patterns

### Pattern: Repository with Specification Query (TypeScript)

```typescript
// Domain layer — repository interface (no DB technology knowledge)
export interface OrderRepository {
  findById(id: string): Promise<Order | null>;
  findAll(spec: OrderSpecification): Promise<Order[]>;
  save(order: Order): Promise<void>;
  delete(id: string): Promise<void>;
}

// Specification — composable query criteria
export interface OrderSpecification {
  toWhereClause(): Record<string, unknown>;
}

export class PendingOrdersForCustomer implements OrderSpecification {
  constructor(private readonly customerId: string) {}

  toWhereClause() {
    return {
      customerId: this.customerId,
      status: 'PENDING',
    };
  }
}

// Infrastructure — Prisma implementation
export class PrismaOrderRepository implements OrderRepository {
  constructor(private readonly db: PrismaClient) {}

  async findAll(spec: OrderSpecification): Promise<Order[]> {
    const rows = await this.db.order.findMany({
      where: spec.toWhereClause(),
      include: { items: true },  // Eager load to prevent N+1
    });
    return rows.map(row => this.toDomain(row));
  }

  async save(order: Order): Promise<void> {
    await this.db.order.upsert({
      where: { id: order.id },
      create: this.toPersistence(order),
      update: this.toPersistence(order),
    });
  }

  private toDomain(row: OrderRow & { items: ItemRow[] }): Order {
    return Order.reconstitute({
      id: row.id,
      customerId: row.customerId,
      status: row.status as OrderStatus,
      items: row.items.map(i => new OrderItem(i.productId, i.qty, Money.of(i.price, i.currency))),
    });
  }
}
```

### Pattern: Unit of Work Transaction Boundary (Java/Spring)

```java
// Service owns the transaction — not the repository
@Service
@Slf4j
public class OrderFulfillmentService {

    private final OrderRepository orders;
    private final InventoryRepository inventory;
    private final DomainEventPublisher events;

    // ONE @Transactional covering all operations = atomic Unit of Work
    @Transactional
    public void fulfillOrder(String orderId) {
        Order order = orders.findById(new OrderId(orderId))
            .orElseThrow(() -> new OrderNotFoundException(orderId));

        List<OrderItem> items = order.items();

        // Reserve inventory — within same transaction
        for (OrderItem item : items) {
            InventoryReservation reservation = inventory
                .reserve(item.productId(), item.quantity());
            // If ANY reservation fails, entire transaction rolls back
        }

        // Change order status
        order.confirm();

        // Save changes — JPA dirty checking handles the SQL
        orders.save(order);

        // Publish event AFTER commit (use TransactionalEventListener)
        events.publish(new OrderConfirmedEvent(order));
    }
}
```

### Pattern: N+1 Prevention with DTO Projection (SQL)

When you need a list of summaries and not full entities, use a DTO projection to load exactly what you need in one query:

```sql
-- The query that replaces 1 + N queries
SELECT
    o.id           AS order_id,
    o.status       AS status,
    o.created_at   AS placed_at,
    c.name         AS customer_name,
    COUNT(oi.id)   AS item_count,
    SUM(oi.price * oi.quantity) AS total
FROM orders o
INNER JOIN customers c ON c.id = o.customer_id
LEFT JOIN order_items oi ON oi.order_id = o.id
WHERE o.status = 'PENDING'
  AND o.created_at > NOW() - INTERVAL '7 days'
GROUP BY o.id, o.status, o.created_at, c.name
ORDER BY o.created_at DESC
LIMIT 100;
```

Java JPQL equivalent:
```java
@Query("""
    SELECT new com.example.PendingOrderSummary(
        o.id, o.status, o.createdAt, c.name, COUNT(oi), SUM(oi.price * oi.quantity)
    )
    FROM Order o
    JOIN Customer c ON c.id = o.customerId
    LEFT JOIN o.items oi
    WHERE o.status = 'PENDING'
    AND o.createdAt > :since
    GROUP BY o.id, o.status, o.createdAt, c.name
    ORDER BY o.createdAt DESC
""")
List<PendingOrderSummary> findPendingSummaries(@Param("since") Instant since, Pageable pageable);
```

### Pattern: Connection Pool Sizing (HikariCP)

```yaml
# application.yml
spring:
  datasource:
    url: jdbc:postgresql://db.internal:5432/myapp
    username: ${DB_USER}
    password: ${DB_PASSWORD}
    hikari:
      # Starting point: (cpu_cores * 2) + effective_spindles
      # For PostgreSQL on 4-core, SSD: (4*2)+1=9, round to 10
      maximum-pool-size: 10

      # Keep at least 5 connections warm
      minimum-idle: 5

      # Fail fast if no connection available — don't queue forever
      connection-timeout: 3000      # 3 seconds

      # Release connections idle longer than 10 minutes
      idle-timeout: 600000

      # Recycle connections periodically to prevent stale connections
      max-lifetime: 1800000

      # Detect connections held longer than 5s — likely leak
      leak-detection-threshold: 5000

      # Validate connection before use
      connection-test-query: SELECT 1
```

Monitoring query (run periodically in Prometheus or dashboards):
```sql
-- PostgreSQL: check pool utilization
SELECT
    count(*) FILTER (WHERE state = 'active') AS active,
    count(*) FILTER (WHERE state = 'idle')   AS idle,
    count(*) FILTER (WHERE state = 'idle in transaction') AS idle_in_tx,
    count(*)                                  AS total
FROM pg_stat_activity
WHERE datname = 'myapp';
```

Alert when: `idle_in_tx > 0` (long-running transactions blocking locks), or `active > max_pool_size * 0.9` (pool near exhaustion).

### Pattern: Consistent Hashing Shard Key Router

```python
import hashlib
import bisect
from typing import List

class ConsistentHashRing:
    """
    Consistent hashing for database sharding.
    Adding/removing shards moves only ~1/n of keys.
    """
    def __init__(self, shards: List[str], virtual_nodes: int = 150):
        self.ring = {}
        self.sorted_keys = []
        self.virtual_nodes = virtual_nodes

        for shard in shards:
            self.add_shard(shard)

    def add_shard(self, shard: str):
        for i in range(self.virtual_nodes):
            key = self._hash(f"{shard}:{i}")
            self.ring[key] = shard
            bisect.insort(self.sorted_keys, key)

    def get_shard(self, key: str) -> str:
        """Determine which shard a given key belongs to."""
        hash_val = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, hash_val) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]

    def _hash(self, value: str) -> int:
        return int(hashlib.md5(value.encode()).hexdigest(), 16)

# Usage
ring = ConsistentHashRing(["shard-1", "shard-2", "shard-3"])

def get_order_db(order_id: str) -> str:
    return ring.get_shard(order_id)

# When shard-4 is added, only ~25% of keys move (not 75% as in modulo hashing)
ring.add_shard("shard-4")
```

## Anti-Patterns

### Anti-Pattern: Repository That Leaks Persistence Concepts

```java
// VIOLATION: repository method returns ORM-specific type
public interface OrderRepository {
    @Query("FROM Order o WHERE o.status = ?1")
    TypedQuery<Order> findByStatusQuery(String status);  // Leaks JPA TypedQuery to caller

    Page<Order> findByCustomerIdOrderByCreatedAtDesc(String customerId, Pageable pageable);
    // ^^^ Spring Data naming convention works but mixes persistence with domain vocabulary
}
```

Repository interfaces should speak domain language. `findRecentOrdersForCustomer(CustomerId, int limit)` is better than `findByCustomerIdOrderByCreatedAtDescWithLimit`. The domain interface should not reference `Page<T>`, `Pageable`, `Sort`, or `TypedQuery`.

### Anti-Pattern: @Transactional on Repository Methods

```java
@Repository
public class JpaOrderRepository {

    @Transactional  // Wrong — transaction too fine-grained
    public void save(Order order) {
        // ...
    }
}
```

Repository-level transactions mean that if a service method saves an order and then reserves inventory, they are in different transactions. If the inventory reservation fails, the order save is already committed and cannot be rolled back. `@Transactional` belongs on the service method that defines the business unit of work.

### Anti-Pattern: Unlimited Query Without Pagination

```java
// Can return millions of rows — crashes the application
List<Order> allOrders = orderRepository.findAll();

// Or worse — loads all in memory for in-memory filtering
List<Order> filtered = orderRepository.findAll()
    .stream()
    .filter(o -> o.status() == PENDING)
    .toList();
```

Every collection query must have a limit. Use pagination for user-facing queries. For batch processing, use cursor-based iteration with `WHERE id > :last_id ORDER BY id LIMIT :batch_size`.

### Anti-Pattern: Eagerly Loading Everything to Avoid N+1 Thinking

```java
@Entity
public class Order {
    @OneToMany(fetch = EAGER)  // Loads ALL items for ALL orders on every query
    private List<OrderItem> items;

    @ManyToOne(fetch = EAGER)  // Loads customer for every order, every time
    private Customer customer;
}
```

EAGER loading trades N+1 for always-load. If you load 100 orders for a list page that shows only the order ID and status, you also loaded 100 customers and all their items. Use LAZY loading as the default; load eagerly only when you know the associations will be used (via JOIN FETCH or @EntityGraph per-query).

## References

- Fowler, Martin. _Patterns of Enterprise Application Architecture_. Addison-Wesley, 2002.
- Petrov, Alex. _Database Internals_. O'Reilly, 2019.
- HikariCP: github.com/brettwooldridge/HikariCP. "About Pool Sizing" wiki.
- Karger, David, et al. "Consistent Hashing and Random Trees." ACM STOC 1997.
- PostgreSQL: postgresql.org/docs. Partitioning, connection management.
