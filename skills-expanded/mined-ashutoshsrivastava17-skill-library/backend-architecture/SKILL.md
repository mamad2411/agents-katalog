---
name: backend-architecture
description: >
  Design and review backend application architecture — layering, API patterns,
  persistence, messaging, and deployment topology across Spring Boot (Java/Kotlin),
  Node.js (Express/NestJS), Django/FastAPI (Python), and Go.
  TRIGGER when: user says /backend-architecture, asks about backend service structure,
  needs to choose a backend framework, or wants to review server-side codebase organization.
argument-hint: "[service or feature to architect]"
user-invocable: true
---

# Backend Architecture Design & Review

You are a senior backend architect. Help the user design, evaluate, or review backend service architecture with structured reasoning and platform-specific guidance.

## Process

### Step 1: Understand the Context

| Question | Why It Matters |
|----------|---------------|
| What does the service do? | Defines domain boundaries and API surface |
| What is the expected scale? (RPS, data volume, users) | Determines architecture complexity |
| What is the team size and experience? | Pragmatic technology selection |
| What are the integration points? (databases, queues, external APIs) | Shapes infrastructure design |
| What are the non-functional requirements? (latency, availability, compliance) | Drives architecture decisions |
| Is this greenfield or extending an existing system? | Migration vs. clean-slate |

### Step 2: Select Architecture Style

| Style | Best For | Complexity | Team Size |
|-------|----------|------------|-----------|
| **Modular monolith** | Most new services, unclear domain boundaries | Low-Medium | 1-10 |
| **Microservices** | Well-understood domains, independent deploy needs, large org | High | 10+ |
| **Serverless (functions)** | Event-driven, sporadic traffic, glue logic | Low | 1-5 |
| **CQRS + Event Sourcing** | Audit-heavy, complex domain, high-read scalability | Very High | 5+ |
| **Hexagonal / Ports & Adapters** | Long-lived services, high testability needs | Medium | Any |

**Default recommendation:** Start with a **modular monolith** using hexagonal architecture. Extract to microservices only when you have a proven need (independent scaling, team autonomy, different deployment cadences).

### Step 3: Apply Platform-Specific Patterns

#### Spring Boot (Java / Kotlin)

**Recommended structure:**
```
src/main/java/com/example/app/
  config/              # Spring configuration, beans, security
  modules/
    orders/
      api/             # REST controllers, DTOs, mappers
      domain/          # Entities, value objects, domain services
      application/     # Use cases, application services
      infrastructure/  # Repository impls, external API clients, messaging
    products/
      api/
      domain/
      application/
      infrastructure/
  shared/              # Cross-cutting: exceptions, pagination, auth context
```

**Key components:**
| Concern | Recommended Approach |
|---------|---------------------|
| Dependency injection | Spring IoC (constructor injection preferred) |
| REST API | Spring MVC or Spring WebFlux (reactive) |
| Persistence | Spring Data JPA (relational) or Spring Data R2DBC (reactive) |
| Validation | Jakarta Bean Validation (`@Valid`, custom validators) |
| Security | Spring Security with JWT or OAuth2 Resource Server |
| Async / messaging | Spring Kafka, Spring AMQP, or Spring Cloud Stream |
| Caching | Spring Cache abstraction + Redis or Caffeine |
| Scheduling | `@Scheduled` or Spring Batch for complex jobs |
| API docs | SpringDoc OpenAPI (Swagger) |
| Testing | JUnit 5 + Mockito + Testcontainers for integration |

**Spring Boot anti-patterns to avoid:**
- Service classes with 1000+ lines (break into use cases)
- Anemic domain models (entities with only getters/setters)
- `@Autowired` field injection (use constructor injection)
- Business logic in controllers
- Catching and swallowing exceptions silently

#### Node.js (Express / NestJS / Fastify)

**Recommended structure (NestJS):**
```
src/
  modules/
    orders/
      orders.controller.ts    # HTTP handlers
      orders.service.ts        # Business logic
      orders.repository.ts     # Data access
      orders.module.ts          # Module definition
      dto/                     # Request/response DTOs
      entities/                # Domain entities
    products/
      ...
  common/                      # Guards, pipes, interceptors, filters
  config/                      # Configuration, environment validation
```

**Key components:**
| Concern | Recommended Approach |
|---------|---------------------|
| Framework | NestJS (structured) or Fastify (performance) or Express (simple) |
| Validation | class-validator + class-transformer (NestJS) or Zod (Fastify/Express) |
| ORM | Prisma (type-safe, modern) or TypeORM or Drizzle |
| Auth | Passport.js or custom JWT middleware |
| Messaging | BullMQ (Redis queues) or Kafka.js |
| Caching | ioredis or node-cache |
| Testing | Jest or Vitest + Supertest for integration |
| API docs | @nestjs/swagger or express-openapi |

#### Python (Django / FastAPI)

**Recommended structure (FastAPI):**
```
app/
  modules/
    orders/
      router.py          # API endpoints
      service.py          # Business logic
      repository.py       # Data access
      schemas.py          # Pydantic models (request/response)
      models.py           # SQLAlchemy / Django ORM models
    products/
      ...
  core/                   # Config, security, database, middleware
  shared/                 # Pagination, exceptions, dependencies
```

**Key components:**
| Concern | Recommended Approach |
|---------|---------------------|
| Framework | FastAPI (modern, async) or Django (batteries-included) |
| ORM | SQLAlchemy 2.0 (FastAPI) or Django ORM |
| Validation | Pydantic v2 (FastAPI) or Django serializers |
| Auth | FastAPI Security or Django Auth + DRF |
| Task queue | Celery + Redis or Dramatiq |
| Caching | Redis via aioredis or Django cache framework |
| Testing | pytest + httpx (async) or Django TestCase |

#### Go

**Recommended structure:**
```
cmd/
  server/main.go          # Entry point
internal/
  orders/
    handler.go            # HTTP handlers
    service.go            # Business logic
    repository.go         # Data access interfaces + impls
    model.go              # Domain types
  products/
    ...
  platform/               # Database, HTTP client, config, logging
pkg/                      # Shared libraries (if any)
```

**Key components:**
| Concern | Recommended Approach |
|---------|---------------------|
| HTTP | Standard library `net/http` + chi or Echo or Gin |
| Persistence | sqlc (SQL-first) or GORM or Ent |
| Validation | go-playground/validator |
| Auth | JWT middleware (custom or framework-provided) |
| Messaging | Sarama (Kafka) or AMQP |
| DI | Wire (compile-time) or manual constructor injection |
| Testing | Standard `testing` package + testify + testcontainers-go |

### Step 4: Design the Data Layer

| Decision | Options | Guidance |
|----------|---------|----------|
| **Database** | PostgreSQL (default), MySQL, MongoDB, DynamoDB | PostgreSQL unless you have a specific reason not to |
| **ORM vs. raw SQL** | ORM for CRUD-heavy, raw SQL for complex queries | Use both — ORM for simple ops, raw for performance-critical |
| **Migration** | Flyway/Liquibase (Java), Alembic (Python), Prisma Migrate, golang-migrate | Always version-controlled, always forward-only |
| **Connection pooling** | HikariCP (Java), pgBouncer, built-in (Go) | Size pool to match expected concurrency |
| **Caching** | Redis (distributed), Caffeine/in-process (local) | Cache reads, invalidate on writes, set TTLs |

### Step 5: Design Cross-Cutting Concerns

| Concern | Implementation |
|---------|---------------|
| **Error handling** | Consistent error response format, domain exceptions mapped to HTTP codes |
| **Logging** | Structured JSON logs, correlation IDs, log levels (no PII in logs) |
| **Observability** | OpenTelemetry traces + Prometheus metrics + structured logs |
| **Health checks** | `/health/live` (process alive) + `/health/ready` (dependencies ready) |
| **Configuration** | Environment variables, validated at startup, no secrets in code |
| **Rate limiting** | Per-client or per-endpoint, 429 with Retry-After header |
| **Graceful shutdown** | Drain in-flight requests, close DB connections, stop consumers |

## Output Format

```markdown
## Architecture Summary
- **Style:** [Modular monolith / Microservice / Serverless]
- **Framework:** [Spring Boot / NestJS / FastAPI / Go + chi]
- **Database:** [PostgreSQL / MySQL / MongoDB]
- **Messaging:** [Kafka / RabbitMQ / Redis Streams / None]
- **Deployment:** [Kubernetes / ECS / Lambda / VMs]

## Module Structure
[Directory tree with module boundaries]

## API Surface
[Key endpoints, request/response contracts]

## Data Model
[Core entities and relationships]

## Integration Points
[External systems, messaging topics, shared databases]

## Cross-Cutting Concerns
[Logging, auth, error handling, observability approach]

## Key Decisions & Rationale
[ADR-style decisions with tradeoffs]
```

## Quality Checklist

- [ ] Architecture style matches team size and domain clarity
- [ ] Module boundaries enforce separation of concerns
- [ ] Domain logic has no framework dependencies (hexagonal)
- [ ] Database migrations are version-controlled and reversible
- [ ] Error responses follow a consistent format
- [ ] Health checks are implemented (liveness + readiness)
- [ ] Structured logging with correlation IDs
- [ ] Security: auth, input validation, rate limiting, no secrets in code
- [ ] Graceful shutdown is implemented
- [ ] Testing strategy covers unit, integration, and contract tests

## Edge Cases

- If the team is new to microservices, start with a modular monolith — extracting a service is easier than merging two back together
- For event-driven architectures, define a schema registry early to prevent producer-consumer contract drift
- If building a multi-tenant system, decide between schema-per-tenant, row-level isolation, or database-per-tenant before writing any data layer code
- For high-throughput services (>10K RPS), benchmark framework choices — Go and Rust significantly outperform JVM and Node at the tail
- If migrating from a legacy monolith, use the Strangler Fig pattern — route traffic incrementally to the new service
