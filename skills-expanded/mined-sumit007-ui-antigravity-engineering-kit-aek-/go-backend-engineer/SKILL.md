---
name: go-backend-engineer
description: Architect and implement high-throughput distributed microservices, REST/gRPC backends, and concurrent pipelines in Go. Enforces context propagation and goroutine leak prevention.
---

# Go Backend Engineer Skill

## Purpose
Enforces idiomatic Go practices for microservices, database transactions, HTTP/gRPC services, and concurrent systems.

## When to Use
- Developing or maintaining backend services in Go.
- Optimizing database queries, connection pools, and migration scripts.
- Debugging race conditions, deadlock risks, or goroutine leaks.

## Engineering Workflow
1. **Service Structuring**: Package by feature or domain, keeping `main.go` minimal.
2. **Context Propagation**: Always pass `ctx context.Context` as the first argument in I/O operations.
3. **Graceful Shutdown**: Intercept `os.Interrupt` / `syscall.SIGTERM` and drain active requests before exit.
4. **Verification**:
   - `golangci-lint run`
   - `go test -race -v ./...`

