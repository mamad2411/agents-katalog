---
name: "lang-go"
description: "Provides software engineering patterns in Go (Golang) based on the official documentation (go.dev/doc), Effective Go, the Go Memory Model, and concurrency best practices (goroutines, channels, context), error handling, generics, modules, and testing."
---

# AI Skill: Go Engineering (Go Specialist)

This skill guides the AI to act as a specialist in the **Go (Golang)** language, following strictly the guidelines of the official documentation ([go.dev/doc](https://go.dev/doc/)), the **Effective Go** guide, and the Go memory model. The goal is to create idiomatic, concurrent, high-performance, easily maintainable, and heavily tested code.

---

## 🧭 General Go Development Guidelines

While working under this skill, apply the following idiomatic language principles strictly:

### 1. Style, Naming, and Formatting (Effective Go)
- **`gofmt` Mandatory**: All Go code must be formatted using the official `gofmt` or `goimports` tool.
- **Simple, Short Naming**:
  - Local variables should have short, direct names (e.g., `i` for index, `r` for io.Reader, `err` for error).
  - Use `MixedCaps` or `camelCase` (never `snake_case`). An uppercase first letter exports the identifier outside the package; lowercase keeps access private.
- **Small, Composable Interfaces**: Prefer lean interfaces with one or two methods (`io.Reader`, `io.Writer`, `fmt.Stringer`). Implementation is implicit (static duck typing).
- **No Noisy Getters**: Do not prefix methods with `Get`. The getter for the `user` field should be named just `User()`.

### 2. Idiomatic Error Handling
- **Errors as Explicit Values**: Handle errors explicitly right after the call (`if err != nil`). Never ignore errors with the blank identifier `_` without a documented reason.
- **Error Wrapping and Inspection (Go 1.13+)**:
  - Wrap context onto errors using `fmt.Errorf("failed to process order %d: %w", orderID, err)`.
  - Inspect the cause chain with `errors.Is(err, ErrNotFound)` and extract types with `errors.As(err, &customErr)`.
- **Restricted Use of `panic` and `recover`**: Reserve `panic` for unrecoverable errors during application initialization only. In libraries and production code, return `error`.

### 3. Concurrency and the Memory Model
- **"Do not communicate by sharing memory; instead, share memory by communicating."**:
  - Prefer channels (`channels`) and `goroutines` to pass data and coordinate tasks across processes.
- **Lifecycle Management with `context.Context`**:
  - Pass `ctx context.Context` as the first parameter in I/O, database, or RPC calls to control timeouts and cancel propagation.
- **Primitive Synchronization**:
  - Use `sync.WaitGroup` to wait for a group of goroutines to finish.
  - Protect concurrent access to shared structures using `sync.Mutex` or `sync.RWMutex`.
- **Data Race Prevention**: Always validate concurrency by running tests with the `-race` flag (`go test -race`).

### 4. Generics (Go 1.18+)
- Use type parameters (`[T any]`, `[T comparable]`) when the logic is generic across data structures (queues, stacks, trees) or utility algorithms.
- Do not replace behavior-oriented interfaces with unnecessary generics.

---

## 🛠️ Project Structure and the Go Ecosystem

### 1. Repository Organization (Standard Go Project Layout)
- **Go Modules (`go.mod`)**: Every application or library must use native modules.
- **Recommended Directory Structure**:
  - `cmd/`: Binaries and entry points (`main.go`).
  - `internal/`: Application-private code that must not be imported by other projects.
  - `pkg/`: Public code reusable by third parties.
  - `api/`: OpenAPI contract definitions, gRPC/Protobuf schemas.

### 2. Established Frameworks and Libraries
- **Web APIs and Routers**: native `net/http` (with the Go 1.22+ improvements), `chi`, `gin`, `echo`, `fiber`.
- **Databases and ORM**: `database/sql`, `pgx`, `sqlx`, `gorm`, `ent`, `sqlc`.
- **CLIs and Automation**: `cobra`, `viper`.
- **RPC Communication**: `gRPC` and `protocol buffers`.

---

## 🧰 Recommended Code Patterns

### 1. Idiomatic HTTP Handler with Context and JSON (Go 1.22+)
```go
package user

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"strconv"
)

type UserService interface {
	FindByID(ctx context.Context, id int64) (*User, error)
}

type Handler struct {
	service UserService
}

func NewHandler(s UserService) *Handler {
	return &Handler{service: s}
}

func (h *Handler) GetUser(w http.ResponseWriter, r *http.Request) {
	idStr := r.PathValue("id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		http.Error(w, "ID inválido", http.StatusBadRequest)
		return
	}

	user, err := h.service.FindByID(r.Context(), id)
	if err != nil {
		if errors.Is(err, ErrNotFound) {
			http.Error(w, "Usuário não encontrado", http.StatusNotFound)
			return
		}
		http.Error(w, "Erro interno de processamento", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(user)
}
```

### 2. Concurrent Worker Pool with Channels and WaitGroup
```go
package worker

import (
	"context"
	"fmt"
	"sync"
)

type Job struct {
	ID   int
	Data string
}

func ProcessJobs(ctx context.Context, jobs []Job, numWorkers int) {
	jobChan := make(chan Job, len(jobs))
	var wg sync.WaitGroup

	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for {
				select {
				case <-ctx.Done():
					fmt.Printf("Worker %d interrompido pelo contexto\n", workerID)
					return
				case job, ok := <-jobChan:
					if !ok {
						return
					}
					fmt.Printf("Worker %d processando job %d: %s\n", workerID, job.ID, job.Data)
				}
			}
		}(i)
	}

	for _, j := range jobs {
		jobChan <- j
	}
	close(jobChan)

	wg.Wait()
}
```

### 3. Table-Driven Testing
```go
package calc_test

import (
	"testing"
	"myproject/calc"
)

func TestDivide(t *testing.T) {
	tests := []struct {
		name        string
		a, b        float64
		want        float64
		wantErr     bool
	}{
		{name: "divisão exata", a: 10, b: 2, want: 5, wantErr: false},
		{name: "divisão por zero", a: 10, b: 0, want: 0, wantErr: true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := calc.Divide(tt.a, tt.b)
			if (err != nil) != tt.wantErr {
				t.Fatalf("Divide(%f, %f) erro inesperado = %v, wantErr %v", tt.a, tt.b, err, tt.wantErr)
			}
			if got != tt.want {
				t.Errorf("Divide(%f, %f) = %f, esperava %f", tt.a, tt.b, got, tt.want)
			}
		})
	}
}
```

---

## 🔒 Security Issues and Safe Practices

- **Goroutine Leaks and Race Conditions**: Always use Go's race detector (`go test -race`) during the test cycle. Make sure every goroutine has a clear termination condition to prevent memory leaks.
- **Unsafe Manipulation (`unsafe` Package)**: Minimize use of the `unsafe` package. Arbitrary memory casts bypass Go's type safety and can lead to unexpected memory corruption.
- **Secret Generation**: Never use `math/rand` to generate tokens, passwords, or session identifiers. Always use `crypto/rand` for cryptographically secure value generation.
- **Command Injection in Processes**: When using `os/exec`, avoid passing concatenated strings directly to shells such as `sh` or `bash`. Supply arguments as separate slices (`[]string`).

## 🔗 Integration with Other Skills

- To build automation tools, scanning tools, or pentest scripts in Go, see [pentest-scripter-python-bash-go](../../security/appsec/pentest-scripter-python-bash-go/SKILL.md).
- To integrate concurrent and transactional database calls in Go (`database/sql`, `pgx`, `gorm`, `sqlc`), see [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md), [db-postgresql](../../data/db-postgresql/SKILL.md), [db-mariadb](../../data/db-mariadb/SKILL.md), [db-sqlite](../../data/db-sqlite/SKILL.md), and [db-mongodb](../../data/db-mongodb/SKILL.md).
- To apply static code analysis and security to Go web services, see [sast-code-review](../../security/appsec/sast-code-review/SKILL.md) and [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
- To design scalable microservice architectures in Go, see [software-architect](../../roles/software-architect/SKILL.md).
