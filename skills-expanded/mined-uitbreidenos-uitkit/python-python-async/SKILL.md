---
name: "python-async"
description: "Python asyncio patterns: async/await, concurrent tasks, aiohttp, timeouts, queues, background tasks, common pitfalls"
---

# Python Async Skill

## When to activate
- Writing async Python code with `asyncio`
- Running I/O operations concurrently (multiple API calls, DB queries)
- Using `aiohttp` for async HTTP requests
- Managing background tasks in FastAPI or other async frameworks
- Debugging async code (event loop issues, deadlocks, blocking calls)
- Setting up async task queues or worker patterns

## When NOT to use
- CPU-bound work — async doesn't help here, use `multiprocessing` or `ProcessPoolExecutor`
- Simple scripts with one or two sequential I/O calls — `requests` is simpler
- When the library you need only has a sync interface — wrap it instead

## Instructions

### Core patterns

```python
import asyncio

# Basic coroutine
async def fetch_user(user_id: int) -> dict:
    await asyncio.sleep(0.1)  # simulates I/O
    return {"id": user_id, "name": "Alice"}

# Run a coroutine
user = asyncio.run(fetch_user(1))

# Await in an async context
async def main():
    user = await fetch_user(1)
    print(user)
```

### Concurrent execution — the key skill

```python
# Sequential (slow — waits for each one)
async def fetch_all_sequential(ids: list[int]) -> list[dict]:
    results = []
    for id in ids:  # each waits for the previous
        results.append(await fetch_user(id))
    return results

# Concurrent with gather (all start at once)
async def fetch_all_concurrent(ids: list[int]) -> list[dict]:
    tasks = [fetch_user(id) for id in ids]
    return await asyncio.gather(*tasks)  # runs all concurrently

# gather with error handling (return_exceptions prevents one failure stopping all)
results = await asyncio.gather(*tasks, return_exceptions=True)
users = [r for r in results if not isinstance(r, Exception)]
errors = [r for r in results if isinstance(r, Exception)]
```

### TaskGroup (Python 3.11+ — structured concurrency)

```python
# TaskGroup is safer than gather — cancels all tasks if any fails
async def fetch_dashboard(user_id: str) -> dict:
    async with asyncio.TaskGroup() as tg:
        user_task    = tg.create_task(fetch_user(user_id))
        orders_task  = tg.create_task(fetch_orders(user_id))
        metrics_task = tg.create_task(fetch_metrics(user_id))
    # All tasks finished by here (or all cancelled if any raised)
    return {
        "user":    user_task.result(),
        "orders":  orders_task.result(),
        "metrics": metrics_task.result(),
    }
```

### Timeouts

```python
import asyncio

# Single operation timeout
try:
    result = await asyncio.wait_for(fetch_user(id), timeout=5.0)
except asyncio.TimeoutError:
    raise HTTPException(504, "Upstream timed out")

# Timeout for a group (Python 3.11+)
try:
    async with asyncio.timeout(10.0):
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(call_service_a())
            t2 = tg.create_task(call_service_b())
except TimeoutError:
    # Both tasks were cancelled
    ...
```

### aiohttp — async HTTP client

```python
import aiohttp

# Session reuse is critical — don't create a new session per request
class HttpClient:
    _session: aiohttp.ClientSession | None = None

    @classmethod
    async def get_session(cls) -> aiohttp.ClientSession:
        if cls._session is None or cls._session.closed:
            cls._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10),
                headers={"User-Agent": "myapp/1.0"},
            )
        return cls._session

    @classmethod
    async def close(cls):
        if cls._session:
            await cls._session.close()

# Single request
async def fetch_github_user(username: str) -> dict:
    session = await HttpClient.get_session()
    async with session.get(f"https://api.github.com/users/{username}") as resp:
        resp.raise_for_status()
        return await resp.json()

# Multiple concurrent requests
async def fetch_many(urls: list[str]) -> list[dict]:
    session = await HttpClient.get_session()
    async def fetch(url: str) -> dict:
        async with session.get(url) as resp:
            resp.raise_for_status()
            return await resp.json()
    return await asyncio.gather(*[fetch(url) for url in urls])
```

### Background tasks in FastAPI

```python
from fastapi import BackgroundTasks

@router.post("/orders")
async def create_order(
    payload: CreateOrderRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    order = await order_service.create(db, payload)

    # Queue side effects — run after response is sent
    background_tasks.add_task(send_confirmation_email, order.id)
    background_tasks.add_task(update_inventory, order.items)

    return order

# For longer-running tasks, use a proper queue (Celery, arq, dramatiq)
```

### Async queues for producer-consumer

```python
import asyncio

async def producer(queue: asyncio.Queue, items: list):
    for item in items:
        await queue.put(item)
    # Signal completion
    await queue.put(None)

async def consumer(queue: asyncio.Queue, worker_id: int):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break  # sentinel received, shut down
        await process(item)
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=100)  # backpressure
    items = list(range(1000))

    # 5 concurrent workers
    workers = [asyncio.create_task(consumer(queue, i)) for i in range(5)]
    await producer(queue, items)
    await queue.join()  # wait for all items processed
    for w in workers:
        w.cancel()
```

### Semaphore — limit concurrency

```python
# Limit to 10 concurrent outbound requests (avoid overloading external APIs)
semaphore = asyncio.Semaphore(10)

async def fetch_with_limit(url: str) -> dict:
    async with semaphore:
        async with session.get(url) as resp:
            return await resp.json()

results = await asyncio.gather(*[fetch_with_limit(url) for url in urls])
```

### Common pitfalls

**Blocking the event loop (the #1 async mistake):**
```python
# Bad — time.sleep() blocks the entire event loop
async def do_work():
    time.sleep(1)          # ❌ blocks all other coroutines
    requests.get(url)      # ❌ sync HTTP library in async context

# Good
async def do_work():
    await asyncio.sleep(1)         # ✅ yields control
    async with session.get(url):   # ✅ async HTTP
        ...

# Run sync blocking code in a thread pool
result = await asyncio.get_event_loop().run_in_executor(
    None, sync_blocking_function, arg1, arg2
)
```

**Forgetting to await:**
```python
# Bad — creates a coroutine object, doesn't execute it
async def bad():
    result = fetch_user(1)  # ❌ missing await — just creates coroutine

# Good
async def good():
    result = await fetch_user(1)  # ✅
```

**Creating tasks without awaiting them:**
```python
# Bad — "fire and forget" can cause errors to be silently lost
async def bad():
    asyncio.create_task(risky_operation())  # errors are swallowed

# Good — keep a reference and handle errors
async def good():
    task = asyncio.create_task(risky_operation())
    task.add_done_callback(lambda t: t.exception() and log_error(t.exception()))
```

### Async context managers

```python
class AsyncDatabaseConnection:
    async def __aenter__(self):
        self.conn = await asyncpg.connect(DATABASE_URL)
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()

async def main():
    async with AsyncDatabaseConnection() as conn:
        await conn.fetch("SELECT 1")

# async generator for streaming
async def stream_rows(query: str):
    async with AsyncDatabaseConnection() as conn:
        async for row in conn.cursor(query):
            yield dict(row)

async def process():
    async for row in stream_rows("SELECT * FROM large_table"):
        await handle(row)
```

## Example

**User:** Fetch data from 3 external APIs concurrently with individual timeouts, retry failed requests once, and return partial results if some fail — all within a 10-second total budget.

**Expected output:**
```python
async def fetch_dashboard(user_id: str) -> DashboardData:
    async with asyncio.timeout(10.0):
        async with asyncio.TaskGroup() as tg:
            profile_task = tg.create_task(
                fetch_with_retry(f"/profiles/{user_id}", timeout=3)
            )
            orders_task = tg.create_task(
                fetch_with_retry(f"/orders/{user_id}", timeout=5)
            )
            metrics_task = tg.create_task(
                fetch_with_retry(f"/metrics/{user_id}", timeout=3)
            )
    return DashboardData(
        profile=profile_task.result(),
        orders=orders_task.result(),
        metrics=metrics_task.result(),
    )
```

---
