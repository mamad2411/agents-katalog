---
description: Maven build conventions for whatsapp-verify
globs: "**/pom.xml"
alwaysApply: false
---

# Maven Conventions

- Use the Maven wrapper (`./mvnw`) for all build commands.
- Managed dependency versions come from `quarkus-bom`; only specify versions for dependencies not in the BOM.
- Keep `<properties>` for version pinning of external dependencies and plugins.

# Build Commands

- Build: `./mvnw clean install --batch-mode`
- Test: `./mvnw test --batch-mode`
- Native build: `./mvnw clean install -Pnative --batch-mode`

# Testing

- Unit tests use JUnit 5 with `quarkus-junit`.
- Integration tests use `@QuarkusMainIntegrationTest` and `@Launch` for CLI testing.
- Code coverage via `quarkus-jacoco`.
