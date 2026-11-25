---
name: ci-cd-csharp
description: "Applies when creating or modifying CI/CD pipelines for C#/.NET projects. Covers NuGet caching, coverlet coverage, dotnet format, and Roslyn analyzers."
---

# C# / .NET CI/CD

## Setup and caching

Use `actions/setup-dotnet@v4`. For caching, set `NUGET_PACKAGES` and cache it:

```yaml
env:
  NUGET_PACKAGES: ${{ github.workspace }}/.nuget/packages

steps:
  - uses: actions/cache@v4
    with:
      path: ${{ env.NUGET_PACKAGES }}
      key: nuget-${{ runner.os }}-${{ hashFiles('**/packages.lock.json') }}
      restore-keys: nuget-${{ runner.os }}-
```

Enable lockfiles in `.csproj`: `<RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>`.

## Install (frozen)

```bash
dotnet restore --locked-mode
```

## Build and test with coverage

```bash
dotnet build --no-restore --warnaserror
dotnet test --no-build --collect:"XPlat Code Coverage"
# or with coverlet:
dotnet test --no-build /p:CollectCoverage=true /p:CoverletOutputFormat=cobertura /p:Threshold=80
```

## Linting and analyzers

```bash
dotnet format --verify-no-changes
```

Enable Roslyn analyzers in `Directory.Build.props`:

```xml
<PropertyGroup>
  <EnableNETAnalyzers>true</EnableNETAnalyzers>
  <AnalysisLevel>latest-all</AnalysisLevel>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
</PropertyGroup>
```

## Dependency audit

```bash
dotnet list package --vulnerable --include-transitive
```

## C#-specific gotchas

1. Use `--no-restore` on `build` and `--no-build` on `test` to avoid redundant work.
2. NuGet lockfiles (`packages.lock.json`) are opt-in — enable them for reproducible restores.
3. Set `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` in `Directory.Build.props` so it applies to all projects.
4. For multi-TFM projects, coverage gets split per framework — merge with `reportgenerator`.
5. Use `dotnet tool restore` for project-local tools defined in `.config/dotnet-tools.json`.

## Sources

- https://github.com/actions/setup-dotnet
- https://github.com/coverlet-coverage/coverlet
