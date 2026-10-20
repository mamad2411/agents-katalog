# Java Spring (Layered Architecture)

## Summary

**One-sentence:** Spring Boot 3.x layered architecture — thin @RestController → @Transactional @Service → narrow repository; record DTOs + Bean Validation; @Async via named executor; MapStruct DTOs.

**One-paragraph:** Spring Boot misuse — `@Transactional` on controllers, services returning JPA entities, `findAll()` without `Pageable`, `@Async` invoked via `this.foo()` (self-invocation), custom error envelopes — produces hard-to-reason-about apps. This methodology pins five rules: controllers are thin (no `@Transactional`, no repo access, no business logic); services own `@Transactional` boundaries; DTOs are records with Bean Validation; list endpoints accept `Pageable` and return `Page<T>`; `@Async` lives in a separate bean with a named executor. Output: layered feature spec (Controller + Service + DTOs + AsyncConfig) conforming to `02-output-contract.xml`.

**Ефективно для:**

- Spring Boot 3.x REST APIs with non-trivial domain.
- Async workflows (`@Async`) needing named, sized executors.
- DTO mapping via MapStruct with Lombok ordering pinned.
- Bean Validation + RFC 7807 `ProblemDetail` error model.
- Pageable list endpoints with deterministic ordering.

## Applies If (ALL must hold)

- Spring Boot 3.x + Java 17+ project.
- Layered architecture (Controller/Service/Repository) is the chosen style.
- MapStruct + Lombok are accepted in the build.
- The team agrees no `@Transactional` outside services.

## Skip If (ANY kills it)

- Reactive stack (WebFlux) — different patterns; apply WebFlux methodology.
- Plain SE / non-Spring app — apply the relevant framework's methodology.
- Single-package CRUD with no domain — Active Record is enough.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec | Markdown | spec |
| Existing service layout | Maven/Gradle module | repo |
| Bean Validation rules | spec | spec |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-jpa-hibernate]] | Repository + transactional service patterns this layer consumes. |
| [[java-junit-testing]] | Test conventions for the layered tests. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: thin-controller, transactional-on-service-only, record-dtos-with-validation, pageable-list-endpoints, async-via-named-executor | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for layered feature spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: transactional-on-controller, async-self-invocation, service-returns-entity, custom-error-envelope | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on layer + concern → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-feature-package` | sonnet | Layered judgment. |
| `write-controller-service` | sonnet | Scaffolding within rules. |
| `wire-async-executor` | sonnet | Named bean + properties. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Controller.java` | Thin @RestController skeleton |
| `templates/Service.java` | @Transactional service skeleton |
| `templates/AsyncConfig.java` | Named ThreadPoolTaskExecutor + @Async |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-spring.py` | Validate layered feature spec | Pre-commit on spec artefact |

## Related

- [[java-jpa-hibernate]]
- [[java-junit-testing]]
- [[csharp-dotnet]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (layer, async need, error contract) to a rule from `01-core-rules.xml`. Use it whenever adding a new feature to a Spring Boot app.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/Controller.java`

```java
package faion.web.orders;

import faion.app.orders.OrdersService;
import jakarta.validation.Valid;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/orders")
public class OrdersController {

    private final OrdersService service;

    public OrdersController(OrdersService service) {
        this.service = service;
    }

    @GetMapping("/{id}")
    public ResponseEntity<OrderResponse> getById(@PathVariable UUID id) {
        return ResponseEntity.ok(service.getById(id));
    }

    @GetMapping
    public Page<OrderSummary> list(Pageable pageable) {
        return service.list(pageable);
    }

    @PostMapping
    public ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest req) {
        OrderResponse created = service.create(req);
        return ResponseEntity.created(java.net.URI.create("/api/orders/" + created.id())).body(created);
    }
}
```

### `templates/Service.java`

```java
package faion.app.orders;

import faion.infra.orders.OrderRepository;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.UUID;

@Service
@Transactional(readOnly = true)
public class OrdersService {

    private final OrderRepository repository;

    public OrdersService(OrderRepository repository) {
        this.repository = repository;
    }

    public OrderResponse getById(UUID id) {
        return repository.findByIdWithItems(id)
            .map(OrderResponse::from)
            .orElseThrow(() -> new OrderNotFoundException(id));
    }

    public Page<OrderSummary> list(Pageable pageable) {
        return repository.findAllSummaries(pageable);
    }

    @Transactional
    public OrderResponse create(CreateOrderRequest req) {
        var saved = repository.save(new faion.domain.orders.Order(req.customerName()));
        return OrderResponse.from(saved);
    }
}

record CreateOrderRequest(
    @NotBlank @Size(max = 200) String customerName,
    @Positive BigDecimal total
) {}

record OrderResponse(UUID id, String customerName, BigDecimal total) {
    static OrderResponse from(faion.domain.orders.Order o) {
        return new OrderResponse(o.getId(), o.getCustomerName(), o.getTotal());
    }
}

record OrderSummary(UUID id, String customerName, BigDecimal total) {}

class OrderNotFoundException extends RuntimeException {
    OrderNotFoundException(UUID id) { super("order not found: " + id); }
}
```

### `templates/AsyncConfig.java`

```java
package faion.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.stereotype.Service;

import java.util.concurrent.Executor;

@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean(name = "emailExecutor")
    public Executor emailExecutor(
        @Value("${faion.email.pool.core-size:4}") int core,
        @Value("${faion.email.pool.max-size:16}") int max,
        @Value("${faion.email.pool.queue-capacity:1000}") int queue
    ) {
        ThreadPoolTaskExecutor exec = new ThreadPoolTaskExecutor();
        exec.setCorePoolSize(core);
        exec.setMaxPoolSize(max);
        exec.setQueueCapacity(queue);
        exec.setThreadNamePrefix("email-");
        exec.initialize();
        return exec;
    }
}

@Service
class EmailSender {

    @Async("emailExecutor")
    public void sendOrderConfirmation(String to, String orderId) {
        // call SMTP / SES; if it throws, the executor logs.
    }
}
```
