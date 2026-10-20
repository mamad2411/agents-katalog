---
title: "Laravel Development — v1"
description: "Laravel PHP development with best practices and patterns"
globs: ["**/*.php", "app/**/*.php", "routes/**/*.php", "database/**/*.php"]
alwaysApply: false
priority: high
---

# Laravel Development Rules

## Technology Stack
- **Framework**: Laravel 10+
- **Language**: PHP 8.1+
- **Build Tool**: Composer
- **Package Manager**: Composer
- **Database**: MySQL, PostgreSQL, SQLite
- **Database**: MySQL, PostgreSQL, SQLite

## Core Principles
- Follow Laravel conventions
- Use Eloquent ORM effectively
- Implement proper validation
- Follow SOLID principles
- Use Laravel's built-in features

## Project Structure
app/
├─ Console/            # Console commands
├─ Exceptions/         # Exception handlers
├─ Http/               # HTTP layer
│   ├─ Controllers/    # Controllers
│   ├─ Middleware/     # Middleware
│   └─ Requests/       # Form requests
├─ Models/             # Eloquent models
├─ Providers/          # Service providers
├─ Services/           # Business logic
└─ View/               # Blade templates
routes/
├─ web.php            # Web routes
├─ api.php            # API routes
└─ console.php        # Console routes
database/
├─ migrations/         # Database migrations
├─ seeders/            # Database seeders
└─ factories/          # Model factories

## Coding Standards
- Use camelCase for variables and functions
- Use PascalCase for classes
- Use descriptive names for methods and variables
- Follow PSR-12 coding standards
- Use proper indentation (4 spaces)

## Best Practices
- Use Eloquent relationships effectively
- Implement proper form validation
- Use Laravel's built-in authentication
- Implement proper error handling
- Use Laravel's caching system

## Common Patterns
- Repository pattern for data access
- Service layer for business logic
- Form request validation
- Resource classes for API responses
- Policy-based authorization

## Testing Strategy
- Write unit tests with PHPUnit
- Use Laravel's testing helpers
- Implement feature tests
- Use database transactions for tests
- Maintain high test coverage
