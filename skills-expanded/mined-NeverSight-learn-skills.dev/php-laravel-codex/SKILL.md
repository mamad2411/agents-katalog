---
name: php-laravel-codex
description: Improve Codex performance on PHP and Laravel projects by enforcing an engineering workflow for analysis, implementation, testing, review, security, SQL performance, and delivery summaries.
---

# PHP Laravel Codex Skill

Use this skill when working inside a PHP or Laravel codebase.

## Core behavior

- Inspect existing project conventions before changing code.
- Prefer Laravel-native solutions over custom framework-like abstractions.
- Make the smallest change that fully solves the task.
- Keep public behavior stable unless the user asks for behavior changes.
- Do not invent classes, config keys, artisan commands, helpers, facades, or package APIs.
- Search the repository for similar implementations before introducing a new pattern.

## Workflow

1. Restate the task internally as a concrete code change.
2. Identify the relevant files, tests, routes, models, controllers, requests, services, jobs, events, listeners, migrations, factories, and seeders.
3. Check Laravel version and package constraints from `composer.json`.
4. Edit code in small steps.
5. Add or update tests when behavior changes.
6. Run focused checks first, then broader checks if useful.
7. Summarize changed files and verification.

## PHP standards

- Follow PSR-12 and the project's existing style.
- Prefer strict, readable types where the project already uses them.
- Avoid clever one-liners when business logic is involved.
- Prefer early returns to deeply nested conditionals.
- Keep exception handling explicit and meaningful.

## Laravel standards

- Controllers should orchestrate, not contain large business workflows.
- Use FormRequest for reusable or complex validation.
- Use Policies/Gates for authorization.
- Use Resources for API serialization when the project uses them.
- Use Jobs for slow external effects.
- Use Events/Listeners only when decoupling is valuable.
- Use transactions for multi-write consistency.
- Use eager loading for relationship-heavy reads.

## Testing

Prefer the project's existing test framework.

Common commands:

```bash
php artisan test
vendor/bin/pest
vendor/bin/phpunit
```

When adding tests:

- Use feature tests for HTTP behavior.
- Use unit tests for isolated domain logic.
- Use factories instead of hard-coded database setup.
- Assert authorization, validation, success path, and important failure paths.

## Static analysis and formatting

Use project tools if present:

```bash
vendor/bin/pint
vendor/bin/phpstan analyse
vendor/bin/psalm
vendor/bin/rector process --dry-run
```

## Security checklist

- Validate all external input.
- Authorize state-changing actions.
- Avoid mass assignment mistakes.
- Do not expose secrets in logs, exceptions, test snapshots, or responses.
- Use parameter binding, query builder, or Eloquent instead of raw SQL interpolation.
- Be careful with file uploads, path traversal, SSRF, command execution, and unserialization.

## SQL and performance checklist

- Look for N+1 queries.
- Add eager loading when a relationship is used in loops.
- Prefer pagination for unbounded lists.
- Check indexes for new filtering or sorting patterns.
- Avoid loading full models when only IDs or aggregates are needed.
