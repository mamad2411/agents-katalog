---
name: aspnet-middleware-order
description: >
  ASP.NET Core middleware pipeline order for owned apps: exception handling, HSTS,
  HTTPS redirection, CORS, authentication, authorization, antiforgery, routing, and
  custom middleware placement. Use when fixing authz bypasses from wrong order, CORS
  preflight failures, or reviewing Program.cs/Startup pipeline security — not for
  attacking third-party .NET sites.
---

# ASP.NET Middleware Order

## Scope And Authorization

- **In scope:** ASP.NET Core applications and APIs you own or may modify under authorization.
- **Out of scope:** Probing third-party apps for middleware mis-order exploits without permission.
- Middleware order bugs can skip authentication/authorization — treat pipeline reviews as security-sensitive.
- Prefer minimal custom middleware; document each `Use*` call’s position.
- Pair with `code-quality-standards` and `csharp-style-conventions`.

## When To Use

- Reviewing `Program.cs` / `Startup.Configure` pipeline for security correctness.
- Debugging “Authorization worked in controller but endpoint is anonymous.”
- Fixing CORS vs auth order, cookie auth challenges, or status-code re-execute paths.
- Adding security headers, rate limiting, or request logging without breaking auth.
- Migrating from netcoreapp3-style Startup to minimal hosting model.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| JWT/API auth design broadly | `api-auth-and-jwt-abuse` (authorized) / API auth skills |
| General C# style | `csharp-style-conventions` |
| OWASP-wide app review | `secure-sdlc-checklist` / web skills |
| Reverse proxy TLS termination | nginx/edge skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Middleware | Typical placement |
| --- | --- |
| Exception handler / DeveloperExceptionPage | First (outermost) |
| HSTS | Early, production only with HTTPS |
| HTTPS redirection | Early |
| Static files | Before auth if public static; careful with sensitive files |
| Routing | Before CORS/auth that depend on endpoint metadata (version-dependent patterns) |
| CORS | Before auth when browsers need preflight success; after routing in endpoint routing model as docs recommend |
| Authentication | Before Authorization |
| Authorization | Before endpoints that require policies |
| Rate limiting | Often after auth identity available, or early for IP limits |
| Controllers / endpoints | Last (`MapControllers` / `Map*`) |

Official guidance evolves slightly by version — verify against your target TFM docs; the invariant is **Authenticate before Authorize**, and **exception handling wraps the pipeline**.

## Canonical Order (template)

```csharp
var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler("/error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles(); // only if needed; never serve secrets

app.UseRouting();

// CORS must see endpoint metadata when using policies with WithOrigins etc.
app.UseCors("Default");

app.UseAuthentication();
app.UseAuthorization();

// Custom middleware that requires User:
app.UseMiddleware<AuditUserMiddleware>();

app.MapControllers();
app.MapRazorPages();
app.Run();
```

## Workflow

### 1. Confirm scope and success criteria

1. Record app type (MVC, Razor, Minimal APIs, gRPC), TFM, auth schemes (cookies, JWT, OIDC).
2. Success: anonymous endpoints stay anonymous; `[Authorize]` enforced; CORS preflight OK for allowed origins only; errors do not leak stack in prod.
3. List custom middleware and what each needs (connection, user, route values).

### 2. Inventory pipeline

```bash
# Find pipeline configuration
rg -n "Use(Authentication|Authorization|Cors|Routing|Https|Hsts|Exception)" src
rg -n "Map(Controllers|Get|Post|Group)" src
```

1. Copy ordered list of `Use*` / `Map*` calls.
2. Note short-circuit middleware (`app.Run`, early `return`).
3. Identify dual pipelines (e.g. health checks branch).

### 3. Baseline

1. Capture failing requests: status codes for anonymous vs authenticated vs wrong origin.
2. Integration tests for `/health` (allow anonymous) and `/admin` (401/403).
3. Browser preflight for SPA origin if applicable.

### 4. Apply correct order and policies

**Authentication before Authorization (required):**

```csharp
app.UseAuthentication();
app.UseAuthorization();
// Never reverse these
```

**Endpoint routing + authorization:**

```csharp
app.MapGet("/admin", () => "secret")
   .RequireAuthorization("Admins");

app.MapGet("/health", () => Results.Ok("ok"))
   .AllowAnonymous();
```

**CORS policy (tight):**

```csharp
builder.Services.AddCors(o => o.AddPolicy("Default", p =>
    p.WithOrigins("https://app.example.com")
     .WithMethods("GET", "POST")
     .WithHeaders("Authorization", "Content-Type")
     .AllowCredentials())); // only if cookies needed; avoid * origin with credentials
```

**Security headers middleware** — place after exception handling; before endpoints; do not strip CORS headers.

**Common footguns**

| Mistake | Effect |
| --- | --- |
| `UseAuthorization` before `UseAuthentication` | User always empty → wrong challenges/allow |
| CORS after auth blocking preflight | SPA fails OPTIONS |
| Exception handler after terminal middleware | Unhandled errors leak or hang |
| Static files after auth for private files | Or static before auth exposing `/uploads` |
| `UseMvc` mixed incorrectly with endpoint routing | Duplicate/confusing pipeline |

### 5. Verify with evidence

```bash
dotnet test
# Manual or integration:
curl -i https://localhost:5001/admin
curl -i -H "Authorization: Bearer $TOKEN" https://localhost:5001/admin
curl -i -X OPTIONS https://localhost:5001/api/data \
  -H "Origin: https://evil.example" \
  -H "Access-Control-Request-Method: GET"
```

1. Expect 401/403 without token; 200 with valid authorized token.
2. Evil origin must not receive `Access-Control-Allow-Origin: *` with credentials.
3. Production: no detailed exception page.

### 6. Observe and harden

1. Log authentication failures without logging tokens/passwords.
2. Monitor 401/403 spikes after pipeline changes.
3. Review new middleware PRs for insertion point comments.

### 7. Hand off

1. Document ordered pipeline in README with rationale.
2. Require architecture test or code review checklist item for `UseAuthentication`/`UseAuthorization` adjacency.
3. Link API auth skills for policy design beyond order.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Auth order | Authenticate then Authorize | Reversed |
| CORS | Explicit origins + methods | `AllowAnyOrigin` + credentials |
| Errors | Generic prod handler | Dev exception page in prod |
| Custom MW | Documented position | Random insert “where it worked” |
| Static | Public assets only | Serving `appsettings.json` |
| Tests | Authz integration tests | “Works on my machine browser” |

## Output Checklist

- [ ] TFM, host model, auth schemes recorded
- [ ] Ordered middleware list captured
- [ ] Exception/HSTS/HTTPS placement correct
- [ ] Authentication immediately before Authorization
- [ ] CORS policy tight and ordered correctly
- [ ] Endpoint `RequireAuthorization` / `AllowAnonymous` intentional
- [ ] Positive/negative HTTP evidence collected
- [ ] Custom middleware positions documented
- [ ] `code-quality-standards` applied

## Rules

- Owned apps only; middleware order is a security control.
- Never ship DeveloperExceptionPage to production.
- Do not “fix” CORS by reflecting any Origin.
- Prefer framework endpoint filters/policies over ad-hoc auth in random middleware.
- Focus on pipeline order; route deep JWT abuse testing to auth skills under authorization.
