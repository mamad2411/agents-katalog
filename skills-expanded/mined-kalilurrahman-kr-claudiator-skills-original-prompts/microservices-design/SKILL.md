---
name: microservices-design
description: Design a microservices architecture from a monolith or new requirements. Outputs service boundaries, communication patterns, data ownership, and deployment strategy.
argument-hint: [domain/business requirements, scale expectations]
allowed-tools: Read, Write, Bash
---

# Microservices Architecture Design

Design a microservices architecture that splits responsibilities correctly, communicates efficiently, and can be deployed independently. No buzzword bingo — specific service boundaries, API contracts, data strategies, and operational concerns.

## Process

1. **Identify bounded contexts.** Use Domain-Driven Design to find natural service boundaries.
2. **Define service responsibilities.** Each service owns a specific business capability.
3. **Design communication.** Synchronous (REST/gRPC) for queries, asynchronous (events) for actions.
4. **Plan data ownership.** Each service has its own database, no shared databases.
5. **Handle cross-cutting concerns.** Auth, logging, monitoring, tracing.
6. **Design for failure.** Circuit breakers, retries, fallbacks, timeouts.
7. **Plan deployment.** Containerization, orchestration, CI/CD per service.
8. **Estimate operational overhead.** Each service = separate deploy, logs, metrics, alerts.

## Output Format

### Microservices Architecture: [System Name]

**Domain:** [E-commerce/Banking/Healthcare/etc.]  
**Scale:** [Expected users, requests/sec, data volume]  
**Total Services:** 8  
**Communication:** Synchronous (REST) + Asynchronous (Kafka)  
**Data Strategy:** Database per service  

---

## Service Inventory

| Service | Responsibility | Database | API Type | Dependencies |
|---------|---------------|----------|----------|--------------|
| user-service | User accounts, auth | PostgreSQL | REST | None |
| product-service | Product catalog | PostgreSQL | REST | None |
| order-service | Order management | PostgreSQL | REST | user-service, product-service, payment-service |
| payment-service | Payment processing | PostgreSQL | REST | External: Stripe |
| inventory-service | Stock management | PostgreSQL | REST + Events | product-service |
| notification-service | Email/SMS | MongoDB | Events only | None |
| analytics-service | User behavior tracking | ClickHouse | Events only | None |
| api-gateway | Route requests, auth | None | REST | All services |

---

## Service Details

### user-service
**Bounded Context:** User identity and access management

**Responsibilities:**
- User registration, login, password reset
- Profile management
- JWT token generation
- Role-based access control (RBAC)

**Does NOT Handle:**
- Order history (owned by order-service)
- Payment methods (owned by payment-service)

**API Endpoints:**
- `POST /users` — Register new user
- `POST /auth/login` — Login, get JWT
- `GET /users/{id}` — Get user profile
- `PUT /users/{id}` — Update profile

**Events Published:**
- `user.created` — When new user registers
- `user.deleted` — When user account deleted

**Events Consumed:**
- None

**Database:**
- PostgreSQL
- Tables: `users`, `roles`, `permissions`

**Scaling:**
- Stateless, horizontal scaling
- Redis cache for JWT validation

---

### order-service
**Bounded Context:** Order lifecycle management

**Responsibilities:**
- Create orders
- Track order status (pending → paid → shipped → delivered)
- Order history
- Refund processing

**Does NOT Handle:**
- Payment processing (delegates to payment-service)
- Inventory updates (publishes events, inventory-service handles)

**API Endpoints:**
- `POST /orders` — Create order
- `GET /orders/{id}` — Get order details
- `GET /users/{userId}/orders` — User order history
- `POST /orders/{id}/refund` — Request refund

**Events Published:**
- `order.created` — When order placed (consumed by inventory, notification)
- `order.paid` — When payment confirmed
- `order.shipped` — When shipped
- `order.cancelled` — When cancelled

**Events Consumed:**
- `payment.completed` — From payment-service, triggers order status update
- `inventory.reserved` — From inventory-service, confirms stock

**Database:**
- PostgreSQL
- Tables: `orders`, `order_items`

**Synchronous Calls:**
- `user-service` — Validate user exists
- `product-service` — Fetch product details, prices
- `payment-service` — Initiate payment

**Scaling:**
- Read-heavy (order history), use read replicas
- Write-heavy during flash sales, queue order creation

---

### inventory-service
**Bounded Context:** Stock and inventory management

**Responsibilities:**
- Track product stock levels
- Reserve stock on order creation
- Release stock on order cancellation
- Stock replenishment

**Does NOT Handle:**
- Product catalog (owned by product-service)
- Pricing (owned by product-service)

**API Endpoints:**
- `GET /inventory/{productId}` — Get stock level
- `POST /inventory/reserve` — Reserve stock (internal only)

**Events Published:**
- `inventory.reserved` — Stock successfully reserved
- `inventory.depleted` — Product out of stock

**Events Consumed:**
- `order.created` — Reserve stock
- `order.cancelled` — Release stock
- `order.shipped` — Finalize reservation

**Database:**
- PostgreSQL
- Tables: `inventory`, `reservations`

**Concurrency Handling:**
- Optimistic locking with version field
- If reserve fails, publish `inventory.depleted` event

---

## Communication Patterns

### Synchronous (REST/gRPC)
**Use When:** Immediate response required, query operations

**Example:**
```
order-service → user-service: GET /users/{userId}
  → Response: User details or 404
```

**Patterns:**
- Request timeout: 5s default, 30s max
- Retry: 3 attempts with exponential backoff
- Circuit breaker: Open after 5 failures, half-open after 30s

### Asynchronous (Events)
**Use When:** Fire-and-forget, eventual consistency acceptable

**Example:**
```
order-service publishes: order.created
  → inventory-service consumes: Reserve stock
  → notification-service consumes: Send confirmation email
```

**Event Schema (JSON):**
```json
{
  "event_id": "uuid",
  "event_type": "order.created",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "order_id": "12345",
    "user_id": "uuid",
    "items": [...]
  }
}
```

**Infrastructure:** Kafka
- Topic per event type: `orders.created`, `payments.completed`
- Retention: 7 days
- Consumer groups per service

---

## Data Strategy

### Database Per Service
- Each service has dedicated database
- No direct database access across services
- Data replication via events if needed

### Shared Data Problem
**Problem:** Order service needs user email for notifications

**Wrong:** Query user-service database directly  
**Right:** 
1. Denormalize: Store user_email in orders table (set during creation)
2. Or: Publish event, let notification-service fetch email

### Data Consistency
**Saga Pattern for Distributed Transactions:**

**Create Order Flow:**
1. order-service: Create order (status: pending)
2. payment-service: Charge card
   - If success: Publish `payment.completed`
   - If failure: Publish `payment.failed`
3. order-service: Update order status based on event
4. inventory-service: Reserve stock
   - If success: Publish `inventory.reserved`
   - If failure: Publish `inventory.depleted`, trigger refund

**Compensation:** If payment succeeds but inventory fails:
1. order-service: Update status to `cancelled`
2. order-service: Call payment-service refund API

---

## Cross-Cutting Concerns

### Authentication & Authorization
- **API Gateway** validates JWT on every request
- Gateway injects `user_id` in header: `X-User-Id: <uuid>`
- Services trust the gateway, no re-validation

### Logging
- Structured JSON logs
- Correlation ID in every request header: `X-Request-Id`
- All services log with same correlation ID for traceability

### Monitoring
- Each service exposes `/metrics` endpoint (Prometheus format)
- Key metrics: request rate, error rate, latency (p50, p95, p99)
- Dashboards per service in Grafana

### Distributed Tracing
- OpenTelemetry spans
- Trace every request across services
- Jaeger for visualization

---

## Deployment Strategy

### Containerization
- Each service = Docker container
- Base image: `node:18-alpine` or `python:3.11-slim`
- Multi-stage builds (builder + runner)

### Orchestration
- Kubernetes
- 1 namespace per environment (dev, staging, prod)
- Each service = 1 Deployment + 1 Service + 1 Ingress (if external)

**Example Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
      - name: order-service
        image: order-service:v1.2.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: order-service-secrets
              key: database-url
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
```

### CI/CD Per Service
- Separate pipeline per service
- Trigger: Push to `service-name/main` branch
- Steps: Test → Build → Push image → Deploy to dev → (manual) deploy to prod

---

## Operational Overhead

### Before Microservices (Monolith)
- 1 repository
- 1 deployment pipeline
- 1 database
- 1 log stream
- 1 set of metrics

### After Microservices (8 Services)
- 8 repositories (or monorepo with 8 pipelines)
- 8 deployment pipelines
- 8 databases (+ monitoring, backups)
- 8 log streams
- 8 sets of metrics
- Inter-service communication failures
- Distributed tracing complexity

**Cost:** 3-5x more operational overhead  
**Benefit:** Independent scaling, deployment, teams

**When to Use Microservices:**
- Team > 15 engineers (can split into service teams)
- Different components have different scaling needs
- Need to deploy parts of system independently
- Different tech stacks make sense for different components

**When NOT to Use:**
- Team < 5 engineers (operational overhead too high)
- System can scale vertically
- Domain boundaries unclear

---

## Migration from Monolith

### Strangler Fig Pattern
1. Start with monolith
2. Identify one bounded context (e.g., notifications)
3. Build new microservice
4. Route traffic to new service via API gateway
5. Keep monolith for other features
6. Repeat for next service

**Do NOT:** Rewrite everything at once

---

## Testing Strategy

### Unit Tests
- Each service has own unit tests
- Run in CI on every commit

### Integration Tests
- Test service with real database (Docker Compose for local)
- Mock external service calls

### Contract Tests
- Consumer-driven contracts (Pact)
- Ensure service A's expectations match service B's responses

### End-to-End Tests
- Test full user flows across services
- Run in staging before production deploy

---

## Failure Scenarios

### Service Down
- Circuit breaker opens
- Caller gets cached response or default value
- Alerts fire

### Database Down
- Service becomes read-only (cache only)
- Write requests queued or failed with 503

### Network Partition
- Services in different availability zones
- If inter-service call fails, retry with exponential backoff
- After 3 retries, circuit breaker opens

### Cascading Failures
- Rate limiting per service
- Bulkhead pattern: Separate thread pools for different dependencies

## Rules

- Each service must have a clear bounded context — "user service" is too vague, "user identity and authentication" is specific.
- No shared databases across services — if you need data from another service, call its API or consume its events.
- Synchronous calls for queries (GET), asynchronous events for commands (POST/PUT/DELETE).
- Every service must be independently deployable — no "deploy all services together."
- Circuit breakers are mandatory for all synchronous inter-service calls.
- If team is < 10 people, start with a modular monolith, not microservices.
- Each service needs health check (`/health`) and readiness check (`/ready`) endpoints.
- Use correlation IDs for request tracing across services.
- Event schemas must be versioned — breaking changes require new event type.
- Operational cost: Each service adds 20-30% overhead (deploy, monitor, debug). Make sure benefits justify costs.
