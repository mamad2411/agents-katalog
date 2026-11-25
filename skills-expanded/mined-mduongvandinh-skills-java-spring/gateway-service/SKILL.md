# Gateway Service Skill

## Service Type: API Gateway

Central entry point for all API requests.

## Responsibilities

- Request routing to backend services
- Authentication/Authorization (JWT validation)
- Rate limiting (Redis-based)
- Circuit breaker (Resilience4j)
- Request/Response logging
- CORS handling

## Package Structure

```
com.company.gateway/
├── config/         # Security, CORS configuration
├── filter/         # Global filters (logging, auth)
└── fallback/       # Circuit breaker fallbacks
```

## Key Components

### Route Configuration
Routes are defined in `application.yml`:
- Path-based routing
- Circuit breaker per service
- Rate limiting per endpoint

### Global Filters
- **LoggingFilter**: Logs all requests, adds trace ID
- **AuthFilter**: Validates JWT tokens (if needed)

### Fallback Controller
Returns friendly error messages when services are down.

## Adding New Route

```yaml
# application.yml
spring:
  cloud:
    gateway:
      routes:
        - id: new-service
          uri: http://localhost:808X
          predicates:
            - Path=/api/new/**
          filters:
            - name: CircuitBreaker
              args:
                name: newService
                fallbackUri: forward:/fallback/default
```

## Commands

```bash
# Run
mvn spring-boot:run

# Test routes
curl http://localhost:8080/api/users
curl http://localhost:8080/actuator/gateway/routes
```
