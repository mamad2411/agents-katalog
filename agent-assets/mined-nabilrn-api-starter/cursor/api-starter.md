---
description: API starter project rules
globs:
  - "**/*.kt"
  - "**/*.kts"
  - "**/*.yml"
  - "**/*.yaml"
alwaysApply: true
---

# API Starter Rules

- Use Kotlin and Spring Boot 3 patterns.
- Keep modules feature-based.
- Use constructor injection.
- Use Flyway for database changes.
- Keep controllers thin and services explicit.
- Add tests for new behavior.
- Keep optional modules disabled by default.
- Do not commit secrets.
- Do not add runtime AI features unless explicitly requested.
- Read docs/plan.md and the relevant docs file before editing a module.
- Run `.\gradlew.bat check` after behavior changes.
