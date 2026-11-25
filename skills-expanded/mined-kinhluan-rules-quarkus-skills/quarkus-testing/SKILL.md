---
name: quarkus-testing
description: Comprehensive Quarkus testing expertise covering @QuarkusTest, @InjectMock, Testcontainers, Dev Services, and native image testing. Use for all Quarkus testing questions.
version: 1.0.0
keywords: [quarkus, testing, junit, testcontainers, mock, integration-test]
---

# quarkus-testing

> Keyword: quarkus-test | Platforms: gemini,claude,codex

Quarkus Testing Expert Skill - Deep knowledge of testing strategies for the Quarkus ecosystem.

## Core Mandates

- **Test at the Right Level:** Use `@QuarkusTest` for integration, `@QuarkusUnitTest` for extension testing, `@QuarkusIntegrationTest` for native/artifact verification.
- **Mock External Dependencies:** Use `@InjectMock` for CDI beans, WireMock/Testcontainers for external services.
- **Dev Services First:** Leverage zero-config Dev Services for databases, Kafka, Redis in dev/test.
- **Test Data Isolation:** Each test must be independent - use `@Transactional` rollback or `@TestTransaction`.
- **Fast Feedback:** Keep `@QuarkusTest` suite fast; move slow tests to `@QuarkusIntegrationTest`.

---

## @QuarkusTest Fundamentals

### Basic Integration Test

```java
@QuarkusTest
class UserResourceTest {

    @Test
    void shouldListUsers() {
        given()
            .when().get("/api/users")
            .then()
            .statusCode(200)
            .body("$.size()", greaterThanOrEqualTo(0));
    }

    @Test
    void shouldCreateUser() {
        given()
            .contentType(ContentType.JSON)
            .body("""
                {"name": "John Doe", "email": "john@example.com"}
                """)
            .when().post("/api/users")
            .then()
            .statusCode(201)
            .header("Location", containsString("/api/users/"));
    }

    @Test
    void shouldReturn404ForMissingUser() {
        given()
            .when().get("/api/users/99999")
            .then()
            .statusCode(404)
            .body("message", containsString("not found"));
    }
}
```

### Testing with Authentication

```java
@QuarkusTest
class SecuredResourceTest {

    @Test
    void shouldAllowAuthenticatedAccess() {
        given()
            .auth().oauth2(getAccessToken("user"))
            .when().get("/api/profile")
            .then()
            .statusCode(200);
    }

    @Test
    void shouldRejectUnauthorizedAccess() {
        given()
            .when().get("/api/profile")
            .then()
            .statusCode(401);
    }

    @Test
    @TestSecurity(authorizationEnabled = false)
    void shouldBypassAuthForTesting() {
        given()
            .when().get("/api/profile")
            .then()
            .statusCode(200);
    }

    @Test
    @TestSecurity(user = "admin", roles = {"admin", "user"})
    void shouldTestWithSpecificRoles() {
        given()
            .when().get("/api/admin/dashboard")
            .then()
            .statusCode(200);
    }
}
```

---

## @InjectMock & @InjectSpy

### Mocking CDI Beans

```java
@QuarkusTest
class OrderServiceTest {

    @InjectMock
    PaymentGateway paymentGateway;

    @InjectMock
    NotificationService notificationService;

    @Inject
    OrderService orderService;

    @Test
    void shouldProcessOrderSuccessfully() {
        when(paymentGateway.charge(any(), any()))
            .thenReturn(Uni.createFrom().item(new PaymentResult("SUCCESS", "txn-123")));

        Order result = orderService.createOrder(new CreateOrderRequest("user-1", BigDecimal.TEN))
            .await().atMost(Duration.ofSeconds(5));

        assertThat(result.status()).isEqualTo(OrderStatus.CONFIRMED);
        verify(paymentGateway).charge(any(), eq(BigDecimal.TEN));
        verify(notificationService).sendOrderConfirmation(result);
    }

    @Test
    void shouldHandlePaymentFailure() {
        when(paymentGateway.charge(any(), any()))
            .thenReturn(Uni.createFrom().failure(new PaymentException("Card declined")));

        assertThatThrownBy(() ->
            orderService.createOrder(new CreateOrderRequest("user-1", BigDecimal.TEN))
                .await().atMost(Duration.ofSeconds(5))
        ).hasCauseInstanceOf(PaymentException.class);

        verify(notificationService, never()).sendOrderConfirmation(any());
    }

    @Test
    void shouldRetryFailedPayment() {
        when(paymentGateway.charge(any(), any()))
            .thenReturn(Uni.createFrom().failure(new PaymentException("Timeout")))
            .thenReturn(Uni.createFrom().item(new PaymentResult("SUCCESS", "txn-456")));

        Order result = orderService.createOrder(new CreateOrderRequest("user-1", BigDecimal.TEN))
            .await().atMost(Duration.ofSeconds(10));

        assertThat(result.status()).isEqualTo(OrderStatus.CONFIRMED);
        verify(paymentGateway, times(2)).charge(any(), any());
    }
}
```

### Spying on Beans

```java
@QuarkusTest
class UserServiceTest {

    @InjectSpy
    UserRepository userRepository;

    @Inject
    UserService userService;

    @Test
    void shouldCacheUserLookup() {
        userService.findById(1L);
        userService.findById(1L);

        verify(userRepository, times(1)).findById(1L);
    }
}
```

### Mockito Argument Matchers with Panache

```java
@QuarkusTest
class PanacheMockingTest {

    @InjectMock
    UserRepository userRepository;

    @Test
    void shouldMockPanacheRepository() {
        User mockUser = new User();
        mockUser.name = "Mocked";
        mockUser.email = "mocked@example.com";

        PanacheMock.mock(User.class);
        when(User.findById(1L)).thenReturn(mockUser);
        when(User.findByEmail("test@example.com"))
            .thenReturn(Optional.of(mockUser));
        when(User.listAll()).thenReturn(List.of(mockUser));

        // Test your service that uses User.findById(...)
    }
}
```

---

## Dev Services (Zero-Config Testing)

### Database Dev Services

```java
@QuarkusTest
class UserRepositoryTest {

    @Inject
    UserRepository userRepository;

    @Test
    @Transactional
    void shouldPersistAndFindUser() {
        User user = new User();
        user.name = "Alice";
        user.email = "alice@example.com";
        userRepository.persist(user);

        Optional<User> found = userRepository.findByEmail("alice@example.com");
        assertThat(found).isPresent();
        assertThat(found.get().name).isEqualTo("Alice");
    }
}
// PostgreSQL container auto-starts via Dev Services - zero configuration needed
```

### Custom Dev Services Configuration

```properties
# application.properties (test profile)
%test.quarkus.datasource.devservices.image-name=postgres:16-alpine
%test.quarkus.datasource.devservices.port=5432
%test.quarkus.datasource.devservices.db-name=testdb

# Kafka Dev Services
%test.quarkus.kafka.devservices.enabled=true
%test.quarkus.kafka.devservices.image-name=redpandadata/redpanda:latest

# Redis Dev Services
%test.quarkus.redis.devservices.enabled=true
%test.quarkus.redis.devservices.image-name=redis:7-alpine
```

### Multiple Datasources

```java
@QuarkusTest
class MultiDatasourceTest {

    @Inject
    @Named("users")
    AgroalDataSource usersDataSource;

    @Inject
    @Named("analytics")
    AgroalDataSource analyticsDataSource;

    @Test
    void shouldConnectToBothDatabases() {
        assertThat(usersDataSource).isNotNull();
        assertThat(analyticsDataSource).isNotNull();
    }
}
```

---

## Testcontainers Integration

### Custom Testcontainers

```java
@QuarkusTest
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class ExternalServiceIntegrationTest {

    @Container
    static GenericContainer<?> wireMock = new GenericContainer<>("wiremock/wiremock:3.5.2")
        .withExposedPorts(8080)
        .waitingFor(Wait.forHttp("/__admin/mappings").forStatusCode(200));

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("external.api.url",
            () -> "http://localhost:" + wireMock.getMappedPort(8080));
        registry.add("quarkus.datasource.jdbc.url", postgres::getJdbcUrl);
        registry.add("quarkus.datasource.username", postgres::getUsername);
        registry.add("quarkus.datasource.password", postgres::getPassword);
    }

    @Test
    void shouldCallExternalService() {
        // Test code using WireMock and PostgreSQL
    }
}
```

### Shared Containers for Performance

```java
public class SharedPostgresResource
    implements QuarkusTestResourceLifecycleManager {

    static PostgreSQLContainer<?> postgres =
        new PostgreSQLContainer<>("postgres:16-alpine");

    @Override
    public Map<String, String> start() {
        postgres.start();
        return Map.of(
            "quarkus.datasource.jdbc.url", postgres.getJdbcUrl(),
            "quarkus.datasource.username", postgres.getUsername(),
            "quarkus.datasource.password", postgres.getPassword()
        );
    }

    @Override
    public void stop() {
        // Don't stop - shared across tests
    }

    public static PostgreSQLContainer<?> getContainer() {
        return postgres;
    }
}

// Usage
@QuarkusTest
@QuarkusTestResource(SharedPostgresResource.class)
class FastIntegrationTest {
    // Tests reuse the same PostgreSQL container
}
```

---

## Transactional Testing

### Automatic Rollback

```java
@QuarkusTest
class TransactionalTest {

    @Inject
    UserRepository userRepository;

    @Test
    @Transactional
    void shouldNotPersistAfterTest() {
        User user = new User();
        user.name = "Temp";
        userRepository.persist(user);

        assertThat(userRepository.count()).isEqualTo(1);
    }  // Automatically rolled back after test

    @Test
    @Transactional
    void shouldSeeCleanDatabase() {
        // Previous test data is gone due to rollback
        assertThat(userRepository.count()).isEqualTo(0);
    }
}
```

### @TestTransaction (Alternative)

```java
@Test
@TestTransaction
void shouldUseTestTransaction() {
    // Same as @Transactional but semantically clearer
    // Always rolls back after test
}
```

### Manual Transaction Control

```java
@Test
void shouldControlTransactionManually() {
    QuarkusTransaction.begin();
    try {
        userRepository.persist(newUser);
        QuarkusTransaction.commit();
    } catch (Exception e) {
        QuarkusTransaction.rollback();
        throw e;
    }
}
```

---

## Native Image Testing

### @QuarkusIntegrationTest

```java
@QuarkusIntegrationTest
class NativeUserResourceIT {

    @Test
    void shouldWorkInNativeMode() {
        given()
            .when().get("/api/users")
            .then()
            .statusCode(200);
    }
}
// Runs against the native binary or container image
```

### Conditional Native Testing

```java
@QuarkusTest
class UserResourceTest {

    @Test
    @DisabledOnNativeImage  // Skip in native mode
    void shouldTestDevOnlyFeature() {
        // This test only runs in JVM mode
    }

    @Test
    @EnabledOnNativeImage  // Only run in native mode
    void shouldTestNativeOnlyFeature() {
        // This test only runs in native mode
    }
}
```

---

## REST Assured Patterns

### Custom Object Mapping

```java
@QuarkusTest
class AdvancedRestAssuredTest {

    @Test
    void shouldDeserializeResponse() {
        User user = given()
            .when().get("/api/users/1")
            .then()
            .statusCode(200)
            .extract().as(User.class);

        assertThat(user.name()).isEqualTo("Alice");
    }

    @Test
    void shouldValidateJsonSchema() {
        given()
            .when().get("/api/users/1")
            .then()
            .body("id", notNullValue())
            .body("name", not(emptyString()))
            .body("email", matchesPattern(".*@.*\\..*"));
    }

    @Test
    void shouldTestWithQueryParams() {
        given()
            .queryParam("page", 0)
            .queryParam("size", 10)
            .queryParam("sort", "name,asc")
            .when().get("/api/users")
            .then()
            .statusCode(200)
            .body("$.size()", lessThanOrEqualTo(10));
    }
}
```

---

## Testing Best Practices

### Test Pyramid for Quarkus

```
    /\
   /  \  E2E Tests (@QuarkusIntegrationTest)
  /----\    ~5% of tests
 /      \
/--------\ Integration Tests (@QuarkusTest)
/          \   ~20% of tests
/------------\ Unit Tests (plain JUnit + Mockito)
/              \   ~75% of tests
```

### Test Naming Convention

```java
// Pattern: should<ExpectedBehavior>When<Condition>
@Test
void shouldReturn404WhenUserNotFound() { }

@Test
void shouldSendNotificationWhenOrderCreated() { }

@Test
void shouldRollbackTransactionWhenPaymentFails() { }
```

### Test Data Builders

```java
public class UserBuilder {
    private String name = "Default User";
    private String email = "default@example.com";
    private Status status = Status.ACTIVE;

    public UserBuilder withName(String name) {
        this.name = name;
        return this;
    }

    public UserBuilder withEmail(String email) {
        this.email = email;
        return this;
    }

    public User build() {
        User user = new User();
        user.name = name;
        user.email = email;
        user.status = status;
        return user;
    }
}

// Usage in tests
User user = new UserBuilder()
    .withName("Alice")
    .withEmail("alice@example.com")
    .build();
```

---

## Troubleshooting

### Test Hangs or Times Out

```
Cause: Mutiny Uni/Multi not subscribed or awaited
Fix: Always call .await().atMost(Duration) in tests
```

### Dev Services Not Starting

```
Cause: Docker not running or insufficient resources
Fix: Check Docker daemon, increase Docker memory limit
```

### @InjectMock Not Working

```
Cause: Bean not discovered by CDI
Fix: Ensure bean has @ApplicationScoped or @Singleton
```

---

## References

- [Quarkus Testing Guide](https://quarkus.io/guides/getting-started-testing)
- [Quarkus Dev Services](https://quarkus.io/guides/dev-services)
- [REST Assured Documentation](https://rest-assured.io/)
- [Testcontainers](https://www.testcontainers.org/)

## Skill Interoperability

The **quarkus-testing** skill extends:
- **quarkus-expert** ⚡: Testing patterns for Quarkus applications.
- **java-expert** ☕: JUnit 5 and Mockito fundamentals.
- **graalvm-expert** 🚀: Native image testing with @QuarkusIntegrationTest.
