---
name: hexagonal-architecture-java
description: >
  Hexagonal Architecture (Ports and Adapters) patterns for Java services.
  Trigger: When designing Java services with hexagonal architecture, clean architecture, or ports-and-adapters pattern.
license: Apache-2.0
metadata:
  version: "1.0"
format: reference
---

## When to Use

**Triggers**: When designing Java services with hexagonal architecture, clean architecture, or ports-and-adapters pattern.

Load when: designing Java applications with hexagonal architecture, implementing ports and adapters, or maintaining clean separation between domain and infrastructure.

## Critical Patterns

### Fundamental Rule: The domain has no external dependencies

```
Domain → no imports from Spring, JPA, HTTP, or any framework
Application → defines ports (interfaces), orchestrates the domain
Infrastructure → implements the ports (JPA, REST, Kafka, etc.)

Dependency flow (always inward):
Infrastructure → Application → Domain
```

### Pattern 1: Pure Domain (no frameworks)

```java
// ✅ Domain entity — no framework annotations
public class Order {
    private final OrderId id;
    private final CustomerId customerId;
    private final List<OrderItem> items;
    private OrderStatus status;

    // Constructor, business methods
    public void confirm() {
        if (this.status != OrderStatus.PENDING) {
            throw new IllegalStateException("Only pending orders can be confirmed");
        }
        this.status = OrderStatus.CONFIRMED;
    }

    public Money total() {
        return items.stream()
            .map(OrderItem::subtotal)
            .reduce(Money.ZERO, Money::add);
    }
}

// ❌ Domain with JPA annotations — violates purity
@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue
    private Long id;          // DB type, not business type

    @Column
    private String status;    // String instead of domain enum
}
```

### Pattern 2: Application Layer — defines ports

```java
// Input port (Use Case)
public interface CreateOrderUseCase {
    OrderId execute(CreateOrderCommand command);
}

// Output port (Repository — defined in application, implemented in infra)
public interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(OrderId id);
    List<Order> findByCustomer(CustomerId customerId);
}

// Output port (notifications)
public interface NotificationPort {
    void notifyOrderConfirmed(Order order);
}

// Application service — implements the use case, uses the ports
@Service // ✅ Spring here is fine — this is the application layer
public class CreateOrderService implements CreateOrderUseCase {

    private final OrderRepository orderRepository;
    private final NotificationPort notificationPort;

    public CreateOrderService(
        OrderRepository orderRepository,
        NotificationPort notificationPort
    ) {
        this.orderRepository = orderRepository;
        this.notificationPort = notificationPort;
    }

    @Override
    @Transactional
    public OrderId execute(CreateOrderCommand command) {
        var order = Order.create(command.customerId(), command.items());
        orderRepository.save(order);
        notificationPort.notifyOrderConfirmed(order);
        return order.id();
    }
}
```

### Pattern 3: Infrastructure — implements the ports

```java
// Persistence adapter (implements the domain port)
@Repository
public class JpaOrderRepository implements OrderRepository {

    private final JpaOrderEntityRepository jpa;
    private final OrderMapper mapper;

    @Override
    public void save(Order order) {
        jpa.save(mapper.toEntity(order));
    }

    @Override
    public Optional<Order> findById(OrderId id) {
        return jpa.findById(id.value())
            .map(mapper::toDomain);
    }
}

// Input REST adapter
@RestController
@RequestMapping("/api/orders")
public class OrderController {

    private final CreateOrderUseCase createOrder;

    @PostMapping
    public ResponseEntity<OrderIdResponse> create(@RequestBody CreateOrderRequest request) {
        var command = new CreateOrderCommand(
            new CustomerId(request.customerId()),
            request.items().stream().map(this::toItem).toList()
        );
        var orderId = createOrder.execute(command);
        return ResponseEntity.ok(new OrderIdResponse(orderId.value()));
    }
}
```

## Code Examples

### Package Structure

```
com.myapp/
├── domain/
│   ├── model/                  # Entities, Value Objects
│   │   ├── Order.java
│   │   ├── OrderId.java        # Value Object
│   │   └── Money.java          # Value Object
│   └── service/                # Domain services (logic that doesn't fit in an entity)
│       └── PricingService.java
├── application/
│   ├── port/
│   │   ├── in/                 # Use cases (input ports)
│   │   │   └── CreateOrderUseCase.java
│   │   └── out/                # Output ports
│   │       ├── OrderRepository.java
│   │       └── NotificationPort.java
│   ├── service/                # Use case implementations
│   │   └── CreateOrderService.java
│   └── dto/                    # Commands and Queries
│       └── CreateOrderCommand.java
└── infrastructure/
    ├── persistence/
    │   ├── JpaOrderRepository.java   # Implements OrderRepository
    │   ├── OrderEntity.java          # JPA Entity
    │   └── OrderMapper.java          # Domain ↔ Entity
    ├── web/
    │   ├── OrderController.java      # REST adapter
    │   └── OrderRequest.java         # DTOs HTTP
    └── notification/
        └── EmailNotificationAdapter.java # Implements NotificationPort
```

### Value Objects

```java
// ✅ Value Object — immutable, validated, no @Entity
public record OrderId(UUID value) {
    public OrderId {
        Objects.requireNonNull(value, "OrderId cannot be null");
    }

    public static OrderId generate() {
        return new OrderId(UUID.randomUUID());
    }

    public static OrderId of(String value) {
        return new OrderId(UUID.fromString(value));
    }
}

public record Money(BigDecimal amount, Currency currency) {
    public static final Money ZERO = new Money(BigDecimal.ZERO, Currency.EUR);

    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("Cannot add different currencies");
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }
}
```

## Anti-Patterns

### ❌ JPA in the Domain

```java
// ❌ Coupling with JPA in the domain
@Entity
public class Order {
    @OneToMany(cascade = CascadeType.ALL)
    private List<OrderItemEntity> items;  // Infrastructure type in domain
}

// ✅ Domain uses its own types
public class Order {
    private final List<OrderItem> items;  // Domain type
}
```

### ❌ Spring Repository in application layer

```java
// ❌ Application depends on infrastructure
import org.springframework.data.repository.CrudRepository; // Spring in application

public interface OrderRepository extends CrudRepository<OrderEntity, Long> {}

// ✅ Port defined in application, no framework imports
public interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(OrderId id);
}
```

## Quick Reference

| Layer | Contains | Does not contain |
|-------|----------|------------------|
| Domain | Entities, VOs, Domain Services | Spring, JPA, HTTP |
| Application | Use Cases, Ports (interfaces), Commands | JPA entities, HTTP |
| Infrastructure | Controllers, JPA Adapters, External APIs | Domain logic |

| Task | Pattern |
|------|---------|
| Input port | Interface in `application/port/in/` |
| Output port | Interface in `application/port/out/` |
| Implement port | In `infrastructure/` |
| Use case | Service in `application/service/` |
| Injection | Constructor injection in all services |

## Rules

- Domain entities and use cases must have zero dependencies on framework classes (no Spring annotations, no JPA annotations inside domain)
- Ports are interfaces defined in the domain layer; adapters are implementations in the infrastructure layer — never the reverse
- Application services (use cases) orchestrate domain logic only; they must not contain persistence or HTTP concerns
- Each adapter must implement exactly one port; combining multiple ports in a single adapter class is a violation of the pattern
- Tests for use cases must use test doubles (stubs/fakes) for ports, never the real adapter implementations
