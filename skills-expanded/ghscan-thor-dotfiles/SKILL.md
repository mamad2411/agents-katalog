---
name: laravel-developer
description: Aids in Laravel development and code reviews, focusing on best practices, Eloquent usage, and security. Use when writing or reviewing PHP code in a Laravel project.
---

# Laravel Developer Skill

This skill provides concise guidelines for writing and reviewing Laravel code, ensuring adherence to modern best practices, security standards, and performance optimization.

## Core Principles

### 1. Code Organization
- **Thin Controllers**: Controllers should only handle request parsing and response formatting. Delegate business logic to **Service Classes** or **Action Classes**.
- **Form Requests**: Always use Form Request classes for validation logic, keeping controllers clean.
- **Resources**: Use API Resources for transforming models into JSON responses.

### 2. Eloquent & Database Performance
- **Eager Loading**: Prevent N+1 query problems by using `with()` for relationships.
- **Mass Assignment**: Use `$fillable` or `$guarded` properties on models to prevent mass assignment vulnerabilities.
- **Scopes**: Use Local Scopes for reusable query constraints (e.g., `scopeActive`).
- **Optimization**: Use `chunk()` or `cursor()` for processing large datasets to manage memory usage.

### 3. Security
- **Validation**: Never trust user input. Validate everything using Form Requests or `$this->validate()`.
- **Sanitization**: Use Blade's `{{ $var }}` syntax to automatically escape output. Use `{!! $var !!}` only when absolutely necessary and safe.
- **Authorization**: Use Policies and Gates to control access to resources.

### 4. Modern Laravel Practices
- **Helpers**: Utilize `Arr::` and `Str::` helpers for array and string manipulation.
- **Collections**: Prefer Laravel Collections (`collect()`) over raw array functions for cleaner, chainable data manipulation.
- **Dependency Injection**: Use constructor injection for dependencies instead of Facades where possible for better testability.

## Review Checklist

When reviewing Laravel code, check for:
- [ ] N+1 queries (missing `with()`).
- [ ] Logic in controllers (move to Services/Actions).
- [ ] Inline validation (move to Form Requests).
- [ ] Missing authorization checks (Policies/Gates).
- [ ] Raw SQL queries where Eloquent/Query Builder could be used.
- [ ] Hardcoded configuration values (use `config()` and `.env`).