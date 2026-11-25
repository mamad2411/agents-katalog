---
name: "clean-arch-patterns"
description: "Clean Architecture patterns with code: a folder structure that enforces the dependency rule, entities that guard their invariants, presenter and view model separation, framework-free use case tests, and ArchUnit rules. Use when building or reviewing a Clean Architecture codebase."
---

# Clean Architecture Patterns

> Named patterns with code examples for use case design, entity invariant enforcement, repository port design, presenter/view model separation, framework-free testing, and ArchUnit enforcement of the dependency rule.

## Patterns

### Pattern: Folder Structure Enforcing the Dependency Rule

```
src/
├── domain/                          # Enterprise Business Rules (innermost)
│   ├── model/
│   │   ├── Order.java               # Entity — no framework deps
│   │   ├── OrderId.java             # Value object
│   │   ├── OrderItem.java           # Value object
│   │   └── Money.java               # Value object
│   ├── event/
│   │   └── OrderPlacedEvent.java    # Domain event
│   └── repository/
│       └── OrderRepository.java     # Output port interface (only interface, not impl)
│
├── application/                     # Application Business Rules (use cases)
│   └── usecase/
│       ├── PlaceOrderUseCase.java   # Input port (interface)
│       ├── PlaceOrderRequest.java   # Request model
│       ├── PlaceOrderResponse.java  # Response model
│       └── PlaceOrderInteractor.java # Implementation (depends on domain only)
│
├── adapter/                         # Interface Adapters
│   ├── web/
│   │   ├── OrderController.java     # Converts HTTP → use case request
│   │   └── OrderApiDto.java         # HTTP-specific DTO (JSON serialization here)
│   └── persistence/
│       ├── JpaOrderRepository.java  # Implements domain's OrderRepository
│       ├── OrderJpaEntity.java      # JPA entity (framework coupling here, not in domain)
│       └── OrderMapper.java         # Domain ↔ JPA mapping
│
└── infrastructure/                  # Frameworks & Drivers
    ├── config/
    │   └── BeanConfig.java          # Spring DI wiring
    └── persistence/
        └── SpringDataOrderRepo.java # Spring Data JPA interface
```

Dependency direction: `infrastructure → adapter → application → domain`. Never reversed.

### Pattern: Entity with Invariant Enforcement

Domain entities enforce their own business invariants. No external service validates the entity — it is self-validating:

```java
public class Order {
    private final OrderId id;
    private final CustomerId customerId;
    private OrderStatus status;
    private final List<OrderItem> items;
    private final Instant placedAt;

    // Private constructor — use factory methods
    private Order(OrderId id, CustomerId customerId, List<OrderItem> items) {
        this.id = Objects.requireNonNull(id);
        this.customerId = Objects.requireNonNull(customerId);
        this.items = Collections.unmodifiableList(new ArrayList<>(items));
        this.status = OrderStatus.PENDING;
        this.placedAt = Instant.now();
        this.validate();
    }

    private void validate() {
        if (items.isEmpty()) {
            throw new DomainException("Order must have at least one item");
        }
        if (items.stream().anyMatch(item -> item.quantity() <= 0)) {
            throw new DomainException("Order item quantity must be positive");
        }
    }

    // Factory method — named for the business action
    public static Order create(CustomerId customerId, List<OrderItem> items) {
        return new Order(OrderId.generate(), customerId, items);
    }

    // Reconstitution from persistence — different from creation
    public static Order reconstitute(OrderId id, CustomerId customerId,
                                     OrderStatus status, List<OrderItem> items,
                                     Instant placedAt) {
        Order order = new Order(id, customerId, items);
        order.status = status;
        return order;
    }

    // Domain behavior — enforces business rule
    public void cancel(String reason) {
        if (this.status == OrderStatus.DISPATCHED) {
            throw new DomainException("Cannot cancel an order that has been dispatched");
        }
        if (this.status == OrderStatus.CANCELLED) {
            throw new DomainException("Order is already cancelled");
        }
        this.status = OrderStatus.CANCELLED;
        // Domain event would be recorded here in event sourcing variant
    }

    // No setters — state changes only through business methods
    public OrderId id() { return id; }
    public OrderStatus status() { return status; }
    // ... other getters
}
```

### Pattern: Presenter / View Model Separation

The presenter converts the use case output model into a view model formatted for the delivery mechanism. The use case does not know about formatting, localization, or HTTP-specific concerns.

```java
// Use case output — plain data
public record PlaceOrderResponse(
    String orderId,
    String status,
    Instant placedAt,
    Money total
) {}

// View model — formatted for HTTP JSON response
public record OrderApiResponse(
    String id,
    String status,
    String placedAt,     // ISO 8601 string, not Instant
    String total,        // "99.99 USD", not Money object
    Map<String, String> links  // HATEOAS links
) {}

// Presenter in the adapter layer
@Component
public class OrderPresenter {

    public OrderApiResponse present(PlaceOrderResponse response) {
        return new OrderApiResponse(
            response.orderId(),
            response.status().toLowerCase(),
            response.placedAt().toString(),
            formatMoney(response.total()),
            Map.of(
                "self", "/api/v1/orders/" + response.orderId(),
                "cancel", "/api/v1/orders/" + response.orderId() + "/cancel"
            )
        );
    }

    private String formatMoney(Money money) {
        return money.amount().toPlainString() + " " + money.currency();
    }
}

// Controller uses presenter — use case output never goes directly to response
@RestController
public class OrderController {

    private final PlaceOrderUseCase useCase;
    private final OrderPresenter presenter;

    @PostMapping("/api/v1/orders")
    public ResponseEntity<OrderApiResponse> placeOrder(@RequestBody OrderRequest req) {
        PlaceOrderRequest request = new PlaceOrderRequest(
            req.customerId(), req.items(), req.shippingAddress()
        );
        PlaceOrderResponse response = useCase.placeOrder(request);
        return ResponseEntity.status(201).body(presenter.present(response));
    }
}
```

### Pattern: Framework-Free Use Case Test

```java
// Test with zero framework dependencies
class CancelOrderInteractorTest {

    // In-memory stubs — no Spring, no database
    private final Map<OrderId, Order> store = new HashMap<>();
    private final OrderRepository repo = new InMemoryOrderRepository(store);
    private final List<DomainEvent> publishedEvents = new ArrayList<>();
    private final EventPublisher publisher = publishedEvents::add;

    private final CancelOrderInteractor interactor = new CancelOrderInteractor(repo, publisher);

    @Test
    void cancels_pending_order_successfully() {
        // Arrange
        Order order = Order.create(new CustomerId("c-1"), List.of(someItem()));
        store.put(order.id(), order);

        CancelOrderRequest request = new CancelOrderRequest(
            order.id().value(),
            "Customer changed mind"
        );

        // Act
        CancelOrderResponse response = interactor.cancel(request);

        // Assert
        assertThat(response.newStatus()).isEqualTo("CANCELLED");
        assertThat(store.get(order.id()).status()).isEqualTo(OrderStatus.CANCELLED);
        assertThat(publishedEvents).hasSize(1)
            .first().isInstanceOf(OrderCancelledEvent.class);
    }

    @Test
    void rejects_cancellation_of_dispatched_order() {
        // Arrange — order that has been dispatched
        Order order = Order.create(new CustomerId("c-1"), List.of(someItem()));
        order.dispatch();  // Business method transition
        store.put(order.id(), order);

        CancelOrderRequest request = new CancelOrderRequest(order.id().value(), "");

        // Act + Assert — domain exception, no framework needed
        assertThatThrownBy(() -> interactor.cancel(request))
            .isInstanceOf(DomainException.class)
            .hasMessageContaining("dispatched");
    }
}

// In-memory repository — no JPA
class InMemoryOrderRepository implements OrderRepository {
    private final Map<OrderId, Order> store;

    public void save(Order order) { store.put(order.id(), order); }

    public Optional<Order> findById(OrderId id) {
        return Optional.ofNullable(store.get(id));
    }
}
```

### Pattern: ArchUnit Dependency Rule Enforcement

```java
@AnalyzeClasses(packages = "com.example.shop")
public class CleanArchitectureFitnessTest {

    @ArchTest
    static final ArchRule domain_must_not_depend_on_spring =
        noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAnyPackage("org.springframework..", "javax.persistence..", "jakarta.persistence..");

    @ArchTest
    static final ArchRule domain_must_not_depend_on_application =
        noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAPackage("..application..");

    @ArchTest
    static final ArchRule application_must_not_depend_on_adapters =
        noClasses()
            .that().resideInAPackage("..application..")
            .should().dependOnClassesThat()
            .resideInAnyPackage("..adapter..", "..infrastructure..");

    @ArchTest
    static final ArchRule use_cases_named_correctly =
        classes()
            .that().resideInAPackage("..application.usecase..")
            .and().haveNameMatching(".*UseCase")
            .should().beInterfaces();

    @ArchTest
    static final ArchRule interactors_implement_use_case =
        classes()
            .that().haveNameMatching(".*Interactor")
            .should().implement(resideInAPackage("..application.usecase.."));
}
```

## Anti-Patterns

### Anti-Pattern: Framework Annotation in Domain Entity

```java
// VIOLATION: JPA annotation in domain entity
@Entity  // Framework coupling!
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue
    private Long id;       // Database ID as primary identity

    @Enumerated(STRING)
    private OrderStatus status;

    // Entity is now coupled to JPA — cannot test without JPA context
    // Cannot change DB schema without touching domain model
}
```

The fix: separate `Order` (domain entity) from `OrderJpaEntity` (JPA entity). Map between them in the adapter layer.

### Anti-Pattern: Use Case That Knows About HTTP

```java
// VIOLATION: Use case imports HTTP types
public class GetOrderInteractor {
    public ResponseEntity<OrderDTO> execute(HttpServletRequest req) {  // Wrong!
        String orderId = req.getParameter("id");
        // ...
        return ResponseEntity.ok(dto);  // Use case formatting HTTP response — wrong!
    }
}
```

The use case input is a request model (plain data). The output is a response model (plain data). HTTP conversion happens in the controller and presenter — outer layers. The use case must be callable from an HTTP controller, a message consumer, a CLI, or a test — without any HTTP infrastructure.

### Anti-Pattern: "Clean Architecture" with One Layer

```
com.example.service/
  OrderService.java     // @Service, @Transactional, JPA queries, business logic, HTTP DTOs
```

Naming something "Clean Architecture" without enforcing the dependency rule. This is a service class that does everything — a God Object with Clean Architecture branding. The key test: can you swap the database without touching any business logic? Can you test the business rules without starting Spring?

### Anti-Pattern: Mapping Everywhere (Over-Engineering)

Clean Architecture does not require a separate DTO for every layer in every case. If the data is truly flat and the only consumer is one HTTP endpoint, a single record used as both use case request and API response is acceptable.

The rule is: **never let framework-coupled types leak inward.** Using a record as both request model and API DTO is fine if that record has no framework annotations and no framework dependencies. The violation is when `@JsonProperty`, `@Entity`, or `@RequestBody` appear inside application or domain layer code.

## References

- Martin, Robert C. _Clean Architecture_. Prentice Hall, 2017. Chapters 17–23.
- Martin, Robert C. "The Clean Architecture." blog.cleancoder.com, 2012.
- Cockburn, Alistair. "Hexagonal Architecture." alistair.cockburn.us, 2005.
- Hombergs, Tom. _Get Your Hands Dirty on Clean Architecture_. 2nd ed., 2023.
- ArchUnit: archunit.org — Java architecture fitness functions.
