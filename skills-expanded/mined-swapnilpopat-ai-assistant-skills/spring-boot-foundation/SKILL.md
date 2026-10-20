---
name: spring-boot-foundation
description: Build a production-ready Spring Boot foundation with configuration, actuator, and operational defaults. Use when starting a new Spring Boot service or standardizing an existing one.
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Spring Boot Foundation

Establish a production-ready Spring Boot 3.x baseline that promotes from laptop to production with minimal rework: deterministic build, externalized config, layered package structure, actuator probes, structured logging, graceful shutdown, and reproducible startup.

## Context

You are starting a new Spring Boot service or hardening an existing one. The output must be operable on Kubernetes, observable, secure-by-default, and trivially testable. Targets the current GA line (Spring Boot 3.5+, Spring Framework 6.2+, Java 21 LTS).

## When to Use This Skill

- Greenfield Spring Boot service.
- Re-platforming a legacy Spring MVC / Boot 2.x app to Boot 3.x (Jakarta EE 10).
- Standardizing a fleet of Spring Boot services on common defaults.
- Triaging a service that "works on my machine" but fails in containers.

## Prerequisites

- Java 21 LTS (or 25 LTS) installed; `JAVA_HOME` set.
- Maven 3.9+ or Gradle 8.x.
- Container runtime (Docker / Podman) for image builds.
- Access to environment-specific config and secret store (env vars, K8s `Secret`, Vault).

## Instructions

### 1. Bootstrap from Spring Initializr

Use https://start.spring.io with the current Boot GA. Default to Maven, Java 21, jar packaging. Add only the starters you actually need now; you can always add more later.

Baseline starters for a typical HTTP service:

- `spring-boot-starter-web`
- `spring-boot-starter-validation`
- `spring-boot-starter-actuator`
- `spring-boot-starter-data-jpa` (only if RDBMS persistence)
- `spring-boot-starter-security` (always for any externally-reachable service)
- `spring-boot-starter-test` (test scope)

Anti-pattern: leaving `devtools`, `h2`, or unused starters in production builds.

### 2. Pin Versions Through the Spring Boot BOM

Use the Spring Boot parent or `dependency-management` plugin so all Spring/Jackson/Hibernate versions stay in lockstep. Never hand-pick a `spring-core` version.

Maven:

```xml
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>3.5.6</version>
  <relativePath/>
</parent>
```

### 3. Adopt a Layered Package Structure

Map packages to responsibilities. Allow only top-down dependencies.

```
com.acme.orders/
  OrdersApplication.java          // @SpringBootApplication
  api/                            // @RestController + DTOs (request/response)
  application/                    // use cases, @Transactional orchestration
  domain/                         // entities (pure), value objects, domain services
  infrastructure/
    persistence/                  // JPA repositories, adapters
    messaging/                    // brokers, outbox
    http/                         // outbound REST clients
  config/                         // @Configuration + @ConfigurationProperties
```

Anti-pattern: package-by-technology only (`controllers/`, `services/`, `repositories/`) - hides feature boundaries and encourages cross-feature coupling.

### 4. Externalize Configuration with Profiles and Type Safety

Defaults in `application.yml`; per-environment overlays in `application-{profile}.yml`. Never hardcode environment values in Java.

```yaml
# application.yml
spring:
  application:
    name: orders
  threads:
    virtual:
      enabled: true              # JDK 21+ blocking workloads
  lifecycle:
    timeout-per-shutdown-phase: 30s
server:
  shutdown: graceful
  forward-headers-strategy: framework   # behind a proxy/ingress
  error:
    include-message: never
    include-stacktrace: never
    include-binding-errors: never
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  endpoint:
    health:
      probes:
        enabled: true
      show-details: never
  observations:
    annotations:
      enabled: true
```

Bind grouped properties with `@ConfigurationProperties` and validate them on startup so misconfiguration fails fast:

```java
@Validated
@ConfigurationProperties(prefix = "orders.payment")
public record PaymentProperties(
    @NotBlank String baseUrl,
    @NotNull @DurationMin(seconds = 1) Duration timeout,
    @Min(1) int maxRetries) {}
```

```java
@Configuration
@EnableConfigurationProperties(PaymentProperties.class)
class PaymentConfig {}
```

Rules: no secrets in source; required values validated; `@Value` only for trivial scalars.

### 5. Expose Operational Endpoints (Actuator)

Minimum set for K8s and SRE dashboards:

- `/actuator/health/liveness` - process is alive (do not include downstream checks).
- `/actuator/health/readiness` - safe to receive traffic (include critical deps).
- `/actuator/info` - build + git metadata (`spring-boot-maven-plugin` `build-info` goal + `git-commit-id-plugin`).
- `/actuator/prometheus` - scraped by Prometheus / OTel collector.

Restrict everything else (`/env`, `/heapdump`, `/loggers`) in non-local profiles. Bind actuator to a separate management port if your platform allows it (`management.server.port`).

### 6. Structured Logging and Correlation by Default

Use Logback with the JSON encoder in non-local profiles. Every request log gets a `traceId`/`spanId` from Micrometer Tracing and a `service.name` field.

```yaml
# application-prod.yml
logging:
  pattern:
    level: "%5p [${spring.application.name},%X{traceId:-},%X{spanId:-}]"
  structured:
    format:
      console: ecs        # Spring Boot 3.4+ built-in JSON formats: ecs, gelf, logstash
```

Add `micrometer-tracing-bridge-otel` + `opentelemetry-exporter-otlp` for distributed traces. See logging-monitoring module for full setup.

### 7. Graceful Shutdown and Container-Friendly Startup

- `server.shutdown=graceful` lets in-flight requests finish.
- `spring.lifecycle.timeout-per-shutdown-phase` aligned to your K8s `terminationGracePeriodSeconds`.
- Liveness probe `initialDelaySeconds` >= cold start P95.
- Health indicators for downstream deps (`HealthIndicator` impls) only on the `readiness` group, never on `liveness` (a flaky DB must not restart your pod).

### 8. Baseline Quality Gates Before First Release

CI must pass:

- Build + dependency lock (Maven `dependency:tree` clean of conflicts; Gradle `dependencyLocking`).
- Smoke test: `@SpringBootTest` that boots the context.
- One controller slice test (`@WebMvcTest`).
- One persistence integration test against Testcontainers (if DB present).
- License + dependency vulnerability scan (e.g., `dependency-check`, OWASP, GitHub Dependabot).

## Common Pitfalls

| Anti-pattern | Why it hurts | Fix |
| --- | --- | --- |
| `spring.jpa.hibernate.ddl-auto=update` in prod | Silent schema drift, data loss risk | Use Flyway/Liquibase; set ddl-auto to `validate` or `none` |
| `management.endpoints.web.exposure.include=*` in prod | Exposes heap dumps, env, threaddump | Whitelist only `health,info,prometheus` |
| `@Value("${...}")` scattered across beans | Hard to validate; fails at runtime | `@ConfigurationProperties` records with `@Validated` |
| Secrets in `application.yml` checked into git | Credential leak | Inject via env / K8s `Secret` / Vault; use Spring Cloud Config or `spring.config.import=optional:file:/etc/secrets/` |
| Logging unstructured text in prod | Hard to index, breaks correlation | JSON encoder + MDC trace IDs |
| No `server.forward-headers-strategy` behind a proxy | Wrong client IP, broken HTTPS detection | Set to `framework` or `native` |
| Liveness probe checks the database | Cascading restarts during DB blip | Liveness = process only; readiness = deps |

## Output Format

When applying this skill, deliver:

1. Dependency baseline table (starter, version source, rationale).
2. Final package layout diagram.
3. `application.yml` + per-profile overlays with annotated decisions.
4. `@ConfigurationProperties` classes for all grouped settings.
5. Actuator exposure policy and probe definitions (with K8s probe YAML if applicable).
6. Logging + tracing setup snippet.
7. Foundation readiness checklist (the eight steps above) signed off.

## Authoritative References

- Spring Boot reference (current): https://docs.spring.io/spring-boot/index.html
- Application properties index: https://docs.spring.io/spring-boot/appendix/application-properties/index.html
- Production-ready features (Actuator): https://docs.spring.io/spring-boot/reference/actuator/index.html
- Externalized configuration: https://docs.spring.io/spring-boot/reference/features/external-config.html
- Graceful shutdown: https://docs.spring.io/spring-boot/reference/web/graceful-shutdown.html
- Structured logging (3.4+): https://docs.spring.io/spring-boot/reference/features/logging.html#features.logging.structured
- Virtual threads: https://docs.spring.io/spring-boot/reference/features/task-execution-and-scheduling.html
- Spring Initializr: https://start.spring.io
- Twelve-Factor App: https://12factor.net/
