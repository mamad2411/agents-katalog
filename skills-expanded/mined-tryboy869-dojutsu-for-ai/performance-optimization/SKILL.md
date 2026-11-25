---
name: performance-optimization
description: "Apply when optimizing slow code, reducing latency, or improving throughput. Covers: profiling methodology, async optimization, database N+1, caching strategies, payload size reduction. Trigger for: slow, performance, optimize, latency, throughput, bottleneck, speed."
---

# PERFORMANCE OPTIMIZATION — Systematic Approach

## Rule #1: Measure first, optimize second
```python
# Never guess — profile first
# 80% of performance problems are in 20% of code

import time, cProfile, pstats

# Quick timing
start = time.perf_counter()
result = my_function()
print(f"{time.perf_counter() - start:.3f}s")

# Full profile
cProfile.run("my_function()", "profile.stats")
p = pstats.Stats("profile.stats")
p.sort_stats("cumulative").print_stats(20)
```

## Database — Most Common Bottleneck

### Fix N+1 (most impactful)
```python
# ❌ N+1: 1 + N queries
jobs = await db.fetch_all("SELECT * FROM jobs")
for job in jobs:
    user = await db.fetch("SELECT * FROM users WHERE id = ?", job.user_id)  # N queries

# ✅ 1 query with JOIN
jobs = await db.fetch_all("""
    SELECT j.*, u.email, u.name
    FROM jobs j JOIN users u ON u.id = j.user_id
""")
```

### Add missing indexes
```sql
-- Find slow queries (PostgreSQL)
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10;

-- Add index for the slow query's WHERE clause
CREATE INDEX CONCURRENTLY idx_jobs_status_created
ON jobs (status, created_at DESC) WHERE status = 'pending';
```

## Async — Parallelize I/O
```python
# ❌ Sequential (slow)
user = await fetch_user(user_id)
jobs = await fetch_jobs(user_id)
settings = await fetch_settings(user_id)

# ✅ Concurrent (3× faster for I/O)
user, jobs, settings = await asyncio.gather(
    fetch_user(user_id),
    fetch_jobs(user_id),
    fetch_settings(user_id),
)
```

## Caching Strategy
```python
# L1: In-process (fastest, process-local)
from functools import lru_cache
@lru_cache(maxsize=256)
def get_config(key: str) -> str: ...

# L2: Redis (shared across workers, survives restart)
async def get_user_cached(user_id: str):
    key = f"user:{user_id}"
    if data := await redis.get(key):
        return json.loads(data)
    user = await db.fetch_user(user_id)
    await redis.setex(key, 300, json.dumps(user))
    return user
```

## Payload Optimization
```python
# Only return fields the client needs
# ❌ SELECT * → full object always
# ✅ Use field selection
@app.get("/jobs")
async def list_jobs(fields: str = "id,status,created_at"):
    selected = fields.split(",")
    return [pick(job, selected) for job in jobs]

# Compression
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

## Forbidden
❌ Optimizing without profiling first
❌ Premature optimization (< 1000 users)
❌ Caching mutable data without TTL
❌ CPU-heavy work in async functions (use ProcessPoolExecutor)
❌ Synchronous DB calls in async context
