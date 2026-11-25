---
name: error-handling
description: Design a comprehensive error handling strategy for an application. Outputs error types, response formats, logging patterns, and user-facing messages.
argument-hint: [application type, language/framework]
allowed-tools: Read, Write
---

# Error Handling Strategy

Design a complete error handling system that catches errors, logs context, returns useful responses, and helps debug production issues. Not just try/catch everywhere — structured error types, consistent formats, and actionable logging.

## Process

1. **Categorize errors.** Client errors (400s), server errors (500s), business logic errors, infrastructure errors.
2. **Define error types.** Create error classes/types for each category.
3. **Design response format.** Consistent JSON structure with error codes, messages, details.
4. **Plan logging strategy.** What to log, log levels, structured context.
5. **Handle edge cases.** Database down, third-party timeout, out of memory.
6. **Set monitoring.** Error rate alerts, specific error type tracking.
7. **User-facing messages.** Technical errors get translated to user-friendly text.
8. **Document error codes.** Every error code has documentation with cause and resolution.

## Output Format

### Error Handling Strategy: [Application Name]

**Language:** [Python/JavaScript/Java/Go/etc.]  
**Framework:** [Django/Express/Spring/etc.]  
**Error Categories:** 6  
**Total Error Codes:** 42  

---

## Error Categories

### 1. Client Errors (4xx)
**Cause:** User sent invalid request  
**Who Fixes:** Client/User  
**HTTP Status:** 400-499  
**Log Level:** INFO (not errors, expected behavior)

### 2. Server Errors (5xx)
**Cause:** Application or infrastructure failure  
**Who Fixes:** Backend team  
**HTTP Status:** 500-599  
**Log Level:** ERROR (requires investigation)

### 3. Business Logic Errors
**Cause:** Valid request but business rules prevent action  
**Who Fixes:** User (change request) or Product (change rules)  
**HTTP Status:** 400 or 422  
**Log Level:** INFO

### 4. Infrastructure Errors
**Cause:** Database, cache, queue, external API failure  
**Who Fixes:** Infrastructure/SRE team  
**HTTP Status:** 503  
**Log Level:** ERROR

### 5. Timeout Errors
**Cause:** Operation exceeded time limit  
**Who Fixes:** Performance team or adjust limits  
**HTTP Status:** 408 or 504  
**Log Level:** WARNING

### 6. Unexpected Errors
**Cause:** Bugs, unhandled edge cases  
**Who Fixes:** Development team  
**HTTP Status:** 500  
**Log Level:** CRITICAL

---

## Error Type Hierarchy (Python Example)

```python
class AppError(Exception):
    """Base error class for all application errors"""
    def __init__(self, message, code, http_status=500, details=None):
        self.message = message
        self.code = code
        self.http_status = http_status
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(AppError):
    """Input validation failed"""
    def __init__(self, message, field=None, details=None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            http_status=400,
            details={"field": field, **(details or {})}
        )

class AuthenticationError(AppError):
    """User authentication failed"""
    def __init__(self, message="Invalid credentials"):
        super().__init__(
            message=message,
            code="AUTHENTICATION_FAILED",
            http_status=401
        )

class AuthorizationError(AppError):
    """User lacks permission"""
    def __init__(self, message="Permission denied", resource=None):
        super().__init__(
            message=message,
            code="AUTHORIZATION_DENIED",
            http_status=403,
            details={"resource": resource}
        )

class NotFoundError(AppError):
    """Resource not found"""
    def __init__(self, resource_type, resource_id):
        super().__init__(
            message=f"{resource_type} not found",
            code="RESOURCE_NOT_FOUND",
            http_status=404,
            details={"resource_type": resource_type, "resource_id": resource_id}
        )

class ConflictError(AppError):
    """Resource already exists or state conflict"""
    def __init__(self, message, conflict_type=None):
        super().__init__(
            message=message,
            code="RESOURCE_CONFLICT",
            http_status=409,
            details={"conflict_type": conflict_type}
        )

class BusinessRuleError(AppError):
    """Business logic prevents action"""
    def __init__(self, message, rule_name):
        super().__init__(
            message=message,
            code="BUSINESS_RULE_VIOLATION",
            http_status=422,
            details={"rule": rule_name}
        )

class ExternalServiceError(AppError):
    """Third-party service failed"""
    def __init__(self, service_name, message):
        super().__init__(
            message=f"{service_name} unavailable: {message}",
            code="EXTERNAL_SERVICE_ERROR",
            http_status=503,
            details={"service": service_name}
        )

class DatabaseError(AppError):
    """Database operation failed"""
    def __init__(self, operation, message):
        super().__init__(
            message=f"Database {operation} failed: {message}",
            code="DATABASE_ERROR",
            http_status=500,
            details={"operation": operation}
        )
```

---

## Error Response Format

### Standard JSON Structure
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email format is invalid",
    "field": "email",
    "request_id": "req_abc123",
    "timestamp": "2024-01-15T10:30:00Z",
    "details": {
      "provided": "not-an-email",
      "expected_format": "user@example.com"
    }
  }
}
```

### Fields Explanation
- `code`: Machine-readable error identifier (SCREAMING_SNAKE_CASE)
- `message`: Human-readable description (English, technical)
- `field`: (Optional) Which input field caused error
- `request_id`: Unique request identifier for log correlation
- `timestamp`: When error occurred (ISO 8601)
- `details`: Additional context (varies by error type)

---

## Error Code Catalog

| Code | HTTP | Meaning | User Action |
|------|------|---------|-------------|
| VALIDATION_ERROR | 400 | Input failed validation | Fix input format |
| MISSING_FIELD | 400 | Required field not provided | Add missing field |
| INVALID_FORMAT | 400 | Field format incorrect | Check format requirements |
| AUTHENTICATION_FAILED | 401 | Login credentials wrong | Check username/password |
| TOKEN_EXPIRED | 401 | Auth token expired | Re-login |
| AUTHORIZATION_DENIED | 403 | User lacks permission | Contact admin |
| RESOURCE_NOT_FOUND | 404 | Requested item doesn't exist | Check resource ID |
| RESOURCE_CONFLICT | 409 | Item already exists | Use existing item or change identifier |
| BUSINESS_RULE_VIOLATION | 422 | Action violates business logic | Review business rules |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests | Wait and retry |
| DATABASE_ERROR | 500 | Database operation failed | Retry or contact support |
| EXTERNAL_SERVICE_ERROR | 503 | Third-party API failed | Retry later |
| TIMEOUT_ERROR | 504 | Operation took too long | Simplify request or retry |

---

## Logging Strategy

### What to Log

**For Every Request:**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "request_id": "req_abc123",
  "method": "POST",
  "path": "/api/orders",
  "user_id": "user_xyz",
  "duration_ms": 247,
  "status": 201
}
```

**For Errors:**
```json
{
  "timestamp": "2024-01-15T10:30:15Z",
  "level": "ERROR",
  "request_id": "req_abc123",
  "error_code": "DATABASE_ERROR",
  "error_message": "Connection pool exhausted",
  "user_id": "user_xyz",
  "path": "/api/orders",
  "stack_trace": "...",
  "context": {
    "query": "INSERT INTO orders...",
    "pool_size": 10,
    "active_connections": 10
  }
}
```

### Log Levels

**DEBUG:** Development only, verbose  
**INFO:** Normal operations (requests, state changes)  
**WARNING:** Unexpected but handled (retry succeeded, slow query)  
**ERROR:** Failures requiring attention (database down, API timeout)  
**CRITICAL:** System-level failures (out of memory, corruption)

### Structured Logging (Python Example)
```python
import logging
import structlog

logger = structlog.get_logger()

# Good: Structured
logger.info(
    "order_created",
    order_id=order.id,
    user_id=user.id,
    amount=order.total,
    request_id=request_id
)

# Bad: String interpolation
logger.info(f"Order {order.id} created by {user.id} for ${order.total}")
```

---

## Error Handling Patterns

### API Endpoint (Express.js Example)
```javascript
app.post('/api/orders', async (req, res, next) => {
  try {
    // Validate input
    const { userId, items } = req.body;
    if (!userId) throw new ValidationError('Missing user_id', 'userId');
    
    // Business logic
    const user = await userService.getUser(userId);
    if (!user) throw new NotFoundError('User', userId);
    
    if (user.status !== 'active') {
      throw new BusinessRuleError('Cannot create order for inactive user', 'active_user_required');
    }
    
    // Create order
    const order = await orderService.create(userId, items);
    
    logger.info('order_created', { orderId: order.id, userId, requestId: req.id });
    
    res.status(201).json({ order });
    
  } catch (error) {
    next(error); // Pass to error handler middleware
  }
});

// Error handler middleware
app.use((err, req, res, next) => {
  const requestId = req.id;
  
  // Known application error
  if (err instanceof AppError) {
    logger.log(
      err.http_status >= 500 ? 'error' : 'info',
      'request_error',
      {
        code: err.code,
        message: err.message,
        status: err.http_status,
        requestId,
        userId: req.userId,
        path: req.path
      }
    );
    
    return res.status(err.http_status).json({
      error: {
        code: err.code,
        message: err.message,
        request_id: requestId,
        timestamp: new Date().toISOString(),
        ...err.details
      }
    });
  }
  
  // Unexpected error (bug)
  logger.error('unhandled_error', {
    message: err.message,
    stack: err.stack,
    requestId,
    userId: req.userId,
    path: req.path
  });
  
  // Don't expose internal errors to users
  res.status(500).json({
    error: {
      code: 'INTERNAL_SERVER_ERROR',
      message: 'An unexpected error occurred',
      request_id: requestId,
      timestamp: new Date().toISOString()
    }
  });
});
```

### Database Operations
```python
def get_user(user_id):
    try:
        user = db.query(User).filter(User.id == user_id).one()
        return user
    except NoResultFound:
        raise NotFoundError("User", user_id)
    except OperationalError as e:
        # Database connection failed
        raise DatabaseError("query", str(e))
    except Exception as e:
        # Unexpected error
        logger.critical("unexpected_db_error", user_id=user_id, error=str(e))
        raise
```

### External API Calls
```python
def charge_payment(amount, token):
    try:
        response = requests.post(
            'https://api.stripe.com/charges',
            json={'amount': amount, 'token': token},
            timeout=10  # Always set timeout
        )
        response.raise_for_status()
        return response.json()
        
    except requests.Timeout:
        logger.error("stripe_timeout", amount=amount)
        raise ExternalServiceError("Stripe", "Request timed out")
        
    except requests.HTTPError as e:
        if e.response.status_code == 402:
            raise BusinessRuleError("Insufficient funds", "payment_declined")
        logger.error("stripe_error", status=e.response.status_code, body=e.response.text)
        raise ExternalServiceError("Stripe", f"HTTP {e.response.status_code}")
        
    except requests.RequestException as e:
        logger.error("stripe_network_error", error=str(e))
        raise ExternalServiceError("Stripe", "Network error")
```

---

## User-Facing Messages

### Technical Error → User-Friendly

| Error Code | Internal Message | User Message |
|-----------|------------------|--------------|
| DATABASE_ERROR | "Connection pool exhausted" | "We're experiencing high traffic. Please try again." |
| EXTERNAL_SERVICE_ERROR | "Stripe API returned 500" | "Payment processing is temporarily unavailable." |
| TIMEOUT_ERROR | "Query exceeded 30s limit" | "This request is taking longer than usual. Please try again." |
| VALIDATION_ERROR | "Email regex failed" | "Please enter a valid email address." |

### Implementation
```python
USER_FRIENDLY_MESSAGES = {
    "DATABASE_ERROR": "We're experiencing technical difficulties. Please try again shortly.",
    "EXTERNAL_SERVICE_ERROR": "A third-party service is unavailable. Please try again later.",
    "TIMEOUT_ERROR": "Your request is taking too long. Please try a simpler search.",
}

def format_user_message(error):
    if error.code in USER_FRIENDLY_MESSAGES:
        return USER_FRIENDLY_MESSAGES[error.code]
    return error.message  # Show technical message for client errors
```

---

## Monitoring & Alerting

### Error Rate Metrics
```
error_rate = (5xx_responses / total_responses) * 100
```

**Alert if:** error_rate > 1% for 5 minutes

### Error Type Tracking
```
error_count{code="DATABASE_ERROR"} — Count of each error type
error_count{code="EXTERNAL_SERVICE_ERROR"}
```

**Alert if:** Any error type > 100 occurrences in 10 minutes

### Example Prometheus Query
```promql
rate(http_requests_total{status=~"5.."}[5m]) > 0.01
```

---

## Testing Error Handling

### Unit Tests
```python
def test_user_not_found():
    with pytest.raises(NotFoundError) as exc_info:
        get_user("nonexistent_id")
    
    assert exc_info.value.code == "RESOURCE_NOT_FOUND"
    assert exc_info.value.http_status == 404
```

### Integration Tests
```python
def test_database_connection_failure(monkeypatch):
    # Simulate database down
    monkeypatch.setattr(db, 'query', lambda: raise_operational_error())
    
    response = client.get('/users/123')
    assert response.status_code == 500
    assert response.json()['error']['code'] == 'DATABASE_ERROR'
```

### Chaos Engineering
- Randomly inject database failures in staging
- Test circuit breakers and fallbacks
- Verify error logging and alerts fire correctly

## Rules

- Every error must have a unique code (SCREAMING_SNAKE_CASE).
- 500 errors must never expose stack traces or internal details to users.
- All errors must be logged with request_id for correlation.
- Client errors (4xx) are INFO level, server errors (5xx) are ERROR level.
- Database errors, external API failures, and timeouts must be retryable with exponential backoff.
- Never log sensitive data (passwords, tokens, SSNs) even in error messages.
- Error responses must be consistent JSON format across all endpoints.
- Every HTTP status code must have a specific error code (not just "400 Bad Request").
- User-facing error messages must be actionable ("Check email format") not vague ("Invalid input").
- If an error occurs more than 10 times in production, create a new error type for it.
