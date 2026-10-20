---
name: java-refactoring
description: Analyze and refactor Java/Spring Boot code for quality, maintainability, and design patterns. Use this skill whenever the user shares Java code and asks to improve it, clean it up, apply design patterns, reduce complexity, fix code smells, or says things like "refactor this", "clean up this class", "this method is too long", "apply SOLID principles", "improve this service", "simplify this code". Always use this skill before suggesting any Java code improvements — it defines the standards and patterns to apply.
---

# Java Refactoring Skill

Systematically analyze Java/Spring Boot code and apply targeted refactoring following SOLID principles, clean code practices, and Java idioms.

## Refactoring Analysis Framework

When given code to refactor, evaluate in this order:

### 1. Code Smells to Detect

| Smell | Signal | Refactoring |
|-------|--------|-------------|
| Long Method | >20 lines | Extract Method |
| God Class | >300 lines, >10 responsibilities | Extract Class |
| Feature Envy | Method uses another class's data more than its own | Move Method |
| Data Clumps | Same 3+ params repeated | Introduce Parameter Object |
| Primitive Obsession | String for email/phone/status | Value Object / Enum |
| Switch Statements | `switch` on type field | Strategy or Polymorphism |
| Duplicate Code | Copy-paste blocks | Extract Method / Template Method |
| Long Parameter List | >3-4 params | Builder or Parameter Object |
| Null Checks Everywhere | `if (x != null)` chains | Optional<T> |
| Mutable State | public setters everywhere | Immutable objects / Builder |

### 2. SOLID Violations to Fix

**S - Single Responsibility**
- A class/method should do ONE thing
- Signal: class name contains "And", "Manager", "Handler", "Util" doing 5 things
- Fix: split into focused classes

**O - Open/Closed**
- Signal: `if/else` or `switch` on type that requires editing when adding new types
- Fix: Strategy pattern, polymorphism

**L - Liskov Substitution**
- Signal: overridden method throws `UnsupportedOperationException`
- Fix: redesign inheritance hierarchy

**I - Interface Segregation**
- Signal: interfaces with 10+ methods, implementations throwing `UnsupportedOperationException`
- Fix: split into focused interfaces

**D - Dependency Inversion**
- Signal: `new ConcreteService()` inside a class, no constructor injection
- Fix: inject abstractions via `@Autowired` constructor injection

### 3. Java/Spring-Specific Improvements

**Use Modern Java (11–21)**
```java
// Before
List<String> names = new ArrayList<>();
for (User user : users) {
    if (user.isActive()) names.add(user.getName());
}

// After
List<String> names = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .toList(); // Java 16+
```

**Prefer Optional over null**
```java
// Before
User user = userRepository.findById(id);
if (user == null) throw new NotFoundException(...);

// After
User user = userRepository.findById(id)
    .orElseThrow(() -> new ResourceNotFoundException("User", id));
```

**Replace magic strings/numbers with constants or enums**
```java
// Before
if (user.getRole().equals("ADMIN")) { ... }

// After
if (user.getRole() == Role.ADMIN) { ... }
```

**Constructor injection over field injection**
```java
// Before (avoid)
@Autowired
private UserService userService;

// After (prefer)
private final UserService userService;

public UserController(UserService userService) {
    this.userService = userService;
}
```

## Refactoring Output Format

For each refactoring, provide:

1. **Problem identified**: What the issue is and why it matters
2. **Before code**: The original snippet
3. **After code**: The refactored version
4. **Pattern applied**: Name of the refactoring or design pattern used
5. **Impact**: Testability / readability / maintainability improvement

## Priority Order

When multiple issues exist, fix in this order:
1. Security issues (hardcoded credentials, SQL injection risk)
2. Correctness bugs (NPE risks, thread safety)
3. Design violations (God classes, tight coupling)
4. Readability (long methods, naming)
5. Style (stream API, modern syntax)

## What NOT to Refactor

- Don't over-engineer simple code with unnecessary patterns
- Don't introduce abstraction layers for a single implementation
- Don't convert working loops to streams if it reduces readability
- Preserve existing public API signatures unless user explicitly asks to change them
