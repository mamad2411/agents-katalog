---
name: qa-go
description: "Go testing skill with table-driven tests, httptest, testify, and integration testing patterns. Use when writing or running Go backend tests."
---

# Go Testing

## Purpose

This skill equips the `tester-go` agent with everything needed to write, run, and maintain Go backend tests in a fullstack Golang + React codebase. It covers unit testing for handlers, services, and repositories, integration testing with database mocks, HTTP handler testing with Chi router, and mock generation with testify. The guiding philosophy: **test behavior at interface boundaries, not internal implementation details**.

## Core Testing Stack

| Tool | Role | Import Path |
|------|------|-------------|
| **testing** | Standard library test runner | `testing` |
| **testify/assert** | Non-fatal assertions | `github.com/stretchr/testify/assert` |
| **testify/require** | Fatal assertions (stop test on failure) | `github.com/stretchr/testify/require` |
| **testify/mock** | Interface mocking | `github.com/stretchr/testify/mock` |
| **testify/suite** | Test suite with setup/teardown (optional) | `github.com/stretchr/testify/suite` |
| **httptest** | HTTP handler testing | `net/http/httptest` |
| **sqlmock** | SQL database mocking | `github.com/DATA-DOG/go-sqlmock` |
| **testcontainers-go** | Real database in Docker (integration) | `github.com/testcontainers/testcontainers-go` |
| **go-chi** | Router context for handler tests | `github.com/go-chi/chi/v5` |

## Table-Driven Tests — The Core Pattern

Every function with multiple scenarios MUST use table-driven tests. This is the single most important Go testing pattern.

### Basic Structure

```go
func TestUserService_Create(t *testing.T) {
    tests := []struct {
        name    string
        input   model.CreateUserRequest
        mockFn  func(*MockUserRepository)
        wantErr bool
        errType error
    }{
        {
            name:  "success - creates user with valid input",
            input: model.CreateUserRequest{Email: "test@example.com", Name: "Test User"},
            mockFn: func(m *MockUserRepository) {
                m.On("GetByEmail", mock.Anything, "test@example.com").Return(nil, repository.ErrNotFound)
                m.On("Create", mock.Anything, mock.AnythingOfType("*model.User")).Return(nil)
            },
            wantErr: false,
        },
        {
            name:  "error - duplicate email returns conflict",
            input: model.CreateUserRequest{Email: "exists@example.com", Name: "Test"},
            mockFn: func(m *MockUserRepository) {
                m.On("GetByEmail", mock.Anything, "exists@example.com").Return(&model.User{}, nil)
            },
            wantErr: true,
            errType: model.ErrAlreadyExists,
        },
        {
            name:  "error - empty email returns validation error",
            input: model.CreateUserRequest{Email: "", Name: "Test"},
            mockFn: func(m *MockUserRepository) {},
            wantErr: true,
            errType: model.ErrValidation,
        },
        {
            name:  "error - repository failure returns internal error",
            input: model.CreateUserRequest{Email: "test@example.com", Name: "Test"},
            mockFn: func(m *MockUserRepository) {
                m.On("GetByEmail", mock.Anything, "test@example.com").Return(nil, repository.ErrNotFound)
                m.On("Create", mock.Anything, mock.AnythingOfType("*model.User")).Return(fmt.Errorf("db connection failed"))
            },
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            repo := new(MockUserRepository)
            tt.mockFn(repo)

            svc := service.NewUserService(repo)
            err := svc.Create(context.Background(), tt.input)

            if tt.wantErr {
                require.Error(t, err)
                if tt.errType != nil {
                    assert.ErrorIs(t, err, tt.errType)
                }
            } else {
                require.NoError(t, err)
            }
            repo.AssertExpectations(t)
        })
    }
}
```

### Table Test Rules

1. **Name every test case** — `name` field is mandatory, must be descriptive
2. **Use `t.Run(tt.name, ...)`** — enables running individual test cases
3. **Include success AND error paths** — minimum 1 success + 2 error cases per function
4. **Mock setup in the table** — use `mockFn` field, not shared mock state
5. **Assert expectations** — always call `mock.AssertExpectations(t)` at the end
6. **Test edge cases** — nil inputs, empty strings, zero values, max-length strings, duplicate operations

## HTTP Handler Testing with httptest + Chi

### Complete Handler Test Pattern

```go
func TestUserHandler_GetByID(t *testing.T) {
    tests := []struct {
        name       string
        userID     string
        mockFn     func(*MockUserService)
        wantStatus int
        wantBody   string
    }{
        {
            name:   "success - returns user",
            userID: "550e8400-e29b-41d4-a716-446655440000",
            mockFn: func(m *MockUserService) {
                m.On("GetByID", mock.Anything, uuid.MustParse("550e8400-e29b-41d4-a716-446655440000")).
                    Return(&model.User{
                        ID:    uuid.MustParse("550e8400-e29b-41d4-a716-446655440000"),
                        Name:  "Test User",
                        Email: "test@example.com",
                    }, nil)
            },
            wantStatus: http.StatusOK,
            wantBody:   `"name":"Test User"`,
        },
        {
            name:   "error - invalid UUID format",
            userID: "not-a-uuid",
            mockFn: func(m *MockUserService) {},
            wantStatus: http.StatusBadRequest,
            wantBody:   `"error"`,
        },
        {
            name:   "error - user not found",
            userID: "550e8400-e29b-41d4-a716-446655440000",
            mockFn: func(m *MockUserService) {
                m.On("GetByID", mock.Anything, mock.Anything).
                    Return(nil, service.ErrNotFound)
            },
            wantStatus: http.StatusNotFound,
            wantBody:   `"error"`,
        },
        {
            name:   "error - internal server error",
            userID: "550e8400-e29b-41d4-a716-446655440000",
            mockFn: func(m *MockUserService) {
                m.On("GetByID", mock.Anything, mock.Anything).
                    Return(nil, fmt.Errorf("database timeout"))
            },
            wantStatus: http.StatusInternalServerError,
            wantBody:   `"error"`,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            svc := new(MockUserService)
            tt.mockFn(svc)
            h := handler.NewUserHandler(svc)

            // Create request with Chi URL params
            req := httptest.NewRequest(http.MethodGet, "/api/v1/users/"+tt.userID, nil)
            rctx := chi.NewRouteContext()
            rctx.URLParams.Add("id", tt.userID)
            req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))

            rec := httptest.NewRecorder()
            h.GetByID(rec, req)

            assert.Equal(t, tt.wantStatus, rec.Code)
            assert.Contains(t, rec.Body.String(), tt.wantBody)
            svc.AssertExpectations(t)
        })
    }
}
```

### POST/PUT Handler Test Pattern with Request Body

```go
func TestUserHandler_Create(t *testing.T) {
    tests := []struct {
        name       string
        body       string
        mockFn     func(*MockUserService)
        wantStatus int
    }{
        {
            name: "success - creates user",
            body: `{"email":"new@test.com","name":"New User","password":"securepass123"}`,
            mockFn: func(m *MockUserService) {
                m.On("Create", mock.Anything, mock.AnythingOfType("model.CreateUserRequest")).
                    Return(&model.User{ID: uuid.New(), Email: "new@test.com", Name: "New User"}, nil)
            },
            wantStatus: http.StatusCreated,
        },
        {
            name:       "error - malformed JSON",
            body:       `{invalid json`,
            mockFn:     func(m *MockUserService) {},
            wantStatus: http.StatusBadRequest,
        },
        {
            name:       "error - missing required field",
            body:       `{"name":"No Email"}`,
            mockFn:     func(m *MockUserService) {},
            wantStatus: http.StatusBadRequest,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            svc := new(MockUserService)
            tt.mockFn(svc)
            h := handler.NewUserHandler(svc)

            req := httptest.NewRequest(http.MethodPost, "/api/v1/users",
                strings.NewReader(tt.body))
            req.Header.Set("Content-Type", "application/json")
            rec := httptest.NewRecorder()

            h.Create(rec, req)

            assert.Equal(t, tt.wantStatus, rec.Code)
            svc.AssertExpectations(t)
        })
    }
}
```

### Chi Router Integration Test

```go
func TestUserRoutes(t *testing.T) {
    svc := new(MockUserService)
    h := handler.NewUserHandler(svc)

    r := chi.NewRouter()
    r.Route("/api/v1/users", func(r chi.Router) {
        r.Get("/", h.List)
        r.Post("/", h.Create)
        r.Get("/{id}", h.GetByID)
        r.Put("/{id}", h.Update)
        r.Delete("/{id}", h.Delete)
    })

    ts := httptest.NewServer(r)
    defer ts.Close()

    // Test through actual router — validates routing, middleware, and URL params
    resp, err := http.Get(ts.URL + "/api/v1/users")
    require.NoError(t, err)
    assert.Equal(t, http.StatusOK, resp.StatusCode)
}
```

## Mock Interface Pattern (testify/mock)

### Generating Mocks from Interfaces

For every interface in the `repository` or `service` package, create a corresponding mock:

```go
// MockUserRepository implements repository.UserRepository
type MockUserRepository struct {
    mock.Mock
}

func (m *MockUserRepository) GetByID(ctx context.Context, id uuid.UUID) (*model.User, error) {
    args := m.Called(ctx, id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*model.User), args.Error(1)
}

func (m *MockUserRepository) GetByEmail(ctx context.Context, email string) (*model.User, error) {
    args := m.Called(ctx, email)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*model.User), args.Error(1)
}

func (m *MockUserRepository) Create(ctx context.Context, user *model.User) error {
    args := m.Called(ctx, user)
    return args.Error(0)
}

func (m *MockUserRepository) Update(ctx context.Context, user *model.User) error {
    args := m.Called(ctx, user)
    return args.Error(0)
}

func (m *MockUserRepository) Delete(ctx context.Context, id uuid.UUID) error {
    args := m.Called(ctx, id)
    return args.Error(0)
}

func (m *MockUserRepository) List(ctx context.Context, opts model.ListOptions) ([]*model.User, int, error) {
    args := m.Called(ctx, opts)
    if args.Get(0) == nil {
        return nil, 0, args.Error(2)
    }
    return args.Get(0).([]*model.User), args.Int(1), args.Error(2)
}
```

### Mock Rules

1. **Mock at interface boundaries only** — mock repositories when testing services, mock services when testing handlers
2. **Never mock internal functions** — if you need to mock a function, extract it behind an interface first
3. **Always call `AssertExpectations(t)`** — verifies all expected calls were made
4. **Use `mock.Anything`** for context.Context — never match on specific context values
5. **Use `mock.AnythingOfType("*model.User")`** when you don't care about the exact value
6. **Handle nil returns** — check `args.Get(0) == nil` before type-asserting pointer returns

## Repository Testing Patterns

### With sqlmock (Unit Tests)

```go
func TestUserRepository_GetByID(t *testing.T) {
    db, mock, err := sqlmock.New()
    require.NoError(t, err)
    defer db.Close()

    repo := repository.NewUserRepository(db)
    userID := uuid.MustParse("550e8400-e29b-41d4-a716-446655440000")

    rows := sqlmock.NewRows([]string{"id", "email", "name", "created_at", "updated_at"}).
        AddRow(userID, "test@example.com", "Test User", time.Now(), time.Now())

    mock.ExpectQuery(`SELECT .+ FROM users WHERE id = \$1`).
        WithArgs(userID).
        WillReturnRows(rows)

    user, err := repo.GetByID(context.Background(), userID)

    require.NoError(t, err)
    assert.Equal(t, "Test User", user.Name)
    assert.Equal(t, "test@example.com", user.Email)
    require.NoError(t, mock.ExpectationsWereMet())
}

func TestUserRepository_GetByID_NotFound(t *testing.T) {
    db, mock, err := sqlmock.New()
    require.NoError(t, err)
    defer db.Close()

    repo := repository.NewUserRepository(db)
    userID := uuid.New()

    mock.ExpectQuery(`SELECT .+ FROM users WHERE id = \$1`).
        WithArgs(userID).
        WillReturnError(sql.ErrNoRows)

    user, err := repo.GetByID(context.Background(), userID)

    assert.Nil(t, user)
    assert.ErrorIs(t, err, repository.ErrNotFound)
    require.NoError(t, mock.ExpectationsWereMet())
}
```

### With testcontainers-go (Integration Tests)

```go
func setupTestDB(t *testing.T) (*sql.DB, func()) {
    t.Helper()
    ctx := context.Background()

    container, err := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
        ContainerRequest: testcontainers.ContainerRequest{
            Image:        "postgres:16-alpine",
            ExposedPorts: []string{"5432/tcp"},
            Env: map[string]string{
                "POSTGRES_USER":     "test",
                "POSTGRES_PASSWORD": "test",
                "POSTGRES_DB":       "testdb",
            },
            WaitingFor: wait.ForListeningPort("5432/tcp").WithStartupTimeout(60 * time.Second),
        },
        Started: true,
    })
    require.NoError(t, err)

    host, _ := container.Host(ctx)
    port, _ := container.MappedPort(ctx, "5432")
    dsn := fmt.Sprintf("postgres://test:test@%s:%s/testdb?sslmode=disable", host, port.Port())

    db, err := sql.Open("postgres", dsn)
    require.NoError(t, err)

    // Run migrations
    runMigrations(t, db)

    cleanup := func() {
        db.Close()
        container.Terminate(ctx)
    }

    return db, cleanup
}

func TestUserRepository_Integration(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping integration test in short mode")
    }

    db, cleanup := setupTestDB(t)
    defer cleanup()

    repo := repository.NewUserRepository(db)

    // Test Create
    user := &model.User{
        ID:    uuid.New(),
        Email: "integration@test.com",
        Name:  "Integration User",
    }
    err := repo.Create(context.Background(), user)
    require.NoError(t, err)

    // Test GetByID
    found, err := repo.GetByID(context.Background(), user.ID)
    require.NoError(t, err)
    assert.Equal(t, user.Email, found.Email)
    assert.Equal(t, user.Name, found.Name)
}
```

## Test Helper Utilities

### Standard Test Helpers (`internal/testutil/`)

```go
// internal/testutil/helpers.go
package testutil

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "strings"
    "testing"

    "github.com/go-chi/chi/v5"
)

// NewRequest creates an httptest.Request with optional JSON body.
func NewRequest(t *testing.T, method, path string, body interface{}) *http.Request {
    t.Helper()
    var req *http.Request
    if body != nil {
        b, err := json.Marshal(body)
        if err != nil {
            t.Fatalf("failed to marshal request body: %v", err)
        }
        req = httptest.NewRequest(method, path, strings.NewReader(string(b)))
        req.Header.Set("Content-Type", "application/json")
    } else {
        req = httptest.NewRequest(method, path, nil)
    }
    return req
}

// WithChiURLParam adds Chi URL parameters to the request context.
func WithChiURLParam(r *http.Request, key, value string) *http.Request {
    rctx := chi.NewRouteContext()
    rctx.URLParams.Add(key, value)
    return r.WithContext(context.WithValue(r.Context(), chi.RouteCtxKey, rctx))
}

// WithChiURLParams adds multiple Chi URL parameters.
func WithChiURLParams(r *http.Request, params map[string]string) *http.Request {
    rctx := chi.NewRouteContext()
    for key, value := range params {
        rctx.URLParams.Add(key, value)
    }
    return r.WithContext(context.WithValue(r.Context(), chi.RouteCtxKey, rctx))
}

// DecodeResponse decodes the JSON response body into the given struct.
func DecodeResponse(t *testing.T, rec *httptest.ResponseRecorder, v interface{}) {
    t.Helper()
    err := json.NewDecoder(rec.Body).Decode(v)
    if err != nil {
        t.Fatalf("failed to decode response: %v", err)
    }
}

// AssertStatus checks the response status code.
func AssertStatus(t *testing.T, rec *httptest.ResponseRecorder, expected int) {
    t.Helper()
    if rec.Code != expected {
        t.Errorf("expected status %d, got %d. Body: %s", expected, rec.Code, rec.Body.String())
    }
}
```

### Test Data Factories

```go
// internal/testutil/factories.go
package testutil

import (
    "time"
    "github.com/google/uuid"
    "myapp/internal/model"
)

// NewUser creates a test user with sensible defaults. Override fields as needed.
func NewUser(overrides ...func(*model.User)) *model.User {
    u := &model.User{
        ID:        uuid.New(),
        Email:     "user@example.com",
        Name:      "Test User",
        CreatedAt: time.Now(),
        UpdatedAt: time.Now(),
    }
    for _, fn := range overrides {
        fn(u)
    }
    return u
}

// WithEmail overrides the user's email.
func WithEmail(email string) func(*model.User) {
    return func(u *model.User) { u.Email = email }
}

// WithName overrides the user's name.
func WithName(name string) func(*model.User) {
    return func(u *model.User) { u.Name = name }
}
```

## Middleware Testing

```go
func TestAuthMiddleware(t *testing.T) {
    tests := []struct {
        name       string
        authHeader string
        mockFn     func(*MockAuthService)
        wantStatus int
    }{
        {
            name:       "success - valid token",
            authHeader: "Bearer valid-token-123",
            mockFn: func(m *MockAuthService) {
                m.On("ValidateToken", mock.Anything, "valid-token-123").
                    Return(&model.User{ID: uuid.New()}, nil)
            },
            wantStatus: http.StatusOK,
        },
        {
            name:       "error - missing auth header",
            authHeader: "",
            mockFn:     func(m *MockAuthService) {},
            wantStatus: http.StatusUnauthorized,
        },
        {
            name:       "error - invalid token format",
            authHeader: "InvalidFormat",
            mockFn:     func(m *MockAuthService) {},
            wantStatus: http.StatusUnauthorized,
        },
        {
            name:       "error - expired token",
            authHeader: "Bearer expired-token",
            mockFn: func(m *MockAuthService) {
                m.On("ValidateToken", mock.Anything, "expired-token").
                    Return(nil, service.ErrTokenExpired)
            },
            wantStatus: http.StatusUnauthorized,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            authSvc := new(MockAuthService)
            tt.mockFn(authSvc)

            // Create a test handler behind the middleware
            nextHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
                w.WriteHeader(http.StatusOK)
            })

            mw := middleware.Auth(authSvc)
            handler := mw(nextHandler)

            req := httptest.NewRequest(http.MethodGet, "/protected", nil)
            if tt.authHeader != "" {
                req.Header.Set("Authorization", tt.authHeader)
            }
            rec := httptest.NewRecorder()

            handler.ServeHTTP(rec, req)
            assert.Equal(t, tt.wantStatus, rec.Code)
            authSvc.AssertExpectations(t)
        })
    }
}
```

## Error Testing Patterns

### Testing Wrapped Errors

```go
func TestServiceError_Wrapping(t *testing.T) {
    // Test that service errors wrap correctly for handler consumption
    repo := new(MockUserRepository)
    repo.On("GetByID", mock.Anything, mock.Anything).
        Return(nil, fmt.Errorf("connection refused"))

    svc := service.NewUserService(repo)
    _, err := svc.GetByID(context.Background(), uuid.New())

    require.Error(t, err)
    // Verify the error wraps with context
    assert.Contains(t, err.Error(), "get user")
    assert.Contains(t, err.Error(), "connection refused")
}
```

### Testing Custom Error Types

```go
func TestAPIError_Response(t *testing.T) {
    tests := []struct {
        name       string
        err        error
        wantStatus int
        wantMsg    string
    }{
        {"not found", service.ErrNotFound, 404, "not found"},
        {"conflict", service.ErrConflict, 409, "already exists"},
        {"validation", service.ErrValidation, 400, "invalid input"},
        {"unauthorized", service.ErrUnauthorized, 401, "unauthorized"},
        {"internal", fmt.Errorf("unexpected"), 500, "internal server error"},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            status, msg := handler.MapErrorToResponse(tt.err)
            assert.Equal(t, tt.wantStatus, status)
            assert.Contains(t, msg, tt.wantMsg)
        })
    }
}
```

## Context and Cancellation Testing

```go
func TestService_RespectsContextCancellation(t *testing.T) {
    repo := new(MockUserRepository)
    svc := service.NewUserService(repo)

    ctx, cancel := context.WithCancel(context.Background())
    cancel() // Cancel immediately

    _, err := svc.GetByID(ctx, uuid.New())
    assert.ErrorIs(t, err, context.Canceled)
}

func TestService_RespectsContextTimeout(t *testing.T) {
    repo := new(MockUserRepository)
    repo.On("List", mock.Anything, mock.Anything).
        Run(func(args mock.Arguments) {
            time.Sleep(100 * time.Millisecond) // Simulate slow query
        }).
        Return(nil, 0, nil)

    svc := service.NewUserService(repo)

    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Millisecond)
    defer cancel()

    _, _, err := svc.List(ctx, model.ListOptions{})
    assert.ErrorIs(t, err, context.DeadlineExceeded)
}
```

## Test Organization

### File Structure

```
internal/
├── handler/
│   ├── user_handler.go
│   ├── user_handler_test.go      ← handler tests (httptest + mock service)
│   ├── project_handler.go
│   └── project_handler_test.go
├── service/
│   ├── user_service.go
│   ├── user_service_test.go      ← service tests (table-driven + mock repo)
│   ├── project_service.go
│   └── project_service_test.go
├── repository/
│   ├── user_repository.go
│   ├── user_repository_test.go   ← repo tests (sqlmock)
│   ├── project_repository.go
│   └── project_repository_test.go
├── middleware/
│   ├── auth.go
│   └── auth_test.go              ← middleware tests
├── model/
│   └── user.go                   ← no tests needed (pure structs)
└── testutil/
    ├── helpers.go                ← shared test utilities
    └── factories.go              ← test data factories
```

### Naming Conventions

| Convention | Example |
|-----------|---------|
| Test file | `user_service_test.go` (same dir as source) |
| Test function | `TestUserService_Create` (Type_Method) |
| Subtest name | `"success - creates user with valid input"` (outcome-based) |
| Mock type | `MockUserRepository` (Mock + interface name) |
| Test helper | `testutil.NewUser()` (in testutil package) |
| Helper function | Always call `t.Helper()` first line |

### Coverage Targets

| Package | Target | Rationale |
|---------|--------|-----------|
| `internal/service/` | **80%+** | Business logic, highest value |
| `internal/handler/` | **70%+** | HTTP layer, test all status codes |
| `internal/repository/` | **60%+** | Data layer, sqlmock or integration |
| `internal/middleware/` | **80%+** | Cross-cutting, every branch matters |
| `internal/model/` | **N/A** | Pure structs, no logic to test |
| `cmd/` | **N/A** | Wiring code, tested via integration |

## Race Condition Detection

Always run tests with the `-race` flag:

```bash
go test -v -race -cover ./...
```

### Common Race Conditions to Test For

1. **Shared map access** — concurrent writes to maps without sync.Mutex
2. **Goroutine leaks** — goroutines writing to channels after handler returns
3. **Shared state in tests** — t.Parallel() with shared variables
4. **Connection pool** — concurrent DB calls with shared connection

### Parallel Test Safety

```go
func TestConcurrentOperations(t *testing.T) {
    tests := []struct { ... }

    for _, tt := range tests {
        tt := tt // Capture range variable for parallel tests
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            // Each test gets its own mock instance
            repo := new(MockUserRepository)
            tt.mockFn(repo)
            // ... test logic
        })
    }
}
```

## Conventions

1. **Every test is self-contained** — no shared mutable state between tests
2. **Use `t.Parallel()` where safe** — tests without shared state should run in parallel
3. **Run with `-race` flag always** — detect data races early
4. **Mock at interface boundaries only** — don't mock internal functions
5. **Test error cases as thoroughly as success cases** — minimum 2 error tests per function
6. **Use `require` for fatal setup assertions** — fail fast if setup is broken
7. **Use `assert` for test assertions** — continue to collect multiple failures
8. **Always call `AssertExpectations`** — verify mocks received expected calls
9. **Use `t.Helper()` in all helper functions** — correct line numbers in test output
10. **Name subtests descriptively** — a failing test name should tell you what broke without reading code
11. **Clean up resources** — use `defer` for DB connections, temp files, test containers
12. **Tag integration tests** — use `testing.Short()` to skip slow tests in quick runs

## Knowledge Strategy

- **Patterns to capture:** Effective mock setups for complex interfaces, test helpers that reduce boilerplate, sqlmock query patterns for common SQL operations, testcontainer configurations that work reliably.
- **Examples to collect:** Well-structured table-driven tests with comprehensive edge cases, handler tests that properly validate response bodies, integration tests with realistic data.
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
