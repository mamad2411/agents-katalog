---
name: python-memory-safe-scripts
description: >-
  Memory-safe Python script patterns for long-running processes under systemd MemoryMax constraints.
  Covers allocator purge (mimalloc/glibc malloc_trim), HTTP response lifecycle, DataFrame cleanup,
  thread-local connection reuse, and periodic GC cadence. Battle-tested through 5 OOM optimization
  cycles on production GPU workstations. Use this skill proactively whenever writing or reviewing
  Python scripts that: run under systemd with MemoryMax, process data in loops (downloads, ETL,
  backfill), use ThreadPoolExecutor, or make repeated HTTP requests. Also use when diagnosing OOM
  kills, RSS creep, or fd exhaustion in Python services.
  TRIGGERS - memory optimization, OOM prevention, RSS reduction, malloc_trim, systemd MemoryMax,
  memory leak, allocator purge, memory-safe script, RSS creep, fd exhaustion, SIGKILL status 9,
  MemoryHigh, glibc arena, mimalloc purge, requests memory leak, ThreadPoolExecutor cleanup.
allowed-tools: Read, Bash, Grep, Edit, Write
---

# Memory-Safe Python Script Patterns

Battle-tested patterns for keeping Python scripts alive under systemd `MemoryMax` constraints. Extracted from `repair_direct_parquet.py` (24-worker parallel repair) and `exness_tick_cache_seeder.py` (10-symbol daily seeder) after 5 OOM optimization cycles on a 62 GB GPU workstation.

**Core insight**: Python's garbage collector frees objects, but the C allocator (glibc ptmalloc2) does NOT return freed pages to the OS. Without explicit `malloc_trim(0)`, RSS only grows — even after `del` and `gc.collect()`. mimalloc with `MIMALLOC_PURGE_DELAY` helps but explicit purge is faster.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## The 7 Patterns

### 1. Cached Allocator Purge

The most important pattern. Cache the ctypes library handle on first call so subsequent purges are a single FFI invocation with zero allocation overhead.

```python
import ctypes
import gc
import sys

_purge_lib = None
_purge_method = None  # "mimalloc" | "glibc" | "none"

def _force_allocator_purge():
    """Force mimalloc/glibc to return freed pages to the OS."""
    global _purge_lib, _purge_method

    if sys.platform != "linux":
        return

    if _purge_method is None:
        try:
            _purge_lib = ctypes.CDLL("libmimalloc.so.2")
            _purge_method = "mimalloc"
        except OSError:
            try:
                _purge_lib = ctypes.CDLL("libc.so.6")
                _purge_method = "glibc"
            except OSError:
                _purge_method = "none"

    if _purge_method == "mimalloc":
        _purge_lib.mi_collect(ctypes.c_bool(True))
    elif _purge_method == "glibc":
        _purge_lib.malloc_trim(0)

def _force_gc():
    """Python GC + allocator purge. Call every 50 iterations + between work units."""
    gc.collect()
    _force_allocator_purge()
```

**Why cached handle matters**: `ctypes.CDLL("libc.so.6")` calls `dlopen()` which itself allocates memory. Calling it 1400 times in a loop is counterproductive. Cache it once.

**Why prefer mimalloc**: When `LD_PRELOAD=libmimalloc.so.2` is active, glibc's `malloc_trim` is a no-op because mimalloc intercepted all allocations. `mi_collect(True)` is the correct purge for mimalloc.

### 2. HTTP Response Lifecycle

Close responses immediately after extracting the content you need. The `requests` library holds the response body, connection pool references, and urllib3 internal state.

```python
# CORRECT: extract content, close, delete
resp = requests.get(url, timeout=60)
if resp.status_code != 200:
    resp.close()
    return None

content = resp.content  # Extract what you need
resp.close()            # Release connection pool reference
del resp                # Drop the Python object

# Process content...
del content             # Release after processing
```

```python
# WRONG: response lives until end of function scope
resp = requests.get(url, timeout=60)
data = parse(resp.content)  # resp still alive, holding ~18 MB
return data                 # resp GC'd eventually... maybe
```

**Why this matters**: Each `requests.Response` holds `content` (the full body), a reference to the `urllib3.HTTPResponse`, and the connection pool's `PoolManager`. With 4 concurrent workers processing 1400 URLs, unclosed responses accumulate hundreds of MB.

### 3. Explicit Object Deletion

Don't rely on Python's GC for large objects. Use `del` immediately after the object is no longer needed.

```python
# After writing a DataFrame to Parquet
_atomic_write_parquet(df, path)
del df  # Only reference gone → immediate refcount GC

# After extracting data from a ZIP
with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
    df = pl.read_csv(zf.open(zf.namelist()[0]), ...)
del zip_bytes  # Release raw ZIP content after parsing

# After processing a list of work items
results = process_all(missing_days)
del missing_days  # Release the 1400-element date list
```

**When to `del`**: any object larger than ~1 MB that you're done with. DataFrames, byte strings from HTTP responses, ZIP contents, large lists.

### 4. Periodic GC Cadence

Call `_force_gc()` at two levels:

```python
# Level 1: Every 50 iterations within a work unit
for i, item in enumerate(items):
    process(item)
    if (i + 1) % 50 == 0:
        _force_gc()

# Level 2: Between major work units
for symbol in symbols:
    seed_symbol(symbol)
    _force_gc()  # Release all per-symbol state before next symbol
```

**Why 50**: Empirically validated on a 32-core workstation. At 100, RSS drifts too high before purge. At 25, the purge overhead is measurable (~2% throughput loss). 50 is the sweet spot from `repair_direct_parquet.py`.

### 5. ThreadPoolExecutor Cleanup

After the executor exits, explicitly clean up residual state.

```python
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    pending = {}
    # ... bounded future submission pattern ...

# After pool exits:
del pending     # Future objects hold references to results
del missing     # Work item list
_force_gc()     # Release worker thread memory + allocator pages
```

For advanced cases (DB connections in workers), close thread-local resources explicitly:

```python
pool.shutdown(wait=False, cancel_futures=True)
for t in threading.enumerate():
    if t.name.startswith("ThreadPoolExecutor"):
        _close_worker_cache()  # Close DB connections
gc.collect()
_force_allocator_purge()
```

### 6. Thread-Local Connection Reuse

Never create database connections or HTTP sessions inside a loop. Use `threading.local()` to get one connection per worker thread.

```python
import threading

_thread_local = threading.local()

def _get_worker_cache():
    """One DB connection per worker thread, reused across all iterations."""
    cache = getattr(_thread_local, "cache", None)
    if cache is None:
        cache = DatabaseClient()
        _thread_local.cache = cache
    return cache

def _close_worker_cache():
    """Explicit cleanup at shutdown."""
    cache = getattr(_thread_local, "cache", None)
    if cache is not None:
        cache.close()
        _thread_local.cache = None
```

**Why this prevents fd exhaustion**: Each `urllib3.PoolManager(maxsize=20)` holds up to 20 file descriptors. Creating a new one per iteration in a 24-worker pool exhausts `ulimit -n 1024` within minutes. Thread-local reuse keeps fd count at ~4N+50 for N workers.

### 7. systemd Service Configuration

```ini
[Service]
# Memory limits — hard kill prevents runaway RSS
MemoryHigh=2G        # Soft limit: triggers reclaim pressure
MemoryMax=4G         # Hard limit: SIGKILL on breach
MemorySwapMax=0      # No swap escape — fail fast, don't thrash

# mimalloc: replaces glibc ptmalloc2, returns freed pages faster
Environment=LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libmimalloc.so.2
Environment=MIMALLOC_PURGE_DELAY=1000

# OOM priority (lower = more likely to survive)
OOMScoreAdjust=-200
ManagedOOMMemoryPressure=kill
```

**MemoryHigh vs MemoryMax**: `MemoryHigh` triggers kernel memory reclaim (cgroup pressure) — the process slows but survives. `MemoryMax` is a hard SIGKILL. Set MemoryHigh at 50-66% of MemoryMax so the kernel gets a chance to reclaim before killing.

---

## Anti-Patterns

| Anti-Pattern                             | Why It Fails                                               | Fix                                                              |
| ---------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------- |
| `ctypes.CDLL("libc.so.6")` inside a loop | `dlopen()` allocates memory; 1000 calls wastes ~50 MB      | Cache the handle in a module global                              |
| `requests.get()` without `resp.close()`  | Response body + connection pool held until GC              | `resp.close()` + `del resp` immediately after extracting content |
| No `gc.collect()` between work units     | Cyclic references accumulate across symbols/batches        | `_force_gc()` between every major work unit                      |
| New DB connection per loop iteration     | Each connection = 20 fds via urllib3 PoolManager           | `threading.local()` for one-per-thread reuse                     |
| Raising `MemoryMax` to fix OOM           | Masks the leak; RSS will grow to fill any limit            | Fix the leak first. The fix is always one of patterns 1-6        |
| `del df` without `gc.collect()`          | Refcount frees the object, but glibc holds the pages       | `del` + `gc.collect()` + `_force_allocator_purge()`              |
| `MemorySwapMax` not set                  | Process swaps to disk instead of dying; thrashes for hours | Set `MemorySwapMax=0` — fail fast, don't thrash                  |

---

## Diagnostic Checklist

When a script gets SIGKILL (status=9) under systemd:

1. **Confirm it's OOM**: `journalctl --user -u service.service | grep -E "killed|signal|KILL"`
2. **Check peak RSS**: `systemctl --user status service.service | grep Memory` (shows peak)
3. **Profile steady-state RSS**: Run the script manually, check `/proc/PID/status` for `VmRSS` at 3 time points 30s apart
4. **Check fd count**: `ls /proc/PID/fd | wc -l` — if >500, suspect connection churn (Pattern 6)
5. **Check allocator**: Is `LD_PRELOAD=libmimalloc.so.2` in the service file? If glibc, check if `malloc_trim` is called
6. **Add periodic logging**: `logger.info("RSS=%d MB", psutil.Process().memory_info().rss // 1048576)` every 50 iterations

---

## Reference Implementations

| Script                                | Patterns Used   | RSS Profile                                        |
| ------------------------------------- | --------------- | -------------------------------------------------- |
| `scripts/repair_direct_parquet.py`    | All 7 patterns  | Starts 3 GB, plateaus ~13 GB with 24 workers       |
| `scripts/exness_tick_cache_seeder.py` | Patterns 1-5, 7 | Flat 163 MB across 10 symbols x 1400 days          |
| `scripts/tick_cache_seeder.py`        | Patterns 3, 7   | Peak 2.5 GB with mimalloc (was 4.47 GB with glibc) |


## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
