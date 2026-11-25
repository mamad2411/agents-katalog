---
name: async-systems
description: "Apply when building async job queues, background workers, task processing systems, message brokers, or any producer-consumer architecture. Critical patterns for production reliability."
---

# ASYNC SYSTEMS — Production Patterns

## Non-Negotiable Architecture Decisions

### Queue Bounds (CRITICAL)
```python
# NEVER: asyncio.Queue() — unbounded = OOM under load
# ALWAYS:
queue = asyncio.Queue(maxsize=1000)  # explicit bound
# Or: Redis with XLEN check before XADD
```

### Backpressure
```python
# When queue is full, block producer (don't drop or crash)
try:
    await asyncio.wait_for(queue.put(job), timeout=5.0)
except asyncio.TimeoutError:
    raise HTTPException(503, "Queue full — retry later")
```

### Dead Letter Queue
```python
# After max_retries exceeded, move to DLQ — never discard
async def move_to_dlq(job, error):
    await redis.lpush("dlq:jobs", json.dumps({
        "job": job, "error": str(error),
        "failed_at": datetime.utcnow().isoformat()
    }))
```

### Idempotency Keys
```python
# Every job submission needs idempotency_key
# Check before processing: if already processed, return cached result
async def is_already_processed(idempotency_key: str) -> bool:
    return await redis.exists(f"idem:{idempotency_key}")
```

### Timeouts — Always Dual (Hard + Soft)
```python
# Soft limit: allow graceful cleanup
# Hard limit: kill regardless
TASK_SOFT_TIMEOUT = 270  # 4.5 min — raise SoftTimeLimitExceeded
TASK_HARD_TIMEOUT = 300  # 5 min — SIGKILL
```

### Worker Heartbeat
```python
# Workers must report liveness — detect zombie workers
async def heartbeat_loop(worker_id: str):
    while True:
        await redis.setex(f"worker:{worker_id}:alive", 30, "1")
        await asyncio.sleep(10)
```

## Stack Recommendations
- **Simple (< 100 jobs/sec)**: FastAPI + asyncio.Queue + asyncio workers
- **Medium (< 10k jobs/sec)**: FastAPI + Redis Streams (XADD/XREAD) + asyncio workers  
- **High throughput**: FastAPI + Celery + Redis/RabbitMQ broker + PostgreSQL for state
- **State persistence**: ALWAYS PostgreSQL for job records, NOT Redis (Redis is ephemeral)

## Forbidden Patterns
❌ `asyncio.Queue()` without maxsize
❌ Retry loops without exponential backoff
❌ Job state stored only in Redis (no persistence on restart)
❌ Workers without heartbeat/health check
❌ No dead letter queue (silent job loss)
❌ Synchronous DB calls inside async workers (blocks event loop)
