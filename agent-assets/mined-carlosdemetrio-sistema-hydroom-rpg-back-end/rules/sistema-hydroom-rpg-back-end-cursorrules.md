# Cursor AI Rules - Ficha Controlador Backend

## Project Overview
Sistema de gerenciamento de fichas RPG com Spring Boot + PostgreSQL + OAuth2.

## Documentation
**ALWAYS CONSULT**: `/docs/AI_GUIDELINES_BACKEND.md` and `/docs/backend/`

Quick links:
- Architecture: `/docs/backend/01-architecture.md`
- Security: `/docs/backend/08-security.md` + `/docs/backend/11-owasp-security.md`
- Testing: `/docs/backend/09-testing.md`

## Tech Stack
- Java 21 (LTS)
- Spring Boot 3.x
- PostgreSQL
- OAuth2 Google (Session-based, NOT JWT!)
- Lombok
- JPA/Hibernate

## Code Style

### Dependency Injection
```java
@RequiredArgsConstructor // ALWAYS use Lombok
public class MyService {
    private final MyRepository repository;
}
```

### Layers (Thin Controllers, Fat Services)
- **Controller**: HTTP coordination only, use Mappers
- **Service**: ALL business logic, work with Entities
- **Repository**: Data access only
- **Mapper**: Entity ↔ DTO (IN CONTROLLER!)

### DTOs
```java
// Simple
public record CreateDTO(@NotBlank String name) {}

// Complex
@Data
@Builder
public class ResponseDTO {
    private Long id;
    private String name;
}
```

### Exceptions
ALWAYS use specific exceptions:
- `ResourceNotFoundException` (404)
- `BusinessRuleException` (422)
- `ConflictException` (409)
- `ForbiddenException` (403)

### Security
```java
// ALWAYS validate permissions
@PreAuthorize("hasRole('MESTRE')")
@PostMapping
public ResponseEntity<GameDTO> create() { }

// Check ownership
@PreAuthorize("@securityService.canEdit(#id)")
@PutMapping("/{id}")
public ResponseEntity<GameDTO> update(@PathVariable Long id) { }
```

## Testing Priority
1. **Integration Tests (80%)** - PRIORITY
2. Unit Tests (20%) - complex logic only

```java
@SpringBootTest(webEnvironment = RANDOM_PORT)
@Transactional
class MyControllerIntegrationTest {
    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void shouldCreateResource() {
        // Arrange
        CreateDTO dto = new CreateDTO("Test");

        // Act
        ResponseEntity<ResponseDTO> response = restTemplate
            .postForEntity("/api/resources", dto, ResponseDTO.class);

        // Assert
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        // Verify in database too
    }
}
```

## Never Do
1. ❌ Business logic in controllers
2. ❌ Expose entities in APIs (use DTOs)
3. ❌ Mappers in services (put in controllers)
4. ❌ Generic exceptions
5. ❌ JWT for auth (we use SESSION!)
6. ❌ Forget @Transactional on writes
7. ❌ Skip @PreAuthorize validation
8. ❌ Stack traces in production

## Naming Conventions
- Tables: `snake_case` (users, user_games)
- Columns: `snake_case` (created_at, user_id)
- Java: `camelCase` (createdAt, userId)

## HTTP Status Codes
- 200 OK (GET, PUT)
- 201 Created (POST)
- 204 No Content (DELETE)
- 400 Bad Request (validation)
- 401 Unauthorized (not authenticated)
- 403 Forbidden (no permission)
- 404 Not Found
- 409 Conflict (duplicate)
- 422 Unprocessable Entity (business rule)

## Swagger Documentation
ALWAYS document:
```java
@Tag(name = "Resources")
@Operation(summary = "Create resource")
@ApiResponses({
    @ApiResponse(responseCode = "201", description = "Created"),
    @ApiResponse(responseCode = "400", description = "Invalid data")
})
```

## Complete Reference
For detailed implementations, see `/docs/backend/` files.
