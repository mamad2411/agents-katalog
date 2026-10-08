---
name: domain-layer
description: >-
  Use this skill when creating or modifying entities, value objects, enums, domain errors, or any code in the Architecture.Domain project. Guides file placement, BaseEntity usage, Result pattern, and error definition conventions.
---

# Domain Layer Skill

This skill teaches the AI agent how to work with the Domain layer of a Clean Architecture .NET 10 project.

## 1. Layer Role
- **Domain** = pure business logic, zero NuGet dependencies, zero project references.
- **Project**: Architecture.Domain (target: net10.0)
- **Depends on**: NOTHING

## 2. File Structure Reference
```text
Architecture.Domain/
├── Common/
│   ├── BaseEntity/
│   │   └── BaseEntity.cs          → Abstract base for all entities
│   └── Results/
│       ├── Error.cs               → Typed error record
│       ├── ErrorType.cs           → Error category enum
│       └── Result.cs              → Result<T> pattern
├── Entities/
│   └── {EntityName}.cs            → Domain entities
└── Enums/
    └── {EnumName}.cs              → Domain enums
```

## 3. Creating a New Entity
When creating a new entity, follow this pattern:
- Inherit from `BaseEntity` (namespace: `Architecture.Domain.Common.BaseEntity`)
- `BaseEntity` provides `Guid Id` with a protected setter, parameterless constructor (auto `Guid.NewGuid()`), and explicit `Guid` constructor.
- Use **private setters** for all properties.
- Add a constructor with validation/invariants.
- Add behavior methods (avoid anemic domain models).
- Place the file in the `Entities/` folder.
- Use namespace: `Architecture.Domain.Entities`

**Example:**
```csharp
using Architecture.Domain.Common.BaseEntity;

namespace Architecture.Domain.Entities;

public class Product : BaseEntity
{
    public string Name { get; private set; }
    public string Description { get; private set; }
    public decimal Price { get; private set; }

    private Product() { } // EF Core

    public Product(string name, string description, decimal price)
    {
        Name = name ?? throw new ArgumentNullException(nameof(name));
        Description = description ?? throw new ArgumentNullException(nameof(description));
        SetPrice(price);
    }

    public void SetPrice(decimal price)
    {
        if (price < 0) throw new ArgumentException("Price cannot be negative.", nameof(price));
        Price = price;
    }

    public void UpdateDetails(string name, string description)
    {
        Name = name ?? throw new ArgumentNullException(nameof(name));
        Description = description ?? throw new ArgumentNullException(nameof(description));
    }
}
```

## 4. Defining Domain Errors
**Pattern**: Create a static class per entity for its errors. Place errors next to or near the entity, or in a shared errors location within Domain.

**Example:**
```csharp
using Architecture.Domain.Common.Results;

namespace Architecture.Domain.Entities;

public static class ProductErrors
{
    public static Error NotFound(Guid id) =>
        Error.NotFound("Product.NotFound", $"Product with ID '{id}' was not found.");

    public static Error DuplicateName(string name) =>
        Error.Conflict("Product.DuplicateName", $"A product with name '{name}' already exists.");

    public static readonly Error InvalidPrice =
        Error.Validation("Product.InvalidPrice", "Product price must be greater than zero.");
}
```

**ErrorType enum values and their meanings:**
- `Failure` (0) — generic failure
- `Validation` (1) — input validation error → maps to HTTP 400
- `NotFound` (2) — entity not found → maps to HTTP 404
- `Conflict` (3) — duplicate/conflict → maps to HTTP 409
- `Unauthorized` (4) — not authenticated → maps to HTTP 401
- `Forbidden` (5) — not authorized → maps to HTTP 403

## 5. Using Result<T>
Here are the actual `Result.cs` patterns to use:
- `Result.Success()` — non-generic success
- `Result.Failure(error)` — non-generic failure
- `Result.Success<T>(value)` — generic success
- `Result.Failure<T>(error)` — generic failure
- **Implicit conversions**: `TValue` → `Result<TValue>` (auto success), `Error` → `Result<TValue>` (auto failure)
- `Error.None` and `Error.NullValue` are built-in constants.

## 6. Enums
- Place in the `Enums/` folder.
- Use namespace: `Architecture.Domain.Enums`
- Use only for domain-meaningful constants.

## 7. Error Handling — Step 1: Creating Errors
Errors are CREATED in the Domain layer and flow outward:
- Domain creates `Error` → Application returns `Result<T>` with that error → API maps to HTTP status codes.
- Use typed `ErrorType` to ensure correct HTTP status code mapping downstream.

## 8. Feature Workflow — Step 1: Domain Layer
When building a new feature:
1. Create the entity in `Entities/` (if a new entity is needed).
2. Define domain errors in a `{Entity}Errors` static class.
3. Add any enums to `Enums/`.
4. Next → refer to the infrastructure-layer skill (Step 2).

## 9. Rules (CRITICAL)
- ❌ **NEVER** add NuGet packages to this project.
- ❌ **NEVER** reference other projects (no EF Core, no MediatR, no ASP.NET).
- ❌ **NEVER** use data annotations (`[Required]`, `[MaxLength]`, etc.) — use EF Core Fluent API in Infrastructure.
- ✅ **ALWAYS** use private setters.
- ✅ **ALWAYS** validate in constructors.
- ✅ **ALWAYS** use `BaseEntity` as the base class for entities.
- ✅ **ALWAYS** use `Error` factory methods (`Error.NotFound`, `Error.Validation`, etc.).
