---
name: laravel-conventions
description: Personal Laravel conventions enforced when creating, modifying, or planning code that will touch code utilizing the Laravel framework.
---

# Laravel Conventions

These are non-negotiable personal conventions unless explicitly overridden by the user.

## Models

**No model observers, ever** — Never use Laravel model observers or listen for Eloquent model events (`creating`, `saved`, etc.). Dispatch explicit domain events instead. This is non-negotiable. If they already exist for a given model, mention it to the user, but keep building.

## Logging

Use `Context@scope()` liberally if important contextual data exists in a parent but not within the children, and the children are writing logs. This allows for maintaining contextual information inside of function calls without needing to pass that data to child functions.

```php
Context::scope(function() use ($user) {
    Context::add('user', $user->id);

    $this->somePrivateMethod($user);
    // ...
});
```

## Helper Methods

Prefer `new Collection()` over `collect()`. This reduces an extra stack and indirection.

Using `tap()` rarely the right call for readability.

## Dependency Injection

Prefer dependency injection to using facades. For large projects, test suite time is always a concern, and using facades disallow writing pure PHPUnit tests.

## Testing

Use `Model::factory()->make()` whenever possible. Database writes are often unnecessary inside of tests.
