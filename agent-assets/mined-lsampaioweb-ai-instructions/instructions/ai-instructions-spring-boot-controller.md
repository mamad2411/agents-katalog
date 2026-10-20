---
description: "Spring Boot REST controller contract for URL design, HTTP verbs, status codes, pagination, and OpenAPI annotations."
applyTo: "**/*RestController.java, **/*OpenApi*.java, **/openapi/**/*.java"
---

# Spring Boot REST Controller Contract

These rules apply to every REST controller, including when the success body is not
JSON. A non-JSON success body is allowed only through an approved Instruction override
of the response clause. Server-rendered page controllers (`*PageController`) and
WebSocket endpoints (`*SocketController`) follow the architecture and Thymeleaf /
WebSocket contracts; this file covers REST only.

Architecture, exception handling, i18n, Lombok, and profile/Swagger YAML stay in
their own instruction files. Do not restate those contracts here.

## Naming

- Name every REST endpoint class `<Feature>RestController` (architecture contract).
  The `RestController` suffix is what loads this file via `applyTo`; do not omit it.
- Annotate with `@RestController`. Do not use `@Controller` for JSON/API endpoints.
- Never name a REST endpoint class `<Feature>Controller`, `<Feature>PageController`,
  or `<Feature>SocketController`.
- Never name a server-rendered MVC class `<Feature>RestController`.

## URL design

- Map REST collections at `/api/v1/{plural-resource}`.
- Do not put a trailing slash on class or method mappings.
- Identify a stored resource with `/{id}` on GET, PUT, and DELETE.
- Annotate numeric ids with `@Positive`.
- Keep the version in the path (`v1`). Do not add a second versioning scheme.

## HTTP verbs and payloads

- Use `GET`, `POST`, `PUT`, and `DELETE`.
- Use `PATCH` only when the product requires a partial update.
- Send create and update payloads as JSON `@RequestBody` records, not as query
  parameters.
- Keep `@Valid` on the request body (exception and architecture contracts).
- Use one `FeatureRequest` when create and update share the same fields. Split
  into `CreateFeatureRequest` and `UpdateFeatureRequest` only when the bodies
  actually differ.

## Responses

- Return `ResponseEntity<T>` from every REST method. Do not return a naked body
  or a `@ResponseStatus` void method.
- `GET` and `PUT` success: `200 OK` with the resource body.
- `POST` that creates a resource: `201 Created` with the body and a `Location`
  header for the new resource, built from `UriComponentsBuilder`.
- `DELETE` success: `204 No Content` with an empty body.
- `POST` that only accepts work for later processing: `202 Accepted`.
- `POST` that performs an action without creating a resource: `200 OK` with the
  result body.
- Domain misses are thrown as `AppException` from the service (exception
  contract). Do not return `Optional` or an empty 404 from a real-app controller.

## Pagination

- Unbounded collection `GET`s take Spring `Pageable` (default `page` 0,
  `size` 20, optional `sort`) and return `ResponseEntity<Page<FeatureResponse>>`.
- Add `spring-data-commons` when `Pageable`/`Page` are used (pom contract; do not
  pull JPA solely for paging).
- Bounded or non-collection endpoints may return a list or a single resource.
- Do not add HATEOAS (`PagedModel`, `EntityModel`, `PagedResourcesAssembler`)
  unless hypermedia is an explicit product requirement.

## OpenAPI

- Every REST application has an `OpenApiConfig` bean with title, version, and
  description.
- Annotate each REST controller with `@Tag`.
- Annotate operations with `@Operation` when the mapping name is not enough.
- Localize OpenAPI prose such as titles, descriptions, summaries, and operation
  text through i18n keys. Stable technical identifiers such as tag names may
  remain literal when they are not natural-language descriptions.
- Enable and disable springdoc in profile YAML (configuration contract).

## Forbidden

- Never map REST collections outside `/api/v1/{plural-resource}`.
- Never use a trailing slash on REST mappings.
- Never return a naked body or `@ResponseStatus` void from a REST controller.
- Never omit `Location` on a resource-creating `POST`.
- Never use `PATCH` as the default update verb.
- Never put create or update fields on query parameters when a JSON body is
  appropriate.
- Never add HATEOAS as the default list representation.
- Never handle domain errors or call `RestClient` from a REST controller.
- Never name a REST endpoint class anything other than `<Feature>RestController`.
- Never use `@Controller` on a REST JSON/API endpoint class.
