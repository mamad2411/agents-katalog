---
name: "mcp-strict-param-rejection"
description: "Strict unknown-parameter rejection for MCP tools: Stage A (UnmappedMemberHandling.Disallow) + Stage B (did-you-mean CallToolFilter)."
domain: "mcp-binding"
confidence: "high"
source: "earned"
---

## Context

Use when adding strict unknown-parameter rejection so callers receive a structured `McpException` instead of silent data loss when they pass a hallucinated or misspelled parameter name.

Two complementary layers — deploy both for best UX + safety:
- **Stage A** — SDK-level `UnmappedMemberHandling.Disallow` (stopgap; no hints)
- **Stage B** — `AddUnknownParameterFilter` CallToolFilter (polished UX with "did you mean" hints)

---

## Stage A — SDK Strict Rejection (Stopgap)

### SDK Mechanism

`Microsoft.Extensions.AI.Abstractions 10.5.2` (shipped with MCP 1.3.0+) includes a strict check in `ReflectionAIFunction.InvokeCoreAsync`:

```
if (SerializerOptions.UnmappedMemberHandling == Disallow && !HasCustomParameterBinding)
    throw ArgumentException(paramName: "arguments",
        message: "The arguments dictionary contains an unexpected key 'X' that does not correspond to any parameter of 'Y'.");
```

### How to Enable

Pass a `JsonSerializerOptions` with `UnmappedMemberHandling = Disallow` **and** `TypeInfoResolver = new DefaultJsonTypeInfoResolver()` to `WithToolsFromAssembly`:

```csharp
using System.Text.Json.Serialization.Metadata;

.WithToolsFromAssembly(typeof(MaestroMcpTools).Assembly, new JsonSerializerOptions
{
    UnmappedMemberHandling = JsonUnmappedMemberHandling.Disallow,
    TypeInfoResolver = new DefaultJsonTypeInfoResolver(),  // ← required companion
})
```

Apply to **both** HTTP and stdio transport registrations if both are used.

### Why `TypeInfoResolver` is required

The SDK calls `MakeReadOnly()` on the passed `JsonSerializerOptions` before schema generation. Setting any property on already-read-only options throws `InvalidOperationException`.

**Fix:** Always set `TypeInfoResolver = new DefaultJsonTypeInfoResolver()` upfront, before `MakeReadOnly()` is called.

---

## Stage B — `AddUnknownParameterFilter` (Polished UX)

### What It Does

Runs as a `CallToolFilter` **before** SDK dispatch. Computes `unknowns = argKeys − canonicalParams`.
On non-empty unknowns, throws a structured `McpException` with "did you mean" hints:

```
Unknown parameter 'chanelId' for tool 'maestro_channel'.
Did you mean: channelId?
Allowed parameters: channelId, noCache.
```

### Registration Order (Critical)

```csharp
options.AddBindingErrorFilter();           // 1. exception wrap
options.AddUnknownParameterFilter(asm);    // 2. did-you-mean check (Stage B)
// SDK dispatch with Disallow runs next     // 3. safety net (Stage A)
```

### Levenshtein Hint Threshold

Threshold: **6**. Catches both typos and hallucinated compound names (e.g. `subscriptionFilter` → `sourceRepoFilter`).

### Stage A Coexistence

Keep `UnmappedMemberHandling.Disallow` alongside Stage B. Defense-in-depth: Stage B fires first with better UX; Stage A catches schema-extraction failures.

---

## Files in This Codebase

- `src/MaestroTool.Core/MaestroMcpTools/McpServerOptionsExtensions.cs` — `AddBindingErrorFilter`, `AddUnknownParameterFilter`, Levenshtein helper
- `src/MaestroTool.Mcp/Program.cs` — `WithToolsFromAssembly` with serializer options (HTTP) + both filter registrations
- `src/MaestroTool/Program.cs` — same for stdio transport
- `src/MaestroTool.Tests/McpServerOptionsExtensionsTests.cs` — binding-error and unknown-param tests
