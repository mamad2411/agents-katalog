---
name: golang-modules
description: "When to activate: Go modules, go.mod, go.sum, versioning, workspaces, private modules, dependency management"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: go
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Go Modules Patterns

## go.mod Structure

```
module github.com/myorg/myapp

go 1.23

require (
    github.com/gin-gonic/gin              v1.10.0
    github.com/jackc/pgx/v5              v5.6.0
    github.com/golang-jwt/jwt/v5         v5.2.1
    github.com/stretchr/testify          v1.9.0
    golang.org/x/crypto                  v0.24.0
)

require (
    // indirect dependencies (auto-managed)
    github.com/bytedance/sonic v1.11.6 // indirect
)
```

## Common go Commands

```bash
# Initialize a new module
go mod init github.com/myorg/myapp

# Add a dependency (downloads and updates go.mod)
go get github.com/gin-gonic/gin@v1.10.0

# Upgrade all dependencies to latest minor/patch
go get -u ./...

# Tidy: remove unused, add missing
go mod tidy

# Vendor dependencies for reproducible offline builds
go mod vendor

# Show module dependency graph
go mod graph | head -20

# Verify checksums in go.sum
go mod verify

# Download all dependencies
go mod download

# Show why a package is needed
go mod why github.com/some/pkg
```

## Version Pinning

```bash
# Exact version
go get github.com/some/pkg@v1.2.3

# Latest patch in v1.2.x
go get github.com/some/pkg@v1.2

# Specific commit
go get github.com/some/pkg@abc1234

# Latest pre-release
go get github.com/some/pkg@latest

# Downgrade
go get github.com/some/pkg@v1.1.0
```

## Go Workspaces (go.work)

Workspaces let you develop multiple modules simultaneously without replace directives.

```bash
# Create workspace
go work init ./myapp ./mylib

# Add module to workspace
go work use ./another-module
```

```
# go.work
go 1.23

use (
    ./myapp
    ./mylib
    ./another-module
)
```

## Replace Directives

```go
// go.mod — for local development only; don't commit replaces to libraries
replace (
    github.com/myorg/mylib => ../mylib                 // local path
    github.com/some/buggy  => github.com/fork/fixed v1.2.3  // fork
)
```

## Private Modules

```bash
# Tell go not to use public proxy for private modules
GONOSUMCHECK=github.com/myorg/*
GONOSUMDB=github.com/myorg/*
GOPRIVATE=github.com/myorg/*

# Or set in ~/.config/go/env
go env -w GOPRIVATE=github.com/myorg/*
go env -w GONOSUMDB=github.com/myorg/*
```

## Multi-Module Repository

```
monorepo/
├── go.work            # workspace file
├── svc-user/
│   ├── go.mod         # module github.com/myorg/svc-user
│   └── cmd/server/
├── svc-order/
│   ├── go.mod         # module github.com/myorg/svc-order
│   └── cmd/server/
└── shared/
    ├── go.mod         # module github.com/myorg/shared
    └── pkg/
```

## Common Anti-Patterns

- **`go get` without version** — always pin a version; `@latest` can break builds
- **Committing `replace` directives in library `go.mod`** — they affect all consumers; use workspaces instead
- **Not running `go mod tidy`** — go.sum and go.mod drift; run in CI
- **Checking in `vendor/` alongside `go.sum`** — pick one strategy; both together causes confusion
- **`GOPATH` mode** — Go modules are the standard; never use `GO111MODULE=off` in new projects
