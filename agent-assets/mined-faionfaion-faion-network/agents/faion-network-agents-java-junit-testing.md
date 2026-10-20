# JUnit Testing for Spring Boot

## Summary

**One-sentence:** JUnit 5 + Spring Boot test conventions — @WebMvcTest for controllers, @ExtendWith(MockitoExtension) for services, @DataJpaTest for slices, Testcontainers for integration.

**One-paragraph:** Spring Boot test misuse — `@SpringBootTest` everywhere, H2 instead of real DB, manual collaborator construction, no `@ParameterizedTest` — produces slow, flaky CI. This methodology pins five rules: controller tests use `@WebMvcTest` + mock service, service unit tests use `@ExtendWith(MockitoExtension.class)`, repository tests use `@DataJpaTest`, integration tests use `@SpringBootTest(webEnvironment=RANDOM_PORT) + @Testcontainers` with real DB, parametric tests use `@ParameterizedTest`. Output: test-class spec conforming to `02-output-contract.xml`.

**Ефективно для:**

- Layered Spring Boot test suite with right-sized slices.
- Repository tests that catch N+1 + lazy bugs.
- Integration tests that use the actual production DB engine.
- Parametric boundary tests via `@CsvSource`/`@ValueSource`.
- Coverage thresholds enforced in CI via JaCoCo.

## Applies If (ALL must hold)

- Spring Boot 3.x with JUnit Jupiter.
- Mockito 5+, AssertJ, Testcontainers available.
- Postgres (or other real engine) is the production DB.
- CI can run docker (for Testcontainers).

## Skip If (ANY kills it)

- Reactive stack — `@WebFluxTest` patterns differ.
- Plain Java SE without Spring Boot — apply the relevant framework's methodology.
- DB-less microservice — repository slice + Testcontainers irrelevant.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Unit-under-test | Java source | repo |
| Test plan | Markdown | spec |
| Testcontainers + Docker | infra | CI config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-spring]] | Controller/service layout being tested. |
| [[java-jpa-hibernate]] | Repository slice tests target these patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: webmvctest-for-controllers, mockitoextension-for-services, datajpatest-for-repo-slices, testcontainers-for-integration, parameterizedtest-for-boundaries | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for test-class spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: springboottest-for-everything, h2-for-relational, manual-collaborator-construction, void-async-test | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on test target → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-test-scope` | sonnet | Unit / slice / integration judgment. |
| `write-test-class` | haiku | Mechanical scaffolding once scope chosen. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ControllerTests.java` | @WebMvcTest skeleton |
| `templates/ServiceTests.java` | Mockito service test skeleton |
| `templates/RepositoryTests.java` | @DataJpaTest skeleton |
| `templates/IntegrationTests.java` | @SpringBootTest + Testcontainers skeleton |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-junit-testing.py` | Validate test-class spec | Pre-commit on spec artefact |

## Related

- [[java-spring]]
- [[java-jpa-hibernate]]
- [[csharp-xunit-testing]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps target (controller/service/repository/integration) to a rule from `01-core-rules.xml`. Use it whenever picking the right Spring Boot test annotation set.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ControllerTests.java`

```java
package faion.web;

import com.fasterxml.jackson.databind.ObjectMapper;
import faion.app.orders.OrderService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(OrdersController.class)
class OrdersControllerTest {

    @Autowired private MockMvc mvc;
    @Autowired private ObjectMapper mapper;
    @MockBean private OrderService service;

    @Test
    void getById_existingOrder_returns200() throws Exception {
        when(service.getById(eq(java.util.UUID.fromString("00000000-0000-0000-0000-000000000001"))))
            .thenReturn(new OrderResponse("00000000-0000-0000-0000-000000000001", "Alice", "10.00"));

        mvc.perform(get("/api/orders/00000000-0000-0000-0000-000000000001"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.customerName").value("Alice"));
    }

    @ParameterizedTest
    @ValueSource(strings = {"not-a-uuid", "00000000-0000-0000-0000-0000000000XX"})
    void getById_invalidUuid_returns400(String id) throws Exception {
        mvc.perform(get("/api/orders/" + id))
            .andExpect(status().isBadRequest());
    }

    record OrderResponse(String id, String customerName, String total) {}
}
```

### `templates/ServiceTests.java`

```java
package faion.app.orders;

import faion.infra.orders.OrderRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.argThat;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock private OrderRepository repository;
    @InjectMocks private OrderService service;

    @Test
    void getById_existingOrder_returnsResponse() {
        UUID id = UUID.randomUUID();
        when(repository.findByIdWithItems(id)).thenReturn(Optional.of(new faion.domain.orders.Order("Alice")));

        OrderResponse response = service.getById(id);

        assertThat(response.customerName()).isEqualTo("Alice");
        verify(repository).findByIdWithItems(argThat(arg -> arg.equals(id)));
    }

    @Test
    void getById_missing_throws() {
        UUID id = UUID.randomUUID();
        when(repository.findByIdWithItems(id)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> service.getById(id))
            .isInstanceOf(OrderNotFoundException.class);
    }
}
```

### `templates/RepositoryTests.java`

```java
package faion.infra.orders;

import faion.domain.orders.Order;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class OrderRepositoryTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");

    @Autowired
    private OrderRepository repository;

    @Test
    void save_and_findById_returnsAggregateWithItems() {
        Order saved = repository.save(new Order("Alice"));

        var found = repository.findByIdWithItems(saved.getId());

        assertThat(found).isPresent();
        assertThat(found.get().getCustomerName()).isEqualTo("Alice");
    }
}
```

### `templates/IntegrationTests.java`

```java
package faion.app;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
class OrdersIntegrationTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");

    @Autowired
    private TestRestTemplate rest;

    @Test
    void createAndGetOrder_endToEnd() {
        ResponseEntity<String> created = rest.postForEntity(
            "/api/orders",
            new CreateOrderRequest("Alice"),
            String.class
        );
        assertThat(created.getStatusCode()).isEqualTo(HttpStatus.CREATED);

        ResponseEntity<String> got = rest.getForEntity(created.getHeaders().getLocation(), String.class);
        assertThat(got.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(got.getBody()).contains("Alice");
    }

    record CreateOrderRequest(String customerName) {}
}
```
