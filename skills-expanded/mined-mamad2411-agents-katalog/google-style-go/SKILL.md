---
name: google-style-go
description: >
  Apply Google's official Go style guide when writing, reviewing, or
  formatting Go code. Use this skill whenever the user asks to review Go
  code for style, asks about Go naming conventions, error handling patterns,
  package organisation, comment format, goroutine safety, or whether code
  follows Google/Uber/idiomatic Go conventions. Also triggers on: "is this
  idiomatic Go?", "clean up this Go code", "how should I name this in Go?",
  "how do I handle errors in Go?", "should I use goroutines here?", "what's
  the Google way for Go package structure?", or any request involving gofmt,
  golangci-lint, or go vet in a style context. Google's Go guide covers three
  dimensions: style rules (guide.md), best practices (best-practices.md),
  and decision rationale (decisions.md) — this skill knows when to consult each.
---

# Google Go Style Guide

Google maintains three complementary Go guides:
- **Style guide** (`guide.md`) — the authoritative rules
- **Best practices** (`best_practices.md`) — patterns and idioms for common situations  
- **Decisions** (`decisions.md`) — rationale behind choices, useful when defending or questioning a rule

Key themes across all three: names are short and clear, errors are explicit and
never ignored, goroutines are always bounded, and formatting is handled entirely
by `gofmt` (never argue about it).

---

## Key Rules at a Glance

### Naming
- **Packages**: short, lowercase, no underscores, singular (`user` not `users`). Avoid generic names like `util`, `common`, `misc`.
- **Exported names**: `PascalCase`, descriptive but not redundant with the package name (`user.Client`, not `user.UserClient`).
- **Unexported names**: `camelCase`.
- **Acronyms**: keep full case — `HTTPServer`, `userID`, `parseURL`.
- **Interfaces**: name by the behaviour they express, often `-er` suffix (`Reader`, `Stringer`). Single-method interfaces are encouraged.
- **Error vars**: prefix with `Err` for sentinel errors (`ErrNotFound`), suffix with `Error` for types (`NotFoundError`).
- **Receivers**: short, 1-2 letter abbreviation of the type. Consistent across all methods (`c` for `Client`, not mixing `c` and `client`).

### Error handling
- Never ignore errors — check every returned error.
- Wrap errors with context using `fmt.Errorf("doing X: %w", err)`.
- Use `errors.Is()` / `errors.As()` to inspect wrapped errors — never string matching.
- Return early on error (the "happy path" stays un-indented).
- Sentinel errors (`var ErrNotFound = errors.New(...)`) only for errors callers need to match; otherwise just return descriptive wrapped errors.

### Goroutines
- Every goroutine must have a clear owner responsible for its lifetime.
- Goroutines must have a way to stop — pass a `context.Context` or use a done channel.
- Document goroutine safety in comments: state whether a type is safe for concurrent use.
- Prefer `sync.WaitGroup` + bounded worker pools over unbounded goroutine spawning.

### Comments
- Every exported identifier needs a doc comment starting with the identifier's name:
  ```go
  // Client manages connections to the backend.
  type Client struct { ... }
  
  // Do executes the given request and returns the response.
  func (c *Client) Do(req *Request) (*Response, error) { ... }
  ```
- Package doc goes in `doc.go` or at the top of the main file: `// Package user provides...`
- Use `//nolint` with a reason, never silently.

### Formatting
- Run `gofmt` — no discussion. All Google Go code is `gofmt`-formatted.
- Line length: no hard limit, but keep lines readable (~100 chars is a soft target).
- Imports: stdlib → third-party → internal, separated by blank lines (`goimports` handles this).

### Context
- `context.Context` is the first parameter of any function that does I/O, calls RPCs, or may be cancelled.
- Name the parameter `ctx`.
- Never store `Context` in a struct field — pass it through function calls.

---

## Which reference file to load

| Task | Load |
|---|---|
| "Is this naming correct?" | `references/guide.md` |
| "How should I structure this package?" | `references/best_practices.md` |
| "Why does Go do X this way?" | `references/decisions.md` |
| Comprehensive code review | all three |
| Quick lookup of a specific rule | `references/index.md` first |

---

## Mode: Reviewing Go Code

When asked to review Go code for Google style compliance:

1. **Naming** — correct casing? Package name concise and non-generic? Receiver names consistent?
2. **Error handling** — every error checked? Errors wrapped with `%w`? `errors.Is()`/`errors.As()` for inspection?
3. **Comments** — all exported identifiers have doc comments? Comments start with the name?
4. **Context** — `ctx context.Context` as first param on I/O functions? Not stored in structs?
5. **Goroutines** — do they have clear owners and a stop mechanism? Is there a risk of goroutine leak?
6. **Imports** — three groups, `goimports` ordered? Any dot imports (`import . "pkg"`)?
7. **Formatting** — assume `gofmt` is run; flag only structural issues.
8. **Interfaces** — defined at the point of use (not in the package that implements them)?

For each issue:
- Cite the relevant file (`guide.md §X`, `best_practices.md §Y`)
- Show the problematic snippet and the corrected version with brief rationale

---

## Mode: Writing New Go Code

When writing new Go following Google style:

1. Package name: short, lowercase, singular, descriptive.
2. `context.Context` as first param on any function doing I/O.
3. Return errors explicitly; use `fmt.Errorf("context: %w", err)` to wrap.
4. All exported identifiers get doc comments — name first.
5. Interfaces defined where they're consumed, not where they're implemented.
6. Goroutines: always pass a `ctx` or done channel; document who owns cleanup.
7. Use `errors.Is()` / `errors.As()` to match specific error types.
8. Short, early returns on error — keep the happy path at the left margin.
9. Prefer table-driven tests (`[]struct{ name, input, want }`).
10. Run `gofmt` and `go vet` before considering code done.

---

## When to Load a Reference File

All three reference files are large (400–3,800 lines each). Load only what you need:

- `references/index.md` — 171-line overview and links to topics, good starting point
- `references/guide.md` — 440 lines, the core rules
- `references/best_practices.md` — 3,828 lines, patterns for specific situations
- `references/decisions.md` — 3,604 lines, rationale and trade-offs

**Also see**: `google-style-common` for cross-language principles on naming and comments.
