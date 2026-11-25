---
name: testing-patterns
description: Testing patterns for Quarkus - @QuarkusTest, RestAssured, Mockito mocking, Dev Services (built-in Testcontainers), and @QuarkusIntegrationTest. Use when user asks about testing, writing tests, test coverage, or test failures.
---

# Testing Patterns Skill

Testing strategies for Quarkus applications. Always write both positive and negative test cases.

## When to Use
- "write tests" / "add test coverage" / "test this"
- Test failures or debugging test issues
- Choosing between plain unit tests, `@QuarkusTest`, and `@QuarkusIntegrationTest`
- Setting up a database/Kafka/etc. for tests

---

## Test Types Overview

Quarkus has three test levels, with no separate "slice" annotations needed per layer:

| Level | How | Speed | Scope | When to Use |
|-------|-----|-------|-------|-------------|
| Plain unit test | No Quarkus annotation, `@ExtendWith(MockitoExtension.class)` | Fastest | Single class, no CDI | Pure business logic with no injected beans |
| `@QuarkusTest` | Boots the full CDI container **in the test JVM** | Fast (app stays up across the test run) | Whole app, in-process | REST endpoints, CDI beans, repositories — the default choice |
| `@QuarkusIntegrationTest` | Starts the **built artifact** (jar / native image / container) as a separate process | Slowest | End-to-end against the real packaged app | Verifying the artifact that actually ships, incl. native image |

---

## Dependencies

```xml
<dependency>
    <groupId>io.quarkus</groupId>
    <artifactId>quarkus-junit5</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>io.rest-assured</groupId>
    <artifactId>rest-assured</artifactId>
    <scope>test</scope>
</dependency>
<!-- Only needed for @InjectMock / @InjectSpy -->
<dependency>
    <groupId>io.quarkus</groupId>
    <artifactId>quarkus-junit5-mockito</artifactId>
    <scope>test</scope>
</dependency>
```

`quarkus-junit5` provides `@QuarkusTest`. RestAssured automatically targets the right test port — no base URL configuration needed.

---

## Plain Unit Tests (Business Logic)

Use these for classes with no CDI dependencies, or where you want to mock collaborators manually without booting Quarkus at all.

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private ProductService productService;

    @InjectMocks
    private OrderService orderService;

    // ✅ Positive test
    @Test
    @DisplayName("Should create order with valid items")
    void shouldCreateOrder() {
        // Given
        var request = new OrderRequest(List.of(new OrderItem(1L, 2)));
        var product = new Product();
        product.setId(1L);
        product.setPrice(new BigDecimal("10.00"));

        when(productService.findById(1L)).thenReturn(product);

        // When
        Order result = orderService.create(request);

        // Then
        assertThat(result).isNotNull();
        verify(orderRepository).persist(any(Order.class));
    }

    // ✅ Negative test
    @Test
    @DisplayName("Should throw when product not found")
    void shouldThrowWhenProductNotFound() {
        var request = new OrderRequest(List.of(new OrderItem(999L, 1)));
        when(productService.findById(999L))
            .thenThrow(new EntityNotFoundException("Product not found"));

        assertThatThrownBy(() -> orderService.create(request))
            .isInstanceOf(EntityNotFoundException.class)
            .hasMessageContaining("Product not found");

        verify(orderRepository, never()).persist(any(Order.class));
    }
}
```

---

## REST API Tests with `@QuarkusTest` + RestAssured

```java
@QuarkusTest
class ProductResourceTest {

    // ✅ Positive - successful creation
    @Test
    @DisplayName("POST /api/v1/products - returns 201")
    void createProduct_validRequest_returns201() {
        given()
            .contentType(ContentType.JSON)
            .body("""
                {"name": "Widget", "price": 10.00}
                """)
            .when().post("/api/v1/products")
            .then()
                .statusCode(201)
                .body("name", is("Widget"));
    }

    // ✅ Negative - validation failure
    @Test
    @DisplayName("POST /api/v1/products - blank name returns 400")
    void createProduct_blankName_returns400() {
        given()
            .contentType(ContentType.JSON)
            .body("""
                {"name": "", "price": 10.00}
                """)
            .when().post("/api/v1/products")
            .then()
                .statusCode(400);
    }

    // ✅ Negative - not found
    @Test
    @DisplayName("GET /api/v1/products/999 - returns 404")
    void getProduct_notFound_returns404() {
        given()
            .when().get("/api/v1/products/999")
            .then()
                .statusCode(404);
    }
}
```

`@TestHTTPEndpoint` binds the test to a resource class instead of hardcoding paths:

```java
@QuarkusTest
@TestHTTPEndpoint(ProductResource.class)
class ProductResourceTest {

    @Test
    void getProduct_notFound_returns404() {
        given()
            .when().get("/999")   // resolved relative to ProductResource's @Path
            .then()
                .statusCode(404);
    }
}
```

### Full CRUD Flow

```java
@QuarkusTest
class ProductIntegrationTest {

    @Test
    @DisplayName("Full CRUD flow works end-to-end")
    void crudFlow() {
        // Create
        Long id = given()
            .contentType(ContentType.JSON)
            .body("""
                {"name": "Widget", "price": 10.00}
                """)
            .when().post("/api/v1/products")
            .then()
                .statusCode(201)
            .extract().jsonPath().getLong("id");

        // Read
        given()
            .when().get("/api/v1/products/{id}", id)
            .then()
                .statusCode(200)
                .body("name", is("Widget"));

        // Delete
        given()
            .when().delete("/api/v1/products/{id}", id)
            .then()
                .statusCode(204);

        given()
            .when().get("/api/v1/products/{id}", id)
            .then()
                .statusCode(404);
    }
}
```

---

## Mocking CDI Beans

### `@InjectMock` (requires `quarkus-junit5-mockito`)

```java
@QuarkusTest
class ProductResourceTest {

    @InjectMock
    ProductService productService;

    @Test
    void getProduct_notFound_returns404() {
        when(productService.findById(999L))
            .thenThrow(new EntityNotFoundException("Product not found"));

        given()
            .when().get("/api/v1/products/999")
            .then()
                .statusCode(404);
    }
}
```

### Mocking a REST Client

```java
@QuarkusTest
class ReportResourceTest {

    @InjectMock
    @RestClient
    CustomerApiClient customerApi;

    @Test
    void generate_returnsReportWithCustomerData() {
        when(customerApi.getCustomer(1L)).thenReturn(new CustomerData(1L, "Acme Corp"));

        given()
            .when().get("/api/v1/reports/1")
            .then()
                .statusCode(200)
                .body("customerName", is("Acme Corp"));
    }
}
```

### `@InjectSpy` for Partial Mocks

```java
@QuarkusTest
class GreetingResourceTest {

    @InjectSpy
    GreetingService greetingService;

    @Test
    void overridesOnlyOneMethod() {
        doReturn("hi").when(greetingService).greet();

        given()
            .when().get("/greeting")
            .then()
                .statusCode(200)
                .body(is("hi"));
    }
}
```

`@InjectMock`/`@InjectSpy` only work with `@QuarkusTest` (same JVM). They do **not** work with `@QuarkusIntegrationTest`, because the application under test runs as a separate process with its own, unmodified CDI container.

---

## Dev Services — Built-In Testcontainers

**Quarkus starts and wires backing services for you, automatically, with zero test code.**

Add the extension for the service you need — no `quarkus.datasource.jdbc.url`, no container declaration, nothing else:

```xml
<dependency>
    <groupId>io.quarkus</groupId>
    <artifactId>quarkus-jdbc-postgresql</artifactId>
</dependency>
<dependency>
    <groupId>io.quarkus</groupId>
    <artifactId>quarkus-hibernate-orm-panache</artifactId>
</dependency>
```

```java
// ✅ No @Testcontainers, no @Container, no manual config - Dev Services does it all
@QuarkusTest
class ProductRepositoryTest {

    @Inject
    ProductRepository productRepository;

    @Test
    @DisplayName("Should find products by name containing")
    @Transactional
    void shouldFindByNameContaining() {
        var product = new Product();
        product.setName("Quarkus Widget");
        product.setPrice(new BigDecimal("10.00"));
        productRepository.persist(product);

        List<Product> results = productRepository.find("lower(name) like ?1", "%widget%").list();

        assertThat(results).hasSize(1);
        assertThat(results.getFirst().getName()).isEqualTo("Quarkus Widget");
    }
}
```

When you run `mvn test` (or start `quarkus:dev`), Quarkus detects that a datasource is configured but no connection URL was given, pulls up a PostgreSQL container via Testcontainers under the hood, points the datasource at it, and tears it down afterwards. The same zero-config mechanism exists for Kafka (`quarkus-kafka-client`, backed by Redpanda by default), RabbitMQ, Redis, MongoDB, Keycloak, and more.

**Useful knobs:**

```properties
# Disable Dev Services globally
quarkus.devservices.enabled=false

# Disable Dev Services for one datasource only
quarkus.datasource.devservices.enabled=false

# Pin the container image Dev Services should use
quarkus.datasource.devservices.image-name=postgres:18-alpine
```

Dev Services requires a running Docker (or Podman) daemon and only activates in dev/test mode — it never runs in production.

### When Dev Services Isn't Enough: `QuarkusTestResource`

Dev Services covers extensions it knows about. For anything else — WireMock to stub a third-party HTTP API, a hand-rolled container, or a resource that needs custom setup — implement `QuarkusTestResourceLifecycleManager` yourself:

```java
public class WireMockResource implements QuarkusTestResourceLifecycleManager {
    private WireMockServer wireMockServer;

    @Override
    public Map<String, String> start() {
        wireMockServer = new WireMockServer(0);
        wireMockServer.start();
        return Map.of("quarkus.rest-client.customer-api.url",
            "http://localhost:" + wireMockServer.port());
    }

    @Override
    public void stop() {
        if (wireMockServer != null) {
            wireMockServer.stop();
        }
    }
}
```

```java
@QuarkusTest
@QuarkusTestResource(WireMockResource.class)
class ReportResourceWireMockTest {
    // the REST client now points at the WireMock server
}
```

`@WithTestResource` is the newer, more ergonomic variant of `@QuarkusTestResource` (repeatable, with a `restrictToAnnotatedClass` flag) — prefer it in new code; both exist side by side.

---

## `@QuarkusIntegrationTest`

Runs the artifact your build actually produces — the runnable jar, the native image, or a container image — as a **separate OS process**, not inside the test JVM.

```java
@QuarkusIntegrationTest
class ProductResourceIT extends ProductResourceTest {
    // Reuses every @Test from ProductResourceTest, now run against the packaged artifact
}
```

Key differences from `@QuarkusTest`:

| | `@QuarkusTest` | `@QuarkusIntegrationTest` |
|---|---|---|
| Runs | In the test JVM | As a separate process (jar / native / container) |
| CDI access from test | Yes (`@Inject`, `@InjectMock`, `@InjectSpy`) | No — it's a different process |
| Catches | Logic bugs | Packaging bugs, native-image-only bugs, missing reflection config |
| Speed | Fast | Slower (full startup, no mocking) |
| Maven plugin | Surefire | Failsafe (`integration-test` + `verify` goals) |

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-failsafe-plugin</artifactId>
    <executions>
        <execution>
            <goals>
                <goal>integration-test</goal>
                <goal>verify</goal>
            </goals>
            <configuration>
                <systemPropertyVariables>
                    <native.image.path>${project.build.directory}/${project.build.finalName}-runner</native.image.path>
                </systemPropertyVariables>
            </configuration>
        </execution>
    </executions>
</plugin>
```

Run native-image verification in CI with:

```bash
./mvnw verify -Pnative
```

Because mocking isn't possible here, keep `@QuarkusIntegrationTest` classes focused on "does the packaged app come up and serve traffic correctly" rather than business-logic edge cases — those belong in `@QuarkusTest`.

---

## Test Profiles

Use a `QuarkusTestProfile` to run the same test class with different config, enabled alternatives, or test resources.

```java
public class MockGreetingProfile implements QuarkusTestProfile {

    @Override
    public Map<String, String> getConfigOverrides() {
        return Map.of("app.notification.enabled", "false");
    }

    @Override
    public String getConfigProfile() {
        return "test-mocked";
    }
}
```

```java
@QuarkusTest
@TestProfile(MockGreetingProfile.class)
class GreetingServiceTest {
    // Runs with app.notification.enabled=false and profile "test-mocked"
}
```

---

## Parameterized Tests

```java
@ParameterizedTest
@ValueSource(strings = {"", " ", "ab"})
@DisplayName("Should reject invalid usernames")
void shouldRejectInvalidUsername(String username) {
    var request = new UserRequest(username, "valid@email.com");

    assertThatThrownBy(() -> userService.create(request))
        .isInstanceOf(ConstraintViolationException.class);
}

@ParameterizedTest
@CsvSource({
    "admin@test.com, ADMIN, true",
    "user@test.com, USER, true",
    "guest@test.com, GUEST, false"
})
@DisplayName("Should check access by role")
void shouldCheckAccessByRole(String email, String role, boolean expected) {
    assertThat(securityService.hasAccess(email, role)).isEqualTo(expected);
}
```

---

## Quick Reference

| Pattern | Use For |
|---------|---------|
| `@ExtendWith(MockitoExtension.class)` | Pure unit tests, no CDI, no Quarkus boot |
| `@QuarkusTest` | In-process tests with real CDI beans and REST endpoints |
| `@QuarkusIntegrationTest` | Testing the built jar/native image/container as a black box |
| `@InjectMock` / `@InjectSpy` | Mock/spy a CDI bean inside `@QuarkusTest` (not available in `@QuarkusIntegrationTest`) |
| `@TestHTTPEndpoint(Resource.class)` | Resolve RestAssured paths relative to a resource class |
| Dev Services (just add the extension) | Zero-config Testcontainers for DB/Kafka/Redis/etc. in dev & test mode |
| `QuarkusTestResource` / `@WithTestResource` | Custom test infrastructure Dev Services doesn't cover (e.g. WireMock) |
| `@TestProfile` | Run a test class with different config/alternatives |
| `assertThatThrownBy()` | Negative test - expect exception |
| `verify(mock, never())` | Verify method was NOT called |

## Naming Convention

```
methodUnderTest_condition_expectedResult
```

Examples: `createUser_validRequest_returns201`, `createUser_duplicateEmail_throws409`
