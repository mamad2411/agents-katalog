# Cline AI Rules - Ficha Controlador Backend

## Project Context
Spring Boot REST API for RPG character sheet management.

**Stack**: Java 21, Spring Boot 3.x, PostgreSQL, OAuth2 Google (Session-based)

## Primary Documentation
📚 **ALWAYS CHECK FIRST**: `/docs/AI_GUIDELINES_BACKEND.md`

Detailed guides in `/docs/backend/`:
- `01-architecture.md` - Layer structure
- `02-entities-dtos.md` - Data modeling
- `03-exceptions.md` - Error handling
- `04-repositories.md` - Data access
- `05-services.md` - Business logic
- `06-mappers.md` - Entity ↔ DTO
- `07-controllers.md` - REST APIs
- `08-security.md` - OAuth2 config
- `09-testing.md` - Integration tests
- `10-database.md` - PostgreSQL/JPA
- `11-owasp-security.md` - Security checklist

## Architecture Pattern

```
Request → Controller → Mapper → Service → Repository → Database
             ↓          ↓         ↓
          @Valid     Entity  Business
           DTO               Logic
```

**Golden Rules**:
- Controller = THIN (coordination only)
- Service = FAT (all business logic)
- Mappers = IN CONTROLLER (not service!)

## Code Generation Rules

### 1. Always Use Lombok
```java
@RequiredArgsConstructor  // NOT @Autowired constructor
public class MyService {
    private final MyRepository repository;
}
```

### 2. Specific Exceptions
```java
// ✅ DO
throw new ResourceNotFoundException("Game", id);
throw new BusinessRuleException("Invalid state");
throw new ConflictException("Name already exists");

// ❌ DON'T
throw new RuntimeException("Error");
throw new Exception("Not found");
```

### 3. Optional Usage
```java
// Return Optional when absence is NOT an error
public Optional<Game> findByIdOptional(Long id) {
    return repository.findById(id);
}

// Throw exception when absence IS an error
public Game findById(Long id) {
    return repository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Game", id));
}
```

### 4. Transactional
```java
@Service
@Transactional(readOnly = true)  // Class level
public class GameService {

    @Transactional  // Override for writes
    public Game create(Game game) {
        return repository.save(game);
    }
}
```

### 5. Security
```java
// ALWAYS validate permissions
@PreAuthorize("hasRole('MESTRE')")
@PostMapping
public ResponseEntity<GameDTO> create() { }

// ALWAYS check ownership
@PreAuthorize("@securityService.canEdit(#id)")
@PutMapping("/{id}")
public ResponseEntity<GameDTO> update(@PathVariable Long id) { }
```

### 6. Testing Priority
```java
// 80% Integration Tests
@SpringBootTest(webEnvironment = RANDOM_PORT)
@Transactional
class MyControllerIntegrationTest {
    @Autowired TestRestTemplate restTemplate;
    @Autowired MyRepository repository;

    @Test
    void shouldCreateResource() {
        // Arrange
        CreateDTO dto = new CreateDTO("Test");

        // Act
        var response = restTemplate.postForEntity("/api/resources", dto, ResponseDTO.class);

        // Assert
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(repository.findAll()).hasSize(1); // Verify DB!
    }
}

// 20% Unit Tests (complex logic only)
@ExtendWith(MockitoExtension.class)
class MyServiceTest {
    @Mock MyRepository repository;
    @InjectMocks MyService service;

    @Test
    void shouldValidateBusinessRule() {
        when(repository.existsByName("Existing")).thenReturn(true);

        assertThatThrownBy(() -> service.create(game))
            .isInstanceOf(ConflictException.class);
    }
}
```

### 7. Swagger Documentation
```java
@RestController
@RequestMapping("/api/resources")
@Tag(name = "Resources", description = "Resource management API")
public class ResourceController {

    @PostMapping
    @Operation(
        summary = "Create new resource",
        description = "Creates a resource with validation"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "201", description = "Created successfully"),
        @ApiResponse(responseCode = "400", description = "Invalid input"),
        @ApiResponse(responseCode = "409", description = "Already exists")
    })
    public ResponseEntity<ResourceDTO> create(
        @Valid @RequestBody CreateResourceDTO dto
    ) { }
}
```

## What to NEVER Do

1. ❌ Business logic in controllers
2. ❌ Expose entities in REST APIs (use DTOs!)
3. ❌ Put mappers in services
4. ❌ Use generic exceptions
5. ❌ Use JWT (we use SESSION-based auth!)
6. ❌ Forget @Transactional on write operations
7. ❌ Skip @PreAuthorize security checks
8. ❌ Expose stack traces in production
9. ❌ Use @Autowired (use Lombok @RequiredArgsConstructor)
10. ❌ Skip integration tests

## Naming Conventions

### Database
- Tables: `snake_case` (users, user_games)
- Columns: `snake_case` (created_at, user_id)
- Foreign Keys: `{table}_id` (user_id, game_id)

### Java
- Classes: `PascalCase` (UserService)
- Methods: `camelCase` (findById)
- Constants: `UPPER_SNAKE_CASE` (MAX_PLAYERS)
- Packages: lowercase (com.myapp.service)

## HTTP Status Codes Reference

| Operation | Success | Code |
|-----------|---------|------|
| GET       | OK      | 200  |
| POST      | Created | 201  |
| PUT       | OK      | 200  |
| DELETE    | No Content | 204 |

| Error Type | Code |
|------------|------|
| Validation | 400  |
| Auth       | 401  |
| Forbidden  | 403  |
| Not Found  | 404  |
| Conflict   | 409  |
| Business   | 422  |
| Server     | 500  |

## When Making Changes

1. **Read relevant doc first**: Check `/docs/backend/` for the pattern
2. **Follow templates**: Use code examples from documentation
3. **Test integration**: Write integration test BEFORE implementation
4. **Check security**: Validate permissions with @PreAuthorize
5. **Document API**: Add Swagger annotations
6. **Verify**: Run tests and check for errors

## File Structure to Follow

```
src/main/java/br/com/yourapp/
├── controller/
│   └── GameController.java
├── service/
│   └── GameService.java
├── repository/
│   └── GameRepository.java
├── entity/
│   └── Game.java
├── dto/
│   ├── request/
│   │   └── CreateGameDTO.java
│   └── response/
│       └── GameResponseDTO.java
├── mapper/
│   └── GameMapper.java
└── exception/
    ├── ResourceNotFoundException.java
    ├── BusinessRuleException.java
    └── ConflictException.java
```

## Additional Resources

For complex scenarios, edge cases, or advanced patterns:
- See full documentation in `/docs/backend/`
- Check OWASP security guidelines in `11-owasp-security.md`
- Review test patterns in `09-testing.md`
- Study architecture decisions in `01-architecture.md`

---

**Remember**: Quality over speed. Follow the patterns, write tests, and check documentation!
