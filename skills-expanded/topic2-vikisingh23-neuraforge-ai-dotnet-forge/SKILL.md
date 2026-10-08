---
name: dotnet-forge
description: Generate production-ready .NET Core APIs with Entity Framework, repository pattern, CQRS, and enterprise standards
category: software-development
triggers:
  - "build a dotnet api"
  - "create .net api"
  - "generate c# api"
---

# .NET API Generation

Generate a complete .NET Core API following enterprise enterprise patterns.

## Instructions

1. Read `agents/forge.md` for the full .NET code generation workflow
2. Read `backend/REPOSITORY_PATTERN.md` and `backend/DOTNET_ADVANCED_PATTERNS.md` for patterns
3. Read `core/NAMING_CONVENTIONS.md` for naming standards
4. Follow the architecture principles: thin controllers, reuse existing services, single responsibility
5. Always include: Entity + DTO + Repository + Service + Controller + FluentValidation + Tests + Migration
6. Audit fields (CreatedBy, ModifiedBy, CreatedAt, ModifiedAt) on ALL entities
7. Soft deletes mandatory — never hard delete financial data
8. Pagination on ALL list endpoints
9. `decimal` for money — never float/double
