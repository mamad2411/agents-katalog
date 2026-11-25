# Asyncio Error Handling

Error handling patterns for async Python code, including TaskGroup, timeouts, and background tasks.

## Basic try/except in async

Works the same as synchronous code:

```python
async def fetch_user(user_id: int) -> User:
    try:
        return await db.users.get(user_id)
    except DatabaseError as e:
        raise UserServiceError("Database unavailable") from e
```

## TaskGroup (Python 3.11+)

### Basic Usage

`TaskGroup` provides structured concurrency with automatic cleanup:

```python
import asyncio

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_user(1))
        task2 = tg.create_task(fetch_user(2))
    
    # Both tasks completed successfully
    user1 = task1.result()
    user2 = task2.result()
```

### Error Handling

If any task fails, all other tasks are cancelled:

```python
async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(fetch_user(1))      # Succeeds
            tg.create_task(failing_task())      # Raises error
            tg.create_task(slow_task())         # Gets cancelled
    except* ValueError as eg:
        # ExceptionGroup containing the ValueError
        for exc in eg.exceptions:
            print(f"Task failed: {exc}")
```

### except* Syntax (Python 3.11+)

Handle multiple exceptions from TaskGroup:

```python
async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(task_raises_value_error())
            tg.create_task(task_raises_type_error())
    except* ValueError as eg:
        print(f"ValueError count: {len(eg.exceptions)}")
    except* TypeError as eg:
        print(f"TypeError count: {len(eg.exceptions)}")
```

## Timeouts

### asyncio.timeout (Python 3.11+)

```python
import asyncio

async def fetch_with_timeout():
    try:
        async with asyncio.timeout(10.0):
            return await slow_operation()
    except TimeoutError:
        raise ExternalServiceError("Operation timed out")
```

### asyncio.wait_for (Legacy)

```python
async def fetch_with_timeout():
    try:
        return await asyncio.wait_for(slow_operation(), timeout=10.0)
    except asyncio.TimeoutError:
        raise ExternalServiceError("Operation timed out")
```

### Nested Timeouts

Inner timeout should be shorter than outer:

```python
async def complex_operation():
    async with asyncio.timeout(30.0):  # Overall timeout
        result1 = await fetch_data()
        
        async with asyncio.timeout(10.0):  # Per-operation timeout
            result2 = await process_data(result1)
        
        return result2
```

## Background Tasks in FastAPI

### The Problem

Background tasks run after the response is sent - exceptions are lost:

```python
from fastapi import BackgroundTasks

@app.post("/orders")
async def create_order(order: Order, background_tasks: BackgroundTasks):
    result = await order_service.create(order)
    # If send_email fails, client never knows
    background_tasks.add_task(send_confirmation_email, result.id)
    return result
```

### Solution: Wrapper Function

```python
import logging

logger = logging.getLogger(__name__)

async def safe_background_task(
    task_func,
    *args,
    task_name: str = "background_task",
    **kwargs
):
    """Wrapper that catches and logs background task errors."""
    try:
        if asyncio.iscoroutinefunction(task_func):
            await task_func(*args, **kwargs)
        else:
            task_func(*args, **kwargs)
    except Exception as e:
        logger.exception(f"Background task '{task_name}' failed: {e}")
        # Optional: Send to error tracking, dead letter queue, etc.

@app.post("/orders")
async def create_order(order: Order, background_tasks: BackgroundTasks):
    result = await order_service.create(order)
    background_tasks.add_task(
        safe_background_task,
        send_confirmation_email,
        result.id,
        task_name="send_confirmation_email"
    )
    return result
```

## Starlette Lifespan Events

### Error in Startup

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await database.connect()
        await cache.connect()
    except Exception as e:
        logger.exception("Startup failed")
        raise  # App won't start
    
    yield
    
    # Shutdown
    await database.disconnect()
    await cache.disconnect()

app = FastAPI(lifespan=lifespan)
```

### Graceful Shutdown

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    # Shutdown - don't raise, just log
    try:
        await database.disconnect()
    except Exception as e:
        logger.error(f"Error during database disconnect: {e}")
    
    try:
        await cache.disconnect()
    except Exception as e:
        logger.error(f"Error during cache disconnect: {e}")
```

## CancelledError Handling

`CancelledError` is a `BaseException` (not `Exception`) - handle carefully:

```python
async def cancellable_task():
    try:
        await long_running_operation()
    except asyncio.CancelledError:
        # Clean up resources
        await cleanup()
        raise  # Always re-raise CancelledError!
```

### Don't Suppress CancelledError

```python
# BAD - Breaks cancellation
async def bad_task():
    try:
        await operation()
    except asyncio.CancelledError:
        pass  # Swallows cancellation - task keeps running!

# GOOD - Re-raise after cleanup
async def good_task():
    try:
        await operation()
    except asyncio.CancelledError:
        await cleanup()
        raise
```

## Common Pitfalls

### Blocking the Event Loop

```python
import asyncio

# BAD - Blocks event loop
async def bad_endpoint():
    time.sleep(10)  # Blocks!
    return {"status": "done"}

# GOOD - Use asyncio.sleep or run_in_executor
async def good_endpoint():
    await asyncio.sleep(10)  # Non-blocking
    return {"status": "done"}

# GOOD - For blocking I/O
async def good_endpoint():
    result = await asyncio.to_thread(blocking_io_operation)
    return result
```

### Fire-and-Forget Tasks

```python
# BAD - Task may be garbage collected
async def bad_handler():
    asyncio.create_task(background_work())  # May disappear!
    return {"status": "ok"}

# GOOD - Keep reference
background_tasks = set()

async def good_handler():
    task = asyncio.create_task(background_work())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    return {"status": "ok"}
```

### Unchecked Task Exceptions

```python
# BAD - Exception is lost
async def main():
    task = asyncio.create_task(failing_task())
    await asyncio.sleep(10)
    # Exception in failing_task is never seen

# GOOD - Check task result
async def main():
    task = asyncio.create_task(failing_task())
    await asyncio.sleep(10)
    if task.done():
        exc = task.exception()
        if exc:
            logger.error(f"Task failed: {exc}")
```

## Concurrent Operations with Error Handling

### asyncio.gather

```python
async def fetch_all_users(user_ids: list[int]) -> list[User | None]:
    # return_exceptions=True - don't fail on first error
    results = await asyncio.gather(
        *[fetch_user(uid) for uid in user_ids],
        return_exceptions=True
    )
    
    users = []
    for uid, result in zip(user_ids, results):
        if isinstance(result, Exception):
            logger.error(f"Failed to fetch user {uid}: {result}")
            users.append(None)
        else:
            users.append(result)
    return users
```

### TaskGroup vs gather

| Feature | TaskGroup | gather |
|---------|-----------|--------|
| Cancels other tasks on error | ✅ | ❌ (unless first exception) |
| Returns exceptions in results | ❌ | ✅ (with return_exceptions=True) |
| Structured concurrency | ✅ | ❌ |
| Python version | 3.11+ | 3.4+ |

```python
# Use TaskGroup when: all tasks must succeed
async with asyncio.TaskGroup() as tg:
    user = await tg.create_task(fetch_user(user_id))
    orders = await tg.create_task(fetch_orders(user_id))

# Use gather when: partial success is acceptable
results = await asyncio.gather(
    fetch_user(user_id),
    fetch_orders(user_id),
    return_exceptions=True
)
```
