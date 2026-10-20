---
name: high-availability-architecture
description: High availability patterns — redundancy, load balancing, health checks, circuit breakers
triggers: [high availability, HA, redundancy, load balancing, fault tolerance, circuit breaker]
---

# SKILL: High Availability Architecture

## Redundancy Patterns

```yaml
# Multi-zone deployment (99.99% availability)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 6  # Spread across zones
  
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app: myapp
        topologyKey: topology.kubernetes.io/zone
```

## Load Balancing

```python
from fastapi import FastAPI, Request
import httpx

app = FastAPI()

# Health check endpoint
@app.get("/health")
async def health():
    # Check dependencies
    db_healthy = check_database()
    cache_healthy = check_redis()
    
    if db_healthy and cache_healthy:
        return {"status": "healthy"}
    else:
        return {"status": "unhealthy"}, 503
```

## Circuit Breaker Pattern

```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
def call_external_api():
    """Circuit breaker: fail fast if service down"""
    response = requests.get("https://api.example.com")
    if response.status_code != 200:
        raise Exception("API error")
    return response.json()

# After 5 failures, circuit "opens" (stops calling)
# After 60 seconds, circuit "half-opens" (tries again)
```

## Quality Checks
- [ ] Multi-zone/region deployment
- [ ] Load balancer configured
- [ ] Health checks implemented
- [ ] Circuit breakers on external calls
- [ ] Auto-scaling enabled
- [ ] Database replication (primary + replica)
- [ ] Graceful shutdown handling
- [ ] 99.9%+ uptime SLA
