---
name: security-audit
description: >
  Use when auditing code for security vulnerabilities: OWASP Top 10 checks,
  secret scanning, dependency audits, SQL injection, XSS, CSRF, authentication
  flaws, insecure deserialization. Works with any stack.
license: MIT
compatibility: opencode
---

# Security Audit Skill

## When to Use

Activate this skill when the user:
- Asks for a security review of code
- Wants to check for OWASP Top 10 vulnerabilities
- Needs to audit authentication/authorization logic
- Asks "is this code secure?"
- Wants to scan for hardcoded secrets

## OWASP Top 10 Checklist

### A01: Broken Access Control
- [ ] All endpoints require appropriate authentication
- [ ] Authorization checked on every request (not just login)
- [ ] User can only access their own resources (IDOR check)
- [ ] Admin functions protected from regular users

### A02: Cryptographic Failures
- [ ] No sensitive data in URLs or logs
- [ ] Passwords hashed with bcrypt/Argon2/PBKDF2 (not MD5/SHA1)
- [ ] TLS enforced for all connections
- [ ] No hardcoded encryption keys

### A03: Injection
- [ ] SQL uses parameterized queries / ORM
- [ ] No string concatenation in SQL, shell commands, LDAP
- [ ] User input sanitized before use in templates
- [ ] NoSQL queries use safe operators

### A04: Insecure Design
- [ ] Threat modeling done for critical flows
- [ ] Rate limiting on authentication endpoints
- [ ] Account lockout after failed attempts

### A05: Security Misconfiguration
- [ ] Debug mode disabled in production
- [ ] Default credentials changed
- [ ] Unnecessary features/endpoints disabled
- [ ] Error messages don't expose stack traces

### A06: Vulnerable Components
```bash
# Run dependency audit
npm audit          # Node.js
dotnet list package --vulnerable  # .NET
go list -json -m all | nancy      # Go
```

### A07: Identification & Authentication Failures
- [ ] Session tokens are random and sufficiently long
- [ ] Sessions invalidated on logout
- [ ] MFA available for sensitive operations
- [ ] Password reset flow is secure (no enumeration)

### A09: Security Logging Failures
- [ ] Authentication events are logged
- [ ] Authorization failures are logged
- [ ] Logs don't contain passwords or tokens
- [ ] Logs are centralized and protected

### A10: SSRF
- [ ] User-supplied URLs validated against allowlist
- [ ] No fetching from internal network based on user input

## Secret Scanning Patterns

Look for these patterns that indicate hardcoded secrets:
```regex
# API Keys
(api[_-]?key|apikey)\s*[=:]\s*['"][a-zA-Z0-9]{16,}['"]
# Generic secrets
(secret|password|passwd|pwd)\s*[=:]\s*['"][^'"]{8,}['"]
# Connection strings with credentials
(mongodb|postgres|mysql):\/\/[^:]+:[^@]+@
```

## Language-Specific Checks

### C# / ASP.NET Core
```csharp
// ✅ SQL Injection safe
await context.Users
    .Where(u => u.Email == email)  // EF Core parameterizes automatically
    .FirstOrDefaultAsync();

// ✅ Password hashing
var hash = BCrypt.HashPassword(password, workFactor: 12);

// ✅ Anti-forgery tokens
[ValidateAntiForgeryToken]
[HttpPost]
public async Task<IActionResult> CreateOrder(...)
```

### Go
```go
// ✅ SQL injection safe
row := db.QueryRowContext(ctx, 
    "SELECT id, name FROM users WHERE email = $1", email)

// ✅ Timing-safe comparison
if !subtle.ConstantTimeCompare([]byte(provided), []byte(stored)) {
    return ErrInvalidCredentials
}
```

### TypeScript
```typescript
// ✅ SQL injection safe (parameterized)
const user = await db.query(
  'SELECT * FROM users WHERE email = $1', [email]
);

// ✅ XSS prevention — never use innerHTML with user data
element.textContent = userInput;  // ✅ safe
element.innerHTML = userInput;    // ❌ XSS risk
```

## Output Format

```markdown
## Security Audit Report

**Overall Risk:** [Low / Medium / High / Critical]
**Date:** [Date]

### 🔴 Critical Vulnerabilities
...

### 🟡 High Risk Issues
...

### 🟢 Medium Risk Issues
...

### ✅ Passed Checks
...

### Recommended Actions
1. [Priority fix 1]
2. [Priority fix 2]
```
