---
name: security-guard
description: Security hardening rules (applies to all files)
alwaysApply: true
---

# Security Guard Rules

Applied to all code. Prevents OWASP Top 10 vulnerabilities.

## Injection Attacks

### SQL Injection

**NEVER**:
```csharp
// ❌ BAD: String concatenation
var query = $"SELECT * FROM Users WHERE Email = '{email}'";
var query = "SELECT * FROM Users WHERE Email = " + email;
```

**ALWAYS**:
```csharp
// ✅ GOOD: Parameterized queries
const string query = "SELECT * FROM Users WHERE Email = @Email";
var user = await connection.QuerySingleOrDefaultAsync<User>(
  query,
  new { Email = email }
);
```

**FLAG IF**:
- SQL query built with string concatenation
- String interpolation in SQL queries
- Missing parameter prefix (@) in Dapper

### Command Injection

**NEVER**:
```csharp
// ❌ BAD: Passing user input to shell commands
var result = ExecuteCommand($"ffmpeg {userInput}");
```

**ALWAYS**:
```csharp
// ✅ GOOD: Use APIs instead of shell commands
var process = new ProcessStartInfo("ffmpeg")
{
  Arguments = EscapeArgument(userInput),
  UseShellExecute = false
};
```

## Input Validation

**ALWAYS**:
- Validate ALL user input (query params, body, headers)
- Use FluentValidation at controller boundary
- Whitelist allowed values (don't just blacklist)
- Check file extensions + content type (not just filename)

**NEVER**:
- Trust user input (email, URL, file path, numbers)
- Validate in frontend only (validate server-side too)
- Use `string.IsNullOrEmpty` alone for security (use explicit validation)

**Example**:
```csharp
// ✅ Controller boundary validation
public class CreateUserRequest
{
  [Required]
  [StringLength(100)]
  [EmailAddress]
  public string Email { get; set; }

  [Required]
  [StringLength(50)]
  [RegularExpression(@"^[a-zA-Z0-9_]*$")]
  public string Username { get; set; }
}
```

## Authentication & Authorization

**ALWAYS**:
- Use `[Authorize]` on all protected endpoints
- Use role-based or policy-based auth
- Validate bearer tokens
- Check permissions before accessing resources

**NEVER**:
- Leave auth off endpoints that access user data
- Trust `UserId` from headers (use `User.FindFirst()`)
- Hardcode admin roles/permissions
- Skip token expiration checks

**Example**:
```csharp
[Authorize(Roles = "Admin")]
[HttpDelete("api/v1/users/{id}")]
public async Task<IActionResult> DeleteUser(int id)
{
  // Verify current user can delete this user
  var currentUserId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
  if (currentUserId != id && !User.IsInRole("SuperAdmin"))
    return Forbid();

  // ... delete logic
}
```

## Sensitive Data

### Logging & Monitoring

**NEVER**:
- Log passwords, API keys, tokens
- Log email addresses or phone numbers
- Log full credit card numbers
- Log personally identifiable info (PII)

**ALWAYS**:
- Log correlation IDs for tracing
- Log error codes (not stack traces to clients)
- Redact sensitive fields in logs
- Use structured logging with semantic properties

**Example**:
```csharp
// ❌ BAD
logger.LogError("User login failed: {FullException}", ex.ToString());

// ✅ GOOD
logger.LogWarning("User login failed. UserId: {UserId}, Error: {ErrorCode}",
  userId, ErrorCode.InvalidCredentials);
```

### Storage

**ALWAYS**:
- Hash passwords (use `bcrypt` or similar)
- Store tokens in secure httpOnly cookies
- Encrypt sensitive data at rest
- Never store credit card data (use payment processor)

**NEVER**:
- Store plain-text passwords
- Store tokens in localStorage (XSS risk)
- Hardcode encryption keys in code

## XSS (Cross-Site Scripting)

### Angular Templates

**NEVER**:
```html
<!-- ❌ BAD: Binding untrusted HTML -->
<div [innerHTML]="userContent"></div>
```

**ALWAYS**:
```html
<!-- ✅ GOOD: Use DomSanitizer -->
<div [innerHTML]="sanitizedContent$ | async"></div>

<!-- Or: Plain text binding -->
<div>{{ userContent }}</div>
```

**Component**:
```typescript
constructor(private sanitizer: DomSanitizer) {}

get sanitizedContent$() {
  return this.userContent$.pipe(
    map(content => this.sanitizer.sanitize(SecurityContext.HTML, content))
  );
}
```

### C# Output Encoding

**ALWAYS**:
- HTML-encode user content before rendering
- Use `System.Web.HttpUtility.HtmlEncode()`
- Use framework helpers (ASP.NET Core handles most cases)

**NEVER**:
- Echo user input directly without encoding

## CORS & Headers

**ALWAYS**:
- Set specific `CORS` origins (not `*`)
- Include security headers:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Content-Security-Policy: ...`
  - `Strict-Transport-Security: ...`
- Validate referrer headers

**NEVER**:
- Allow `Origin: *` on authenticated endpoints
- Skip CORS (leaving default open)

## Secrets Management

**ALWAYS**:
- Store secrets in configuration (appsettings.json → environment variables)
- Use Azure Key Vault for production
- Rotate secrets regularly
- Never commit API keys or passwords

**NEVER**:
- Hardcode API keys in source code
- Commit `.env` files
- Share secrets via chat/email
- Use same secret across environments

**Example**:
```csharp
// ✅ Read from config
var apiKey = configuration["OpenRouter:ApiKey"];
var secret = secretClient.GetSecret("openrouter-api-key").Value.Value;
```

## Deserialization

**ALWAYS**:
- Validate deserialized objects
- Use type-safe deserialization (not dynamic)
- Set limits on collection sizes (prevent DOS)

**NEVER**:
- Deserialize untrusted JSON into `dynamic`
- Deserialize without type information
- Allow arbitrary type deserialization

## Path Traversal

**ALWAYS**:
- Validate file paths
- Use `Path.GetFullPath()` and verify it's within allowed directory
- Never build file paths from user input

**NEVER**:
```csharp
// ❌ BAD
var filePath = Path.Combine("/uploads", userProvidedPath);
return File(System.IO.File.ReadAllBytes(filePath));

// ✅ GOOD
var userPath = Path.GetFullPath(Path.Combine("/uploads", userProvidedPath));
if (!userPath.StartsWith("/uploads/"))
  return BadRequest("Invalid path");
return File(System.IO.File.ReadAllBytes(userPath));
```

## HTTPS Enforcement

**ALWAYS**:
- Use HTTPS for all production endpoints
- Redirect HTTP → HTTPS
- Include `Strict-Transport-Security` header

**NEVER**:
- Accept HTTP for authentication endpoints
- Use self-signed certs in production

---

**Last Updated**: 2026-04-09 | **Severity**: CRITICAL

