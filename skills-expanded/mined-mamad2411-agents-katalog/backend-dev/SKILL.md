---
name: backend-dev
description: >
  Backend development skill for APIs, databases, server logic, and microservices. Use when the user
  needs API endpoints, database schemas, migrations, CRUD operations, authentication/authorization
  logic, business logic implementation, queue/worker setup, caching, ORM models, REST/GraphQL APIs,
  WebSocket handlers, or any server-side code. Trigger on: "API", "endpoint", "database", "migration",
  "model", "controller", "service", "middleware", "auth", "REST", "GraphQL", "query", "ORM",
  "backend", "server", "microservice", "queue", "cache", "redis", "postgres", "mongo", or server-side work.
---

# Backend Developer

## Stack
**Java 21 · Spring Boot 3.4 · Spring Data JPA · Spring Security · Flyway · MapStruct 1.6.3 · Lombok 1.18.34 · PostgreSQL (prod) / H2 (dev) · Maven**

## Before Writing Code
1. Read the existing structure under `backend/src/main/java/com/lawfirm/`
2. Follow the Hexagonal Architecture strictly: `domain → application → infrastructure → presentation`
3. **YAGNI**: build only the endpoints/models needed for the current feature — no future-proofing
4. Check the latest Flyway migration version: `backend/src/main/resources/db/migration/` (currently V62)

## Hexagonal Architecture Rules
```
domain/         ← Entities, Repository interfaces, Specifications — NO framework imports
application/    ← DTOs, MapStruct Mappers, Service implementations
infrastructure/ ← Security, JPA repository impls, Config beans
presentation/   ← REST Controllers, GlobalExceptionHandler, DTOs validation
```
- **NO business logic in Controllers or Entities** — services only
- **NO manual mapping** — MapStruct only (`@Mapper(componentModel = "spring")`)
- **NO `hibernate.ddl-auto=update`** — Flyway migrations only

## Mandatory Patterns

### Entity (domain layer)
```java
@Entity
@Table(name = "example")
@Getter @Setter @NoArgsConstructor
public class Example extends BaseEntity {   // extends BaseEntity for id/version/createdAt/updatedAt
    @Column(nullable = false, unique = true)
    private String name;
}
```

### DTO + Validation (application layer)
```java
public record ExampleRequest(
    @NotBlank String name,
    @Email String email
) {}
```

### MapStruct Mapper (application layer — ONLY way to map)
```java
@Mapper(componentModel = "spring")
public interface ExampleMapper {
    ExampleResponse toResponse(Example entity);
    Example toEntity(ExampleRequest request);
}
```

### Service (application layer)
```java
@Service @RequiredArgsConstructor @Transactional
public class ExampleService {
    private final ExampleRepository repository;
    private final ExampleMapper mapper;

    public ExampleResponse findById(Long id) {
        return repository.findById(id)
            .map(mapper::toResponse)
            .orElseThrow(() -> new ResourceNotFoundException("Example", id));
    }
}
```

### Controller (presentation layer)
```java
@RestController @RequestMapping("/api/examples")
@RequiredArgsConstructor @Tag(name = "Examples")
public class ExampleController {
    private final ExampleService service;

    @GetMapping("/{id}")
    @PreAuthorize("hasAuthority('EXAMPLE_READ')")
    public ResponseEntity<ExampleResponse> getById(@PathVariable Long id) {
        return ResponseEntity.ok(service.findById(id));
    }
}
```

### Flyway Migration (always next version)
```sql
-- backend/src/main/resources/db/migration/V63__description.sql
-- IMPORTANT: File must use LF line endings (not CRLF) to prevent checksum errors
CREATE TABLE examples (
    id         BIGSERIAL PRIMARY KEY,
    name       VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    version    BIGINT       NOT NULL DEFAULT 0
);
```

## API Design Checklist
- [ ] RESTful naming: nouns for resources, HTTP verbs for actions (`/api/users`, not `/api/getUsers`)
- [ ] Input validation with Bean Validation (`@NotBlank`, `@Email`, `@Size`)
- [ ] Proper HTTP status codes (201 Created, 404 Not Found, 409 Conflict)
- [ ] Pagination for list endpoints (Spring Pageable)
- [ ] `@PreAuthorize("hasAuthority('...')")` on protected endpoints
- [ ] OpenAPI annotations (`@Tag`, `@Operation`, `@ApiResponse`)
- [ ] Errors via `ResourceNotFoundException` (404) or `DuplicateResourceException` (409)

## Exception Handling
Use existing exception classes in `presentation/`:
```java
throw new ResourceNotFoundException("User", id);         // → 404
throw new DuplicateResourceException("User", "email");   // → 409
// GlobalExceptionHandler catches all — no try/catch in controllers
```

## JPA Repository Rules
```java
// Use JOIN FETCH to prevent N+1 — never lazy-load in loops
@Query("SELECT u FROM User u LEFT JOIN FETCH u.roles WHERE u.id = :id")
Optional<User> findByIdWithRoles(@Param("id") Long id);
```

## Performance Checklist
- [ ] N+1 prevention: use `JOIN FETCH` or `@EntityGraph`
- [ ] Pagination on all list endpoints (`Pageable pageable`)
- [ ] Index foreign keys in Flyway migration
- [ ] Soft delete for user-facing data (`deleted = true`, not hard delete)

## Verification Commands
```bash
# Backend (run in /backend)
mvn clean compile          # Check for compilation errors + MapStruct generation
mvn test                   # Run unit tests
mvn verify                 # Full build + Checkstyle + SpotBugs + JaCoCo (70% required)
mvn spring-boot:run        # Start with H2 (dev profile)
```

## Handoff Points
- **← From Tech Lead**: API specs, architecture decisions, ADR
- **← From DBA**: Schema, Flyway migration files, optimized queries
- **→ DBA**: Request schema design, query optimization, migration review
- **→ Frontend Dev**: API contracts (endpoint URLs, request/response JSON shapes)
- **→ Tester**: Endpoint list for integration testing, expected status codes
- **→ Security Engineer**: Auth/authorization review for new endpoints
- **→ DevOps**: New env vars needed, DB changes, infra requirements
