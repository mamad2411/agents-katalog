---
name: minimal-api-scaffolder
audience: team
description: >
  Scaffolds .NET 10 Minimal API endpoints with OpenAPI documentation, versioning strategies, and
  security patterns. Use when creating REST APIs, adding endpoints, setting up API projects, or
  configuring API infrastructure. Do NOT use when the project is controller-based MVC — use
  dotnet-vertical-slice for handler architecture instead.
---

# .NET 10 Minimal API Scaffolder

> "Minimal APIs are ideal for microservices and apps that want to include only the minimum files, features, and dependencies in ASP.NET Core."
> -- Microsoft Documentation

> "A good API is not just easy to use but also hard to misuse."
> -- Joshua Bloch

## Core Philosophy

This skill scaffolds and maintains Minimal API endpoints in .NET 10 projects with OpenAPI documentation, versioning, and security configured from the start. Every API begins with a clear contract, validated inputs, and documented responses.

**Non-Negotiable Constraints:**

1. **OpenAPI-First Design** — Every endpoint must have OpenAPI metadata: name, summary, request/response types, and status codes. No endpoint ships without `.WithName()`, `.WithSummary()`, and `.Produces<T>()`.
2. **Versioning from Day One** — API versioning is configured at project creation, not retrofitted. Every endpoint group includes a version segment. There is no "we'll add versioning later."
3. **Security by Default** — Groups default to `.RequireAuthorization()`. Anonymous access is an explicit opt-in via `.AllowAnonymous()`, never an implicit default.
4. **Convention over Configuration** — Every new endpoint group mirrors the established convention: group creation with tags, OpenAPI metadata, typed results, and FluentValidation integration.
5. **Typed Results, Not Raw Responses** — All handlers return `TypedResults` with explicit union return types (`Results<Ok<T>, NotFound, ValidationProblem>`). No raw `IResult`, no untyped `Results.Ok()`, no status code magic numbers.

## Workflow

The scaffold lifecycle flows: **CONFIGURE → SCAFFOLD → SECURE → DOCUMENT**. Each phase has a verification checklist before advancing to the next.

### Phase 1: CONFIGURE

Set up the project foundation before any endpoints are created.

- [ ] Create or verify `.csproj` with required packages (see `references/endpoint-patterns.md`)
- [ ] Configure `Program.cs` with service registrations: OpenAPI, versioning, FreeMediator, FluentValidation, DbContext
- [ ] Set up authentication and authorization pipeline
- [ ] Configure API versioning strategy (URL recommended)
- [ ] Register rate limiting policies
- [ ] Configure CORS for target environments

### Phase 2: SCAFFOLD

Create endpoint groups, request/response models, and validators.

- [ ] Create endpoint group static class with extension method pattern
- [ ] Define all CRUD operations with typed results
- [ ] Create request records for each mutating operation
- [ ] Create response DTOs for each query operation
- [ ] Implement FluentValidation validators for all request models
- [ ] Wire endpoint group into `Program.cs` via `api.Map{Resource}Endpoints()`

### Phase 3: SECURE

Apply authorization, rate limiting, and CORS to all endpoints.

- [ ] Apply `.RequireAuthorization()` to endpoint groups
- [ ] Define and apply specific policies for sensitive operations
- [ ] Apply rate limiting to public-facing or high-traffic endpoints
- [ ] Verify CORS is configured for all consuming origins
- [ ] Add health check endpoints with anonymous access
- [ ] Verify authentication middleware is in the pipeline

### Phase 4: DOCUMENT

Ensure every endpoint is fully documented via OpenAPI metadata.

- [ ] Verify every endpoint has `.WithName()` and `.WithSummary()`
- [ ] Verify every endpoint declares all `.Produces<T>()` responses
- [ ] Add `.WithDescription()` for complex endpoints
- [ ] Test Swagger UI renders correctly for all versions
- [ ] Verify versioned Swagger docs are accessible
- [ ] Confirm request/response schemas appear in OpenAPI spec

**Load on demand — `references/operating-guide.md`:** Domain Principles, Knowledge Base Lookups (run them before the first phase), AI Discipline Rules, Anti-Patterns, Error Recovery.

## State Block Format

```
<api-scaffold-state>
mode: SCAFFOLD
project_name: MyApp.Api
dotnet_version: net10.0
endpoints_created: [UsersEndpoints]
versioning_strategy: url
auth_configured: true
openapi_configured: true
last_action: Scaffolded UsersEndpoints with full CRUD
next_action: Create OrdersEndpoints group
</api-scaffold-state>
```

## Output Templates

```markdown
## API Project: [Name] | .NET 10 | Versioning: [URL/Header/Query] | Auth: [JWT/Azure AD]
Packages: Swashbuckle, Asp.Versioning.Http, FluentValidation, FreeMediator

## Endpoint Group: [Resource]
Base Path: /api/v{version}/[resource] | Auth: Required | Rate Limited: [Yes/No]
| Method | Path | Name | Request Type | Response Type | Auth Override |
| GET / | GET /{id} | POST / | PUT /{id} | DELETE /{id} |
Error responses: 400 Validation | 401 Auth | 403 Forbidden | 404 Not Found | 500 Server Error
```

Full templates (Project Setup Checklist with packages, Endpoint Group Report with request/response schemas, Validation Report, API Documentation Summary): `references/endpoint-patterns.md`

## Integration with Other Skills

| Skill | Integration Point | When to Use |
|-------|-------------------|-------------|
| **dotnet-vertical-slice** | Feature architecture for handlers behind endpoints | Scaffold CQRS handlers, commands, queries, and validators that endpoint groups delegate to |
| **dotnet-architecture-checklist** | Review scaffolded API projects | Run after scaffolding to verify architectural best practices |
| **test-scaffold** | Generate API integration tests | Create test classes exercising endpoints via `WebApplicationFactory<Program>` |
| **dotnet-security-review** | Security audit of API configuration | Verify JWT configuration, authorization policies, CORS settings, and rate limiting |
| **ef-migration-manager** | Database setup for API data access | Use when endpoints need new entities or schema changes |

References: `references/endpoint-patterns.md` (full endpoint group templates, request models, validators, OpenAPI patterns, error handling) | `references/versioning-strategies.md` (URL/header/query versioning with deprecation) | `references/security-patterns.md` (authorization, rate limiting, CORS, health checks, JWT setup)
