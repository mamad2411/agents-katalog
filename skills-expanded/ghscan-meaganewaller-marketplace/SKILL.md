---
name: rails-caching
description: This skill should be used when the user asks to "cache this page", "add fragment caching", "set up Solid Cache", "add HTTP cache headers", "use Russian doll caching", "invalidate a cache key", or "stop recomputing this on every request". For diagnosing why something is slow in the first place, use rails-performance.
---

# Rails Caching

Apply caching at the right layer with clear invalidation rules.

## When to Use This Skill

- Russian doll caching
- Solid Cache config
- HTTP cache headers

## Defaults

Assume mise-managed Ruby and Rails with `bin/*` binstubs — not rbenv, rvm, or
asdf. Read `${CLAUDE_PLUGIN_ROOT}/references/conventions.md` for versions,
command forms, and type-system pairing before running project commands.

## Core Guidance

1. **Development**: Toggle `rails dev:cache` to test caching locally.

2. **Keys**: Include locale, roles, and `updated_at` in cache keys.

3. **Solid Cache**: Default in Rails 8 — store in DB; tune `config/cache.yml`.

4. **HTTP**: `stale?`, `fresh_when` in controllers for conditional GET.

5. **Avoid** caching user-specific HTML without key segmentation.

## Quick Commands

```bash
mise exec -- bin/rails dev:cache
mise exec -- bin/rails runner 'Rails.cache.write("ping", "pong")'
```

## Anti-Patterns

- Caching nil or error responses
- Forever caches without invalidation

## See Also

- **rails-performance**
