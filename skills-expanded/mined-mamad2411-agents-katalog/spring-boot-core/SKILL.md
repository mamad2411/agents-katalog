---
name: spring-boot-core
description: Build, create, configure, structure, and scaffold Spring Boot 3.x microservices with dependency injection (constructor injection), @ConfigurationProperties validation, profile-based configuration (dev/staging/prod), Actuator health checks, custom HealthIndicator beans, Kubernetes liveness/readiness probes, and bean lifecycle management. Fix DI failures (UnsatisfiedDependencyException, NoSuchBeanDefinitionException) and BindException errors, validate environment-specific YAML, and implement secure configuration patterns. Use when creating Spring Boot services, configuring beans, setting up health endpoints, implementing DI patterns, or structuring microservice projects.
license: MIT
metadata:
  version: 1.0.0
  audience: developers
  workflow: backend-development
---

# Spring Boot Core

Build production-ready Spring Boot microservices with proper dependency injection, externalized configuration, and health monitoring.

## What I Do

- Scaffold and structure Spring Boot 3.x microservices (packages, config, modules)
- Fix DI and startup failures (`UnsatisfiedDependencyException`, `NoSuchBeanDefinitionException`)
- Implement externalized configuration (`@ConfigurationProperties`, profiles, secrets)
- Configure Actuator health/info/metrics endpoints safely for production
- Set up Kubernetes liveness and readiness probes

## When to Use Me

- Create, scaffold, or structure a new Spring Boot microservice
- Configure beans with constructor injection
- Set up @ConfigurationProperties with validation
- Implement profile-based configuration (dev, staging, prod)
- Configure Actuator endpoints and health checks
- Troubleshoot bean lifecycle or injection issues

## Context7 Integration

Query Context7 MCP for current Spring Boot documentation:
```
context7_resolve-library-id: "Spring Boot"
context7_query-docs: libraryId="/spring-projects/spring-boot", query="ConfigurationProperties"
```

## Core Patterns

### Constructor Injection

Use constructor injection for all dependencies. Single constructors are auto-wired.

```java
@Service
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentClient paymentClient;

    public OrderService(OrderRepository orderRepository, PaymentClient paymentClient) {
        this.orderRepository = orderRepository;
        this.paymentClient = paymentClient;
    }
}
```

**Benefits:** Immutable fields, explicit dependencies, easier testing, better IDE support.

> **Note on `@Autowired`:** Spring auto-wires a class when there is a single
> constructor, so you do **not** need `@Autowired` on it. Adding it is redundant
> noise. Use `@Autowired` only when a class declares **multiple** constructors
> and you need to mark one as the preferred injection target. Prefer field or
> setter injection only when constructor injection is genuinely impossible
> (e.g., framework constraints or optional collaborators).

### @ConfigurationProperties with Validation

```java
@ConfigurationProperties("app.service")
@Validated
public class ServiceProperties {
    @NotBlank private String name;
    @NotNull private Duration timeout = Duration.ofSeconds(30);
    @Valid private final Security security = new Security();
    // Getters/setters required
}
```

Enable with `@ConfigurationPropertiesScan` on main class.

> **Boot 3.x Note:** Records with constructor binding are supported:
> ```java
> @ConfigurationProperties("app")
> public record AppConfig(@NotBlank String name, @NotNull Duration timeout) {}
> ```

### Profile-Based Configuration

```
src/main/resources/
  application.yml           # Defaults
  application-dev.yml       # Dev overrides  
  application-prod.yml      # Production
```

```yaml
# application-prod.yml
app.service:
  timeout: 10s
  security.api-key: ${API_KEY}
```

Activate: `--spring.profiles.active=prod` or `SPRING_PROFILES_ACTIVE=prod`

### Actuator Health Configuration

```yaml
management:
  endpoints.web.exposure.include: health,info,metrics
  endpoint.health:
    show-details: when-authorized
    probes.enabled: true  # Kubernetes liveness/readiness
```

**Custom health indicator:**
```java
@Component
public class ApiHealthIndicator implements HealthIndicator {
    private final ApiClient client;
    public ApiHealthIndicator(ApiClient client) { this.client = client; }
    
    @Override
    public Health health() {
        return client.isReachable() 
            ? Health.up().build() 
            : Health.down().withDetail("reason", "unreachable").build();
    }
}
```

### Service Directory Structure

```
com.example.service/
  Application.java           # @SpringBootApplication in root
  config/                    # @Configuration classes
  controller/                # @RestController
  service/                   # @Service business logic
  repository/                # @Repository data access
  model/                     # Domain entities
  dto/                       # Request/response objects
  exception/                 # Custom exceptions
  client/                    # External API clients
```

## Production Operations

### Graceful Shutdown

Spring Boot 2.3+ supports graceful shutdown — when the JVM receives `SIGTERM`
(Kubernetes pod eviction, `docker stop`), in-flight requests get a chance to
finish before the context closes.

```yaml
# application.yml
server:
  shutdown: graceful            # 'immediate' (default) | 'graceful'

spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s   # Max wait per SmartLifecycle phase
```

**How it works:**
1. Server stops accepting new requests immediately on `SIGTERM`.
2. In-flight requests continue until completion or `timeout-per-shutdown-phase` elapses.
3. `SmartLifecycle` beans (e.g., Kafka listeners, scheduled tasks) stop in phase order.
4. Context closes; JVM exits.

**Verify readiness drains traffic first:**

```yaml
management:
  endpoint:
    health:
      probes:
        enabled: true
```

Readiness probe flips to `DOWN` when shutdown begins, so the Service / Ingress
stops routing new traffic before the grace timer starts. Always pair
`shutdown: graceful` with readiness probes — otherwise clients see connection
refusals during the grace window.

### Container Image Build (`spring-boot:build-image`)

Spring Boot 3.x includes the Cloud Native Buildpacks integration out of the
box. No Dockerfile required.

**Maven:**
```bash
./mvnw spring-boot:build-image \
  -Dspring-boot.build-image.imageName=us-docker.pkg.dev/PROJECT/REPO/my-app:1.0.0
```

**Gradle:**
```bash
./gradlew bootBuildImage \
  --imageName=us-docker.pkg.dev/PROJECT/REPO/my-app:1.0.0
```

The build creates a layered OCI image with:
- `dependencies` layer (deps that don't change often — high cache reuse)
- `spring-boot-loader` (the launcher)
- `application` (your code — top layer, invalidates least cache)

**Customize the builder or layers** via `pom.xml` / `build.gradle` `build-image`
configuration block (e.g., `builderRegistry`, `network`, `env`, `layers`).
Useful when you need a non-default Java version, a private builder image, or
to expose additional certificates.

## Quick Reference

| Need | Solution |
|------|----------|
| Inject dependency | Constructor injection |
| Multiple constructors | `@Autowired` on preferred |
| Optional dependency | `Optional<T>` parameter |
| External config | `@ConfigurationProperties` + `@Validated` |
| Env-specific | `application-{profile}.yml` |
| Secrets | Environment variables `${VAR_NAME}` |
| Health check | Custom `HealthIndicator` bean |
| K8s probes | `management.endpoint.health.probes.enabled=true` |
| Graceful shutdown | `server.shutdown=graceful` + `spring.lifecycle.timeout-per-shutdown-phase` |
| Build OCI image | `mvn spring-boot:build-image` (no Dockerfile) |

## Common Errors

| Error | Solution |
|-------|----------|
| `NoSuchBeanDefinitionException` | Add @Component; verify package under @SpringBootApplication |
| `UnsatisfiedDependencyException` | Break circular dependency; use @Lazy |
| `BindException` on startup | Check YAML syntax; verify property names |
| Validation not triggering | Add @Validated to @ConfigurationProperties class |
| Actuator 404 | Add to `management.endpoints.web.exposure.include` |

## Anti-Patterns

```java
// AVOID: Field injection
@Autowired private Repository repo;

// AVOID: Hardcoded config  
private static final String URL = "https://api.example.com";

// PREFER: Constructor injection + externalized config
```

## Related Skills

| Skill | Use When |
|-------|----------|
| spring-data | Database access (JPA, MongoDB, Redis) |
| spring-security | Authentication, OAuth2 |
| spring-testing | Unit/integration tests |
| spring-reactive | WebFlux, R2DBC |

## References

| Reference | Load When |
|-----------|-----------|
| [research.md](references/research.md) | Need detailed rationale and advanced patterns |
