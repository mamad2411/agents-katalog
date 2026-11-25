# Eval: Java Persistence Performance

## Prompt

This order list endpoint is slow under load. Diagnose the persistence issue and fix it with the smallest safe change. Add or update a test that would catch an N+1 regression.

```java
@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {

    private final OrderRepository orderRepository;

    public OrderController(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    @GetMapping
    public List<OrderResponse> list(@RequestParam UUID customerId) {
        return orderRepository.findByCustomerId(customerId).stream()
            .map(order -> new OrderResponse(
                order.getId(),
                order.getStatus(),
                order.getLines().size(),
                order.getLines().stream().map(Line::getSku).toList()))
            .toList();
    }
}
```

## Expected Agent Behavior

- Identifies lazy-loading N+1 when accessing `order.getLines()` per order
- Proposes fetch join, entity graph, or projection instead of loading full graphs blindly
- Keeps pagination or warns if the endpoint returns unbounded lists
- Adds an integration test or documents query-count verification approach
- Summarizes root cause, fix, and verification command

## Failure Signals

- Enables Open Session In View as the only fix without explanation
- Adds `@Transactional` on the controller without addressing fetch strategy
- Eager-fetches all associations globally
- Suggests cache as the first fix without measuring query behavior
