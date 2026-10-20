---
name: "API Integration Layer"
version: "1.0.0"
description: "Builds robust API clients with retry logic, caching, error handling, and request/response transformation."
author: "workspace"
activated: false
---

# API Integration Layer

Builds robust, resilient API integrations with retry, caching, and transformation.

## Decision Framework

### When to Apply
Use when:
- Integrating with external REST/GraphQL APIs
- Building webhook handlers
- Creating API client libraries
- Need retry/circuit breaker patterns

### When NOT to Apply
Don't use when:
- Simple single-endpoint calls with no error handling needed
- Internal function calls within same service
- Real-time streaming (use WebSocket skill instead)

## Anti-Patterns

### 1. No Timeout
```javascript
// BAD: Hangs forever if server doesn't respond
const response = await fetch(url);

// GOOD: Timeout with abort
const controller = new AbortController();
setTimeout(() => controller.abort(), 10000);
const response = await fetch(url, { signal: controller.signal });
```

### 2. Swallowing Errors
```javascript
// BAD: Silent failure
try { await api.call(); } catch (e) { }

// GOOD: Handle or propagate
try { await api.call(); } catch (e) {
  logger.error('API call failed', { error: e.message, endpoint: url });
  throw new ApiError(e.message, { cause: e, endpoint: url });
}
```

### 3. Hardcoded URLs
```javascript
// BAD
const API = 'https://api.example.com/v1';

// GOOD
const API = process.env.API_BASE_URL || 'https://api.example.com/v1';
```


## Trigger Phrases

- "Connect to API"
- "API client"
- "REST integration"
- "GraphQL client"
- "Webhook handler"
- "API error handling"

## Patterns

### Resilient Client
```javascript
class ApiClient {
  constructor(config) {
    this.baseUrl = config.baseUrl;
    this.timeout = config.timeout || 10000;
    this.retries = config.retries || 3;
    this.retryDelay = config.retryDelay || 1000;
  }

  async request(method, path, options = {}) {
    let lastError;
    for (let i = 0; i <= this.retries; i++) {
      try {
        const response = await this._execute(method, path, options);
        return this._transform(response, options.transform);
      } catch (error) {
        lastError = error;
        if (!this._isRetryable(error) || i === this.retries) throw error;
        await this._delay(this.retryDelay * Math.pow(2, i));
      }
    }
    throw lastError;
  }

  _isRetryable(error) {
    return error.status >= 500 || error.code === 'ECONNRESET' || error.code === 'ETIMEDOUT';
  }
}
```

### Response Transformer
```javascript
const transformSnakeToCamel = (obj) => {
  if (Array.isArray(obj)) return obj.map(transformSnakeToCamel);
  if (obj !== null && typeof obj === 'object') {
    return Object.fromEntries(
      Object.entries(obj).map(([k, v]) => [
        k.replace(/_([a-z])/g, (_, c) => c.toUpperCase()),
        transformSnakeToCamel(v)
      ])
    );
  }
  return obj;
};
```

## Integration
- Works with: error-recovery-orchestrator, performance-budget-enforcer
- Feeds into: notification-system-builder (on failures)
