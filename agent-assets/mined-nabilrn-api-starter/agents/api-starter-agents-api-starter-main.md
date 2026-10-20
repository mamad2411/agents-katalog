# API Starter Agent Instructions

## Project

Reusable Kotlin + Spring Boot API starter for REST backends.

## Current Architecture

- Kotlin and Spring Boot 3.
- Gradle Kotlin DSL.
- PostgreSQL with Flyway migrations.
- Spring Data JPA for persistence.
- REST JSON APIs as the default interface.
- OAuth, HMAC, and field encryption are optional backend modules, disabled by default.
- AI agent support means repository-level coding-agent setup, not a runtime AI backend module.

## Implementation Rules

- Keep modules feature-based, not layer-only.
- Use constructor injection.
- Keep controllers thin; put business logic in services.
- Use DTOs for request and response bodies.
- Use Flyway for schema changes. Do not rely on Hibernate schema generation.
- Use Spring Security for auth and authorization.
- Store refresh tokens hashed, not as raw tokens.
- Keep OAuth account linking separate from the user table.
- Do not add runtime AI features unless explicitly requested for a specific app.
- Do not commit secrets or real `.env` files.
- Before large edits, read `docs/plan.md` and the relevant docs page.
- After behavior changes, run `.\gradlew.bat test` and `.\gradlew.bat check`.

## Testing Rules

- Add tests for new service behavior.
- Add web/security tests for protected endpoint behavior.
- Use MockK for unit tests.
- Use Testcontainers for database integration tests.
- Keep JaCoCo thresholds passing.

## Style

- Prefer Kotlin idioms and null safety.
- Avoid unnecessary abstractions until a second concrete use case exists.
- Keep comments short and only for non-obvious code.
- Prefer clear names over abbreviations.

## Agent Workflow

When using an AI coding agent on this repo:

1. Read `AGENTS.md`, `docs/plan.md`, and the relevant module doc.
2. Inspect existing code before proposing changes.
3. Keep changes scoped to the requested module.
4. Add/update tests for changed behavior.
5. Run `.\gradlew.bat check` before considering work complete.
6. Never invent endpoints, schemas, or dependencies without updating docs.
