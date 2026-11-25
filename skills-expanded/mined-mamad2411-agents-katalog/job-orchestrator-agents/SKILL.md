# AGENTS.md

This file helps AI coding agents become productive quickly in this repository.

## Scope

- Main library: [JobOrchestrator.Core](JobOrchestrator.Core)
- Optional UI package: [JobOrchestrator.Dashboard](JobOrchestrator.Dashboard)
- Sample consumer app: [Samples/JobOrchestrator.Api](Samples/JobOrchestrator.Api)

## Start Here

- Overview and quick usage: [README.md](README.md)
- Full package usage and exception patterns: [README_NUGET.md](README_NUGET.md)
- Architecture and refactoring history: [REFACTORING.md](REFACTORING.md)
- NuGet packaging refactor notes: [NUGET_REFACTORING.md](NUGET_REFACTORING.md)

Prefer linking to those docs instead of duplicating their content in code comments or PR descriptions.

## Build, Run, and Pack

Run from repository root unless noted.

- Restore: dotnet restore
- Build all: dotnet build
- Run sample API: dotnet run --project Samples/JobOrchestrator.Api/JobOrchestrator.Api.csproj
- Pack core library: dotnet pack JobOrchestrator.Core/JobOrchestrator.Core.csproj

Notes:

- The solution is in [JobOrchestrator.slnx](JobOrchestrator.slnx).
- There are currently no test projects in this repository.

## Architecture Boundaries

- Public entrypoint for registration is [JobOrchestrator.Core/Services/ServiceCollectionExtensions.cs](JobOrchestrator.Core/Services/ServiceCollectionExtensions.cs).
- Consumers implement handlers via [JobOrchestrator.Core/Services/IJobHandler.cs](JobOrchestrator.Core/Services/IJobHandler.cs).
- Core business flow lives in services and repositories under [JobOrchestrator.Core/Services](JobOrchestrator.Core/Services) and [JobOrchestrator.Core/Repositories](JobOrchestrator.Core/Repositories).
- Persistence is EF Core in [JobOrchestrator.Core/Data/SchedulerDbContext.cs](JobOrchestrator.Core/Data/SchedulerDbContext.cs) with migrations in [JobOrchestrator.Core/Migrations](JobOrchestrator.Core/Migrations).
- HTTP exception mapping middleware is optional and in [JobOrchestrator.Core/Middleware/GlobalExceptionHandlingMiddleware.cs](JobOrchestrator.Core/Middleware/GlobalExceptionHandlingMiddleware.cs).

When changing public contracts, validate impact on both the sample API and dashboard projects.

## Conventions to Follow

- Keep nullable reference types enabled and avoid introducing nullable warnings.
- Preserve async flow and CancellationToken usage across service and handler APIs.
- Continue exception-first behavior using custom types in [JobOrchestrator.Core/Exceptions](JobOrchestrator.Core/Exceptions).
- Keep DI registration patterns fluent and consistent with [JobOrchestrator.Core/Services/ServiceCollectionExtensions.cs](JobOrchestrator.Core/Services/ServiceCollectionExtensions.cs).
- Use repository abstractions instead of bypassing them with direct service-level DbContext access.

## Common Pitfalls

- After calling AddScheduler, storage must be configured with UseInMemoryStorage or UseSqlServer (see [JobOrchestrator.Core/Services/ServiceCollectionExtensions.cs](JobOrchestrator.Core/Services/ServiceCollectionExtensions.cs)).
- Dashboard and middleware are optional; avoid forcing web-only dependencies into core logic.
- If schema changes are introduced, update migrations under [JobOrchestrator.Core/Migrations](JobOrchestrator.Core/Migrations).

## Change Workflow for Agents

- Keep edits minimal and scoped to the requested behavior.
- Do not create commits unless the user explicitly asks for a commit.
- Do not refactor unrelated areas in the same change.
- If touching public APIs, update docs in [README_NUGET.md](README_NUGET.md) and sample usage in [Samples/JobOrchestrator.Api/Program.cs](Samples/JobOrchestrator.Api/Program.cs) when needed.
- If you add tests in future PRs, place them in a dedicated test project instead of mixing tests into production projects.