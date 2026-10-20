# Spring Boot Patterns

## Summary

**One-sentence:** Idiomatic Spring Boot patterns for configuration binding, exception handling, conditional beans, and externalized properties.

**One-paragraph:** Apply Spring Boot's idiomatic patterns — @ConfigurationProperties for type-safe configuration, @ControllerAdvice + ProblemDetail for centralized exception translation, @Conditional bean wiring, and Profiles for environment isolation. The patterns make services portable across environments and surface configuration drift at startup, not at runtime.

**Ефективно для:**

- Сервіси з багатьма env-specific параметрами (dev/staging/prod) — type-safe @ConfigurationProperties.
- Уніфікована обробка помилок REST → ProblemDetail (RFC 7807) через @ControllerAdvice.
- Conditional bean wiring (@ConditionalOnProperty, @ConditionalOnClass) — feature-flag friendly.
- Externalized configuration через application-{profile}.yml + Spring Cloud Config / Vault.

## Applies If (ALL must hold)

- Spring Boot 3.x service with non-trivial configuration surface (>10 properties).
- REST API needs a single uniform error contract (ProblemDetail).
- Multiple deployment environments with different bean wirings.
- Need to expose configuration validation errors at startup (fail fast).

## Skip If (ANY kills it)

- Trivial single-purpose CLI — pattern overhead outweighs benefit.
- Legacy Boot 2.x services — ProblemDetail/binding APIs differ; use Boot 2.x methodology.
- Non-Spring stack (Quarkus, Micronaut) — patterns named differently.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Property surface | list of env vars / config keys | ops |
| Error catalogue | list of business exceptions → HTTP status | API design |
| Profile map | dev/staging/prod yml files | deployment |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot]] | Layered architecture is the substrate these patterns plug into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: configuration-properties-typed, controller-advice-problem-detail, conditional-on-property, validation-on-properties, no-system-getenv | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-properties-record` | sonnet | Templated record generation. |
| `design-error-catalogue` | opus | Mapping business exceptions ↔ HTTP status is decision-heavy. |
| `lint-system-getenv` | haiku | Mechanical grep audit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/MailProperties.java` | Typed @ConfigurationProperties record with Jakarta Bean Validation |
| `templates/GlobalExceptionHandler.java` | @RestControllerAdvice translating business exceptions to ProblemDetail |
| `templates/application-prod.yml` | Profile-specific configuration overlay (prod) |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-spring-boot-patterns.py` | Validate the Boot-patterns artefact against the schema | Pre-commit + CI |

## Related

- [[java-spring-boot]]
- [[java-spring-async]]
- [[clean-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/MailProperties.java`

```java
package com.example.config;

import jakarta.validation.constraints.*;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

@Validated
@ConfigurationProperties(prefix = "app.mail")
public record MailProperties(
        @NotBlank String host,
        @Min(1) @Max(65535) int port,
        @NotBlank String user,
        String password,
        @NotBlank @Email String from,
        @Min(0) int maxRetries,
        @Min(100) int timeoutMs,
        boolean tlsEnabled
) {}
```

### `templates/GlobalExceptionHandler.java`

```java
package com.example.web;

import java.net.URI;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler(OrderNotFoundException.class)
    public ProblemDetail handleOrderNotFound(OrderNotFoundException ex) {
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
        pd.setType(URI.create("https://errors.example.com/order-not-found"));
        pd.setProperty("orderId", ex.getOrderId());
        return pd;
    }

    @ExceptionHandler(MailRejectedException.class)
    public ProblemDetail handleMailRejected(MailRejectedException ex) {
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_GATEWAY, "mail vendor rejected the message");
        pd.setType(URI.create("https://errors.example.com/mail-rejected"));
        return pd;
    }
}
```

### `templates/application-prod.yml`

```yaml
spring:
  profiles:
    active: prod

app:
  mail:
    host: smtp.prod.example.com
    port: 587
    user: ${MAIL_USER}
    password: ${MAIL_PASSWORD}
    from: noreply@example.com
    max-retries: 3
    timeout-ms: 5000
    tls-enabled: true

management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  endpoint:
    health:
      probes:
        enabled: true
```
