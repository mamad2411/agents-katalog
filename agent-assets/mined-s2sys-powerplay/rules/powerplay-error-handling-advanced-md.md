---
name: error-handling-advanced
description: Exception hierarchy, ProblemDetails, structured logging, resilience patterns
globs: ["**/*.cs"]
alwaysApply: false
---

# Advanced Error Handling

Design exception hierarchies. Use ProblemDetails RFC 7807 for API errors. Structured logging with context. Implement resilience with Polly.

## Exception Hierarchy

**ALWAYS**:
- Create custom exception hierarchy (domain exceptions)
- Inherit from `Exception` base or specific base (ArgumentException, InvalidOperationException)
- Never throw bare `Exception` or `ApplicationException`
- Provide context: message, inner exception, data properties
- Catch specific exceptions, not generic `Exception`

**NEVER**:
- Throw `Exception` without specificity
- Catch all with bare `catch { }`
- Swallow exceptions silently
- Expose internal stack traces to API clients
- Use exceptions for flow control

### ✅ GOOD Example
```csharp
// Custom exception hierarchy
public abstract class DomainException : Exception
{
  protected DomainException(string message) : base(message) { }
  protected DomainException(string message, Exception inner) : base(message, inner) { }
}

public class OrderNotFoundException : DomainException
{
  public int OrderId { get; }
  
  public OrderNotFoundException(int orderId) 
    : base($"Order {orderId} not found")
  {
    OrderId = orderId;
  }
}

public class InvalidOrderStateException : DomainException
{
  public string CurrentState { get; }
  
  public InvalidOrderStateException(string currentState, string message)
    : base(message)
  {
    CurrentState = currentState;
  }
}

// Exception handling
public async Task<Order> GetOrderAsync(int orderId, CancellationToken ct)
{
  try
  {
    return await _repository.GetOrderAsync(orderId, ct);
  }
  catch (OrderNotFoundException ex)
  {
    // Specific handling
    _logger.LogWarning(ex, "Order {OrderId} not found", ex.OrderId);
    throw; // Re-throw with context preserved
  }
}
```

### ❌ BAD Example
```csharp
// Generic exception - no context
public void ProcessOrder(Order order)
{
  throw new Exception("Error processing order");
}

// Bare catch - swallows context
try
{
  var order = await GetOrderAsync(id);
}
catch { } // Silent failure!

// Expose stack trace to client
public IActionResult GetOrder(int id)
{
  try
  {
    return Ok(_repository.GetOrder(id));
  }
  catch (Exception ex)
  {
    // NEVER return stack trace to client
    return BadRequest(ex.ToString());
  }
}

// Exception for flow control
try
{
  return int.Parse(value);
}
catch (FormatException)
{
  return 0; // Using exception for validation is slow and bad practice
}
```

---

## ProblemDetails RFC 7807

**ALWAYS**:
- Return `ProblemDetails` from exception handlers
- Include: type (URI), title, status, detail, instance
- Never expose stack traces in production
- Provide unique error code or correlation ID for tracking
- Include traceId for logging correlation

**NEVER**:
- Return raw exception messages
- Include sensitive data in error responses
- Return different error formats from different endpoints
- Omit status code from error response

### ✅ GOOD Example
```csharp
// Exception handler middleware
public class ExceptionHandlingMiddleware
{
  public async Task InvokeAsync(HttpContext context, ILogger<ExceptionHandlingMiddleware> logger)
  {
    try
    {
      await _next(context);
    }
    catch (Exception ex)
    {
      logger.LogError(ex, "Unhandled exception");
      await HandleExceptionAsync(context, ex, logger);
    }
  }
  
  private static Task HandleExceptionAsync(HttpContext context, Exception exception, ILogger logger)
  {
    context.Response.ContentType = "application/problem+json";
    
    var problemDetails = new ProblemDetails
    {
      Instance = context.Request.Path,
      Type = "https://yourdomain.com/errors/general-error",
      Title = "An error occurred",
      Status = StatusCodes.Status500InternalServerError,
      Detail = "An unexpected error occurred. Please contact support.",
      Extensions = new Dictionary<string, object>
      {
        { "traceId", context.TraceIdentifier }
      }
    };
    
    return context.Response.WriteAsJsonAsync(problemDetails);
  }
}

// Domain exception handler
[ExceptionHandler]
public IActionResult HandleOrderException(OrderNotFoundException ex)
{
  var problemDetails = new ProblemDetails
  {
    Type = "https://yourdomain.com/errors/order-not-found",
    Title = "Order Not Found",
    Status = StatusCodes.Status404NotFound,
    Detail = ex.Message,
    Extensions = new Dictionary<string, object>
    {
      { "orderId", ex.OrderId },
      { "timestamp", DateTime.UtcNow }
    }
  };
  
  return NotFound(problemDetails);
}
```

---

## Structured Logging

**ALWAYS**:
- Use `ILogger<T>` — never Console.WriteLine
- Include correlation ID or trace ID in all logs
- Use log levels correctly: Error, Warning, Information, Debug
- Include context: user ID, order ID, operation name
- Use structured properties (not string interpolation in message)

**NEVER**:
- Log passwords, API keys, PII
- Use string interpolation for business data (use properties)
- Log at high levels (Debug, Verbose) in production code path
- Ignore errors in logging itself

### ✅ GOOD Example
```csharp
// Structured logging with context
public async Task<Order> ProcessOrderAsync(int orderId, int userId, CancellationToken ct)
{
  using var scope = _logger.BeginScope("OrderProcessing");
  
  try
  {
    _logger.LogInformation(
      "Starting order processing. OrderId={OrderId}, UserId={UserId}", 
      orderId, 
      userId);
    
    var order = await _repository.GetOrderAsync(orderId, ct);
    _logger.LogInformation(
      "Order retrieved. Status={Status}, Total={Total}", 
      order.Status, 
      order.Total);
    
    // Process order
    
    _logger.LogInformation(
      "Order processed successfully. OrderId={OrderId}, Duration={Duration}ms",
      orderId,
      watch.ElapsedMilliseconds);
    
    return order;
  }
  catch (OrderNotFoundException ex)
  {
    _logger.LogWarning(
      ex, 
      "Order not found. OrderId={OrderId}, UserId={UserId}",
      orderId,
      userId);
    throw;
  }
  catch (Exception ex)
  {
    _logger.LogError(
      ex,
      "Error processing order. OrderId={OrderId}, UserId={UserId}",
      orderId,
      userId);
    throw;
  }
}
```

### ❌ BAD Example
```csharp
// String interpolation, no context
_logger.LogInformation($"Processing order {order}"); // Objects don't serialize well

// No structured properties
_logger.LogError("User login failed for user: " + username); // String concatenation

// Logging sensitive data
_logger.LogInformation($"API Key: {apiKey}, Password: {password}"); // NEVER!

// No correlation ID
_logger.LogError("Something failed"); // Can't trace which request this belongs to
```

---

## Resilience Patterns (Polly)

**ALWAYS**:
- Use Polly for external API calls
- Retry with exponential backoff (with jitter)
- Circuit breaker for failing services
- Timeout for all external calls
- Fallback when possible

**NEVER**:
- Immediate retry without delay (hammers failing service)
- Infinite retries
- No timeout on external calls (can hang indefinitely)

### ✅ GOOD Example
```csharp
// Polly resilience policy
var retryPolicy = Policy
  .Handle<HttpRequestException>()
  .Or<TimeoutException>()
  .WaitAndRetryAsync(
    retryCount: 3,
    sleepDurationProvider: retryAttempt =>
      TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)) + 
      TimeSpan.FromMilliseconds(Random.Shared.Next(0, 100)),
    onRetry: (outcome, delay, retry, context) =>
    {
      _logger.LogWarning(
        "Retry {Retry} after {Delay}ms. Endpoint: {Endpoint}",
        retry,
        delay.TotalMilliseconds,
        context["endpoint"]);
    });

var circuitBreakerPolicy = Policy
  .Handle<HttpRequestException>()
  .OrResult<HttpResponseMessage>(r => !r.IsSuccessStatusCode)
  .CircuitBreakerAsync(
    handledEventsAllowedBeforeBreaking: 3,
    durationOfBreak: TimeSpan.FromSeconds(30),
    onBreak: (outcome, duration) =>
    {
      _logger.LogError("Circuit breaker opened for {Duration}ms", duration.TotalMilliseconds);
    });

var timeoutPolicy = Policy.TimeoutAsync<HttpResponseMessage>(TimeSpan.FromSeconds(10));

var combinedPolicy = Policy.WrapAsync(retryPolicy, circuitBreakerPolicy, timeoutPolicy);

// Usage
var context = new Polly.Context { { "endpoint", "https://api.example.com/users" } };
var response = await combinedPolicy.ExecuteAsync(
  ctx => _httpClient.GetAsync("https://api.example.com/users"),
  context);
```

---

## Error Recovery Strategies

**Always have a plan for**:
- Network failures → retry with backoff
- Timeout → circuit breaker
- Rate limiting (429) → exponential backoff
- Server error (5xx) → retry
- Not found (404) → fail fast, don't retry
- Validation error (400) → fail fast, don't retry

### ✅ GOOD Example
```csharp
public async Task<User> GetUserWithFallbackAsync(int userId, CancellationToken ct)
{
  try
  {
    // Try primary service with timeout
    var cts = CancellationTokenSource.CreateLinkedTokenSource(ct);
    cts.CancelAfter(TimeSpan.FromSeconds(5));
    
    return await _userService.GetUserAsync(userId, cts.Token);
  }
  catch (OperationCanceledException)
  {
    _logger.LogWarning("User service timeout. UserId={UserId}", userId);
    
    // Fallback to cache
    return _cache.GetUser(userId) ?? throw new UserNotFoundException(userId);
  }
  catch (HttpRequestException ex) when (ex.StatusCode == HttpStatusCode.NotFound)
  {
    _logger.LogWarning("User not found. UserId={UserId}", userId);
    throw new UserNotFoundException(userId); // Fail fast
  }
}
```

---

## Error Handling Checklist

- [ ] Custom exception hierarchy defined
- [ ] Never throw bare `Exception`
- [ ] Specific exception catching (not bare `catch`)
- [ ] ProblemDetails used for API errors
- [ ] No stack traces exposed to clients
- [ ] ILogger<T> used (not Console)
- [ ] Structured logging with context
- [ ] No PII or secrets in logs
- [ ] Polly resilience policies for external calls
- [ ] Circuit breaker for failing services
- [ ] Timeout on all external calls
- [ ] Retry with exponential backoff
- [ ] Correlation ID/Trace ID in logs
