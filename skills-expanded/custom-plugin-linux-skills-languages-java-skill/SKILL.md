---
name: java
description: Java development skill - Modern Java 21+, Spring Boot, enterprise patterns
version: "1.0.0"
sasmp_version: "1.3.0"

input_schema:
  type: object
  properties:
    task: { type: string, enum: [code, debug, explain, optimize, review] }
    framework: { type: string, enum: [spring, quarkus, micronaut, vanilla] }
  required: [task]

output_schema:
  type: object
  properties:
    solution: { type: string }
    dependencies: { type: array }

retry_config:
  max_attempts: 3
  backoff: exponential

timeout_ms: 30000
---

# Java Skill

## PURPOSE
Enterprise Java development with modern features and frameworks.

## CORE COMPETENCIES
```
Java 21+ Features:
├── Virtual threads
├── Pattern matching
├── Record classes
├── Sealed classes
└── Switch expressions

Spring Boot 3:
├── Native compilation
├── Observability
├── WebFlux (reactive)
└── Data JPA
```

## CODE PATTERNS

### Service Pattern
```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository repository;

    @Transactional(readOnly = true)
    public Optional<User> findById(Long id) {
        return repository.findById(id);
    }

    @Retryable(maxAttempts = 3)
    public User create(CreateUserRequest req) {
        return repository.save(mapper.toEntity(req));
    }
}
```

## TROUBLESHOOTING

| Issue | Cause | Solution |
|-------|-------|----------|
| OutOfMemoryError | Heap exhaustion | Tune JVM, check leaks |
| N+1 queries | Lazy loading | Use fetch joins |

## TESTING
```java
@SpringBootTest
class UserServiceTest {
    @MockBean
    private UserRepository repository;

    @Test
    void shouldFindUser() {
        given(repository.findById(1L)).willReturn(Optional.of(user));
        var result = service.findById(1L);
        assertThat(result).isPresent();
    }
}
```
