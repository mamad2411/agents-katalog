# xUnit Testing for .NET

## Summary

**One-sentence:** xUnit + Moq + WebApplicationFactory test conventions for .NET 8 — AAA layout, IClassFixture, async Task return, FluentAssertions diffs, deterministic isolation.

**One-paragraph:** xUnit misuse — async void test methods, `WebApplicationFactory<Program>` without `public partial class Program`, shared mutable state across parallel tests, lazy `It.IsAny<T>()` mock setups, missing FluentAssertions — produces flaky CI and unreadable failure output. This methodology pins five rules: every async test returns `Task`; controller tests use `IClassFixture<WebApplicationFactory<Program>>`; `[Theory]` + `[InlineData]` for parametric tests; mocks use precise `It.Is<T>(...)` matchers; assertions use `FluentAssertions`. Output: test class conforming to `02-output-contract.xml`.

**Ефективно для:**

- xUnit + Moq + FluentAssertions stacks on .NET 6+.
- Controller integration tests via `WebApplicationFactory<Program>`.
- Service unit tests with constructor-injected collaborators.
- Repository slice tests with SQLite-in-memory or Testcontainers.
- Coverage thresholds enforced in CI via Coverlet.

## Applies If (ALL must hold)

- xUnit is the chosen test framework (not MSTest / NUnit).
- The project targets .NET 6+ (top-level `Program.cs`).
- Tests run in CI with parallelization enabled by default.
- Reviewers expect AAA layout + FluentAssertions diffs.

## Skip If (ANY kills it)

- MSTest / NUnit is mandated by the org — apply the relevant methodology.
- BDD-style tests via SpecFlow drive the test plan — different conventions.
- Manual QA only; automated tests are not the source of truth.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Unit-under-test | C# class | repo |
| Test plan | Markdown | spec |
| `Program.cs` (for integration tests) | top-level | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-dotnet]] | Controller + service patterns the tests exercise. |
| [[csharp-entity-framework]] | EF patterns repository tests target. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: async-task-return, class-fixture-required, theory-for-params, precise-mock-matchers, fluent-assertions-required | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for test class spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: async-void-test, parallel-state-collision, web-factory-program-not-public, im-memory-vs-relational | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: classify → fixture → test → mock → assert | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on test scope → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-test-scope` | sonnet | Unit / slice / integration judgment. |
| `write-test-class` | haiku | Mechanical AAA scaffolding. |
| `audit-flaky-test` | sonnet | Look for shared state + non-deterministic setup. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ControllerTests.cs` | WebApplicationFactory integration test |
| `templates/ServiceTests.cs` | Service unit test with Moq |
| `templates/ProgramPartial.cs` | `public partial class Program {}` shim |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-xunit-testing.py` | Validate test-class spec against schema | Pre-commit on spec artefact |

## Related

- [[csharp-dotnet]]
- [[csharp-entity-framework]]
- [[csharp-background-services]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps test scope (unit / slice / integration) to a rule from `01-core-rules.xml`. Use it whenever choosing between mocking a collaborator vs spinning up `WebApplicationFactory` vs using Testcontainers for a real database.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ControllerTests.cs`

```csharp
using System.Net;
using System.Net.Http.Json;
using FluentAssertions;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace Faion.Tests;

public sealed class OrdersControllerTests : IClassFixture<TestAppFactory>
{
    private readonly HttpClient _client;

    public OrdersControllerTests(TestAppFactory factory) => _client = factory.CreateClient();

    [Fact]
    public async Task Get_ExistingId_Returns200()
    {
        var response = await _client.GetAsync("/api/orders/1");
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        var dto = await response.Content.ReadFromJsonAsync<OrderResponse>();
        dto.Should().BeEquivalentTo(new OrderResponse(1, "Alice", 10m));
    }

    [Theory]
    [InlineData(0, HttpStatusCode.NotFound)]
    [InlineData(99, HttpStatusCode.NotFound)]
    public async Task Get_MissingId_Returns404(int id, HttpStatusCode expected)
    {
        var response = await _client.GetAsync($"/api/orders/{id}");
        response.StatusCode.Should().Be(expected);
    }
}

public sealed class TestAppFactory : WebApplicationFactory<Program>
{
    private readonly SqliteConnection _conn = new("DataSource=:memory:");

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        _conn.Open();
        builder.ConfigureServices(services =>
        {
            services.RemoveAll<DbContextOptions<AppDbContext>>();
            services.AddDbContext<AppDbContext>(opt => opt.UseSqlite(_conn));
        });
    }
}

public sealed record OrderResponse(int Id, string CustomerName, decimal Total);
```

### `templates/ServiceTests.cs`

```csharp
using FluentAssertions;
using Moq;

namespace Faion.Tests;

public sealed class OrdersServiceTests
{
    private readonly Mock<IOrderRepository> _repo = new();
    private readonly OrdersService _svc;

    public OrdersServiceTests()
    {
        _svc = new OrdersService(_repo.Object);
    }

    [Fact]
    public async Task GetAsync_ExistingOrder_ReturnsDto()
    {
        _repo.Setup(r => r.GetAsync(It.Is<int>(id => id == 1), It.IsAny<CancellationToken>()))
             .ReturnsAsync(new Order(1, "Alice", 10m));

        var result = await _svc.GetAsync(1, CancellationToken.None);

        result.Should().BeEquivalentTo(new OrderResponse(1, "Alice", 10m));
        _repo.Verify(r => r.GetAsync(1, It.IsAny<CancellationToken>()), Times.Once);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-5)]
    public async Task GetAsync_NonPositiveId_Throws(int id)
    {
        var act = () => _svc.GetAsync(id, CancellationToken.None);
        await act.Should().ThrowAsync<ArgumentOutOfRangeException>();
    }
}

public interface IOrderRepository { Task<Order?> GetAsync(int id, CancellationToken ct); }
public sealed record Order(int Id, string CustomerName, decimal Total);
public sealed record OrderResponse(int Id, string CustomerName, decimal Total);
public sealed class OrdersService
{
    private readonly IOrderRepository _r;
    public OrdersService(IOrderRepository r) => _r = r;
    public async Task<OrderResponse?> GetAsync(int id, CancellationToken ct)
    {
        if (id <= 0) throw new ArgumentOutOfRangeException(nameof(id));
        var o = await _r.GetAsync(id, ct);
        return o is null ? null : new OrderResponse(o.Id, o.CustomerName, o.Total);
    }
}
```

### `templates/ProgramPartial.cs`

```csharp
// Append to the bottom of the API project's Program.cs:

public partial class Program { }
```
