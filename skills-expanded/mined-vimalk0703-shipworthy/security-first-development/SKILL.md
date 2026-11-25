---
name: security-first-development
description: OWASP-aware security practices — input validation, secrets management, auth patterns, injection prevention, CORS, rate limiting, and CSP headers.
invoke_when: Use when writing auth logic, API endpoints, database queries, file operations, user input handling, or any code that touches external data.
---

# Security-First Development

## Core Rule

**Every piece of external data is hostile until validated.**

## OWASP Practical Checklist

### Injection Prevention
- **SQL**: Parameterized queries ONLY. Never concatenate strings into queries.
- **NoSQL**: Use query builders, never raw object construction from user input.
- **Command**: Never pass user input to shell commands. Use argument arrays.
- **XSS**: Escape all output. Use framework defaults (React auto-escapes JSX).

### Authentication
- Use established libraries (NextAuth, Passport) — never roll your own
- Passwords: bcrypt/argon2. Never MD5/SHA for passwords.
- Sessions: HTTP-only, secure, SameSite cookies
- Rate limit login attempts

### Authorization
- Check permissions on EVERY request, not just the UI
- Default deny — explicitly grant, never explicitly deny
- Verify resource ownership (user A can't access user B's data)

### Secrets Management
- **NEVER** hardcode secrets in source code
- Use environment variables with validation at startup
- `.env` files MUST be in `.gitignore`
- Different secrets per environment

### Input Validation
- Validate at the boundary (API handler, form submission)
- **ALWAYS install and use a schema validation library** — never write manual if/else validation:
  - TypeScript/JavaScript: `npm install zod` — use `z.object()` schemas for every request body
  - Python: Pydantic models for every endpoint
  - Go: validator package or custom validation
- Whitelist valid input, don't blacklist bad input
- Validate BEFORE processing: parse the request body with the schema, reject if invalid, then proceed with the typed result

### CORS
- Never use `*` in production
- Explicitly list allowed origins

### Rate Limiting
- All public endpoints must have rate limits
- Return 429 with Retry-After header

### Content Security Policy
- Set CSP headers to prevent XSS
- Restrict script sources, style sources, frame ancestors

### Dependencies
- Run `npm audit` / `pip audit` before committing
- No packages with known critical vulnerabilities
