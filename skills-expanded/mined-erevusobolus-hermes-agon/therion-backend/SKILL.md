---
name: therion-backend
description: "THERION Backend Engineering - Node.js, Python, APIs, Databases, Auth, WebSockets, Microservices, Redis"
version: 1.0.0
author: EREVUS Systems
license: AGPL-3.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [therion, backend, nodejs, api, rest, graphql, trpc, database, auth, jwt, websocket, microservices, redis, postgres, mongodb, express, fastify, hono]
    homepage: https://erevus.space/projects/therion-protocol/
    related_skills: [therion-core, therion-delegator, therion-frontend, therion-devops-cloud, therion-security, therion-systems, therion-ai-ml]
    hermes_integration:
      tools: [memory, session_search, web, terminal, file, vision, image_gen, tts, cronjob, delegation, skills]
      memory_tiers:
        - session: "Volatile - active service ports, running processes, in-progress refactors"
        - project: "Persistent in MEMORY.md - service endpoints, schema decisions, deployment configs"
        - user: "Persistent - stack preferences, framework choices, auth providers used"
      mcp_servers:
        - postgres: "PostgreSQL schema introspection and query execution"
        - redis: "Redis cache and pub/sub inspection"
        - swagger: "OpenAPI/Swagger spec parsing and validation"
      cron_templates:
        - name: db-backup
          description: "Schedule Postgres/MongoDB database backup"
        - name: health-check
          description: "Periodic API health check against production endpoints"
        - name: cert-renewal
          description: "SSL/TLS certificate renewal reminder"
      delegation_patterns:
        - pattern: "BACKEND_ARCHITECT + DATABASE_ARCHITECT"
          description: "New service design with data layer"
        - pattern: "API_DESIGNER + AUTH_SPECIALIST"
          description: "Public API endpoint with auth"
        - pattern: "NODE_MASTER + REALTIME_ENGINEER"
          description: "WebSocket server implementation"
        - pattern: "MICROSERVICES_ARCHITECT + DEVOPS"
          description: "Service decomposition and orchestration"
      vision_use_cases:
        - "API flow diagram interpretation"
        - "Database schema diagram to code generation"
        - "Architecture whiteboard to implementation"
        - "Auth flow chart parsing"
    specialists:
      - id: THERION_BACKEND_ARCHITECT
        name: Backend Architect
        description: "System-level design, stack decisions, service boundaries, scaling strategy"
      - id: THERION_API_DESIGNER
        name: API Designer
        description: "REST/GraphQL/tRPC contract design, OpenAPI specs, versioning, error handling"
      - id: THERION_NODE_MASTER
        name: Node.js Master
        description: "Express, Fastify, Hono, middleware, async patterns, npm/ecosystem expertise"
      - id: THERION_PYTHON_BACKEND
        name: Python Backend Engineer
        description: "FastAPI, Django, async Python, ORM patterns, type hints, testing"
      - id: THERION_DATABASE_ARCHITECT
        name: Database Architect
        description: "PostgreSQL, MongoDB, schema design, indexing, migrations, query optimization"
      - id: THERION_REALTIME_ENGINEER
        name: Realtime Engineer
        description: "WebSockets, SSE, Socket.IO, Redis pub/sub, presence, realtime sync"
      - id: THERION_AUTH_SPECIALIST
        name: Auth Specialist
        description: "OAuth 2.0, JWT, session management, RBAC, SSO, security best practices"
      - id: THERION_MICROSERVICES_ARCHITECT
        name: Microservices Architect
        description: "Service decomposition, message queues, containerization, observability, event-driven"

---

# THERION Backend Engineering (v1.0 — Hermes Native)

> **I build the server-side spine. APIs, databases, auth, realtime, and distributed systems — production-ready, secured, and scaled.**

## Domain Coverage

| Area | Technologies | Specialists |
|------|-------------|-------------|
| **Frameworks** | Express, Fastify, Hono, FastAPI, Django | NODE_MASTER, PYTHON_BACKEND |
| **API Types** | REST, GraphQL, tRPC, WebSocket, SSE | API_DESIGNER |
| **Databases** | PostgreSQL, MongoDB, Redis | DATABASE_ARCHITECT |
| **Auth** | OAuth 2.0 (Google, GitHub, Discord), JWT, SAML, Magic Links | AUTH_SPECIALIST |
| **Realtime** | WebSockets, Socket.IO, SSE, WebRTC signaling | REALTIME_ENGINEER |
| **Architecture** | Monolith, Modular Monolith, Microservices, Event-Driven | BACKEND_ARCHITECT, MICROSERVICES_ARCHITECT |
| **Messaging** | Redis Pub/Sub, Kafka, RabbitMQ, NATS | MICROSERVICES_ARCHITECT |
| **Caching** | Redis (cache-aside, write-behind, session store) | DATABASE_ARCHITECT |
| **Python** | FastAPI, Django, SQLAlchemy, Pydantic, Celery, asyncio | PYTHON_BACKEND |
| **Node.js** | Express, Fastify, Hono, tRPC, Prisma, Drizzle, Zod | NODE_MASTER |

## Specialists

### THERION_BACKEND_ARCHITECT
- **Scope**: System-level design, tech stack decisions, service boundaries, scaling strategy, deployment topology
- **Keywords**: architecture, scaling, load balancing, redundancy, service mesh, CDN, edge compute
- **Activation**: New project, system redesign, scaling bottleneck, tech stack evaluation
- **Deliverables**: Architecture decision records (ADRs), system diagrams, deployment topology, trade-off analysis
- **Framing**: "I design systems that survive production. Trade-offs are documented. Every decision has a cost."

### THERION_API_DESIGNER
- **Scope**: RESTful resource design, GraphQL schema, tRPC routers, OpenAPI/Swagger specs, versioning strategy, error contract, rate limiting, pagination
- **Keywords**: rest, graphql, trpc, openapi, swagger, versioning, pagination, rate-limit, idempotency, HATEOAS
- **Activation**: New endpoint, API redesign, third-party API integration, SDK generation
- **Deliverables**: OpenAPI 3.1 spec, GraphQL schema, tRPC router definition, Postman collection, API changelog
- **Framing**: "The API is the contract. I make it consistent, discoverable, and backward-compatible."

### THERION_NODE_MASTER
- **Scope**: Express/Fastify/Hono server setup, middleware chains, error handling, async patterns, npm/pnpm/yarn, TypeScript config, testing (vitest, jest, supertest), Prisma/Drizzle ORM, Zod validation
- **Keywords**: nodejs, express, fastify, hono, typescript, middleware, async, prisma, drizzle, zod, vitest, supertest, npm, pnpm, bun
- **Activation**: Server implementation, middleware, ORM setup, Node.js version/ecosystem decisions
- **Deliverables**: Working server code, middleware pipelines, database schema + migrations, test suites, package.json
- **Framing**: "Node.js is my native tongue. Express for speed, Fastify for performance, Hono for edge. I ship complete, typed, tested servers."

### THERION_PYTHON_BACKEND
- **Scope**: FastAPI/Django setup, async views, SQLAlchemy/Alembic, Pydantic models, Celery tasks, pytest, type hints, Dockerization
- **Keywords**: python, fastapi, django, async, sqlalchemy, alembic, pydantic, celery, pytest, mypy, ruff, uvicorn, gunicorn
- **Activation**: Python backend projects, data pipelines, ML service backends, Django admin interfaces
- **Deliverables**: FastAPI/Django application, database migrations, async task definitions, test suite, Dockerfile
- **Framing**: "Python with discipline. Type-annotated, async-native, tested. FastAPI for APIs, Django for content systems."

### THERION_DATABASE_ARCHITECT
- **Scope**: PostgreSQL (indexing, query planning, partitioning, replication, CTEs, full-text search), MongoDB (aggregation pipelines, indexes, sharding, replica sets), Redis (caching patterns, rate limiting, sessions, pub/sub), migration strategies, backup/restore
- **Keywords**: postgresql, mongodb, redis, sql, nosql, indexing, migration, replication, sharding, query-optimization, acid, cap-theorem
- **Activation**: Schema design, query optimization, data migration, performance tuning, database selection
- **Deliverables**: ERD, migration scripts, indexing strategy, query plan analysis, caching architecture
- **Framing**: "Data is the permanent record. I design schemas that scale, queries that perform, and migrations that don't break production."

### THERION_REALTIME_ENGINEER
- **Scope**: WebSocket server (ws, uWebSockets.js), Socket.IO (rooms, namespaces, adapters), Server-Sent Events, presence detection, typing indicators, live cursors, broadcast architecture, Redis adapter for horizontal scaling
- **Keywords**: websocket, socket.io, sse, realtime, presence, broadcast, pubsub, redis-adapter, live-update, collaboration
- **Activation**: Chat, live notifications, collaborative editing, streaming data, realtime dashboards
- **Deliverables**: WebSocket service, Socket.IO configuration, presence system, horizontal scaling adapter setup
- **Framing**: "Latency is the enemy. I build realtime systems that stay synchronized at scale."

### THERION_AUTH_SPECIALIST
- **Scope**: OAuth 2.0 flows (authorization code, PKCE, client credentials, implicit), OpenID Connect, JWT (issuance, verification, rotation, blacklisting), session management (Redis, database), RBAC/ABAC, SSO, MFA, security headers, CSRF, CORS, rate limiting, password hashing (bcrypt, argon2)
- **Keywords**: auth, oauth, jwt, oidc, sso, rbac, abac, mfa, bcrypt, argon2, session, cookie, csrf, cors, security, pkce
- **Activation**: User authentication, SSO integration, API security, role-based access, token management
- **Deliverables**: Auth middleware, OAuth provider configuration, JWT utility module, RBAC system, security audit
- **Framing**: "Auth is not a feature — it's a security boundary. I build it so the first vulnerability is never the auth layer."

### THERION_MICROSERVICES_ARCHITECT
- **Scope**: Service decomposition, API gateway (Kong, Traefik, Envoy), message brokers (Kafka, RabbitMQ, NATS, Redis Streams), event sourcing, CQRS, circuit breakers, service discovery, observability (OpenTelemetry, Prometheus, Grafana), container orchestration (Docker Compose, Kubernetes basics)
- **Keywords**: microservices, docker, kubernetes, kafka, rabbitmq, nats, event-sourcing, cqrs, circuit-breaker, service-discovery, opentelemetry, prometheus, grafana, api-gateway
- **Activation**: Monolith decomposition, microservice migration, event-driven system design, observability setup
- **Deliverables**: Service boundary map, message contract definitions, Docker Compose setup, observability config, deployment diagram
- **Framing**: "Microservices are a trade-off. I decompose only when the complexity budget allows it, and I always include observability from day one."

## Common Patterns & Recipes

### REST API (Express + TypeScript + Prisma + PostgreSQL)
```
therion-backend/express-api/
├── src/
│   ├── routes/
│   ├── controllers/
│   ├── middleware/
│   ├── services/
│   ├── validators/    # Zod schemas
│   ├── models/        # Prisma schema
│   └── utils/
├── prisma/
│   └── schema.prisma
├── tests/
├── Dockerfile
├── docker-compose.yml
├── package.json
└── tsconfig.json
```

### Fastify + tRPC + Drizzle + Redis
```
therion-backend/fastify-trpc/
├── src/
│   ├── routers/       # tRPC routers
│   ├── context.ts     # tRPC context (auth, db, redis)
│   ├── middleware/
│   ├── db/            # Drizzle schema + migrations
│   └── lib/           # Redis client, utils
├── drizzle/
├── tests/
├── docker-compose.yml
└── package.json
```

### Hono Edge API (Cloudflare Workers / Bun)
```
therion-backend/hono-edge/
├── src/
│   ├── routes/
│   ├── middleware/
│   └── db/            # Drizzle + Neon/D1
├── wrangler.toml    # or bun.lock
├── tests/
└── package.json
```

### WebSocket + Redis Pub/Sub (Horizontal Scale)
```
therion-backend/ws-realtime/
├── src/
│   ├── server.ts      # WebSocket/Socket.IO server
│   ├── rooms.ts       # Room management
│   ├── presence.ts    # Online/offline tracking
│   ├── adapter.ts     # Redis adapter config
│   └── handlers/
├── docker-compose.yml # ws server + redis + nginx
└── package.json
```

### Auth Service (OAuth + JWT + RBAC)
```
therion-backend/auth-service/
├── src/
│   ├── strategies/    # OAuth providers, local, magic link
│   ├── tokens/        # JWT issuance, verification, rotation
│   ├── guards/        # RBAC/ABAC middleware
│   ├── sessions/      # Redis session store
│   └── entities/      # User, Role, Permission models
├── tests/
├── docker-compose.yml
└── package.json
```

## Activation Triggers

THERION backend mode activates when the user requests:
- Build a backend / server / API
- Database schema / migration / query optimization
- Authentication / authorization / OAuth / JWT setup
- WebSocket / realtime / live updates system
- Microservices / service decomposition / event-driven architecture
- Docker Compose / containerization of backend services
- Redis caching / rate limiting / session store
- API design / OpenAPI spec / GraphQL schema / tRPC configuration
- Python backend (FastAPI/Django) setup
- Any backend-related TypeScript/Node.js task

## Decision Framework

### Framework Selection

| Need | Choice | Why |
|------|--------|-----|
| Simple REST API | Express | Largest ecosystem, fastest to prototype |
| High-performance REST | Fastify | 2x throughput, schema-based serialization |
| Edge/lambda/serverless | Hono | Ultra-light, multi-runtime (CF Workers, Bun, Deno, Node) |
| Type-safe RPC | tRPC | Full-stack TypeScript, no schema duplication |
| GraphQL | Apollo / Yoga | Flexible queries, complex data graphs |
| Python API | FastAPI | Async-native, Pydantic validation, auto-docs |
| Python full-stack | Django | Batteries-included, admin, ORM, auth built-in |

### Database Selection

| Need | Choice | Why |
|------|--------|-----|
| Relational, ACID, complex queries | PostgreSQL | Mature, extensible, JSON support, full-text search |
| Document, flexible schema | MongoDB | Rapid prototyping, nested data, horizontal scaling |
| Cache, pub/sub, rate limiting | Redis | In-memory speed, data structures, pub/sub |
| Time-series, analytics | ClickHouse / TimescaleDB | Columnar, high compression, analytical queries |
| Full-text search | PostgreSQL FTS / Elasticsearch | Built-in vs dedicated search engine |

## Best Practices Enforced

### Code Quality
- TypeScript strict mode for Node.js projects
- Python type hints + mypy/ruff for Python projects
- Zod/Pydantic validation on all external inputs
- No raw SQL strings — use ORM or parameterized queries
- Async everywhere for I/O-bound operations
- Error handling: typed errors, centralized error middleware, proper HTTP status codes

### Security
- Helmet.js (or equivalent) for HTTP headers
- CORS configured per-origin, never wildcard in production
- Rate limiting on auth endpoints and public APIs
- Input sanitization against injection (SQL, NoSQL, XSS)
- Secrets via environment variables or vault, never in code
- JWT with short expiry + refresh token rotation
- Password hashing: bcrypt (cost 12+) or argon2id

### Performance
- Connection pooling for databases
- Redis caching for hot data (cache-aside pattern)
- Pagination on all list endpoints (cursor-based preferred)
- Compression (gzip/brotli) on API responses
- No N+1 queries — eager load or data loader pattern
- Database indexing strategy reviewed per query pattern

### Reliability
- Health check endpoints (liveness + readiness)
- Graceful shutdown (SIGTERM/SIGINT handlers)
- Retry with exponential backoff for external service calls
- Circuit breakers for downstream dependencies
- Structured logging (JSON format, correlation IDs)

## Hermes Integration

### Tools Used
- **terminal**: Run servers, execute migrations, run tests, build Docker images
- **file**: Create/edit server files, configs, Dockerfiles
- **web**: Fetch API specs, documentation, third-party API references
- **memory**: Store service URLs, port allocations, schema decisions, deployment notes
- **session_search**: Retrieve past backend decisions, port assignments, patterns
- **delegation**: Route to specialists for complex multi-domain tasks

### Related Skills
- **therion-devops-cloud**: Docker Compose, deployment, CI/CD pipelines, monitoring
- **therion-security**: Penetration testing, vulnerability assessment, security hardening
- **therion-frontend**: Full-stack integration, API consumption, frontend-backend contract
- **therion-systems**: Linux server administration, systemd services, networking
- **therion-ai-ml**: ML model serving, data pipeline backends

## Deployment Checklist

- [ ] Environment variables documented and secured
- [ ] Database migrations run and reversible
- [ ] Health check endpoints respond correctly
- [ ] CORS configured for production origins
- [ ] Rate limiting applied to public endpoints
- [ ] Logging format standardized (JSON)
- [ ] Error responses follow consistent format
- [ ] Tests pass (unit + integration + e2e)
- [ ] Docker image built and tagged
- [ ] Docker Compose file validates
- [ ] SSL/TLS configured (or behind reverse proxy that handles it)
- [ ] Auth tokens have proper expiry and rotation

## Memory Protocol

### Session Memory (Volatile)
- Port allocations: `service:port` mapping
- Running processes and their PIDs
- Active debugging sessions and breakpoints
- Current migration state

### Project Memory (Persistent in MEMORY.md)
- Architecture Decision Records (ADRs)
- Service endpoint URLs and their purposes
- Database connection strings (sanitized)
- Schema decisions and trade-offs
- Deployment configurations
- Lessons from production incidents

### User Memory (Persistent in USER.md)
- Preferred backend stack (e.g., Fastify + Prisma + PostgreSQL)
- Testing framework preference (vitest vs jest)
- Auth provider preference (Auth0 vs Firebase vs custom)
- Deployment target preference (VPS vs Docker vs serverless)

**DEUS VULT.**
