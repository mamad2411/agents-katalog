---
name: ezscim
description: "Guided setup for integrating EzSCIM into an ASP.NET Core project. USE FOR: add SCIM 2.0 endpoint, integrate EzSCIM package, set up SCIM provisioning, implement SCIM users and groups, connect Entra ID provisioning, annotate entity with ScimProperty, implement IUserGroupDataRepository, use EfScimRepositoryBase, register EzSCIM services, add JWT authentication to SCIM API, add SCIM operation callbacks, observe SCIM reads/updates, log SCIM errors in host logger, EzSCIM getting started, EzSCIM IQueryable model, EzSCIM EF Core model. DO NOT USE FOR: SCIM protocol questions unrelated to EzSCIM, non-.NET projects, Azure AD application registration steps."
argument-hint: "Describe your project stack (e.g. ASP.NET Core + EF Core + SQL Server, or ASP.NET Core + Dapper)"
license: MIT
metadata:
  author: miiitch
  docs: https://ezscim.miiitch.dev
---

# EzSCIM Setup

## When to Use

- Add a SCIM 2.0 provisioning endpoint to an ASP.NET Core project
- Connect an existing data source (EF Core, Dapper, Cosmos DB, custom…) to SCIM
- Configure Entra ID (Microsoft) provisioning against a custom API
- Add JWT Bearer authentication to a SCIM endpoint

## Mandatory Questions

Ask all four questions at once before doing any work:

1. `Integration model? (IQueryable / EF Core)`
   — Choose **EF Core** if the project already uses Entity Framework Core.
   — Choose **IQueryable** for any other data source (Dapper, Cosmos DB, custom…).

2. `Group support needed? (Yes / No)`
   — Yes → implement `IUserGroupDataRepository<TUser, TGroup>` / use `EfScimRepositoryBase<TUser, TGroup, TContext>`.
   — No → implement `IUserDataRepository<TUser>` only.

3. `Database / ORM already in use? (free text)`
   — Example: "EF Core + SQL Server", "EF Core + PostgreSQL", "Dapper + MySQL", "none yet"
   — Used to tailor DbContext column types (`nvarchar(max)` vs `jsonb`) and connection strings.

4. `Add JWT Bearer authentication? (Yes / No)`

## Workflow

1. **Detect context** — read existing `Program.cs`, `.csproj`, and entity files if present.
2. **Ask the four mandatory questions** (above).
3. **Choose integration path** based on answers:
   - IQueryable → follow [references/iqueryable.md](references/iqueryable.md)
   - EF Core → follow [references/efcore.md](references/efcore.md)
4. **Generate boilerplate** for each step (entity, repository, DI registration).
5. **Add authentication** if requested → follow [references/authentication.md](references/authentication.md).
6. **Point to the official docs** for any topic not covered here:
   `https://ezscim.miiitch.dev`

## Packages

```bash
# Any data source (IQueryable model)
dotnet add package EzSCIM

# EF Core model — both packages required
dotnet add package EzSCIM
dotnet add package EzSCIM.EfCore
```

## Integration Paths

### Path A — IQueryable

See [references/iqueryable.md](references/iqueryable.md) for the full step-by-step.

Key steps:
1. Annotate entity properties with `[ScimProperty]`
2. Implement `IUserGroupDataRepository<TUser, TGroup>` (or `IUserDataRepository<TUser>`)
3. Register services in `Program.cs`

### Path B — EF Core

See [references/efcore.md](references/efcore.md) for the full step-by-step.

Key steps:
1. Implement `IScimEntity` on entity classes
2. Set up `DbContext` with correct column types
3. Inherit `EfScimRepositoryBase<TUser, TGroup, TContext>`
4. Register services in `Program.cs`

## Authentication

See [references/authentication.md](references/authentication.md).

Add to `Program.cs`:

```csharp
builder.Services.AddJwtTokenService();
builder.Services.AddAuthentication()
    .AddScheme<JwtBearerTokenAuthenticationOptions, JwtBearerTokenAuthenticationHandler>(
        "Bearer", null);
builder.Services.AddAuthorization();
```

Configure in `appsettings.json`:
```json
{
  "Jwt": {
    "SecretKey": "<at-least-32-char-secret>",
    "ExpirationMinutes": 1440
  }
}
```

> ⚠️ Never commit the secret key. Use environment variables or Azure Key Vault in production.

For local testing, expose the token endpoint:
```csharp
builder.Services.AddScimTokenGeneratorEndpoint(); // disabled automatically in production
```

## Observability (optional)

See [references/observability.md](references/observability.md).

Lets a host app register callbacks for SCIM operations (last read, last update, etc.) and capture
errors for its own logging/monitoring — fully optional, does not replace EzSCIM's internal `ILogger<T>`
logging, zero overhead if never registered.

```csharp
builder.Services.AddScoped<IScimRepository, MyScimRepository>();
builder.Services.AddScimOperationCallback<MyScimMonitoringCallbacks>(); // must come after IScimRepository
```

## SCIM Endpoints Exposed

Once registered, EzSCIM mounts the following routes:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/scim/Users` | List / filter users |
| POST | `/scim/Users` | Create user |
| GET | `/scim/Users/{id}` | Get user |
| PUT | `/scim/Users/{id}` | Replace user |
| PATCH | `/scim/Users/{id}` | Partial update |
| DELETE | `/scim/Users/{id}` | Delete user |
| GET | `/scim/Groups` | List / filter groups (if enabled) |
| POST/GET/PUT/PATCH/DELETE | `/scim/Groups/{id}` | Group CRUD |
| GET | `/scim/Schemas` | Schema discovery |
| GET | `/scim/ServiceProviderConfig` | Capabilities |

## Entra ID Configuration

1. Azure Portal → **Microsoft Entra ID → Enterprise Applications**
2. Select your app → **Provisioning → Admin Credentials**
3. **Tenant URL**: `https://your-domain.com/scim`
4. **Secret Token**: full JWT with `Bearer` prefix
5. Click **Test Connection**

Full guide: [https://ezscim.miiitch.dev/authentication/#6-configure-entra-id-microsoft](https://ezscim.miiitch.dev/authentication/#6-configure-entra-id-microsoft)

## Quality Checklist

- [ ] Entity properties annotated with `[ScimProperty]` (IQueryable) or `IScimEntity` implemented (EF Core)
- [ ] `IQueryable<T>` returned from `QueryUsers()` / `QueryGroups()` (not `IEnumerable<T>`)
- [ ] `IScimRepository` registered in DI
- [ ] Filter translators registered (`GenericScimFilterTranslator<T>`) for IQueryable path
- [ ] `app.UseAuthentication()` and `app.UseAuthorization()` called in correct order
- [ ] JWT secret key is at least 32 characters and not committed to Git
- [ ] JSON columns (`EmailsJson`, `MembersJson`) handled in `OnBeforeUpdateUserAsync` / `OnBeforeUpdateGroupAsync` (EF Core path)
- [ ] `userName` is unique-indexed in the database
- [ ] Operation callbacks (if used) are registered via `AddScimOperationCallback` — never required
