---
name: toolchain-go
description: "Go project toolchain -- build, test, lint, module management, and debugging."
metadata: {"thinkfleetbot":{"emoji":"🔵","requires":{"bins":["go"]}}}
---

# Go Toolchain

Common commands for Go projects.

## Build & run

```bash
go build ./...
go run .
go run cmd/server/main.go
```

## Testing

```bash
go test ./...
go test -v ./...
go test -race ./...
go test -cover ./...
go test -coverprofile=coverage.out ./... && go tool cover -html=coverage.out -o coverage.html
go test ./pkg/api/ -run TestLogin -v
```

## Benchmarks

```bash
go test -bench=. -benchmem ./...
```

## Linting

```bash
# golangci-lint (recommended)
golangci-lint run ./...

# Built-in
go vet ./...
```

## Formatting

```bash
gofmt -w .
goimports -w .
```

## Module management

```bash
go mod init mymodule
go mod tidy
go mod download
go get github.com/pkg/errors@latest
go list -m all                    # List all dependencies
go list -m -u all                 # Check for updates
```

## Build for different platforms

```bash
GOOS=linux GOARCH=amd64 go build -o bin/app-linux ./cmd/server
GOOS=darwin GOARCH=arm64 go build -o bin/app-darwin ./cmd/server
```

## Debugging

```bash
# Delve debugger
dlv debug ./cmd/server
dlv test ./pkg/api/
```

## Generate

```bash
go generate ./...
```

## Notes

- Go projects use `go.mod` for module definition and dependency management.
- Use `./...` to target all packages recursively.
- `go vet` catches common mistakes; `golangci-lint` is more comprehensive.
