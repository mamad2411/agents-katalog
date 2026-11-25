---
name: app-service-worker-observability
description: Establish and review the Azure App Service observability baseline for .NET worker, WebJob, background-service, or ASP.NET Core deployments. Use whenever an App Service worker is being deployed, startup failures are hard to diagnose, logs disappear before Application Insights initializes, or infrastructure logging and temporary incident diagnostics need to be source-controlled.
---

# App Service worker observability

Make worker failures observable through two independent paths: durable centralized telemetry for
normal operation and short-lived App Service filesystem diagnostics for failures that occur before
the telemetry pipeline is ready. Keep the diagnostic configuration in infrastructure code so the
deployed state is reviewable and reversible.

## Required baseline

Implement all six parts. Treat a missing part as an observability gap, not as an optional
enhancement.

1. Wire Application Insights into the host before registering or starting hosted services.
2. Configure an App Service diagnostic setting that sends resource logs to the chosen durable
   sink, normally Log Analytics.
3. In non-production, enable bounded filesystem application logging so startup and worker failures
   remain available when centralized telemetry cannot initialize.
4. Enable detailed error capture for Windows App Service troubleshooting.
5. Enable failed-request tracing for Windows App Service troubleshooting.
6. Express temporary escalation controls in source control with an owner, reason, expiry, bounded
   retention, and an explicit off state.

Detailed errors and failed-request tracing are Windows App Service capabilities. For Linux or a
custom container, record that platform constraint and use console/application logs plus the durable
diagnostic sink; do not pretend that an unsupported switch is active.

## Application wiring

Choose one telemetry stack and initialize it at host construction. Prefer the Azure Monitor
OpenTelemetry distribution for new services. An existing service may keep the Application
Insights Worker Service SDK if migration would add unrelated risk.

For the Worker Service SDK:

```csharp
var builder = Host.CreateApplicationBuilder(args);

builder.Services.AddApplicationInsightsTelemetryWorkerService();
builder.Logging.AddAzureWebAppDiagnostics();

builder.Services.AddHostedService<Worker>();
await builder.Build().RunAsync();
```

Reference `Microsoft.ApplicationInsights.WorkerService` and
`Microsoft.Extensions.Logging.AzureAppServices`. Supply
`APPLICATIONINSIGHTS_CONNECTION_STRING` through App Service configuration or a secret-aware
deployment system; never commit the connection string. Preserve the console provider so Linux and
container deployments emit to the App Service log stream.

Emit a startup event after the host is built and a structured error at the worker boundary. Include
stable operation names and correlation identifiers, but exclude secrets and sensitive payloads.

## Infrastructure baseline

Represent the durable diagnostic sink and the temporary filesystem controls separately. This Bicep
shape is illustrative; adapt resource names and API versions to the repository's existing IaC:

```bicep
@allowed(['off', 'errors', 'verbose'])
param temporaryDiagnostics string = 'off'
param environmentName string

var isProduction = environmentName == 'production'
var filesystemLevel = isProduction || temporaryDiagnostics == 'off'
  ? 'Off'
  : temporaryDiagnostics == 'verbose' ? 'Verbose' : 'Error'
var windowsTroubleshooting = !isProduction && temporaryDiagnostics != 'off'

resource appLogs 'Microsoft.Web/sites/config@2024-04-01' = {
  parent: app
  name: 'logs'
  properties: {
    applicationLogs: {
      fileSystem: {
        level: filesystemLevel
      }
    }
    detailedErrorMessages: {
      enabled: windowsTroubleshooting
    }
    failedRequestsTracing: {
      enabled: windowsTroubleshooting
    }
    httpLogs: {
      fileSystem: {
        enabled: windowsTroubleshooting
        retentionInDays: 3
        retentionInMb: 35
      }
    }
  }
}

resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'app-service-observability'
  scope: app
  properties: {
    workspaceId: logAnalytics.id
    logs: [
      { category: 'AppServiceAppLogs', enabled: true }
      { category: 'AppServiceConsoleLogs', enabled: true }
      { category: 'AppServiceHTTPLogs', enabled: true }
    ]
    metrics: [
      { category: 'AllMetrics', enabled: true }
    ]
  }
}
```

Confirm the available diagnostic categories for the selected App Service platform and region during
deployment. Do not silently drop an unsupported category.

## Temporary escalation contract

Keep escalation exceptional and reviewable:

- Default the mode to `off`; production filesystem logging stays off unless a separately approved
  incident procedure explicitly permits it.
- Store the mode in environment parameter files or another reviewed IaC input, not as an
  unrecorded portal toggle.
- Require an incident or issue identifier, named owner, UTC expiry, and rollback change in the same
  review. Add a CI check that rejects an expired non-`off` mode.
- Bound filesystem quota and retention. Filesystem logs are a diagnostic buffer, not the durable
  observability store.
- Return the mode to `off` after evidence is collected and verify the deployed configuration.

## Verification

Prove the baseline rather than checking only that deployment succeeded:

1. Start a non-production instance with a controlled startup failure before the worker loop begins.
2. Confirm the error appears in App Service filesystem or console logs with the expected instance
   and correlation data.
3. Start normally, execute one worker operation, and confirm its trace/log reaches Application
   Insights.
4. Confirm App Service resource logs reach the durable diagnostics sink.
5. On Windows, exercise one controlled failed HTTP request and locate its detailed error and
   failed-request trace.
6. Re-deploy with temporary diagnostics `off` and verify filesystem, detailed-error, and
   failed-request switches are disabled while centralized telemetry remains enabled.

## Review checklist

- Telemetry registration precedes hosted-service registration and startup.
- Connection strings and credentials come from deployment configuration, not source.
- Durable diagnostic settings cover application, console, and HTTP logs where supported.
- Non-production startup failures have an independent filesystem or console path.
- Windows detailed errors and failed-request tracing are explicit and bounded.
- Temporary escalation is source-controlled, time-bounded, owned, and reversible.
- Verification covers failure before telemetry initialization and the return to normal settings.

## Primary references

- [Enable diagnostic logging for Azure App Service](https://learn.microsoft.com/azure/app-service/troubleshoot-diagnostic-logs)
- [Configure Azure Monitor OpenTelemetry](https://learn.microsoft.com/azure/azure-monitor/app/opentelemetry-configuration)
- [Application Insights connection strings](https://learn.microsoft.com/azure/azure-monitor/app/connection-strings)
- [Azure CLI App Service log controls](https://learn.microsoft.com/cli/azure/webapp/log)
