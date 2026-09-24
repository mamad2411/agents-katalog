---
name: project-setup
description: >
  Tech-stack selection advisor for .NET projects: recommended defaults for
  database, auth, caching, messaging, observability, and resilience, with the
  rationale behind each default. Load when choosing or reviewing a project's
  tech stack, or when the user says "tech stack", "which database", "pick a
  stack", "recommended defaults", or "what should I use for". For project
  initialization use dotnet-init, for codebase assessment use health-check,
  for upgrades and schema changes use migrate.
---

# Project Setup — Tech-Stack Advisor

This skill owns one thing: the kit's recommended tech-stack defaults and why. The workflows that consume it live elsewhere:

- **Initializing a project / generating CLAUDE.md** → `dotnet-init` (interactive flow, architecture questionnaire, CLAUDE.md generation)
- **Assessing an existing codebase** → `health-check` (the canonical 8-dimension graded assessment)
- **EF Core schema, NuGet, or .NET version migrations** → `migrate`
- **Choosing an architecture** → `architecture-advisor` (always ask before recommending)

## Core Principles

1. **Recommend a default, explain the why, let the user choose** — Every dimension has a kit default, but defaults are starting points, not mandates. State the trade-off in one line so the choice is informed.
2. **Prefer built-in .NET over third-party** — `HybridCache` over Redis-client wrappers, built-in rate limiting over packages, built-in OpenAPI over Swashbuckle. Fewer dependencies means fewer licensing surprises and upgrade breaks.
3. **License-aware picks** — MediatR (v13+), MassTransit (v9+), and FluentAssertions (v8+) went commercial. The kit defaults to MIT alternatives: Mediator, Wolverine, plain xUnit asserts.
4. **Add messaging later, not never** — Most projects don't need a message bus on day one. Default to "None (add later)" and reach for Wolverine when async workflows actually appear.

## Patterns

### Tech-Stack Dimensions and Defaults

| Dimension | Options | Default | Why |
|-----------|---------|---------|-----|
| Database | PostgreSQL, SQL Server, SQLite | PostgreSQL | Open source, best EF Core provider outside SQL Server, first-class Testcontainers support |
| Auth | JWT Bearer, OIDC (Keycloak/Auth0), None | JWT Bearer | Simplest secure default for APIs; move to OIDC when an external IdP exists |
| Caching | HybridCache, Redis, None | HybridCache | Built-in, stampede protection, L1+L2 — add Redis only as its L2 backend |
| Messaging | Wolverine (RabbitMQ), MassTransit, None | None (add later) | Premature messaging adds ops burden; Wolverine (MIT) when needed |
| Observability | Serilog + OpenTelemetry, Basic logging | Serilog + OTEL | Structured logs + traces from day one are cheap; retrofitting is not |
| Resilience | Polly v8 pipelines, Basic retry | Polly v8 | `AddStandardResilienceHandler()` is one line for production-grade defaults |
| API docs | Built-in OpenAPI + Scalar | OpenAPI + Scalar | Framework-maintained spec generation; Scalar replaces Swagger UI |
| Testing | xUnit v3 + Testcontainers | xUnit v3 + Testcontainers | Real databases in tests; in-memory providers hide real bugs |

Once dimensions are chosen, `dotnet-init` bakes them into the generated CLAUDE.md, and each choice maps to a skill to load when working in that area (`ef-core`, `authentication`, `caching`, `messaging`, `serilog`, `opentelemetry`, `resilience`, `openapi`, `scalar`, `testing`).

## Anti-patterns

### Prescribing a Stack Without Asking

```
# BAD — assuming the kit defaults apply everywhere
"You should use PostgreSQL and Wolverine."
# The team runs SQL Server enterprise-wide and has zero async workflows.

# GOOD — default + trade-off + question
"Kit default is PostgreSQL (best OSS EF provider). Any organizational
constraint — existing SQL Server licenses, DBA support — that should
override it?"
```

### Re-Running Workflows This Skill Doesn't Own

```
# BAD — improvising a health grading or init flow from this skill
"Let me grade your codebase across 5 categories..."
# That grading conflicts with the canonical one.

# GOOD — route to the owner
Init/CLAUDE.md → dotnet-init | Assessment → health-check | Upgrades → migrate
```

## Decision Guide

| Scenario | Route to |
|----------|----------|
| "Set up this project for Claude Code" | `dotnet-init` |
| "Which database/auth/caching should I use?" | This skill — table above |
| "How healthy is this codebase?" | `health-check` |
| "Upgrade to .NET 10" / "update packages" | `migrate` |
| "Which architecture fits?" | `architecture-advisor` |
| Stack chosen, ready to build | `scaffold` for the first feature |
