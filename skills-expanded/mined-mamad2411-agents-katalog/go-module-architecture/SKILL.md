---
name: go-module-architecture
description: "Scaffold a production-grade Go feature module under internal/module/{name}/, following a feature-based structure with one controller file per action, a DB-agnostic repository interface, and DTOs validated with go-playground/validator. Supports both Gin and net/http (auto-detected from the project's go.mod/imports) and both SQL (GORM) and MongoDB (mongo-go-driver) persistence. Use this skill whenever the user asks to create a new Go module, add a new feature/resource/service in a Go backend, or asks how to structure a package in a Go project — including requests like 'create a users module in Go', 'add a Go feature for X', 'scaffold a Go service package', or 'how should I structure this in Go'. This is the Go counterpart to the user's own express-module-architecture skill (Node/Express/TypeScript) — trigger it any time the same kind of request is made for a Go project instead of a Node one."
---

# Go Module Architecture Skill

Go counterpart to `express-module-architecture`. Same feature-per-folder philosophy,
adapted to Go's toolchain constraints (package naming, `_test.go` discovery, `swag`
annotation placement) and extended with a repository interface so one module can be
backed by either SQL or MongoDB without the service layer knowing which.

## Output Format

Always output a tree diagram showing the full module structure with a one-line
annotation per file, matching the annotated-tree style already used by
`express-module-architecture`. No code unless explicitly requested — structs/interfaces
may be shown as bare signatures (no bodies) only when needed to clarify a contract.

## Step 0 — Detect the project's framework and datastore

Before scaffolding, check the project (in this priority order) rather than asking by default:

1. `go.mod` — presence of `github.com/gin-gonic/gin` → Gin; absence → net/http (stdlib).
2. Existing modules under `internal/module/` — copy whatever pattern is already
   established in the repo (framework AND datastore) for consistency, even if it
   differs from the defaults below.
3. If this is the *first* module in a new repo and neither signal exists, ask once:
   framework (Gin vs net/http) and datastore (SQL vs MongoDB) — then remember the
   answer for the rest of the session/repo.

Never mix frameworks inside one binary. A module CAN be SQL-backed while another
module in the same project is Mongo-backed — the repository interface makes that safe.

## Folder Structure

Every module lives under `internal/module/{name}/` (package names are **lowercase**,
no camelCase/PascalCase/underscores — Go convention, not style preference):

```
internal/
└── module/
    └── {name}/
        ├── controller/
        │   └── {feature}_controller.go
        ├── service/
        │   └── {feature}_service.go
        ├── repository/
        │   ├── {feature}_repository.go
        │   ├── {feature}_repository_sql.go
        │   └── {feature}_repository_mongo.go
        ├── schema/
        │   ├── {feature}_schema.go
        │   └── {feature}_document.go
        ├── dto/
        │   └── dto.go
        ├── {feature}_docs.go
        ├── {feature}_routes.go
        ├── {feature}_test.go
        └── module.go
```

## File Responsibilities

| File/Folder | Responsibility |
|-------------|---------------|
| `controller/{feature}_controller.go` | One handler per action (e.g. `login.go`-style split is optional in Go — default to one file per action only if the module has ≥4 actions, otherwise keep them together in `{feature}_controller.go`). Gin: `func Login(c *gin.Context)`. net/http: `func Login(w http.ResponseWriter, r *http.Request)`. Thin — calls service, writes response. **Swaggo annotation comments live here, directly above each handler** (swag parses the comment block immediately preceding the function it documents — a separate file cannot hold them). |
| `service/{feature}_service.go` | All business logic. Depends on the `repository` **interface**, never on GORM/mongo-driver types directly. |
| `repository/{feature}_repository.go` | Defines the interface (e.g. `type Repository interface { Create(ctx, *Entity) error; ... }`). This is the DB-agnostic contract the service depends on. |
| `repository/{feature}_repository_sql.go` | GORM implementation of the interface. Only present if this module is SQL-backed. |
| `repository/{feature}_repository_mongo.go` | mongo-go-driver implementation of the interface. Only present if this module is Mongo-backed. |
| `schema/{feature}_schema.go` | GORM struct + tags (SQL variant). |
| `schema/{feature}_document.go` | bson struct (Mongo variant). Only include whichever file matches the module's datastore — don't scaffold both unless the module genuinely needs dual persistence. |
| `dto/dto.go` | Request/response structs with `validate:"..."` tags (go-playground/validator — the structural equivalent of your Zod schemas; alternatives are ozzo-validation or ent's built-in validation, but validator is the de facto standard and keeps the DTO file shape closest to your Node one). |
| `{feature}_docs.go` | Shared Swagger response/error model structs referenced by `@Success`/`@Failure` tags (e.g. `type ErrorResponse struct{...}`). Does **not** hold handler annotations — see the controller row above. |
| `{feature}_routes.go` | Route registration. Gin: takes a `*gin.RouterGroup`. net/http: takes a `*http.ServeMux`. Whichever the project uses. |
| `{feature}_test.go` | Co-located test file — Go's own tooling (`go test`) only discovers files ending `_test.go` in the same directory/package as the code under test; there is no `__tests__/`-style folder option in this ecosystem. |
| `module.go` | Barrel-equivalent: constructs controller+service+repository with their dependencies and exposes `RegisterRoutes(...)`. |

## Naming Rules

- Package/module folder: **lowercase**, one word where possible — `auth`, `listing`, `propertylisting` (not `property-listing` or `PropertyListing`; Go package names can't contain hyphens and idiomatic Go avoids underscores too).
- Files: `snake_case` — `login_controller.go`, `auth_repository_sql.go` (Go convention, unlike TS `dot.notation`).
- Types/interfaces: `PascalCase` — same as your TS side.
- Functions/variables: `camelCase` for unexported, `PascalCase` for exported.

## Why the repository interface layer (vs. calling GORM/Mongoose directly, like your Node service does)

- **Problem it solves:** lets a service be backed by either SQL or MongoDB (your stated requirement) without branching on datastore inside business logic, and makes the service unit-testable against a mock without a real DB.
- **When it's worth it:** any module where dual-persistence is a real possibility, or where you want fast unit tests for the service layer.
- **Drawback:** one more file per module than your Node pattern (Mongoose's model-in-service was already a thin-enough abstraction there) — pure ceremony for a module that will only ever use one DB.
- **Alternative:** skip `repository/`, call GORM/mongo-driver straight from `service/` — closer to your Node pattern, less indirection. Use this if a given module is a throwaway/simple CRUD module you're confident will never change datastore.

## How to Respond

1. Run Step 0 (detect framework + datastore) before anything else.
2. Confirm the module name if ambiguous.
3. Infer the list of actions from the module name/context.
4. Output the full annotated tree, specific to the module (not generic) — mark which repository/schema file(s) actually apply given the detected datastore.
5. Note any inter-module dependencies.
6. Do NOT generate file contents/function bodies unless the user explicitly asks — bare struct/interface signatures are fine when needed to clarify a contract.

## Example Output (for an `auth` module, Gin + PostgreSQL detected)

```
internal/
└── module/
    └── auth/
        ├── controller/
        │   └── auth_controller.go        → Login, Register, Logout, Refresh, ForgetPassword, ResetPassword handlers (gin.Context); swaggo annotations inline
        ├── service/
        │   └── auth_service.go           → login/register/logout/refresh logic; depends on repository.Repository interface
        ├── repository/
        │   ├── auth_repository.go        → Repository interface: FindByEmail, Create, UpdateRefreshToken, ...
        │   └── auth_repository_sql.go    → GORM implementation
        ├── schema/
        │   └── auth_schema.go            → User struct with GORM tags
        ├── dto/
        │   └── dto.go                    → LoginRequest, RegisterRequest, ResetPasswordRequest (+ validate tags)
        ├── auth_docs.go                  → ErrorResponse, TokenPairResponse (shared swagger models)
        ├── auth_routes.go                → RegisterRoutes(rg *gin.RouterGroup)
        ├── auth_test.go                  → table-driven tests for auth_service.go
        └── module.go                     → NewModule(db *gorm.DB) *Module; exposes RegisterRoutes
```

## Integration Point

After scaffolding, remind the user to wire the module into the binary's entrypoint:

```go
// cmd/api/main.go
authModule := auth.NewModule(db)
authModule.RegisterRoutes(router.Group("/auth"))
```

If a `go-full-backend-architecture`-scaffolded project exists, this is where `backend/`
(or `internal/`) modules get mounted onto `cmd/api`'s router — see that skill for the
surrounding project layout.
