---
name: "monolith-patterns"
description: "Modular monolith patterns with code: public module facades, in-process events between modules, ArchUnit boundary rules, vertical slice organization, and module-scoped integration tests. Use when structuring or untangling a monolith."
---

# Monolith Patterns

> Named patterns with code for modular monolith structure, public module facade, in-process events, ArchUnit boundary enforcement, and vertical slicing.

## Patterns

### Pattern: Public Module Facade (Java)

```java
// modules/ordering/api/OrderFacade.java
// This is the ONLY way other modules interact with Ordering
// All implementation details are hidden behind this interface

public interface OrderFacade {
    OrderId placeOrder(PlaceOrderCommand command);
    Optional<OrderDto> findById(OrderId orderId);
    void cancelOrder(CancelOrderCommand command);
}

// The implementation lives in the private side of the module
@Component
class OrderFacadeImpl implements OrderFacade {

    private final PlaceOrderUseCase placeOrder;
    private final CancelOrderUseCase cancelOrder;
    private final OrderQueryService queryService;

    @Override
    public OrderId placeOrder(PlaceOrderCommand command) {
        return placeOrder.execute(command);
    }

    @Override
    public Optional<OrderDto> findById(OrderId orderId) {
        return queryService.findById(orderId);
    }

    @Override
    public void cancelOrder(CancelOrderCommand command) {
        cancelOrder.execute(command);
    }
}

// modules/payment/application/PaymentService.java
// Payment module talks to Ordering ONLY through OrderFacade — never through domain/repo
@Service
public class PaymentService {

    private final OrderFacade orderFacade;  // Public API — OK

    public void processPaymentForOrder(String orderId, PaymentDetails details) {
        OrderDto order = orderFacade.findById(new OrderId(orderId))
            .orElseThrow(() -> new OrderNotFoundException(orderId));

        // Use order data from the facade DTO — not from Order domain object
        Money amount = order.totalAmount();
        chargeCustomer(order.customerId(), amount, details);
    }
}
```

### Pattern: In-Process Events for Module Decoupling (Spring)

```java
// Ordering module publishes an in-process event — no Kafka needed in monolith
@Component
class PlaceOrderInteractor implements PlaceOrderUseCase {

    private final OrderRepository orderRepo;
    private final ApplicationEventPublisher events;  // Spring's in-process event bus

    @Override
    @Transactional
    public OrderId execute(PlaceOrderCommand command) {
        Order order = Order.create(command.customerId(), command.items());
        orderRepo.save(order);

        // Publish in-process event — synchronous within same transaction
        events.publishEvent(new OrderPlacedEvent(order.id(), order.customerId(), order.total()));

        return order.id();
    }
}

// Inventory module listens — in same transaction (or @Async for decoupling)
@Component
class InventoryEventListener {

    private final InventoryService inventoryService;

    @EventListener
    @Transactional
    public void on(OrderPlacedEvent event) {
        // Called synchronously in same thread/transaction as the publisher
        inventoryService.reserveStock(event.orderId(), event.items());
    }
}

// To convert to microservices later:
// 1. Replace ApplicationEventPublisher with KafkaTemplate
// 2. Move InventoryEventListener to its own service
// 3. The event schema is already defined — no change needed
```

### Pattern: ArchUnit Module Boundary Enforcement (Java)

```java
@AnalyzeClasses(packages = "com.example")
class ModuleArchitectureTest {

    // Modules can only access each other's api packages
    @ArchTest
    static final ArchRule modules_communicate_via_api_only =
        noClasses()
            .that().resideInAPackage("..modules.ordering..")
            .should().dependOnClassesThat()
            .resideInAnyPackage(
                "..modules.catalog.domain..",
                "..modules.catalog.infrastructure..",
                "..modules.payment.domain..",
                "..modules.payment.infrastructure.."
            )
            .as("Modules must communicate only through api packages");

    // Shared kernel is accessible to all
    @ArchTest
    static final ArchRule shared_kernel_is_accessible =
        classes().that().resideInAPackage("..shared..")
            .should().bePublic();

    // Domain objects stay in domain layer
    @ArchTest
    static final ArchRule domain_objects_not_exposed_in_api =
        noClasses()
            .that().resideInAPackage("..modules..api..")
            .should().dependOnClassesThat().resideInAPackage("..modules..domain..")
            .allowEmptyShould(false);
}
```

### Pattern: Vertical Slice Feature Organization (TypeScript/NestJS)

```typescript
// Feature-organized module — all layers for "place order" in one place
// src/modules/orders/place-order/
//   place-order.command.ts     (input DTO)
//   place-order.handler.ts     (use case / application service)
//   place-order.controller.ts  (HTTP adapter)
//   place-order.spec.ts        (unit test)

// place-order.handler.ts
@Injectable()
export class PlaceOrderHandler {
  constructor(
    private readonly orderRepo: OrderRepository,
    private readonly events: EventEmitter2,
  ) {}

  async execute(command: PlaceOrderCommand): Promise<string> {
    const order = Order.create(command.customerId, command.items);
    await this.orderRepo.save(order);
    this.events.emit('order.placed', new OrderPlacedEvent(order.id, order.total));
    return order.id;
  }
}

// place-order.controller.ts
@Controller('orders')
export class PlaceOrderController {
  constructor(private readonly handler: PlaceOrderHandler) {}

  @Post()
  async placeOrder(@Body() dto: PlaceOrderDto): Promise<{ orderId: string }> {
    const command = PlaceOrderCommand.fromDto(dto);
    const orderId = await this.handler.execute(command);
    return { orderId };
  }
}
```

### Pattern: Module-Scoped Integration Test

```java
// Tests the entire ordering module in isolation
// No catalog, no payment, no Kafka — just ordering's Spring context
@SpringBootTest(classes = OrderingModuleConfig.class)
@Transactional
@ActiveProfiles("test")
class PlaceOrderIntegrationTest {

    @Autowired
    private OrderFacade orderFacade;

    @Autowired
    private OrderRepository orderRepo;

    @Test
    void shouldPlaceOrderAndPersistIt() {
        var command = new PlaceOrderCommand(
            new CustomerId("cust-1"),
            List.of(new OrderItem(new ProductId("prod-1"), 2, Money.of(10, "USD")))
        );

        OrderId orderId = orderFacade.placeOrder(command);

        assertThat(orderRepo.findById(orderId)).isPresent();
        assertThat(orderFacade.findById(orderId))
            .map(OrderDto::status)
            .hasValue("DRAFT");
    }
}
```

## Anti-Patterns

### Anti-Pattern: Shared Database Tables Across Modules

```java
// WRONG: CatalogService queries the orders table directly
@Repository
public class CatalogRepository {
    public List<Product> findPopularProducts() {
        return em.createQuery(
            "SELECT p FROM Product p JOIN OrderItem oi ON oi.productId = p.id " +
            "GROUP BY p.id ORDER BY COUNT(oi) DESC"
        ).getResultList();
    }
}
```

The catalog module now depends on the ordering module's database schema. The ordering team cannot rename `OrderItem` columns without breaking the catalog module. Fix: the ordering module publishes `OrderItemPurchased` events; the catalog module maintains its own `product_popularity` table fed by those events.

### Anti-Pattern: God Facade

A module facade with 50 methods covering every possible operation the module could expose. This is not a facade — it is a service layer that leaks the internal data model. Limit facades to the operations other modules actually need (typically 3-8 methods).

### Anti-Pattern: Circular Module Dependencies

Module A calls Module B's facade; Module B calls Module A's facade. Now you cannot deploy one without the other. Break the cycle: identify which module should own the shared concept and have the other depend on it, or introduce a shared kernel for the shared type.

## References

- Grzybek, Kamil. Modular Monolith with DDD. github.com/kgrzybek/modular-monolith-with-ddd.
- Fowler, Martin. "MonolithFirst." martinfowler.com/bliki/MonolithFirst.html, 2015.
- ArchUnit: archunit.org
- Newman, Sam. _Building Microservices_, 2nd ed. O'Reilly, 2021. Chapter 1.
