---
name: security-backend
description: Backend security hardening for BallastLane (beyond the auth flow itself) — secrets management via user-secrets/Options, BCrypt password hashing, cookie-based JWT specifics, strict token validation params, CORS with AllowCredentials, HTTPS-required-locally, refresh-token gaps, and logging PII. Load this skill when configuring secrets/CORS/HTTPS, reviewing security, or adding a protected endpoint. For the step-by-step auth implementation, use the jwt-auth skill instead.
---

# Security — Backend

This skill is the *hardening/configuration* view. For the worked register/login/protect walkthrough, see the `jwt-auth` skill; they're complementary.

## Secrets Management

- **Never hardcode the SQL Server connection string, JWT signing key (`JwtSettings.Secret`), or any credential in source.** Use `dotnet user-secrets` locally; environment variables or a secrets manager in any deployed environment. Bind via the Options pattern (`IOptions<JwtSettings>`) — just make sure the underlying value comes from configuration, not a hardcoded default.

```csharp
// DO
var conn = builder.Configuration.GetConnectionString("Database");
builder.Services.Configure<JwtSettings>(builder.Configuration.GetSection("Jwt")); // Secret from config/user-secrets

// DON'T
var conn = "Server=localhost;Database=BallastLane;User Id=sa;Password=hunter2;";
```

- **`appsettings.Development.json` with real credentials, `.env` files, and any secrets file are gitignored.** Seed data (demo credentials) is fine to keep in a seed script — that's intentionally public/demo data, not a real secret.

## Password Hashing — Confirmed Real Pattern

- **BCrypt via `BCrypt.Net.BCrypt`**, confirmed in `Infrastructure/Hasher/PasswordHasher.cs` — keep using this rather than rolling a custom scheme.

```csharp
public class PasswordHasher : IPasswordHasher
{
    public string HashPassword(string password) => BCrypt.Net.BCrypt.HashPassword(password);
    public bool VerifyPassword(string password, string hashedPassword) => BCrypt.Net.BCrypt.Verify(password, hashedPassword);
}
// DON'T: user.PasswordHash = request.Password; // plaintext
```

## JWT Authentication — Cookie-Based, Confirmed Real Pattern

⚠️ This backend does **not** use the `Authorization: Bearer` header / standard `AddJwtBearer()` middleware. It uses **HttpOnly cookies + a custom `AuthenticationHandler`**. Any new protected endpoint relies on this scheme, not a bearer token.

- **Access token (JWT) and refresh token are both delivered as cookies**, set by the controller after the handler returns them in its response DTO — never set from inside a MediatR handler (`Response.Cookies` requires `HttpContext`, which stays out of Application).

```csharp
Response.Cookies.Append("authToken", response.AccessToken, new CookieOptions
{
    HttpOnly = true, Secure = true, SameSite = SameSiteMode.None, Expires = response.AccessTokenExpiry
});
```

- **`HttpOnly = true` and `Secure = true` are both required.** Combined with `SameSite = None`, this requires HTTPS **even in local development** for the cookie to be sent at all — over plain `http://` the browser silently drops these cookies. Run the API over HTTPS locally (`dotnet run --launch-profile https`), or auth won't work.
- **A custom `AuthenticationHandler` reads the cookie and validates it**, delegating to `IJwtValidatorService` (`CookieJwtAuthHandler`). On an invalid token it explicitly deletes the cookie (`Response.Cookies.Delete("authToken")`) before failing — keep that cleanup when extending the handler.
- **Token validation parameters are strict**, confirmed real: `ValidateIssuer`, `ValidateAudience`, `ValidateLifetime`, `ValidateIssuerSigningKey` all `true`, `ClockSkew = TimeSpan.Zero`. Don't loosen these for convenience — if expiry testing is annoying, shorten `AccessTokenExpiryMinutes` in config instead of disabling `ValidateLifetime`.
- **Explicit `[Authorize]` or `[AllowAnonymous]` on every controller/action.** `register`/`login`/`refresh` are `[AllowAnonymous]`; `logout`/`validate` and all of `TasksController` require a valid `authToken` cookie.

## Refresh Token Handling — Real Pattern + Flagged Gaps

- **Generation:** `RandomNumberGenerator.GetBytes` on 32 bytes, base64-encoded — confirmed real and solid (cryptographically random, not a JWT).
- ⚠️ **Currently stored in plaintext** on `UserDomain.RefreshToken`. **Recommended upgrade:** hash it before persisting and compare hashes on lookup during `/refresh`. A database read alone shouldn't hand out a directly usable refresh token.
- ⚠️ **No rotation-with-reuse-detection.** Each login/refresh overwrites the previous value via `SetRefreshToken`. **Recommended upgrade:** on `/refresh`, issue a new refresh token and invalidate the old one; if an already-invalidated token is presented again, treat it as compromise and force logout. Not required for this exercise's scope.
- **UTC for all token expiry math**, even though business-facing timestamps elsewhere use a Peru-timezone helper — confirmed real and correct. Keep the split: **anything security/protocol-facing stays UTC.**

## Input Validation

- **Duplicate-check for registration is done in the handler, not a separate Validator** — confirmed real: `SignUpHandler` calls `GetByUsernameAsync`/`GetByEmailAsync` before insert. If you introduce FluentValidation for `Task` use cases, that's a valid addition — Auth doesn't have a `Validator` file to mirror.
- **Entity-level guard clauses double as input validation** — `UserDomain`'s constructor throws `ArgumentNullException` on null `username`/`passwordHash`/`email`. Keep true invariants in Domain; API-shape checks (well-formed email) belong at the boundary.
- **Parameterized queries only** via EF Core (default) — no raw SQL string concatenation.

## Transport & CORS

- **HTTPS enforced**, and **actually required locally too** (per the `Secure=true` cookie note above).
- **CORS must allow credentials explicitly.** Cookie-based cross-origin auth (`SameSite=None`) requires `AllowCredentials()` plus a named origin. `AllowAnyOrigin()` is incompatible with `AllowCredentials()` in ASP.NET Core — the explicit origin *and* `AllowCredentials()` both need to be present.

```csharp
builder.Services.AddCors(o => o.AddPolicy("Angular", p =>
    p.WithOrigins("https://localhost:4200")
     .AllowAnyMethod()
     .AllowAnyHeader()
     .AllowCredentials()));
```

## Logging

- **No plaintext passwords or raw token values logged** — confirmed real code respects this (logs token *length*, e.g. `AccessLength`, not the token itself).
- ⚠️ **Username is logged at Information level** in multiple places (`LogInHandler`, `AuthController`). If usernames are sensitive (emails/real names), consider `Debug` instead, consistent with "no PII at Information level." A conscious decision, not a default.
