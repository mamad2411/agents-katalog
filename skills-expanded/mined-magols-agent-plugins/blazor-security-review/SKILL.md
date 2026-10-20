---
name: blazor-security-review
description: 'Security-focused review for Blazor and C# code. Covers XSS via MarkupString, authentication/authorization correctness, CSRF, WASM client-side secrets, SignalR hub security, input validation, CSP, and OWASP Top 10 mapped to Blazor-specific patterns.'
---

# Blazor Security Review

Your goal is to perform a security-focused review of Blazor and C# code, identifying vulnerabilities and mapping them to OWASP Top 10 and Blazor-specific risks.

## Output Format

```
## 🔴 Critical (Fix Before Deploy)
### [OWASP Category] — [Issue Title]
File: filename.razor / filename.cs, line N
> problematic code
Risk: explanation of the security impact
✅ Fix: corrected code or approach

## 🟡 Warning (Fix Soon)
...

## 🔵 Hardening (Best Practice)
...

---
## Security Summary
- 🔴 Critical: N
- 🟡 Warning: N
- 🔵 Hardening: N

**Deploy recommendation**: [BLOCK / CONDITIONAL / APPROVE]
```

---

## Security Checklist

### A03 — Injection

#### XSS via MarkupString / BlazorHtml

- 🔴 **Critical**: `@((MarkupString)userInput)` where `userInput` comes from untrusted sources (database, query string, API)
- 🔴 **Critical**: `new MarkupString(value)` without sanitization
- 🔵 **Hardening**: If HTML rendering from user content is required, use a server-side sanitizer (e.g., `HtmlSanitizer` NuGet package) before casting to `MarkupString`

```csharp
// ❌ Critical XSS risk
@((MarkupString)Model.UserProvidedHtml)

// ✅ Sanitize first
@((MarkupString)sanitizer.Sanitize(Model.UserProvidedHtml))
```

#### SQL Injection via EF Core Raw SQL

- 🔴 **Critical**: String interpolation in raw SQL methods

```csharp
// ❌ SQL Injection
context.Products.FromSqlRaw($"SELECT * FROM Products WHERE Name = '{name}'");

// ✅ Parameterized
context.Products.FromSqlInterpolated($"SELECT * FROM Products WHERE Name = {name}");
// or
context.Products.FromSqlRaw("SELECT * FROM Products WHERE Name = {0}", name);
```

### A01 — Broken Access Control

#### Missing Authorization on Pages and Components

- 🔴 **Critical**: Routable Blazor page (`@page`) that displays sensitive data without `[Authorize]` or `<AuthorizeView>`
- 🔴 **Critical**: API endpoints called from Blazor that don't enforce authorization server-side

```razor
@* ❌ Missing authorization *@
@page "/admin/users"
<UserList />

@* ✅ Correct *@
@page "/admin/users"
@attribute [Authorize(Roles = "Admin")]
<UserList />
```

#### AuthorizeView Misuse

- 🟡 **Warning**: `<AuthorizeView>` used as the sole authorization gate — it only hides UI, doesn't block server-side data access
- 🔵 **Hardening**: Always pair `<AuthorizeView>` with server-side policy enforcement

#### Policy-Based Authorization

- 🔵 **Hardening**: Prefer `[Authorize(Policy = "RequiresAdmin")]` over role strings for maintainability

```csharp
// In Program.cs
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("RequiresAdmin", policy =>
        policy.RequireRole("Admin").RequireClaim("department", "IT"));
});
```

### A02 — Cryptographic Failures

#### Sensitive Data in Blazor WASM

- 🔴 **Critical**: API keys, connection strings, or secrets embedded in WASM client code (`appsettings.json` in `wwwroot`, hardcoded in `.razor.cs`)
- 🔴 **Critical**: JWT tokens stored in `localStorage` (vulnerable to XSS)

```csharp
// ❌ Secret in WASM client code — visible to all users
private const string ApiKey = "sk-live-abc123";

// ✅ All secrets must live server-side; expose only via secured API endpoints
```

- 🟡 **Warning**: Sensitive data returned from APIs not filtered to the minimum needed by the client
- 🔵 **Hardening**: Store auth tokens in `sessionStorage` or memory (not `localStorage`) for WASM apps; prefer server-side sessions for Blazor Server

### A05 — Security Misconfiguration

#### CSRF in Blazor Forms

- 🔴 **Critical** (SSR/Static forms): Form POST handlers without antiforgery validation
- Blazor Web App with interactivity: `UseAntiforgery()` must be called and `EditForm` uses antiforgery automatically
- Static SSR form: Must use `[ValidateAntiForgeryToken]` or Blazor's built-in antiforgery

```csharp
// In Program.cs — required before MapRazorComponents
app.UseAntiforgery(); // ✅ Must be present
```

#### Missing Security Headers

- 🟡 **Warning**: No Content Security Policy configured
- 🔵 **Hardening**: Add security headers in middleware:

```csharp
app.Use(async (context, next) =>
{
    context.Response.Headers.Append("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Append("X-Frame-Options", "DENY");
    context.Response.Headers.Append("Referrer-Policy", "strict-origin-when-cross-origin");
    // Customize CSP for your app's needs
    context.Response.Headers.Append("Content-Security-Policy",
        "default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline'");
    await next();
});
```

### A07 — Identification and Authentication Failures

#### SignalR Hub Security (Blazor Server)

- 🔴 **Critical**: SignalR hub that sends user-specific data without verifying the caller's identity
- 🟡 **Warning**: Missing `[Authorize]` on hub methods that modify server state

```csharp
// ❌ No authorization — any connected client can call this
public async Task UpdateUserProfile(ProfileDto dto) { ... }

// ✅ Authorized hub method
[Authorize]
public async Task UpdateUserProfile(ProfileDto dto)
{
    var userId = Context.UserIdentifier; // safe to use after [Authorize]
    await profileService.UpdateAsync(userId!, dto);
}
```

### A03 — Input Validation

#### DataAnnotations Validation

- 🟡 **Warning**: Model bound from forms or query strings lacks `[Required]`, `[StringLength]`, `[Range]` etc.
- 🟡 **Warning**: Server-side validation not re-checked on the backend for Interactive Server apps (client-side validation can be bypassed)
- 🔵 **Hardening**: Use FluentValidation for complex business rules

```csharp
public class CreateOrderDto
{
    [Required]
    [StringLength(200, MinimumLength = 1)]
    public string ProductName { get; set; } = string.Empty;

    [Range(1, 10_000)]
    public int Quantity { get; set; }

    [RegularExpression(@"^\d{4}-\d{2}-\d{2}$")]
    public string? DeliveryDate { get; set; }
}
```

### A09 — Security Logging and Monitoring Failures

- 🟡 **Warning**: Authentication failures, authorization denials, or exceptions caught and silently swallowed without logging
- 🔵 **Hardening**: Log security-relevant events with `ILogger` at Warning or Error level, including user identity context

```csharp
// ✅ Log security events
catch (UnauthorizedAccessException ex)
{
    logger.LogWarning(ex, "Unauthorized access attempt by user {UserId} to resource {Resource}",
        userId, resourceId);
    throw;
}
```

---

## Workflow

1. Read all files completely before writing findings
2. Prioritize Critical findings — these block deployment
3. Map each finding to its OWASP category
4. Provide a concrete fix for every Critical and Warning finding
5. Write the security summary and deploy recommendation last
