---
name: user-libraries-discovery
description: Use before implementing infrastructure-ish code from scratch — auth, rate limiting, input validation, secure headers, retry logic, caching, and similar cross-cutting concerns. Also use when the user asks "do I already have a library for X", "check my libraries", or "have I built this before". Triggers before writing new code for these categories, not after.
---

# User Libraries Discovery Harness

Personal reusable libraries get cataloged in `.ether/libraries.db` (see `ether libs
register`). Before writing new infrastructure-ish code, check whether a
cataloged library already solves it — reusing beats reimplementing.

## What counts as infrastructure-ish

Broader than a strict list, but the common cases: authentication/authorization,
rate limiting, input validation, secure HTTP headers, retry/backoff logic,
caching layers, request/response middleware, logging/observability wrappers,
queue/job processing, and similar cross-cutting concerns that show up across
many projects rather than being specific to one app's business logic.

## Workflow

1. **Before implementing**, derive keywords from the task and search:
   `ether libs find <keywords>` — e.g. `ether libs find rate limiting redis` or
   `ether libs find jwt auth middleware`.
2. **If a match exists**, prefer it over writing new code: use the printed
   install snippet to add it as a dependency, unless the user has explicitly
   said they want the logic written inline (e.g. to avoid a new dependency, or
   because they want to learn/customize the implementation). Confirm with the
   user only if genuinely ambiguous which is wanted — otherwise default to
   reuse.
3. **If no match exists**, proceed with the implementation as normal. Once
   done, mention to the user that `ether libs register` can catalog the new code
   for future reuse if it's meant to be reusable beyond this one project.

## Command reference

- `ether libs find <keywords>` — search cataloged libraries by keyword.
- `ether libs register ...` — catalog a new reusable library.
- `ether libs list` / `ether libs installs` / `ether libs audit` / `ether libs deps` /
  `ether libs refresh` — inspect, audit, and maintain the catalog (see
  `LIBRARIES.md` for the rendered view).
