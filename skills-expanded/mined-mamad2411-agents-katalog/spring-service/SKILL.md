---
name: spring-service
description: Generate a Spring Boot service class for a named entity with constructor injection, logging, exception handling, and unit tests. Invoke as /spring-service <Entity>.
paths:
  - "**/*.java"
user-invocable: true
---

# Spring Service Scaffold

Generate a `$ARGUMENTS`Service with:

- `@Service` annotation
- Constructor injection of `$ARGUMENTS`Repository (no field `@Autowired`)
- CRUD methods: `findAll()`, `findById(id)`, `create(request)`, `update(id, request)`, `delete(id)`
- Domain exceptions (e.g., `EntityNotFoundException`) thrown for missing-by-id; let `@ControllerAdvice` translate to HTTP if present
- SLF4J logging at meaningful boundaries — entry on writes, warn on validation rejection, debug on reads
- Unit tests using JUnit 5 + Mockito, with `@MockitoBean` and `@MockitoSpyBean` where appropriate
- Use modern Java idioms (records for DTOs, pattern matching, `var` where readable)

## Constraints

- Match the existing project package layout
- Don't introduce `Lombok` if the project doesn't already use it
- If the project uses MapStruct, generate a mapper interface; otherwise, write the mapping inline
- Tests should cover happy path, not-found, and at least one validation/edge case per write method

**Usage:** `/spring-service User` → `UserService`, `UserServiceTest`
