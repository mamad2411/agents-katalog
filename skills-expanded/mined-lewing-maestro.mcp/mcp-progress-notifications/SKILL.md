# Skill: Emitting MCP Progress Notifications (ModelContextProtocol C# SDK ≥ 1.3.0)

## When to apply
A `[McpServerTool]` method routinely takes more than ~1 second
(parallel API fan-out, flow graph computation, validation passes). The MCP client
needs interim progress so its UI doesn't appear hung.

## The pattern (server side, C#)

```csharp
[McpServerTool(Name = "maestro_subscription_health")]
public async Task<string> GetSubscriptionHealth(
    string targetRepository,
    bool validate = false,
    // Auto-injected by the SDK. Parameter is *omitted from the tool's
    // JSON schema* — clients never see it.
    IProgress<ProgressNotificationValue>? progress = null,
    CancellationToken cancellationToken = default)
{
    var results = await _service.GetSubscriptionHealthAsync(
        targetRepository, 
        noCache, 
        includeCommitDetails, 
        validate,
        McpProgressAdapter.Wrap(progress),  // ← adapter at boundary
        cancellationToken);
    
    return FormatResults(results);
}
```

### Key facts about the SDK behavior
- The SDK auto-injects `IProgress<ProgressNotificationValue>` for any
  parameter of that type. **You don't register or wire anything.**
- If the client included `_meta.progressToken` in `tools/call`, every
  `Report` becomes a `notifications/progress` JSON-RPC message tagged
  with that token.
- **If the client did NOT supply a progress token**, the injected sink
  is a no-op. `progress?.Report(...)` is always safe.

## Granularity rules (don't violate)
- **5–10 emits per long run.** Not per-item.
  `step = ProgressReporter.ItemStep(total)` → `max(1, total / 10)`.
- Add a wall-clock throttle (≥ 250 ms between emits) for very fast operations.
- Always emit one final 100% so the client can dismiss its progress UI.

## Always include a human-readable `Message`
The numeric pair drives progress bars *eventually*; the message is what
shows up in clients today. Make it parseable at a glance: 
`"Checked 5 of 50: dotnet/runtime → dotnet/dotnet"`,
`"Resolving 120 nodes and 300 edges..."`.

## Keeping the service layer transport-agnostic
Don't put `ModelContextProtocol` types in `MaestroTool.Core`. Define a small domain record:

```csharp
// MaestroTool.Core
public readonly record struct ProgressUpdate(
    double Current, double? Total, string? Message);
```

…and put a tiny adapter in the MCP tool layer:

```csharp
// MaestroTool.Core/MaestroMcpTools/McpProgressAdapter.cs
internal static class McpProgressAdapter
{
    public static IProgress<ProgressUpdate>? Wrap(
        IProgress<ProgressNotificationValue>? mcp)
        => mcp is null ? null : new Adapter(mcp);

    private sealed class Adapter(IProgress<ProgressNotificationValue> mcp)
        : IProgress<ProgressUpdate>
    {
        public void Report(ProgressUpdate v) => mcp.Report(new()
        {
            Progress = (float)v.Current,
            Total    = v.Total is null ? null : (float)v.Total.Value,
            Message  = v.Message,
        });
    }
}
```

Service methods take `IProgress<ProgressUpdate>?`, MCP tools translate at
the boundary. CLI callers (and unit tests) just pass `null`.

## Signature placement convention (this repo)
Put the new optional `IProgress<ProgressUpdate>?` parameter **before**
`CancellationToken cancellationToken = default`, so CT stays visually
last. At the MCP tool boundary, the MCP-specific IProgress parameter
goes before CT as well.

## Verification checklist
1. `dotnet build` clean.
2. `dotnet test` clean (existing tests should not regress — they pass
   `null` to the new optional param implicitly).
3. Tools that fetch in a single shot (no streaming, no per-item loop)
   should NOT be instrumented — the spec is for *long-running* ops.

## Tools instrumented in this repo
- `maestro_subscription_health` with `validate=true`: Reports per-subscription progress during parallel fan-out ("Checked N of M: source → target")
- `maestro_flow_graph`: Reports at start ("Computing flow graph...") and completion ("Resolving X nodes/edges...")

## References
- `src/MaestroTool.Core/ProgressUpdate.cs`
- `src/MaestroTool.Core/ProgressReporter.cs`
- `src/MaestroTool.Core/MaestroMcpTools/McpProgressAdapter.cs`
- `src/MaestroTool.Core/Maestro/MaestroService.cs` (GetSubscriptionHealthAsync with IProgress parameter)
