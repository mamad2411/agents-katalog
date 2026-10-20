# Gemini CLI Java Spring Boot Rules

## Role
- You are a Gemini CLI coding agent in Spring Boot 3.x Java codebases.
- Optimize for explicit contracts, safe evolution, and production readiness.

## Feature-Oriented Structure
- Use package-by-feature layout as the default.
- Keep feature modules cohesive with clear API and service layers.
- Avoid broad utility dumping grounds.

## Injection and Dependency Rules
- Use constructor injection only.
- Do not use field injection.
- Keep injected dependencies immutable and explicit.

## DTO and Records
- Prefer Java records for API DTOs.
- Keep DTOs separate from persistence entities.
- Keep mapping logic clear and localized.

## Optional and Null Safety
- Use Optional for explicit absence semantics where appropriate.
- Never call `Optional.get()` without checking presence first.
- Prefer fluent Optional operations for readability and safety.

## Exception Handling
- Centralize HTTP exception mapping with `@ControllerAdvice`.
- Keep external error responses consistent and sanitized.
- Preserve internal details only in logs.

## Logging Standards
- Use SLF4J across all layers.
- Log key identifiers and operation context.
- Never log credentials, tokens, or sensitive PII.

## Testing Standards
- Use JUnit 5 for test framework support.
- Use Mockito for collaborator mocking.
- Test happy path, edge cases, and error behavior for changed code.

## Build Rules
- Follow repo-standard Maven or Gradle conventions.
- Keep plugin/dependency choices compatible with Spring Boot 3.x.
- Keep build configuration simple and maintainable.

## Lombok Guidance
- Keep Lombok usage minimal.
- Prefer records and explicit code for core business logic.
- Avoid over-annotation that obscures intent.

## Completion Criteria
- Build succeeds and tests pass.
- New code follows feature packaging, injection, Optional, logging, and error rules.
