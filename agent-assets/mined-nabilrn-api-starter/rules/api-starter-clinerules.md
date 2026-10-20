# API Starter Cline Rules

Follow `AGENTS.md` as the source of truth.

Before editing:

- Read `docs/plan.md`.
- Read the relevant module doc.
- Inspect existing code patterns.

Implementation rules:

- Keep modules feature-based.
- Keep controllers thin.
- Put business logic in services.
- Use DTOs for request/response bodies.
- Use Flyway for schema changes.
- Do not store raw refresh tokens.
- Do not trust OAuth profile data from frontend clients.
- Do not add runtime AI code unless explicitly requested.

Verification:

- Run `.\gradlew.bat test`.
- Run `.\gradlew.bat check`.
- Keep JaCoCo thresholds passing.
