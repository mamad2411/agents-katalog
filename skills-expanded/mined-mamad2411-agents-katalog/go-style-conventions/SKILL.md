---
name: go-style-conventions
description: >
  Idiomatic Go style conventions: naming, package layout, error handling, context
  first, interfaces, concurrency basics, gofmt/go vet/staticcheck, and comments.
  Use as the language style companion for owned Go code; does not replace
  code-quality-standards.
---

# Go Style Conventions

## Scope And Authorization

- **In scope:** Go code in repositories you maintain.
- **Out of scope:** Rewriting third-party modules for style alone without need.
- Format with `gofmt`/`goimports` — non-negotiable in CI.
- Pair with `code-quality-standards` for reliability/security; this skill is language idioms.
- Comments depth → `comment-writing-standards` when needed.

## When To Use

- Reviewing PRs for idiomatic Go.
- Bootstrapping a new Go module’s CONTRIBUTING style section.
- Aligning a team migrating from other languages.
- Before deeper skills (race, slog, modules).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Reliability/security baseline | `code-quality-standards` |
| Race detector | `go-race-detector-workflow` |
| Context timeouts | `go-context-timeouts` |
| Module release | `go-module-release-workflow` |
| slog details | `go-slog-structured-logging` |
| Naming cross-language | `naming-conventions-general` |

## Concepts (idioms)

| Topic | Idiom |
| --- | --- |
| Format | `gofmt` is the style |
| Names | MixedCaps; short local names; no `Get` prefix noise |
| Packages | Short, lowercase, no underscores; name = import purpose |
| Errors | Return `error` last; wrap with `%w`; sentinel/`errors.Is` |
| Context | First parameter; not in structs long-lived |
| Interfaces | Accept interfaces, return structs; small interfaces |
| Concurrency | Don’t communicate by sharing memory… (channels/ownership) |
| Init | Avoid heavy `init()`; prefer explicit setup |

## Workflow

### 1. Toolchain gates

```bash
gofmt -w .
goimports -w .
go vet ./...
go test ./...
# recommended:
staticcheck ./...
```

CI:

```bash
test -z "$(gofmt -l .)"
go vet ./...
```

### 2. Naming

```go
// Good
func (c *Client) Publish(ctx context.Context, topic string, body []byte) error

// Bad
func (c *Client) GetPublishMessage(ctx context.Context, topicNameString string, messageBodyBytes []byte) error
```

| Kind | Convention |
| --- | --- |
| Exported | `Client`, `Publish` |
| Unexported | `parseConfig` |
| Acronyms | `URL`, `ID` as `URL`/`ID` (consistent `ServeHTTP`) |
| Files | `client.go`, `client_test.go` |

### 3. Errors

```go
if err != nil {
    return fmt.Errorf("load user %s: %w", id, err)
}
if errors.Is(err, sql.ErrNoRows) {
    return ErrNotFound
}
```

- Do not panic for routine failures.
- Do not ignore err with `_` without comment/justification.

### 4. Packages and layout

```text
/cmd/app/main.go      # thin main
/internal/...         # private libs
/pkg/...              # only if truly public API (optional)
/api/, /web/          # as needed
```

Avoid `util`/`common` grab-bags; name by domain (`billing`, `authn`).

### 5. Interfaces

```go
// Consumer-side small interface
type UserStore interface {
    Find(ctx context.Context, id string) (User, error)
}
```

Define interfaces where used, not always in producer packages.

### 6. Concurrency style

- Prefer explicit ownership and `errgroup` limits (`go-errgroup-limits`).
- Always know who stops a goroutine.
- Document thread-safety of exported types.

### 7. Comments and docs

```go
// Package billing charges invoices via the payment gateway.
package billing

// Client is a concurrent-safe billing API client.
type Client struct{ /* ... */ }
```

- Doc comments start with the name.
- Explain *why* for non-obvious code; skip restating the line.

### 8. Tests style

- Table-driven tests preferred.
- `cmp.Diff` for structs (`go-cmp-diff-tests`).
- Avoid time.Sleep flakes; use channels/synctest where appropriate.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Format | gofmt clean | Spaces-aligned hand style |
| Errors | wrap `%w` | `err.Error()` string compare |
| Context | first param | buried in options only |
| Export | minimal API surface | Everything capital for “JSON” |
| Packages | `mailer` | `mailer_utils_v2` |
| Nil | useful zero values | Needless builders everywhere |

## Output Checklist

- [ ] gofmt/goimports clean
- [ ] go vet (/staticcheck) clean
- [ ] Names idiomatic
- [ ] Errors wrapped and inspected with Is/As
- [ ] Context first on blocking APIs
- [ ] Packages coherent
- [ ] Interfaces small and local
- [ ] Goroutine lifecycle clear
- [ ] Docs on exported API
- [ ] `code-quality-standards` also considered

## Rules

- gofmt is not optional.
- Errors are values; handle them.
- Context first; cancel correctly.
- Simplicity over premature abstraction.
- This is style — security/reliability still need `code-quality-standards`.
