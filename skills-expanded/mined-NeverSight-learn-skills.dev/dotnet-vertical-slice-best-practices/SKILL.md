---
name: dotnet-vertical-slice-best-practices
description: Implement and evolve .NET backends using vertical slices, explicit validation and error handling, PostgreSQL persistence, dedicated EF Core migrations, clear AppHost/API composition boundaries, centralized solution defaults through Directory.Build.props and Directory.Packages.props, and GitHub Actions build/versioning practices for backend and migrator images. Use when a coding assistant needs to create or change backend features, endpoints, commands, queries, handlers, contracts, persistence, migrations, startup composition, GitHub CI artifacts, or modernization-sensitive .NET backend behavior.
compatibility: Designed for Agent Skills-compatible coding assistants, including OpenAI Codex, GitHub Copilot-compatible environments, and Claude Code-style clients.
metadata:
  version: "1.4.0"
---

# .NET Backend Vertical Slice

Use this skill when backend code needs to be planned, implemented, devops, databases, or refined in a .NET application that follows a vertical-slice style.

## Core rule

Keep behavior local to the use case, preserve stable API contracts, and treat persistence, validation,
error handling, and migrations as part of the same backend change.

## Working flow

1. Inspect the repository structure and preserve valid local conventions.
2. Identify the affected use case, route, request, response, and persistence impact.
3. Minimize the amount of logic in the transport layer; focus on routing and serialization only, and keep all business logic and validation within the same handler or module associated with the slice.
4. Address concerns in this priority order:
   - First: validation rules and expected failure paths.
   - Second: authorization and ownership checks.
   - Third: migrations and persistence changes.
5. Load the references that apply using the decision table below:

   | Task involves…                                                                 | Load this reference              |
   |--------------------------------------------------------------------------------|----------------------------------|
   | Minimal APIs, route groups, HTTP result mapping, or OpenAPI                    | dotnet-minimal-api.md            |
   | Commands, queries, handlers, or MediatR slices                                  | dotnet-cqrs-slice.md             |
   | Startup composition, project boundaries, or solution-wide build/package defaults | dotnet-solution-topology.md      |
   | Dedicated migrator or containerized local backend startup                        | dotnet-migrations-project.md; create or update `compose.yml` so `docker compose up` runs dependencies and migrations in order |
   | GitHub Actions build workflows, release images, or backend/migrator artifact versioning | devops-github.md |
   | Modernization or version-sensitive upgrades                                     | dotnet-platform-baseline.md (load before recommending upgrades) |

6. Run the most relevant verification for the touched backend surface.

## Required checklist

For every meaningful backend change, reason through the following categories in order:

**1. Use Case and Contracts** (start here)
- slice or feature affected;
- command or query semantics;
- endpoint and route behavior;
- request and response contracts;

**2. Validation and Authorization**
- validation rules;
- expected business errors;
- authorization and ownership checks;

**3. Persistence and Migrations**
- persistence impact;
- migration impact;

**4. Composition and Caller Impact**
- host/composition or solution-boundary impact when relevant;
- caller impact.

## Reference files

Load only the references that apply:

- [dotnet-minimal-api.md](references/dotnet-minimal-api.md)
  Covers Minimal API endpoint structure, route groups, `IEndpoint` registration, result mapping, `ProblemDetails`, and OpenAPI expectations.
- [dotnet-cqrs-slice.md](references/dotnet-cqrs-slice.md)
  Covers CQRS/MediatR slice structure, request shapes, handler rules, and query/command boundaries.
- [dotnet-vertical-slice.md](references/dotnet-vertical-slice.md)
  Explains slice structure, file responsibilities, contract boundaries, and version-discipline expectations.
- [dotnet-validation-and-errors.md](references/dotnet-validation-and-errors.md)
  Covers request validation, business validation, expected failure modeling, and HTTP response consistency.
- [dotnet-migrations-project.md](references/dotnet-migrations-project.md)
  Covers dedicated EF Core migrations projects, executable migration runners, Compose orchestration, migration quality, and persistence-change checks.
- [dotnet-solution-topology.md](references/dotnet-solution-topology.md)
  Covers `AppHost` versus `Api` responsibilities, `Directory.Build.props`, `Directory.Packages.props`, and container-build expectations.
- [dotnet-platform-baseline.md](references/dotnet-platform-baseline.md)
  Provides the current stable .NET modernization baseline and upgrade review checklist.
- [devops-github.md](references/devops-github.md)
  Covers GitHub Actions build triggers on `main`, backend and migrator image artifacts, and shared image-tag versioning.

## Output shape

When reporting implementation work, prefer this structure:

```markdown
## Scope

## Skills Used

## Files Changed

## Impacted Contracts

## Persistence And Migrations

## Verification Run

## Frontend Impact

## Open Risks
```
