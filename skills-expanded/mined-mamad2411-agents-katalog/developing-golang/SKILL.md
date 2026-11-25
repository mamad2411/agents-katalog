---
name: developing-golang
description: Guides Go development with best practices from Google Style Guide and Effective Go. Use when go.mod is detected or Go code is being written. Covers naming, error handling, concurrency, testing, and project structure.
---

# Modern Go Development Guide

## 🎯 When to Use
- **Creating new Go projects**
- **Reviewing or improving existing Go code**
- **Implementing concurrency**
- **Designing error handling**
- **Writing Go tests**

## 📚 Document Structure

This skill consists of the following documents:

### 1. [Naming Conventions](references/NAMING.md)
Best practices for naming in Go:
- How to name packages
- Rules for variable and function names
- Interface naming (-er suffix)
- Philosophy of exported names

### 2. [Error Handling](references/ERROR-HANDLING.md)
Robust error handling patterns:
- Treating errors as values
- Error wrapping (%w vs %v)
- Sentinel errors and custom error types
- Proper use of panic/recover

### 3. [Concurrency](references/CONCURRENCY.md)
Powerful concurrency patterns in Go:
- Basics of goroutines
- Communication via channels
- Utilizing select statements
- Synchronization primitives (sync.Mutex, etc.)
- Cancellation with context

### 4. [Testing Strategy](references/TESTING.md)
How to write effective Go tests:
- Table-driven tests
- Distinguishing between t.Error and t.Fatal
- Subtests (t.Run)
- Benchmark tests
- Creating test helpers

### 5. [Project Structure](references/PROJECT-STRUCTURE.md)
Recommended directory layout:
- Distinguishing between cmd/ and internal/
- Proper use of pkg/
- Managing go.mod
- Module design

### 6. [Development Tooling](references/TOOLING.md)
Leveraging the Go ecosystem:
- gofmt / goimports
- golangci-lint
- go vet
- delve (debugger)
- Makefile patterns

## 🎯 Go Design Philosophy

### Prioritize Simplicity
```go
// Good: Simple and clear
func ProcessItems(items []Item) error {
    for _, item := range items {
        if err := item.Process(); err != nil {
            return fmt.Errorf("process item %s: %w", item.ID, err)
        }
    }
    return nil
}

// Bad: Over-abstraction
func ProcessItems(items []Item, processor ItemProcessor, validator ItemValidator) error {
    // Unnecessary complexity
}
```

### Be Explicit
```go
// Good: Explicit error handling
result, err := doSomething()
if err != nil {
    return err
}

// Bad: Ignoring errors
result, _ := doSomething()
```

### Share Memory by Communicating
```go
// Good: Communication via channels
results := make(chan Result)
go func() {
    results <- process(data)
}()
result := <-results

// Avoid: Communication by sharing memory (only when necessary)
var mu sync.Mutex
var shared int
```

## 🚀 Quick Start

### 1. Project Initialization
```bash
# Create module
mkdir my-project && cd my-project
go mod init github.com/username/my-project

# Basic structure
mkdir -p cmd/myapp internal/my-context-1/application internal/my-context-1/infrastructure internal/my-context-2/application internal/my-context-2/infrastructure
```

### 2. Basic main.go
```go
package main

import (
    "context"
    "log"
    "os"
    "os/signal"
    "syscall"
)

func main() {
    ctx, cancel := signal.NotifyContext(context.Background(),
        os.Interrupt, syscall.SIGTERM)
    defer cancel()

    if err := run(ctx); err != nil {
        log.Fatal(err)
    }
}

func run(ctx context.Context) error {
    // Application logic
    return nil
}
```

### 3. Development Commands
```bash
# Format
gofmt -w .

# Lint
golangci-lint run

# Test
go test ./...

# Build
go build -o bin/myapp ./cmd/myapp
```

## 💡 Key Principles

### Leverage Zero Values
```go
// Good: Valid state with zero values
type Counter struct {
    mu    sync.Mutex
    count int  // Zero value is 0, which is valid
}

func (c *Counter) Inc() {
    c.mu.Lock()
    c.count++
    c.mu.Unlock()
}

// Usable without explicit initialization
var c Counter
c.Inc()
```

### Keep Interfaces Small
```go
// Good: Single-method interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// Extend through composition
type ReadWriter interface {
    Reader
    Writer
}
```

### Early Return
```go
// Good: Early return with guard clauses
func process(item *Item) error {
    if item == nil {
        return errors.New("item is nil")
    }
    if item.ID == "" {
        return errors.New("item ID is empty")
    }

    // Main logic
    return item.Save()
}
```

## 📖 Reference Resources

- [Effective Go](https://go.dev/doc/effective_go)
- [Google Go Style Guide](https://google.github.io/styleguide/go/)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)

## 📖 Next Steps

1. **Newcomers**: Start with [Project Structure](references/PROJECT-STRUCTURE.md)
2. **Naming doubts**: Refer to [Naming Conventions](references/NAMING.md)
3. **Error handling**: Check patterns in [Error Handling](references/ERROR-HANDLING.md)
4. **Concurrency**: Learn goroutines/channels in [Concurrency](references/CONCURRENCY.md)
5. **Writing tests**: Use [Testing Strategy](references/TESTING.md) for table-driven tests
6. **Tool configuration**: Set up linting in [Development Tooling](references/TOOLING.md)
