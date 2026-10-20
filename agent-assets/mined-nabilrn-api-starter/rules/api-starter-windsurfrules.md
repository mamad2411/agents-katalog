# API Starter Windsurf Rules

Read `AGENTS.md` first. It is the source of truth.

Project defaults:

- Kotlin + Spring Boot 3.
- REST JSON API.
- PostgreSQL + Flyway.
- Spring Data JPA.
- Spring Security.
- JWT access tokens and hashed refresh tokens.
- Optional OAuth, HMAC, and AES-GCM modules.

Rules:

- Do not add runtime AI modules unless explicitly requested.
- Do not commit secrets or real `.env` files.
- Use Flyway for schema changes.
- Add/update tests for behavior changes.
- Run `.\gradlew.bat check` before considering work complete.
- Update docs when endpoint, config, schema, or security behavior changes.
