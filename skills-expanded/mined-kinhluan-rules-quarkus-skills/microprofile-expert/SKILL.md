---
name: microprofile-expert
description: Expert knowledge for Eclipse MicroProfile specifications including Config, Health, Metrics, OpenAPI, Fault Tolerance, and JWT. Use for cloud-native Java microservices standards.
version: 1.0.0
keywords: [microprofile, config, health, metrics, openapi, fault-tolerance, jwt, microservices]
---

# microprofile-expert

> Keyword: microprofile | Platforms: gemini,claude,codex

MicroProfile Expert Skill - Deep knowledge of Eclipse MicroProfile specifications for building cloud-native microservices.

## Core Mandates

- **Config Externalization:** All environment-specific values must use `@ConfigProperty`, never hardcode.
- **Health Probes:** Always implement both `@Liveness` and `@Readiness` checks for container orchestration.
- **Metrics Exposure:** Expose application metrics via `@Timed`, `@Counted`, `@Metered` for observability.
- **API Documentation:** Auto-generate OpenAPI specs from code annotations.
- **Fault Tolerance:** Use `@Retry`, `@CircuitBreaker`, `@Timeout`, `@Fallback` for resilient services.
- **Security First:** Use MicroProfile JWT for stateless authentication in microservices.

---

## MicroProfile Config

### @ConfigProperty

```java
@ApplicationScoped
public class PaymentConfig {

    @ConfigProperty(name = "payment.timeout", defaultValue = "30")
    int timeoutSeconds;

    @ConfigProperty(name = "payment.gateway.url")
    String gatewayUrl;  // Required - fails if missing

    @ConfigProperty(name = "payment.api-key")
    Optional<String> apiKey;  // Optional

    @ConfigProperty(name = "payment.features")
    Optional<List<String>> features;  // Comma-separated list

    @ConfigProperty(name = "payment.enabled", defaultValue = "true")
    boolean enabled;
}
```

### Config Sources Priority

```
1. System properties (-Dpayment.timeout=60)
2. Environment variables (PAYMENT_TIMEOUT=60)
3. application.properties / application.yaml
4. META-INF/microprofile-config.properties
5. Custom ConfigSource implementations
```

### Custom ConfigSource

```java
@Priority(400)
public class DatabaseConfigSource implements ConfigSource {

    @Override
    public Map<String, String> getProperties() {
        // Load from database
        return Map.of(
            "db.host", "postgres.internal",
            "db.port", "5432"
        );
    }

    @Override
    public String getValue(String propertyName) {
        return getProperties().get(propertyName);
    }

    @Override
    public String getName() {
        return "DatabaseConfigSource";
    }

    @Override
    public int getOrdinal() {
        return 400;  // Higher = higher priority
    }
}
```

### Config Profiles

```properties
# Default
payment.timeout=30

# Development
%dev.payment.timeout=5

# Test
%test.payment.timeout=1

# Production
%prod.payment.timeout=60
%prod.payment.gateway.url=https://api.payment.com/v1
```

---

## MicroProfile Health

### Liveness Check

```java
@Liveness
@ApplicationScoped
public class DatabaseLivenessCheck implements HealthCheck {

    @Inject
    AgroalDataSource dataSource;

    @Override
    public HealthCheckResponse call() {
        try (Connection conn = dataSource.getConnection()) {
            if (conn.isValid(5)) {
                return HealthCheckResponse.up("database");
            }
        } catch (SQLException e) {
            return HealthCheckResponse.down("database")
                .withData("error", e.getMessage());
        }
        return HealthCheckResponse.down("database");
    }
}
```

### Readiness Check

```java
@Readiness
@ApplicationScoped
public class ServiceReadinessCheck implements HealthCheck {

    @Inject
    PaymentGateway paymentGateway;

    @Override
    public HealthCheckResponse call() {
        try {
            paymentGateway.healthCheck();
            return HealthCheckResponse.up("payment-gateway");
        } catch (Exception e) {
            return HealthCheckResponse.down("payment-gateway")
                .withData("error", e.getMessage());
        }
    }
}
```

### Startup Check

```java
@Startup
@ApplicationScoped
public class CacheWarmupCheck implements HealthCheck {

    @Inject
    CacheManager cacheManager;

    @Override
    public HealthCheckResponse call() {
        if (cacheManager.isWarmedUp()) {
            return HealthCheckResponse.up("cache-warmup");
        }
        return HealthCheckResponse.down("cache-warmup")
            .withData("status", "warming up");
    }
}
```

### Health Endpoints

```
GET /q/health         - Aggregate health status
GET /q/health/live    - Liveness probes
GET /q/health/ready   - Readiness probes
GET /q/health/started - Startup probes
```

---

## MicroProfile Metrics

### Application Metrics

```java
@ApplicationScoped
public class OrderService {

    @Inject
    MeterRegistry registry;

    @Timed(name = "order.processing.time", description = "Time taken to process orders")
    @Counted(name = "order.processed.count", description = "Total orders processed")
    public Order processOrder(CreateOrderRequest request) {
        // Processing logic
        return order;
    }

    @Metered(name = "order.errors", description = "Order processing errors")
    public void handleError(OrderError error) {
        // Error handling
    }
}
```

### Custom Metrics

```java
@ApplicationScoped
public class CustomMetrics {

    @Inject
    MetricRegistry metricRegistry;

    void initMetrics() {
        // Counter
        Counter orderCounter = metricRegistry.counter("orders.created");
        orderCounter.inc();

        // Gauge
        metricRegistry.gauge("orders.pending", () -> pendingOrders::size);

        // Histogram
        Histogram responseSize = metricRegistry.histogram("response.size.bytes");
        responseSize.update(responseBytes);

        // Timer
        Timer timer = metricRegistry.timer("api.latency");
        try (Timer.Context ctx = timer.time()) {
            // Measured operation
        }
    }
}
```

### Metrics Endpoint

```
GET /q/metrics              - All metrics (Prometheus format)
GET /q/metrics/application  - Application metrics only
GET /q/metrics/base         - Base JVM metrics
GET /q/metrics/vendor       - Vendor-specific metrics
```

### Prometheus Output Example

```
# HELP order_processing_time_seconds Time taken to process orders
# TYPE order_processing_time_seconds summary
order_processing_time_seconds_count 42
order_processing_time_seconds_sum 12.345
order_processing_time_seconds_max 0.987
```

---

## MicroProfile OpenAPI

### Annotating REST Endpoints

```java
@Path("/api/users")
@OpenAPIDefinition(
    info = @Info(
        title = "User API",
        version = "1.0.0",
        description = "API for user management",
        contact = @Contact(name = "API Support", email = "api@example.com")
    )
)
public class UserResource {

    @GET
    @Operation(
        summary = "List all users",
        description = "Returns a paginated list of users"
    )
    @APIResponse(
        responseCode = "200",
        description = "Successful response",
        content = @Content(schema = @Schema(implementation = UserList.class))
    )
    @APIResponse(
        responseCode = "401",
        description = "Unauthorized"
    )
    public List<User> listUsers(
        @Parameter(description = "Page number", example = "0")
        @QueryParam("page") @DefaultValue("0") int page,
        @Parameter(description = "Page size", example = "20")
        @QueryParam("size") @DefaultValue("20") int size
    ) {
        return userService.findAll(page, size);
    }

    @POST
    @Operation(summary = "Create a new user")
    @RequestBody(
        description = "User to create",
        required = true,
        content = @Content(schema = @Schema(implementation = CreateUserRequest.class))
    )
    @APIResponse(
        responseCode = "201",
        description = "User created",
        content = @Content(schema = @Schema(implementation = User.class))
    )
    @APIResponse(
        responseCode = "400",
        description = "Invalid input"
    )
    public Response createUser(@Valid CreateUserRequest request) {
        User user = userService.create(request);
        return Response.created(URI.create("/api/users/" + user.id())).entity(user).build();
    }
}
```

### Schema Annotations

```java
@Schema(description = "User representation")
public class User {

    @Schema(description = "Unique identifier", example = "123", required = true)
    public Long id;

    @Schema(description = "User's full name", example = "John Doe", required = true)
    public String name;

    @Schema(description = "Email address", example = "john@example.com", required = true)
    public String email;

    @Schema(description = "Account status", example = "ACTIVE", allowableValues = {"ACTIVE", "INACTIVE", "SUSPENDED"})
    public Status status;
}
```

### OpenAPI Endpoints

```
GET /q/openapi          - OpenAPI spec (YAML)
GET /q/openapi?format=json - OpenAPI spec (JSON)
GET /q/swagger-ui       - Swagger UI (if enabled)
```

---

## MicroProfile Fault Tolerance

### @Retry

```java
@ApplicationScoped
public class PaymentService {

    @Retry(
        maxRetries = 3,
        delay = 200,           // 200ms initial delay
        delayUnit = ChronoUnit.MILLIS,
        maxDuration = 10000,   // 10s max total duration
        retryOn = {PaymentException.class, TimeoutException.class},
        abortOn = {IllegalArgumentException.class}
    )
    public PaymentResult processPayment(PaymentRequest request) {
        return gateway.charge(request);
    }
}
```

### @CircuitBreaker

```java
@ApplicationScoped
public class ExternalService {

    @CircuitBreaker(
        requestVolumeThreshold = 10,    // 10 requests in rolling window
        failureRatio = 0.5,             // Open if 50% fail
        delay = 5000,                   // Wait 5s before half-open
        successThreshold = 3            // 3 successes to close
    )
    @Fallback(fallbackMethod = "getDefaultData")
    public Data fetchData(String id) {
        return httpClient.getData(id);
    }

    public Data getDefaultData(String id) {
        return Data.defaultFor(id);
    }
}
```

### @Timeout

```java
@ApplicationScoped
public class ReportService {

    @Timeout(value = 5, unit = ChronoUnit.SECONDS)
    @Fallback(fallbackMethod = "generateEmptyReport")
    public Report generateReport(ReportRequest request) {
        return reportGenerator.create(request);
    }

    public Report generateEmptyReport(ReportRequest request) {
        return Report.empty(request.id());
    }
}
```

### @Bulkhead

```java
@ApplicationScoped
public class EmailService {

    @Bulkhead(10)  // Max 10 concurrent calls
    public void sendEmail(Email email) {
        emailClient.send(email);
    }

    @Bulkhead(value = 5, waitingTaskQueue = 10)  // Thread pool bulkhead
    public void sendBulkEmails(List<Email> emails) {
        emails.forEach(this::sendEmail);
    }
}
```

### Combining Annotations

```java
@ApplicationScoped
public class ResilientService {

    @Timeout(5000)
    @Retry(maxRetries = 3, delay = 1000)
    @CircuitBreaker(requestVolumeThreshold = 10, failureRatio = 0.5)
    @Fallback(fallbackMethod = "fallback")
    @Bulkhead(10)
    public Result callExternalService(Request request) {
        return externalApi.call(request);
    }

    public Result fallback(Request request) {
        return Result.cached(request.id());
    }
}
```

---

## MicroProfile JWT

### Securing Endpoints

```java
@Path("/api/admin")
@Authenticated
public class AdminResource {

    @Inject
    JsonWebToken jwt;

    @Inject
    @Claim("preferred_username")
    Optional<String> username;

    @GET
    @Path("/users")
    @RolesAllowed("admin")
    public List<User> listAllUsers() {
        String currentUser = jwt.getName();
        auditLog.logAccess(currentUser, "list-users");
        return userService.findAll();
    }

    @DELETE
    @Path("/users/{id}")
    @RolesAllowed("admin")
    public void deleteUser(@PathParam("id") Long id) {
        userService.delete(id);
    }

    @GET
    @Path("/profile")
    public UserProfile getProfile() {
        return new UserProfile(
            jwt.getSubject(),
            jwt.getName(),
            jwt.getGroups()
        );
    }
}
```

### JWT Configuration

```properties
# application.properties
mp.jwt.verify.publickey.location=META-INF/resources/publicKey.pem
mp.jwt.verify.issuer=https://auth.example.com
smallrye.jwt.sign.key.location=META-INF/resources/privateKey.pem

# Quarkus specific
quarkus.smallrye-jwt.enabled=true
```

### Programmatic JWT Verification

```java
@ApplicationScoped
public class JwtService {

    @Inject
    JWTParser parser;

    public JsonWebToken parseToken(String token) throws ParseException {
        return parser.parse(token);
    }

    public boolean hasRole(JsonWebToken jwt, String role) {
        return jwt.getGroups().contains(role);
    }
}
```

---

## MicroProfile Rest Client

### Declarative Client

```java
@Path("/api")
@RegisterRestClient(configKey = "payment-api")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public interface PaymentClient {

    @POST
    @Path("/payments")
    PaymentResult process(@Valid PaymentRequest request);

    @GET
    @Path("/payments/{id}")
    PaymentStatus status(@PathParam("id") String id);

    @DELETE
    @Path("/payments/{id}")
    void cancel(@PathParam("id") String id);
}
```

### Configuration

```properties
# REST Client config
payment-api/mp-rest/url=https://api.payment.com
payment-api/mp-rest/connectTimeout=5000
payment-api/mp-rest/readTimeout=10000

# Or using Quarkus config
quarkus.rest-client.payment-api.url=https://api.payment.com
quarkus.rest-client.payment-api.connect-timeout=5000
quarkus.rest-client.payment-api.read-timeout=10000
```

### Using the Client

```java
@ApplicationScoped
public class OrderService {

    @Inject
    @RestClient
    PaymentClient paymentClient;

    public Order createOrder(CreateOrderRequest request) {
        PaymentResult result = paymentClient.process(request.payment());
        // Process result
        return order;
    }
}
```

---

## References

- [MicroProfile Specification](https://microprofile.io/)
- [MicroProfile Config](https://github.com/eclipse/microprofile-config)
- [MicroProfile Health](https://github.com/eclipse/microprofile-health)
- [MicroProfile Metrics](https://github.com/eclipse/microprofile-metrics)
- [MicroProfile OpenAPI](https://github.com/eclipse/microprofile-open-api)
- [MicroProfile Fault Tolerance](https://github.com/eclipse/microprofile-fault-tolerance)
- [MicroProfile JWT](https://github.com/eclipse/microprofile-jwt-auth)
- [MicroProfile Rest Client](https://github.com/eclipse/microprofile-rest-client)
- [Quarkus MicroProfile Guide](https://quarkus.io/guides/microprofile)

## Skill Interoperability

The **microprofile-expert** skill provides cloud-native standards for:
- **quarkus-expert** ⚡: Quarkus implements all MicroProfile specifications.
- **java-expert** ☕: Core Java language features.
- **quarkus-testing** 🧪: Testing MicroProfile features with `@QuarkusTest`.
