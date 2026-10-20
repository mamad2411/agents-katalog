---
title: "Go Development — v1"
description: "Go development with best practices and patterns"
globs: ["**/*.go", "cmd/**/*.go", "internal/**/*.go", "pkg/**/*.go"]
alwaysApply: false
priority: high
---

# Go Development Rules

## Technology Stack
- **Language**: Go 1.19+
- **Build Tool**: Go modules
- **Package Manager**: go mod
- **Web Framework**: Gin, Echo, Fiber
- **Architecture**: Clean Architecture

## Core Principles
- Follow Go idioms and conventions
- Use interfaces effectively
- Implement proper error handling
- Write clean, readable code
- Use Go's concurrency features

## Project Structure
cmd/
├─ main.go            # Application entry point
internal/             # Private application code
├─ handler/           # HTTP handlers
├─ service/           # Business logic
├─ repository/        # Data access
├─ model/             # Data models
└─ config/            # Configuration
pkg/                  # Public packages
go.mod                # Go modules file
go.sum                # Go modules checksum

## Coding Standards
- Use camelCase for variables and functions
- Use PascalCase for exported names
- Use descriptive names for functions and variables
- Follow Go naming conventions
- Use proper indentation (tabs)

## Best Practices
- Use meaningful variable names
- Implement proper error handling
- Use interfaces for abstraction
- Implement proper logging
- Use Go's built-in testing

## Common Patterns
- HTTP handlers with middleware
- Repository pattern for data access
- Service layer for business logic
- Dependency injection
- Error wrapping and handling

## Testing Strategy
- Write unit tests with testing package
- Use testify for assertions
- Implement integration tests
- Use table-driven tests
- Maintain high test coverage
