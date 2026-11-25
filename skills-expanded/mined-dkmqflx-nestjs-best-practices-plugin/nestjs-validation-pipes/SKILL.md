---
name: nestjs-validation-pipes
description: NestJS validation and pipes best practices. Use when validating or transforming request input in NestJS — DTO validation, ValidationPipe, class-validator/class-transformer, or custom pipes. Triggers on ValidationPipe, @IsString/@IsEmail, ParseIntPipe, whitelist, or transform.
license: MIT
metadata:
  author: nestjs
  version: "1.0.0"
---

# NestJS Validation & Pipes

Pipes run before route handlers to validate and transform incoming request data. Combined with `class-validator` and `class-transformer`, they keep DTOs the single source of truth for input shape and constraints.

## When to Apply

- Validating request bodies, query params, or route params in a NestJS app.
- Configuring `ValidationPipe` (globally or per-route).
- Annotating DTOs with `class-validator` decorators.
- Coercing param types with built-in parse pipes (`ParseIntPipe`, `ParseUUIDPipe`, ...).
- Writing a reusable custom pipe via `PipeTransform`.

## Rules

- `global-validation-pipe` - Register `ValidationPipe` once in `main.ts` so every endpoint is validated.
- `whitelist-strip-unknown` - Use `whitelist` + `forbidNonWhitelisted` to strip or reject unexpected properties.
- `transform-payloads` - Enable `transform: true` to auto-instantiate DTO classes and coerce primitive types.
- `dto-classes-not-interfaces` - Define DTOs as classes; interfaces are erased at runtime and carry no metadata.
- `class-validator-decorators` - Annotate every DTO field with `class-validator` decorators.
- `nested-object-validation` - Use `@ValidateNested` + `@Type` to validate nested DTOs and arrays.
- `built-in-parse-pipes` - Use `ParseIntPipe`/`ParseUUIDPipe`/`ParseBoolPipe` to coerce and validate params.
- `custom-pipe-implementation` - Implement `PipeTransform` for reusable custom validation or transformation.

## How to Use

Read the relevant file under `rules/` for the topic at hand. Each rule states why it matters and shows an incorrect vs. correct example. Apply them when writing or reviewing NestJS input-handling code.
