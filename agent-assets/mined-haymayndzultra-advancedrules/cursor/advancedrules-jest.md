---
title: "Jest Testing — v1"
description: "Jest unit testing with best practices and patterns"
globs: ["**/*.test.ts", "**/*.test.js", "**/*.spec.ts", "**/*.spec.js"]
alwaysApply: false
priority: high
---

# Jest Testing Rules

## Technology Stack
- **Framework**: Jest
- **Language**: TypeScript, JavaScript
- **Build Tool**: Jest CLI
- **Package Manager**: npm, yarn, pnpm
- **Testing**: Unit, Integration, Snapshot

## Core Principles
- Write reliable unit tests
- Use proper test isolation
- Follow testing best practices
- Use Jest's built-in features
- Maintain high test coverage

## Project Structure
src/                  # Source code
├─ components/        # Components to test
├─ utils/            # Utilities to test
└─ services/         # Services to test
tests/               # Test files
├─ unit/             # Unit tests
├─ integration/      # Integration tests
└─ __mocks__/        # Mock files
jest.config.js       # Jest configuration

## Coding Standards
- Use camelCase for variables and functions
- Use descriptive names for tests and functions
- Follow testing naming conventions
- Use proper indentation (2 spaces)
- Use consistent test structure

## Best Practices
- Use proper test isolation
- Implement proper mocking
- Use Jest's built-in assertions
- Implement proper error handling
- Use Jest's debugging tools

## Common Patterns
- Test-driven development
- Mocking external dependencies
- Snapshot testing
- Test utilities and helpers
- Test data management

## Testing Strategy
- Write unit tests for all functions
- Use proper test isolation
- Implement integration tests
- Use Jest's debugging tools
- Maintain high test coverage
