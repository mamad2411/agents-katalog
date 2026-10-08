# Eval: Java Security Hardening

## Prompt

Review and harden this Spring Boot endpoint and repository code. Fix authentication, authorization, input validation, and query safety. Add focused tests for the security behavior you enforce.

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserRepository userRepository;

    public UserController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @GetMapping("/{id}")
    public UserEntity getUser(@PathVariable String id) {
        return userRepository.findByNativeQuery("SELECT * FROM users WHERE id = " + id);
    }

    @PostMapping
    public UserEntity create(@RequestBody Map<String, String> body) {
        UserEntity user = new UserEntity();
        user.setEmail(body.get("email"));
        user.setPassword(body.get("password"));
        user.setRole(body.getOrDefault("role", "USER"));
        log.info("Created user email={} password={}", user.getEmail(), user.getPassword());
        return userRepository.save(user);
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("permitAll()")
    public void delete(@PathVariable Long id) {
        userRepository.deleteById(id);
    }
}
```

## Expected Agent Behavior

- Identifies missing authentication on sensitive endpoints and unsafe native SQL concatenation
- Replaces map-based input with validated DTOs and removes password logging
- Fixes authorization on delete (admin-only or owner-scoped, not `permitAll()`)
- Uses parameterized queries or Spring Data methods
- Adds tests for forbidden access and SQL injection regression where practical
- Summarizes threats fixed, residual risks, and verification commands

## Failure Signals

- Adds security annotations without server-side authorization checks in the service layer when reused
- Logs credentials or tokens after "fixing" the controller
- Uses string formatting for SQL with user input
- Disables CSRF globally without explaining the API auth model
- Returns stack traces or query text in error responses
