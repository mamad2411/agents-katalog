---
name: generate-speakmanai-code-go
description: Internal LANG_CONFIG reference for Go/BFF backend projects, read automatically by the generate-speakmanai-code router (Step 1c). Not a standalone workflow — do not trigger this on its own; use generate-speakmanai-code instead.
---

# generate-speakmanai-code-go — Go Variant

This file is read by the `generate-speakmanai-code` router (Step 1c) to extract LANG_CONFIG
for Go projects. It is not invoked directly.

The frontend is always React / Vite (JavaScript) regardless of backend language — only the
backend and BFF services are written in Go.

---

## LANG_CONFIG

### CODING_STANDARDS

- **Indent**: tabs (enforced by `gofmt`)
- **Formatting**: run `gofmt -w .` before every commit — the gate will fail if `gofmt` produces a diff
- **Naming**:
  - Exported identifiers: PascalCase (`TodoItem`, `CreateTodo`)
  - Unexported identifiers: camelCase (`todoItem`, `createTodo`)
  - Packages: lowercase, one word (`domain`, `usecases`, `repositories`)
  - SQL columns: snake_case per NAMING_DICT `sql_column`
  - JSON fields: camelCase per NAMING_DICT `json_field` (use `json:"fieldName"` struct tags)
  - All canonical names in NAMING_DICT take precedence over inferred names
- **Error handling**: functions that can fail return `(T, error)` — never panic in business logic
- **Context**: pass `context.Context` as the first argument to every function that does I/O
- **Structs**: use structs for data, interface types for contracts — no class emulation
- **Constructors**: use `NewX(...)` constructor functions that return `(*X, error)`
- **No global mutable state** outside of the db singleton in `infrastructure/database`

---

### DIR_SKELETON_LAYOUT

```
{REPO_PATH}/
  backend/
    cmd/
      server/
        main.go               ← entry point; wires everything together
    internal/
      domain/
        {aggregate}/          ← one package per aggregate root in DOMAIN_MODEL
          {aggregate}.go      ← struct type, New constructor, invariants
          {aggregate}_test.go ← domain unit tests
      application/
        interfaces/           ← repository interface definitions (Go interfaces)
        usecases/             ← one file per UC-XX
        usecases_test.go      ← application unit tests
      infrastructure/
        database/
          connection.go       ← sql.DB singleton
          migrations.go       ← DDL execution
          {aggregate}_repo.go ← one repository implementation per aggregate
          {aggregate}_repo_test.go
      interface/
        http/
          router.go           ← chi router assembly
          {resource}_handler.go ← one handler file per API resource group
          middleware/
            auth.go           ← JWT verification middleware
    go.mod
    go.sum
    .env.example
    .env
  bff/
    main.go                   ← Go reverse proxy; always present
    go.mod
    go.sum
    .env.example
    .env
  frontend/
    src/
      components/
      pages/
      hooks/
    public/                   ← if SPA framework is in TECH_STACK
```

The `bff/` directory is always present. If no SPA framework is in TECH_STACK, `frontend/`
is omitted.

---

### DEPENDENCIES_DERIVATION

List Go module dependencies in `go.mod` per service.

**backend/go.mod** — `module {repo-name}/backend`, `go 1.22`

| Dependency | Module path | When to include |
|---|---|---|
| HTTP router | `github.com/go-chi/chi/v5` | Always (no stdlib mux for DDD routing) |
| SQLite driver | `modernc.org/sqlite` | When TECH_STACK includes SQLite (pure Go — no CGO required) |
| PostgreSQL driver | `github.com/jackc/pgx/v5` | When TECH_STACK includes Postgres |
| JWT | `github.com/golang-jwt/jwt/v5` | When API_SCHEMA defines BearerAuth |
| Password hashing | `golang.org/x/crypto` | When DOMAIN_MODEL / FIELD_DEFS references password hashing |
| UUID | `github.com/google/uuid` | When random UUIDs are generated at runtime |
| Test assertions | `github.com/stretchr/testify` | Always (standard Go testing supplement) |
| env loading | `github.com/joho/godotenv` | Always for dev; production uses OS env directly |
| External SDKs | From API_SCHEMA operation tags | Stripe → `github.com/stripe/stripe-go/v76`; SES → AWS SDK v2 |

**bff/go.mod** — `module {repo-name}/bff`, `go 1.22`

| Dependency | Module path |
|---|---|
| HTTP router | `github.com/go-chi/chi/v5` |
| env loading | `github.com/joho/godotenv` |

**frontend/** — npm packages as in the `js` variant (frontend is always React / Vite).

---

### SCAFFOLD_CONFIG

**backend/go.mod:**
```
module github.com/{repo-name}/backend

go 1.22

require (
    github.com/go-chi/chi/v5 v5.1.0
    modernc.org/sqlite v1.33.1
    github.com/golang-jwt/jwt/v5 v5.2.1
    github.com/google/uuid v1.6.0
    github.com/stretchr/testify v1.9.0
    github.com/joho/godotenv v1.5.1
    golang.org/x/crypto v0.24.0
)
```

**Makefile** at repo root (optional but strongly recommended):
```makefile
.PHONY: test test-domain test-application test-infrastructure test-interface test-e2e fmt

fmt:
	cd backend && gofmt -w .

test-domain:
	cd backend && go test ./internal/domain/...

test-application:
	cd backend && go test ./internal/application/...

test-infrastructure:
	cd backend && go test ./internal/infrastructure/...

test-interface:
	cd backend && go test ./internal/interface/...

test-e2e:
	cd backend && go test ./tests/e2e/... -tags=e2e

test: fmt test-domain test-application test-infrastructure test-interface test-e2e
```

**bff/go.mod:**
```
module github.com/{repo-name}/bff

go 1.22

require (
    github.com/go-chi/chi/v5 v5.1.0
    github.com/joho/godotenv v1.5.1
)
```

---

### SCAFFOLD_FILES

For any Vite-based frontend in DIR_SKELETON, create the same two files as the JS variant:
`frontend/index.html` and `frontend/src/main.jsx`. (The frontend is always React/Vite.)

---

### GITIGNORE_ENTRIES

```
# Binaries
/backend/bin/
/bff/bin/
*.exe

# Test binaries
*.test

# Coverage
*.out
coverage.html

# Environment
.env

# Database files
*.db
*.sqlite

# Node (frontend)
node_modules/
dist/
.vite/
coverage/
```

---

### SECRET_GENERATION_CMD

```bash
openssl rand -hex 32
```

Or in Go: `import "crypto/rand"` with `rand.Read(b)` and hex-encode — but `openssl` is
simpler for the scaffold step.

---

### VALIDATION_GATE

```bash
make test
```

(Runs `gofmt` check + all per-layer test suites. Must be defined in the Makefile above.)

---

### MILESTONE_GATES

```
install:        go mod download             (run in each Go service directory that has new/changed modules)
domain:         make test-domain
application:    make test-application
infrastructure: make test-infrastructure
interface:      make test-interface
e2e:            make test-e2e
ui_build:       cd frontend && npm install && npm run build   (frontend is always React/Vite)
```

---

### LOCAL_DB_TEST

SQLite in-memory: use `"file::memory:?cache=shared&mode=memory"` as the DSN when constructing
`sql.Open("sqlite", ...)` in test setup. The `modernc.org/sqlite` driver accepts this.

---

### DOMAIN_IMPLEMENTATION_GUIDE

Implement each aggregate root as a Go struct with a `New` constructor function in
`internal/domain/{aggregate}/{aggregate}.go`.

**Domain error type** — define once in `internal/domain/errors.go`:
```go
package domain

import "fmt"

type DomainError struct {
	Code    string
	Message string
}

func (e *DomainError) Error() string {
	return fmt.Sprintf("[%s] %s", e.Code, e.Message)
}

func ValidationError(msg string) *DomainError {
	return &DomainError{Code: "VALIDATION_ERROR", Message: msg}
}

func NotFoundError(msg string) *DomainError {
	return &DomainError{Code: "NOT_FOUND", Message: msg}
}

func ConflictError(msg string) *DomainError {
	return &DomainError{Code: "CONFLICT", Message: msg}
}

func UnauthorizedError(msg string) *DomainError {
	return &DomainError{Code: "UNAUTHORIZED", Message: msg}
}
```

**Aggregate struct pattern:**
```go
package todoitem

import (
	"time"
	"{repo-name}/backend/internal/domain"
)

type TodoItem struct {
	ID          string
	Title       string
	IsCompleted bool
	CreatedAt   time.Time
}

func New(id, title string) (*TodoItem, error) {
	if id == "" {
		return nil, domain.ValidationError("id is required")
	}
	if title == "" {
		return nil, domain.ValidationError("title is required")
	}
	return &TodoItem{
		ID:          id,
		Title:       title,
		IsCompleted: false,
		CreatedAt:   time.Now().UTC(),
	}, nil
}
```

**Value Object pattern:**
```go
type Email struct{ Value string }

func NewEmail(value string) (Email, error) {
	if !strings.Contains(value, "@") {
		return Email{}, domain.ValidationError("email must be a valid email address")
	}
	return Email{Value: strings.ToLower(value)}, nil
}
```

**Domain layer rules:**
- No database imports, no `net/http`, no `os.File`, no side effects
- All invariant checks in the `New` / value-object constructor — return `(nil, error)` on failure
- Use `domain.ValidationError(...)` — never `fmt.Errorf(...)` alone
- Structs are exported; constructor functions are always exported (`New...`)

---

### REPO_INTERFACE_PATTERN

Define repository interfaces in `internal/application/interfaces/`:

```go
package interfaces

import (
	"context"
	"{repo-name}/backend/internal/domain/todoitem"
)

type TodoRepository interface {
	Save(ctx context.Context, item *todoitem.TodoItem) error
	FindByID(ctx context.Context, id string) (*todoitem.TodoItem, error)
	FindAll(ctx context.Context) ([]*todoitem.TodoItem, error)
	Delete(ctx context.Context, id string) error
}

type AuditRepository interface {
	Save(ctx context.Context, entry *AuditEntry) error
}
```

These are contracts only — no implementation code in `interfaces/`.

---

### DOMAIN_TEST_GUIDE

Use Go's `testing` package with `testify/assert`:

```go
package todoitem_test

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"{repo-name}/backend/internal/domain/todoitem"
)

func TestNew_EmptyTitle_ReturnsValidationError(t *testing.T) {
	_, err := todoitem.New("id-1", "")
	require.Error(t, err)
	assert.Contains(t, err.Error(), "VALIDATION_ERROR")
}

func TestNew_ValidInput_CreatesItem(t *testing.T) {
	item, err := todoitem.New("id-1", "Buy milk")
	require.NoError(t, err)
	assert.Equal(t, "Buy milk", item.Title)
	assert.False(t, item.IsCompleted)
}
```

---

### APPLICATION_IMPLEMENTATION_GUIDE

Implement each UC-XX as a function in `internal/application/usecases/`:

```go
package usecases

import (
	"context"
	"github.com/google/uuid"
	"{repo-name}/backend/internal/application/interfaces"
	"{repo-name}/backend/internal/domain/todoitem"
)

type Repos struct {
	Todos  interfaces.TodoRepository
	Audits interfaces.AuditRepository
}

func CreateTodo(ctx context.Context, repos Repos, title, userID string) (*todoitem.TodoItem, error) {
	item, err := todoitem.New(uuid.NewString(), title)
	if err != nil {
		return nil, err
	}
	if err := repos.Todos.Save(ctx, item); err != nil {
		return nil, err
	}
	_ = repos.Audits.Save(ctx, &interfaces.AuditEntry{
		Action:   "TODO_CREATED",
		EntityID: item.ID,
		UserID:   userID,
	})
	return item, nil
}
```

Never import from `infrastructure` or `interface/http` packages. Repositories are injected
via the `Repos` struct.

---

### APPLICATION_TEST_GUIDE

Use testify/mock to stub repository interfaces:

```go
package usecases_test

import (
	"context"
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"{repo-name}/backend/internal/application/usecases"
	"{repo-name}/backend/internal/application/interfaces"
)

type MockTodoRepo struct{ mock.Mock }
func (m *MockTodoRepo) Save(ctx context.Context, item *todoitem.TodoItem) error {
	return m.Called(ctx, item).Error(0)
}
// ... other interface methods

func TestCreateTodo_SavesItemAndAudit(t *testing.T) {
	todoRepo := new(MockTodoRepo)
	auditRepo := new(MockAuditRepo)
	todoRepo.On("Save", mock.Anything, mock.Anything).Return(nil)
	auditRepo.On("Save", mock.Anything, mock.Anything).Return(nil)

	item, err := usecases.CreateTodo(context.Background(), usecases.Repos{Todos: todoRepo, Audits: auditRepo}, "Buy milk", "u1")
	assert.NoError(t, err)
	assert.Equal(t, "Buy milk", item.Title)
	todoRepo.AssertExpectations(t)
	auditRepo.AssertExpectations(t)
}
```

---

### INFRASTRUCTURE_IMPLEMENTATION_GUIDE

Use `database/sql` with the `modernc.org/sqlite` driver.

**Connection module** (`internal/infrastructure/database/connection.go`):
```go
package database

import (
	"database/sql"
	_ "modernc.org/sqlite"
)

var _db *sql.DB

func Open(dsn string) (*sql.DB, error) {
	if _db != nil {
		return _db, nil
	}
	db, err := sql.Open("sqlite", dsn)
	if err != nil {
		return nil, err
	}
	_db = db
	return _db, nil
}
```

**Migration runner** (`internal/infrastructure/database/migrations.go`):
```go
func RunMigrations(db *sql.DB) error {
	_, err := db.Exec(`
		CREATE TABLE IF NOT EXISTS todo_items (
			id TEXT PRIMARY KEY,
			title TEXT NOT NULL,
			is_completed INTEGER NOT NULL DEFAULT 0,
			created_at TEXT NOT NULL
		)
	`)
	return err
}
```

**Repository implementation** — one per aggregate:
```go
type SQLiteTodoRepository struct{ db *sql.DB }

func NewTodoRepository(db *sql.DB) *SQLiteTodoRepository {
	return &SQLiteTodoRepository{db: db}
}

func (r *SQLiteTodoRepository) Save(ctx context.Context, item *todoitem.TodoItem) error {
	_, err := r.db.ExecContext(ctx,
		`INSERT INTO todo_items (id, title, is_completed, created_at) VALUES (?, ?, ?, ?)
		 ON CONFLICT(id) DO UPDATE SET title=excluded.title, is_completed=excluded.is_completed`,
		item.ID, item.Title, boolToInt(item.IsCompleted), item.CreatedAt.Format(time.RFC3339),
	)
	if isSQLiteConstraint(err) {
		return domain.ConflictError("todo item already exists")
	}
	return err
}

func (r *SQLiteTodoRepository) FindByID(ctx context.Context, id string) (*todoitem.TodoItem, error) {
	row := r.db.QueryRowContext(ctx, `SELECT id, title, is_completed, created_at FROM todo_items WHERE id = ?`, id)
	return scanTodoItem(row)
}

func scanTodoItem(row *sql.Row) (*todoitem.TodoItem, error) {
	var item todoitem.TodoItem
	var isCompleted int
	var createdAt string
	if err := row.Scan(&item.ID, &item.Title, &isCompleted, &createdAt); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, domain.NotFoundError("todo item not found")
		}
		return nil, err
	}
	item.IsCompleted = isCompleted != 0
	item.CreatedAt, _ = time.Parse(time.RFC3339, createdAt)
	return &item, nil
}

func boolToInt(b bool) int {
	if b { return 1 }
	return 0
}

func isSQLiteConstraint(err error) bool {
	if err == nil { return false }
	return strings.Contains(err.Error(), "UNIQUE constraint")
}
```

---

### INFRASTRUCTURE_TEST_GUIDE

Use real in-memory SQLite — no mocks:

```go
package database_test

import (
	"context"
	"database/sql"
	"testing"
	_ "modernc.org/sqlite"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"{repo-name}/backend/internal/infrastructure/database"
)

func TestTodoRepository_SaveAndFindByID(t *testing.T) {
	db, err := sql.Open("sqlite", "file::memory:?cache=shared&mode=memory")
	require.NoError(t, err)
	require.NoError(t, database.RunMigrations(db))

	repo := database.NewTodoRepository(db)
	item, _ := todoitem.New("id-1", "Buy milk")
	require.NoError(t, repo.Save(context.Background(), item))

	found, err := repo.FindByID(context.Background(), "id-1")
	require.NoError(t, err)
	assert.Equal(t, "Buy milk", found.Title)
}

func TestTodoRepository_FindByID_NotFound(t *testing.T) {
	db, _ := sql.Open("sqlite", "file::memory:?cache=shared&mode=memory")
	database.RunMigrations(db)
	repo := database.NewTodoRepository(db)

	_, err := repo.FindByID(context.Background(), "nonexistent")
	require.Error(t, err)
	assert.Contains(t, err.Error(), "NOT_FOUND")
}
```

---

### INTERFACE_IMPLEMENTATION_GUIDE

Use `chi` for routing. Handlers live in `internal/interface/http/`.

**Router assembly** (`internal/interface/http/router.go`):
```go
package http

import (
	"net/http"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

func NewRouter(repos usecases.Repos) http.Handler {
	r := chi.NewRouter()
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)

	r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{"status":"ok"}`))
	})

	r.Route("/api", func(r chi.Router) {
		r.Use(JWTMiddleware)
		r.Mount("/todos", TodoHandler(repos))
	})

	return r
}
```

**Handler pattern** (`internal/interface/http/todo_handler.go`):
```go
func TodoHandler(repos usecases.Repos) http.Handler {
	r := chi.NewRouter()

	r.Post("/", func(w http.ResponseWriter, r *http.Request) {
		var body struct {
			Title string `json:"title"`
		}
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			writeError(w, http.StatusBadRequest, "VALIDATION_ERROR", "invalid request body")
			return
		}
		if body.Title == "" {
			writeError(w, http.StatusUnprocessableEntity, "VALIDATION_ERROR", "title is required")
			return
		}
		userID := r.Context().Value(contextKeyUserID).(string)
		item, err := usecases.CreateTodo(r.Context(), repos, body.Title, userID)
		if err != nil {
			writeErr(w, err)
			return
		}
		writeJSON(w, http.StatusCreated, item)
	})

	return r
}
```

**Error writing helpers** (`internal/interface/http/helpers.go`):
```go
func writeErr(w http.ResponseWriter, err error) {
	var de *domain.DomainError
	if errors.As(err, &de) {
		status := map[string]int{
			"NOT_FOUND": 404, "UNAUTHORIZED": 401, "CONFLICT": 409, "VALIDATION_ERROR": 422,
		}[de.Code]
		if status == 0 { status = 500 }
		writeError(w, status, de.Code, de.Message)
		return
	}
	log.Printf("unhandled error: %v", err)
	writeError(w, 500, "INTERNAL_ERROR", "Internal server error")
}

func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(v)
}

func writeError(w http.ResponseWriter, status int, code, message string) {
	writeJSON(w, status, map[string]string{"error": code, "message": message})
}
```

**JWT middleware** (`internal/interface/http/middleware/auth.go`):
```go
func JWTMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		header := r.Header.Get("Authorization")
		tokenStr, _ := strings.CutPrefix(header, "Bearer ")
		if tokenStr == "" {
			writeError(w, 401, "UNAUTHORIZED", "Missing or invalid token")
			return
		}
		claims := jwt.MapClaims{}
		token, err := jwt.ParseWithClaims(tokenStr, claims, func(t *jwt.Token) (any, error) {
			return []byte(os.Getenv("JWT_SECRET")), nil
		})
		if err != nil || !token.Valid {
			writeError(w, 401, "UNAUTHORIZED", "Missing or invalid token")
			return
		}
		ctx := context.WithValue(r.Context(), contextKeyUserID, claims["sub"])
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}
```

---

### BFF_PRESENT

`true` — the BFF is a separate Go binary using `httputil.ReverseProxy`.

---

### BFF_IMPLEMENTATION

The BFF is a minimal Go service (`bff/main.go`):

```go
package main

import (
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"github.com/go-chi/chi/v5"
	"github.com/joho/godotenv"
)

func main() {
	godotenv.Load()

	backendURL, _ := url.Parse(os.Getenv("BACKEND_URL"))
	proxy := httputil.NewSingleHostReverseProxy(backendURL)
	proxy.ErrorHandler = func(w http.ResponseWriter, r *http.Request, err error) {
		log.Printf("BFF proxy error: %v", err)
		w.WriteHeader(http.StatusBadGateway)
		w.Write([]byte(`{"error":"BAD_GATEWAY","message":"Backend service unavailable"}`))
	}

	r := chi.NewRouter()
	r.Handle("/api/*", proxy)

	port := os.Getenv("PORT")
	if port == "" { port = "3000" }
	log.Printf("BFF listening on :%s → %s", port, backendURL)
	log.Fatal(http.ListenAndServe(":"+port, r))
}
```

---

### INTERFACE_TEST_GUIDE

Use `net/http/httptest` with a real chi router backed by in-memory database:

```go
package http_test

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	httphandler "{repo-name}/backend/internal/interface/http"
)

func TestCreateTodo_Returns201(t *testing.T) {
	repos := setupTestRepos(t)          // creates in-memory DB + real repo impls
	handler := httphandler.NewRouter(repos)

	token := signTestJWT(t)
	body := `{"title":"Buy milk"}`
	req := httptest.NewRequest(http.MethodPost, "/api/todos", strings.NewReader(body))
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)

	assert.Equal(t, http.StatusCreated, rec.Code)
	var res map[string]any
	require.NoError(t, json.Unmarshal(rec.Body.Bytes(), &res))
	assert.Equal(t, "Buy milk", res["title"])
}

func TestCreateTodo_Returns422_WhenTitleMissing(t *testing.T) {
	repos := setupTestRepos(t)
	handler := httphandler.NewRouter(repos)

	token := signTestJWT(t)
	req := httptest.NewRequest(http.MethodPost, "/api/todos", strings.NewReader(`{}`))
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)

	assert.Equal(t, http.StatusUnprocessableEntity, rec.Code)
}
```

---

### E2E_IMPLEMENTATION_GUIDE

One test file per UC-ID named `UC{XX}_test.go` in `backend/tests/e2e/`. Build tag: `//go:build e2e`.
Use `httptest.NewServer` to spin up a real HTTP server backed by an in-memory database.

```go
//go:build e2e

package e2e_test

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestUC01_CreateAndRetrieveTodo(t *testing.T) {
	srv := httptest.NewServer(buildTestServer(t))
	defer srv.Close()

	// Register and obtain a token through the real API — no seeding
	regBody := `{"username":"alice","password":"Password123!"}`
	regRes, err := http.Post(srv.URL+"/api/auth/register", "application/json", strings.NewReader(regBody))
	require.NoError(t, err)
	var auth map[string]any
	json.NewDecoder(regRes.Body).Decode(&auth)
	token := auth["token"].(string)

	// Create a todo through the API
	req, _ := http.NewRequest(http.MethodPost, srv.URL+"/api/todos", strings.NewReader(`{"title":"Buy milk"}`))
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Content-Type", "application/json")
	createRes, err := http.DefaultClient.Do(req)
	require.NoError(t, err)
	assert.Equal(t, http.StatusCreated, createRes.StatusCode)

	var todo map[string]any
	json.NewDecoder(createRes.Body).Decode(&todo)
	id := todo["id"].(string)

	// Retrieve it
	getReq, _ := http.NewRequest(http.MethodGet, srv.URL+"/api/todos/"+id, nil)
	getReq.Header.Set("Authorization", "Bearer "+token)
	getRes, err := http.DefaultClient.Do(getReq)
	require.NoError(t, err)
	assert.Equal(t, http.StatusOK, getRes.StatusCode)
}
```

---

### RUN_LOCALLY_INSTRUCTIONS

```
cd {REPO_PATH}/backend  && go run ./cmd/server    # backend API (default :3001)
cd {REPO_PATH}/bff      && go run .               # BFF proxy (default :3000)
cd {REPO_PATH}/frontend && npm run dev            # React SPA (Vite, default :5173)
```
