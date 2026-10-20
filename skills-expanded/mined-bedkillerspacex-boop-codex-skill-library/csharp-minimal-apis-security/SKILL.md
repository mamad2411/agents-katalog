---
name: csharp-minimal-apis-security
description: >
  Secure ASP.NET Core Minimal APIs on owned apps: authentication, authorization
  policies, endpoint filters, anti-forgery for cookie apps, secrets, HTTPS, rate
  limits, and validation. Use when building or reviewing MapGet/MapPost APIs,
  JWT bearer setups, or migrating controllers to minimal endpoints without
  dropping authz.
---

# C# Minimal APIs Security

## Scope And Authorization

- **In scope:** ASP.NET Core Minimal API projects you develop or are authorized to assess.
- **Out of scope:** Attacking third-party APIs; disabling auth “to debug prod” without ticketed break-glass.
- Prefer integration tests proving anonymous access is denied.
- Redact JWTs and connection strings.
- Pair with `code-quality-standards`, `csharp-style-conventions`, and CSRF/CORS skills as needed.

## When To Use

- New Minimal API surface (`MapGroup`, `MapGet`, `MapPost`, …).
- Ensuring `.RequireAuthorization()` is not forgotten on sensitive routes.
- Cookie + SPA or BFF patterns with antiforgery.
- JWT bearer validation parameters review.
- Adding rate limiting, request size limits, and problem details without leaking stacks.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full CSRF deep dive | `csrf-cross-site-request-forgery` |
| CORS allowlists | CORS skills |
| Channels pipelines | `csharp-channels-pipelines` |
| Style/naming only | `csharp-style-conventions` |
| Implementation quality baseline | `code-quality-standards` |

## Threat focus for Minimal APIs

| Risk | Footgun | Control |
| --- | --- | --- |
| Missing authz | Open `MapPost` by default | `RequireAuthorization` / fallback policy |
| IDOR | Trust route ids only | Resource-based authz / checks |
| Mass assignment | Bind full entity | DTO + validation |
| JWT misconfig | `ValidateAudience = false` | Strict metadata |
| Secrets | `appsettings.json` prod secrets | User secrets / KeyVault / env |
| CSRF | Cookie auth without token | Antiforgery on mutating endpoints |
| Info leak | Dev exception page in prod | Exception handler |

## Workflow

### 1. Confirm scope and success criteria

1. Auth modes (JWT, cookies, mTLS), public vs private endpoints list.
2. Success: unauthenticated calls get 401; forbidden 403; tests cover both; scanners clean for trivial issues.

### 2. Inventory endpoints

```bash
rg -n 'Map(Get|Post|Put|Patch|Delete)|MapGroup' --glob '*.cs'
rg -n 'RequireAuthorization|AllowAnonymous|AddAuthentication|AddAuthorization' --glob '*.cs'
```

### 3. Authentication & authorization baseline

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddAuthentication().AddJwtBearer(o =>
{
    o.Authority = builder.Configuration["Auth:Authority"];
    o.Audience = builder.Configuration["Auth:Audience"];
    o.TokenValidationParameters.ValidateAudience = true;
    o.TokenValidationParameters.ValidateIssuer = true;
});
builder.Services.AddAuthorization(o =>
{
    o.FallbackPolicy = new AuthorizationPolicyBuilder()
        .RequireAuthenticatedUser()
        .Build();
    o.AddPolicy("Admin", p => p.RequireRole("admin"));
});

var app = builder.Build();
app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();

var api = app.MapGroup("/api/v1");
api.MapGet("/health", () => Results.Ok(new { status = "ok" }))
   .AllowAnonymous();

api.MapGet("/me", (ClaimsPrincipal user) => Results.Ok(new { sub = user.Identity?.Name }))
   .RequireAuthorization();

api.MapDelete("/admin/users/{id}", (string id) => Results.NoContent())
   .RequireAuthorization("Admin");

app.Run();
```

**Middleware order:** routing → authn → authz → endpoints. Do not skip `UseAuthentication`/`UseAuthorization` when using endpoint metadata auth.

### 4. Validation and filters

```csharp
api.MapPost("/items", async (CreateItemDto dto, IValidator<CreateItemDto> v) =>
{
    var result = await v.ValidateAsync(dto);
    if (!result.IsValid) return Results.ValidationProblem(result.ToDictionary());
    // persist...
    return Results.Created($"/api/v1/items/{id}", null);
});
```

Use `IValidatableObject` / FluentValidation / data annotations consistently. Bind DTOs, not EF entities.

### 5. Cookie + antiforgery (if applicable)

1. For browser cookie sessions, add antiforgery tokens on unsafe methods.
2. Prefer API bearer tokens for pure SPA+API when design allows (still apply CORS carefully).
3. Set cookie flags: `HttpOnly`, `Secure`, `SameSite`.

### 6. Hardening checklist items

```csharp
builder.WebHost.ConfigureKestrel(o => o.Limits.MaxRequestBodySize = 1_048_576);
builder.Services.AddRateLimiter(_ => /* per-endpoint policies */);
// app.UseRateLimiter();
```

1. `dotnet list package --vulnerable`
2. Disable detailed errors in prod.
3. HTTPS redirection + HSTS at edge or app.
4. Secrets from configuration providers, not source.

### 7. Verify

```bash
dotnet test
curl -sSI https://localhost:7xxx/api/v1/me   # expect 401 without token
curl -sS https://localhost:7xxx/api/v1/me -H "Authorization: Bearer $TOKEN"
```

Integration tests: `WebApplicationFactory` with anonymous and authorized clients.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Default authz | FallbackPolicy authenticated | Opt-in auth forgotten on new routes |
| JWT | Validate iss/aud/lifetime | Symmetric key in repo + no aud |
| Input | DTO + validate | `MapPost((JsonElement body) => …)` unchecked |
| Errors | ProblemDetails | Exception stack to clients |
| Cookies | Antiforgery + SameSite | Cookie auth CSRF-open |

## Output Checklist

- [ ] Endpoint inventory with auth metadata
- [ ] Fallback or explicit authz on sensitive routes
- [ ] JWT/cookie config reviewed
- [ ] DTO validation on writes
- [ ] CSRF story for cookie auth
- [ ] Rate limits / body limits considered
- [ ] Package vulnerability scan
- [ ] 401/403 tests automated
- [ ] Secrets not in git
- [ ] Residual risks documented

## Rules

- New Minimal API routes inherit no magic security — be explicit.
- Fail closed on authorization middleware order mistakes.
- Authorized apps only; focus on **Minimal API security wiring**.
