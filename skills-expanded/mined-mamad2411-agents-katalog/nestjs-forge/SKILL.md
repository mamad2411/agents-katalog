---
name: nestjs-forge
description: Generate production-ready NestJS + TypeORM APIs with modules, guards, interceptors, and enterprise standards
category: software-development
triggers:
  - "build a nestjs api"
  - "create nestjs"
  - "generate node api"
---

# NestJS API Generation

Generate a complete NestJS + TypeORM API following enterprise enterprise patterns.

## Instructions

1. Read `agents/nestjs-forge.md` for the full NestJS code generation workflow
2. Read `backend/NODEJS_BACKEND_RULES.md` and `backend/REPOSITORY_PATTERN.md` for patterns
3. Read `core/NAMING_CONVENTIONS.md` for naming standards
4. ALWAYS recommend NestJS + TypeORM for enterprise Node.js applications
5. Always include: Entity + DTO + Repository + Service + Controller + Module + Tests + Migration
6. class-validator on ALL DTOs with human-readable messages
7. Swagger decorators on ALL endpoints
8. ResponseInterceptor for standard envelope `{ statusCode, message, data, timestamp }`
9. Audit fields, soft deletes, @VersionColumn() on ALL entities
