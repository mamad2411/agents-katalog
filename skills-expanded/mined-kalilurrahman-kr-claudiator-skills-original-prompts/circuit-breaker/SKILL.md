---
name: circuit-breaker
description: Circuit breaker pattern for handling service failures gracefully. Outputs states (closed/open/half-open), thresholds, fallback strategies, and monitoring.
argument-hint: [service dependencies, failure tolerance, recovery time]
allowed-tools: Read, Write, Bash
---

# Circuit Breaker Pattern

Design circuit breakers that prevent cascading failures when downstream services fail. Not just retry logic — state management, failure thresholds, half-open testing, fallback responses.

## Process

1. **Identify protected services.** External APIs, databases, microservices.
2. **Define states.** Closed (normal), Open (failing), Half-Open (testing recovery).
3. **Set thresholds.** Failure rate (%), consecutive failures, timeout duration.
4. **Configure timeouts.** Request timeout, open state duration, half-open test count.
5. **Design fallbacks.** Cached data, default values, degraded mode.
6. **Add monitoring.** State changes, failure rates, recovery time.

## Output Format

### Circuit Breaker Config: [Service Name]

**Protected Service:** Payment API  
**Failure Threshold:** 50% failures in 10 requests  
**Timeout:** 5 seconds  
**Open Duration:** 60 seconds  
**Half-Open Tests:** 3 requests  
**Fallback:** Cached response or 503

---

## States

### CLOSED (Normal Operation)
- All requests pass through
- Failures counted
- Transitions to OPEN if threshold exceeded

### OPEN (Failing, Block Requests)
- Requests fail immediately without calling service
- Return fallback response
- After timeout, transition to HALF-OPEN

### HALF-OPEN (Testing Recovery)
- Allow limited requests through (e.g., 3)
- If all succeed → CLOSED
- If any fail → OPEN

```
CLOSED ──(failures > threshold)──> OPEN
  ↑                                   │
  │                                   │
  └──(tests pass)── HALF-OPEN ←──(timeout)
         │
         └──(test fails)──> OPEN
```

---

## Implementation (Python)

```python
from enum import Enum
import time
from threading import Lock

class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,      # Consecutive failures
        timeout: float = 60.0,            # Open state duration (seconds)
        half_open_max_calls: int = 3     # Requests to test in half-open
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.half_open_max_calls = half_open_max_calls
        
        self.state = State.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0
        
        self.lock = Lock()
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        
        with self.lock:
            if self.state == State.OPEN:
                if time.time() - self.last_failure_time >= self.timeout:
                    # Timeout expired, try half-open
                    self.state = State.HALF_OPEN
                    self.half_open_calls = 0
                else:
                    # Still open, fail fast
                    raise CircuitBreakerError("Circuit breaker is OPEN")
            
            if self.state == State.HALF_OPEN:
                if self.half_open_calls >= self.half_open_max_calls:
                    raise CircuitBreakerError("Half-open test limit reached")
                self.half_open_calls += 1
        
        # Execute function
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        with self.lock:
            if self.state == State.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.half_open_max_calls:
                    # All tests passed, close circuit
                    self.state = State.CLOSED
                    self.failure_count = 0
                    self.success_count = 0
            else:
                # Reset failure count on success
                self.failure_count = 0
    
    def _on_failure(self):
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.state == State.HALF_OPEN or \
               self.failure_count >= self.failure_threshold:
                # Open the circuit
                self.state = State.OPEN
                self.success_count = 0

class CircuitBreakerError(Exception):
    pass

# Usage
breaker = CircuitBreaker(failure_threshold=5, timeout=60)

try:
    result = breaker.call(external_api.get_data, param1, param2)
except CircuitBreakerError:
    # Use fallback
    result = cached_data or default_value
```

---

## Rate-Based Circuit Breaker

```python
from collections import deque
import time

class RateBasedCircuitBreaker:
    """Opens circuit based on failure rate, not count"""
    
    def __init__(
        self,
        failure_rate_threshold: float = 0.5,  # 50%
        window_size: int = 10,                 # Last 10 requests
        min_requests: int = 5                  # Min requests before checking
    ):
        self.failure_rate_threshold = failure_rate_threshold
        self.window_size = window_size
        self.min_requests = min_requests
        
        self.state = State.CLOSED
        self.results = deque(maxlen=window_size)  # True=success, False=failure
        self.last_failure_time = None
        self.timeout = 60
    
    def call(self, func, *args, **kwargs):
        if self.state == State.OPEN:
            if time.time() - self.last_failure_time >= self.timeout:
                self.state = State.HALF_OPEN
            else:
                raise CircuitBreakerError("Circuit OPEN")
        
        try:
            result = func(*args, **kwargs)
            self.results.append(True)  # Success
            
            if self.state == State.HALF_OPEN:
                self.state = State.CLOSED
            
            return result
            
        except Exception as e:
            self.results.append(False)  # Failure
            self.last_failure_time = time.time()
            
            # Check failure rate
            if len(self.results) >= self.min_requests:
                failure_rate = self.results.count(False) / len(self.results)
                if failure_rate >= self.failure_rate_threshold:
                    self.state = State.OPEN
            
            raise

# Usage: Opens if 50% of last 10 requests fail
breaker = RateBasedCircuitBreaker(failure_rate_threshold=0.5, window_size=10)
```

---

## Fallback Strategies

### 1. Cached Response
```python
import redis
cache = redis.Redis()

def get_user_profile(user_id):
    cache_key = f"user:{user_id}"
    
    try:
        # Try with circuit breaker
        profile = breaker.call(user_service.get_profile, user_id)
        
        # Cache on success
        cache.setex(cache_key, 3600, json.dumps(profile))
        return profile
        
    except CircuitBreakerError:
        # Return cached data
        cached = cache.get(cache_key)
        if cached:
            return json.loads(cached)
        raise
```

### 2. Default/Stub Response
```python
DEFAULT_RECOMMENDATIONS = ['popular_item_1', 'popular_item_2']

def get_recommendations(user_id):
    try:
        return breaker.call(ml_service.recommend, user_id)
    except CircuitBreakerError:
        # Return safe defaults
        return DEFAULT_RECOMMENDATIONS
```

### 3. Degraded Functionality
```python
def search_products(query):
    try:
        # Full search with ML ranking
        return breaker.call(advanced_search, query)
    except CircuitBreakerError:
        # Fallback to simple SQL search
        return db.query(Product).filter(
            Product.name.ilike(f"%{query}%")
        ).limit(20).all()
```

---

## Decorator Pattern

```python
from functools import wraps

def circuit_breaker(name: str, **breaker_kwargs):
    """Decorator to protect functions with circuit breaker"""
    breaker = CircuitBreaker(**breaker_kwargs)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return breaker.call(func, *args, **kwargs)
            except CircuitBreakerError:
                # Log and re-raise or handle
                logger.warning(f"Circuit {name} is OPEN")
                raise
        
        wrapper.circuit_breaker = breaker  # Access for monitoring
        return wrapper
    
    return decorator

# Usage
@circuit_breaker('payment_api', failure_threshold=5, timeout=60)
def charge_payment(amount, token):
    return stripe.charge(amount, token)

# Check state
if charge_payment.circuit_breaker.state == State.OPEN:
    return {"error": "Payment service unavailable"}, 503
```

---

## Integration with Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2))
@circuit_breaker('external_api', failure_threshold=5)
def call_external_api(params):
    return requests.get('https://api.example.com', params=params, timeout=5)

# Retry up to 3 times, but circuit breaker can still open if too many failures
```

---

## Monitoring with Prometheus

```python
from prometheus_client import Counter, Gauge, Histogram

circuit_state = Gauge(
    'circuit_breaker_state',
    'Circuit breaker state (0=closed, 1=open, 2=half_open)',
    ['service']
)

circuit_failures = Counter(
    'circuit_breaker_failures_total',
    'Total failures',
    ['service']
)

circuit_state_changes = Counter(
    'circuit_breaker_state_changes_total',
    'State transitions',
    ['service', 'from_state', 'to_state']
)

class MonitoredCircuitBreaker(CircuitBreaker):
    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
    
    def _on_failure(self):
        old_state = self.state
        super()._on_failure()
        
        circuit_failures.labels(service=self.name).inc()
        
        if old_state != self.state:
            circuit_state_changes.labels(
                service=self.name,
                from_state=old_state.value,
                to_state=self.state.value
            ).inc()
        
        circuit_state.labels(service=self.name).set(
            0 if self.state == State.CLOSED else
            1 if self.state == State.OPEN else 2
        )
```

**Alerts:**
```yaml
- alert: CircuitBreakerOpen
  expr: circuit_breaker_state{service="payment_api"} == 1
  for: 1m
  annotations:
    summary: "Payment API circuit breaker is OPEN"
```

---

## Per-User Circuit Breakers

```python
class PerUserCircuitBreaker:
    """Separate circuit breaker per user to isolate issues"""
    
    def __init__(self, **breaker_kwargs):
        self.breakers = {}
        self.breaker_kwargs = breaker_kwargs
    
    def get_breaker(self, user_id: str) -> CircuitBreaker:
        if user_id not in self.breakers:
            self.breakers[user_id] = CircuitBreaker(**self.breaker_kwargs)
        return self.breakers[user_id]
    
    def call(self, user_id: str, func, *args, **kwargs):
        breaker = self.get_breaker(user_id)
        return breaker.call(func, *args, **kwargs)

# Usage
user_breakers = PerUserCircuitBreaker(failure_threshold=3)

def get_user_data(user_id):
    try:
        return user_breakers.call(user_id, external_api.fetch, user_id)
    except CircuitBreakerError:
        return cached_user_data(user_id)
```

---

## Distributed Circuit Breaker (Redis)

```python
import redis
import json

class DistributedCircuitBreaker:
    """Circuit breaker shared across multiple servers"""
    
    def __init__(self, name: str, redis_url: str, **kwargs):
        self.name = name
        self.redis = redis.from_url(redis_url)
        self.local_breaker = CircuitBreaker(**kwargs)
    
    def call(self, func, *args, **kwargs):
        # Check global state in Redis
        state_key = f"circuit:{self.name}:state"
        global_state = self.redis.get(state_key)
        
        if global_state == b'OPEN':
            raise CircuitBreakerError("Global circuit OPEN")
        
        # Execute with local breaker
        try:
            result = self.local_breaker.call(func, *args, **kwargs)
            
            # Update global state on success
            if self.local_breaker.state == State.CLOSED:
                self.redis.set(state_key, 'CLOSED', ex=60)
            
            return result
            
        except Exception as e:
            # Update global state on failure
            if self.local_breaker.state == State.OPEN:
                self.redis.set(state_key, 'OPEN', ex=60)
            raise
```

---

## Testing

```python
def test_circuit_breaker_opens_after_threshold():
    breaker = CircuitBreaker(failure_threshold=3)
    
    def failing_func():
        raise Exception("Service down")
    
    # First 3 failures should pass through
    for _ in range(3):
        with pytest.raises(Exception):
            breaker.call(failing_func)
    
    # 4th call should fail fast
    with pytest.raises(CircuitBreakerError):
        breaker.call(failing_func)
    
    assert breaker.state == State.OPEN

def test_half_open_recovery():
    breaker = CircuitBreaker(failure_threshold=2, timeout=1)
    
    # Open the circuit
    for _ in range(2):
        with pytest.raises(Exception):
            breaker.call(lambda: raise_exception())
    
    # Wait for timeout
    time.sleep(1.1)
    
    # Should enter half-open
    breaker.call(lambda: "success")  # Successful test
    
    assert breaker.state == State.CLOSED
```

## Rules

- Circuit breaker protects caller from repeated failures, not called service.
- OPEN state must fail fast — return immediately without calling service.
- Half-open state tests with limited requests (3-5) before fully closing.
- Timeout in OPEN state typically 30-60 seconds — enough for service to recover.
- Failure threshold 5-10 consecutive failures OR 50% failure rate in last 10 requests.
- Fallback required for user-facing features — cached data, defaults, degraded mode.
- Monitor state changes — OPEN state triggers PagerDuty for critical services.
- Per-endpoint breakers, not per-service — `/slow-endpoint` may fail while `/fast` works.
- Request timeout (5-30s) must be shorter than circuit evaluation to prevent hanging.
- Distributed systems need shared state (Redis) so all servers see OPEN state.
