---
name: rate-limiting-design
description: "Design and implement rate limiting strategies to protect APIs and services from abuse while maintaining quality of service."
category: architecture
tags: [rate-limiting, throttle, api, security, performance]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Rate Limiting Designer

## Purpose
Protect APIs and services from abuse, ensure fair usage, and maintain system stability under high load.

## Rate Limiting Algorithms

### Fixed Window
```
Simplest: Count requests per time window
Problem: Allows 2x burst at window boundary

Window: 10 requests per minute
Key: user:123:2026-07-10-10:30
```

### Sliding Window (Recommended)
```python
def check_rate_limit(user_id: str, limit: int, window: int) -> bool:
    now = time.time()
    window_start = now - window
    key = f"ratelimit:{user_id}"
    
    # Remove expired entries
    redis.zremrangebyscore(key, '-inf', window_start)
    
    # Count in current window
    count = redis.zcard(key)
    if count >= limit:
        return False
    
    # Add current request
    redis.zadd(key, {str(now): now})
    redis.expire(key, window)
    return True
```

### Token Bucket
```
Best for: Allowing bursts up to bucket capacity
Bucket: 100 tokens, refill 10/second
Each request: costs 1 token
Burst allowed: up to 100 requests instantly
```

## Response Headers
```
X-RateLimit-Limit: 100        # Limit per window
X-RateLimit-Remaining: 45     # Requests remaining
X-RateLimit-Reset: 1625000000 # Unix timestamp of window reset
Retry-After: 60               # Seconds until retry allowed (429 only)
```

## Tiered Rate Limits
```
Anonymous: 20 requests/minute
Free tier: 100 requests/minute
Pro tier: 1000 requests/minute
Enterprise: Custom
```

## Outputs
1. Rate limiting middleware implementation
2. Per-endpoint limit configuration
3. Response header standards
4. Bypass allowlist for internal services
5. Monitoring and alerting for rate limit events
