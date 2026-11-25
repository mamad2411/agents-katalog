# EdgeRush LootMan - AI Agent Rules

You are an expert Kotlin/Spring Boot developer working on EdgeRush LootMan, a World of Warcraft guild loot distribution system.

## Project Context
- **Purpose**: WoW guild loot distribution using FLPS (Final Loot Priority Score) algorithm
- **Tech Stack**: Kotlin, Spring Boot 3.x, PostgreSQL, Docker, JDK 24
- **Architecture**: Microservices with external API integration (WoWAudit)
- **Key Algorithm**: FLPS = (RMS × IPI) × RDF

## Code Style & Standards
- Follow Kotlin idioms and coroutines best practices
- Use data classes for DTOs and entities
- Implement proper error handling with Result<T> types
- Write comprehensive tests (unit + integration)
- Document business logic with clear comments
- Use dependency injection with Spring annotations

## File Structure Rules
- Main code: `data-sync-service/src/main/kotlin/com/edgerush/datasync/`
- Tests: `data-sync-service/src/test/kotlin/com/edgerush/datasync/`
- Configs: `data-sync-service/src/main/resources/`
- Migrations: `data-sync-service/src/main/resources/db/migration/`

## Development Patterns
1. **API Clients**: Use WebClient with retry mechanisms and circuit breakers
2. **Services**: Implement business logic with suspend functions for async operations
3. **Repositories**: Extend JpaRepository with custom query methods
4. **Entities**: Use JPA annotations with Kotlin data classes
5. **DTOs**: Separate request/response models from domain entities

## Key Business Rules
- FLPS scores must be between 0.0 and 1.0
- All external API calls must have proper error handling
- Character data sync is critical for accurate scoring
- Attendance tracking affects RMS calculations
- Recent loot awards impact RDF calculations

## Testing Requirements
- Unit tests for all business logic
- Integration tests for repository layers
- API client tests with MockWebServer
- End-to-end tests for critical workflows
- Minimum 80% code coverage

## Documentation Standards
- Update API_REFERENCE.md for interface changes
- Document complex algorithms in comments
- Maintain architecture diagrams for structural changes
- Include usage examples for new APIs

## External Dependencies
- WoWAudit API for guild data
- PostgreSQL for persistence
- Docker for containerization
- Flyway for database migrations

## Common Issues to Avoid
- Blocking operations in suspend functions
- Null pointer exceptions with nullable types
- Database connection leaks
- API rate limit violations
- Inconsistent error responses

## File Headers
Use this template for new Kotlin files:

```kotlin
/**
 * EdgeRush LootMan - [Component Description]
 * 
 * [Brief description of file purpose]
 * 
 * Key responsibilities:
 * - [Primary responsibility]
 * - [Secondary responsibility]
 * 
 * @author AI Agent
 * @since [Version]
 */
```

## Reference Documentation
- Read AI_AGENT_GUIDE.md for project overview
- Check CODE_ARCHITECTURE.md for technical details
- Follow AI_DEVELOPMENT_STANDARDS.md for conventions
- Use API_REFERENCE.md for interface documentation
- Consult QUICK_REFERENCE.md for common tasks

## Success Criteria
- All tests pass: `./gradlew test`
- Health checks green: `curl http://localhost/api/actuator/health`
- No build warnings or errors
- Code follows established patterns
- Documentation updated for changes