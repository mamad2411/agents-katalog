# Repository Guidelines

## Project Structure & Module Organization
This is a small Go CLI project with flat source layout at the repository root.

- `main.go`: CLI entrypoint, flag parsing, app wiring.
- `server.go`, `hub.go`, `watcher.go`: HTTP server, SSE hub, file watching.
- `renderer.go`, `template.go`: Markdown rendering and HTML template output.
- `Makefile`: build/install automation.
- `README.md`: user-facing usage docs.
- `screen.gif`: demo asset used by the README.

When adding new packages, prefer clear boundaries (e.g., `internal/render`, `internal/server`) rather than growing root-level files.

## Build, Test, and Development Commands
- `make build`: compile local binary `./mdv`.
- `make install`: build and install to `$PREFIX/bin/mdv` (default: `~/.local/bin`).
- `make uninstall`: remove installed binary.
- `make clean`: remove local build artifact.
- `go test ./...`: run all tests (currently no test files; add as features grow).
- `go run . --no-browser README.md`: quick local smoke test.

## Coding Style & Naming Conventions
- Follow standard Go formatting: run `gofmt` (or `go fmt ./...`) before committing.
- Use idiomatic Go names: exported identifiers in `CamelCase`, unexported in `camelCase`.
- Keep functions focused and small; colocate related helpers in the same file/module.
- Prefer explicit, descriptive filenames (`watcher.go`, `renderer.go`) over generic names.

## Testing Guidelines
- Use Go’s built-in `testing` package.
- Place tests in `*_test.go` files next to the code they verify.
- Name tests by behavior, e.g., `TestResolvePort_SkipsOccupiedPort`.
- Prioritize coverage for parser/render behavior, port selection, and watcher event handling.

## Commit & Pull Request Guidelines
- Match existing commit style: short imperative subject line (e.g., `Fix SSE reconnect handling`).
- Keep commits focused; avoid mixing refactors with behavior changes.
- PRs should include:
  - What changed and why.
  - How to validate (`make build`, `go test ./...`, manual run command).
  - Screenshots/GIFs for UI/output-visible changes when relevant.
