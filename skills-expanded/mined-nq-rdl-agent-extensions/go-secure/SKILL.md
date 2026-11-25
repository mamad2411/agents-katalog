---
name: go-secure
license: CC-BY-4.0
description: >-
  Secure Go error handling across trust boundaries: never return err.Error()
  to external callers, translate domain errors at HTTP, gRPC, and CLI
  boundaries, redact secrets in slog logs, and return safe API error
  responses. Use when writing or reviewing Go handlers, services, or error and
  logging code whose output reaches users or logs, even if security is not
  mentioned.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Secure Go Error Handling

Go's "errors are values" design means every error is explicitly handled at the call
site. This is powerful — but it also means every error is a potential data leak if it
crosses a trust boundary without sanitization.

Real-world impact: [CVE-2025-7445](https://github.com/kubernetes/kubernetes/issues/133897): the
Kubernetes secrets-store-sync-controller (before v0.0.2) wrote service account tokens to
its logs when marshalling the provider `parameters` failed. Verbose errors in production
have leaked SQL queries, file paths, credentials, and infrastructure topology.

## The Core Rule

**Never return `err.Error()` to external callers.**

`err.Error()` is for developers reading logs. It is not for API clients, end users,
or any consumer outside your trust boundary. Always translate errors before they
cross a boundary.

---

## Pattern 1: Domain Error Types

Separate what's safe to show externally from what's safe to log internally. The
`Error()` method returns only the safe message — this is your last line of defense
if the error accidentally reaches an HTTP response body.

```go
// DomainError separates safe user-facing messages from raw internal details.
type DomainError struct {
	Code     string            // Machine-readable: "USER_NOT_FOUND", "VALIDATION_FAILED"
	UserMsg  string            // Safe for clients: "User not found"
	Internal error             // Raw upstream error — never expose via API
	Metadata map[string]string // Sanitized context for structured logging
}

// Error returns only the safe message. If this error is accidentally serialized
// to an HTTP response via fmt.Fprintf(w, "%v", err), only UserMsg leaks.
func (e *DomainError) Error() string { return e.UserMsg }
func (e *DomainError) Unwrap() error { return e.Internal }

// HTTPStatus maps error codes to HTTP status codes.
func (e *DomainError) HTTPStatus() int {
	switch e.Code {
	case "USER_NOT_FOUND", "RESOURCE_NOT_FOUND":
		return http.StatusNotFound
	case "VALIDATION_FAILED":
		return http.StatusBadRequest
	case "UNAUTHORIZED":
		return http.StatusUnauthorized
	case "FORBIDDEN":
		return http.StatusForbidden
	default:
		return http.StatusInternalServerError
	}
}
```

### Constructors enforce consistency

```go
func NewNotFound(resource string, internal error) *DomainError {
	return &DomainError{
		Code:     "RESOURCE_NOT_FOUND",
		UserMsg:  resource + " not found",
		Internal: internal,
	}
}

func NewInternal(internal error) *DomainError {
	return &DomainError{
		Code:     "INTERNAL",
		UserMsg:  "An internal error occurred",
		Internal: internal,
	}
}
```

---

## Pattern 2: Trust Boundary Translation

Every time an error crosses a trust boundary, translate it. Never propagate raw
upstream errors — they contain implementation details that hint at your tech stack,
SQL injection vectors, or infrastructure topology.

### Database -> Domain

```go
func (r *UserRepo) FindByID(ctx context.Context, id string) (*User, error) {
	row := r.db.QueryRowContext(ctx, "SELECT id, name, email FROM users WHERE id = $1", id)

	var u User
	if err := row.Scan(&u.ID, &u.Name, &u.Email); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, NewNotFound("user", err)
		}
		// "pq: duplicate key violates constraint..." never reaches callers
		return nil, NewInternal(err)
	}
	return &u, nil
}
```

### Domain -> HTTP

```go
func (s *Server) handleGetUser(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	user, err := s.users.FindByID(r.Context(), id)
	if err != nil {
		s.writeError(w, r, err)
		return
	}
	s.writeJSON(w, http.StatusOK, user)
}

func (s *Server) writeError(w http.ResponseWriter, r *http.Request, err error) {
	requestID := r.Header.Get("X-Request-ID")

	// Log the full error chain internally — this is where developers look
	slog.ErrorContext(r.Context(), "request failed",
		"request_id", requestID,
		"path", r.URL.Path,
		"error", err,
	)

	// Return only safe information to client
	var domErr *DomainError
	if errors.As(err, &domErr) {
		s.writeJSON(w, domErr.HTTPStatus(), map[string]string{
			"error":      domErr.Code,
			"message":    domErr.UserMsg,
			"request_id": requestID,
		})
		return
	}

	// Unknown errors get a completely generic response
	s.writeJSON(w, http.StatusInternalServerError, map[string]string{
		"error":      "INTERNAL",
		"message":    "An internal error occurred",
		"request_id": requestID,
	})
}
```

### Domain -> gRPC

```go
import "google.golang.org/grpc/status"

func domainToGRPC(err error) error {
	var domErr *DomainError
	if errors.As(err, &domErr) {
		switch domErr.Code {
		case "RESOURCE_NOT_FOUND":
			return status.Error(codes.NotFound, domErr.UserMsg)
		case "VALIDATION_FAILED":
			return status.Error(codes.InvalidArgument, domErr.UserMsg)
		default:
			return status.Error(codes.Internal, "internal error")
		}
	}
	return status.Error(codes.Internal, "internal error")
}
```

---

## Pattern 3: Structured Logging with Redaction

Use `log/slog` (Go 1.21+) for structured logging. The key advantage over
`fmt.Sprintf`: fields are typed and individually controllable, so you can redact
sensitive values without losing the rest of the context.

### Implement `slog.LogValuer` for sensitive types

```go
// Credentials prevents accidental password logging.
type Credentials struct {
	Username string
	Password string
}

// LogValue controls what slog outputs — Password is never logged.
func (c Credentials) LogValue() slog.Value {
	return slog.GroupValue(
		slog.String("username", c.Username),
		slog.String("password", "[REDACTED]"),
	)
}
```

### Strip sensitive headers before logging

```go
func SafeHeaders(h http.Header) map[string]string {
	sensitive := map[string]bool{
		"Authorization": true,
		"Cookie":        true,
		"Set-Cookie":    true,
		"X-Api-Key":     true,
	}
	safe := make(map[string]string, len(h))
	for k := range h {
		if sensitive[k] {
			safe[k] = "[REDACTED]"
		} else {
			safe[k] = h.Get(k)
		}
	}
	return safe
}
```

### Never log request bodies or structs directly

```go
// BAD — logs passwords, tokens, PII
slog.Info("request received", "body", string(body))

// GOOD — log only fields you've verified are safe
slog.Info("user signup",
	"email", req.Email,
	"plan", req.Plan,
	// req.Password deliberately omitted
)
```

---

## Pattern 4: Opaque Wrapping

Standard `fmt.Errorf("...: %w", err)` creates chains traversable via `errors.Is`
and `errors.As`. In library code, this leaks implementation details — callers can
discover which database driver or cache backend you use.

When you don't want callers to introspect the underlying cause:

```go
// OpaqueError wraps an error without exposing it to errors.Is/errors.As.
// Use at library/package boundaries to hide implementation details.
type OpaqueError struct {
	msg      string
	internal error // not exposed via Unwrap
}

func (e *OpaqueError) Error() string { return e.msg }

// No Unwrap method — errors.Is/errors.As cannot traverse past this point.
// The internal error is available only for logging within the package.
```

**Use opaque wrapping when:**
- Your library wraps a third-party dependency and callers shouldn't depend on its error types
- Error details reveal internal architecture (which cache backend, which message queue)

**Use standard `%w` wrapping when:**
- Callers legitimately need to check for specific error conditions
- The wrapped error type is part of your public API contract

---

## Pattern 5: Context Metadata (Allowlist Approach)

When building structured error context, use an allowlist of known-safe fields.
Never log entire request or error structs — they may gain sensitive fields later,
and your log statement will silently start leaking them.

```go
func SafeRequestContext(r *http.Request) []slog.Attr {
	return []slog.Attr{
		slog.String("method", r.Method),
		slog.String("path", r.URL.Path),
		slog.String("remote_addr", r.RemoteAddr),
		slog.String("request_id", r.Header.Get("X-Request-ID")),
		// Deliberately NOT including: headers, query params, body
	}
}
```

---

## Security Audit Checklist

Before shipping error handling code, run through the checklist in
`references/audit-checklist.rst`. It covers the decision tree for each error:
is the caller trusted? Does the error contain sensitive data? Will it cross
a trust boundary?

---

## References

- JetBrains: [Secure Go Error Handling Best Practices (2026-03-02)](https://blog.jetbrains.com/go/2026/03/02/secure-go-error-handling-best-practices/)
- OWASP: [Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)
