---
name: java-streams
description: "When to activate: Java Stream API, map, filter, reduce, collectors, parallel streams, Optional, records, pattern matching"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: java-kotlin
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Java Stream API & Modern Java Patterns

## Stream Basics

```java
List<String> names = users.stream()
    .filter(User::isActive)
    .sorted(Comparator.comparing(User::getName))
    .map(User::getName)
    .distinct()
    .limit(10)
    .collect(Collectors.toList());

// toList() — immutable, Java 16+
List<String> immutable = users.stream()
    .map(User::getEmail)
    .filter(e -> e.endsWith("@example.com"))
    .toList();
```

## Collectors

```java
// groupingBy
Map<Role, List<User>> byRole = users.stream()
    .collect(Collectors.groupingBy(User::getRole));

// groupingBy with downstream collector
Map<Role, Long> countByRole = users.stream()
    .collect(Collectors.groupingBy(User::getRole, Collectors.counting()));

Map<String, DoubleSummaryStatistics> statsByDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDepartment,
             Collectors.summarizingDouble(Employee::getSalary)));

// partitioningBy
Map<Boolean, List<User>> activeVsInactive = users.stream()
    .collect(Collectors.partitioningBy(User::isActive));

// joining
String csv = users.stream()
    .map(User::getName)
    .collect(Collectors.joining(", ", "[", "]"));

// toMap
Map<Long, User> byId = users.stream()
    .collect(Collectors.toMap(User::getId, Function.identity(),
             (a, b) -> a)); // merge fn handles duplicate keys
```

## Optional

```java
// Chain operations safely
Optional<String> email = Optional.ofNullable(user)
    .filter(User::isActive)
    .map(User::getEmail)
    .filter(e -> e.contains("@"));

// orElseThrow — preferred over get()
User user = userRepo.findById(id)
    .orElseThrow(() -> new ResourceNotFoundException("User " + id));

// ifPresentOrElse
userRepo.findById(id).ifPresentOrElse(
    u -> log.info("Found: {}", u.getName()),
    () -> log.warn("User {} not found", id)
);

// flatMap for Optional<Optional<T>>
Optional<Address> address = userRepo.findById(id)
    .flatMap(User::getAddress);
```

## Records (Java 16+)

```java
public record UserDto(Long id, String name, String email) {
    // Compact constructor for validation
    public UserDto {
        Objects.requireNonNull(name, "name must not be null");
        email = email.toLowerCase().trim();
    }

    // Additional methods allowed
    public String displayName() {
        return name + " <" + email + ">";
    }
}

// Records are automatically: immutable, equals/hashCode/toString, serializable
UserDto dto = new UserDto(1L, "Alice", "ALICE@EXAMPLE.COM");
dto.email(); // "alice@example.com" — normalized by compact constructor
```

## Pattern Matching

```java
// instanceof pattern matching (Java 16+)
Object obj = getShape();
if (obj instanceof Circle c) {
    System.out.println("Area: " + Math.PI * c.radius() * c.radius());
} else if (obj instanceof Rectangle r) {
    System.out.println("Area: " + r.width() * r.height());
}

// Switch pattern matching (Java 21)
double area = switch (shape) {
    case Circle c    -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.width() * r.height();
    case Triangle t  -> 0.5 * t.base() * t.height();
};

// Guarded patterns
String describe = switch (obj) {
    case Integer i when i > 0 -> "positive int: " + i;
    case Integer i when i < 0 -> "negative int: " + i;
    case Integer i             -> "zero";
    case String s              -> "string: " + s;
    case null                  -> "null";
    default                    -> "other: " + obj;
};
```

## Parallel Streams

```java
// Use for CPU-bound, independent, large datasets
long count = largeList.parallelStream()
    .filter(this::expensiveCheck)
    .count();

// Custom ForkJoinPool — avoid blocking common pool
ForkJoinPool pool = new ForkJoinPool(4);
List<Result> results = pool.submit(() ->
    largeList.parallelStream().map(this::process).toList()
).get();

// DON'T parallelize: I/O-bound work, small lists, order-dependent operations
```

## Text Blocks & String Methods (Java 15+)

```java
String json = """
    {
        "name": "%s",
        "email": "%s"
    }
    """.formatted(user.getName(), user.getEmail());

// String methods
"  hello  ".strip();           // Unicode-aware trim
"hello".repeat(3);             // "hellohellohello"
"".isBlank();                  // true (vs isEmpty — handles whitespace)
"a\nb\nc".lines().toList();    // ["a", "b", "c"]
```

## Key Rules
- Use `toList()` (Java 16+) for immutable result lists; `Collectors.toList()` returns a mutable list
- `Optional` is for return types, not method parameters or fields — don't serialize it
- Parallel streams use the common `ForkJoinPool` — never use for blocking I/O; use a custom pool if needed
- `record` replaces Lombok `@Value` for immutable data carriers — prefer it for DTOs
- Pattern matching in `switch` requires exhaustiveness — the compiler enforces this for sealed types
