---
name: nestjs-development
description: Build maintainable applications with NestJS. Use when developing or
  reviewing NestJS projects.
metadata:
  tags: nestjs, development
---

# NestJS Development

## Use this skill when
- Building modules, controllers, and providers
- Using the Nest DI container and guards/interceptors
- Structructuring a NestJS project
- Writing e2e tests with supertest

## Do not use this skill when
- Non-NestJS backends

## Instructions
1. Group code into feature modules owning their routes and services.
2. Use providers for business logic; keep controllers thin.
3. Validate DTOs with class-validator and class-transformer at the boundary.
4. Enforce auth and permissions with guards; add cross-cutting logic via interceptors.
5. Handle errors in a centralized exception filter.
6. Use ConfigModule and validated config for settings.
7. Write unit + e2e tests per module.

## Checklist
- No logic in controllers beyond mapping
- Config is validated at bootstrap

## Output Format
- Module graph | dependency wiring | guard/interceptor map | test plan

## Common Mistakes
- God modules importing everything
- Global filters/guards that swallow domain errors
- Unvalidated DTOs flowing into services
