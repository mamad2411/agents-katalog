---
name: system-design
description: "System design and code review skill for fullstack Go+React apps. Use when designing architecture or reviewing code against design specifications."
---

# System Design

## Purpose

This skill provides the knowledge base for designing and reviewing fullstack applications built with Go (backend) and React (frontend) with PostgreSQL as the data layer. It covers two operating modes:

- **Design Mode (Phase 1):** Produce a complete system design document from a PRD -- API contracts, database schema, component architecture, and Go project structure.
- **Review Mode (Phase 4):** Verify implemented code conforms to the design document, flagging deviations, anti-patterns, and missing pieces.

## Key Patterns

### 1. REST API Design (OpenAPI/Swagger)

**Endpoint Naming Conventions:**
- Use plural nouns for resource collections: `/api/v1/users`, `/api/v1/projects`
- Use path parameters for specific resources: `/api/v1/users/{id}`
- Nest related resources max 2 levels deep: `/api/v1/projects/{id}/tasks`
- Use query parameters for filtering, sorting, pagination: `?status=active&sort=created_at&order=desc&page=1&limit=20`
- API versioning in path prefix: `/api/v1/`, `/api/v2/`
- Use kebab-case for multi-word paths: `/api/v1/user-profiles`

**HTTP Methods:**
| Method | Purpose | Idempotent | Request Body | Success Code |
|--------|---------|------------|--------------|--------------|
| GET | Retrieve resource(s) | Yes | No | 200 |
| POST | Create resource | No | Yes | 201 |
| PUT | Full replace | Yes | Yes | 200 |
| PATCH | Partial update | Yes | Yes | 200 |
| DELETE | Remove resource | Yes | No | 204 |

**Standard Status Codes:**
- `200 OK` -- Successful GET, PUT, PATCH
- `201 Created` -- Successful POST (include `Location` header)
- `204 No Content` -- Successful DELETE
- `400 Bad Request` -- Validation errors, malformed input
- `401 Unauthorized` -- Missing or invalid authentication
- `403 Forbidden` -- Authenticated but not authorized
- `404 Not Found` -- Resource does not exist
- `409 Conflict` -- Duplicate resource, version conflict
- `422 Unprocessable Entity` -- Semantically invalid input
- `500 Internal Server Error` -- Unexpected server failure

**Standard Error Response Schema:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      {
        "field": "email",
        "message": "must be a valid email address"
      }
    ]
  }
}
```

**Pagination Response Envelope:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 142,
    "total_pages": 8
  }
}
```

### 2. Database Schema Design (PostgreSQL)

**Table Conventions:**
- Table names: plural, snake_case (`users`, `project_tasks`)
- Column names: snake_case (`created_at`, `user_id`)
- Every table MUST have: `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`, `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`, `updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`
- Soft delete via `deleted_at TIMESTAMPTZ` column (nullable, NULL = active)
- Foreign keys always have explicit `ON DELETE` clause (CASCADE, SET NULL, or RESTRICT)
- Create indexes on: foreign keys, columns used in WHERE clauses, columns used in ORDER BY, unique constraints

**Migration Conventions:**
- Sequential numbered files: `001_create_users.up.sql`, `001_create_users.down.sql`
- Every UP migration has a corresponding DOWN migration
- DOWN migrations must be reversible (drop what UP created)
- Use `golang-migrate/migrate` or `pressly/goose` format
- Never modify existing migrations in production -- create new ones

**Common Patterns:**
```sql
-- Audit columns trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to every table
CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON {table_name}
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- Soft delete index (only index active rows)
CREATE INDEX idx_{table}_active ON {table} (id) WHERE deleted_at IS NULL;
```

**Relationship Patterns:**
- One-to-many: FK on the "many" side (`user_id UUID REFERENCES users(id)`)
- Many-to-many: Junction table with composite PK (`user_roles` with `user_id` + `role_id`)
- One-to-one: FK with UNIQUE constraint
- Self-referential: FK referencing same table (`parent_id UUID REFERENCES categories(id)`)

### 3. React Component Architecture

**Component Hierarchy:**
```
App
  Layout
    Header (auth state, navigation)
    Sidebar (navigation menu)
    Main
      Page (route-level, fetches data)
        Container (state logic, data transformation)
          Presentational (UI rendering, props only)
```

**Component Classification:**
- **Page Components** (`pages/`): Route entry points. Own data fetching via hooks. Pass data down.
- **Container Components** (`containers/`): Business logic, state management, API calls. Minimal JSX.
- **Presentational Components** (`components/`): Pure rendering. Props in, JSX out. No side effects.
- **Layout Components** (`layouts/`): Page structure (header, sidebar, footer). Render `children`.

**State Management Strategy:**
- **Server state:** React Query / TanStack Query (caching, refetching, optimistic updates)
- **Local UI state:** `useState` / `useReducer` (form inputs, toggles, modals)
- **Global app state:** React Context (auth, theme, feature flags) -- NOT for server data
- **URL state:** React Router search params (filters, pagination, sort)

**Props Flow Rules:**
- Props flow DOWN only. Never pass setters more than 2 levels.
- If prop drilling exceeds 2 levels, extract to Context or compose with render props.
- Define explicit TypeScript interfaces for all props.
- Use `children` for composition over configuration.

**File Naming:**
- Components: PascalCase (`UserProfile.tsx`, `TaskList.tsx`)
- Hooks: camelCase with `use` prefix (`useAuth.ts`, `useTasks.ts`)
- Utils: camelCase (`formatDate.ts`, `validators.ts`)
- Types: PascalCase in dedicated files (`types.ts` or `User.types.ts`)

### 4. Go Project Structure

**Standard Layout (handler -> service -> repository):**
```
cmd/
  server/
    main.go                 # Entry point: config, DI, server startup
internal/
  config/
    config.go               # Environment/config loading
  handler/
    user_handler.go          # HTTP handlers (parse request, call service, write response)
    user_handler_test.go
    middleware.go            # Auth, logging, CORS, recovery middleware
  service/
    user_service.go          # Business logic (validation, orchestration, rules)
    user_service_test.go
  repository/
    user_repository.go       # Database access (queries, transactions)
    user_repository_test.go
  model/
    user.go                  # Domain models (structs, enums, constants)
    errors.go                # Domain error types
  dto/
    user_dto.go              # Request/response DTOs (separate from domain models)
    validation.go            # DTO validation rules
  router/
    router.go                # Route definitions, middleware chaining
pkg/
  response/
    response.go              # Standard JSON response helpers
  pagination/
    pagination.go            # Pagination parsing and response
migrations/
  001_create_users.up.sql
  001_create_users.down.sql
api/
  openapi.yaml               # OpenAPI 3.0 specification
```

**Layer Responsibilities:**

| Layer | Does | Does NOT |
|-------|------|----------|
| Handler | Parse HTTP request, validate input, call service, write HTTP response | Contain business logic, access DB directly |
| Service | Business rules, validation, orchestrate repositories, error wrapping | Know about HTTP, parse requests, write responses |
| Repository | SQL queries, scan results into models, manage transactions | Contain business logic, know about HTTP |
| Model | Define domain types, constants, domain errors | Import from handler/service/repository |
| DTO | Define API request/response shapes, input validation | Contain business logic |

**Dependency Direction:**
```
handler -> service -> repository
   |          |           |
   v          v           v
  dto       model       model
```
Handlers depend on services. Services depend on repositories. All depend on models. Never reverse this flow.

**Interface Pattern (dependency injection):**
```go
// Define interface in the CONSUMER package (service defines what it needs from repo)
type UserRepository interface {
    GetByID(ctx context.Context, id uuid.UUID) (*model.User, error)
    Create(ctx context.Context, user *model.User) error
    Update(ctx context.Context, user *model.User) error
    Delete(ctx context.Context, id uuid.UUID) error
    List(ctx context.Context, filter UserFilter) ([]model.User, int, error)
}

// Implement in the PROVIDER package
type userRepository struct {
    db *sql.DB
}

func NewUserRepository(db *sql.DB) UserRepository {
    return &userRepository{db: db}
}
```

**Error Handling:**
- Define domain errors in `model/errors.go`
- Services wrap repository errors with domain context
- Handlers map domain errors to HTTP status codes
- Never expose internal error details to clients
```go
// model/errors.go
var (
    ErrNotFound      = errors.New("resource not found")
    ErrAlreadyExists = errors.New("resource already exists")
    ErrForbidden     = errors.New("access denied")
)
```

### 5. API Contract Definition

**Request/Response Type Rules:**
- Every endpoint has explicitly defined request and response types
- Request types: only fields the client sends (no `id`, no `created_at`)
- Response types: what the client receives (includes `id`, timestamps)
- List endpoints return paginated envelope, not raw arrays
- Use `omitempty` on optional fields in Go structs
- Validate requests at the handler/DTO layer, not in services

**Go DTO Patterns:**
```go
// CreateUserRequest -- POST /api/v1/users
type CreateUserRequest struct {
    Email    string `json:"email" validate:"required,email"`
    Name     string `json:"name" validate:"required,min=2,max=100"`
    Password string `json:"password" validate:"required,min=8"`
}

// UserResponse -- returned by all user endpoints
type UserResponse struct {
    ID        uuid.UUID `json:"id"`
    Email     string    `json:"email"`
    Name      string    `json:"name"`
    CreatedAt time.Time `json:"created_at"`
    UpdatedAt time.Time `json:"updated_at"`
}

// ListResponse[T] -- generic paginated response
type ListResponse[T any] struct {
    Data       []T        `json:"data"`
    Pagination Pagination `json:"pagination"`
}
```

**TypeScript API Types (frontend mirror):**
```typescript
// types/api.ts
interface CreateUserRequest {
  email: string;
  name: string;
  password: string;
}

interface UserResponse {
  id: string;
  email: string;
  name: string;
  created_at: string;
  updated_at: string;
}

interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    total_pages: number;
  };
}
```

### 6. Code Review Patterns

**Conformance Checking (Design vs Implementation):**
- Every endpoint in the design doc MUST exist in the router
- Every DB table in the design doc MUST have a migration file
- Every React component in the design doc MUST exist as a file
- Request/response types MUST match the design doc field-for-field
- HTTP methods and status codes MUST match the design doc

**Anti-Pattern Detection:**

| Anti-Pattern | What to Flag | Correct Pattern |
|--------------|-------------|----------------|
| Fat handler | Business logic in handler | Move to service layer |
| Anemic service | Service just passes through to repo | Add validation/rules to service |
| Direct DB in handler | `sql.DB` used in handler | Use repository interface |
| God component | React component > 200 lines | Split into container + presentational |
| Prop drilling | Props passed > 2 levels | Use Context or composition |
| Raw SQL strings | Unparameterized queries | Use parameterized queries (`$1`, `$2`) |
| Missing error handling | Unchecked `err` returns | Always check and handle errors |
| N+1 queries | Query in a loop | Use JOINs or batch queries |
| Hardcoded config | Connection strings in code | Use environment variables |
| Missing indexes | FK columns without indexes | Add indexes on FK columns |

**Severity Levels:**
- **CRITICAL:** Security vulnerability, data loss risk, broken functionality. MUST fix before merge.
- **HIGH:** Design deviation, missing validation, incorrect status code. Should fix before merge.
- **MEDIUM:** Anti-pattern, suboptimal structure, missing index. Fix in this PR or next.
- **LOW:** Style issue, naming convention, minor improvement. Suggestion only.

## Conventions

1. **API-first design:** Define endpoints and contracts BEFORE writing code.
2. **One migration per change:** Each schema change gets its own numbered migration pair.
3. **Interface-driven Go:** Define interfaces in consumers, implement in providers.
4. **Strict layer separation:** Handlers never import repositories. Services never import `net/http`.
5. **TypeScript strict mode:** All React projects use `"strict": true` in tsconfig.
6. **Explicit error types:** No generic error strings. Define typed errors in `model/errors.go`.
7. **Context propagation:** Every Go function that does I/O takes `context.Context` as first parameter.
8. **UUID primary keys:** Always use UUIDs, never auto-increment integers, for all public-facing IDs.
9. **Timestamps are UTC:** All `TIMESTAMPTZ` values stored and transmitted in UTC.
10. **JSON field naming:** Use `snake_case` in JSON (Go tags + TypeScript interfaces must match).

## Knowledge Strategy

- **Patterns to capture:** Successful API designs, reusable SQL migration templates, component tree patterns that scaled well, Go error handling chains that worked cleanly.
- **Examples to collect:** Complete design documents that passed review, review reports that caught real issues, migration sequences that handled complex schema evolution.
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
