---
name: dotnet-build-and-runtime
description: Apply when touching the .slnx file, project files, OpenAPI / Scalar config, Docker compose, or .NET 10 toolchain quirks for the api/ build and runtime.
metadata:
  stack: [dotnet]
---

# .NET 10 build & runtime gotchas

These are the easy-to-miss things about the api/ build, OpenAPI, and Docker setup. Each line saved someone an hour at some point.

## Solution format

- .NET 10 uses **`.slnx`**, not `.sln`. The repo's solution file is `<api-root>/<Solution>.slnx`. Build / test / format commands target the `.slnx`.

## OpenAPI

- `Microsoft.AspNetCore.OpenApi` uses **Microsoft.OpenApi v2**. Types live in the `Microsoft.OpenApi` namespace, **not** `Microsoft.OpenApi.Models`.
- `MapOpenApi()` and `MapScalarApiReference()` both need `.AllowAnonymous()` because `Program.cs` sets a global authenticated-user `FallbackPolicy`. Without it, hitting the spec or the Scalar UI returns 401.
- Scalar UI: `http://localhost:5001/scalar/v1`. OpenAPI spec: `http://localhost:5001/openapi/v1.json`. Both Development only.

## Infrastructure project

- `Infrastructure.csproj` requires `<FrameworkReference Include="Microsoft.AspNetCore.App" />` even though it's a class library. Without it, ASP.NET Core types (e.g. `IHttpContextAccessor`) won't resolve.

## Docker

- API listens **internally** on `8080`; exposed on host `5001`.
- SPA listens on `:3000`. The `spa` compose service is gated behind the **`full` profile** — the default `docker compose up` does **not** start it. To get the SPA: `docker compose --profile full up`.
- Networking:
  - In compose, the SPA calls the API via `http://api:8080`.
  - In bare-metal dev (running `dotnet run` + `pnpm dev` on the host), the SPA calls the API via `http://localhost:5001`.
- Mobile-app talks to the API by the same URLs; pick the right one for the target environment.

## Test commands

- `dotnet test <api-root>/<Solution>.slnx` — full suite (domain unit + application unit + api integration).
- `dotnet test <api-root>/tests/<Solution>.Domain.UnitTest` — domain only.
- xUnit + FluentAssertions + FakeItEasy.

## Anti-patterns

- Editing `<Solution>.sln` (doesn't exist) instead of `.slnx`.
- Using `Microsoft.OpenApi.Models` namespace — that's the old v1 surface, removed in v2.
- Hitting `/openapi/v1.json` or `/scalar/v1` in non-Development environments and being confused by 404 — both routes are guarded by `app.Environment.IsDevelopment()`.
- `docker compose up` and wondering why the SPA isn't reachable on `:3000` — need the `full` profile.
- Calling the API from inside the compose-deployed SPA via `localhost` — that's the SPA container's localhost, not the host.
