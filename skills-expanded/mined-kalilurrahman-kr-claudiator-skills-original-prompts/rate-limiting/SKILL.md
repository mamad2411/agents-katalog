---
name: rate-limiting
description: Design rate limiting to prevent abuse and ensure fair usage. Outputs algorithms (token bucket, sliding window), storage strategies, and bypass rules.
argument-hint: [API type, traffic patterns, abuse scenarios]
allowed-tools: Read, Write, Bash
---

# Rate Limiting Strategy

Design production-grade rate limiting that prevents abuse while allowing legitimate traffic. Not just "limit to 100/hour" — algorithm selection, distributed counting, user tiers, bypass rules, and monitoring.

## Process

1. **Identify resources to protect.** APIs, logins, file uploads, expensive operations.
2. **Choose algorithm.** Token bucket (burst), sliding window (precise), fixed window (simple).
3. **Define limits.** Per-user, per-IP, per-endpoint, global limits.
4. **Select storage.** Redis for distributed, in-memory for single server.
5. **Handle exceeded limits.** 429 response, retry-after header, exponential backoff.
6. **Add bypass rules.** Whitelist IPs, premium users, internal services.
7. **Monitor.** Rate limit hits, abuse attempts, false positives.

## Output Format

### Rate Limiting Configuration: [API Name]

**Algorithm:** Token Bucket  
**Storage:** Redis Cluster  
**Default Limit:** 1000 requests/hour per user  
**Burst:** 100 requests/minute  
**Bypass:** Internal IPs, Premium tier

---

## Algorithm Comparison

| Algorithm | Precision | Memory | Burst Allowed | Best For |
|-----------|-----------|--------|---------------|----------|
| Fixed Window | Low | O(1) | Yes (at window start) | Simple APIs |
| Sliding Window | High | O(n) | No | Strict enforcement |
| Token Bucket | Medium | O(1) | Yes (controlled) | Most APIs |
| Leaky Bucket | High | O(1) | No | Smooth traffic |

### Token Bucket (Recommended)

**How it works:**
- Bucket holds tokens (max capacity = burst size)
- Tokens added at fixed rate (refill rate)
- Each request consumes 1 token
- If no tokens → reject

**Example:**
```python
import time
import redis

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity  # Max tokens
        self.refill_rate = refill_rate  # Tokens per second
        self.redis = redis.Redis()
    
    def allow_request(self, user_id: str) -> bool:
        key = f"rate_limit:{user_id}"
        
        # Get current state
        data = self.redis.get(key)
        if data:
            tokens, last_update = map(float, data.decode().split(','))
        else:
            tokens = self.capacity
            last_update = time.time()
        
        # Refill tokens
        now = time.time()
        elapsed = now - last_update
        tokens = min(self.capacity, tokens + elapsed * self.refill_rate)
        
        # Check if request allowed
        if tokens >= 1:
            tokens -= 1
            self.redis.setex(key, 3600, f"{tokens},{now}")
            return True
        else:
            self.redis.setex(key, 3600, f"{tokens},{now}")
            return False

# Usage
limiter = TokenBucket(capacity=100, refill_rate=1000/3600)  # 100 burst, 1000/hour
if limiter.allow_request("user_123"):
    # Process request
else:
    # Return 429 Too Many Requests
```

**Pros:** Allows bursts, smooth over time  
**Cons:** Slightly complex

---

### Sliding Window Log

**How it works:**
- Store timestamp of each request in sorted set
- Remove entries older than window
- Count remaining entries
- If count < limit → allow

**Redis Implementation:**
```python
import time
import redis

class SlidingWindowLog:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self.redis = redis.Redis()
    
    def allow_request(self, user_id: str) -> bool:
        key = f"rate_limit:{user_id}"
        now = time.time()
        window_start = now - self.window
        
        # Remove old entries
        self.redis.zremrangebyscore(key, 0, window_start)
        
        # Count current requests
        count = self.redis.zcard(key)
        
        if count < self.limit:
            # Add current request
            self.redis.zadd(key, {now: now})
            self.redis.expire(key, self.window)
            return True
        else:
            return False

# Usage: 100 requests per 60 seconds
limiter = SlidingWindowLog(limit=100, window_seconds=60)
```

**Pros:** Precise, no edge cases  
**Cons:** High memory (stores each request)

---

### Fixed Window Counter

**How it works:**
- Time divided into fixed windows (e.g., 1 hour)
- Counter per window
- Reset counter at window boundary

**Implementation:**
```python
import time
import redis

class FixedWindowCounter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self.redis = redis.Redis()
    
    def allow_request(self, user_id: str) -> bool:
        now = time.time()
        window_key = int(now // self.window)
        key = f"rate_limit:{user_id}:{window_key}"
        
        count = self.redis.incr(key)
        self.redis.expire(key, self.window * 2)
        
        return count <= self.limit

# Usage
limiter = FixedWindowCounter(limit=1000, window_seconds=3600)
```

**Pros:** Simple, low memory  
**Cons:** Burst at window edges (2x limit in 2 seconds)

---

## Multi-Tier Rate Limits

```python
RATE_LIMITS = {
    'free': {
        'requests_per_hour': 100,
        'burst': 10,
    },
    'basic': {
        'requests_per_hour': 1000,
        'burst': 50,
    },
    'premium': {
        'requests_per_hour': 10000,
        'burst': 200,
    },
    'internal': {
        'requests_per_hour': float('inf'),
        'burst': float('inf'),
    }
}

def get_user_tier(user_id: str) -> str:
    user = db.get_user(user_id)
    return user.subscription_tier

def check_rate_limit(user_id: str) -> bool:
    tier = get_user_tier(user_id)
    limits = RATE_LIMITS[tier]
    
    limiter = TokenBucket(
        capacity=limits['burst'],
        refill_rate=limits['requests_per_hour'] / 3600
    )
    
    return limiter.allow_request(user_id)
```

---

## API Middleware (Express.js)

```javascript
const redis = require('redis');
const client = redis.createClient();

const rateLimiter = (options = {}) => {
  const limit = options.limit || 100;
  const window = options.window || 3600;
  
  return async (req, res, next) => {
    const userId = req.user?.id || req.ip;
    const key = `rate_limit:${userId}`;
    
    try {
      const count = await client.incr(key);
      
      if (count === 1) {
        await client.expire(key, window);
      }
      
      // Set headers
      res.set('X-RateLimit-Limit', limit);
      res.set('X-RateLimit-Remaining', Math.max(0, limit - count));
      res.set('X-RateLimit-Reset', Date.now() + window * 1000);
      
      if (count > limit) {
        res.set('Retry-After', window);
        return res.status(429).json({
          error: 'Too Many Requests',
          message: `Rate limit exceeded. Try again in ${window} seconds.`,
          limit: limit,
          window: window
        });
      }
      
      next();
    } catch (err) {
      // Fail open: Allow request if Redis down
      console.error('Rate limiter error:', err);
      next();
    }
  };
};

// Usage
app.use('/api/', rateLimiter({ limit: 1000, window: 3600 }));
app.use('/api/login', rateLimiter({ limit: 5, window: 900 }));
```

---

## Distributed Rate Limiting (Redis)

```python
import redis
from redis.lock import Lock

class DistributedRateLimiter:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
    
    def check_limit(self, key: str, limit: int, window: int) -> tuple[bool, dict]:
        """
        Check rate limit using sliding window.
        Returns (allowed, metadata)
        """
        now = time.time()
        window_start = now - window
        
        # Lua script for atomic operation
        script = """
        local key = KEYS[1]
        local now = tonumber(ARGV[1])
        local window_start = tonumber(ARGV[2])
        local limit = tonumber(ARGV[3])
        
        redis.call('ZREMRANGEBYSCORE', key, 0, window_start)
        local count = redis.call('ZCARD', key)
        
        if count < limit then
            redis.call('ZADD', key, now, now)
            redis.call('EXPIRE', key, ARGV[4])
            return {1, count + 1}
        else
            return {0, count}
        end
        """
        
        allowed, count = self.redis.eval(
            script, 1, key, now, window_start, limit, window
        )
        
        return bool(allowed), {
            'limit': limit,
            'remaining': max(0, limit - count),
            'reset': int(now + window)
        }
```

---

## Per-Endpoint Limits

```python
ENDPOINT_LIMITS = {
    'GET /api/users': (1000, 3600),        # 1000/hour
    'POST /api/users': (10, 3600),         # 10/hour
    'POST /api/login': (5, 900),           # 5 per 15 min
    'POST /api/upload': (20, 86400),       # 20/day
    'GET /api/expensive': (10, 60),        # 10/minute
}

def get_endpoint_key(request):
    return f"{request.method} {request.path}"

@app.before_request
def check_rate_limit():
    endpoint = get_endpoint_key(request)
    
    if endpoint in ENDPOINT_LIMITS:
        limit, window = ENDPOINT_LIMITS[endpoint]
        user_id = request.user.id if request.user else request.remote_addr
        
        allowed, metadata = limiter.check_limit(
            f"rate_limit:{endpoint}:{user_id}",
            limit,
            window
        )
        
        if not allowed:
            return jsonify({
                'error': 'Rate limit exceeded',
                'retry_after': metadata['reset'] - time.time()
            }), 429
```

---

## Bypass Rules

```python
BYPASS_IPS = [
    '10.0.0.0/8',      # Internal network
    '172.16.0.0/12',   # Private network
]

BYPASS_USERS = [
    'admin_user_id',
    'monitoring_bot',
]

def should_bypass_rate_limit(user_id: str, ip: str) -> bool:
    # Check user whitelist
    if user_id in BYPASS_USERS:
        return True
    
    # Check IP whitelist
    import ipaddress
    user_ip = ipaddress.ip_address(ip)
    for cidr in BYPASS_IPS:
        if user_ip in ipaddress.ip_network(cidr):
            return True
    
    # Check premium tier
    user = db.get_user(user_id)
    if user.tier == 'enterprise':
        return True
    
    return False
```

---

## Response Headers

```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640000000
Retry-After: 3600
Content-Type: application/json

{
  "error": "rate_limit_exceeded",
  "message": "You have exceeded the rate limit of 100 requests per hour",
  "limit": 100,
  "remaining": 0,
  "reset": 1640000000
}
```

---

## Monitoring

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram

rate_limit_exceeded = Counter(
    'rate_limit_exceeded_total',
    'Total rate limit violations',
    ['endpoint', 'tier']
)

rate_limit_remaining = Histogram(
    'rate_limit_remaining',
    'Remaining rate limit capacity',
    ['endpoint']
)

def track_rate_limit(endpoint, tier, remaining):
    if remaining == 0:
        rate_limit_exceeded.labels(endpoint=endpoint, tier=tier).inc()
    
    rate_limit_remaining.labels(endpoint=endpoint).observe(remaining)
```

**Alerts:**
- Rate limit hit rate > 10% → Users hitting limits frequently
- Specific IP exceeds limit 100x → Potential attack

---

## Cost-Based Rate Limiting

```python
OPERATION_COSTS = {
    'GET /api/users/:id': 1,
    'GET /api/search': 5,        # Expensive query
    'POST /api/generate-report': 100,  # Very expensive
}

class CostBasedLimiter:
    def __init__(self, budget: int, window: int):
        self.budget = budget
        self.window = window
    
    def check_limit(self, user_id: str, operation: str) -> bool:
        cost = OPERATION_COSTS.get(operation, 1)
        key = f"cost_limit:{user_id}"
        
        spent = self.redis.get(key) or 0
        spent = int(spent)
        
        if spent + cost <= self.budget:
            self.redis.incrby(key, cost)
            self.redis.expire(key, self.window)
            return True
        else:
            return False

# User has 1000 points per hour
# Simple GET = 1 point, expensive search = 5 points
```

---

## Testing

```python
import pytest
import time

def test_rate_limiter_allows_within_limit():
    limiter = TokenBucket(capacity=10, refill_rate=10/60)
    
    for _ in range(10):
        assert limiter.allow_request("user_1") == True
    
    # 11th request should be denied
    assert limiter.allow_request("user_1") == False

def test_rate_limiter_refills():
    limiter = TokenBucket(capacity=5, refill_rate=5)  # 5 per second
    
    # Use all tokens
    for _ in range(5):
        assert limiter.allow_request("user_1") == True
    
    # Wait 1 second for refill
    time.sleep(1)
    
    # Should have ~5 tokens again
    for _ in range(5):
        assert limiter.allow_request("user_1") == True

def test_distributed_limiter():
    limiter = DistributedRateLimiter('redis://localhost')
    
    # Simulate 100 concurrent requests
    from concurrent.futures import ThreadPoolExecutor
    
    def make_request():
        return limiter.check_limit('user_1', limit=50, window=60)
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda _: make_request(), range(100)))
    
    # Exactly 50 should be allowed
    allowed = sum(1 for allowed, _ in results if allowed)
    assert allowed == 50
```

## Rules

- Rate limiting must be per-user (authenticated) or per-IP (anonymous), never global.
- 429 responses must include Retry-After header and X-RateLimit-* headers.
- Critical endpoints (login, password reset) need stricter limits: 5 attempts per 15 minutes.
- Rate limiter must fail open (allow requests) if Redis/storage is down — availability over strict enforcement.
- Token bucket algorithm recommended for most cases — allows bursts while enforcing long-term limits.
- Distributed systems must use atomic operations (Lua scripts in Redis) to prevent race conditions.
- Premium/paid users must have higher limits than free tier.
- Internal service-to-service calls should bypass rate limiting via IP whitelist.
- Monitor rate limit hit rate — > 10% means limits too strict or abuse attempt.
- Cost-based limiting (point system) recommended for APIs with varying operation costs.
