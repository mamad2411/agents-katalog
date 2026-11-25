---
name: graceful-degradation
description: Design systems that continue operating with reduced functionality when components fail. Outputs fallback strategies, partial failure handling, feature toggles, and user-facing degraded-mode experiences.
argument-hint: [system name, critical vs non-critical features, acceptable degradation levels]
allowed-tools: Read, Write, Bash
---

# Graceful Degradation

Design fallback mechanisms that keep your system functional when dependencies fail, traffic spikes, or services become unavailable. The goal: users get *something* rather than nothing.

## Process

1. **Classify features by criticality.** Core (must work), important (degrade gracefully), nice-to-have (can silently drop).
2. **Map dependencies.** For each feature, list external calls, databases, caches, queues.
3. **Define failure modes.** Timeout, error response, partial data, stale data.
4. **Design fallbacks.** Cached response, default value, simplified version, queue-and-retry.
5. **Set thresholds.** When does degradation activate? Error rate, latency P99, circuit breaker state.
6. **Plan user communication.** Silent fallback vs. banner vs. error message.
7. **Test degraded paths.** Chaos engineering, kill switches, dependency mocks.
8. **Monitor degraded state.** Alert when in degradation, track duration and frequency.

## Output Format

### Degradation Matrix

| Feature | Dependency | Failure Mode | Fallback | User Impact |
|---------|-----------|--------------|----------|-------------|
| Product search | Elasticsearch | Timeout | Return cached results (5 min TTL) | Slightly stale results |
| Recommendations | ML service | Error | Show bestsellers list | Generic recommendations |
| User profile | Auth service | Unavailable | Read-only session cache | Can't update profile |
| Payment | Stripe API | Timeout | Queue for async processing | Delayed confirmation |
| Images | CDN | 5xx | Serve placeholder + retry | Broken image replaced |

### Fallback Implementation

#### Pattern 1: Stale Cache Fallback
```python
import redis
from functools import wraps
import time

class GracefulCache:
    def __init__(self, redis_client, stale_ttl=300):
        self.redis = redis_client
        self.stale_ttl = stale_ttl  # How long stale data is acceptable
    
    def with_fallback(self, key: str, ttl: int = 60):
        """Decorator: serve stale cache when source fails."""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Try live data
                try:
                    result = await func(*args, **kwargs)
                    # Store with timestamp for staleness check
                    self.redis.setex(
                        key,
                        ttl + self.stale_ttl,
                        json.dumps({"data": result, "ts": time.time(), "fresh": True})
                    )
                    return result
                except Exception as e:
                    # Fetch stale cache
                    cached = self.redis.get(key)
                    if cached:
                        entry = json.loads(cached)
                        age = time.time() - entry["ts"]
                        if age < self.stale_ttl:
                            logger.warning(f"Serving stale cache for {key}, age={age:.0f}s, error={e}")
                            return entry["data"]
                    # No stale data — raise or return default
                    raise
            return wrapper
        return decorator

cache = GracefulCache(redis_client)

@cache.with_fallback("product:search:popular", ttl=60)
async def get_popular_products():
    return await elasticsearch.search(index="products", body={"query": ...})
```

#### Pattern 2: Circuit Breaker with Fallback
```python
from enum import Enum
import asyncio
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"       # Normal operation
    OPEN = "open"           # Failing — reject calls
    HALF_OPEN = "half_open" # Testing recovery

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        half_open_attempts: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_attempts = half_open_attempts
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_successes = 0

    async def call(self, func, *args, fallback=None, **kwargs):
        if self.state == CircuitState.OPEN:
            elapsed = (datetime.now() - self.last_failure_time).seconds
            if elapsed > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_successes = 0
            else:
                if fallback:
                    return await fallback(*args, **kwargs)
                raise CircuitOpenError(f"Circuit open, retry after {self.recovery_timeout - elapsed}s")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            if fallback:
                return await fallback(*args, **kwargs)
            raise

    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.half_open_successes += 1
            if self.half_open_successes >= self.half_open_attempts:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
        elif self.state == CircuitState.CLOSED:
            self.failure_count = max(0, self.failure_count - 1)

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
ml_circuit = CircuitBreaker(failure_threshold=3, recovery_timeout=30)

async def get_recommendations(user_id: str):
    async def fallback(user_id):
        return await get_bestsellers()  # Simplified fallback
    
    return await ml_circuit.call(
        ml_service.get_personalized,
        user_id,
        fallback=fallback
    )
```

#### Pattern 3: Feature Flag Degradation
```python
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class FeatureFlag:
    name: str
    enabled: bool
    degraded: bool = False  # Running in degraded mode
    degraded_reason: Optional[str] = None

class FeatureManager:
    def __init__(self):
        self._flags: dict[str, FeatureFlag] = {}
    
    def register(self, name: str, enabled: bool = True):
        self._flags[name] = FeatureFlag(name=name, enabled=enabled)
    
    def degrade(self, name: str, reason: str):
        """Mark feature as degraded — still runs but with fallback."""
        if name in self._flags:
            self._flags[name].degraded = True
            self._flags[name].degraded_reason = reason
            logger.warning(f"Feature {name} degraded: {reason}")
    
    def disable(self, name: str, reason: str):
        """Fully disable a feature."""
        if name in self._flags:
            self._flags[name].enabled = False
            logger.error(f"Feature {name} disabled: {reason}")
    
    def is_enabled(self, name: str) -> bool:
        flag = self._flags.get(name)
        return flag.enabled if flag else False
    
    def is_degraded(self, name: str) -> bool:
        flag = self._flags.get(name)
        return flag.degraded if flag else False

features = FeatureManager()
features.register("real_time_pricing", enabled=True)
features.register("personalized_search", enabled=True)
features.register("live_inventory", enabled=True)

# At runtime when dependency fails:
async def handle_pricing_service_outage():
    features.degrade("real_time_pricing", "Pricing service latency >2s, using cached prices")

async def get_product_price(product_id: str) -> dict:
    if not features.is_enabled("real_time_pricing"):
        return {"price": get_catalog_price(product_id), "source": "catalog", "live": False}
    
    if features.is_degraded("real_time_pricing"):
        cached = await cache.get(f"price:{product_id}")
        if cached:
            return {**cached, "source": "cache", "live": False, "cached_at": cached["ts"]}
    
    # Normal path
    return await pricing_service.get_price(product_id)
```

#### Pattern 4: Retry with Exponential Backoff
```python
import asyncio
import random
from typing import TypeVar, Callable, Awaitable

T = TypeVar("T")

async def retry_with_backoff(
    func: Callable[..., Awaitable[T]],
    *args,
    max_attempts: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 30.0,
    jitter: bool = True,
    retryable_exceptions: tuple = (ConnectionError, TimeoutError),
    **kwargs
) -> T:
    last_exception = None
    
    for attempt in range(max_attempts):
        try:
            return await func(*args, **kwargs)
        except retryable_exceptions as e:
            last_exception = e
            if attempt == max_attempts - 1:
                break
            
            delay = min(base_delay * (2 ** attempt), max_delay)
            if jitter:
                delay *= (0.5 + random.random())  # ±50% jitter
            
            logger.warning(
                f"Attempt {attempt + 1}/{max_attempts} failed: {e}. "
                f"Retrying in {delay:.2f}s"
            )
            await asyncio.sleep(delay)
    
    raise last_exception
```

#### Pattern 5: Bulkhead Isolation
```python
import asyncio
from asyncio import Semaphore

class Bulkhead:
    """Isolate failures with resource pools per service."""
    
    def __init__(self, max_concurrent: int = 10, timeout: float = 5.0):
        self._semaphore = Semaphore(max_concurrent)
        self.timeout = timeout
        self.rejected_count = 0
    
    async def execute(self, func, *args, **kwargs):
        try:
            async with asyncio.timeout(0.1):  # Don't wait long for slot
                await self._semaphore.acquire()
        except asyncio.TimeoutError:
            self.rejected_count += 1
            metrics.increment("bulkhead.rejected", tags={"func": func.__name__})
            raise BulkheadFullError(f"Bulkhead full ({self._semaphore._value} slots)")
        
        try:
            async with asyncio.timeout(self.timeout):
                return await func(*args, **kwargs)
        finally:
            self._semaphore.release()

# Separate pools prevent one slow service from starving others
payment_bulkhead = Bulkhead(max_concurrent=20, timeout=10.0)
inventory_bulkhead = Bulkhead(max_concurrent=50, timeout=2.0)
recommendation_bulkhead = Bulkhead(max_concurrent=30, timeout=1.0)
```

### User Communication Strategy

```python
from enum import Enum

class DegradationLevel(Enum):
    NONE = "none"           # Fully operational
    MINOR = "minor"         # Slight impact, no user message
    MODERATE = "moderate"   # Visible impact, banner message
    SEVERE = "severe"       # Major impact, prominent warning
    CRITICAL = "critical"   # Core functionality broken, error page

def get_user_message(level: DegradationLevel, feature: str) -> dict | None:
    messages = {
        DegradationLevel.MINOR: None,  # Silent
        DegradationLevel.MODERATE: {
            "type": "info",
            "message": f"Some {feature} may show slightly outdated information.",
            "dismissible": True
        },
        DegradationLevel.SEVERE: {
            "type": "warning",
            "message": f"{feature} is experiencing issues. We're working on it.",
            "dismissible": False,
            "action": "Check status page"
        },
        DegradationLevel.CRITICAL: {
            "type": "error",
            "message": f"{feature} is temporarily unavailable.",
            "dismissible": False,
            "action": "Try again later"
        }
    }
    return messages.get(level)
```

### Health Check with Degradation Status

```python
from fastapi import FastAPI
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str  # healthy | degraded | unhealthy
    version: str
    checks: dict[str, dict]

app = FastAPI()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    checks = {}
    overall = "healthy"
    
    # Database
    try:
        await db.execute("SELECT 1")
        checks["database"] = {"status": "ok", "latency_ms": db.last_latency_ms}
    except Exception as e:
        checks["database"] = {"status": "error", "error": str(e)}
        overall = "unhealthy"
    
    # Cache
    try:
        await cache.ping()
        checks["cache"] = {"status": "ok"}
    except Exception as e:
        checks["cache"] = {"status": "degraded", "fallback": "in-memory"}
        if overall == "healthy":
            overall = "degraded"
    
    # ML Service
    try:
        await ml_service.health()
        checks["ml_service"] = {"status": "ok"}
    except Exception as e:
        checks["ml_service"] = {"status": "degraded", "fallback": "bestsellers"}
        if overall == "healthy":
            overall = "degraded"
    
    return HealthResponse(
        status=overall,
        version=settings.VERSION,
        checks=checks
    )
```

## Monitoring & Alerting

```yaml
# Prometheus alerting rules
groups:
  - name: degradation
    rules:
      - alert: ServiceDegraded
        expr: degradation_active{severity="moderate"} == 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.service }} is in degraded mode"
          
      - alert: DegradationDurationHigh
        expr: time() - degradation_start_timestamp > 1800
        labels:
          severity: critical
        annotations:
          summary: "Degradation active for >30 minutes on {{ $labels.service }}"
          
      - alert: FallbackRateHigh
        expr: rate(fallback_used_total[5m]) / rate(requests_total[5m]) > 0.1
        labels:
          severity: warning
        annotations:
          summary: "Fallback rate >10% on {{ $labels.service }}"
```

## Testing Degraded Paths

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_recommendation_falls_back_to_bestsellers():
    with patch("services.ml_service.get_personalized", side_effect=TimeoutError):
        result = await get_recommendations(user_id="user-123")
        assert result["source"] == "bestsellers"
        assert len(result["items"]) > 0

@pytest.mark.asyncio
async def test_circuit_breaker_opens_after_threshold():
    breaker = CircuitBreaker(failure_threshold=3)
    
    for _ in range(3):
        with pytest.raises(Exception):
            await breaker.call(AsyncMock(side_effect=ConnectionError))
    
    assert breaker.state == CircuitState.OPEN

@pytest.mark.asyncio
async def test_stale_cache_served_when_source_fails():
    # Pre-warm cache
    await cache.set("product:search:popular", {"items": ["item1"]}, ex=300)
    
    with patch("services.elasticsearch.search", side_effect=ConnectionError):
        result = await get_popular_products()
        assert result["items"] == ["item1"]
```

## Rules

- **Every external call needs a fallback** — timeout, error, or unavailable must return *something*.
- **Classify before you code** — know which features can degrade vs. must stay up.
- **Never degrade silently for critical paths** — payment, auth, data writes must fail loudly.
- **Use stale data over errors** — a 5-minute-old price beats a 500 error page.
- **Set meaningful timeouts** — 30s timeout is not a fallback, it's a broken user experience.
- **Test the fallback path** — if it's not tested, it's broken.
- **Monitor degradation duration** — alert when degraded state exceeds SLA.
- **Degrade incrementally** — reduce quality step by step, not all-or-nothing.
- **Never cascade degradation** — isolate with bulkheads; one failure shouldn't sink everything.
- **Document degraded UX** — product team must sign off on what users see in each fallback.
