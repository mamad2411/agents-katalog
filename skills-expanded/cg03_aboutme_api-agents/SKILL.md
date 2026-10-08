# CG03 AboutMe Backend

## Repository purpose

This directory contains the backend application for CG03 AboutMe.

The backend is a REST API for a personal portfolio website.

Primary technologies:

- .NET 10
- ASP.NET Core 10 Web API
- C#
- Entity Framework Core 10
- Npgsql
- PostgreSQL hosted on Supabase
- Supabase Storage
- Swagger / OpenAPI
- ProblemDetails
- Serilog
- xUnit
- Docker
- GitHub Actions

The current MVP does not include realtime chat, Redis, AI bot, or group chat.

---

## Project sources of truth

Before making non-trivial changes, inspect the relevant project documentation.

Primary documents:

- `docs/BACKEND_SPEC.md`
- `docs/database.md`

Approved implementation contracts:

- `docs/adr/0001-mvp-contract-decisions.md` for MVP architecture and scope decisions;
- `docs/api/API_CONTRACT.md` before changing routes, DTOs, status codes, publication, or disclosure behavior;
- `docs/security/THREAT_MODEL.md` before authentication, public data, upload, Contact, database-access, or secret-handling changes;
- `docs/testing/TEST_STRATEGY.md` before adding or restructuring automated tests;
- `CONTEXT.md` for canonical portfolio domain terms.

`BACKEND_SPEC.md` defines:

- backend scope;
- feature requirements;
- API conventions;
- authentication and authorization expectations;
- validation;
- file upload;
- logging;
- Docker;
- CI/CD;
- testing;
- Definition of Done.

`database.md` defines:

- PostgreSQL tables;
- relationships;
- constraints;
- indexes;
- translation tables;
- Resume versioning;
- database-specific business rules.

When documentation and implementation disagree:

1. inspect the current source code;
2. inspect EF Core migrations;
3. identify the discrepancy;
4. do not silently change architecture or database behavior;
5. report the discrepancy before making a destructive or architectural change.

Do not invent database columns, endpoints, policies, entities, or application rules that are not supported by the current code or documentation.

---

# Architecture

The backend uses a simple Layered Architecture designed for a small personal portfolio application.

The goal is to keep the codebase easy to understand, fast to develop, testable, and maintainable without introducing unnecessary patterns or abstraction layers.

The backend consists of three main projects:

```text
Portfolio.Api
Portfolio.Application
Portfolio.Infrastructure
```

The intended solution structure is:

```text
Portfolio.sln
├── src/
│   ├── Portfolio.Api/
│   ├── Portfolio.Application/
│   └── Portfolio.Infrastructure/
└── tests/
    ├── Portfolio.UnitTests/
    └── Portfolio.IntegrationTests/
```

## Runtime request flow

For most features, prefer:

```text
HTTP Request
    ↓
Controller
    ↓
IService
    ↓
Service
    ↓
IRepository
    ↓
Repository
    ↓
PortfolioDbContext
    ↓
PostgreSQL
```

Entity/model classes are data/domain representations used by the service, repository, and EF Core mapping. They are not a separate runtime execution layer.

## Dependency direction

Use abstractions at layer boundaries where they provide meaningful separation.

```text
Portfolio.Api
    ↓
IService
    ↓
Portfolio.Application
    ↓
IRepository
    ↑
Portfolio.Infrastructure implements repository abstractions
```

Important rules:

- Controllers depend on service abstractions, not concrete data-access implementations.
- Application services depend on repository abstractions, not concrete repository classes.
- Repository implementations own EF Core query and persistence details.
- `PortfolioDbContext` is an Infrastructure concern.
- Do not reference Infrastructure implementation details from controllers.
- Avoid circular dependencies between projects.

This project intentionally uses Layered Architecture, not a full Clean Architecture implementation.

Do not introduce CQRS, MediatR, domain events, event buses, specification pattern, generic repositories, or other architectural patterns unless a concrete requirement justifies them.

---

## Portfolio.Api

The API layer is responsible for HTTP and hosting concerns.

It may contain:

- Controllers
- Middleware
- Authentication configuration
- Authorization policies
- Global exception handling
- ProblemDetails
- Swagger / OpenAPI
- Dependency Injection composition root
- Health checks
- Application configuration

Controllers should:

- receive HTTP requests;
- perform model binding;
- obtain authenticated user information;
- call application service abstractions;
- return appropriate HTTP responses.

Controllers should not:

- contain business logic;
- access `PortfolioDbContext` directly;
- execute SQL directly;
- call repository implementations directly.

---

## Portfolio.Application

The Application layer contains the business and use-case logic of the portfolio.

It may contain:

- Service interfaces
- Service implementations
- Repository interfaces
- DTOs
- Request / response models
- Validators
- Mapping logic
- Business rules
- Feature-specific application models

Example structure:

```text
Portfolio.Application/
├── Common/
├── Profiles/
├── About/
├── Skills/
├── Experiences/
├── Projects/
├── Certificates/
├── Resumes/
└── Contacts/
```

Application services are responsible for use-case orchestration such as:

- validating business rules;
- checking ownership and authorization-related business conditions;
- publishing and unpublishing content;
- reordering content;
- coordinating repository operations;
- managing Resume versions;
- coordinating file upload metadata changes;
- handling transaction-sensitive business flows.

Application services should depend on abstractions.

Example:

```text
ProjectsController
    ↓
IProjectService
    ↓
ProjectService
    ↓
IProjectRepository
```

Do not create abstractions that only duplicate framework APIs without a concrete reason.

---

## Portfolio.Infrastructure

The Infrastructure layer contains persistence and external-service implementations.

It may contain:

- `PortfolioDbContext`
- EF Core entity configurations
- EF Core migrations
- Repository implementations
- PostgreSQL / Npgsql configuration
- Supabase Storage integration
- Authentication infrastructure
- External-service adapters

Example structure:

```text
Portfolio.Infrastructure/
├── Persistence/
│   ├── PortfolioDbContext.cs
│   ├── Entities/
│   ├── Configurations/
│   ├── Migrations/
│   └── Repositories/
├── Storage/
├── Authentication/
└── DependencyInjection.cs
```

Repository implementations are responsible for:

- EF Core queries;
- persistence operations;
- projections where appropriate;
- database-specific query details;
- loading entities required by application services.

Repositories must not contain application business rules.

---

# Repository and Unit of Work policy

Use feature-specific repositories as the persistence boundary.

Examples:

- `IProjectRepository`
- `ISkillRepository`
- `IExperienceRepository`
- `ICertificateRepository`
- `IResumeRepository`
- `IContactRepository`

Repository interfaces should model meaningful feature-specific persistence operations rather than generic CRUD APIs.

Prefer:

```csharp
public interface IProjectRepository
{
    Task<bool> SlugExistsAsync(
        string slug,
        CancellationToken cancellationToken);

    Task<Project?> GetByIdAsync(
        Guid id,
        CancellationToken cancellationToken);

    Task<Project?> GetPublishedBySlugAsync(
        string slug,
        string locale,
        CancellationToken cancellationToken);

    Task AddAsync(
        Project project,
        CancellationToken cancellationToken);
}
```

Avoid generic repositories such as:

```csharp
IRepository<T>
```

when they only duplicate `DbSet<T>` CRUD operations.

Do not introduce a custom Unit of Work abstraction solely to wrap Entity Framework Core.

Use EF Core `DbContext` as the Unit of Work implementation.

Use:

- change tracking;
- `SaveChangesAsync()`;
- EF Core transaction APIs;

for operations that must be committed atomically.

Do not create `IUnitOfWork` / `UnitOfWork` if they only forward calls to `PortfolioDbContext.SaveChangesAsync()`.

For multi-step operations, use the same scoped `PortfolioDbContext` instance and an explicit EF Core transaction when necessary.

---

# SOLID and Dependency Injection

Apply SOLID pragmatically.

## Single Responsibility Principle

Keep responsibilities separated:

```text
Controller
→ HTTP concerns

Service
→ business/use-case logic

Repository
→ persistence logic

DbContext
→ EF Core persistence/session management
```

## Open/Closed Principle

Introduce abstractions when a dependency has meaningful variability or multiple implementations.

Examples where interfaces are valuable:

- file storage;
- email sender;
- current user accessor;
- external API clients;
- authentication adapters.

## Liskov Substitution Principle

Implementations must preserve the contracts defined by their abstractions.

Do not create interfaces whose implementations behave inconsistently with the expected contract.

## Interface Segregation Principle

Prefer small feature-specific interfaces.

Do not create large "god interfaces" containing unrelated operations.

## Dependency Inversion Principle

High-level application logic should depend on abstractions rather than concrete low-level repository implementations.

Prefer:

```text
ProjectService
    ↓
IProjectRepository
    ↑
ProjectRepository
```

rather than:

```text
ProjectService
    ↓
ProjectRepository
```

Use Dependency Injection for runtime composition.

Register dependencies centrally in the composition root.

Example:

```csharp
services.AddScoped<IProjectService, ProjectService>();
services.AddScoped<IProjectRepository, ProjectRepository>();
```

Do not instantiate application services, repositories, DbContext, storage clients, or infrastructure services manually inside controllers.

---

# Database

PostgreSQL is the durable source of truth.

Database access uses Entity Framework Core 10 and Npgsql.

Before changing persistence:

1. inspect `database.md`;
2. inspect the relevant entity/model;
3. inspect EF Core entity configuration;
4. inspect existing migrations;
5. inspect the repository queries;
6. inspect affected API/application behavior.

For schema changes consider:

- primary keys;
- foreign keys;
- nullability;
- unique constraints;
- check constraints;
- default values;
- indexes;
- cascade behavior;
- timestamps;
- migration compatibility.

Do not modify an existing migration that may already have been applied.

Create a new migration instead.

---

# Multilingual content

The portfolio supports English (`en`) and Vietnamese (`vi`).

Translated content is stored in translation tables such as:

- `profile_translations`
- `about_translations`
- `skill_category_translations`
- `technology_translations`
- `experience_translations`
- `project_translations`
- `project_image_translations`
- `certificate_translations`
- `resume_translations`

Do not duplicate translated text into base tables without a deliberate schema decision.

When implementing publish operations, preserve translation completeness rules defined by the application specification.

---

# Querying with EF Core

For read-only public queries:

- prefer projection to response DTOs;
- use `AsNoTracking()` where tracking is unnecessary;
- avoid loading full object graphs when only a subset of fields is required;
- avoid N+1 query patterns;
- inspect generated SQL for non-trivial queries;
- use pagination where list size can grow;
- apply filtering and ordering in SQL, not in memory.

Do not add indexes speculatively.

Indexes must correspond to real filter, join, ordering, uniqueness, or performance requirements.

---

# Transactions

Use EF Core transactions when multiple changes must succeed or fail together.

Examples include:

- reordering multiple records;
- allocating a Resume version and inserting the Resume metadata;
- switching the active Resume;
- replacing file metadata;
- updating multiple related entities that form one business operation.

Prefer one logical commit per use case where practical.

Avoid scattered `SaveChangesAsync()` calls without a clear reason.

Pass `CancellationToken` through the full call chain:

```text
Controller
→ Service
→ Repository
→ EF Core / Storage
```

---

# API conventions

Base API route:

```text
/api/v1
```

Use appropriate status codes:

- 200 for successful reads/updates;
- 201 for resource creation;
- 204 for successful deletion with no body;
- 400 for invalid requests/business validation;
- 401 for unauthenticated requests;
- 403 for authenticated but unauthorized requests;
- 404 for missing resources;
- 409 for conflicts;
- 413 for oversized uploads;
- 429 for rate limiting;
- 500 for unexpected server failures.

Use RFC Problem Details for error responses.

Do not expose stack traces, SQL internals, secrets, JWTs, service-role keys, or connection strings to clients.

---

# Validation

Validation has three levels.

## DTO validation

Use for:

- required values;
- string length;
- format;
- range;
- basic structural validation.

## Application rules

Use for:

- ownership;
- duplicate slug detection;
- publish rules;
- Resume current-version transitions;
- relationships between resources;
- business state transitions.

## Database invariants

Use PostgreSQL constraints for rules that must remain valid regardless of application code.

Examples:

- unique keys;
- foreign keys;
- check constraints;
- one active Resume per language;
- valid date relationships where appropriate.

Do not rely solely on frontend validation.

---

# Authentication and authorization

Do not trust authorization information supplied by the client.

Never use request fields such as:

- `userId`;
- `isAdmin`;
- ownership flags;

as proof of authorization.

Authenticated identity must come from the authenticated server-side context.

All `/admin` endpoints require the configured Admin authorization policy.

Ownership must be verified when operations are owner-scoped.

Never log:

- passwords;
- access tokens;
- refresh tokens;
- service-role keys;
- database connection strings.

The current authentication implementation must follow the final project decision documented in the source/specification. If authentication documentation conflicts, report the conflict before implementing authentication-sensitive changes.

---

# File uploads

Uploaded files must not be stored permanently on the application container filesystem.

Use object storage such as Supabase Storage.

For uploads:

1. verify a file exists;
2. verify file size is greater than zero;
3. enforce configured size limits;
4. validate allowed extension;
5. validate MIME/content type where appropriate;
6. generate a server-side storage key;
7. upload the new object;
8. persist metadata;
9. clean up the newly uploaded object if database persistence fails;
10. delete the previous object only after the new state is safely persisted.

Never use the raw client file name as the storage key.

Do not trust arbitrary storage paths supplied by clients.

---

# Resume versioning

Resume version numbers are server-generated.

The client must not determine Resume version.

Version allocation and active Resume transitions must follow the rules defined in `database.md`.

Changing metadata or publish/current state must not incorrectly create a new version.

Replacing the actual Resume file means creating a new Resume version rather than overwriting historical versions.

The version counter update, Resume insert, and active Resume transition must be transaction-safe.

---

# Public portfolio rules

Public APIs must return only content allowed to be public.

Do not expose drafts.

Projects with restricted or limited disclosure must be sanitized on the server.

Do not rely on frontend CSS, hidden fields, or frontend filtering to protect private data.

---

# Contact endpoint

The public Contact endpoint requires:

- input validation;
- email validation;
- field-length limits;
- rate limiting;
- spam mitigation where configured.

Public users may create contact messages but must not be able to read the contact inbox.

Notification side effects must not cause an already-persisted contact message to be lost.

---

# Error handling

Use centralized exception handling.

Prefer:

```csharp
builder.Services.AddProblemDetails();
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();

app.UseExceptionHandler();
```

Map known application exceptions to stable HTTP responses.

Unexpected exceptions:

- should be logged server-side;
- should return HTTP 500;
- must not expose implementation details.

Include a request or trace identifier where possible for log correlation.

Do not add repetitive `try/catch` blocks to controllers when the exception can be handled globally.

---

# Logging

Use structured logging with Serilog.

Log useful context such as:

- request/trace ID;
- HTTP method;
- route/path;
- status code;
- duration;
- relevant resource ID where safe.

Do not log secrets or sensitive authentication data.

Avoid logging entire uploaded file contents, request bodies containing secrets, or raw credentials.

---

# Testing

Use:

- xUnit for unit tests;
- integration tests for persistence and API boundaries.

Follow the AAA pattern for unit tests:

```text
Arrange
Act
Assert
```

Use unit tests primarily for:

- service business rules;
- validators;
- mapping logic;
- authorization-related application behavior;
- important regressions;
- pure logic.

Repository and persistence behavior should be covered with integration tests where practical.

Do not rely on mocks to prove EF Core queries, PostgreSQL constraints, transactions, or migrations work correctly.

Important test scenarios include:

- happy path;
- validation failure;
- authorization failure;
- ownership failure;
- not found;
- conflicts;
- transaction-sensitive behavior;
- important database constraints.

Mock interfaces at meaningful boundaries.

Examples:

```text
Controller test
→ mock IService

Service unit test
→ mock IRepository / storage / external interfaces

Repository integration test
→ real DbContext + PostgreSQL-compatible test database
```

---

# Change discipline

Before editing code:

1. read the applicable `AGENTS.md`;
2. inspect the responsible project and feature;
3. inspect neighboring implementations;
4. inspect tests;
5. inspect `BACKEND_SPEC.md` when feature behavior is involved;
6. inspect `database.md` when persistence is involved;
7. inspect migrations before schema changes.

Prefer:

- minimal coherent changes;
- existing project conventions;
- root-cause fixes;
- explicit tradeoffs;
- readable code;
- simple feature-specific abstractions.

Avoid:

- speculative refactoring;
- unrelated cleanup;
- unnecessary abstraction;
- generic repository wrappers over EF Core;
- custom Unit of Work wrappers over `DbContext` without concrete value;
- CQRS/MediatR without a real need;
- adding libraries without demonstrated need;
- changing API contracts without identifying consumers.

---

# Skill usage

Use `systematic-debugging` when:

- behavior is incorrect;
- the root cause is unknown;
- builds fail unexpectedly;
- tests fail unexpectedly;
- deployment/runtime behavior differs from expectations.

Do not modify code before collecting enough evidence to identify a credible root cause.

Use `writing-plans` when:

- a feature spans multiple layers;
- a database migration is required;
- an API contract changes;
- authentication/authorization architecture changes;
- deployment architecture changes;
- a change affects multiple features or external systems.

Use `test-driven-development` when the behavior can reasonably be expressed as tests before implementation, especially for:

- application service rules;
- validators;
- authorization behavior;
- important regression fixes;
- deterministic business logic.

Use `verification-before-completion` before declaring implementation complete.

Use `karpathy-guidelines` as general implementation discipline:

- understand before editing;
- prefer simple solutions;
- make surgical changes;
- avoid unnecessary scope expansion;
- verify behavior instead of assuming correctness.

---

# Verification

Before claiming completion, run checks relevant to the change.

Typical backend verification:

```bash
dotnet restore
dotnet build --configuration Release
dotnet test --configuration Release
```

When migrations are changed, inspect:

```bash
dotnet ef migrations list \
  --project src/Portfolio.Infrastructure \
  --startup-project src/Portfolio.Api
```

For deployment-related changes, also verify:

```bash
docker build .
```

Do not claim that a change works based only on source inspection when executable verification is available.

Report explicitly:

- which commands were run;
- which passed;
- which were not run;
- why any verification was skipped.

---

# Definition of Done

A backend feature is not complete until the relevant parts of the following have been satisfied:

- API contract implemented;
- DTO validation implemented;
- business rules implemented;
- authentication and authorization checked;
- ownership checked where required;
- repository behavior implemented;
- database migration/index/constraint impact reviewed;
- transaction requirements reviewed;
- ProblemDetails behavior preserved;
- logging considered;
- tests added or updated where appropriate;
- Swagger/OpenAPI updated;
- solution builds successfully;
- relevant tests pass;
- Docker build checked when deployment is affected.
