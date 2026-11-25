---
name: microservice-spec
description: Write complete technical specifications for microservices including architecture, domain model, API contracts, database schema, inter-service communication, and deployment configuration. Use this skill whenever the user wants to design a microservice, write a technical spec, plan a new service, define service boundaries, or says things like "spec out a microservice for X", "design a service for X", "write the technical spec for X", "how should I structure this microservice", "define the domain model for X". Always use this skill for any microservice design or specification task.
---

# Microservice Specification Skill

Produce complete, actionable technical specifications for Spring Boot microservices following Domain-Driven Design and modern microservice patterns.

## Specification Template

Use this structure for every microservice spec:

---

### 1. Service Overview

```markdown
## Service: [ServiceName]-service

**Responsibility**: [One sentence — what does this service own?]
**Domain**: [DDD Bounded Context name]
**Owner Team**: [Team name]
**Port**: [e.g., 8081]
**Base URL**: /api/v1/[resource]
```

---

### 2. Domain Model

Define the **Aggregates**, **Entities**, and **Value Objects**:

```markdown
### Aggregates
- **[AggregateRoot]**: [Root entity that owns the consistency boundary]
  - Entities: [child entities within the aggregate]
  - Value Objects: [immutable data structures — Money, Address, Email]

### Domain Events
- [EventName]: Published when [trigger]
  - Payload: { field1, field2, ... }
```

Example:
```markdown
### Aggregates
- **Order** (root): owns all order lifecycle
  - Entities: OrderItem, ShippingAddress
  - Value Objects: Money(amount, currency), DeliveryWindow

### Domain Events
- OrderPlaced: Published when an order transitions to PENDING
- OrderCancelled: Published when order is cancelled
```

---

### 3. Database Schema

```sql
-- Primary table
CREATE TABLE orders (
    id          BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    status      VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    total       NUMERIC(10,2) NOT NULL,
    currency    VARCHAR(3) NOT NULL DEFAULT 'EUR',
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    version     BIGINT NOT NULL DEFAULT 0  -- optimistic locking
);

-- Constraints
ALTER TABLE orders ADD CONSTRAINT chk_order_status 
    CHECK (status IN ('PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED'));

-- Indexes
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);
```

---

### 4. API Contract

List all endpoints with full request/response:

```markdown
### Endpoints

#### POST /api/v1/orders
Create a new order.

**Request:**
```json
{
  "customerId": 42,
  "items": [
    { "productId": 1, "quantity": 2, "unitPrice": 29.99 }
  ]
}
```

**Response 201:**
```json
{
  "id": 1001,
  "status": "PENDING",
  "total": 59.98,
  "items": [...],
  "createdAt": "2024-01-15T10:30:00Z"
}
```

**Errors:**
- 400: Validation error (empty items, negative quantity)
- 404: Customer not found
- 409: Product out of stock
```

---

### 5. Inter-Service Communication

```markdown
### Synchronous (REST)
| Calls | Method | URL | Purpose |
|-------|--------|-----|---------|
| → customer-service | GET | /api/v1/customers/{id} | Validate customer exists |
| → inventory-service | POST | /api/v1/inventory/reserve | Reserve stock |

### Asynchronous (Events)
| Direction | Topic | Event | Trigger |
|-----------|-------|-------|---------|
| PUBLISH | orders.events | OrderPlaced | On order creation |
| PUBLISH | orders.events | OrderCancelled | On cancellation |
| SUBSCRIBE | payments.events | PaymentConfirmed | Update order status |
```

Kafka topic config:
```java
@Bean
public NewTopic ordersTopic() {
    return TopicBuilder.name("orders.events")
        .partitions(3)
        .replicas(2)
        .build();
}
```

---

### 6. Configuration

```yaml
# application.yml
server:
  port: 8081

spring:
  application:
    name: order-service
  datasource:
    url: jdbc:postgresql://localhost:5432/orders_db
  jpa:
    hibernate:
      ddl-auto: validate  # Use Flyway, not auto DDL
    open-in-view: false

# Feign clients
feign:
  client:
    config:
      customer-service:
        connectTimeout: 2000
        readTimeout: 5000

# Resilience4j circuit breaker
resilience4j:
  circuitbreaker:
    instances:
      customer-service:
        failureRateThreshold: 50
        waitDurationInOpenState: 10s
        slidingWindowSize: 10
```

---

### 7. Service Dependencies

```markdown
### Required Services
- **customer-service**: customer validation
- **inventory-service**: stock reservation
- **PostgreSQL**: primary data store
- **Kafka**: event publishing/consuming

### Optional / Graceful Degradation
- **notification-service**: email/SMS — failure should NOT fail the order
```

---

### 8. Error Handling Strategy

```markdown
### Synchronous Failures
- customer-service unavailable → 503 with retry headers
- inventory-service unavailable → 503, use circuit breaker

### Compensation / Saga Pattern
If order creation fails after inventory reservation:
1. Publish `InventoryReleaseRequested` event
2. inventory-service consumes and releases reservation
→ Use Outbox pattern to guarantee event delivery
```

---

### 9. Non-Functional Requirements

```markdown
| Requirement | Target |
|-------------|--------|
| Response time (p99) | < 200ms |
| Throughput | 500 req/s |
| Availability | 99.9% |
| Data retention | 3 years |
| Horizontal scaling | Yes (stateless) |
```

---

## DDD Service Boundary Heuristics

Use these rules to define correct service boundaries:

- Each service owns **one aggregate or closely related aggregates**
- Services do **not share databases**
- A service is a **consistency boundary** — everything inside is transactional together
- If two services always change together, they might be one service
- If a service needs data from another, use **async events** or **query projections**, not shared tables

## Technology Recommendations per Pattern

| Need | Recommended Approach |
|------|---------------------|
| Sync inter-service calls | Spring Cloud OpenFeign + Resilience4j |
| Async messaging | Spring Kafka or Spring AMQP (RabbitMQ) |
| Service discovery | Spring Cloud Eureka or Kubernetes DNS |
| Config management | Spring Cloud Config or Kubernetes ConfigMap |
| Distributed tracing | Micrometer + Zipkin/Jaeger |
| DB migrations | Flyway |
| API gateway | Spring Cloud Gateway |
