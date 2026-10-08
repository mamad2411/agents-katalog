# Project Standards — Clean Architecture (Go + React)

## Architecture Rules

This project follows **Clean Architecture** principles. All code MUST respect the dependency rule:

```
Entity (innermost) → Use Case → Interface (outermost)
```

### Layer Responsibilities

#### 1. Entity (`internal/entity/`)
- Pure domain models and business rules
- NO imports from other layers
- NO framework dependencies (no GORM tags, no JSON tags for API)
- Define interfaces that outer layers must implement

#### 2. Use Case (`internal/use_case/`)
- Application-specific business logic
- Depends ONLY on Entity layer (interfaces)
- Orchestrates entities and repository interfaces
- Each use case = one business operation
- Must NOT know about HTTP, database drivers, or frameworks

#### 3. Repository (`internal/repository/`)
- Implements data access interfaces defined in Entity/Use Case
- One directory per aggregate (e.g., `user_repository/`, `ticket_repository/`)
- Contains database-specific code (GORM models, queries)
- Maps between DB models and domain entities

#### 4. Interface (`internal/interface/`)
- HTTP handlers, middleware, routing
- Depends on Use Case layer
- Maps between HTTP request/response and use case input/output
- Framework-specific code lives here (Gin, Echo, etc.)

### Go Project Layout

```
cmd/
  api/main.go          # Application entry point (wiring & DI)
internal/
  entity/              # Domain models & interfaces
  use_case/            # Business logic
  repository/          # Data access implementations
  interface/           # HTTP handlers, routes, middleware
pkg/                   # Shared utilities (jwt, helpers)
```

- `cmd/` contains entry points — one subdirectory per binary (`api`, `worker`, `cli`)
- `internal/` is Go's built-in access control — code here cannot be imported by external packages
- `pkg/` is for code that CAN be imported by external packages

## Dependency Injection

- All wiring happens in `cmd/api/main.go`
- Use constructor injection (pass interfaces, not concrete types)
- Inner layers define interfaces; outer layers implement them

## Naming Conventions

- Repository files: `<aggregate>_repository/` (e.g., `user_repository/`)
- Use case files: descriptive of the operation (e.g., `create_ticket.go`)
- Handlers: grouped by domain in interface layer
- Test files: `*_test.go` next to the code they test

## Testing Strategy

- Use cases: unit test with mocked repository interfaces
- Repositories: integration test with real database
- Handlers: HTTP test with mocked use cases
- Keep test files alongside source files

## Code Quality

- Always handle errors explicitly — no silent swallows
- Use context.Context for request-scoped values and cancellation
- Validate input at the interface (handler) layer
- Return domain errors from use cases, map to HTTP status in handlers

## Documentation Rule

**IMPORTANT:** Every time you make changes to the project (new feature, bug fix, refactoring, config change), you MUST update `README.md` to reflect the current state. This includes:
- New API endpoints
- Changed project structure
- New environment variables
- Setup/installation steps
- Any breaking changes

## Frontend (React)

- Components in `src/components/`
- Pages in `src/pages/`
- API calls through a centralized service layer
- Use TypeScript when possible
