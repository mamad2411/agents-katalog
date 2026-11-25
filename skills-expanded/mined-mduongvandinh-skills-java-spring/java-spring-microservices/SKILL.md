# Java Spring Microservices Skill Set

## Overview

Enterprise-grade microservices architecture with Spring Boot and Spring Cloud.

## When to Use

| Condition | Use This |
|-----------|----------|
| Team > 5 developers | ✅ Microservices |
| Independent scaling needed | ✅ Microservices |
| Multiple deployment cycles | ✅ Microservices |
| Simple CRUD app | ❌ Use java-spring-skills |
| Single team, small project | ❌ Use java-spring-skills |

## Architecture

```
                    ┌─────────────┐
                    │   Gateway   │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │    User    │  │   Order    │  │  Payment   │
    │  Service   │  │  Service   │  │  Service   │
    └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
          │               │               │
          ▼               ▼               ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │  user_db   │  │  order_db  │  │ payment_db │
    └────────────┘  └────────────┘  └────────────┘
          │               │               │
          └───────────────┴───────────────┘
                          │
                    ┌─────▼─────┐
                    │   Kafka   │
                    └─────┬─────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
       ┌────────────┐          ┌────────────┐
       │Notification│          │   Audit    │
       │  Service   │          │  Service   │
       └────────────┘          └────────────┘
```

## Service Types

### 1. Core Service
Business logic with database.
```bash
.\tools\generators\new-service.ps1 -Name "product" -Type "core"
```

### 2. Event Service
Kafka consumer only.
```bash
.\tools\generators\new-service.ps1 -Name "analytics" -Type "event"
```

### 3. Gateway Service
API Gateway with routing.
```bash
# Copy from templates
Copy-Item -Path "tools\generators\templates\gateway-service" -Destination "services\gateway-service" -Recurse
```

### 4. BFF Service
Backend for Frontend aggregator.
```bash
.\tools\generators\new-service.ps1 -Name "web" -Type "bff"
```

## Project Structure

```
java-spring-microservices/
├── services/                    # Microservices
│   ├── user-service/
│   ├── order-service/
│   ├── payment-service/
│   ├── notification-service/
│   └── gateway-service/
│
├── shared/                      # Shared Libraries
│   ├── common-lib/              # DTOs, Exceptions
│   ├── event-lib/               # Domain Events
│   └── api-contracts/           # OpenAPI specs
│
├── infrastructure/
│   ├── docker/                  # Docker Compose
│   └── kubernetes/              # K8s manifests
│
├── tools/generators/            # Service generator
│
└── docs/architecture/           # Architecture docs
```

## Code Conventions

### Package Structure (Core Service)
```
com.company.{service}/
├── domain/           # Entities, Repositories
├── application/      # Use Cases, DTOs
├── infrastructure/   # JPA, Kafka, Feign
└── interfaces/       # Controllers, Event Handlers
```

### Use Case Pattern
```java
@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class CreateOrderUseCase {
    private final OrderRepository repository;
    private final UserServiceClient userClient;
    private final OrderEventPublisher publisher;

    public OrderDto execute(CreateOrderRequest request) {
        // 1. Validate
        var user = userClient.getUserById(request.getUserId());

        // 2. Create
        var order = Order.builder()...build();
        order = repository.save(order);

        // 3. Publish event
        publisher.publishOrderCreated(order);

        return toDto(order);
    }
}
```

### Feign Client
```java
@FeignClient(name = "user-service", fallbackFactory = UserClientFallback.class)
public interface UserServiceClient {
    @GetMapping("/api/users/{id}")
    UserDto getUserById(@PathVariable Long id);
}
```

### Event Publishing
```java
kafkaTemplate.send("order-events", OrderCreatedEvent.builder()
    .orderId(order.getId())
    .userId(order.getUserId())
    .build());
```

## Communication

| Type | Use Case | Technology |
|------|----------|------------|
| Sync | Queries, immediate response | REST/Feign |
| Async | State changes, notifications | Kafka |

## Commands

```bash
# Start infrastructure
cd infrastructure/docker && docker-compose up -d

# Create new service
.\tools\generators\new-service.ps1 -Name "product" -Type "core"

# Build all
mvn clean package

# Deploy to K8s
kubectl apply -k infrastructure/kubernetes/base
```

## Documentation

- [QUICKSTART.md](QUICKSTART.md) - Get started in 10 minutes
- [Architecture Overview](docs/architecture/overview.md)
- [Event Flows](docs/architecture/event-flows.md)
- [API Contracts](shared/api-contracts/)
