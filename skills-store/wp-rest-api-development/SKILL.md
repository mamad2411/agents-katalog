---
name: wp-rest-api-development
description: WordPress REST API review for Codex. Use when reviewing custom routes, permission callbacks, request validation, schema design, controller classes, response shape, or versioned API behavior.
---

# Codex WordPress REST API Review

## Purpose

Use this skill when Codex should review WordPress REST API code for route registration quality, authorization, validation, schema design, and predictable response behavior.

## Focus Areas

- `register_rest_route()` correctness
- `permission_callback` logic
- Request arg validation and sanitization
- `WP_REST_Request` handling
- Response shape, status codes, and versioning

## Workflow

1. Identify route registration and controller structure.
2. Check auth and validation first.
3. Review response consistency and API contract quality.
4. Load only the needed shared references from `../../claude-skills/wp-rest-api-development/references/`.
5. Report findings with severity, file references, impact, and recommended fixes.

## References

- `../../claude-skills/wp-rest-api-development/references/route-patterns.md`
- `../../claude-skills/wp-rest-api-development/references/schema-and-auth-guide.md`

