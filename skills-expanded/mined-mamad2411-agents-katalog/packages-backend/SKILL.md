---
name: packages-backend
description: NuGet package management for the BallastLane backend — always install latest stable (never pin from memory), the core package set (MediatR, AutoMapper, FluentValidation, EF Core SqlServer, NUnit, BCrypt, JwtBearer), and when to adopt Directory.Packages.props. Load this skill before running `dotnet add package`, choosing a library, or setting up a new .csproj.
---

# Package Management — Backend (NuGet)

## Always Use Latest Stable Versions

- **Never hardcode package versions from memory.** Training data may reference outdated versions of MediatR, EF Core, or FluentValidation. Verify the latest stable release before adding a package.
- **Run `dotnet add package <name>` without `--version`** to pull the latest stable automatically.

```bash
# DO
dotnet add package MediatR
dotnet add package AutoMapper
dotnet add package FluentValidation
dotnet add package FluentValidation.DependencyInjectionExtensions
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package NUnit
dotnet add package NUnit3TestAdapter
dotnet add package Microsoft.NET.Test.Sdk

# DON'T
dotnet add package MediatR --version 9.0.0
```

## Core Package Set for This Project

| Concern | Package |
|---|---|
| CQRS / mediator | `MediatR` |
| Object mapping | `AutoMapper` (+ `AutoMapper.Extensions.Microsoft.DependencyInjection` if not bundled) |
| Validation | `FluentValidation`, `FluentValidation.DependencyInjectionExtensions` |
| ORM | `Microsoft.EntityFrameworkCore.SqlServer`, `Microsoft.EntityFrameworkCore.Tools` |
| Testing | `NUnit`, `NUnit3TestAdapter`, `Microsoft.NET.Test.Sdk` |
| Assertions (optional, improves readability) | `FluentAssertions` or `Shouldly` |
| JWT | `Microsoft.AspNetCore.Authentication.JwtBearer` |
| Password hashing | ASP.NET Identity's `PasswordHasher<T>` (via `Microsoft.AspNetCore.Identity`) or `BCrypt.Net-Next` |

## Central Package Management

- **Use `Directory.Packages.props` if the solution grows past 2–3 projects**, to pin versions once instead of per-`.csproj`. For a take-home exercise scoped to 4 projects + tests, this is optional but keeps version drift from creeping in as the solution grows.

## Version Verification

- If unsure of the latest version, check NuGet.org directly rather than guessing.
- **Never downgrade an already-installed package** without an explicit reason (known incompatibility).
- Prefer stable releases over preview/RC packages for a project meant to demo cleanly.
