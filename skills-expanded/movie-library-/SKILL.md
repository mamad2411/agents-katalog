# Movie Library - Coding Rules

## Import Rules
- ALWAYS use @/ for absolute imports within src/
- NEVER use relative imports like ../../../
- Exception: files outside src/ use relative paths when needed

## Code Style  
- Use functional programming over classes
- Export individual functions, not classes
- Prefer pure functions and immutability
- Avoid comments unless absolutely necessary - code should be self-documenting
- Use arrow functions for simple functions
- Use const over let when possible

## Architecture
- Follow hexagonal architecture pattern
- Use Repository pattern for data access
- Use Factory functions over constructors
- Keep domain logic separate from infrastructure

## TypeScript
- Use proper typing, avoid any
- Prefer interfaces over types for object shapes
- Use type for unions and aliases

## File Organization
- Group related functionality in folders
- Export directly from individual files, avoid index.ts barrel exports
- Keep files focused on single responsibility

## Project-Specific Rules
- Never create duplicate files - always unify and consolidate
- Use cases should be in core/use-cases with types in core/models
- Service layer (application services) acts as facade between UI and domain
- API layer should use real use cases, not simulations
- All operations should be async and handle errors gracefully
- Use fallback patterns for resilient UX (local fallback if API fails)
- Remove documentation files after integration - keep knowledge in code

## Integration Patterns
- UI Context → Hooks → API Layer → Application Service → Use Cases → Repository
- Maintain backward compatibility when refactoring
- Use single source of truth for data operations
- Mock services only in tests, not in production code paths
