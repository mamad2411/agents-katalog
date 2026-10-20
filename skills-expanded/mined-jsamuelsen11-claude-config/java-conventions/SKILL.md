---
name: java-conventions
description:
  This skill should be used when working on Java or Kotlin projects, writing Java code, configuring
  Spring Boot, or reviewing Java code.
version: 0.1.0
---

# Java Code Style and Idiomatic Patterns

This skill defines comprehensive conventions for writing modern Java 21+ code following the Google
Java Style Guide, Spring Boot best practices, and community-standard idioms.

## Modern Java Records

### Use Records for DTOs and Value Objects

Prefer Java records over traditional POJOs for immutable data carriers. Records provide equals,
hashCode, toString, and accessors automatically.

```java
// CORRECT: Record for a DTO
public record UserResponse(
    Long id,
    String username,
    String email,
    Instant createdAt
) {}
```

```java
// WRONG: Verbose POJO for simple data carrier
public class UserResponse {
    private final Long id;
    private final String username;
    private final String email;
    private final Instant createdAt;

    public UserResponse(Long id, String username, String email, Instant createdAt) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.createdAt = createdAt;
    }

    public Long getId() { return id; }
    public String getUsername() { return username; }
    public String getEmail() { return email; }
    public Instant getCreatedAt() { return createdAt; }

    @Override
    public boolean equals(Object o) { /* boilerplate */ }

    @Override
    public int hashCode() { /* boilerplate */ }

    @Override
    public String toString() { /* boilerplate */ }
}
```

#### Records with Compact Constructors for Validation

Use compact constructors to add validation logic to records.

```java
// CORRECT: Compact constructor with validation
public record OrderItem(
    String productId,
    int quantity,
    BigDecimal unitPrice
) {
    public OrderItem {
        if (quantity <= 0) {
            throw new IllegalArgumentException("Quantity must be positive");
        }
        Objects.requireNonNull(productId, "productId must not be null");
        Objects.requireNonNull(unitPrice, "unitPrice must not be null");
    }

    public BigDecimal totalPrice() {
        return unitPrice.multiply(BigDecimal.valueOf(quantity));
    }
}
```

```java
// WRONG: Using a canonical constructor when compact will do
public record OrderItem(String productId, int quantity, BigDecimal unitPrice) {
    public OrderItem(String productId, int quantity, BigDecimal unitPrice) {
        if (quantity <= 0) throw new IllegalArgumentException("Quantity must be positive");
        this.productId = productId;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
    }
}
```

#### When Not to Use Records

Do not use records for JPA entities or mutable objects that need setters.

```java
// CORRECT: JPA entity remains a class (records cannot be entities)
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String username;

    // JPA requires no-arg constructor
    protected User() {}

    public User(String username) {
        this.username = username;
    }

    // getters and setters required by JPA
}
```

```java
// WRONG: Record as JPA entity (will not work)
@Entity
public record User(Long id, String username) {}
```

## Sealed Interfaces and Classes

### Use Sealed Interfaces for Restricted Type Hierarchies

Sealed interfaces restrict which classes can implement them, enabling exhaustive pattern matching.

```java
// CORRECT: Sealed interface with permitted subtypes
public sealed interface PaymentResult
    permits PaymentResult.Success, PaymentResult.Declined, PaymentResult.Error {

    record Success(String transactionId, Instant processedAt) implements PaymentResult {}
    record Declined(String reason, String code) implements PaymentResult {}
    record Error(Exception cause) implements PaymentResult {}
}
```

```java
// WRONG: Open interface that should be sealed
public interface PaymentResult {}

public class Success implements PaymentResult {
    private final String transactionId;
    // ...
}

public class Declined implements PaymentResult {
    private final String reason;
    // ...
}
```

#### Sealed Interfaces with Pattern Matching Switch

Combine sealed interfaces with switch expressions for exhaustive handling.

```java
// CORRECT: Exhaustive pattern matching on sealed interface
public String describeResult(PaymentResult result) {
    return switch (result) {
        case PaymentResult.Success s ->
            "Payment processed: " + s.transactionId();
        case PaymentResult.Declined d ->
            "Payment declined: " + d.reason() + " (" + d.code() + ")";
        case PaymentResult.Error e ->
            "Payment error: " + e.cause().getMessage();
    };
}
```

```java
// WRONG: instanceof chain instead of pattern matching
public String describeResult(PaymentResult result) {
    if (result instanceof PaymentResult.Success) {
        PaymentResult.Success s = (PaymentResult.Success) result;
        return "Payment processed: " + s.transactionId();
    } else if (result instanceof PaymentResult.Declined) {
        PaymentResult.Declined d = (PaymentResult.Declined) result;
        return "Payment declined: " + d.reason();
    } else {
        return "Unknown result";
    }
}
```

## Pattern Matching

### Use Pattern Matching for instanceof

Use pattern matching with instanceof to eliminate explicit casts.

```java
// CORRECT: Pattern matching instanceof
public double calculateArea(Shape shape) {
    return switch (shape) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.width() * r.height();
        case Triangle t -> 0.5 * t.base() * t.height();
    };
}
```

```java
// WRONG: Traditional instanceof with cast
public double calculateArea(Shape shape) {
    if (shape instanceof Circle) {
        Circle c = (Circle) shape;
        return Math.PI * c.radius() * c.radius();
    } else if (shape instanceof Rectangle) {
        Rectangle r = (Rectangle) shape;
        return r.width() * r.height();
    }
    throw new IllegalArgumentException("Unknown shape");
}
```

#### Guarded Patterns in Switch

Use guarded patterns with when clauses for conditional matching.

```java
// CORRECT: Guarded pattern matching
public String classifyTemperature(Number temp) {
    return switch (temp) {
        case Integer i when i < 0 -> "freezing";
        case Integer i when i < 15 -> "cold";
        case Integer i when i < 25 -> "comfortable";
        case Integer i -> "hot";
        case Double d when d < 0.0 -> "freezing";
        case Double d -> "measured: " + d;
        default -> "unknown type";
    };
}
```

## Switch Expressions

### Prefer Switch Expressions Over Switch Statements

Use switch expressions to return values directly and ensure exhaustiveness.

```java
// CORRECT: Switch expression with arrow syntax
public BigDecimal applyDiscount(CustomerTier tier, BigDecimal price) {
    BigDecimal discount = switch (tier) {
        case BRONZE -> new BigDecimal("0.05");
        case SILVER -> new BigDecimal("0.10");
        case GOLD -> new BigDecimal("0.15");
        case PLATINUM -> new BigDecimal("0.20");
    };
    return price.multiply(BigDecimal.ONE.subtract(discount));
}
```

```java
// WRONG: Traditional switch statement with fall-through risk
public BigDecimal applyDiscount(CustomerTier tier, BigDecimal price) {
    BigDecimal discount;
    switch (tier) {
        case BRONZE:
            discount = new BigDecimal("0.05");
            break;
        case SILVER:
            discount = new BigDecimal("0.10");
            break;
        default:
            discount = BigDecimal.ZERO;
            break;  // Easy to forget break
    }
    return price.multiply(BigDecimal.ONE.subtract(discount));
}
```

## Virtual Threads

### Use Virtual Threads for I/O-Bound Work

Use virtual threads (Project Loom) for I/O-bound operations instead of platform threads.

```java
// CORRECT: Virtual thread executor for I/O-bound tasks
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<UserProfile>> futures = userIds.stream()
        .map(id -> executor.submit(() -> fetchUserProfile(id)))
        .toList();

    List<UserProfile> profiles = futures.stream()
        .map(f -> {
            try {
                return f.get();
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        })
        .toList();
}
```

```java
// WRONG: Fixed thread pool for I/O-bound work (wastes platform threads)
ExecutorService executor = Executors.newFixedThreadPool(100);
try {
    List<Future<UserProfile>> futures = userIds.stream()
        .map(id -> executor.submit(() -> fetchUserProfile(id)))
        .toList();
    // ...
} finally {
    executor.shutdown();
}
```

#### Virtual Threads in Spring Boot

Configure Spring Boot to use virtual threads for request handling.

```java
// CORRECT: Enable virtual threads in Spring Boot 3.2+
@Configuration
public class VirtualThreadConfig {

    @Bean
    public TomcatProtocolHandlerCustomizer<?> virtualThreadCustomizer() {
        return protocolHandler ->
            protocolHandler.setExecutor(Executors.newVirtualThreadPerTaskExecutor());
    }
}
```

```yaml
# Or via application.yml in Spring Boot 3.2+
spring:
  threads:
    virtual:
      enabled: true
```

## Local Variable Type Inference

### Use var for Local Variables with Clear Types

Use var when the type is obvious from the right-hand side. Never use var when it reduces
readability.

```java
// CORRECT: var with obvious types
var users = new ArrayList<User>();
var response = restTemplate.getForObject(url, UserResponse.class);
var config = loadConfiguration();
var entry = Map.entry("key", "value");

// CORRECT: var in try-with-resources
try (var reader = new BufferedReader(new FileReader(path))) {
    // ...
}

// CORRECT: var in enhanced for loops
for (var user : users) {
    process(user);
}
```

```java
// WRONG: var hides the type and reduces readability
var result = service.process(data);  // What type is result?
var x = calculate(a, b, c);         // Meaningless variable name with var

// WRONG: var with literals where type matters
var count = 0;       // Is this int, long, Integer?
var amount = 3.14;   // Is this float or double?

// WRONG: var with diamond operator (type is lost)
var list = new ArrayList<>();  // ArrayList<Object>, not useful
```

#### Never Use var for Fields or Method Parameters

var is only for local variables, not for fields, method parameters, or return types.

```java
// CORRECT: Explicit types for fields and parameters
public class OrderService {
    private final OrderRepository repository;

    public OrderResponse processOrder(OrderRequest request) {
        var order = repository.save(request.toOrder());  // var OK for local
        return OrderResponse.from(order);
    }
}
```

```java
// WRONG: var cannot be used here (compilation error)
public class OrderService {
    private var repository;  // Compilation error
    public var processOrder(var request) { }  // Compilation error
}
```

## Optional Patterns

### Return Optional Instead of Null

Use Optional for return types where absence is a valid outcome.

```java
// CORRECT: Return Optional for nullable results
public Optional<User> findByEmail(String email) {
    return Optional.ofNullable(
        jdbcTemplate.queryForObject(
            "SELECT * FROM users WHERE email = ?",
            userRowMapper,
            email
        )
    );
}

// CORRECT: Chain Optional operations
public String getUserDisplayName(Long userId) {
    return userRepository.findById(userId)
        .map(User::displayName)
        .orElse("Anonymous");
}
```

```java
// WRONG: Return null when Optional is appropriate
public User findByEmail(String email) {
    // Callers must remember to check for null
    return jdbcTemplate.queryForObject(
        "SELECT * FROM users WHERE email = ?",
        userRowMapper,
        email
    );
}
```

#### Never Use Optional for Fields or Parameters

Optional should only be used as a return type, never as a field type or method parameter.

```java
// CORRECT: Use Optional only as return type
public class UserService {
    public Optional<User> findUser(Long id) {
        return repository.findById(id);
    }
}
```

```java
// WRONG: Optional as field
public class User {
    private Optional<String> middleName;  // Don't do this
}

// WRONG: Optional as parameter
public void updateUser(Optional<String> name) {  // Don't do this
    // ...
}
```

#### Use orElseThrow for Required Values

Use orElseThrow with a meaningful exception for required values.

```java
// CORRECT: orElseThrow with descriptive exception
public User getUser(Long id) {
    return userRepository.findById(id)
        .orElseThrow(() -> new UserNotFoundException("User not found: " + id));
}
```

```java
// WRONG: get() without check (throws NoSuchElementException)
public User getUser(Long id) {
    return userRepository.findById(id).get();  // Unsafe!
}

// WRONG: isPresent/get pattern
public User getUser(Long id) {
    Optional<User> opt = userRepository.findById(id);
    if (opt.isPresent()) {
        return opt.get();  // Use map/orElse/orElseThrow instead
    }
    throw new UserNotFoundException("Not found");
}
```

## Stream API Best Practices

### Prefer Streams for Collection Transformations

Use Stream API for declarative collection processing.

```java
// CORRECT: Stream for filtering and mapping
public List<UserSummary> getActiveUserSummaries() {
    return userRepository.findAll().stream()
        .filter(User::isActive)
        .map(user -> new UserSummary(user.id(), user.displayName()))
        .sorted(Comparator.comparing(UserSummary::displayName))
        .toList();
}
```

```java
// WRONG: Imperative loop for simple transformations
public List<UserSummary> getActiveUserSummaries() {
    List<User> users = userRepository.findAll();
    List<UserSummary> result = new ArrayList<>();
    for (User user : users) {
        if (user.isActive()) {
            result.add(new UserSummary(user.id(), user.displayName()));
        }
    }
    Collections.sort(result, Comparator.comparing(UserSummary::displayName));
    return result;
}
```

#### Use Collectors.toUnmodifiableList for Immutable Results

Prefer toList() (Java 16+) or Collectors.toUnmodifiableList() for immutable results.

```java
// CORRECT: Immutable list result (Java 16+)
List<String> names = users.stream()
    .map(User::name)
    .toList();  // Returns unmodifiable list

// CORRECT: Immutable map result
Map<Long, User> userById = users.stream()
    .collect(Collectors.toUnmodifiableMap(User::id, Function.identity()));
```

```java
// WRONG: Mutable list when immutability is preferred
List<String> names = users.stream()
    .map(User::name)
    .collect(Collectors.toList());  // Mutable list, use toList() instead
```

#### Avoid Complex Stream Chains

Keep stream chains readable. Extract complex operations into methods.

```java
// CORRECT: Break complex chains into named steps
public OrderReport generateReport(List<Order> orders) {
    var completedOrders = filterCompleted(orders);
    var revenueByProduct = calculateRevenueByProduct(completedOrders);
    var topProducts = findTopProducts(revenueByProduct, 10);
    return new OrderReport(topProducts, revenueByProduct);
}

private List<Order> filterCompleted(List<Order> orders) {
    return orders.stream()
        .filter(o -> o.status() == OrderStatus.COMPLETED)
        .toList();
}
```

```java
// WRONG: Overly long stream chain
public OrderReport generateReport(List<Order> orders) {
    return orders.stream()
        .filter(o -> o.status() == OrderStatus.COMPLETED)
        .flatMap(o -> o.items().stream())
        .collect(Collectors.groupingBy(
            OrderItem::productId,
            Collectors.reducing(BigDecimal.ZERO, OrderItem::total, BigDecimal::add)
        ))
        .entrySet().stream()
        .sorted(Map.Entry.<String, BigDecimal>comparingByValue().reversed())
        .limit(10)
        // ... too much in one chain
        .toList();
}
```

## Text Blocks

### Use Text Blocks for Multi-Line Strings

Use text blocks for SQL queries, JSON templates, and other multi-line strings.

```java
// CORRECT: Text block for SQL
String query = """
    SELECT u.id, u.username, u.email
    FROM users u
    JOIN orders o ON u.id = o.user_id
    WHERE o.status = 'ACTIVE'
    ORDER BY u.username
    """;

// CORRECT: Text block for JSON templates
String jsonTemplate = """
    {
        "name": "%s",
        "email": "%s",
        "role": "USER"
    }
    """.formatted(name, email);
```

```java
// WRONG: String concatenation for multi-line content
String query = "SELECT u.id, u.username, u.email " +
    "FROM users u " +
    "JOIN orders o ON u.id = o.user_id " +
    "WHERE o.status = 'ACTIVE' " +
    "ORDER BY u.username";
```

## Immutable Collections

### Prefer Immutable Collections

Use unmodifiable collection factories and avoid exposing mutable internal state.

```java
// CORRECT: Immutable collection factories
List<String> roles = List.of("ADMIN", "USER", "GUEST");
Set<String> permissions = Set.of("READ", "WRITE", "DELETE");
Map<String, Integer> limits = Map.of(
    "FREE", 100,
    "PRO", 1000,
    "ENTERPRISE", 10000
);

// CORRECT: Defensive copy in constructor
public class Config {
    private final List<String> servers;

    public Config(List<String> servers) {
        this.servers = List.copyOf(servers);  // Defensive copy
    }

    public List<String> servers() {
        return servers;  // Already unmodifiable
    }
}
```

```java
// WRONG: Exposing mutable internal state
public class Config {
    private final List<String> servers;

    public Config(List<String> servers) {
        this.servers = servers;  // Caller can modify the list
    }

    public List<String> getServers() {
        return servers;  // Exposes mutable reference
    }
}
```

## Logging with SLF4J

### Use SLF4J with Parameterized Messages

Always use SLF4J for logging with parameterized messages instead of string concatenation.

```java
// CORRECT: SLF4J parameterized logging
private static final Logger log = LoggerFactory.getLogger(UserService.class);

public User createUser(CreateUserRequest request) {
    log.info("Creating user with email={}", request.email());
    try {
        User user = userRepository.save(request.toUser());
        log.info("User created successfully: id={}, email={}", user.id(), user.email());
        return user;
    } catch (DataIntegrityViolationException e) {
        log.warn("Duplicate email detected: email={}", request.email());
        throw new DuplicateEmailException(request.email(), e);
    }
}
```

```java
// WRONG: String concatenation in logging
log.info("Creating user with email=" + request.email());  // Always evaluates

// WRONG: Using System.out for logging
System.out.println("User created: " + user.id());

// WRONG: Wrong log level
log.debug("CRITICAL: Payment failed for order=" + orderId);  // Use error, not debug
```

#### Structured Logging

Use structured logging with key-value pairs for machine-parseable logs.

```java
// CORRECT: Structured logging with MDC
import org.slf4j.MDC;

public OrderResponse processOrder(OrderRequest request) {
    MDC.put("orderId", request.orderId());
    MDC.put("userId", request.userId());
    try {
        log.info("Processing order: amount={}, items={}",
            request.totalAmount(), request.items().size());
        // process...
        log.info("Order processed successfully");
        return response;
    } finally {
        MDC.clear();
    }
}
```

## Spring Dependency Injection

### Use Constructor Injection

Always use constructor injection. Never use field injection with @Autowired.

```java
// CORRECT: Constructor injection (single constructor, @Autowired optional)
@Service
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentGateway paymentGateway;
    private final NotificationService notificationService;

    public OrderService(
            OrderRepository orderRepository,
            PaymentGateway paymentGateway,
            NotificationService notificationService) {
        this.orderRepository = orderRepository;
        this.paymentGateway = paymentGateway;
        this.notificationService = notificationService;
    }
}
```

```java
// WRONG: Field injection
@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private PaymentGateway paymentGateway;

    @Autowired
    private NotificationService notificationService;
}
```

## Spring Configuration Properties

### Use @ConfigurationProperties Over @Value

Prefer type-safe @ConfigurationProperties over scattered @Value annotations.

```java
// CORRECT: Type-safe configuration properties
@ConfigurationProperties(prefix = "app.payment")
public record PaymentProperties(
    String apiKey,
    String apiUrl,
    Duration timeout,
    RetryProperties retry
) {
    public record RetryProperties(
        int maxAttempts,
        Duration delay
    ) {}
}
```

```yaml
# application.yml
app:
  payment:
    api-key: ${PAYMENT_API_KEY}
    api-url: https://api.payment.example.com
    timeout: 30s
    retry:
      max-attempts: 3
      delay: 1s
```

```java
// WRONG: Scattered @Value annotations
@Service
public class PaymentService {
    @Value("${app.payment.api-key}")
    private String apiKey;

    @Value("${app.payment.api-url}")
    private String apiUrl;

    @Value("${app.payment.timeout}")
    private Duration timeout;
}
```

## Spring @Transactional Best Practices

### Apply @Transactional at the Service Layer

Place @Transactional on service methods, not on repository or controller methods.

```java
// CORRECT: @Transactional on service methods
@Service
public class TransferService {
    private final AccountRepository accountRepository;

    public TransferService(AccountRepository accountRepository) {
        this.accountRepository = accountRepository;
    }

    @Transactional
    public TransferResult transfer(Long fromId, Long toId, BigDecimal amount) {
        Account from = accountRepository.findById(fromId)
            .orElseThrow(() -> new AccountNotFoundException(fromId));
        Account to = accountRepository.findById(toId)
            .orElseThrow(() -> new AccountNotFoundException(toId));

        from.debit(amount);
        to.credit(amount);

        accountRepository.save(from);
        accountRepository.save(to);

        return new TransferResult(from.balance(), to.balance());
    }

    @Transactional(readOnly = true)
    public AccountBalance getBalance(Long accountId) {
        return accountRepository.findById(accountId)
            .map(Account::balance)
            .orElseThrow(() -> new AccountNotFoundException(accountId));
    }
}
```

```java
// WRONG: @Transactional on controller
@RestController
public class TransferController {
    @Transactional  // Don't put transactions on controllers
    @PostMapping("/transfer")
    public TransferResult transfer(@RequestBody TransferRequest request) {
        // ...
    }
}
```

#### Understand @Transactional Proxy Gotchas

Internal method calls bypass Spring's proxy, so @Transactional will not apply.

```java
// CORRECT: Separate transactional operations into distinct beans
@Service
public class OrderService {
    private final OrderProcessor orderProcessor;

    public OrderService(OrderProcessor orderProcessor) {
        this.orderProcessor = orderProcessor;
    }

    public void processAndNotify(Order order) {
        orderProcessor.process(order);  // Transaction applied via proxy
        notify(order);
    }
}

@Service
public class OrderProcessor {
    @Transactional
    public void process(Order order) {
        // Transactional work
    }
}
```

```java
// WRONG: Self-invocation skips proxy
@Service
public class OrderService {
    @Transactional
    public void process(Order order) {
        // Transactional work
    }

    public void processAndNotify(Order order) {
        process(order);  // @Transactional NOT applied (self-invocation)
        notify(order);
    }
}
```

## Spring Profiles

### Use Profiles for Environment-Specific Configuration

Use Spring profiles to manage environment-specific configuration.

```yaml
# application.yml (common config)
spring:
  application:
    name: my-service

# application-local.yml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb

# application-prod.yml
spring:
  datasource:
    url: ${DATABASE_URL}
```

```java
// CORRECT: Profile-specific bean
@Configuration
public class CacheConfig {

    @Bean
    @Profile("local")
    public CacheManager localCacheManager() {
        return new ConcurrentMapCacheManager("users", "orders");
    }

    @Bean
    @Profile("prod")
    public CacheManager redisCacheManager(RedisConnectionFactory factory) {
        return RedisCacheManager.builder(factory).build();
    }
}
```

## Try-with-Resources

### Always Use Try-with-Resources for AutoCloseable

Use try-with-resources for any AutoCloseable resource to ensure proper cleanup.

```java
// CORRECT: Try-with-resources
public List<User> readUsersFromCsv(Path csvPath) throws IOException {
    try (var reader = Files.newBufferedReader(csvPath);
         var csvParser = new CSVParser(reader, CSVFormat.DEFAULT.withFirstRecordAsHeader())) {
        return csvParser.getRecords().stream()
            .map(record -> new User(record.get("id"), record.get("name")))
            .toList();
    }
}
```

```java
// WRONG: Manual resource management
public List<User> readUsersFromCsv(Path csvPath) throws IOException {
    BufferedReader reader = null;
    try {
        reader = Files.newBufferedReader(csvPath);
        // process...
    } finally {
        if (reader != null) {
            reader.close();  // Can throw and mask original exception
        }
    }
}
```

## Lombok Conventions

### Follow Project Conventions for Lombok

If the project uses Lombok, follow its established patterns. Prefer records for new projects.

```java
// CORRECT: Lombok when project already uses it
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LegacyUser {
    private Long id;
    private String username;
    private String email;
}

// CORRECT: Lombok @Value for immutable class (pre-records codebase)
@Value
@Builder
public class LegacyUserResponse {
    Long id;
    String username;
    String email;
}
```

```java
// WRONG: Mixing Lombok and records inconsistently in the same project
// Pick one approach and be consistent

// WRONG: @Data on entity without @EqualsAndHashCode exclusion
@Data
@Entity
public class User {
    @Id
    @GeneratedValue
    private Long id;  // id in equals/hashCode causes Hibernate issues
}

// CORRECT: Exclude id from equals/hashCode for entities
@Getter
@Setter
@EqualsAndHashCode(exclude = "id")
@Entity
public class User {
    @Id
    @GeneratedValue
    private Long id;
}
```

## Google Java Style Guide Essentials

### Formatting Rules

Follow the Google Java Style Guide for consistent formatting.

```java
// CORRECT: Google Java Style formatting
public class OrderService {

    private static final Logger log = LoggerFactory.getLogger(OrderService.class);
    private static final int MAX_RETRY = 3;

    private final OrderRepository repository;

    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    public OrderResponse processOrder(OrderRequest request) {
        // 4-space indentation
        // Opening brace on same line
        // One statement per line
        if (request.items().isEmpty()) {
            throw new IllegalArgumentException("Order must have at least one item");
        }

        return switch (request.type()) {
            case STANDARD -> processStandard(request);
            case EXPRESS -> processExpress(request);
            case BULK -> processBulk(request);
        };
    }
}
```

#### Import Ordering

Follow Google Java Style import ordering: static imports first, then regular imports, sorted
alphabetically within groups.

```java
// CORRECT: Import ordering (Google style)
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;

import com.example.domain.Order;
import com.example.repository.OrderRepository;
import java.time.Instant;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;
```

```java
// WRONG: Unsorted or wildcard imports
import java.util.*;
import com.example.domain.*;
import org.springframework.stereotype.Service;
import java.time.Instant;
import com.example.repository.OrderRepository;
```

## Existing Repository Compatibility

### Respect Established Patterns

When contributing to existing repositories, respect their established conventions.

```java
// Check existing patterns before writing code:
// - Look at pom.xml/build.gradle for Java version and dependencies
// - Check for Lombok usage
// - Review existing record vs POJO patterns
// - Follow the existing logging framework
// - Match the existing test framework and patterns
// - Follow the established error handling approach
```

```bash
# Discover project conventions
cat pom.xml | grep java.version      # Java version
grep -r "@Value" src/                  # @Value vs @ConfigurationProperties
grep -r "lombok" pom.xml              # Lombok usage
ls src/test/                           # Test structure
```

This skill ensures Java code follows modern idioms, is maintainable, and leverages the latest
language features available in Java 21+. Apply these rules consistently across all Java projects
while respecting existing project conventions.
