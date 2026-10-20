---
title: "Java Development — v1"
description: "Java development with best practices and patterns"
globs: ["**/*.java", "src/**/*.java", "main/**/*.java"]
alwaysApply: false
priority: high
---

# Java Development Rules

## Technology Stack
- **Language**: Java 8+ (prefer Java 11+)
- **Build Tool**: Maven, Gradle
- **Package Manager**: Maven Central, Gradle
- **Architecture**: Spring Boot, Clean Architecture

## Core Principles
- Follow SOLID principles
- Use object-oriented programming effectively
- Implement proper exception handling
- Write clean, readable code
- Use modern Java features

## Project Structure
src/
├─ main/
│   ├─ java/           # Java source files
│   │   └─ com/company/app/
│   │       ├─ controller/  # REST controllers
│   │       ├─ service/     # Business logic
│   │       ├─ repository/  # Data access
│   │       ├─ model/       # Data models
│   │       └─ config/      # Configuration
│   └─ resources/      # Configuration files
├─ test/               # Test source files
├─ pom.xml            # Maven configuration
└─ build.gradle       # Gradle configuration

## Coding Standards
- Use camelCase for variables and methods
- Use PascalCase for classes and interfaces
- Use descriptive names for methods and variables
- Follow Java naming conventions
- Use proper indentation (4 spaces)

## Best Practices
- Use meaningful variable names
- Implement proper exception handling
- Use collections effectively
- Implement proper logging
- Use annotations appropriately

## Common Patterns
- Dependency injection with Spring
- Repository pattern for data access
- Service layer for business logic
- DTO pattern for data transfer
- Builder pattern for complex objects

## Testing Strategy
- Write unit tests with JUnit
- Use Mockito for mocking
- Implement integration tests
- Use TestContainers for database tests
- Maintain high test coverage
