---
name: azure-functions-isolated
description: >
  Azure Functions .NET isolated worker model for owned apps: process separation from
  the host, Program.cs DI, middleware, gRPC worker channel, cold start/performance
  notes, migration from in-process, and secure configuration with managed identity.
  Use when building or migrating isolated-process Function apps — not for generic
  Container Apps or unauthorized tenant deployments.
---

# Azure Functions Isolated Worker (.NET)

## Scope And Authorization

- **In scope:** Function apps and codebases you own or are authorized to change.
- **Out of scope:** Deploying to foreign subscriptions; embedding secrets in app settings without Key Vault.
- Isolated worker changes host/runtime packaging — test triggers and bindings in nonprod.
- Pair with `azure-keyvault-appconfig-split` for config; `code-quality-standards` + `csharp-style-conventions`.

## When To Use

- New .NET Function apps (Microsoft recommends isolated for modern .NET).
- Migrating from in-process (`Microsoft.NET.Sdk.Functions`) to isolated (`Microsoft.Azure.Functions.Worker`).
- Needing full middleware pipeline, custom DI, or .NET versions not supported in-process.
- Debugging worker host connectivity, binding differences, or cold starts.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Container Apps hosting | `azure-container-apps` |
| Key Vault vs App Config split | `azure-keyvault-appconfig-split` |
| AKS identity | `azure-aks-workload-identity` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Topic | Isolated worker notes |
| --- | --- |
| Process model | Worker process separate from Functions host |
| Entry point | `Program.cs` with `HostBuilder` / `ConfigureFunctionsWorkerDefaults` |
| Bindings | Worker extensions packages; attributes differ slightly from in-process |
| Middleware | `IFunctionsWorkerMiddleware` pipeline |
| Language | First-class for modern .NET; other languages have their own worker models |
| Tooling | Azure Functions Core Tools, `func`, Visual Studio, Application Insights |

## Workflow

### 1. Confirm scope and success criteria

1. Runtime version, triggers (HTTP, Service Bus, Event Hubs, Timer), auth (function key vs AAD), authorization.
2. Success: local + Azure invoke works; DI resolves; insights traces show requests; secrets from KV/MI.
3. Rollback plan if migration: keep in-process slot until isolated proven.

### 2. Inventory current Function app

```bash
az functionapp list -g "$RG" -o table
az functionapp config show -g "$RG" -n "$APP" --query "{net:netFrameworkVersion,linux:linuxFxVersion,java:javaVersion}"
az functionapp config appsettings list -g "$RG" -n "$APP" -o table  # redact values
# In repo:
# csproj Sdk, PackageReference for Worker vs in-process
```

1. Identify in-process markers: `FunctionsStartup`, `Microsoft.NET.Sdk.Functions`.
2. List bindings used — check isolated extension support.
3. Note channel/host version settings (`FUNCTIONS_WORKER_RUNTIME=dotnet-isolated`).

### 3. Baseline

1. Capture cold start and steady latency.
2. Inventory app settings secrets to move to Key Vault references.
3. Integration test suite for each trigger.

### 4. Implement or migrate isolated worker

**Project sketch:**

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <AzureFunctionsVersion>v4</AzureFunctionsVersion>
    <OutputType>Exe</OutputType>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.Azure.Functions.Worker" Version="*" />
    <PackageReference Include="Microsoft.Azure.Functions.Worker.Sdk" Version="*" />
    <PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.Http.AspNetCore" Version="*" />
    <!-- Add ServiceBus/EventHubs/etc. worker extensions as needed -->
  </ItemGroup>
</Project>
```

```csharp
// Program.cs
var builder = FunctionsApplication.CreateBuilder(args);
builder.ConfigureFunctionsWebApplication();
builder.Services.AddApplicationInsightsTelemetryWorkerService();
builder.Services.AddSingleton<IMyService, MyService>();
builder.Build().Run();
```

```csharp
public class HttpExample
{
    private readonly IMyService _svc;
    public HttpExample(IMyService svc) => _svc = svc;

    [Function("HttpExample")]
    public IActionResult Run(
        [HttpTrigger(AuthorizationLevel.Function, "get", "post")] HttpRequestData req)
        => // prefer ASP.NET Core integration types when package enabled
           new OkObjectResult(_svc.GetData());
}
```

**Ops settings:**

```bash
az functionapp config appsettings set -g "$RG" -n "$APP" --settings \
  FUNCTIONS_WORKER_RUNTIME=dotnet-isolated \
  AzureWebJobsStorage="@Microsoft.KeyVault(SecretUri=...)" 
# Enable system MI and KV access
az functionapp identity assign -g "$RG" -n "$APP"
```

1. Replace in-process startup with DI in `Program.cs`.
2. Port bindings to worker extension packages; retest poison message/retry behavior.
3. HTTP: consider ASP.NET Core integration model for middleware parity.
4. Avoid storing secrets in `local.settings.json` committed to git; use User Secrets / KV.
5. Durable Functions and some advanced features — verify isolated support matrix before migrate.

### 5. Verify with evidence

```bash
func start
curl -sS "http://localhost:7071/api/HttpExample" -H "x-functions-key: $KEY"
az functionapp function list -g "$RG" -n "$APP" -o table
# Slot swap after smoke tests
```

1. All triggers fire in Azure with Application Insights dependency traces.
2. Failure: invalid function key → 401; missing MI role → handled without leaking secrets.
3. Compare cold start budget to baseline; adjust premium plan / pre-warm if needed.

### 6. Observe and harden

1. Alerts on failed executions, host recycle loops, queue depth for trigger sources.
2. Use Premium/Flex plans when cold start or VNET is required.
3. Defender for Cloud recommendations on Function apps; restrict CORS; prefer AAD auth for HTTP APIs.

### 7. Hand off

1. Migration notes: package list, binding changes, settings.
2. Local dev README: Core Tools version, `local.settings.json` template without secrets.
3. CI: build worker project, run tests, publish zip/run-from-package.

## In-process vs Isolated

| Concern | In-process | Isolated |
| --- | --- | --- |
| Host coupling | Same process | Separate worker |
| DI / middleware | Limited legacy patterns | Full .NET generic host |
| .NET version flexibility | Constrained | Broader modern TFMs |
| Migration cost | — | Binding/package rewrites |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Runtime setting | `dotnet-isolated` explicit | Wrong runtime → silent fail |
| Secrets | KV refs + MI | Connection strings in source |
| HTTP auth | AAD where possible | Anonymous admin endpoints |
| Packages | Worker extensions aligned | Mixing in-process attributes |
| Tests | Trigger integration tests | Only compile checks |

## Output Checklist

- [ ] Worker model confirmed (`dotnet-isolated`)
- [ ] Packages and Program.cs DI structured
- [ ] All triggers retested locally and in Azure
- [ ] App settings secrets via Key Vault/MI
- [ ] Insights/logging verified without secret leakage
- [ ] Cold start/plan expectations documented
- [ ] CI publish path works
- [ ] `code-quality-standards` / C# style applied

## Rules

- Prefer isolated for new .NET Function apps.
- Never commit secrets or production function keys.
- Validate binding feature parity before production migration.
- Authorized deployments only.
- Fail closed on auth for HTTP triggers handling sensitive data.
