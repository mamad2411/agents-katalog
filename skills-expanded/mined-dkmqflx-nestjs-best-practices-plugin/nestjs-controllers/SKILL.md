---
name: nestjs-controllers
description: NestJS controller and routing best practices. Use when writing or reviewing NestJS controllers, route handlers, DTOs, or request/response handling. Triggers on @Controller, @Get/@Post, route params, DTOs, serialization, or API versioning.
license: MIT
metadata:
  author: nestjs
  version: "1.0.0"
---

# NestJS Controllers & Routing

Controllers are the entry point of a NestJS HTTP application: they bind routes to handlers, extract and validate request data, and shape responses. The framework gives you a lot for free (status codes, serialization, validation, versioning) — but only when you stay on the idiomatic path. These rules keep controllers thin, type-safe, and aligned with NestJS v10/v11 conventions so you don't accidentally opt out of framework features.

## When to Apply

- Writing or reviewing classes decorated with `@Controller`
- Adding route handlers with `@Get`, `@Post`, `@Put`, `@Patch`, `@Delete`
- Extracting request data via `@Param`, `@Query`, `@Body`, `@Req`, `@Res`
- Defining DTO classes for request bodies
- Controlling response status codes and serialization
- Designing RESTful resource paths or versioning a public API

## Rules

- [thin-controllers](rules/thin-controllers.md) — CRITICAL — controllers only route and validate; business logic lives in services
- [dto-request-bodies](rules/dto-request-bodies.md) — HIGH — typed DTO classes for `@Body`, never `any`
- [async-handlers-return-promises](rules/async-handlers-return-promises.md) — MEDIUM — return promises/observables and let Nest resolve them
- [param-decorators-over-req](rules/param-decorators-over-req.md) — HIGH — use `@Param`/`@Query`/`@Body`, avoid raw `@Req`/`@Res`
- [restful-resource-routing](rules/restful-resource-routing.md) — MEDIUM — consistent resource paths, plural nouns, proper HTTP verbs
- [http-status-codes](rules/http-status-codes.md) — MEDIUM — use `@HttpCode` for non-default statuses (e.g. 201/204)
- [serialize-responses](rules/serialize-responses.md) — CRITICAL — `ClassSerializerInterceptor` + `@Exclude` to hide sensitive fields
- [api-versioning](rules/api-versioning.md) — LOW — `enableVersioning` for evolving public APIs

## How to Use

Read individual rule files in `rules/`.
