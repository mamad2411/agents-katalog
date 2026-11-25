# Roslyn C# Context Indexing

## Purpose
Build and query code-context indexes for C# and .NET solutions using the Roslyn compiler platform: MSBuild workspace loading, syntax-tree and semantic-model symbol extraction, reference and implementation search, type-hierarchy expansion, and incremental reindexing keyed on document versions for AI agent context retrieval.

## Use when
- An agent needs accurate C# symbols, find-references results, interface implementations, or base-derived type chains from a `.sln` or `.csproj` codebase.
- The .NET 8 SDK with MSBuildLocator and Microsoft.CodeAnalysis 4.11 or newer is available in the environment.
- Index freshness must track per-document edits without reloading whole solutions.
- Query answers must fit a fixed token budget with deterministic ranking.

## Do not use when
- The target language is not C#, F#, or VB.NET on the Roslyn platform; use the matching engine skill instead.
- Only file-level grep is required with no need for overload resolution, generics instantiation, or cross-project references.
- No buildable solution or project file exists and semantic models therefore cannot be constructed.

## Required context
- Solution or project path, target frameworks such as net8.0, and the Roslyn version in use, for example 4.11.0.
- Token budget for a single query answer: at most 40 symbols and 12000 tokens of emitted context.
- Performance targets: solution load time, query p95 latency, and the golden symbol recall set.
- Exclusion list for generated files such as obj/, bin/, and designer outputs.

## Procedure
1. **Load the workspace**: register the .NET 8 SDK with `MSBuildLocator.RegisterDefaults()`, then call `MSBuildWorkspace.OpenSolutionAsync` on `Billing.sln`. Fail loudly if any of the 14 projects report load diagnostics, and record the Roslyn version in the spec.
2. **Extract symbols**: walk each document `SyntaxTree` for `ClassDeclaration`, `MethodDeclaration`, `PropertyDeclaration`, and `InterfaceDeclaration` nodes, resolve each through `SemanticModel.GetDeclaredSymbol`, and store the fully qualified metadata name, `ISymbol` kind, containing assembly, file, and line span.
3. **Index references and hierarchies**: run `SymbolFinder.FindReferencesAsync` for cross-project call sites and `SymbolFinder.FindImplementationsAsync` for interface members, then expand `INamedTypeSymbol.BaseType` plus `AllInterfaces` chains up to 3 levels. Cap hierarchy payloads at 60 nodes per query.
4. **Reindex incrementally**: key freshness on Roslyn document `VersionStamp`; on change, re-resolve only documents whose version advanced plus their direct dependents. Purge rows for removed documents in the same pass.
5. **Serve ranked queries**: expose `symbols --name 'Billing.Invoices.InvoiceCalculator'`, `refs --symbol <metadata-name>`, and `hierarchy --type <metadata-name> --depth 3`. Rank exact metadata-name matches first, then same-project proximity, then dependency-distance hops, then recency, truncating at the 40-symbol and 12000-token caps.
6. **Verify against goldens**: run `scripts/verify.sh`, assert query p95 under 300 ms on a warm solution, and require 100% recall on the checked-in golden set covering overloads, explicit interface implementations, and generic instantiations.

## Decision rules
- **Semantic model is truth**: syntax-only matches are hints, never answers; every reported symbol must resolve through a `SemanticModel`.
- **Metadata name is identity**: symbols are keyed by fully qualified metadata name plus containing assembly, never by file plus line.
- **Generated code is quarantined**: obj/, bin/, and `*.Designer.cs` files are excluded from ranking and listed separately, never silently merged.
- **Bounded hierarchies always**: type-hierarchy expansion stops at depth 3 or 60 nodes, whichever comes first.
- **Load diagnostics are fatal**: a solution that loads with errors produces no index until the diagnostics are resolved or explicitly waived with justification.

## Evidence required
- Index specification following `templates/roslyn-context-indexing-spec.md` with solution, frameworks, and Roslyn version.
- Symbol and reference row counts plus the generated-code exclusion list.
- Golden recall log covering overloads, explicit implementations, and generics, with measured query p95.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Loaded Roslyn solution with per-project load diagnostics report.
- Queryable symbol, reference, implementation, and type-hierarchy index.
- Golden recall and latency report proving the index meets its targets.

## Stop conditions
- Golden symbol recall reaches 100% with query p95 under 300 ms on a warm solution.
- Single-document edit reindexes in under 4 seconds including dependents.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the .NET build owner if the solution fails to load due to missing SDK workloads, broken project references, or unrestorable NuGet packages.
- Escalate to the lead architect if source generators produce symbols the indexer cannot resolve deterministically.
