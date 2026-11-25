---
name: logging
description: >
  Observability overview and glue for .NET 10: how the pieces fit together,
  plus the cross-cutting parts owned here — ASP.NET health check endpoints
  (/health), correlation IDs, and log-level strategy. For deep Serilog setup
  load `serilog`; for traces and metrics load `opentelemetry`. Load this
  skill when setting up observability from scratch, wiring health check
  endpoints or correlation IDs, or when the user says "logging",
  "observability", "monitoring setup", "liveness", "readiness", or "ILogger".
---

# Logging & Observability

## Core Principles

1. **Structured logging with Serilog** — Every log entry is a structured event with named properties, not a formatted string. This enables searching, filtering, and alerting. All setup (two-stage bootstrap, `AddSerilog()`, sinks, enrichers) lives in the **serilog** skill — that skill's `AddSerilog()`-over-`UseSerilog()` guidance is canonical.
2. **OpenTelemetry for distributed tracing** — Traces connect requests across services; metrics track system health over time. Full setup lives in the **opentelemetry** skill.
3. **Health checks for operational readiness** — Every service exposes `/health` endpoints for load balancers and orchestrators. Liveness and readiness are separate questions and separate endpoints.
4. **Correlation IDs for request tracing** — Every request gets a unique ID that flows through all log entries and downstream service calls, so one user complaint maps to one filtered log stream.

## Patterns

### How the Pieces Fit Together

| Concern | Owner | Skill |
|---------|-------|-------|
| Structured application logs | Serilog (`AddSerilog()`) | `serilog` |
| Request summary logging | `UseSerilogRequestLogging()` | `serilog` |
| Traces + metrics + OTLP export | OpenTelemetry SDK | `opentelemetry` |
| Health endpoints, correlation IDs, log-level strategy | This skill | `logging` |

Wire logging first (you need logs to debug the rest), then health checks, then tracing.

### Correlation IDs

```csharp
// Middleware to set correlation ID
public class CorrelationIdMiddleware(RequestDelegate next)
{
    private const string CorrelationIdHeader = "X-Correlation-Id";

    public async Task InvokeAsync(HttpContext context)
    {
        var correlationId = context.Request.Headers[CorrelationIdHeader].FirstOrDefault()
            ?? Guid.NewGuid().ToString();

        context.Items["CorrelationId"] = correlationId;
        context.Response.Headers[CorrelationIdHeader] = correlationId;

        using (LogContext.PushProperty("CorrelationId", correlationId))
        {
            await next(context);
        }
    }
}

// Program.cs — register early so every downstream log carries the ID
app.UseMiddleware<CorrelationIdMiddleware>();
```

Why middleware: pushing the property once at the pipeline edge attaches it to every log event in the request scope — no per-call-site plumbing. Propagate the same header on outgoing `HttpClient` calls via a `DelegatingHandler` (see the **httpclient-factory** skill).

### Health Checks

```csharp
// Program.cs
builder.Services.AddHealthChecks()
    .AddNpgSql(builder.Configuration.GetConnectionString("Default")!,
        name: "database", tags: ["ready"])
    .AddRedis(builder.Configuration.GetConnectionString("Redis")!,
        name: "redis", tags: ["ready"])
    .AddRabbitMQ(builder.Configuration.GetConnectionString("RabbitMq")!,
        name: "rabbitmq", tags: ["ready"]);

// Map endpoints
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false // No dependency checks — just "am I running?"
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

Why two endpoints: liveness failing means "restart me"; readiness failing means "stop sending traffic". Conflating them makes a slow database restart your app in a loop.

### Log-Level Strategy

| Level | Use for | Environment default |
|-------|---------|---------------------|
| Debug | Diagnostic detail, payload dumps (never PII in prod) | Development only |
| Information | Business events: order placed, job completed | Dev + staging |
| Warning | Recoverable anomalies: retry fired, fallback used | Everywhere — production default |
| Error | Failed operations that need attention | Everywhere |
| Fatal/Critical | App cannot continue | Everywhere |

Why Warning as the production default: Information-level request noise at scale costs real money in log storage and drowns the signals. Keep Information for genuine business events via namespace overrides (see the **serilog** skill's `MinimumLevel.Override` pattern).

## Anti-patterns

### Don't Log Sensitive Data

```csharp
// BAD — logging credentials
logger.LogInformation("User logged in: {Email} with password {Password}", email, password);

// GOOD — log identifiers, never secrets or PII at Information level
logger.LogInformation("User {UserId} logged in", userId);
```

### Don't Skip Health Check Tags

```csharp
// BAD — all checks run for liveness AND readiness
app.MapHealthChecks("/health");

// GOOD — separate liveness (am I running?) from readiness (can I serve traffic?)
app.MapHealthChecks("/health/live", new() { Predicate = _ => false });
app.MapHealthChecks("/health/ready", new() { Predicate = c => c.Tags.Contains("ready") });
```

### Don't Re-Implement What the Owning Skill Provides

```csharp
// BAD — hand-rolling Serilog bootstrap here from memory
builder.Host.UseSerilog(...);  // legacy API — the serilog skill forbids this

// GOOD — load the serilog skill and use its two-stage AddSerilog() bootstrap
builder.Services.AddSerilog((services, lc) => lc.ReadFrom.Configuration(builder.Configuration)...);
```

## Decision Guide

| Scenario | Recommendation |
|----------|---------------|
| Application logging setup | Load `serilog` — `AddSerilog()` two-stage bootstrap |
| Distributed tracing / metrics | Load `opentelemetry` — OTLP exporter |
| Custom business metrics | `IMeterFactory` + counters/histograms (`opentelemetry` skill) |
| Request tracing | Correlation ID middleware (this skill) |
| Container health | `/health/live` and `/health/ready` endpoints (this skill) |
| Log storage | Seq (development), Elastic/Grafana/OTLP backend (production) |
| Log levels | Debug in dev, Information in staging, Warning default in production |
