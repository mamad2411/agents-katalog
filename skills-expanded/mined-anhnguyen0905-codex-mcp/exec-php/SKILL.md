---
name: exec-php
description: PHP execution idioms to embed into Codex prompts when the target project is PHP — PSR-12, strict types, error handling, and framework conventions.
---

# PHP Idioms (embed when project is PHP)

```
PHP standards:
- declare(strict_types=1) at the top of every file; type every param, return, and property; use
  enums and readonly properties where the version supports them.
- Errors: throw specific exceptions (extend the framework's or SPL types); catch narrowly; never
  suppress with @; use finally for cleanup; never return false/null to signal errors that callers
  will forget to check.
- Immutability: readonly properties / value objects for data that shouldn't change after construction;
  avoid mutating arrays passed by reference unless the API contract says so.
- Follow PSR-12 formatting and PSR-4 autoloading; match Composer package/namespace structure. Add
  dependencies only via composer.json.
- Framework (if Laravel/Symfony): use its idioms — Eloquent/Doctrine correctly (no N+1: eager-load
  relations), form requests / validators for input, dependency injection over facades in new code,
  migrations for schema. Don't hand-roll what the framework provides.
- Security: parameterized queries / query builder only (never interpolate input into SQL); escape
  output in templates; validate and sanitize all request input at the boundary.
- Tests: PHPUnit (or Pest if the repo uses it); arrange-act-assert; data providers for case tables;
  assert behavior, match existing test namespace/layout.
```
