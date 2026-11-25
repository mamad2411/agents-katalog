---
name: express-development
description: Build HTTP APIs with Express. Use when developing or reviewing
  Express, Fastify, or connect-style servers.
metadata:
  tags: express, development
---

# Express Development

## Use this skill when
- Building REST endpoints and middleware pipelines
- Reviewing route handlers and error handling
- Structuring an Express/Fastify app

## Do not use this skill when
- Using a heavier framework (NestJS, Rails) in that codebase
- Non-HTTP services

## Instructions
1. Organize by feature/module, not by file type.
2. Keep route handlers thin: parse input, call service, map output.
3. Validate and coerce input at the boundary before handlers use it.
4. Centralize error handling in an error-handling middleware.
5. Use async handlers with a safe wrapper; never leave rejected promises.
6. Structure middleware order: security, body parsing, auth, routes, errors.
7. Use a router per resource; mount with prefixes.
8. Configure helmet, CORS, compression, and body size limits explicitly.

## Checklist
- All routes have a defined error path
- Body size and origin policies are explicit

## Output Format
- Route map | middleware order | error contract | module layout

## Common Mistakes
- Fat route handlers with business logic
- Errors that leak stack traces to clients
- Inline auth checks scattered across routes
