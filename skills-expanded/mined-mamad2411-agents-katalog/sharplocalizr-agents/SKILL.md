# SharpLocalizr Agent Guide

## Purpose
SharpLocalizr is a .NET 10 application for localizing resource data. The current solution is organized around Domain, Application, Infrastructure, Composition, and the ASP.NET/Blazor host under `src/`. Preserve this architecture when implementing localization features.

## Repository structure
- `src/Localizr.Domain`: domain entities and domain rules. Keep infrastructure concerns out.
- `src/Localizr.Application`: feature abstractions, Requests, Commands/Queries, handlers, validators, common responses, repositories and unit-of-work abstractions.
- `src/Localizr.Infrastructure`: concrete services, persistence and external integrations.
- `src/Localizr.Composition`: dependency-injection/composition extensions.
- `src/Localizr`: ASP.NET Core host, controllers and Razor/Blazor UI.
- `tests/Localizr.UnitTests`: deterministic unit tests for Application, Infrastructure and host behavior that can be exercised without external infrastructure.

The existing Identity flow is the reference implementation: controllers receive feature Requests, construct Mediator messages, handlers call an application abstraction/service, and the service owns the feature operation. The current controller follows this pattern directly, and the handler delegates to `IIdentityService`. Do not introduce a parallel CQRS style without a strong reason.

## Architectural rules
1. HTTP input belongs in a feature `Requests` DTO; do not expose domain entities from controllers.
2. Controllers translate Requests into `Command`/`Query` objects and call `IMediator.Send`.
3. Command/query handlers are thin orchestration components. They validate through the existing pipeline and call the feature service.
4. Feature services contain the use-case implementation. If persistence is needed, inject `IRepository<T>` (and `IUnitOfWork` when appropriate) and work with Domain entities.
5. Infrastructure implements Application abstractions. External providers such as Google Translate belong behind an Application abstraction and are implemented in Infrastructure.
6. Responses should follow the existing `Response<T>`/feature-response conventions instead of inventing a second response envelope.
7. Use `async`/`await` correctly for asynchronous work. Never block asynchronous I/O with `.Result`, `.Wait()`, or equivalent synchronous waits.
8. Always propagate `CancellationToken` through every asynchronous application, service, repository, HTTP, file and test operation where the API supports cancellation.
9. Keep Blazor/Razor UI concerns in the host. A page may call Mediator directly when it is a trusted in-process UI, or call the HTTP controller when the page is intended to behave like an API client. Pick one deliberately and document it.
10. Never put Google credentials, API keys, or provider-specific secrets in Domain/Application or source-controlled configuration.
11. Keep the initial JSON implementation extensible: parsing and writing must be isolated so future .NET `.resx`, Java, and other resource formats can be added without changing translation orchestration.
12. Follow current .NET 10 APIs and practices. Do not preserve obsolete patterns solely for compatibility with older .NET versions.
13. Public APIs and public implementation types introduced by the project must have complete XML documentation in en-US, including all applicable `<summary>`, `<param>`, `<returns>`, `<typeparam>`, `<exception>`, and other documentation elements. Do not leave placeholder or empty XML elements.

## Localization feature direction
The first vertical slice should accept a neutral JSON resource represented as `Dictionary<string,string>`, a target culture, translate values while preserving keys, and return the translated dictionary. A `HashSet` is not a replacement for a dictionary because key-to-value association is fundamental to the use case. Use `Dictionary<string,string>` unless profiling demonstrates a different representation is required.

Prefer an abstraction such as `ITranslatorService` for resource translation/read/write responsibilities. The concrete Google Translate integration should live in Infrastructure and be replaceable. Avoid scraping the public Google Translate web page with HTML parsing for the production implementation; use an official supported translation API/client and isolate provider-specific behavior.

## Testing rules
1. Maintain at least 80% coverage for lines and branches. Track method coverage when the selected coverage tool reports it.
2. Test every meaningful business-rule case implemented by the feature, including success, validation failure, boundary, failure and cancellation behavior where applicable.
3. Unit-test validators, commands/queries and handlers, feature services, resource adapters and deterministic provider boundaries. Handlers should verify both returned results and propagation of command data/cancellation tokens.
4. Tests must be deterministic and must not require live Google credentials, external services or a developer's local database unless they are explicitly integration tests.
5. The .NET 10 test workflow uses Microsoft.Testing.Platform (MTP) with `dotnet test`. MTP does not support the VSTest `coverlet.msbuild`/collector integration; use the native `coverlet.MTP` extension for MTP-based coverage and the MTP TRX report extension. Do not reintroduce VSTest-only coverage packages into an MTP test project.
6. Keep the existing GitHub Actions test-summary output structure stable. Changes to the test runner or coverage file naming may require only the minimum path/argument changes needed to feed the same summary format.
7. If local build/test commands are unavailable in the agent environment, inspect the workflow for the current implementation branch and use its GitHub Actions step summary and uploaded artifacts to validate test execution and coverage.
8. When coverage falls below 80%, add or improve tests rather than weakening the coverage scope or gate. Exclude only generated/framework code that is legitimately outside the application's testable surface.

## Commit rules
- Implement the largest coherent set of related changes in a commit rather than creating one commit per file.
- When working inside an already-open feature pull request, prefer commits that contain the maximum practical number of related files so unnecessary repeated build/test executions are avoided.
- Never combine unrelated features merely to increase commit size; preserve reviewability and architectural boundaries.

## Quality gates
Before considering a feature complete, build the solution, run the relevant tests, inspect the test/coverage reports, and add tests until the 80% line/branch target is satisfied. Fix warnings/errors introduced by the feature before completion. Do not silently change unrelated files.
