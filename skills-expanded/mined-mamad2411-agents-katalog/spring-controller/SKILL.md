---
name: spring-controller
description: Generate a Spring REST controller for a named entity with CRUD endpoints, validation, OpenAPI documentation, and integration tests. Invoke as /spring-controller <Entity>.
paths:
  - "**/*.java"
  - "pom.xml"
  - "build.gradle*"
user-invocable: true
---

# Spring REST Controller Scaffold

Generate a `$ARGUMENTS`Controller with the following:

- `@RestController` and `@RequestMapping("/api/$ARGUMENTS")` (lowercased plural)
- CRUD endpoints with proper HTTP verbs and status codes:
  - `GET /api/$ARGUMENTS` — list (with pagination params)
  - `GET /api/$ARGUMENTS/{id}` — fetch one (404 on miss)
  - `POST /api/$ARGUMENTS` — create (201 + Location header)
  - `PUT /api/$ARGUMENTS/{id}` — update (200 or 404)
  - `DELETE /api/$ARGUMENTS/{id}` — delete (204)
- Request and response DTOs for `$ARGUMENTS` (don't expose the JPA entity directly)
- `@Valid` + Jakarta validation annotations on the request DTOs
- OpenAPI annotations (`@Operation`, `@ApiResponses`)
- Integration tests using `@SpringBootTest` + `MockMvc` covering happy path, validation failure, and 404

## Conventions

- Constructor injection (no field `@Autowired`)
- ResponseEntity return types so HTTP status is explicit
- Use the project's existing exception handler if `@ControllerAdvice` is present
- Match the package layout of existing controllers

**Usage:** `/spring-controller User` → `UserController`, `UserRequest`, `UserResponse`, `UserControllerIntegrationTest`
