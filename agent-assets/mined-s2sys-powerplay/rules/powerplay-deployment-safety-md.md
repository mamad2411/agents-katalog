---
name: deployment-safety
description: Pre-deploy checklist — environment config, secret management, health checks, Dockerfile standards, CI gates
globs: ["**/appsettings*.json", "**/Dockerfile", "**/*.yml", "**/*.yaml"]
alwaysApply: false
---

# Deployment Safety

Production deployments must pass strict safety checks: environment-specific config, no secrets in source, health checks, container hardening, and CI gates.

## Environment Configuration

**ALWAYS**:
- Use `appsettings.{Environment}.json` for environment-specific values (Development, Staging, Production)
- Base `appsettings.json` contains ONLY common defaults (never secrets)
- Values loaded in this order: base → environment → environment variables (env vars win)
- All secrets (`apiKey`, `connectionString`, `password`) come from environment variables
- Use `.env` file locally (never committed to git)
- Use secrets manager in production (Azure Key Vault, AWS Secrets Manager, HashiCorp Vault)
- Log which config is loaded on startup: `Configuration loaded: Production, 42 values, 0 errors`

**NEVER**:
- Hardcode secrets in source code (including config files)
- Commit `.env`, `appsettings.Production.json`, or `secrets.json`
- Use same connection string for dev/staging/production
- Load config from environment variables without validation
- Store secrets in Docker image (use secret mounts)
- Log sensitive values (passwords, tokens, keys) anywhere

### ✅ GOOD Configuration (C# ASP.NET Core)
```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Load config in correct order
builder.Configuration
    .AddJsonFile("appsettings.json", optional: false)
    .AddJsonFile($"appsettings.{builder.Environment.EnvironmentName}.json", optional: true)
    .AddEnvironmentVariables();

// Validate on startup
var dbConfig = builder.Configuration.GetSection("Database");
if (string.IsNullOrEmpty(dbConfig["ConnectionString"]))
{
    throw new InvalidOperationException(
        "Missing Database:ConnectionString. Set via appsettings.Production.json or environment variable DB_CONNECTION_STRING"
    );
}

// Log config loaded (non-sensitive only)
var env = builder.Environment.EnvironmentName;
var configCount = builder.Configuration.AsEnumerable().Count();
Console.WriteLine($"✓ Configuration loaded: {env}, {configCount} values");

var app = builder.Build();

// Verify health on startup
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
    await db.Database.CanConnectAsync();
    Console.WriteLine("✓ Database connected");
}

app.Run();
```

### ✅ GOOD appsettings.json (base)
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning"
    }
  },
  "Database": {
    "ConnectionString": "NOT_SET_CONFIGURE_ENVIRONMENT",
    "CommandTimeout": 30
  },
  "Cache": {
    "Enabled": true,
    "DurationSeconds": 300
  }
}
```

### ✅ GOOD appsettings.Production.json
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Warning"
    }
  },
  "Database": {
    "CommandTimeout": 60
  },
  "AllowedOrigins": ["https://app.example.com"],
  "SecurityHeaders": {
    "StrictTransportSecurity": "max-age=31536000; includeSubDomains"
  }
}
```

### ✅ GOOD .env.example (Template, NEVER commit actual .env)
```bash
# Copy to .env and fill in your local values
# NEVER commit .env to git

DB_CONNECTION_STRING=Server=localhost;Database=MyDb;User Id=sa;Password=YourPassword
API_KEY=your-api-key-here
OPENROUTER_API_KEY=your-openrouter-key
JWT_SECRET=your-jwt-secret-min-32-chars
```

### ❌ BAD Configuration
```csharp
// Hardcoded secret (CRITICAL SECURITY ISSUE)
var connectionString = "Server=prod.example.com;User Id=admin;Password=SuperSecret123!";

// No validation
var apiKey = Environment.GetEnvironmentVariable("API_KEY");

// Logging secrets
Console.WriteLine($"Connecting with: {connectionString}");

// Same config everywhere
var dbConfig = "Server=localhost;Database=MyDb";
```

---

## Health Checks and Readiness

**ALWAYS**:
- Implement `/health` endpoint (liveness probe — is service running?)
- Implement `/health/ready` endpoint (readiness probe — is service ready for traffic?)
- Liveness checks: memory usage, process running (fast, < 100ms)
- Readiness checks: database connectivity, cache reachability, external service connectivity
- Return `200 OK` when healthy, `503 Service Unavailable` when degraded
- Include health status in logs on every probe
- Document probe thresholds (e.g., memory > 80% = unhealthy)
- Set Kubernetes probes: `initialDelaySeconds: 10, periodSeconds: 10, timeoutSeconds: 5, failureThreshold: 3`

**NEVER**:
- Skip health checks in production
- Make health checks too expensive (should be < 100ms total)
- Return `200 OK` when any critical dependency is down
- Include sensitive data in health check responses
- Make health checks require authentication

### ✅ GOOD Health Check (C# ASP.NET Core)
```csharp
// Program.cs
builder.Services.AddHealthChecks()
    .AddDbContextCheck<ApplicationDbContext>(
        name: "Database",
        failureStatus: HealthStatus.Unhealthy
    )
    .AddCheck<RedisHealthCheck>(
        name: "Redis",
        failureStatus: HealthStatus.Degraded
    );

var app = builder.Build();

// Liveness: is the service running?
app.MapGet("/health", async (HealthCheckService healthCheck) =>
{
    var result = await healthCheck.CheckHealthAsync();
    if (result.Status == HealthStatus.Healthy)
    {
        return Results.Ok(new { status = "healthy", timestamp = DateTime.UtcNow });
    }
    return Results.StatusCode(503);
});

// Readiness: can we accept traffic?
app.MapGet("/health/ready", async (HealthCheckService healthCheck) =>
{
    var result = await healthCheck.CheckHealthAsync();
    var entries = result.Entries
        .Where(e => e.Value.Status == HealthStatus.Unhealthy)
        .Select(e => new { component = e.Key, issue = e.Value.Description });

    if (result.Status == HealthStatus.Healthy)
    {
        return Results.Ok(new { ready = true });
    }

    return Results.StatusCode(503);
});

app.Run();

// Custom health check
public class RedisHealthCheck : IHealthCheck
{
    private readonly IConnectionMultiplexer _redis;

    public RedisHealthCheck(IConnectionMultiplexer redis)
    {
        _redis = redis;
    }

    public async Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext context, CancellationToken cancellationToken = default)
    {
        try
        {
            var server = _redis.GetServer(_redis.GetEndPoints().First());
            await server.PingAsync();
            return HealthCheckResult.Healthy("Redis is reachable");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("Redis is unreachable", ex);
        }
    }
}
```

---

## Docker Container Hardening

**ALWAYS**:
- Use minimal base image (`alpine`, `debian:bookworm-slim`, not `latest`)
- Run as non-root user (never `USER root`)
- Multi-stage build (separate build from runtime)
- No secrets in image (use runtime environment variables or secret mounts)
- Scan image for vulnerabilities (`docker scan`, Snyk, Trivy)
- Set resource limits (memory, CPU)
- Use health checks in Dockerfile
- Log to stdout/stderr (not files; container orchestrators capture logs)

**NEVER**:
- Use `FROM ubuntu` or `FROM debian` (too large, too many packages)
- Run as root
- Include credentials in image
- Copy `.env` or secrets file into image
- Forget `CMD` or entrypoint
- Use `latest` tag in production
- Set unbounded resource requests

### ✅ GOOD Dockerfile (Multi-stage .NET)
```dockerfile
# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build
WORKDIR /src

# Copy project files
COPY ["MyApp.csproj", "."]
RUN dotnet restore "MyApp.csproj"

# Copy source and build
COPY . .
RUN dotnet build "MyApp.csproj" -c Release -o /app/build

# Publish
FROM build AS publish
RUN dotnet publish "MyApp.csproj" -c Release -o /app/publish

# Runtime stage
FROM mcr.microsoft.com/dotnet/runtime:8.0-alpine
WORKDIR /app

# Security: non-root user
RUN addgroup -g 1001 appuser && adduser -u 1001 -G appuser -s /bin/sh appuser

# Copy published app
COPY --from=publish /app/publish .

# Switch to non-root
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# Expose port
EXPOSE 8080

# Run
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

### ✅ GOOD Dockerfile (Node/TypeScript)
```dockerfile
# Build stage
FROM node:20-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Runtime stage
FROM node:20-alpine
WORKDIR /app

# Non-root user
RUN addgroup -g 1001 appuser && adduser -u 1001 -G appuser -s /bin/sh appuser

# Copy built app from build stage
COPY --from=build --chown=appuser:appuser /app/dist ./dist
COPY --from=build --chown=appuser:appuser /app/node_modules ./node_modules
COPY --chown=appuser:appuser package.json .

# Switch to non-root
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})"

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### ❌ BAD Dockerfile
```dockerfile
# Too large base image
FROM ubuntu:latest

# Running as root
# (no USER statement)

# Secrets hardcoded
ENV API_KEY=sk-1234567890
ENV DB_PASSWORD=SuperSecret123!

# No health check
# No resource limits
ENTRYPOINT ["npm", "start"]
```

---

## Pre-Deployment Checklist

**Before every production deployment:**

### Code
- [ ] All tests passing (unit, integration, e2e)
- [ ] Code review completed (at least 1 approval)
- [ ] No `console.log()` in production code (use structured logging)
- [ ] No hardcoded secrets, API keys, or connection strings
- [ ] No `TODO`, `FIXME`, or `HACK` comments in critical paths
- [ ] Vulnerable dependencies patched (`npm audit`, `dotnet list package --vulnerable`)

### Configuration
- [ ] Environment variables set in target environment
- [ ] Secrets in vault, not in config files
- [ ] Database migrations scripted and reversible
- [ ] Configuration validated on startup

### Deployment
- [ ] Blue-green deployment or canary available
- [ ] Rollback plan documented and tested
- [ ] Health checks passing in staging
- [ ] Load balancer configured correctly
- [ ] DNS/SSL certificates valid

### Monitoring
- [ ] Logging configured (structured logs, correct level)
- [ ] Alerts configured (high error rate, downtime, etc.)
- [ ] Metrics exported (latency, throughput, errors)
- [ ] On-call rotation aware of deployment

### Security
- [ ] OWASP Top 10 review done
- [ ] Input validation and output encoding in place
- [ ] Authentication and authorization working
- [ ] HTTPS only, HSTS headers set
- [ ] CORS configured correctly (not `*` in production)

---

## Deployment Checklist

- [ ] No hardcoded secrets anywhere
- [ ] Environment-specific config in appsettings.{env}.json
- [ ] All secrets in environment variables from vault
- [ ] Health checks implemented and passing
- [ ] Docker image scanned for vulnerabilities
- [ ] Non-root user in Dockerfile
- [ ] Resource limits set (memory, CPU)
- [ ] Logging to stdout/stderr
- [ ] All tests passing
- [ ] Rollback plan documented and tested
- [ ] On-call team aware of changes
