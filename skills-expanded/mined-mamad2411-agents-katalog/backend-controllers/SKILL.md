---
name: backend-controllers
description: Design controller/handler layers for HTTP backends. Use when
  defining the boundary between HTTP and application logic.
metadata:
  tags: backend, controllers
---

# Backend Controllers & Handlers

## Use this skill when
- Designing route handlers and controllers
- Mapping HTTP requests to application commands/queries
- Keeping the HTTP layer isolated from business logic

## Do not use this skill when
- Designing the full API surface (use api-contracts)
- Writing business logic

## Instructions
1. Controllers parse, validate, and map; they do not contain business logic.
2. Bind URL params, query, and body explicitly.
3. Translate domain results to HTTP status codes consistently.
4. Return a uniform response shape for success and error.
5. Keep validation at the boundary, not scattered in methods.
6. Do not leak exceptions: convert to the error contract.
7. Document each endpoint’s status codes and examples.

## Output Format
- Endpoint | input contract | output contract | status mapping

## Common Mistakes
- Business logic in controllers
- Raw ORM/exception types leaking to the client
- Status codes that lie about failure
