---
name: ai-observability-dotnet
description: 'Implement observability for .NET AI systems using OpenTelemetry. Use when adding traces, logs, metrics for model inference, tool calls, workflow execution, and safety events. Covers telemetry schema, ASP.NET Core setup, safe logging with redaction, alerting thresholds, and correlation IDs across async boundaries.'
---

# AI Observability for .NET

Production-grade observability for .NET AI applications using OpenTelemetry and structured logging.

## When To Use This Skill

- Missing visibility into model latency, failures, token usage, or cost.
- Need end-to-end correlation IDs across AI pipelines and workflow nodes.
- Need dashboards and alerts for AI reliability, performance degradation, or anomalies.
- Debugging AI system behavior in production (latency spikes, error rates, model switching).

## Recommended Telemetry Schema

### Trace Operations
```
- ai.model.invoke         [model, provider, model_version, latency_ms, cost_usd, input_tokens, output_tokens, temperature]
- ai.tool.invoke          [tool_name, tool_version, latency_ms, success, error_reason]
- ai.workflow.start       [workflow_id, workflow_name, correlation_id, user_id]
- ai.workflow.step        [step_name, step_index, provider, latency_ms]
- ai.workflow.end         [workflow_id, total_latency_ms, step_count, success, error_reason]
- ai.safety.filter        [filter_type (prompt_injection, content_policy, etc.), action (allowed, blocked), confidence]
- ai.content.validation   [validation_rule, input_type, passed, rejection_reason]
```

### Key Tags (Low-Cardinality Dimensions)
```
service.name = "my-ai-app"
service.version = "1.0.0"
deployment.environment = "prod|staging|dev"
ai.provider = "azure_openai|openai|anthropic|ollama"
ai.model = "gpt-4-turbo|claude-3-opus|etc"  [limited set of known models]
http.status_code = "200|400|429|500"
error.type = "ModelError|ToolError|TimeoutError|etc"
```

### Metrics
```
ai.model.request.total           [counter, tags: provider, model, status]
ai.model.request.latency_ms      [histogram, tags: provider, model]
ai.model.tokens.input            [counter, tags: provider, model]
ai.model.tokens.output           [counter, tags: provider, model]
ai.model.cost_usd                [counter, tags: provider, model]
ai.tool.request.total            [counter, tags: tool_name, status]
ai.tool.request.latency_ms       [histogram, tags: tool_name]
ai.workflow.duration_ms          [histogram, tags: workflow_name, status]
ai.safety.events.total           [counter, tags: filter_type, action]
```

## Initial Workflow

### 1. ASP.NET Core Setup

```csharp
// Program.cs
var builder = WebApplicationBuilder.CreateBuilder(args);

// Add OpenTelemetry
builder.Services
    .AddOpenTelemetry()
    .WithTracing(tracing =>
    {
        tracing
            .AddAspNetCoreInstrumentation()
            .AddHttpClientInstrumentation()
            .AddOtlpExporter(opts =>
            {
                opts.Endpoint = new Uri(builder.Configuration["OTEL_EXPORTER_OTLP_ENDPOINT"]);
            });
    })
    .WithMetrics(metrics =>
    {
        metrics
            .AddAspNetCoreInstrumentation()
            .AddHttpClientInstrumentation()
            .AddMeter("MyApp.AI")
            .AddOtlpExporter();
    });

// Add custom AI instrumentation
builder.Services.AddSingleton<AiInstrumentationService>();
builder.Services.AddChatClient(...)
    .UseLogging()
    .UseInstrumentation();  // Custom middleware

var app = builder.Build();
app.Run();
```

### 2. Custom Instrumentation Middleware

```csharp
public class AiInstrumentationService
{
    private readonly ActivitySource _activitySource;
    private readonly IMeterFactory _meterFactory;

    public AiInstrumentationService()
    {
        _activitySource = new ActivitySource("MyApp.AI");
        var meter = new Meter("MyApp.AI");
        TokenCounter = meter.CreateCounter<long>("ai.model.tokens.input");
        CostCounter = meter.CreateCounter<long>("ai.model.cost_usd");
    }

    public Counter<long> TokenCounter { get; }
    public Counter<long> CostCounter { get; }

    public Activity StartModelCall(string model, string provider)
    {
        var activity = _activitySource.StartActivity("ai.model.invoke", ActivityKind.Internal);
        activity?.SetTag("ai.model", model);
        activity?.SetTag("ai.provider", provider);
        activity?.SetTag("otel.kind", "internal");
        return activity;
    }
}

// Extension for IChatClient middleware
public static class AiInstrumentationExtensions
{
    public static ChatClientBuilder UseInstrumentation(this ChatClientBuilder builder)
    {
        return builder.Use(async (request, next, context) =>
        {
            using var instrumentation = new AiInstrumentationService();
            using var activity = instrumentation.StartModelCall(
                context.Options?.GetProperty("model_name") as string ?? "unknown",
                context.Options?.GetProperty("provider") as string ?? "unknown");

            try
            {
                var response = await next(request, context);
                activity?.SetTag("http.status_code", 200);
                return response;
            }
            catch (Exception ex)
            {
                activity?.SetTag("http.status_code", 500);
                activity?.SetTag("error.type", ex.GetType().Name);
                throw;
            }
        });
    }
}
```

### 3. Worker Service Setup

```csharp
// Program.cs (Worker Service)
var builder = Host.CreateDefaultBuilder(args);

builder.ConfigureServices(services =>
{
    services
        .AddOpenTelemetry()
        .WithTracing(tracing =>
        {
            tracing
                .AddSource("MyApp.AI")
                .AddOtlpExporter(opts =>
                {
                    opts.Endpoint = new Uri(Environment.GetEnvironmentVariable("OTEL_EXPORTER_OTLP_ENDPOINT"));
                });
        })
        .WithMetrics(metrics =>
        {
            metrics
                .AddMeter("MyApp.AI")
                .AddOtlpExporter();
        });

    services.AddHostedService<AiWorkerService>();
});

var host = builder.Build();
host.Run();
```

### 4. Safe Logging for AI Content

```csharp
public static class SafeAiLogging
{
    private static readonly ILogger Logger = LoggerFactory.Create(b => b.AddConsole())
        .CreateLogger("AI.SafeLogging");

    /// <summary>
    /// Log AI interaction with safe redaction of sensitive payloads.
    /// </summary>
    public static void LogAiInteraction(
        string operationId,
        string model,
        int inputTokens,
        int outputTokens,
        TimeSpan latency,
        bool success,
        string? errorReason = null,
        string? prompt = null)
    {
        // Log metadata only, never raw prompt/response
        Logger.LogInformation(
            "AI Operation Complete | OperationId={OperationId} Model={Model} " +
            "InputTokens={InputTokens} OutputTokens={OutputTokens} LatencyMs={LatencyMs} " +
            "Success={Success} Error={Error}",
            operationId, model, inputTokens, outputTokens, latency.TotalMilliseconds,
            success, errorReason ?? "none");

        // If debugging is needed, use structured logging with separate redaction
        if (Logger.IsEnabled(LogLevel.Debug) && !string.IsNullOrEmpty(prompt))
        {
            var redactedPrompt = RedactSensitiveContent(prompt);
            Logger.LogDebug("Prompt (redacted): {RedactedPrompt}", redactedPrompt);
        }
    }

    private static string RedactSensitiveContent(string content)
    {
        // Redact email addresses, phone numbers, API keys, etc.
        var redacted = System.Text.RegularExpressions.Regex.Replace(
            content,
            @"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  // Email
            "[EMAIL_REDACTED]");
        redacted = System.Text.RegularExpressions.Regex.Replace(
            redacted,
            @"\b\d{3}-\d{3}-\d{4}\b",  // Phone
            "[PHONE_REDACTED]");
        return redacted.Length > 500 ? redacted.Substring(0, 500) + "..." : redacted;
    }
}

// Usage
SafeAiLogging.LogAiInteraction(
    operationId: Activity.Current?.Id ?? "unknown",
    model: "gpt-4-turbo",
    inputTokens: 150,
    outputTokens: 320,
    latency: stopwatch.Elapsed,
    success: true);
```

## Alerting & Runbook Starters

### Alert Thresholds

| Alert | Threshold | Runbook |
|-------|-----------|---------|
| **Model Latency High** | p95 > 5s for 5 min | Check provider API status; review model workload; consider rate limiting |
| **Error Rate Spike** | Error rate > 5% for 2 min | Check model availability; review recent code changes; verify API keys/quotas |
| **Token Cost Anomaly** | Daily cost > 150% baseline | Review prompt length; check for repeated calls; audit tool invocation logic |
| **Safety Filter Blocks** | Block rate > 2% for 5 min | Review prompt injection attack patterns; check if user input validation is weak |
| **Workflow Timeout** | Workflow latency > 30s (or SLA) | Review step latencies; check if tools are hanging; consider async optimization |

### Example Alert Query (Prometheus)

```promql
# Alert: Model error rate exceeds 5%
(rate(ai_model_request_total{status="error"}[5m]) / rate(ai_model_request_total[5m])) > 0.05

# Alert: Token cost spike
increase(ai_model_cost_usd[1h]) > avg_over_time(increase(ai_model_cost_usd[1h])[7d:1h]) * 1.5

# Alert: Workflow p95 latency
histogram_quantile(0.95, rate(ai_workflow_duration_ms_bucket[5m])) > 5000
```

## Gotchas

- **High-Cardinality Metrics**: Never use raw prompt content, model versions, or user IDs as metric labels—leads to cardinality explosion. Use predefined, low-cardinality tag values only.
- **Sensitive Data in Logs**: Never log raw prompts or model responses by default. Use `SafeAiLogging` for redaction; enable detailed logging only in staging/debug environments.
- **Cost Attribution Drift**: Track input + output tokens separately; calculate cost per model+provider to catch billing anomalies early.
- **Correlation ID Loss**: Ensure `Activity.Current?.Id` is propagated through all async boundaries; use `Activity.Default.Id` in background tasks.
- **Sampling Bias**: If sampling traces, ensure you capture errors and slow operations. Use tail-based sampling (e.g., OTel Collector) for production.

## References

- **OpenTelemetry .NET**: <https://opentelemetry.io/docs/languages/net/>
- **Microsoft.Extensions.Logging**: <https://learn.microsoft.com/dotnet/api/microsoft.extensions.logging>
- **OpenTelemetry Instrumentation**: <https://opentelemetry.io/docs/instrumentation/net/>
- **Semantic Conventions (Traces)**: <https://opentelemetry.io/docs/specs/semconv/>
- **Prometheus Alerting**: <https://prometheus.io/docs/alerting/latest/overview/>
