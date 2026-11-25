# {{SERVICE_NAME_PASCAL}} BFF Skill

## Service Type: Backend for Frontend

Aggregates data from multiple services for specific frontend needs.

## Characteristics

- **Aggregation**: Combines data from multiple services
- **Caching**: Caffeine cache for frequently accessed data
- **Parallel calls**: Uses CompletableFuture for concurrent requests
- **Graceful degradation**: Fallbacks when services are down
- **No database**: Stateless aggregator

## Package Structure

```
com.company.{{SERVICE_NAME}}/
├── config/         # Cache, Feign configuration
├── aggregator/     # Business logic for combining data
├── client/         # Feign clients to backend services
└── dto/            # Response DTOs for frontend
```

## Aggregation Pattern

```java
@Cacheable(value = "dashboard", key = "#userId")
@CircuitBreaker(name = "dashboard", fallbackMethod = "fallback")
public DashboardResponse getDashboard(Long userId) {
    // Parallel calls
    var userFuture = CompletableFuture.supplyAsync(() -> userClient.get(userId));
    var ordersFuture = CompletableFuture.supplyAsync(() -> orderClient.get(userId));

    // Wait and combine
    CompletableFuture.allOf(userFuture, ordersFuture).join();

    return DashboardResponse.builder()
        .user(userFuture.join())
        .orders(ordersFuture.join())
        .build();
}
```

## Commands

```bash
mvn spring-boot:run
curl http://localhost:808X/api/dashboard/1
```
