---
name: java-expert
description: Expert knowledge for Modern Java (21+) development, including Virtual Threads, performance tuning, and idiomatic clean code. Use for deep Java language/logic questions.
version: 1.2.0
keywords: [java, jdk21, virtual-threads, performance, jvm, backend]
---

# java-expert

> Keyword: java | Platforms: gemini,claude,codex

High-Performance Modern Java Expert Skill - Specialized in Java 21+ and cloud-native architecture.

## Core Mandates

- **Google Java Style:** Strictly adhere to the [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) for formatting, naming, and structure.
- **Java 21+ First:** Mandate `var` (LVTI) where readable, Records for DTOs, and Pattern Matching for `instanceof` and `switch`.
- **Concurrency:** Prefer Virtual Threads (`@RunOnVirtualThread` in Quarkus or `Executors.newVirtualThreadPerTaskExecutor()`) over traditional Thread Pools for I/O-bound tasks.
- **Immutability:** Use `record`, `final` fields, and `unmodifiable` collections (`List.of`, `Map.of`).
- **Functional Style:** Leverage Streams, `Optional`, and Functional Interfaces to reduce boilerplate and side effects.
- **Visibility:** Default to `package-private` or `private`. Only `public` what must be exposed (API/SPI).

## Virtual Threads (Project Loom)

### When to Use Virtual Threads

```
Is the task I/O-bound (DB queries, HTTP calls, file reads)?
  YES → Virtual Threads (scales to millions of concurrent tasks)
  NO → Is it CPU-bound (crypto, compression, ML inference)?
    YES → Platform Threads with ForkJoinPool (work-stealing)
    NO → Is it reactive streaming with backpressure?
      YES → Mutiny / Vert.x (Reactive Streams)
      NO → Virtual Threads (default choice for most workloads)
```

### Patterns

```java
// PATTERN 1: Simple virtual thread executor
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<String>> futures = urls.stream()
        .map(url -> executor.submit(() -> fetchUrl(url)))
        .toList();

    List<String> results = futures.stream()
        .map(f -> { try { return f.get(); } catch (Exception e) { throw new RuntimeException(e); } })
        .toList();
}

// PATTERN 2: Structured Concurrency (Preview in 21, stable in 25)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var userTask  = scope.fork(() -> userService.findById(id));
    var orderTask = scope.fork(() -> orderService.findByUser(id));
    scope.join().throwIfFailed();
    return new UserProfile(userTask.get(), orderTask.get());
}

// PATTERN 3: Quarkus integration
@Path("/users")
public class UserResource {
    @GET
    @RunOnVirtualThread  // Offloads blocking call to virtual thread
    public List<User> list() {
        return User.listAll();  // Blocking Panache call - safe on VT
    }
}
```

### Anti-Patterns

```java
// BAD - synchronized blocks pin virtual threads to carrier threads
synchronized (lock) {
    var result = db.query("SELECT ...");  // Pins carrier thread!
}

// GOOD - use ReentrantLock instead (does not pin)
lock.lock();
try {
    var result = db.query("SELECT ...");
} finally {
    lock.unlock();
}

// BAD - ThreadLocal with large state on virtual threads (millions of VTs = millions of copies)
private static final ThreadLocal<ExpensiveCache> cache = ThreadLocal.withInitial(ExpensiveCache::new);

// GOOD - use ScopedValue (Preview) or shared concurrent structure
private static final ScopedValue<RequestContext> CONTEXT = ScopedValue.newInstance();

void handleIncoming(RequestContext ctx) {
    ScopedValue.runWhere(CONTEXT, ctx, () -> handleRequest());
}

// BAD - pooling virtual threads (defeats the purpose)
ExecutorService pool = Executors.newFixedThreadPool(100);  // Platform threads only!

// GOOD - create virtual threads freely, they are cheap
ExecutorService vt = Executors.newVirtualThreadPerTaskExecutor();
```

## Records

```java
// PATTERN: Record as immutable DTO with validation
public record CreateUserRequest(
    @NotBlank String name,
    @Email String email,
    @Min(18) int age
) {
    // Compact constructor for validation
    public CreateUserRequest {
        name = name.strip();
        email = email.toLowerCase();
    }
}

// PATTERN: Record with derived fields
public record Money(BigDecimal amount, Currency currency) {
    public Money add(Money other) {
        if (!currency.equals(other.currency)) throw new IllegalArgumentException("Currency mismatch");
        return new Money(amount.add(other.amount), currency);
    }
}

// ANTI-PATTERN: Don't use records for mutable entities
// BAD - records are immutable, JPA entities need mutability
@Entity
public record User(Long id, String name) {}  // Won't work with Hibernate

// GOOD - use class for JPA entities
@Entity
public class User {
    @Id @GeneratedValue private Long id;
    private String name;
}
```

## Pattern Matching

### instanceof Pattern Matching

```java
// BAD - old style with explicit cast
if (shape instanceof Circle) {
    Circle c = (Circle) shape;
    return Math.PI * c.radius() * c.radius();
}

// GOOD - pattern variable binding
if (shape instanceof Circle c) {
    return Math.PI * c.radius() * c.radius();
}

// GOOD - guarded patterns
if (shape instanceof Circle c && c.radius() > 0) {
    return Math.PI * c.radius() * c.radius();
}
```

### Switch Pattern Matching (Java 21 - finalized)

```java
// Exhaustive switch with sealed types
sealed interface Shape permits Circle, Rectangle, Triangle {}
record Circle(double radius) implements Shape {}
record Rectangle(double w, double h) implements Shape {}
record Triangle(double base, double height) implements Shape {}

double area(Shape shape) {
    return switch (shape) {
        case Circle c    -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.w() * r.h();
        case Triangle t  -> 0.5 * t.base() * t.height();
        // No default needed - compiler ensures exhaustiveness
    };
}

// Guarded patterns with when
String classify(Object obj) {
    return switch (obj) {
        case Integer i when i < 0  -> "negative";
        case Integer i when i == 0 -> "zero";
        case Integer i             -> "positive";
        case String s when s.isBlank() -> "blank string";
        case String s              -> "string: " + s;
        case null                  -> "null";
        default                    -> "unknown: " + obj.getClass();
    };
}
```

## Sealed Classes

```java
// PATTERN: Domain modeling with sealed hierarchy
public sealed interface PaymentMethod permits CreditCard, BankTransfer, Wallet {
    BigDecimal maxAmount();
}

public record CreditCard(String number, YearMonth expiry) implements PaymentMethod {
    public BigDecimal maxAmount() { return new BigDecimal("10000"); }
}
public record BankTransfer(String iban) implements PaymentMethod {
    public BigDecimal maxAmount() { return new BigDecimal("1000000"); }
}
public record Wallet(String walletId, BigDecimal balance) implements PaymentMethod {
    public BigDecimal maxAmount() { return balance; }
}

// Compiler enforces exhaustiveness - adding a new PaymentMethod
// will cause compile errors wherever a switch doesn't cover it
String processPayment(PaymentMethod method, BigDecimal amount) {
    return switch (method) {
        case CreditCard cc   -> chargeCard(cc, amount);
        case BankTransfer bt -> initTransfer(bt, amount);
        case Wallet w        -> debitWallet(w, amount);
    };
}
```

## Migration Guide: Java 11/17 → 21

### Key Changes by Version

| Feature | Java 11 | Java 17 | Java 21 |
|---------|---------|---------|---------|
| Text blocks | ❌ | ✅ `"""..."""` | ✅ |
| Records | ❌ | ✅ | ✅ |
| Sealed classes | ❌ | ✅ (final) | ✅ |
| Pattern matching instanceof | ❌ | ✅ (final) | ✅ |
| Switch pattern matching | ❌ | ❌ (preview) | ✅ (final) |
| Virtual Threads | ❌ | ❌ | ✅ (final) |
| Sequenced Collections | ❌ | ❌ | ✅ |
| String templates | ❌ | ❌ | Preview |

### Common Migration Patterns

```java
// Java 11 → 21: Replace verbose instanceof chains
// BEFORE (Java 11)
if (event instanceof OrderCreated) {
    OrderCreated e = (OrderCreated) event;
    handle(e);
} else if (event instanceof OrderCancelled) {
    OrderCancelled e = (OrderCancelled) event;
    cancel(e);
}

// AFTER (Java 21)
switch (event) {
    case OrderCreated e   -> handle(e);
    case OrderCancelled e -> cancel(e);
    default -> log.warn("Unknown event: {}", event);
}

// Java 11 → 21: Replace DTOs with Records
// BEFORE
public class UserDto {
    private final String name;
    private final String email;
    public UserDto(String name, String email) { this.name = name; this.email = email; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    // equals, hashCode, toString...
}

// AFTER
public record UserDto(String name, String email) {}

// Java 11 → 21: Replace Thread pools for I/O tasks
// BEFORE
ExecutorService pool = Executors.newFixedThreadPool(200);
Future<String> f = pool.submit(() -> httpClient.send(req).body());

// AFTER
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<String> f = executor.submit(() -> httpClient.send(req).body());
}
```

### Migration Gotchas

- **`finalize()` removed** → use `Cleaner` or try-with-resources
- **Security Manager removed** → migrate to other security mechanisms
- **Nashorn removed (Java 15)** → use GraalVM polyglot for JS
- **Applet API removed** → N/A for server-side
- **`Thread.stop()` throws UOE** → use interruption pattern with `Thread.interrupt()`

## Architectural Patterns

### Hexagonal / Clean Architecture
- **Domain:** Pure Java, zero external dependencies (no Quarkus/Spring in domain classes).
- **Ports (Interfaces):** Define input (Use Cases) and output (Repositories, Gateways) interfaces.
- **Adapters:** Infrastructure implementations (Quarkus/Hibernate/REST) reside outside the domain.

### Performance & Memory
- **Garbage Collection:** Favor **G1GC** for typical workloads or **ZGC** for ultra-low latency (<1ms).
- **Memory Management:** Minimize object allocation in hot loops. Use `StringBuilder` instead of `+` in loops.
- **Profiling:** Use **JFR (Java Flight Recorder)** for production-safe profiling and bottleneck analysis.

### GC Decision Tree

```
Workload type?
  General server (most cases) → G1GC (-XX:+UseG1GC, default in JDK 21)
  Ultra-low latency (<1ms pause) → ZGC (-XX:+UseZGC)
  Small heap (<256MB), short-lived → SerialGC (-XX:+UseSerialGC)
  Native Image (GraalVM) → SerialGC (default) or G1 (--gc=G1)
  High throughput batch → G1GC with large heap + tuned regions
```

## Testing Strategy

- **JUnit 5 & AssertJ:** The industry standard for fluent, readable assertions.
- **Mockito:** Deep stubbing and spying for complex dependencies.
- **ArchUnit:** Enforce architectural rules (e.g., "Domain must not depend on Infrastructure").
- **Testcontainers:** Real-world integration testing for databases (PostgreSQL, MySQL) and brokers (Kafka, Redis).

## Bytecode & Classloading

- **Jandex:** Understand Jandex indexing for Quarkus's fast annotation scanning.
- **Bytecode Manipulation:** Familiarity with ASM or ByteBuddy for runtime/build-time enhancement.
- **ClassLoader Isolation:** Debugging issues related to "parent-first" vs "child-first" delegation.

## Expert Tips

- Avoid `System.out.println()`; always use a logger (SLF4J/Logback).
- Prefer `Interface-based` design for testability.
- Use `Sealed Classes` to define closed hierarchy types for better exhaustiveness checking in `switch`.
- Use `List.copyOf()` / `Map.copyOf()` to defensively copy mutable collections in public APIs.
- Prefer `Optional.orElseThrow()` over `Optional.get()` (never call `.get()` without `.isPresent()`).

## 🌐 Java Knowledge Sources

> **Directive:** Use `web_fetch` to find the latest JDK 21+ features, JEP details, or performance tuning flags (G1GC, ZGC) before giving architecture advice.

- **JDK 21 Release Notes:** [Java 21 Documentation](https://docs.oracle.com/en/java/javase/21/relnotes/) - Breaking changes and new APIs.
- **Coding Standards:** [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) - Formatting, naming, and whitespace conventions.
- **Virtual Threads (Project Loom):** [JEP 444](https://openjdk.org/jeps/444) - Comprehensive guide to Virtual Threads.
- **Modern Concurrency:** [Structured Concurrency (JEP 453)](https://openjdk.org/jeps/453) - Managing subtasks.
- **Performance Tuning:** [HotSpot Virtual Machine Garbage Collection](https://docs.oracle.com/en/java/javase/21/gctuning/) - Tuning G1 and ZGC.

## References

- [Official Java SE Documentation](https://docs.oracle.com/en/java/javase/21/)
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [Effective Java (Joshua Bloch)](https://www.oreilly.com/library/view/effective-java-3rd-edition/9780134686097/)
- [Java Flight Recorder (JFR) Reference](https://docs.oracle.com/en/java/javase/21/jdkapi/java-flight-recorder.html)
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)

## Skill Interoperability

The **java-expert** ☕ skill provides the foundational language expertise (JDK 21+, Virtual Threads) required by:
- **vertx-expert** 🌀: Uses modern Java for high-performance reactive programming.
- **quarkus-expert** ⚡: Leverages the JVM features for the Quarkus framework.
