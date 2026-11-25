---
name: "saga-patterns"
description: "Saga patterns with code: an orchestrated saga in Temporal, a choreographed saga with compensating Kafka events, the semantic lock countermeasure, and idempotent compensating transactions. Use when a business process spans several services."
---

# Saga Patterns

> Named patterns with code for orchestrated saga with Temporal, choreography with compensating events, saga state machine, semantic lock countermeasure, and idempotent compensating transactions.

## Patterns

### Pattern: Orchestrated Saga with Temporal (Java)

```java
// Workflow interface — the saga contract
@WorkflowInterface
public interface OrderFulfillmentWorkflow {
    @WorkflowMethod
    OrderResult fulfillOrder(FulfillOrderRequest request);
}

// Activities — each activity is one saga step (one local transaction)
@ActivityInterface
public interface PaymentActivities {
    String authorizePayment(String customerId, Money amount);
    void voidAuthorization(String authId);  // Compensation
    void capturePayment(String authId);
}

@ActivityInterface
public interface InventoryActivities {
    void reserveStock(String orderId, List<OrderItem> items);
    void releaseReservation(String orderId);  // Compensation
}

// Workflow implementation — durable execution (survives process crashes)
@WorkflowImpl
public class OrderFulfillmentWorkflowImpl implements OrderFulfillmentWorkflow {

    private final PaymentActivities payment = Workflow.newActivityStub(
        PaymentActivities.class,
        ActivityOptions.newBuilder()
            .setStartToCloseTimeout(Duration.ofSeconds(30))
            .setRetryOptions(RetryOptions.newBuilder()
                .setMaximumAttempts(3)
                .setInitialInterval(Duration.ofSeconds(1))
                .build())
            .build()
    );

    private final InventoryActivities inventory = Workflow.newActivityStub(
        InventoryActivities.class,
        ActivityOptions.newBuilder().setStartToCloseTimeout(Duration.ofSeconds(10)).build()
    );

    @Override
    public OrderResult fulfillOrder(FulfillOrderRequest request) {
        String authId = null;
        boolean stockReserved = false;

        try {
            // Step 1
            authId = payment.authorizePayment(request.customerId(), request.amount());
            // Step 2
            inventory.reserveStock(request.orderId(), request.items());
            stockReserved = true;
            // Step 3 — capture payment (charge customer)
            payment.capturePayment(authId);

            return OrderResult.success(request.orderId());

        } catch (ActivityFailure e) {
            // Compensate in reverse order
            if (stockReserved) inventory.releaseReservation(request.orderId());
            if (authId != null) payment.voidAuthorization(authId);
            return OrderResult.failed(e.getMessage());
        }
    }
}

// Start workflow from application code
WorkflowOptions options = WorkflowOptions.newBuilder()
    .setTaskQueue("order-fulfillment")
    .setWorkflowId("order-" + orderId)  // Idempotency: same ID = idempotent start
    .setWorkflowRunTimeout(Duration.ofMinutes(10))
    .build();

OrderFulfillmentWorkflow workflow = client.newWorkflowStub(OrderFulfillmentWorkflow.class, options);
OrderResult result = workflow.fulfillOrder(new FulfillOrderRequest(orderId, customerId, items, total));
```

### Pattern: Choreography Saga with Compensating Events (Kafka)

```java
// OrderService publishes event — starts the saga
@Service
@Transactional
public class OrderService {

    public void placeOrder(PlaceOrderCommand cmd) {
        Order order = Order.create(cmd);
        order.setStatus(OrderStatus.PENDING_PAYMENT);  // Semantic lock: visible to other sagas
        orderRepo.save(order);
        eventPublisher.publish("orders", new OrderCreatedEvent(order.id(), order.customerId(), order.total()));
    }

    // Compensation: payment service failed — cancel the order
    @KafkaListener(topics = "payment-events")
    public void onPaymentEvent(PaymentEvent event) {
        Order order = orderRepo.findById(event.orderId()).orElseThrow();
        if (event instanceof PaymentFailedEvent) {
            order.cancel("Payment failed");
            orderRepo.save(order);
            // No further compensation needed — order was never confirmed
        } else if (event instanceof PaymentAuthorizedEvent) {
            order.setStatus(OrderStatus.PAYMENT_AUTHORIZED);
            orderRepo.save(order);
            // Inventory saga step starts (inventory listens to OrderCreatedEvent)
        }
    }
}

// PaymentService — listens to order events
@KafkaListener(topics = "orders")
@Service
public class PaymentSagaParticipant {

    public void onOrderCreated(OrderCreatedEvent event) {
        try {
            String authId = paymentGateway.authorize(event.customerId(), event.total());
            eventPublisher.publish("payment-events",
                new PaymentAuthorizedEvent(event.orderId(), authId));
        } catch (PaymentException e) {
            eventPublisher.publish("payment-events",
                new PaymentFailedEvent(event.orderId(), e.getMessage()));
        }
    }
}
```

### Pattern: Semantic Lock Countermeasure (Java)

```java
// Prevent other operations from acting on data in the middle of a saga
@Entity
public class Order {
    @Enumerated(EnumType.STRING)
    private OrderStatus status;  // PENDING_PAYMENT = "semantic lock" — saga in progress

    public void beginFulfillment() {
        if (this.status != OrderStatus.CONFIRMED) {
            throw new DomainException("Cannot begin fulfillment — order not confirmed");
        }
        this.status = OrderStatus.FULFILLMENT_IN_PROGRESS;  // Lock acquired
    }

    public void completeFulfillment() {
        this.status = OrderStatus.FULFILLED;  // Lock released
    }

    public void cancelFulfillment(String reason) {
        this.status = OrderStatus.CONFIRMED;  // Lock released, back to pre-fulfillment state
        this.cancellationReason = reason;
    }

    public boolean isLocked() {
        return this.status == OrderStatus.FULFILLMENT_IN_PROGRESS
            || this.status == OrderStatus.PENDING_PAYMENT;
    }
}

// Other services check the lock
public void updateShippingAddress(UpdateAddressCommand cmd) {
    Order order = orderRepo.findById(cmd.orderId()).orElseThrow();
    if (order.isLocked()) {
        throw new DomainException("Cannot update order while fulfillment is in progress");
    }
    order.updateShippingAddress(cmd.address());
    orderRepo.save(order);
}
```

### Pattern: Idempotent Compensating Transaction

```java
// Compensation must be safe to call multiple times
// Temporal retries activities on failure — compensation may be called 2+ times

@ActivityImpl(taskQueues = "order-fulfillment")
public class PaymentActivitiesImpl implements PaymentActivities {

    @Override
    public void voidAuthorization(String authId) {
        // Idempotent: check if already voided before calling gateway
        PaymentRecord record = paymentRepo.findByAuthId(authId)
            .orElseThrow(() -> new ActivityFailure("Authorization not found: " + authId));

        if (record.getStatus() == PaymentStatus.VOIDED) {
            log.info("Authorization {} already voided — skipping", authId);
            return;  // Already compensated — safe to return
        }

        paymentGateway.void(authId);
        record.setStatus(PaymentStatus.VOIDED);
        paymentRepo.save(record);
    }
}
```

## Anti-Patterns

### Anti-Pattern: Saga Without Compensating Transactions

Designing the happy path and assuming the failure path can be handled "later." When step 3 of a 5-step saga fails in production, there is no compensation for steps 1 and 2. Data is left in a partial state. Manual cleanup required.

Every saga step that modifies state must have a compensation defined before the saga is deployed.

### Anti-Pattern: Long Choreography Chains

Saga: OrderCreated → PaymentAuthorized → StockReserved → ShipmentScheduled → ShipmentDispatched → OrderDelivered → LoyaltyPointsAwarded (7 steps, 7 services).

When LoyaltyPointsAwarded fails, what compensates? Which service knows the saga state? Nobody can see the full process. Debugging requires tracing events across 7 Kafka topics.

Fix: use orchestration (Temporal) for sagas longer than 2-3 steps. The workflow definition is the single source of truth for the process.

### Anti-Pattern: Non-Idempotent Compensations

A compensation that fails halfway through and leaves the system in a worse state than the original failure. Example: "cancel order" compensation deletes the order record — but if called twice, the second call fails with "order not found" and the orchestrator marks the compensation as failed, leaving the saga stuck.

Fix: compensations must be idempotent. "Cancel order" should check if order is already cancelled and return success if so.

### Anti-Pattern: Saga for Simple Database Operations

Using a saga for an operation that could be a single local transaction. If payment and order are in the same service and database, use a local transaction — not a saga. Sagas are for operations that span multiple services or multiple databases.

## References

- Richardson, Chris. _Microservices Patterns_. Manning, 2018. Chapter 4.
- Garcia-Molina, Hector, and Kenneth Salem. "Sagas." ACM SIGMOD 1987.
- Temporal.io: docs.temporal.io/workflows
- Richardson, Chris. microservices.io/patterns/data/saga.html
