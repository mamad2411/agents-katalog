---
name: backend-architecture
description: Use when adding or changing an endpoint, business rule, model or repository in the .NET backend (backend/). Explains the layers, auth and the checklist for a new feature.
---

# Backend architecture

ASP.NET Core minimal APIs on .NET 10. Nullable on, warnings are errors.

## Layers

| Folder | Holds | Rules |
|---|---|---|
| `Domain/` | Entities (`User`, `FeatureFlag`, `Item`) | No framework code |
| `Data/` | Repository interfaces + implementations, seed data | Endpoints never touch storage directly |
| `Auth/` | `AccountService` (account rules), `Tokens`, `CurrentUserFilter` | Rules live here, not in endpoints |
| `Contracts/` | Request/response records | Never return domain entities from endpoints |
| `Endpoints/` | One static class per area, `Map…Endpoints` | Thin: validate, call a service/repository, map to a contract |
| `Program.cs` | Composition root | Only place that registers implementations |

## Auth

- Bearer tokens (`AddBearerToken`). Sign-in returns `{ accessToken, expiresIn, refreshToken }`.
- Signed-in endpoints: `.RequireAuthorization().AddEndpointFilter<CurrentUserFilter>()`, then `CurrentUserFilter.Get(http)`.
- Admin endpoints: `.RequireAuthorization(Tokens.AdminPolicy)`.
- Sign-out and access changes rotate `User.SecurityStamp`, which invalidates old tokens.

## Checklist: new feature

1. Model in `Domain/`, storage behind an interface in `Data/` (in-memory first).
2. Rules in a service with unit tests.
3. Contracts in `Contracts/`; validation returns `Results.ValidationProblem` with field names in camelCase.
4. Endpoints in `Endpoints/`, mapped in `Program.cs`.
5. Integration tests through `ApiFactory`.
6. If it is switchable, add a feature flag to `InMemoryFeatureFlagRepository` and to the defaults in every app.
7. Update the API table in `backend/README.md` and every app that uses the endpoint.
