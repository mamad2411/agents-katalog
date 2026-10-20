# Spring Boot 3.x Project Rules

## Scope
- Applies to Java services built with Spring Boot 3.x.
- Optimize for clear boundaries, testability, and reliable operations.

## Architecture and Packaging
- Use package-by-feature over package-by-layer.
- Within each feature, keep clear API, application, and data boundaries.
- Keep controller code minimal and delegate business logic to services.

## Injection and Class Design
- Use constructor injection exclusively.
- Field injection is not allowed.
- Keep dependencies `final` and explicit.
- Favor immutability in service collaborators.

## DTOs and Data Shapes
- Use `record` for request/response DTOs.
- Separate transport DTOs from JPA entities.
- Keep mapper logic explicit and tested.

## Optional Usage
- Avoid null for optional domain values.
- Do not call `Optional.get()` without `isPresent()` or safe alternatives.
- Prefer `orElseThrow` with meaningful exception types where absence is invalid.

## Error Strategy
- Handle API exceptions centrally with `@ControllerAdvice`.
- Provide consistent status codes and error body schema.
- Map internal exceptions to client-safe responses.

## Logging Standards
- Use SLF4J for logging across layers.
- Include key business identifiers in logs.
- Avoid noisy logs and never log secrets.

## Testing Standards
- Use JUnit 5 as the testing framework.
- Use Mockito for mocking external collaborators.
- Cover service logic, controller contracts, and exception handlers.

## Build Conventions
- Respect existing Maven or Gradle conventions in the repository.
- Keep dependency declarations clean and versions aligned.
- Ensure Spring Boot starter usage matches Boot 3.x.

## Lombok Policy
- Keep Lombok usage minimal.
- Prefer records, constructors, and explicit code for clarity.
- Avoid Lombok annotations that obscure business behavior.

## Definition of Done
- Build and tests pass.
- Exception, logging, and package-by-feature conventions are followed.
