---
name: backend-implementation
description: "Backend implementation skill. Use when implementing any server-side feature, API route, service, middleware, database model, or migration. Covers language selection (Node.js/TypeScript, Python, Go, Java, Rust), framework choice (Express, Fastify, NestJS, FastAPI, Gin, Spring Boot), ORM/database, auth patterns, and API design. Guides the user to choose or confirms the existing stack before writing any code. Trigger phrases: 'backend', 'rota', 'route', 'API', 'endpoint', 'middleware', 'serviço', 'service', 'banco de dados', 'database', 'migration', 'model', 'schema', 'autenticação', 'auth', 'server', 'servidor'."
argument-hint: "Descreva o que precisa ser implementado no backend (ex: 'rota POST /transactions', 'middleware de autenticação', 'migração para adicionar campo')"
---

# Backend Implementation Skill

This skill ensures the right backend stack and patterns are established before writing any server-side code. It either confirms the existing project stack or guides a new project through language, framework, and tooling decisions.

## When to Use

Load this skill before implementing:
- New API routes or endpoints
- Services, controllers, or business logic
- Database models, migrations, or seeds
- Authentication and authorization middleware
- Background jobs or scheduled tasks
- When starting a backend project from scratch

---

## Procedure

### Step 1 — Detect the Existing Stack

Before asking anything, inspect the workspace:
- Check for `server/`, `backend/`, `api/`, or `src/` folders at the root.
- Read `package.json` (Node.js), `requirements.txt` / `pyproject.toml` (Python), `go.mod` (Go), `pom.xml` / `build.gradle` (Java).
- Identify the framework: Express, Fastify, NestJS, FastAPI, Flask, Django, Gin, Fiber, Spring Boot.
- Identify the ORM/database layer: Prisma, TypeORM, Drizzle, SQLAlchemy, GORM, Hibernate.
- Identify auth strategy: JWT, session, OAuth, API keys.
- Look at one existing route/controller file to understand the code structure and patterns in use.

**If a stack is already established:**
→ Skip to Step 4. Do NOT re-evaluate language or framework choice.
→ Confirm briefly: "Detected stack: [language] + [framework] + [ORM]. Following existing conventions."

**If no stack is established (new project):**
→ Continue to Step 2.

---

### Step 2 — Language Selection (New Projects Only)

Ask the user about project requirements using the decision factors below, then recommend the **top 2 options** from [languages.md](./references/languages.md) with clear rationale.

**Decision factors to ask:**
1. **Team familiarity** — What languages does the team already know?
2. **Performance requirements** — Is this a high-throughput API (10k+ req/s) or a standard CRUD API?
3. **Ecosystem needs** — Need ML/AI libraries? Payment SDKs? Specific integrations?
4. **Development speed priority** — Prototype fast vs. production-grade from day one?
5. **Deployment target** — Serverless (Lambda, Vercel), container (Railway, Render, Fly.io), or bare metal?
6. **Frontend stack** — Sharing code (types, validators) with the frontend? (favors Node.js/TypeScript)

Present the top 2 matches in this format:

```
## Option A: [Language + Runtime]
**Best for:** [reason based on answers]
**Tradeoffs:** [what they give up]
**Full stack example:** [language] + [framework] + [ORM] + [database]

## Option B: [Language + Runtime]
...
```

Ask the user to confirm one before continuing.

---

### Step 3 — Framework & Tooling Decisions (New Projects Only)

After the language is chosen, guide remaining decisions. Load [frameworks.md](./references/frameworks.md) for details.

For each category, present **2 options max** with the key tradeoff:

| Category | Options |
|---|---|
| **Framework** | Express vs Fastify vs NestJS (Node) / FastAPI vs Django (Python) / Gin vs Fiber (Go) |
| **ORM / Query builder** | Prisma vs Drizzle vs TypeORM (Node) / SQLAlchemy vs Tortoise (Python) / GORM vs sqlx (Go) |
| **Database** | PostgreSQL (default) vs MySQL vs SQLite vs MongoDB |
| **Auth strategy** | JWT (stateless) vs Sessions (stateful) vs OAuth |
| **Validation** | Zod (Node) vs Pydantic (Python) vs go-validator (Go) |
| **Testing** | Vitest + Supertest (Node) vs Pytest (Python) vs testing package (Go) |

Confirm all choices before continuing.

---

### Step 4 — Code Conventions

Before writing any code, extract and follow the project's conventions:

**File structure:**
- Where do routes live? (`routes/`, `controllers/`, `handlers/`?)
- Is there a service layer separate from routes? (`services/`)
- Where are types/interfaces defined? (`types.ts`, co-located, `lib/types/`?)
- Are middleware functions in their own folder? (`middleware/`)

**Route conventions:**
- HTTP verb + resource naming: `GET /transactions`, `POST /transactions`, `PATCH /transactions/:id`
- Error response shape: `{ error: string }` or `{ message: string, code: string }`?
- Success response shape: raw object, `{ data: T }`, or `{ data: T, meta: PageMeta }`?
- Auth: via `Authorization: Bearer <token>` header or cookie?

**Service layer pattern:**
- Are DB queries in the route handler or in a dedicated service?
- Do services throw errors or return result objects?

**TypeScript conventions (if applicable):**
- `interface` vs `type` for request/response shapes
- Are Zod schemas the source of truth for types?

If any can't be inferred, use the defaults from [patterns.md](./references/patterns.md).

**Load [patterns.md](./references/patterns.md) and apply:**
- Route handler pattern (validate → service call → respond)
- Service layer pattern (business logic, row-level auth scoping)
- Global error handler (throw with `.status`, catch in `next(err)`)
- Auth middleware pattern
- Prisma singleton + safe migration rules

**If the task involves schema changes**, load [database.md](./references/database.md) to check:
- Migration safety (nullable first, backfill, then NOT NULL)
- Index requirements for new query patterns
- Relation `onDelete` strategy

---

### Step 5 — Security Checklist (Run Before Every Implementation)

Before writing any route or service, verify OWASP Top 10 compliance:

- [ ] **Input validation** — All user input validated with Zod/Pydantic/validator before use
- [ ] **Auth on protected routes** — Middleware applied, not inline
- [ ] **Authorization** — User can only access their own resources (row-level check, not just auth)
- [ ] **SQL injection** — Using ORM parameterized queries, never raw string concatenation
- [ ] **Rate limiting** — Sensitive routes (auth, password reset) have stricter limits
- [ ] **Sensitive data** — Passwords hashed (bcrypt), tokens not logged, secrets in env vars
- [ ] **CORS** — Configured explicitly, not `origin: *` in production
- [ ] **Error messages** — Do not expose stack traces or internal details to clients

Flag any checklist item that the task needs to address and handle it explicitly in the implementation.

---

### Step 6 — Implementation Checklist

Before submitting:

- [ ] Route is registered in the router/app entry point
- [ ] Request body/params/query validated with schema
- [ ] Response returns the correct HTTP status code (201 for create, 204 for delete, etc.)
- [ ] Error cases have explicit handling and return meaningful messages
- [ ] Auth/authorization middleware applied if route is protected
- [ ] Database queries use the ORM — no raw SQL strings unless necessary
- [ ] No secrets or credentials hardcoded — use `process.env`
- [ ] Types are correct — no `any`, request/response shapes are typed
- [ ] Migration created if schema changed
- [ ] New migration does not break existing data (safe to run on production)

---

## Constraints

- DO NOT introduce a new language, framework, or ORM if the project already has one.
- DO NOT write raw SQL unless the ORM cannot express the query.
- DO NOT skip the security checklist — validate input on every route.
- ALWAYS follow the existing route/service structure found in the codebase.
- ALWAYS use environment variables for secrets, URLs, and credentials.
- If the task requires a library not in `package.json` / `requirements.txt` / `go.mod`, flag it and ask the user before adding it.
- If a database schema change is needed, always create a migration — never mutate the schema directly.
