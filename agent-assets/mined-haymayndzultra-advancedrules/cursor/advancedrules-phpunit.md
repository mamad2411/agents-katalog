---
title: "PHPUnit Testing — v1"
description: "PHPUnit testing with best practices and patterns"
globs: ["**/*.php", "tests/**/*.php", "**/*Test.php"]
alwaysApply: false
priority: medium
---

# PHPUnit Testing Rules

## Technology Stack
- **Framework**: PHPUnit 9+
- **Language**: PHP 8.0+
- **Build Tool**: Composer
- **Package Manager**: Composer
- **Testing**: Unit, Integration, Functional

## Core Principles
- Write reliable unit tests
- Use proper test isolation
- Follow testing best practices
- Use PHPUnit's built-in features
- Maintain high test coverage

## Project Structure
src/                  # Source code
├─ classes/           # Classes to test
├─ functions/         # Functions to test
└─ services/          # Services to test
tests/                # Test files
├─ Unit/              # Unit tests
├─ Integration/       # Integration tests
└─ Functional/        # Functional tests
phpunit.xml           # PHPUnit configuration

## Coding Standards
- Use camelCase for variables and functions
- Use PascalCase for classes
- Use descriptive names for tests and functions
- Follow PSR-12 coding standards
- Use proper indentation (4 spaces)

## Best Practices
- Use proper test isolation
- Implement proper mocking
- Use PHPUnit's built-in assertions
- Implement proper error handling
- Use PHPUnit's debugging tools

## Common Patterns
- Test-driven development
- Mocking external dependencies
- Data providers
- Test utilities and helpers
- Test data management

## Testing Strategy
- Write unit tests for all methods
- Use proper test isolation
- Implement integration tests
- Use PHPUnit's debugging tools
- Maintain high test coverage
