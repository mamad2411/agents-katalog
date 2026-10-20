# C# Background Services

## Summary

**One-sentence:** Long-running in-process workers in ASP.NET Core via BackgroundService + Channels with bounded back-pressure, scoped DI, graceful shutdown, and health checks.

**One-paragraph:** Ad-hoc Task.Run loops bypass IHost lifecycle, ignore CancellationToken, and capture scoped DI as singletons. BackgroundService extends IHostedService and integrates with graceful shutdown, IHealthCheck, and System.Threading.Channels for in-memory queues with back-pressure. This methodology pins five testable rules: extend BackgroundService (never Task.Run), pass stoppingToken everywhere, catch per-item inside ExecuteAsync, CreateScope() for DbContext access, and Channel.CreateBounded with FullMode.Wait. Output: a worker class + DI registration + xUnit test conforming to the contract in `02-output-contract.xml`.

**Ефективно для:**

- Queue consumers, periodic cleanup, cache warming inside the API host.
- In-memory back-pressure between HTTP and background workers.
- Graceful shutdown coordination via CancellationToken propagation.
- IHealthCheck wiring for Kubernetes liveness/readiness probes.
- Moderate-throughput scheduled tasks where Hangfire/Quartz is overkill.

## Applies If (ALL must hold)

- The work must run inside the API host process (no separate Worker host).
- Jobs may be lost on shutdown — at-least-once with restart-tolerance is the goal.
- Throughput fits on a single replica or leader-elected replica.
- Graceful shutdown must drain in-flight work before stopping.

## Skip If (ANY kills it)

- Jobs MUST survive restarts — use Hangfire, Quartz.NET, or a durable broker.
- Heavy CPU work — would starve the HTTP thread pool; isolate to a Worker host.
- Distributed scheduling across replicas without leader election.
- Exactly-once semantics — in-memory channels lose state on shutdown.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Job spec | Markdown | team / ticket |
| ASP.NET Core 6+ project | csproj | repo |
| DbContext or downstream service contract | C# interface | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-dotnet]] | Base .NET wiring, DI, hosting model. |
| [[csharp-entity-framework]] | Scoped DbContext lifecycle the worker depends on. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: extend-backgroundservice, pass-stoppingtoken, per-item-trycatch, scope-per-item, bounded-channel | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for worker spec + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: task-run-loop, unbounded-channel, captive-dbcontext, no-stoppingtoken | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: classify → design channel → write worker → register + health → test | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on durability/throughput → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-job-shape` | sonnet | Apply decision tree on durability/throughput/cpu. |
| `write-worker-class` | sonnet | C# scaffolding with the 5 rules. |
| `write-xunit-test` | haiku | Mechanical AAA test against IHostedService API. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Worker.cs` | BackgroundService + Channel reader skeleton |
| `templates/ProgramRegistration.cs` | Channel + worker + health check DI registration |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-background-services.py` | Validate worker spec JSON against the schema | Pre-commit on the spec artefact |

## Related

- [[csharp-dotnet]]
- [[csharp-entity-framework]]
- [[csharp-xunit-testing]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (job durability requirement, throughput, CPU profile, distribution) to a rule from `01-core-rules.xml` and either approves BackgroundService or redirects to a durable broker / Worker host. Use it whenever an engineer reaches for `Task.Run` or considers a hosted-service for periodic work.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/Worker.cs`

```csharp
using System.Threading.Channels;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace Faion.Workers;

public sealed class OrderProcessorService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<OrderProcessorService> _logger;
    private readonly Channel<int> _channel;

    public OrderProcessorService(
        IServiceProvider serviceProvider,
        ILogger<OrderProcessorService> logger,
        Channel<int> channel)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
        _channel = channel;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await foreach (var orderId in _channel.Reader.ReadAllAsync(stoppingToken))
        {
            try
            {
                await ProcessAsync(orderId, stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed processing order {OrderId}", orderId);
            }
        }
    }

    private async Task ProcessAsync(int orderId, CancellationToken ct)
    {
        using var scope = _serviceProvider.CreateScope();
        var service = scope.ServiceProvider.GetRequiredService<IOrderService>();
        await service.ProcessAsync(orderId, ct);
    }
}

public interface IOrderService
{
    Task ProcessAsync(int orderId, CancellationToken ct);
}
```

### `templates/ProgramRegistration.cs`

```csharp
using System.Threading.Channels;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using Faion.Workers;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSingleton(Channel.CreateBounded<int>(
    new BoundedChannelOptions(1000) { FullMode = BoundedChannelFullMode.Wait }));

builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddSingleton<OrderProcessorHealth>();
builder.Services.AddHostedService<OrderProcessorService>();
builder.Services.AddHealthChecks()
    .AddCheck<OrderProcessorHealth>("order-processor");

var app = builder.Build();
app.MapHealthChecks("/healthz");
app.Run();

public sealed class OrderProcessorHealth : IHealthCheck
{
    public DateTime LastSuccess { get; set; } = DateTime.UtcNow;

    public Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext _, CancellationToken __)
        => Task.FromResult(
            DateTime.UtcNow - LastSuccess > TimeSpan.FromMinutes(5)
                ? HealthCheckResult.Unhealthy("no successful run in >5m")
                : HealthCheckResult.Healthy());
}
```
