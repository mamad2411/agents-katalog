---
name: golang-testing
description: Comprehensive testing strategies for test-driven development and ensuring high quality Go code.
---

# Go Testing

Comprehensive testing strategies for TDD and ensuring high quality Go code.

## When to Activate

- Writing new Go code
- Reviewing Go code
- Improving existing tests
- Increasing test coverage
- Debugging and bug fixing

## Core Principles

### 1. Test-Driven Development (TDD)

Follow the cycle: write a failing test, implement, refactor.

```go
// 1. Write the test (it fails)
func TestCalculateTotal(t *testing.T) {
    total := CalculateTotal([]float64{10.0, 20.0, 30.0})
    want := 60.0
    if total != want {
        t.Errorf("got %f, want %f", total, want)
    }
}

// 2. Implement (make the test pass)
func CalculateTotal(prices []float64) float64 {
    var total float64
    for _, price := range prices {
        total += price
    }
    return total
}

// 3. Refactor — improve without breaking tests
```

### 2. Table-Driven Tests

Systematically test multiple cases.

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name string
        a, b int
        want int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -2, -3, -5},
        {"mixed signs", -2, 3, 1},
        {"zeros", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := Add(tt.a, tt.b)
            if got != tt.want {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, got, tt.want)
            }
        })
    }
}
```

### 3. Subtests

Organize tests logically with subtests.

```go
func TestUser(t *testing.T) {
    t.Run("validation", func(t *testing.T) {
        t.Run("empty email", func(t *testing.T) {
            user := User{Email: ""}
            if err := user.Validate(); err == nil {
                t.Error("expected validation error")
            }
        })

        t.Run("valid email", func(t *testing.T) {
            user := User{Email: "test@example.com"}
            if err := user.Validate(); err != nil {
                t.Errorf("unexpected error: %v", err)
            }
        })
    })
}
```

## Test Organization

### File Structure

```text
mypackage/
├── user.go
├── user_test.go          # Unit tests
├── integration_test.go   # Integration tests
├── testdata/             # Test fixtures
│   ├── valid_user.json
│   └── invalid_user.json
└── export_test.go        # Exported internals for testing
```

### Test Packages

```go
// user_test.go — same package (white-box testing)
package user

func TestInternalFunction(t *testing.T) {
    // Can test internals
}

// user_external_test.go — external package (black-box testing)
package user_test

import "myapp/user"

func TestPublicAPI(t *testing.T) {
    // Test public API only
}
```

## Assertions and Helpers

### Custom Helper Functions

```go
func assertEqual(t *testing.T, got, want interface{}) {
    t.Helper()
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
}

func assertNoError(t *testing.T, err error) {
    t.Helper()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}
```

### Deep Equality

```go
import "reflect"

func assertDeepEqual(t *testing.T, got, want interface{}) {
    t.Helper()
    if !reflect.DeepEqual(got, want) {
        t.Errorf("got %+v, want %+v", got, want)
    }
}
```

## Mocking and Stubs

### Interface-Based Mocks

```go
// Production code
type UserStore interface {
    GetUser(id string) (*User, error)
    SaveUser(user *User) error
}

// Test code
type MockUserStore struct {
    users map[string]*User
    err   error
}

func (m *MockUserStore) GetUser(id string) (*User, error) {
    if m.err != nil {
        return nil, m.err
    }
    return m.users[id], nil
}

func (m *MockUserStore) SaveUser(user *User) error {
    if m.err != nil {
        return m.err
    }
    m.users[user.ID] = user
    return nil
}
```

### Mocking Time

```go
type TimeProvider interface {
    Now() time.Time
}

type RealTime struct{}
func (RealTime) Now() time.Time { return time.Now() }

type MockTime struct{ current time.Time }
func (m MockTime) Now() time.Time { return m.current }

func TestTimeDependent(t *testing.T) {
    mockTime := MockTime{
        current: time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC),
    }
    service := &Service{time: mockTime}
    // Test with fixed time...
}
```

### HTTP Client Mocking

```go
type HTTPClient interface {
    Do(req *http.Request) (*http.Response, error)
}

type MockHTTPClient struct {
    response *http.Response
    err      error
}

func (m *MockHTTPClient) Do(req *http.Request) (*http.Response, error) {
    return m.response, m.err
}
```

## HTTP Handler Testing

### Using httptest

```go
func TestHandler(t *testing.T) {
    handler := http.HandlerFunc(MyHandler)

    req := httptest.NewRequest("GET", "/users/123", nil)
    rec := httptest.NewRecorder()

    handler.ServeHTTP(rec, req)

    if rec.Code != http.StatusOK {
        t.Errorf("got status %d, want %d", rec.Code, http.StatusOK)
    }

    var response map[string]interface{}
    json.NewDecoder(rec.Body).Decode(&response)

    if response["id"] != "123" {
        t.Errorf("got id %v, want 123", response["id"])
    }
}
```

### Middleware Testing

```go
func TestAuthMiddleware(t *testing.T) {
    nextHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    })

    handler := AuthMiddleware(nextHandler)

    tests := []struct {
        name       string
        token      string
        wantStatus int
    }{
        {"valid token", "valid-token", http.StatusOK},
        {"invalid token", "invalid", http.StatusUnauthorized},
        {"no token", "", http.StatusUnauthorized},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest("GET", "/", nil)
            if tt.token != "" {
                req.Header.Set("Authorization", "Bearer "+tt.token)
            }
            rec := httptest.NewRecorder()
            handler.ServeHTTP(rec, req)

            if rec.Code != tt.wantStatus {
                t.Errorf("got status %d, want %d", rec.Code, tt.wantStatus)
            }
        })
    }
}
```

## Database Testing

### Transaction-Based Test Isolation

```go
func TestUserRepository(t *testing.T) {
    db := setupTestDB(t)
    defer db.Close()

    tests := []struct {
        name string
        fn   func(*testing.T, *sql.DB)
    }{
        {"create user", testCreateUser},
        {"find user", testFindUser},
        {"update user", testUpdateUser},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            tx, err := db.Begin()
            if err != nil {
                t.Fatal(err)
            }
            defer tx.Rollback() // Rollback after test

            tt.fn(t, tx)
        })
    }
}
```

## Benchmarks

```go
func BenchmarkCalculation(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Calculate(100)
    }
}

func BenchmarkWithAllocs(b *testing.B) {
    b.ReportAllocs()
    for i := 0; i < b.N; i++ {
        ProcessData([]byte("test data"))
    }
}
```

## Fuzz Testing (Go 1.18+)

```go
func FuzzParseInput(f *testing.F) {
    f.Add("hello")
    f.Add("world")
    f.Add("123")

    f.Fuzz(func(t *testing.T, input string) {
        result, err := ParseInput(input)
        if err == nil && result == nil {
            t.Error("got nil result with no error")
        }
    })
}
```

## Integration Tests with Build Tags

```go
//go:build integration

package myapp_test

func TestDatabaseIntegration(t *testing.T) {
    // Tests that require a real DB
}
```

```bash
# Run integration tests
go test -tags=integration ./...

# Exclude integration tests
go test ./...
```

## Test Commands

```bash
# Basic tests
go test ./...
go test -v ./...                    # Verbose output
go test -run TestSpecific ./...     # Run specific test

# Coverage
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out -o coverage.html

# Race detection
go test -race ./...

# Benchmarks
go test -bench=. -benchmem ./...

# Fuzzing
go test -fuzz=FuzzTest

# JSON format (CI integration)
go test -json ./...
```

---

**Remember**: Tests are not optional. They are the safety net that enables confident refactoring, rapid development, and production reliability.
