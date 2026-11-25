---
name: "microservices-patterns"
description: "Microservices patterns with code: Spring Boot health checks for Kubernetes, OpenTelemetry tracing, versioned Nginx gateway routing, gRPC service definitions, and service-to-service mTLS with Istio. Use when building or reviewing a microservice fleet."
---

# Microservices Patterns

> Named patterns with code for service decomposition, health checks, distributed tracing, API versioning, and inter-service communication.

## Patterns

### Pattern: Service Health Check (Spring Boot + Kubernetes)

```java
// Spring Boot Actuator health indicator
@Component
public class DatabaseHealthIndicator implements HealthIndicator {

    private final DataSource dataSource;

    @Override
    public Health health() {
        try (Connection conn = dataSource.getConnection()) {
            conn.createStatement().executeQuery("SELECT 1");
            return Health.up()
                .withDetail("database", "PostgreSQL")
                .withDetail("status", "connected")
                .build();
        } catch (SQLException e) {
            return Health.down()
                .withDetail("database", "PostgreSQL")
                .withDetail("error", e.getMessage())
                .build();
        }
    }
}
```

```yaml
# application.yml
management:
  endpoint:
    health:
      show-details: when-authorized
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
```

```yaml
# Kubernetes deployment probes
spec:
  containers:
    - name: order-service
      livenessProbe:
        httpGet:
          path: /actuator/health/liveness
          port: 8080
        initialDelaySeconds: 30
        periodSeconds: 10
        failureThreshold: 3
      readinessProbe:
        httpGet:
          path: /actuator/health/readiness
          port: 8080
        initialDelaySeconds: 10
        periodSeconds: 5
        failureThreshold: 3
```

### Pattern: OpenTelemetry Distributed Tracing (Java)

```java
// Auto-instrumentation via Java agent (no code changes for HTTP, JDBC, Kafka)
// java -javaagent:opentelemetry-javaagent.jar \
//      -Dotel.service.name=order-service \
//      -Dotel.exporter.otlp.endpoint=http://otel-collector:4317 \
//      -jar order-service.jar

// Manual span for business operations
@Service
public class OrderService {

    private final Tracer tracer = GlobalOpenTelemetry.getTracer("order-service");

    public Order confirmOrder(String orderId) {
        Span span = tracer.spanBuilder("OrderService.confirmOrder")
            .setAttribute("order.id", orderId)
            .startSpan();

        try (Scope scope = span.makeCurrent()) {
            Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException(orderId));
            order.confirm();
            orderRepository.save(order);
            span.setAttribute("order.status", "CONFIRMED");
            return order;
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }
}
```

### Pattern: API Gateway Routing with Versioning (Nginx)

```nginx
# Nginx routing for versioned microservices
upstream order-service-v1 {
    server order-service-v1:8080;
}

upstream order-service-v2 {
    server order-service-v2:8080;
}

server {
    listen 80;

    # Route by URI version prefix
    location /api/v1/orders {
        proxy_pass http://order-service-v1;
        proxy_set_header X-Request-ID $request_id;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /api/v2/orders {
        proxy_pass http://order-service-v2;
        proxy_set_header X-Request-ID $request_id;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Deprecation header for v1
    location /api/v1/ {
        add_header Sunset "Sat, 31 Dec 2025 23:59:59 GMT";
        add_header Deprecation "true";
        add_header Link '</api/v2/>; rel="successor-version"';
    }
}
```

### Pattern: gRPC Service Definition with Protobuf

```protobuf
// order_service.proto
syntax = "proto3";
package com.example.orders.v1;

service OrderService {
  rpc PlaceOrder(PlaceOrderRequest) returns (PlaceOrderResponse);
  rpc GetOrder(GetOrderRequest) returns (Order);
  rpc ListOrders(ListOrdersRequest) returns (stream Order);  // Server streaming
}

message PlaceOrderRequest {
  string customer_id = 1;
  repeated OrderItem items = 2;
  string idempotency_key = 3;  // Client-generated UUID — prevents duplicate orders
}

message PlaceOrderResponse {
  string order_id = 1;
  string status = 2;
  google.protobuf.Timestamp created_at = 3;
}

message OrderItem {
  string product_id = 1;
  int32 quantity = 2;
  double unit_price_amount = 3;
  string unit_price_currency = 4;
}
```

### Pattern: Service-to-Service Authentication with mTLS (Istio)

```yaml
# Istio PeerAuthentication — require mTLS for all services in namespace
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT  # Reject plaintext — all traffic must use mTLS

---
# AuthorizationPolicy — order-service can only be called by api-gateway and saga-orchestrator
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: order-service-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: order-service
  rules:
    - from:
        - source:
            principals:
              - cluster.local/ns/production/sa/api-gateway
              - cluster.local/ns/production/sa/saga-orchestrator
```

## Anti-Patterns

### Anti-Pattern: Shared Database Between Services

```
OrderService ──┐
               ├──▶ orders_db (shared schema)
InventoryService─┘
```

Both services can read and modify each other's tables. A schema change in orders_db requires coordinating both teams. Neither service can be deployed independently. The database becomes the integration layer — all the coupling, none of the benefits of microservices.

Fix: each service owns its schema. InventoryService subscribes to OrderPlaced events and maintains its own view of order data it needs.

### Anti-Pattern: Synchronous Call Chains

```
Client → API Gateway → OrderService → InventoryService → ProductService → PricingService
```

Total latency = sum of all service latencies. Failure of any service cascades to the client. With 4 services at 99.9% availability: combined availability = 0.999^4 = 99.6%.

Fix: use async events for write-path operations. Use API composition (parallel reads) when multiple services' data is needed for a response.

### Anti-Pattern: Chatty Services (Distributed Monolith)

Services that make dozens of synchronous calls to each other for every user request. A service that needs 10 calls to function is not independent — it is a distributed monolith with worse latency and worse failure modes than a monolith.

Fix: reconsider service boundaries. Services that communicate heavily may belong together. Use event-driven data replication so services have local copies of needed data.

### Anti-Pattern: No Observability Before Going Live

Deploying microservices without distributed tracing, structured logging with correlation IDs, or service-level metrics. The first production incident becomes untraceable across service boundaries.

Fix: instrument with OpenTelemetry before first deployment. Require trace context propagation in code review.

## References

- Newman, Sam. _Building Microservices_, 2nd ed. O'Reilly, 2021.
- Richardson, Chris. _Microservices Patterns_. Manning, 2018.
- OpenTelemetry: opentelemetry.io
- Istio security: istio.io/latest/docs/concepts/security
- Fowler, Martin. "MonolithFirst." martinfowler.com/bliki/MonolithFirst.html, 2015.
