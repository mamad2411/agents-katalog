# Spring Boot Layered Architecture

## Summary

**One-sentence:** Structure Spring Boot applications with clean layered Controller → Service → Repository architecture (JPA, Bean Validation, Actuator, declarative @Transactional).

**One-paragraph:** Build enterprise Java services with the standard layered Controller → Service → Repository stack using Spring Data JPA, Bean Validation (Jakarta), dependency injection, declarative transactions, and Actuator-based observability. The patterns prevent subtle runtime bugs like lazy-load exceptions, N+1 queries, and proxy-based annotation failures.

**Ефективно для:**

- Зрілі Spring Boot 3.x монолітні API з REST-контролерами та реляційною БД.
- Greenfield REST-сервіси з валідацією, transactional service-layer та health-checks.
- Brownfield рефакторинг fat-controllers → service-layer з @Transactional на service-методах.
- Стандартизація валідації (@Valid + @ControllerAdvice + ProblemDetail) у багатомодульних проєктах.

## Applies If (ALL must hold)

- Spring Boot 3.x service exposing REST endpoints backed by a relational DB via JPA.
- Team agreed on Controller → Service → Repository layering (no DDD/Hexagonal/CQRS).
- Need consistent validation + @Transactional placement across modules.
- Production observability via Spring Boot Actuator + Micrometer is mandatory.

## Skip If (ANY kills it)

- Reactive stack (WebFlux + R2DBC) — different concurrency model; this methodology assumes blocking servlet stack.
- Microservice with DDD/Hexagonal architecture — use ddd-aggregates / clean-architecture instead.
- Console-only batch app — Spring Batch methodology fits better.
- Boot 3.2+ with virtual threads aggressively replacing thread-per-request — pool sizing rules differ.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain entity | Java class + DB table | domain model |
| API contract | OpenAPI / endpoint list | product/BA |
| Datasource config | application.yml spring.datasource.* | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot-patterns]] | Bean wiring + DI conventions assumed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: service-layer-transactions, constructor-injection-only, dto-not-entity, validation-on-controller, actuator-health-required | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-layer-stack` | sonnet | Templated generation of Controller + Service + Repository + DTO. |
| `decide-tx-boundary` | opus | Transaction propagation choices are decision-heavy. |
| `lint-layering` | haiku | Mechanical audit (spring-boot-layering-audit.sh). |

## Templates

| File | Purpose |
|------|---------|
| `templates/OrderController.java` | REST controller skeleton with @Valid + ResponseEntity + no @Transactional |
| `templates/OrderService.java` | Service with @Transactional placement + entity↔DTO mapping |
| `templates/OrderRepository.java` | Spring Data JPA interface with @EntityGraph |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-spring-boot.py` | Validate the Spring Boot layer-stack artefact against the schema | Pre-commit + CI |
| `scripts/spring-boot-layering-audit.sh` | Lint @Transactional on controllers, entities crossing controller boundary, field injection | CI on every PR touching @RestController / @Service |

## Related

- [[java-spring-boot-patterns]]
- [[java-spring-async]]
- [[clean-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/OrderController.java`

```java
package com.example.order.web;

import jakarta.validation.Valid;
import java.net.URI;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.example.order.dto.OrderRequest;
import com.example.order.dto.OrderResponse;
import com.example.order.service.OrderService;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService service;

    public OrderController(OrderService service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<OrderResponse> create(@Valid @RequestBody OrderRequest req) {
        OrderResponse out = service.create(req);
        return ResponseEntity.created(URI.create("/orders/" + out.id())).body(out);
    }

    @GetMapping("/{id}")
    public OrderResponse get(@PathVariable String id) {
        return service.get(id);
    }
}
```

### `templates/OrderService.java`

```java
package com.example.order.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.order.domain.Order;
import com.example.order.domain.OrderRepository;
import com.example.order.dto.OrderRequest;
import com.example.order.dto.OrderResponse;

@Service
public class OrderService {

    private final OrderRepository repo;

    public OrderService(OrderRepository repo) {
        this.repo = repo;
    }

    @Transactional
    public OrderResponse create(OrderRequest req) {
        Order order = new Order(req.customer(), req.items());
        repo.save(order);
        return OrderResponse.from(order);
    }

    @Transactional(readOnly = true)
    public OrderResponse get(String id) {
        return repo.findWithItemsById(id)
                   .map(OrderResponse::from)
                   .orElseThrow(() -> new OrderNotFoundException(id));
    }
}
```

### `templates/OrderRepository.java`

```java
package com.example.order.domain;

import java.util.Optional;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderRepository extends JpaRepository<Order, String> {

    @EntityGraph(attributePaths = {"items"})
    Optional<Order> findWithItemsById(String id);
}
```
