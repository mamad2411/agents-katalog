# Humanlog Project Rules

## Shared Guidelines Reference

- **This project follows the shared LLM assistant guidelines in [`llm-shared/`](../llm-shared/):**
  - [`llm-shared/project_tech_stack.md`](../llm-shared/project_tech_stack.md): Project management, validation, build/test/lint workflows, and universal conventions for all projects.
  - [`llm-shared/languages/go.md`](../llm-shared/languages/go.md): Go-specific best practices, library choices, and code formatting/testing standards.
  - [`llm-shared/utils/`](../llm-shared/utils/): Tools for code analysis and validation (e.g., `gofuncs`, `validate-docs`).
  - [`llm-shared/templates/`](../llm-shared/templates/): Example `.gitignore`, `Taskfile.yml`, and CI workflow templates.

> **Always consult the above files for baseline rules. This file documents only project-specific conventions and architectural notes for `humanlog`.**

---

## Project-Specific Rules for `humanlog`

### Overview & Architecture

- This package provides a human-readable formatter for Go's `log/slog` output.
- Main components:
  - `Handler` (`handler.go`): Implements `slog.Handler` with custom formatting.
  - `Options` (`options.go`): Configures handler behavior.
  - `NewHandler` (`humanlog.go`): Entry point for handler creation.
- Example usage: `example/main.go`. Tests: `handler_test.go`.

### Developer Workflows

- **Build**: Use standard Go tools (`go build`, `go install`).
- **Test**: `go test ./...` (see `handler_test.go`).
- **Example**: `go run example/main.go` to see formatted log output.

### Project-Specific Conventions

- No global state; all config via `Options` or method params.
- `NewHandler` panics if given a nil writer (enforced contract).
- All exported types/functions must have doc comments.
- Formatting helpers are unexported and colocated with usage.
- Log messages are padded/truncated to a fixed width (see `messageWidth` in `handler.go`).
- Color output for log levels unless `DisableColor` is set.

### Integration & Dependencies

- Only standard library and `log/slog` are used.
- Go module path: `github.com/lepinkainen/humanlog` (see `go.mod`).

### Patterns & Examples

- See `example/main.go` for idiomatic usage patterns.
- See `handler_test.go` for test structure and coverage.

---

_If any section is unclear or missing important project-specific details, please provide feedback or point to additional documentation to improve these rules._
