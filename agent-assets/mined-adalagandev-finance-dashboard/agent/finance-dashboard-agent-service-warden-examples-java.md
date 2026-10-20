# Service Rules — Java Examples

**Framework basis:** Java 17+, Spring Boot 3.x (Spring Framework 6, `jakarta.*`),
Spring Data JPA. The rules themselves are framework-agnostic — these examples
only show one concrete stack.
**Translation hints:** Quarkus/Micronaut → same shape, different DI annotations;
Jakarta EE → `@Stateless`/`@Transactional` from `jakarta.ejb`/`jakarta.transaction`;
plain Java → wire constructors manually in a composition root.
**Version-sensitive:** Spring Boot 3.x uses `jakarta.*` — Boot 2.x uses
`javax.*` imports; transaction proxies behave the same but annotations import
differently. Records (used for DTOs) require Java 16+.

## Rule 1 — One capability per service
Violation:
```java
@Service
class OrderService {
    void placeOrder(...) {}
    void sendOrderEmail(...) {}     // notification capability
    byte[] renderInvoicePdf(...) {} // document capability
}
```
Correct:
```java
@Service class OrderService { void placeOrder(...) {} }
@Service class NotificationService { ... }
@Service class InvoiceService { ... }
```

## Rule 2 — Inject dependencies
Violation:
```java
@Service
class OrderService {
    @Autowired private OrderRepository repo;          // field injection
    private final PdfClient pdf = new PdfClient();    // self-instantiated
}
```
Correct:
```java
@Service
class OrderService {
    private final OrderRepositoryPort repo;
    private final Clock clock;
    OrderService(OrderRepositoryPort repo, Clock clock) {  // constructor
        this.repo = repo; this.clock = clock;
    }
}
```

## Rule 3 — No transport/persistence in logic
Violation:
```java
public Order placeOrder(HttpServletRequest req) {          // HTTP inside
    jdbcTemplate.update("INSERT INTO orders ...");         // raw SQL inside
}
```
Correct:
```java
public Order placeOrder(PlaceOrderCommand cmd) {
    ...
    return repo.save(order);                               // via port
}
```

## Rule 4 — DTOs at the boundary
Violation:
```java
public OrderEntity placeOrder(OrderRequest body) {   // request DTO in,
    return repo.save(body.toEntity());               // entity out to caller
}
```
Correct:
```java
// controller:
var cmd = new PlaceOrderCommand(body.customerId(), body.lines());
Order order = orderService.placeOrder(cmd);          // domain inside
return OrderResponse.from(order);                    // mapped at the edge
```

## Rule 5 — Service method = transaction boundary
Violation:
```java
@Service
class OrderService {
    public void placeOrder(...) { validate(...); doPlace(...); }
    @Transactional void doPlace(...) { ... }  // self-invocation: proxy
}                                             // skipped, NO transaction runs
```
Correct:
```java
@Service
class OrderService {
    @Transactional                            // on the public entry point
    public void placeOrder(PlaceOrderCommand cmd) {
        repo.save(order);
        stock.reserve(order);                 // both commit or both roll back
    }
}
```

## Rule 6 — Domain exceptions only
Violation:
```java
throw new ResponseStatusException(HttpStatus.CONFLICT, "no stock");
```
Correct:
```java
throw new InsufficientStockException(sku, requested, available);
// @RestControllerAdvice maps it to 409 (exception-warden's territory)
```

## Rule 7 — Invariants in service, syntax at edge
Violation:
```java
public void placeOrder(PlaceOrderCommand cmd) {
    if (!EMAIL.matcher(cmd.email()).matches()) ...  // format re-checked
    // ...customer existence/permission never checked
}
```
Correct:
```java
public void placeOrder(PlaceOrderCommand cmd) {   // @Valid ran at boundary
    var customer = customers.findById(cmd.customerId())
        .orElseThrow(() -> new CustomerNotFoundException(cmd.customerId()));
    if (!customer.mayOrder()) throw new CustomerSuspendedException(customer.id());
}
```

## Rule 8 — Stateless services
Violation:
```java
@Service
class CartService {
    private Cart current;                      // singleton bean shared
    void load(long userId) { current = ...; }  // across threads: data race
}
```
Correct:
```java
@Service
class CartService {
    Receipt checkout(UserId userId) {
        Cart cart = repo.forUser(userId);      // state via params/storage
    }
}
```

## Rule 9 — Isolate side effects and time
Violation:
```java
if (order.createdAt().isBefore(LocalDateTime.now().minus(TTL))) ...
```
Correct:
```java
private final Clock clock;                     // injected java.time.Clock
if (order.createdAt().isBefore(LocalDateTime.now(clock).minus(TTL))) ...
// tests use Clock.fixed(...)
```

## Rule 10 — CQS; orchestrate, don't accumulate
Violation:
```java
public Order getOrder(OrderId id) {
    var order = repo.get(id);
    order.setLastViewed(now());                // query mutates state
    repo.save(order);
    return order;
}
```
Correct:
```java
public Order getOrder(OrderId id) { return repo.get(id); }   // query
public void recordView(OrderId id) { ... }                    // command
```
