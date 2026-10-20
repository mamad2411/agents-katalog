---
applyTo: "**/*"
---

# Security Checklist (Always Enforced)

## Input Validation

- Validate ALL user input server-side with Pydantic models — never trust the client
- Use Zod/Valibot on the frontend for form validation before submission
- Sanitize HTML output to prevent XSS — use framework auto-escaping, never `v-html` or `dangerouslySetInnerHTML` with user data
- Validate and sanitize file uploads: check MIME type, size limits, scan for malware patterns

## Database Security

- ALWAYS use parameterized queries — never concatenate or f-string user input into SQL
- Use SQLAlchemy ORM methods or `text()` with bound parameters
- Apply least-privilege database roles: app user should not have DDL permissions
- Audit and limit query results with pagination — never return unbounded result sets

## Authentication & Authorization

- Hash passwords with `bcrypt` or `argon2` — never store plaintext
- Use short-lived JWTs (15 min access, 7 day refresh) with proper signing (RS256 or HS256)
- Implement role-based access control (RBAC) at the service layer
- Validate authorization on every request — never rely solely on frontend route guards

## Secrets Management

- NEVER hardcode secrets, API keys, or credentials in source code
- Use environment variables loaded from `.env` files (excluded from git)
- Reference secrets via `os.environ` or a vault client — never default values for secrets
- Rotate secrets regularly; use short-lived tokens where possible

## API Security

- Enable CORS with explicit allowed origins — never use `*` in production
- Implement rate limiting on authentication and public endpoints
- Add CSRF protection for cookie-based authentication
- Return consistent error response structure — never leak stack traces or internal paths
- Use HTTPS everywhere; set `Secure`, `HttpOnly`, `SameSite` flags on cookies

## Dependency Security

- Pin all dependency versions in `pyproject.toml` / `package-lock.json`
- Run `pip audit` and `npm audit` in CI pipelines
- No unused dependencies — remove anything not actively imported
- Review new dependencies before adding: check maintenance status, known CVEs, license

## Code Patterns to Reject

```python
# ❌ NEVER: SQL injection risk
query = f"SELECT * FROM user WHERE email = '{email}'"

# ✅ ALWAYS: Parameterized query
stmt = select(User).where(User.email == email)
```

```python
# ❌ NEVER: Secret in code
API_KEY = "sk-abc123..."

# ✅ ALWAYS: Environment variable
API_KEY = os.environ["API_KEY"]
```

```typescript
// ❌ NEVER: XSS risk
<div v-html="userComment" />

// ✅ ALWAYS: Text interpolation
<div>{{ userComment }}</div>
```
