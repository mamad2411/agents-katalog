---
description: Java and Quarkus coding standards for whatsapp-verify
globs: "**/*.java"
alwaysApply: true
---

# Java Standards

- Target **Java 25** (project uses Mandrel/GraalVM via sdkman).
- Use modern Java features: records, sealed classes, pattern matching, enhanced switch, string templates where appropriate.
- Follow camelCase for methods/variables, PascalCase for classes.

# Quarkus & Picocli

- This is a **CLI application** using `quarkus-picocli`, not a REST service.
- Commands implement `Runnable` and use `@CommandLine.Command`.
- The top-level command is `WhatsAppVerifyCommand`; subcommands are registered via `subcommands`.
- Use `@Inject` for CDI dependency injection. Prefer constructor injection for new classes.

# GraalVM Native Image

- The project builds native executables with `-Pnative`.
- Register reflection config in `ReflectionConfiguration.java` when adding classes that need runtime reflection.

# Error Handling

- Catch specific exceptions; avoid empty catch blocks.
- Use `org.jboss.logging.Logger` for logging, not `System.out`.

# Code Style

- Keep methods focused and short.
- Prefer immutable data structures and records for value objects (see `Member.java`).
