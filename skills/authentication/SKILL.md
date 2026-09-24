---
name: authentication
description: >
  Authentication and authorization for ASP.NET Core. Covers JWT bearer tokens,
  OpenID Connect, ASP.NET Identity, authorization policies, role and claim-based
  authorization, and API key authentication.
  Load this skill when implementing login, protecting endpoints, designing
  authorization rules, or when the user mentions "auth", "JWT", "bearer token",
  "OIDC", "OpenID Connect", "Identity", "claims", "roles", "authorize",
  "RequireAuthorization", "API key", or "cookie auth".
---

# Authentication & Authorization

## Core Principles

1. **Use ASP.NET Identity for user management** — Don't build your own user store. Identity handles password hashing, lockout, two-factor, email confirmation, and (since .NET 10) built-in passkey/WebAuthn support for passwordless login.
2. **JWT for APIs, cookies for web apps** — APIs use Bearer token authentication; Blazor/MVC apps use cookie authentication.
3. **Policy-based authorization over roles** — Policies are testable, composable, and more expressive than `[Authorize(Roles = "Admin")]`.
4. **Never store secrets in code** — Use user secrets in development, Azure Key Vault / environment variables in production.

## Patterns

### JWT Bearer Authentication

```csharp
// Program.cs
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]!)),
            ClockSkew = TimeSpan.Zero
        };
    });

builder.Services.AddAuthorization();
```

### Token Generation

Use `JsonWebTokenHandler` from `Microsoft.IdentityModel.JsonWebTokens` — it is the maintained, span-based handler that ASP.NET Core itself validates with. `JwtSecurityTokenHandler` (System.IdentityModel.Tokens.Jwt) is the legacy stack.

```csharp
public sealed class TokenService(IConfiguration config, TimeProvider clock)
{
    private static readonly JsonWebTokenHandler TokenHandler = new();

    public string GenerateToken(User user, IEnumerable<string> roles)
    {
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(config["Jwt:Key"]!));
        var now = clock.GetUtcNow();

        var descriptor = new SecurityTokenDescriptor
        {
            Issuer = config["Jwt:Issuer"],
            Audience = config["Jwt:Audience"],
            IssuedAt = now.UtcDateTime,
            Expires = now.AddHours(1).UtcDateTime,
            Claims = new Dictionary<string, object>
            {
                [JwtRegisteredClaimNames.Sub] = user.Id,
                [JwtRegisteredClaimNames.Email] = user.Email!,
                [JwtRegisteredClaimNames.Name] = user.UserName!,
                ["roles"] = roles.ToArray()
            },
            SigningCredentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256)
        };

        return TokenHandler.CreateToken(descriptor);
    }
}
```

### Policy-Based Authorization

```csharp
// Define policies
builder.Services.AddAuthorizationBuilder()
    .AddPolicy("AdminOnly", policy => policy.RequireRole("Admin"))
    .AddPolicy("CanManageOrders", policy => policy
        .RequireAuthenticatedUser()
        .RequireClaim("permission", "orders:write"))
    .AddPolicy("MinimumAge", policy => policy
        .AddRequirements(new MinimumAgeRequirement(18)));

// Custom requirement + handler
public class MinimumAgeRequirement(int minimumAge) : IAuthorizationRequirement
{
    public int MinimumAge => minimumAge;
}

public class MinimumAgeHandler(TimeProvider clock) : AuthorizationHandler<MinimumAgeRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        MinimumAgeRequirement requirement)
    {
        var dateOfBirthClaim = context.User.FindFirst("date_of_birth");
        if (dateOfBirthClaim is not null &&
            DateOnly.TryParse(dateOfBirthClaim.Value, out var dob) &&
            dob.AddYears(requirement.MinimumAge) <= DateOnly.FromDateTime(clock.GetUtcNow().DateTime))
        {
            context.Succeed(requirement);
        }
        return Task.CompletedTask;
    }
}
```

### Protecting Endpoints

```csharp
// Protect an entire group
app.MapGroup("/api/admin")
    .WithTags("Admin")
    .RequireAuthorization("AdminOnly")
    .MapAdminEndpoints();

// Protect individual endpoints
group.MapPost("/", CreateOrder)
    .RequireAuthorization("CanManageOrders");

// Allow anonymous on a protected group
group.MapGet("/public-info", GetPublicInfo)
    .AllowAnonymous();
```

### OpenID Connect (External Identity Provider)

```csharp
builder.Services.AddAuthentication(options =>
{
    options.DefaultScheme = CookieAuthenticationDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = OpenIdConnectDefaults.AuthenticationScheme;
})
.AddCookie()
.AddOpenIdConnect(options =>
{
    options.Authority = builder.Configuration["Oidc:Authority"];
    options.ClientId = builder.Configuration["Oidc:ClientId"];
    options.ClientSecret = builder.Configuration["Oidc:ClientSecret"];
    options.ResponseType = "code";
    options.SaveTokens = true;
    options.Scope.Add("openid");
    options.Scope.Add("profile");
    options.Scope.Add("email");
});
```

### Accessing Current User

```csharp
// In minimal API handlers — inject ClaimsPrincipal or HttpContext
group.MapGet("/me", (ClaimsPrincipal user) =>
{
    var userId = user.FindFirstValue(ClaimTypes.NameIdentifier);
    var email = user.FindFirstValue(ClaimTypes.Email);
    return TypedResults.Ok(new { userId, email });
}).RequireAuthorization();
```

## Anti-patterns

### Don't Use Role Strings Everywhere

```csharp
// BAD — magic strings, hard to refactor, not testable
[Authorize(Roles = "Admin,SuperAdmin,Manager")]
public class AdminController { }

// GOOD — policy-based
builder.Services.AddAuthorizationBuilder()
    .AddPolicy("AdminAccess", p => p.RequireRole("Admin", "SuperAdmin", "Manager"));

group.MapGet("/", Handler).RequireAuthorization("AdminAccess");
```

### Don't Store Secrets in appsettings.json

```json
// BAD — committed to source control
{
  "Jwt": {
    "Key": "super-secret-key-12345"
  }
}
```

```bash
# GOOD — use user secrets in development
dotnet user-secrets set "Jwt:Key" "super-secret-key-12345"
```

### Don't Skip Token Validation

```csharp
// BAD — disabling validation
options.TokenValidationParameters = new TokenValidationParameters
{
    ValidateIssuer = false,      // DON'T
    ValidateAudience = false,    // DON'T
    ValidateLifetime = false,    // DEFINITELY DON'T
};

// GOOD — validate everything (see JWT Bearer Authentication pattern above for full setup)
```

## Decision Guide

| Scenario | Recommendation |
|----------|---------------|
| REST API | JWT Bearer authentication |
| Blazor Server / MVC | Cookie authentication |
| External identity provider | OpenID Connect |
| User registration / login | ASP.NET Identity |
| Passwordless login | ASP.NET Identity passkeys (WebAuthn, built-in since .NET 10) |
| Permission checking | Policy-based authorization |
| Multi-tenant API | Claims-based with tenant claim |
| API-to-API communication | Client credentials (OAuth 2.0) |
| Simple API keys | Custom `AuthenticationHandler<T>` |
