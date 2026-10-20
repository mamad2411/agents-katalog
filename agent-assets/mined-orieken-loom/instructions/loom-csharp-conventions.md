---
applyTo: "**/*.cs"
---
# C# Conventions

Grounded in `saturday-monorepo-csharp` (the C# port of Saturday, ported from TypeScript) — confirmed
2026-07-07 against that repo's own README, not assumed. This is the most mature of the non-TypeScript
Saturday ports — it has a dedicated reporting package, which Python's port doesn't yet.

## Project Tooling
- **Runtime**: .NET 8.
- **Package management**: NuGet with **Central Package Management** (`Directory.Packages.props`) —
  pin versions once at the solution level, individual `.csproj` files reference packages without a
  version string.
- **Build properties**: centralized via `Directory.Build.props` (nullable reference types, language
  version) rather than repeated per-project.

## Project Structure
Single .NET solution (`.sln`), one project per concern under `src/` (`Saturday.Core`, `Saturday.BDD`,
`Saturday.OTel`, etc. — see below), tests under `tests/` as `Saturday.*.Tests` projects plus
application-specific E2E test projects. Clean architectural boundaries between packages are enforced by
project references, not just convention (see the Saturday-C# dependency graph: `Saturday.BDD` depends on
`Saturday.Core`/`Saturday.Certs`/`Saturday.OTel`, never the reverse).

## Testing & QA Tooling
- **Unit testing framework**: **xUnit** (primary) — used for the Reqnroll BDD scenario bindings
  (`SaturdayWorld` dependency injection). **NUnit** is also supported via a dedicated
  `Saturday.NUnit` adapter package for teams that specifically want it — xUnit is the default, NUnit is
  an accommodated alternative, not a coin-flip between equals.
- **BDD**: [Reqnroll](https://reqnroll.net/) (the actively-maintained successor to SpecFlow) driving
  Gherkin `.feature` files, integrated with xUnit.
- **Browser automation**: Playwright (.NET) — official Microsoft-maintained binding.
- **Fake/synthetic data (faker-equivalent)**: [`Bogus`](https://github.com/bchavez/Bogus) — the de
  facto standard .NET faker library, explicitly inspired by faker.js (same naming lineage as
  `@faker-js/faker`).
- **Factories / fixtures (fishery-equivalent)**: [`AutoFixture`](https://github.com/AutoFixture/AutoFixture)
  — the established .NET auto-generation library for building test objects. Pair with
  [`AutoBogus`](https://github.com/nickdodd79/AutoBogus) to get `Bogus`-quality realistic fake values
  inside `AutoFixture`-generated objects, rather than AutoFixture's own less-realistic defaults.
- **Mutation testing** (ADR-008 clause 2): Stryker.NET — a candidate, **not yet verified** against a
  real project. Verify before relying on its score: a mutant that did not compile, or timed out,
  must never be counted as killed.
- **Performance testing**: k6, via this stack's own `Saturday.K6Exporter` (Playwright request
  logging → structured k6 script generation) and `Saturday.K6Redaction` (sanitizes tokens, auth headers,
  and passwords from exported scripts before they leave the machine).
- **Reporting**: `Saturday.Reporting` / `Saturday.Reporting.Cli` — writes run manifests, bundles
  recorded `.webm` scenario videos, and compiles a single self-contained HTML report with embedded
  playback. This is the reference implementation the other language ports' reporting stories should
  eventually match, not just "a nice extra" — `Saturday.Reporting.Cli` is a real, working example of
  what Python's still-missing reporting package should aim for.

## Other Saturday-C# Packages (context, not testing-specific)
`Saturday.OTel` (OpenTelemetry activity metadata + W3C trace propagation), `Saturday.Certs` (mTLS
credentials, GPU/WebGL launch options), `Saturday.ML` (screenshot diffing and click-telemetry heatmaps
via `SixLabors.ImageSharp`), `Saturday.Swagger` (OpenAPI scenario scaffolding).
