---
name: api-gateway-patterns
description: API gateway patterns — Request routing, composition, rate limiting, versioning, security headers, caching
globs: ["**/*.cs", "**/*.ts", "**/*.js", "**/*.yaml", "**/*.yml"]
alwaysApply: false
---

# API Gateway Patterns

API gateways sit between clients and backend services, providing routing, composition, rate limiting, security, and caching. Build scalable, secure, and maintainable APIs.

---

## API Gateway Responsibilities

**ALWAYS**:
- Route requests to correct backend service (path-based: /api/orders → OrderService)
- Authenticate & authorize (JWT, OAuth, API keys)
- Rate limit (per user, per IP, per endpoint)
- Cache responses (reduce backend load)
- Transform responses (consistent format, version handling)
- Add security headers (CORS, CSP, X-Frame-Options)
- Log requests (audit trail, debugging)
- Handle versioning (/api/v1, /api/v2)

**NEVER**:
- Add business logic (that belongs in services)
- Store state (gateways are stateless)
- Trust external input (validate everything)
- Expose backend services directly

### ✅ GOOD API Gateway Design

```
Client
  ↓
┌─────────────────────────────────┐
│  API Gateway                    │
├─────────────────────────────────┤
│ • Authentication (JWT validate) │
│ • Rate limiting (per user)      │
│ • Request routing               │
│ • Response caching              │
│ • Security headers (CORS, CSP)  │
│ • Logging & monitoring          │
└─────────────────────────────────┘
  ↓     ↓     ↓     ↓
OrderService | PaymentService | UserService | ProductService
(internal, never exposed directly)
```

---

## Request Routing

**ALWAYS**:
- Route by path (/api/orders → OrderService)
- Route by method (GET orders vs. POST create order)
- Route by header (Accept: application/json vs. application/xml)
- Handle 404 for unmapped routes
- Document all routes (OpenAPI spec)

**NEVER**:
- Expose backend service URLs directly
- Hardcode service addresses (use service discovery)
- Allow routing to unregistered services

### ✅ GOOD Request Routing

```csharp
// API Gateway using Ocelot (ASP.NET)
public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        services.AddOcelot();
    }
    
    public void Configure(IApplicationBuilder app)
    {
        app.UseRouting();
        app.UseEndpoints(endpoints =>
        {
            // Route /api/orders/* to OrderService
            endpoints.MapGet("/api/orders", OrderServiceRoute);
            endpoints.MapGet("/api/orders/{id}", OrderServiceRoute);
            endpoints.MapPost("/api/orders", OrderServiceRoute);
            
            // Route /api/payments/* to PaymentService
            endpoints.MapGet("/api/payments", PaymentServiceRoute);
            endpoints.MapPost("/api/payments", PaymentServiceRoute);
            
            // Route /api/users/* to UserService
            endpoints.MapGet("/api/users/{id}", UserServiceRoute);
            
            // Catch unmapped routes
            endpoints.MapFallback(ctx => 
                ctx.Response.StatusCode = 404);
        });
        
        app.UseOcelot().Wait();
    }
}

// Ocelot configuration (appsettings.json)
{
  "Routes": [
    {
      "DownstreamPathTemplate": "/orders/{everything}",
      "DownstreamScheme": "http",
      "DownstreamHostAndPorts": [
        {
          "Host": "order-service",
          "Port": 80
        }
      ],
      "UpstreamPathTemplate": "/api/orders/{everything}",
      "UpstreamHttpMethod": ["Get", "Post", "Put", "Delete"],
      "RateLimitOptions": {
        "EnableRateLimiting": true,
        "Period": "1m",
        "Limit": 100
      },
      "AuthenticationOptions": {
        "AuthenticationProviderKey": "Bearer",
        "AllowedScopes": ["orders:read", "orders:write"]
      }
    },
    {
      "DownstreamPathTemplate": "/payments/{everything}",
      "DownstreamScheme": "http",
      "DownstreamHostAndPorts": [
        {
          "Host": "payment-service",
          "Port": 80
        }
      ],
      "UpstreamPathTemplate": "/api/payments/{everything}",
      "UpstreamHttpMethod": ["Post"],
      "RateLimitOptions": {
        "EnableRateLimiting": true,
        "Period": "1m",
        "Limit": 50  // Stricter limit for payments
      }
    }
  ],
  
  "GlobalConfiguration": {
    "ServiceDiscoveryProvider": {
      "Type": "Consul",
      "Host": "consul",
      "Port": 8500
    },
    "RateLimitOptions": {
      "EnableRateLimiting": true,
      "HttpStatusCode": 429,
      "ClientIdHeader": "X-Client-ID"
    }
  }
}
```

---

## API Composition

**ALWAYS**:
- Aggregate responses from multiple services (client makes 1 request, gateway calls multiple services)
- Parallel calls when independent (order + user details)
- Sequential calls when dependent (get order, then get payments for order)
- Handle partial failures (return available data + error)
- Timeout per service (prevent hanging)

**NEVER**:
- Block client on slowest service (use circuit breaker)
- Ignore failures (inform client of partial data)
- Make synchronous calls to sync services (defeats async pattern)

### ✅ GOOD API Composition

```csharp
// Composite endpoint - combines data from 3 services
[HttpGet("api/orders/{orderId}/full")]
public async Task<OrderSummaryDto> GetOrderSummaryAsync(Guid orderId)
{
    // Call services in parallel (independent data)
    var orderTask = _orderServiceClient.GetOrderAsync(orderId);
    var paymentTask = _paymentServiceClient.GetPaymentsAsync(orderId);
    var customerTask = _userServiceClient.GetCustomerAsync(orderId);
    
    try
    {
        await Task.WhenAll(orderTask, paymentTask, customerTask);
        
        return new OrderSummaryDto
        {
            Order = await orderTask,
            Payments = await paymentTask,
            CustomerDetails = await customerTask
        };
    }
    catch (TimeoutException ex)
    {
        // Partial response if one service times out
        return new OrderSummaryDto
        {
            Order = await orderTask,
            Payments = await paymentTask,
            CustomerDetails = null,  // Failed to fetch
            PartialData = true,
            Error = "Customer details unavailable"
        };
    }
}

// Service client with timeout & circuit breaker
public class OrderServiceClient
{
    private readonly HttpClient _httpClient;
    private readonly IAsyncPolicy<HttpResponseMessage> _circuitBreaker;
    
    public OrderServiceClient(HttpClient httpClient)
    {
        _httpClient = httpClient;
        
        // Circuit breaker: fail fast if service is down
        _circuitBreaker = Policy
            .Handle<HttpRequestException>()
            .Or<TaskCanceledException>()
            .OrResult<HttpResponseMessage>(r => !r.IsSuccessStatusCode)
            .CircuitBreakerAsync<HttpResponseMessage>(
                handledEventsAllowedBeforeBreaking: 5,
                durationOfBreak: TimeSpan.FromSeconds(30)
            );
    }
    
    public async Task<OrderDto> GetOrderAsync(Guid orderId)
    {
        var request = new HttpRequestMessage(
            HttpMethod.Get,
            $"http://order-service/api/orders/{orderId}"
        );
        
        // Execute with timeout & circuit breaker
        using (var cts = new CancellationTokenSource(TimeSpan.FromSeconds(5)))
        {
            var response = await _circuitBreaker.ExecuteAsync(
                () => _httpClient.SendAsync(request, cts.Token)
            );
            
            return await response.Content.ReadAsAsync<OrderDto>();
        }
    }
}
```

---

## Rate Limiting

**ALWAYS**:
- Limit by user/API key (authenticated)
- Limit by IP (anonymous)
- Different limits for different endpoints (payments stricter than reads)
- Use sliding window (fair distribution)
- Return 429 Too Many Requests (with Retry-After header)
- Persist rate limit state (Redis for distributed systems)

**NEVER**:
- Limit without informing client (return 429)
- Use fixed window (unfair bursts at boundary)
- Block all traffic at first limit (implement backoff)

### ✅ GOOD Rate Limiting Setup

```csharp
// Rate limiting middleware using StackExchange.Redis
public class RateLimitingMiddleware
{
    private readonly IDatabase _redis;
    private readonly ILogger<RateLimitingMiddleware> _logger;
    
    public async Task InvokeAsync(HttpContext context)
    {
        // Get client identifier
        var clientId = context.Request.Headers["X-Client-ID"].ToString()
            ?? context.Connection.RemoteIpAddress?.ToString()
            ?? "unknown";
        
        // Get endpoint-specific limit
        var (limit, windowSeconds) = GetRateLimitForEndpoint(context.Request.Path);
        
        // Check rate limit (Redis-backed sliding window)
        var key = $"ratelimit:{clientId}:{context.Request.Path}";
        var current = await _redis.StringGetAsync(key);
        var count = current.HasValue ? int.Parse(current) : 0;
        
        if (count >= limit)
        {
            // Over limit - return 429
            context.Response.StatusCode = 429;
            context.Response.Headers.Add(
                "Retry-After",
                windowSeconds.ToString()
            );
            context.Response.Headers.Add(
                "X-RateLimit-Limit",
                limit.ToString()
            );
            context.Response.Headers.Add(
                "X-RateLimit-Remaining",
                "0"
            );
            
            _logger.LogWarning(
                "Rate limit exceeded for client {ClientId} on {Path}",
                clientId, context.Request.Path
            );
            
            await context.Response.WriteAsync("Rate limit exceeded");
            return;
        }
        
        // Increment counter with expiration
        var ttl = await _redis.KeyTimeToLiveAsync(key);
        if (!ttl.HasValue || ttl.Value.TotalSeconds < 0)
        {
            // New window
            await _redis.StringSetAsync(
                key,
                "1",
                TimeSpan.FromSeconds(windowSeconds)
            );
        }
        else
        {
            // Existing window
            await _redis.StringIncrementAsync(key);
        }
        
        // Add headers for remaining quota
        context.Response.Headers.Add(
            "X-RateLimit-Limit",
            limit.ToString()
        );
        context.Response.Headers.Add(
            "X-RateLimit-Remaining",
            (limit - count - 1).ToString()
        );
        
        await context.Next.Invoke(context);
    }
    
    private (int limit, int windowSeconds) GetRateLimitForEndpoint(string path)
    {
        return path switch
        {
            "/api/payments" => (50, 60),  // 50 req/minute
            "/api/orders" => (100, 60),   // 100 req/minute
            _ => (1000, 60)  // Default: 1000 req/minute
        };
    }
}

// Configure rate limiting
services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = "redis:6379";
});

app.UseMiddleware<RateLimitingMiddleware>();
```

---

## API Versioning

**ALWAYS**:
- Version in URL path (/api/v1, /api/v2) not header
- Maintain backward compatibility (old clients work with new API)
- Deprecate old versions (6-12 month notice)
- Keep old version running during transition
- Document breaking changes

**NEVER**:
- Remove old API versions without warning
- Break existing clients (maintain compatibility)
- Use version headers (URL path is clearer)

### ✅ GOOD API Versioning

```csharp
// Multiple API versions side-by-side

[ApiController]
[Route("api/v1/[controller]")]
public class OrdersV1Controller : ControllerBase
{
    [HttpGet("{id}")]
    public async Task<OrderV1Dto> GetOrderAsync(Guid id)
    {
        var order = await _orderService.GetOrderAsync(id);
        return new OrderV1Dto
        {
            Id = order.Id,
            Amount = order.Amount,
            Status = order.Status
        };
    }
}

[ApiController]
[Route("api/v2/[controller]")]
public class OrdersV2Controller : ControllerBase
{
    [HttpGet("{id}")]
    public async Task<OrderV2Dto> GetOrderAsync(Guid id)
    {
        var order = await _orderService.GetOrderAsync(id);
        return new OrderV2Dto
        {
            Id = order.Id,
            Amount = order.Amount,
            Status = order.Status,
            CreatedAt = order.CreatedAt,  // NEW in v2
            ShippingAddress = order.ShippingAddress  // NEW in v2
        };
    }
}

// API Gateway routes both versions
{
  "Routes": [
    {
      "UpstreamPathTemplate": "/api/v1/orders/{everything}",
      "DownstreamPathTemplate": "/api/orders/{everything}",
      "DownstreamScheme": "http",
      "DownstreamHostAndPorts": [{"Host": "order-service", "Port": 80}]
    },
    {
      "UpstreamPathTemplate": "/api/v2/orders/{everything}",
      "DownstreamPathTemplate": "/api/v2/orders/{everything}",
      "DownstreamScheme": "http",
      "DownstreamHostAndPorts": [{"Host": "order-service", "Port": 80}]
    }
  ]
}

// Deprecation headers
[HttpGet("{id}")]
[ApiVersion("1.0", Deprecated = true)]  // Mark as deprecated
public async Task<OrderV1Dto> GetOrderV1Async(Guid id)
{
    Response.Headers.Add("Deprecation", "true");
    Response.Headers.Add("Sunset", "Sun, 01 Jan 2027 00:00:00 GMT");  // When it disappears
    Response.Headers.Add("Link", "</api/v2/orders/{id}>; rel=\"successor-version\"");  // Migration link
    
    return await GetOrderAsync(id);
}
```

---

## Security Headers

**ALWAYS**:
- Content-Type: application/json (prevent MIME sniffing)
- X-Content-Type-Options: nosniff (don't guess content type)
- X-Frame-Options: DENY (prevent clickjacking)
- X-XSS-Protection: 1; mode=block (XSS protection)
- Strict-Transport-Security: max-age=31536000 (HTTPS only)
- Content-Security-Policy: strict policy
- CORS headers: Access-Control-Allow-Origin (restrictive)

**NEVER**:
- Send sensitive data in response headers
- Allow cross-origin requests from *
- Trust client-provided content type

### ✅ GOOD Security Headers

```csharp
// Security headers middleware
public class SecurityHeadersMiddleware
{
    private readonly RequestDelegate _next;
    
    public SecurityHeadersMiddleware(RequestDelegate next)
    {
        _next = next;
    }
    
    public async Task InvokeAsync(HttpContext context)
    {
        // Prevent MIME sniffing
        context.Response.Headers.Add("X-Content-Type-Options", "nosniff");
        
        // Prevent clickjacking
        context.Response.Headers.Add("X-Frame-Options", "DENY");
        
        // XSS protection (browser level)
        context.Response.Headers.Add("X-XSS-Protection", "1; mode=block");
        
        // Force HTTPS (1 year)
        context.Response.Headers.Add(
            "Strict-Transport-Security",
            "max-age=31536000; includeSubDomains; preload"
        );
        
        // Content Security Policy (strict)
        context.Response.Headers.Add(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
        );
        
        // Remove server header (don't advertise stack)
        context.Response.Headers.Remove("Server");
        
        // CORS (restrictive)
        var origin = context.Request.Headers["Origin"].ToString();
        if (IsAllowedOrigin(origin))
        {
            context.Response.Headers.Add("Access-Control-Allow-Origin", origin);
            context.Response.Headers.Add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
            context.Response.Headers.Add("Access-Control-Allow-Headers", "Content-Type, Authorization");
        }
        
        await _next(context);
    }
    
    private bool IsAllowedOrigin(string origin)
    {
        var allowedOrigins = new[] { "https://app.example.com", "https://admin.example.com" };
        return allowedOrigins.Contains(origin);
    }
}

// Register middleware
app.UseMiddleware<SecurityHeadersMiddleware>();
```

---

## Response Caching

**ALWAYS**:
- Cache GET requests (idempotent)
- Use Cache-Control header (public, max-age=300)
- Vary by query parameters
- Cache in Redis (distributed)
- Invalidate on state changes (DELETE/PUT/POST)

**NEVER**:
- Cache POST/PUT/DELETE (mutable operations)
- Cache authenticated responses (unless user-specific)
- Cache sensitive data without encryption

### ✅ GOOD Response Caching

```csharp
// Caching middleware
public class CachingMiddleware
{
    private readonly IDistributedCache _cache;
    
    [HttpGet("api/orders/{id}")]
    [ResponseCache(Duration = 300, VaryByQueryKeys = new[] { "id" })]  // 5 minutes
    public async Task<OrderDto> GetOrderAsync(Guid id)
    {
        var cacheKey = $"order:{id}";
        
        // Check cache
        var cached = await _cache.GetStringAsync(cacheKey);
        if (cached != null)
        {
            return JsonConvert.DeserializeObject<OrderDto>(cached);
        }
        
        // Get from database
        var order = await _db.Orders.FindAsync(id);
        
        // Cache for 5 minutes
        await _cache.SetStringAsync(
            cacheKey,
            JsonConvert.SerializeObject(order),
            new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5)
            }
        );
        
        return order;
    }
    
    [HttpPut("api/orders/{id}")]
    public async Task<IActionResult> UpdateOrderAsync(Guid id, UpdateOrderDto dto)
    {
        // Update order
        var order = await _orderService.UpdateOrderAsync(id, dto);
        
        // Invalidate cache
        await _cache.RemoveAsync($"order:{id}");
        
        return Ok(order);
    }
}
```

---

## API Gateway Checklist

- [ ] Request routing configured (path-based, method-based)
- [ ] Service discovery integrated (Consul, Kubernetes)
- [ ] Authentication implemented (JWT validation, OAuth)
- [ ] Authorization enforced (scopes, policies)
- [ ] Rate limiting configured (per user, per endpoint)
- [ ] API composition for complex queries
- [ ] Circuit breaker for failing services
- [ ] Response caching (Redis-backed)
- [ ] API versioning strategy (/api/v1, /api/v2)
- [ ] Security headers configured (CORS, CSP, HSTS)
- [ ] Logging & monitoring (request/response)
- [ ] Error handling standardized (consistent error format)
- [ ] Documentation updated (OpenAPI spec)

---

## Summary

Good API gateway patterns:
1. **Routing** — Smart request routing to correct service
2. **Composition** — Aggregate responses from multiple services
3. **Rate limiting** — Prevent abuse, fair usage
4. **Caching** — Reduce backend load, improve latency
5. **Versioning** — Manage API evolution, backward compatibility
6. **Security** — Authenticate, authorize, add security headers
7. **Monitoring** — Log requests, detect issues

API gateways are critical for scalable, secure microservice architectures.
