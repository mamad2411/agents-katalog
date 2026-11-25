---
name: "hex-arch-patterns"
description: "Hexagonal architecture patterns with code: package layout, driving ports with use case interactors, driven ports with JPA adapters, in-memory test adapters, and ArchUnit fitness tests. Use when building or reviewing a ports-and-adapters service."
---

# Hexagonal Architecture Patterns

> Named patterns with code for driving ports, driven ports, adapter implementation, in-memory test adapters, and ArchUnit fitness functions.

## Patterns

### Pattern: Folder Structure

```
src/
  domain/
    model/
      Order.java            (entity — no framework dependencies)
      OrderId.java          (value object)
      OrderItem.java        (entity within Order aggregate)
      Money.java            (value object)
    event/
      OrderPlacedEvent.java (domain event)
    port/
      out/
        OrderRepository.java    (driven port — interface owned by domain/application)
        EventPublisher.java     (driven port)
  application/
    port/
      in/
        PlaceOrderUseCase.java  (driving port)
        CancelOrderUseCase.java (driving port)
    service/
      PlaceOrderInteractor.java (implements PlaceOrderUseCase)
    dto/
      PlaceOrderCommand.java
  adapter/
    web/
      OrderController.java      (driving adapter — calls PlaceOrderUseCase)
      OrderRequest.java         (HTTP DTO)
      OrderResponse.java        (HTTP DTO)
    persistence/
      JpaOrderRepository.java   (driven adapter — implements OrderRepository)
      OrderJpaEntity.java       (JPA entity — @Entity, @Column here, NOT on domain)
      OrderEntityMapper.java    (maps domain ↔ JPA entity)
    messaging/
      OrderEventPublisher.java  (driven adapter — implements EventPublisher)
```

### Pattern: Driving Port with Use Case Interactor (Java)

```java
// Driving port — in application.port.in
public interface PlaceOrderUseCase {
    record PlaceOrderCommand(
        CustomerId customerId,
        List<OrderItem> items
    ) {}

    OrderId placeOrder(PlaceOrderCommand command);
}

// Interactor — implements the driving port
// Lives in application.service
@Service
@Transactional
public class PlaceOrderInteractor implements PlaceOrderUseCase {

    private final OrderRepository orderRepository;    // Driven port
    private final EventPublisher eventPublisher;      // Driven port
    private final CustomerRepository customerRepository;  // Driven port

    @Override
    public OrderId placeOrder(PlaceOrderCommand command) {
        Customer customer = customerRepository.findById(command.customerId())
            .orElseThrow(() -> new CustomerNotFoundException(command.customerId()));

        Order order = Order.create(command.customerId(), command.items());
        orderRepository.save(order);

        List<DomainEvent> events = order.collectEvents();
        events.forEach(eventPublisher::publish);

        return order.id();
    }
}
```

### Pattern: Driven Port with JPA Adapter (Java)

```java
// Driven port — interface in domain.port.out (owned by inner hexagon)
public interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(OrderId id);
    List<Order> findByCustomerId(CustomerId customerId);
}

// Driven adapter — implements port, lives in adapter.persistence
// @Repository is a Spring annotation — ok here, not in domain
@Repository
public class JpaOrderRepositoryAdapter implements OrderRepository {

    private final SpringDataOrderRepository springRepo;
    private final OrderEntityMapper mapper;

    @Override
    public void save(Order order) {
        OrderJpaEntity entity = mapper.toEntity(order);
        springRepo.save(entity);
    }

    @Override
    public Optional<Order> findById(OrderId id) {
        return springRepo.findById(id.value())
            .map(mapper::toDomain);
    }

    @Override
    public List<Order> findByCustomerId(CustomerId customerId) {
        return springRepo.findByCustomerId(customerId.value()).stream()
            .map(mapper::toDomain)
            .toList();
    }
}

// JPA Entity — @Entity annotation ONLY here, never on domain Order class
@Entity
@Table(name = "orders")
public class OrderJpaEntity {
    @Id
    @Column(name = "order_id")
    private String orderId;

    @Column(name = "customer_id")
    private String customerId;

    @Column(name = "status")
    private String status;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL)
    private List<OrderItemJpaEntity> items;
}
```

### Pattern: In-Memory Test Adapter (Java)

```java
// Test double — implements the same driven port
// No database, no Spring context — runs in milliseconds
class InMemoryOrderRepository implements OrderRepository {

    private final Map<OrderId, Order> store = new HashMap<>();

    @Override
    public void save(Order order) {
        store.put(order.id(), order);
    }

    @Override
    public Optional<Order> findById(OrderId id) {
        return Optional.ofNullable(store.get(id));
    }

    @Override
    public List<Order> findByCustomerId(CustomerId customerId) {
        return store.values().stream()
            .filter(o -> o.customerId().equals(customerId))
            .toList();
    }

    // Test helper — not part of the port
    public int size() { return store.size(); }
}

// Fast unit test — no Spring, no H2, no Testcontainers
class PlaceOrderInteractorTest {

    private InMemoryOrderRepository orderRepo = new InMemoryOrderRepository();
    private InMemoryEventPublisher eventPublisher = new InMemoryEventPublisher();
    private InMemoryCustomerRepository customerRepo = new InMemoryCustomerRepository();
    private PlaceOrderUseCase useCase;

    @BeforeEach
    void setUp() {
        customerRepo.save(Customer.of(CUSTOMER_ID, "Alice"));
        useCase = new PlaceOrderInteractor(orderRepo, eventPublisher, customerRepo);
    }

    @Test
    void shouldSaveOrderAndPublishEvent() {
        var cmd = new PlaceOrderCommand(CUSTOMER_ID, List.of(ITEM));
        OrderId orderId = useCase.placeOrder(cmd);

        assertThat(orderRepo.findById(orderId)).isPresent();
        assertThat(eventPublisher.events()).hasSize(1)
            .first().isInstanceOf(OrderPlacedEvent.class);
    }
}
```

### Pattern: ArchUnit Hexagonal Fitness Test

```java
@AnalyzeClasses(packages = "com.example.orders")
class HexagonalArchitectureFitnessTest {

    @ArchTest
    static final ArchRule domain_has_no_framework_dependencies =
        noClasses().that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAnyPackage("org.springframework..", "javax.persistence..", "jakarta.persistence..");

    @ArchTest
    static final ArchRule ports_are_interfaces =
        classes().that().resideInAnyPackage("..port.in..", "..port.out..")
            .should().beInterfaces()
            .as("Ports must be interfaces — adapters provide implementations");

    @ArchTest
    static final ArchRule adapters_do_not_call_each_other =
        noClasses().that().resideInAPackage("..adapter.web..")
            .should().dependOnClassesThat().resideInAPackage("..adapter.persistence..")
            .as("Web adapter must not call persistence adapter — go through use case");

    @ArchTest
    static final ArchRule application_does_not_depend_on_infrastructure =
        noClasses().that().resideInAnyPackage("..domain..", "..application..")
            .should().dependOnClassesThat().resideInAPackage("..adapter..");
}
```

## Anti-Patterns

### Anti-Pattern: Port Interface in Infrastructure Layer

```java
// WRONG: the port interface is in the infrastructure/adapter layer
package com.example.adapter.persistence;

public interface OrderRepository { ... }  // Wrong location

// The domain/application layer now depends on infrastructure to import this interface
// Dependency arrow points outward — violates the hexagonal rule
```

Fix: move port interfaces to `domain.port.out` or `application.port.out`. The inner hexagon owns the interface.

### Anti-Pattern: JPA Annotations on Domain Objects

```java
// WRONG: domain entity has persistence concerns
@Entity  // Framework annotation in the domain
@Table(name = "orders")
public class Order {
    @Id
    private String id;

    @OneToMany(cascade = CascadeType.ALL)  // JPA semantics leaking into domain
    private List<OrderItem> items;
}
```

Fix: create a separate `OrderJpaEntity` class in the persistence adapter. Map between domain `Order` and `OrderJpaEntity` in `OrderEntityMapper`. The domain `Order` has no JPA annotations.

### Anti-Pattern: Use Case Interactor Directly Instantiating Adapters

```java
// WRONG: interactor creates the adapter — hardcoded dependency, untestable
public class PlaceOrderInteractor implements PlaceOrderUseCase {
    private final OrderRepository repo = new JpaOrderRepositoryAdapter(...);  // new!
}
```

Fix: inject the driven port via constructor. Spring (or any DI container) wires the adapter. Tests inject an in-memory adapter.

### Anti-Pattern: Web Controller Calling Repository Directly

```java
// WRONG: controller skips the application layer entirely
@RestController
public class OrderController {
    private final OrderRepository orderRepository;  // Direct to persistence

    @PostMapping("/orders")
    public Order createOrder(...) {
        return orderRepository.save(...);  // No use case, no domain logic, no invariants
    }
}
```

Fix: controllers call use case ports. Use cases call repository ports. The flow: Controller → UseCase → Repository.

## References

- Cockburn, Alistair. "Hexagonal Architecture." alistair.cockburn.us, 2005.
- Hombergs, Tom. _Get Your Hands Dirty on Clean Architecture_, 2nd ed. Packt, 2023.
- ArchUnit: archunit.org (fitness functions for architecture)
- Graca, Herberto. herbertograca.com/dev-theory/explicit-architecture
