---
name: python-concurrency
description: "When to activate: multiprocessing, threading, concurrent.futures, ProcessPoolExecutor, GIL, CPU-bound tasks"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Python Concurrency Patterns

## When to Use What
| Scenario | Tool |
|----------|------|
| I/O-bound async (web, db, APIs) | `asyncio` + `async/await` |
| I/O-bound threads (legacy libs) | `ThreadPoolExecutor` |
| CPU-bound parallel work | `ProcessPoolExecutor` |
| Simple parallel map | `multiprocessing.Pool.map` |
| Background jobs / distributed | Celery / ARQ |

## ProcessPoolExecutor (CPU-bound)
```python
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
import os

def compute_chunk(chunk: list[int], power: float) -> list[float]:
    return [x ** power for x in chunk]

def parallel_compute(data: list[int], power: float = 2.0) -> list[float]:
    num_cpus = os.cpu_count() or 4
    chunk_size = max(1, len(data) // num_cpus)
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    
    results = []
    with ProcessPoolExecutor(max_workers=num_cpus) as executor:
        fn = partial(compute_chunk, power=power)
        futures = {executor.submit(fn, chunk): i for i, chunk in enumerate(chunks)}
        ordered = {}
        for future in as_completed(futures):
            idx = futures[future]
            ordered[idx] = future.result()
    
    return [item for i in sorted(ordered) for item in ordered[i]]
```

## ThreadPoolExecutor (I/O-bound, sync libs)
```python
from concurrent.futures import ThreadPoolExecutor
import requests

def fetch_url(url: str) -> dict:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def fetch_all_sync(urls: list[str], max_workers: int = 10) -> list[dict]:
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(fetch_url, urls))

# Run sync in async context (don't block event loop)
import asyncio

async def fetch_sync_in_async(url: str) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, fetch_url, url)
```

## Multiprocessing Patterns
```python
import multiprocessing as mp
from multiprocessing import Pool, Queue, Process

# Shared state with Manager (across processes)
def worker(shared_dict: dict, key: str, value: int) -> None:
    shared_dict[key] = value

with mp.Manager() as manager:
    shared = manager.dict()
    processes = [Process(target=worker, args=(shared, f"key_{i}", i)) for i in range(4)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print(dict(shared))

# Queue-based producer-consumer
def producer(queue: Queue, items: list) -> None:
    for item in items:
        queue.put(item)
    queue.put(None)  # sentinel

def consumer(queue: Queue, results: list) -> None:
    while True:
        item = queue.get()
        if item is None:
            break
        results.append(process(item))
```

## GIL Awareness
- Python's GIL means threads run one at a time for Python code
- Threads help for I/O-bound tasks (GIL released during I/O)
- Threads do NOT help for CPU-bound tasks (GIL prevents parallelism)
- Processes bypass the GIL (separate memory space)
- `asyncio` is single-threaded cooperative multitasking (no GIL issue)
- In Python 3.13+: optional no-GIL mode (`python -X nogil`)
