---
name: code-java
description: Java Standards - Use this skill to learn how to update Java code. This is the Java coding standard that you MUST apply to all your Java code or when you update `.java` files. 
---

# Java Coding Standard

## Core Enforcements

### Annotations (@Override, @Deprecated)

**@Override** mandatory for ALL overridden methods:
```java
@Override
public String toString() {
    return "User{id=" + id + ", name='" + name + '\'' + '}';
}

@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof User)) return false;
    User user = (User) o;
    return Objects.equals(id, user.id) && Objects.equals(name, user.name);
}
```

**@Deprecated** with Javadoc and replacement:
```java
/**
 * @deprecated Use {@link #newMethod()} instead. Removed in v2.0.
 */
@Deprecated(since = "1.5", forRemoval = true)
public void oldMethod() {
    newMethod();
}
```

### Exception Handling

**Rules:** Catch specific exceptions, never generic `Exception`. NO empty catch blocks. ALWAYS log or rethrow with context.

```java
// ✅ CORRECT
try {
    fileReader.readFile(filename);
} catch (FileNotFoundException e) {
    logger.error("Config file not found: {}", filename, e);
    throw new ConfigurationException("Missing config", e);
} catch (IOException e) {
    logger.error("IO error reading: {}", filename, e);
    throw new ApplicationException("Unable to read", e);
}

// ❌ WRONG: Catches everything, empty, or swallows exceptions
try { fileReader.readFile(filename); } 
catch (Exception e) { }  // Masks real issues
```

### Static Member Access

Access via class name, never instance variable:
```java
// ✅ CORRECT
String version = ApplicationConstants.APP_VERSION;

// ❌ WRONG
ApplicationConstants instance = new ApplicationConstants();
String version = instance.APP_VERSION;
```

### Resource Management

Use try-with-resources or Spring lifecycle (@PostConstruct/@PreDestroy):
```java
// ✅ Try-with-resources
try (Connection conn = dataSource.getConnection();
     Statement stmt = conn.createStatement()) {
    ResultSet rs = stmt.executeQuery(sql);
} catch (SQLException e) {
    logger.error("Database error: {}", sql, e);
    throw e;
}

// ✅ Spring lifecycle
@Component
public class DatabaseManager {
    @PostConstruct
    public void initialize() { logger.info("Initializing"); }
    
    @PreDestroy
    public void cleanup() { logger.info("Cleaning up"); }
}
```

### Null Checking & Optional

Prefer Optional for chains; null checks only when necessary:
```java
// ✅ Optional pattern
findByEmail(email)
    .map(User::getName)
    .orElse("Unknown");

// ✅ Null check when needed
if (user != null && user.isActive()) {
    process(user);
}

// ❌ NPE risk
String name = user.getName();  // No null check
```

### Records

Only create records for lambda expressions; never for DTO classes.

### Lombok

- Never create constructors on classes in Lombok enabled projects; use Lombok annotations like @AllArgsConstructor, @NoArgsConstructor, or @RequiredArgsConstructor instead.
- Multiple constructors required? Create specific beans instead of adding multiple constructors.

---

## Javadoc Requirements (Mandatory)

ALL public classes and methods REQUIRE Javadoc with complete tags:

```java
/**
 * Authenticates user with credentials.
 * Validates username/password against auth service.
 * Generates and stores session token on success.
 *
 * @param username login name (non-null, non-empty)
 * @param password password (non-null, non-empty)
 * @return true if auth successful, false if invalid
 * @throws AuthenticationException if service unavailable
 * @throws IllegalArgumentException if username/password null/empty
 */
public boolean authenticate(String username, String password) 
    throws AuthenticationException { }
```

**Mandatory Tags:** @param (all params), @return (if not void), @throws (checked exceptions), @deprecated (with replacement), @since (version)

---

## SonarQube Critical Rules (Enforced)

**S1161:** Missing @Override annotation
```java
// ❌ WRONG
class Child extends Parent {
    public String toString() { return "child"; }
}

// ✅ CORRECT
class Child extends Parent {
    @Override
    public String toString() { return "child"; }
}
```

**S2097:** Unsafe equals() - missing instanceof check
```java
// ❌ WRONG
@Override
public boolean equals(Object obj) {
    User user = (User) obj;  // No type check!
    return Objects.equals(id, user.id);
}

// ✅ CORRECT
@Override
public boolean equals(Object obj) {
    if (!(obj instanceof User)) return false;
    User user = (User) obj;
    return Objects.equals(id, user.id);
}
```

**S2737:** Catch doing nothing but rethrowing
```java
// ❌ WRONG - catch should do more
try {
    operation();
} catch (IOException e) {
    throw e;
}

// ✅ CORRECT
try {
    operation();
} catch (IOException e) {
    logger.error("IO operation failed", e);
    throw new ApplicationException("Operation failed", e);
}
```

### Spring-Specific Critical Rules

**S6829/S6818:** Single constructor injection, @Autowired not needed
```java
// ✅ CORRECT
@Service
public class UserService {
    private final UserRepository repository;
    
    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}
```

**S6838:** @Bean methods must inject dependencies, not call directly
```java
// ❌ WRONG
@Bean
public Component component() {
    return new Component(service1());  // Direct call
}

// ✅ CORRECT
@Bean
public Component component(Service service1) {  // Inject via parameter
    return new Component(service1);
}
```

**S7184:** @Scheduled methods must have no arguments
```java
// ✅ CORRECT
@Scheduled(fixedRate = 5000)
public void scheduledTask() { }
```

### SonarQube Quality Gates

| Metric | Threshold | Action |
|--------|-----------|--------|
| Critical Bugs | 0 | Block deployment |
| Security Vulnerabilities | 0 | Block deployment |
| Cyclomatic Complexity | ≤ 5 per method | Refactor if exceeded |

---

## Spring Patterns

### Service Layer
```java
@Service
@Transactional
public class UserService {
    private static final Logger logger = LoggerFactory.getLogger(UserService.class);
    private final UserRepository repository;
    
    public UserService(UserRepository repository) {
        this.repository = repository;
    }
    
    /**
     * Creates new user account.
     * @param userDTO user data (non-null)
     * @return created user
     * @throws ValidationException if data invalid
     */
    public User createUser(UserDTO userDTO) {
        if (userDTO == null || userDTO.getEmail() == null) {
            throw new ValidationException("Invalid user data");
        }
        User user = new User();
        user.setEmail(userDTO.getEmail());
        repository.save(user);
        logger.info("User created: {}", user.getId());
        return user;
    }
    
    public Optional<User> getUserById(Long userId) {
        return repository.findById(userId);
    }
}
```

### Controller Layer
```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    private final UserService userService;
    
    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<UserDTO> getUserById(@PathVariable Long id) {
        return userService.getUserById(id)
            .map(user -> ResponseEntity.ok(mapToDTO(user)))
            .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<UserDTO> createUser(@RequestBody UserDTO userDTO) {
        User created = userService.createUser(userDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(mapToDTO(created));
    }
    
    private UserDTO mapToDTO(User user) {
        UserDTO dto = new UserDTO();
        dto.setId(user.getId());
        dto.setEmail(user.getEmail());
        return dto;
    }
}
```

---

## Code Review Checklist

- [ ] All overridden methods have @Override
- [ ] All deprecated methods documented with replacement
- [ ] Exception handling: specific exceptions, no generic Exception, no empty catch blocks
- [ ] All exceptions logged or rethrown with context
- [ ] Javadoc on all public classes/methods with @param, @return, @throws
- [ ] Static members accessed via class name, not instance
- [ ] Resources use try-with-resources or Spring lifecycle
- [ ] Null-safe: Optional for chains, null checks for single values
- [ ] SonarQube warnings addressed (S1161, S2097, S2737, S6829, S6838, S7184)
- [ ] No duplicate code
- [ ] Cyclomatic complexity ≤ 5 per method

---

## Key Takeaways

1. **@Override** mandatory for every overridden method
2. **Exception handling** specific, logged, never empty
3. **Javadoc** with @param, @return, @throws required for all public APIs
4. **Optional** for null-safe chains; null checks for single values
5. **Resources** managed via try-with-resources or Spring lifecycle
6. **SonarQube** blocks deployment on critical bugs (S1161, S2097, S2737)
7. **Spring rules** enforce proper @Bean invocation, @Scheduled args, single constructor injection
8. **Static** members accessed via class name
9. **Cyclomatic complexity** ≤ 5 per method
10. **Code review** checklist used on every pull request

---

**Document Status:** BMW Java Coding Standard  
**Last Updated:** Current  
**Audience:** BMW Java Developers, Backend Engineers
