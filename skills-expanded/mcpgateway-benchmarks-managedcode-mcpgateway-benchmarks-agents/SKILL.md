# AGENTS.md

Project: ManagedCode.MCPGateway.Benchmarks
Owned by: ManagedCode.MCPGateway package maintainers

Parent: `../../AGENTS.md`

## Purpose

- This project owns BenchmarkDotNet performance and allocation benchmarks for `ManagedCode.MCPGateway`.
- It measures representative package hot paths without becoming a shipping runtime dependency.

## Entry Points

- `Program.cs`
- `BenchmarkCatalog.cs`
- `McpGatewayIndexBuildBenchmarks.cs`
- `McpGatewaySearchBenchmarks.cs`
- `McpGatewayToolSetBenchmarks.cs`

## Boundaries

- In scope: benchmark scenarios, benchmark catalog fixtures, allocation/runtime measurement, and benchmark documentation.
- Out of scope: production runtime code, integration tests, CI release gates, and test-only assertion helpers.
- Protected or high-risk areas: benchmark realism, stable input data, Release-only execution, and avoiding benchmark-only changes in production code.

## Project Commands

- `benchmark`: `dotnet run -c Release --project benchmarks/ManagedCode.MCPGateway.Benchmarks/ManagedCode.MCPGateway.Benchmarks.csproj -- --filter "*"`
- `benchmark-search`: `dotnet run -c Release --project benchmarks/ManagedCode.MCPGateway.Benchmarks/ManagedCode.MCPGateway.Benchmarks.csproj -- --filter "*Search*"`
- `benchmark-index`: `dotnet run -c Release --project benchmarks/ManagedCode.MCPGateway.Benchmarks/ManagedCode.MCPGateway.Benchmarks.csproj -- --filter "*Index*"`
- `benchmark-tools`: `dotnet run -c Release --project benchmarks/ManagedCode.MCPGateway.Benchmarks/ManagedCode.MCPGateway.Benchmarks.csproj -- --filter "*ToolSet*"`

## Applicable Skills

- `mcaf-dotnet`
- `mcaf-dotnet-profiling`
- `mcaf-dotnet-format`
- `mcaf-dotnet-roslynator`
- `mcaf-solid-maintainability`

## Local Constraints

- Run benchmarks in `Release`.
- CI and release benchmark coverage run the complete BenchmarkDotNet suite with `--filter "*"`; do not replace it with smoke-only, dry-run, or short-run benchmark coverage.
- Keep benchmark fixtures deterministic and network-free.
- Keep benchmark methods focused on one measurable operation.
- Use BenchmarkDotNet `MemoryDiagnoser` so allocations are visible with mean timing.
- Do not optimize production code only for a synthetic benchmark shape; the scenario must represent a real gateway path.
