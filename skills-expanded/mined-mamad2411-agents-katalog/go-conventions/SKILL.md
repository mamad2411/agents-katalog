---
name: go-conventions
description:
  This skill should be used when working on Go projects, writing Go code, running Go tests, managing
  Go dependencies, or reviewing Go code.
version: 0.1.0
---

# Go Conventions and Idiomatic Patterns

This skill defines comprehensive conventions for writing idiomatic Go code following community best
practices and the official Go team guidelines.

## Error Handling

### Always Check Errors

Every error must be checked. Ignoring errors leads to subtle bugs and production failures.

```go
// CORRECT: Check all errors
file, err := os.Open("config.json")
if err != nil {
    return fmt.Errorf("failed to open config: %w", err)
}
defer file.Close()

data, err := io.ReadAll(file)
if err != nil {
    return fmt.Errorf("failed to read config: %w", err)
}
```

```go
// WRONG: Ignoring errors
file, _ := os.Open("config.json")
data, _ := io.ReadAll(file)
```

#### Error Wrapping with fmt.Errorf and %w

Wrap errors to add context while preserving the error chain for errors.Is and errors.As.

```go
// CORRECT: Wrap errors with %w
func loadUser(id string) (*User, error) {
    data, err := db.Query(id)
    if err != nil {
        return nil, fmt.Errorf("load user %s: %w", id, err)
    }
    return parseUser(data)
}
```

```go
// WRONG: Losing error chain with %v
func loadUser(id string) (*User, error) {
    data, err := db.Query(id)
    if err != nil {
        return nil, fmt.Errorf("load user %s: %v", id, err)
    }
    return parseUser(data)
}
```

#### Sentinel Errors

Define sentinel errors as package-level variables for expected error conditions.

```go
// CORRECT: Sentinel errors for known conditions
var (
    ErrNotFound     = errors.New("resource not found")
    ErrUnauthorized = errors.New("unauthorized access")
    ErrInvalidInput = errors.New("invalid input")
)

func GetUser(id string) (*User, error) {
    if id == "" {
        return nil, ErrInvalidInput
    }
    user, err := db.Find(id)
    if err != nil {
        return nil, err
    }
    if user == nil {
        return nil, ErrNotFound
    }
    return user, nil
}
```

```go
// WRONG: Creating new error instances
func GetUser(id string) (*User, error) {
    if id == "" {
        return nil, errors.New("invalid input")  // Not comparable
    }
    return db.Find(id)
}
```

#### Use errors.Is and errors.As

Check for specific errors using errors.Is and extract error types with errors.As.

```go
// CORRECT: Using errors.Is and errors.As
func handleError(err error) {
    if errors.Is(err, ErrNotFound) {
        log.Println("resource not found")
        return
    }

    var validationErr *ValidationError
    if errors.As(err, &validationErr) {
        log.Printf("validation failed: %v", validationErr.Fields)
        return
    }

    log.Printf("unexpected error: %v", err)
}
```

```go
// WRONG: Direct comparison loses wrapped context
func handleError(err error) {
    if err == ErrNotFound {  // Fails if error is wrapped
        log.Println("not found")
    }
}
```

#### Return Errors, Do Not Panic

Panics should only be used for programming errors, not for expected error conditions.

```go
// CORRECT: Return errors for expected failures
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}
```

```go
// WRONG: Panic for expected conditions
func divide(a, b int) int {
    if b == 0 {
        panic("division by zero")  // Don't panic on expected errors
    }
    return a / b
}
```

## Code Style and Formatting

### Use gofumpt for Formatting

Always format code with gofumpt, which is stricter than gofmt.

```bash
# Install gofumpt
go install mvdan.cc/gofumpt@latest

# Format all files
gofumpt -l -w .
```

```go
// CORRECT: gofumpt style
package main

import (
    "context"
    "fmt"
)

type Config struct {
    Host string
    Port int
}
```

#### Run golangci-lint

Use golangci-lint with a comprehensive configuration for static analysis.

```bash
# Install golangci-lint
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Run linter
golangci-lint run ./...
```

```toml
# .golangci.yml recommended configuration
linters:
  enable:
    - errcheck
    - gosimple
    - govet
    - ineffassign
    - staticcheck
    - unused
    - gofumpt
    - revive
    - gosec
```

#### Prefer Standard Library

Use the standard library when possible before adding external dependencies.

```go
// CORRECT: Use stdlib encoding/json
import "encoding/json"

func parseConfig(data []byte) (*Config, error) {
    var cfg Config
    if err := json.Unmarshal(data, &cfg); err != nil {
        return nil, err
    }
    return &cfg, nil
}
```

```go
// WRONG: Unnecessary dependency for basic JSON
import "github.com/goccy/go-json"  // Only if performance critical
```

#### Context First Parameter

Always pass context.Context as the first parameter in functions that may block or need cancellation.

```go
// CORRECT: Context as first parameter
func FetchUser(ctx context.Context, id string) (*User, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", "/users/"+id, nil)
    if err != nil {
        return nil, err
    }

    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    var user User
    if err := json.NewDecoder(resp.Body).Decode(&user); err != nil {
        return nil, err
    }
    return &user, nil
}
```

```go
// WRONG: Context not first or missing
func FetchUser(id string, ctx context.Context) (*User, error) {  // Wrong order
    // ...
}

func FetchUser(id string) (*User, error) {  // Missing context
    req, _ := http.NewRequest("GET", "/users/"+id, nil)
    // ...
}
```

#### Short Receiver Names

Use short, consistent receiver names (one or two letters), typically the first letter of the type.

```go
// CORRECT: Short receiver names
type User struct {
    ID   string
    Name string
}

func (u *User) SetName(name string) {
    u.Name = name
}

func (u *User) Validate() error {
    if u.ID == "" {
        return errors.New("ID required")
    }
    return nil
}
```

```go
// WRONG: Long or inconsistent receiver names
func (user *User) SetName(name string) {  // Too long
    user.Name = name
}

func (this *User) Validate() error {  // Don't use "this" or "self"
    return nil
}
```

#### Verb-er Interface Naming

Name interfaces with an -er suffix describing their behavior.

```go
// CORRECT: Verb-er interface names
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type Closer interface {
    Close() error
}

type UserFetcher interface {
    FetchUser(ctx context.Context, id string) (*User, error)
}
```

```go
// WRONG: Poor interface naming
type ReaderInterface interface {  // Redundant "Interface"
    Read(p []byte) (n int, err error)
}

type IReader interface {  // Don't use "I" prefix
    Read(p []byte) (n int, err error)
}
```

#### Unexported by Default

Start with unexported types and functions. Only export what consumers need.

```go
// CORRECT: Unexported internals, exported API
package config

type Config struct {  // Exported
    settings map[string]string  // Unexported field
}

func Load(path string) (*Config, error) {  // Exported
    return parseFile(path)
}

func parseFile(path string) (*Config, error) {  // Unexported
    // ...
    return &Config{settings: make(map[string]string)}, nil
}
```

```go
// WRONG: Over-exporting internals
type Config struct {
    Settings map[string]string  // Don't expose internal state
}

func ParseFile(path string) (*Config, error) {  // Don't export if only used internally
    // ...
}
```

#### Iota Pattern for Constants

Use iota for enumerated constants with clear zero values.

```go
// CORRECT: iota with explicit zero value
type Status int

const (
    StatusUnknown Status = iota  // 0 is explicit unknown/unset
    StatusPending
    StatusActive
    StatusInactive
)

func (s Status) String() string {
    switch s {
    case StatusPending:
        return "pending"
    case StatusActive:
        return "active"
    case StatusInactive:
        return "inactive"
    default:
        return "unknown"
    }
}
```

```go
// WRONG: Missing zero value consideration
const (
    StatusActive Status = iota  // 0 is "active"? Unclear
    StatusInactive
)
```

#### Struct Embedding for Composition

Use struct embedding to compose behavior, not for inheritance.

```go
// CORRECT: Embedding for composition
type Logger interface {
    Log(msg string)
}

type Service struct {
    Logger  // Embedded interface
    db      *sql.DB
}

func (s *Service) Process(ctx context.Context) error {
    s.Log("starting process")  // Delegated to embedded Logger
    return s.db.PingContext(ctx)
}
```

```go
// WRONG: Embedding just to avoid typing
type Service struct {
    *sql.DB  // Don't embed concrete types unless clear benefit
}
```

## Tooling and Development Workflow

### Use Task (Taskfile)

Prefer Task over Makefiles for Go projects. Task uses YAML and has better cross-platform support.

```yaml
# Taskfile.yml
version: '3'

tasks:
  build:
    desc: Build the application
    cmds:
      - go build -o bin/app ./cmd/app

  test:
    desc: Run tests
    cmds:
      - go test -v -race -coverprofile=coverage.out ./...

  lint:
    desc: Run linters
    cmds:
      - golangci-lint run ./...
      - gofumpt -l -w .

  tidy:
    desc: Tidy dependencies
    cmds:
      - go mod tidy
      - go mod verify

  vuln:
    desc: Check for vulnerabilities
    cmds:
      - govulncheck ./...

  default:
    desc: Run all checks
    cmds:
      - task: lint
      - task: test
      - task: build
```

```bash
# Run tasks
task          # Run default task
task test     # Run specific task
task -l       # List all tasks
```

#### gofumpt for Stricter Formatting

Use gofumpt instead of gofmt for more opinionated formatting.

```bash
# Format and check
gofumpt -l -w .

# In CI, check formatting
gofumpt -l . | grep . && exit 1 || exit 0
```

#### golangci-lint Configuration

Configure golangci-lint with appropriate linters for your project.

```yaml
# .golangci.yml
linters-settings:
  errcheck:
    check-blank: true
  govet:
    enable-all: true
  revive:
    rules:
      - name: exported
        severity: warning

linters:
  enable:
    - errcheck
    - gosimple
    - govet
    - ineffassign
    - staticcheck
    - unused
    - gofumpt
    - revive
    - gosec
    - misspell
    - unconvert
    - unparam

run:
  timeout: 5m
  tests: true
```

#### go mod tidy

Always run go mod tidy to clean up dependencies.

```bash
# Clean dependencies
go mod tidy

# Verify checksums
go mod verify

# Explain why dependency is needed
go mod why github.com/pkg/errors
```

#### govulncheck for Security

Regularly check for known vulnerabilities in dependencies.

```bash
# Install govulncheck
go install golang.org/x/vuln/cmd/govulncheck@latest

# Check for vulnerabilities
govulncheck ./...

# In CI
govulncheck -test ./...
```

## go generate Hygiene

### Generated File Headers

Always add clear headers to generated files indicating they are auto-generated.

```go
// CORRECT: Clear generated file header
// Code generated by generate.go; DO NOT EDIT.

package models

type User struct {
    ID   string
    Name string
}
```

```bash
# Generate command
go generate ./...
```

#### Commit Generated Files

Commit generated files to version control for reproducible builds.

```bash
# Generate before commit
go generate ./...
git add .
git commit -m "chore: regenerate mocks and code"
```

```gitignore
# WRONG: Don't ignore generated files in most cases
# *_generated.go  # Usually should be committed
```

#### CI Verification

Verify generated files are up-to-date in CI.

```bash
# CI script to verify generation
go generate ./...
git diff --exit-code || (echo "Generated files out of date" && exit 1)
```

```yaml
# GitHub Actions example
- name: Verify generated files
  run: |
    go generate ./...
    git diff --exit-code
```

## Existing Repository Compatibility

### Respect Established Toolchain

When contributing to existing repositories, respect their established conventions.

```go
// Check existing patterns
// - Look at go.mod for Go version
// - Check for Makefile or Taskfile.yml
// - Review .golangci.yml configuration
// - Follow existing error handling patterns
// - Match existing test structure
```

```bash
# Discover project conventions
cat go.mod                # Check Go version
cat Taskfile.yml          # Or Makefile
cat .golangci.yml         # Linter config
ls cmd/                   # Entry points
ls internal/              # Internal packages
```

#### Match Existing Code Style

Analyze existing code patterns before making changes.

```go
// If project uses:
// - Custom logger -> use it
// - Specific error wrapping -> follow it
// - Test helpers -> reuse them
// - Mocking library -> use same library

// CORRECT: Follow project patterns
// If project uses zerolog:
import "github.com/rs/zerolog/log"

func Process() {
    log.Info().Msg("processing")  // Match existing style
}
```

```go
// WRONG: Introducing new patterns without discussion
import "log/slog"  // Don't introduce new logger if project uses zerolog

func Process() {
    slog.Info("processing")  // Inconsistent with project
}
```

## Package Organization

### Internal Package for Private Code

Use internal/ directory for code that should not be imported by external modules.

```text
myapp/
  cmd/
    myapp/
      main.go
  internal/
    service/
      user.go
    repository/
      postgres.go
  pkg/
    client/
      client.go
  go.mod
```

```go
// internal/service/user.go - Cannot be imported outside module
package service

type UserService struct{}
```

#### cmd Directory for Entry Points

Place main packages in cmd/ directory with subdirectories for each binary.

```text
cmd/
  server/
    main.go
  worker/
    main.go
  migrate/
    main.go
```

```go
// CORRECT: cmd/server/main.go
package main

import "myapp/internal/service"

func main() {
    svc := service.New()
    svc.Start()
}
```

## Naming Conventions

### Use MixedCaps

Use MixedCaps or mixedCaps, not underscores, for multi-word names.

```go
// CORRECT: MixedCaps naming
type UserService struct{}

func (s *UserService) GetUserByID(id string) (*User, error) {
    return s.repo.FindByID(id)
}

var errNotFound = errors.New("not found")
```

```go
// WRONG: Underscores in names
type User_Service struct{}  // Wrong

func (s *User_Service) Get_User_By_ID(id string) (*User, error) {  // Wrong
    return nil, nil
}

var err_not_found = errors.New("not found")  // Wrong
```

#### Package Names

Package names should be short, concise, and lowercase without underscores.

```go
// CORRECT: Good package names
package user
package httputil
package ioutil
```

```go
// WRONG: Poor package names
package user_service  // No underscores
package userService   // No mixed caps
package utils         // Too generic
```

## Concurrency Patterns

### Always Close Channels from Sender

The sender should close channels, not the receiver.

```go
// CORRECT: Sender closes channel
func produce(n int) <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)  // Sender closes
        for i := 0; i < n; i++ {
            ch <- i
        }
    }()
    return ch
}

func consume() {
    for v := range produce(10) {  // Receiver just ranges
        fmt.Println(v)
    }
}
```

```go
// WRONG: Receiver closing channel
func consume(ch chan int) {
    for v := range ch {
        fmt.Println(v)
    }
    close(ch)  // Wrong: receiver shouldn't close
}
```

#### Use sync.WaitGroup for Goroutine Coordination

Use sync.WaitGroup to wait for multiple goroutines to complete.

```go
// CORRECT: WaitGroup for coordination
func processBatch(items []Item) error {
    var wg sync.WaitGroup
    errCh := make(chan error, len(items))

    for _, item := range items {
        wg.Add(1)
        go func(item Item) {
            defer wg.Done()
            if err := process(item); err != nil {
                errCh <- err
            }
        }(item)
    }

    wg.Wait()
    close(errCh)

    for err := range errCh {
        if err != nil {
            return err
        }
    }
    return nil
}
```

#### Context for Cancellation

Use context for cancellation and timeout control in concurrent operations.

```go
// CORRECT: Context-aware goroutines
func worker(ctx context.Context, jobs <-chan Job) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case job, ok := <-jobs:
            if !ok {
                return nil
            }
            if err := processJob(ctx, job); err != nil {
                return err
            }
        }
    }
}
```

## Performance Considerations

### Preallocate Slices When Size Known

Preallocate slices when the final size is known to avoid reallocations.

```go
// CORRECT: Preallocate slice
func transform(input []int) []int {
    result := make([]int, 0, len(input))  // Preallocate capacity
    for _, v := range input {
        result = append(result, v*2)
    }
    return result
}
```

```go
// WRONG: No preallocation
func transform(input []int) []int {
    var result []int  // Will reallocate multiple times
    for _, v := range input {
        result = append(result, v*2)
    }
    return result
}
```

#### Use strings.Builder for String Concatenation

Use strings.Builder for efficient string building instead of concatenation.

```go
// CORRECT: strings.Builder
func buildMessage(parts []string) string {
    var b strings.Builder
    b.Grow(len(parts) * 10)  // Estimate size
    for i, part := range parts {
        if i > 0 {
            b.WriteString(", ")
        }
        b.WriteString(part)
    }
    return b.String()
}
```

```go
// WRONG: String concatenation
func buildMessage(parts []string) string {
    msg := ""
    for i, part := range parts {
        if i > 0 {
            msg += ", "  // Creates new string each time
        }
        msg += part
    }
    return msg
}
```

## Documentation

### Document All Exported Items

All exported functions, types, constants, and variables must have documentation comments.

```go
// CORRECT: Documented exports
// User represents a user in the system.
type User struct {
    // ID is the unique identifier for the user.
    ID string
    // Name is the user's display name.
    Name string
}

// NewUser creates a new User with the given ID and name.
func NewUser(id, name string) *User {
    return &User{ID: id, Name: name}
}
```

```go
// WRONG: Missing documentation
type User struct {  // No doc comment
    ID   string
    Name string
}

func NewUser(id, name string) *User {  // No doc comment
    return &User{ID: id, Name: name}
}
```

#### Package Documentation

Every package should have a package comment describing its purpose.

```go
// CORRECT: Package documentation
// Package user provides user management functionality.
//
// It includes user creation, validation, and persistence operations.
// Use NewService to create a user service instance.
package user
```

This skill ensures Go code follows community best practices, is maintainable, performant, and
idiomatic. Apply these rules consistently across all Go projects.
