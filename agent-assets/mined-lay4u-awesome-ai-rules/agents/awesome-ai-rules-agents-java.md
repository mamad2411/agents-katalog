# Codex Java Spring Boot Rules

## Role
- You are an OpenAI Codex agent operating in Spring Boot 3.x repositories.
- Optimize for correctness, maintainability, and operational safety.

## Architectural Conventions
- Use package-by-feature as the default project structure.
- Keep controllers focused on transport concerns.
- Keep business logic in services and domain modules.

## Dependency Injection
- Constructor injection only.
- Field injection is forbidden.
- Dependencies should be `final` and explicit.

## DTO and Type Design
- Prefer `record` for immutable request/response DTOs.
- Separate DTOs from entities and internal domain objects.
- Keep mapping code explicit at boundaries.

## Optional Handling
- Never call `Optional.get()` without a presence check.
- Prefer `orElseThrow`, `orElse`, `map`, and `flatMap`.
- Avoid null when Optional communicates absence better.

## Error Handling Strategy
- Use `@ControllerAdvice` for centralized API exception mapping.
- Return stable, documented error formats.
- Do not expose stack traces or internal details.

## Logging
- Use SLF4J for all logging.
- Include contextual fields for tracing operations.
- Do not log secrets or sensitive request bodies.

## Testing
- Use JUnit 5 for unit and integration tests.
- Use Mockito for mocking external collaborators.
- Cover success, validation failures, and exceptional flows.

## Build and Dependency Hygiene
- Follow existing Maven or Gradle conventions.
- Keep dependencies aligned with Spring Boot 3.x.
- Avoid unnecessary build-time complexity.

## Lombok Policy
- Use Lombok minimally.
- Prefer records and explicit constructors for clarity.
- Avoid patterns that hide generated behavior.

## Definition of Done
- Build passes and tests pass.
- New code follows injection, Optional, logging, and package conventions.
