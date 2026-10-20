---
name: observability-standards
description: Observability standards — structured logging, distributed tracing, metrics, health checks
globs: ["**/*.cs", "**/*.ts", "**/appsettings*.json"]
alwaysApply: false
---

# Observability Standards — Logging, Tracing, Metrics

Good observability means you can understand production behavior without debugging production. This requires structured logs, distributed tracing, and metrics. Build observability in from day one.

---

## Structured Logging

**ALWAYS**:
- Use ILogger<T> (C#) or structured logger (Winston, Pino in TypeScript)
- Log in key=value format, not string interpolation
- Include context: userId, requestId, correlationId, operation name
- Log at appropriate level: Debug, Info, Warn, Error
- Never log secrets: passwords, API keys, tokens, PII (SSN, email)
- Include exception details (stacktrace, inner exceptions)
- Use consistent log field names across all services

**NEVER**:
- Log sensitive data (passwords, tokens, credit cards)
- Use string interpolation for logs: `logger.Info($"User {userId} logged in")` ❌
- Log without context (no way to trace back to request)
- Swallow exceptions: catch and return null without logging
- Log full objects (just the relevant fields)
- Different log format per method (inconsistent parsing)

### ✅ GOOD Structured Logging (C#)

```csharp
// ILogger with structured fields (key=value)
logger.LogInformation(
  "User login successful: userId={UserId}, email={Email}, timestamp={Timestamp}",
  userId, email, DateTime.UtcNow);

// With correlation ID (for distributed tracing)
logger.LogInformation(
  "Processing order: orderId={OrderId}, correlationId={CorrelationId}",
  orderId, Activity.Current?.Id);

// Error with exception context
try {
  await database.SaveAsync(user);
} catch (Exception ex) {
  logger.LogError(ex,
    "Failed to save user: userId={UserId}, error={ErrorMessage}",
    userId, ex.Message);
  throw;
}

// Warn with actionable detail
if (executionTime > 2000) {
  logger.LogWarning(
    "Slow query detected: query={Query}, duration={DurationMs}, threshold={ThresholdMs}",
    sqlQuery, executionTime, 2000);
}
```

### ✅ GOOD Structured Logging (TypeScript)

```typescript
// Winston with structured fields
logger.info('User login successful', {
  userId: user.id,
  email: user.email,
  timestamp: new Date().toISOString(),
  correlationId: req.id
});

// With request context
logger.error('Database query failed', {
  userId: req.user?.id,
  query: 'SELECT...', // SQL only, never result set
  error: err.message,
  correlationId: req.id
});

// Warn for slow operations
if (duration > 2000) {
  logger.warn('Slow API endpoint', {
    endpoint: req.path,
    durationMs: duration,
    threshold: 2000,
    correlationId: req.id
  });
}
```

### ❌ BAD Logging

```csharp
// ❌ String interpolation (can't parse/search)
logger.LogInformation($"User {userId} with email {email} logged in");

// ❌ Logging secrets
logger.LogInformation($"API key: {apiKey}");

// ❌ No context (can't trace back to request)
logger.LogInformation("Order processed");

// ❌ Logging full objects (huge, unreadable)
logger.LogInformation($"User object: {JsonConvert.SerializeObject(user)}");

// ❌ Swallowing exceptions
try {
  await db.SaveAsync(user);
} catch {
  return null; // Silent failure — no log!
}
```

---

## Correlation & Request Tracing

**ALWAYS**:
- Generate correlationId on entry (API, message, scheduled job)
- Pass correlationId through all calls (headers, message metadata, context)
- Log correlationId with every log statement
- Use Activity.Current (C#) or OpenTelemetry context
- Include traceId for distributed tracing across services

**NEVER**:
- Lose correlation ID between services (always pass in headers)
- Create new correlationId mid-request (use the same ID end-to-end)
- Log without correlationId (impossible to trace the request)

### ✅ GOOD Correlation (C#)

```csharp
// Middleware: Generate correlation ID if missing
public class CorrelationMiddleware {
  public async Task InvokeAsync(HttpContext context) {
    var correlationId = context.Request.Headers
      .FirstOrDefault(h => h.Key == "X-Correlation-Id").Value.FirstOrDefault()
      ?? Guid.NewGuid().ToString();
    
    context.Items["CorrelationId"] = correlationId;
    Activity.Current?.AddTag("correlationId", correlationId);
    
    context.Response.Headers.Add("X-Correlation-Id", correlationId);
    await next(context);
  }
}

// Service: Use correlation ID in all logs
public class OrderService {
  public async Task ProcessOrderAsync(int orderId, string correlationId) {
    _logger.LogInformation(
      "Processing order: orderId={OrderId}, correlationId={CorrelationId}",
      orderId, correlationId);
    
    try {
      var order = await _orderRepository.GetAsync(orderId);
      _logger.LogInformation(
        "Order loaded: orderId={OrderId}, items={ItemCount}, correlationId={CorrelationId}",
        orderId, order.Items.Count, correlationId);
      
      await _paymentService.ProcessAsync(order, correlationId); // Pass along
    } catch (Exception ex) {
      _logger.LogError(ex,
        "Order processing failed: orderId={OrderId}, correlationId={CorrelationId}",
        orderId, correlationId);
      throw;
    }
  }
}

// Call to another service: Always pass correlation ID
var response = await _httpClient.GetAsync(
  $"/api/v1/payment/process",
  headers: new() { ["X-Correlation-Id"] = correlationId });
```

### ✅ GOOD Correlation (TypeScript)

```typescript
// Express middleware: correlationId tracking
app.use((req, res, next) => {
  const correlationId = req.headers['x-correlation-id'] || uuidv4();
  req.id = correlationId;
  res.set('X-Correlation-Id', correlationId);
  
  // Store in async context for use throughout request
  asyncLocalStorage.run({ correlationId }, () => next());
});

// Service: log with correlationId from context
class OrderService {
  async processOrder(orderId: number) {
    const { correlationId } = asyncLocalStorage.getStore();
    logger.info('Processing order', { orderId, correlationId });
    
    try {
      const order = await this.repository.get(orderId);
      logger.info('Order loaded', { orderId, itemCount: order.items.length, correlationId });
      
      await this.paymentService.process(order, correlationId); // Pass along
    } catch (error) {
      logger.error('Order processing failed', { orderId, correlationId, error: error.message });
      throw error;
    }
  }
}
```

---

## Metrics & Monitoring

**ALWAYS**:
- Track key business metrics: orders/hour, users online, payment success rate
- Track system metrics: request latency (P50, P95, P99), error rate, CPU, memory
- Use consistent metric names across services
- Tag metrics with dimensions: environment, service, endpoint
- Expose metrics in Prometheus format (/metrics endpoint)

**NEVER**:
- Ignore slow endpoints (measure everything that matters)
- Mix metrics with logs (separate concerns)
- Create high-cardinality metrics (unique value per user = bad)

### ✅ GOOD Metrics (C#)

```csharp
// Using Prometheus.NET
public class OrderMetrics {
  private static readonly Counter OrdersProcessed = Metrics
    .CreateCounter("orders_processed_total", "Total orders processed",
      labelNames: new[] { "status", "environment" });
  
  private static readonly Histogram OrderProcessingDuration = Metrics
    .CreateHistogram("order_processing_duration_seconds", "Order processing duration",
      labelNames: new[] { "service", "status" });
  
  public async Task ProcessOrderAsync(Order order) {
    var watch = Stopwatch.StartNew();
    try {
      await _service.ProcessAsync(order);
      watch.Stop();
      
      OrdersProcessed.Labels("success", Environment.GetEnvironmentVariable("ENVIRONMENT")).Inc();
      OrderProcessingDuration.Labels("OrderService", "success").Observe(watch.Elapsed.TotalSeconds);
    } catch (Exception ex) {
      OrdersProcessed.Labels("error", Environment.GetEnvironmentVariable("ENVIRONMENT")).Inc();
      OrderProcessingDuration.Labels("OrderService", "error").Observe(watch.Elapsed.TotalSeconds);
      throw;
    }
  }
}

// Expose metrics at /metrics
app.MapGet("/metrics", async (HttpContext context) => {
  await Metrics.DefaultRegistry.CollectAndSerializeAsPrometheusAsync(context.Response);
});
```

### ✅ GOOD Metrics (TypeScript + Prom Client)

```typescript
// Prometheus metrics
const ordersProcessed = new Counter({
  name: 'orders_processed_total',
  help: 'Total orders processed',
  labelNames: ['status', 'environment']
});

const orderDuration = new Histogram({
  name: 'order_processing_duration_seconds',
  help: 'Order processing duration',
  labelNames: ['service', 'status']
});

async function processOrder(order: Order) {
  const timer = orderDuration.startTimer({ service: 'OrderService' });
  try {
    await service.process(order);
    ordersProcessed.labels('success', process.env.ENVIRONMENT || 'dev').inc();
    timer({ status: 'success' });
  } catch (error) {
    ordersProcessed.labels('error', process.env.ENVIRONMENT || 'dev').inc();
    timer({ status: 'error' });
    throw error;
  }
}

// Expose metrics
app.get('/metrics', (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(register.metrics());
});
```

---

## Health Checks

**ALWAYS**:
- Expose /health endpoint (liveness check)
- Expose /health/ready endpoint (readiness check)
- Check external dependencies: database, cache, APIs
- Return JSON with service status, dependencies, version
- Use appropriate HTTP status: 200 OK, 503 Service Unavailable

**NEVER**:
- Skip health checks in health-dependent systems (Kubernetes, load balancers)
- Report success if dependencies fail (propagate failures)

### ✅ GOOD Health Check (C#)

```csharp
public class HealthCheckController : ControllerBase {
  private readonly IHealthCheckService _healthCheck;
  
  [HttpGet("/health")]
  public async Task<IActionResult> Liveness() {
    // Simple: is this service running?
    return Ok(new { status = "healthy", timestamp = DateTime.UtcNow });
  }
  
  [HttpGet("/health/ready")]
  public async Task<IActionResult> Readiness() {
    // Complex: can this service handle requests?
    var dbCheck = await _healthCheck.CheckDatabaseAsync();
    var cacheCheck = await _healthCheck.CheckCacheAsync();
    var apiCheck = await _healthCheck.CheckExternalApiAsync();
    
    if (dbCheck.Status != HealthStatus.Healthy) {
      return StatusCode(503, new {
        status = "unhealthy",
        reason = "database unavailable",
        checks = new { database = dbCheck.Status, cache = cacheCheck.Status }
      });
    }
    
    return Ok(new {
      status = "ready",
      version = "2.1.0",
      timestamp = DateTime.UtcNow,
      checks = new {
        database = dbCheck.Status,
        cache = cacheCheck.Status,
        externalApi = apiCheck.Status
      }
    });
  }
}
```

### ✅ GOOD Health Check (TypeScript + Express)

```typescript
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

app.get('/health/ready', async (req, res) => {
  const dbCheck = await checkDatabase();
  const cacheCheck = await checkCache();
  const apiCheck = await checkExternalApi();
  
  if (dbCheck.status !== 'healthy') {
    return res.status(503).json({
      status: 'unhealthy',
      reason: 'database unavailable',
      checks: { database: dbCheck.status, cache: cacheCheck.status }
    });
  }
  
  res.json({
    status: 'ready',
    version: '2.1.0',
    timestamp: new Date().toISOString(),
    checks: {
      database: dbCheck.status,
      cache: cacheCheck.status,
      externalApi: apiCheck.status
    }
  });
});
```

---

## Log Levels

| Level | Use Case | Example |
|-------|----------|---------|
| **Debug** | Development & troubleshooting | Variable values, loop iterations, cache hits |
| **Info** | Significant events | User login, order placed, service started |
| **Warn** | Unexpected but recoverable | Slow query, retry attempt, missing optional field |
| **Error** | Errors that need attention | Database connection failed, validation error, API timeout |

### ✅ GOOD Log Level Usage

```csharp
// Debug: Too verbose for production
logger.LogDebug("Cache lookup for key={CacheKey}, hit={IsCacheHit}", cacheKey, isCacheHit);

// Info: User-facing events
logger.LogInformation("User login: userId={UserId}, email={Email}", userId, email);

// Warn: Something unexpected (but handled)
logger.LogWarning("Retry attempt {Attempt} of {MaxRetries} for order={OrderId}", attempt, maxRetries, orderId);

// Error: Requires attention
logger.LogError(ex, "Payment processing failed: orderId={OrderId}, error={ErrorMessage}", orderId, ex.Message);
```

---

## Observability Checklist

- [ ] All services use ILogger<T> (C#) or structured logger (TypeScript)
- [ ] Logs include correlationId for tracing
- [ ] No sensitive data logged (PII, secrets, tokens)
- [ ] Structured key=value format (not string interpolation)
- [ ] Health check endpoints expose status + dependencies
- [ ] Metrics track key business and system operations
- [ ] Metrics exposed in Prometheus format
- [ ] Log levels used appropriately (Debug, Info, Warn, Error)
- [ ] Error logs include exception details
- [ ] Slow operations (> 2s) trigger warnings
- [ ] All services can be monitored without connecting to production
- [ ] Request tracing works end-to-end across services

---

## Summary

Good observability means:
1. **Structured logs** — key=value format with context
2. **Request tracing** — correlationId through all calls
3. **Metrics** — business & system health measured
4. **Health checks** — dependencies verified on demand
5. **No secrets** — never log passwords, tokens, PII
6. **Context** — every log tied to request, user, operation

This prevents firefighting in production and enables confident deployments.
