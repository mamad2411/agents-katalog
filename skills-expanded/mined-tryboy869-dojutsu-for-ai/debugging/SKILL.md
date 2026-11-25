---
name: debugging
description: "Apply when debugging errors, crashes, performance issues, or unexpected behavior. Covers: systematic debug approach, Python debuggers, logging strategies, profiling, common error patterns. Trigger for: bug, error, crash, debug, traceback, exception, not working."
---

# DEBUGGING — Systematic Approach

## The 5-Step Method (always)
1. **Reproduce** — get a minimal reproducible case
2. **Isolate** — binary search: comment half, does it still fail?
3. **Hypothesize** — one theory at a time
4. **Verify** — prove or disprove with a test
5. **Fix + test** — confirm fix doesn't break other things

## Python Debugging Tools
```python
# 1. pdb — built-in debugger
import pdb; pdb.set_trace()
# or Python 3.7+:
breakpoint()  # drops into pdb

# 2. Rich traceback (much more readable)
from rich.traceback import install
install(show_locals=True)

# 3. Inspect object at runtime
import inspect
print(inspect.getmembers(obj, predicate=inspect.ismethod))

# 4. Trace all calls (nuclear option)
import sys
def trace(frame, event, arg):
    print(f"{event}: {frame.f_code.co_filename}:{frame.f_lineno}")
    return trace
sys.settrace(trace)
```

## Async Debugging
```python
# Detect unawaited coroutines
import asyncio
asyncio.get_event_loop().set_debug(True)

# Find deadlocks — print all running tasks
for task in asyncio.all_tasks():
    print(task.get_name(), task.get_coro())
```

## Performance Profiling
```python
# cProfile — which function is slow?
python -m cProfile -s cumulative myapp.py | head -30

# Memory — find leaks
from memory_profiler import profile
@profile
def my_function(): ...

# Line-level timing
from line_profiler import LineProfiler
lp = LineProfiler(my_function)
lp.run("my_function()")
lp.print_stats()
```

## Common Error Patterns
```python
# RecursionError → missing base case or circular reference
# MemoryError → loading entire dataset, use generators/chunks
# RuntimeError: event loop closed → mixing sync/async incorrectly
# TypeError: coroutine was never awaited → missing await keyword
# KeyError in dict → use .get() or check with 'in'
# AttributeError: NoneType → null check before .method()
```

## Forbidden Debugging Habits
❌ `print()` statements left in production code
❌ "It works on my machine" without checking env differences
❌ Fixing symptoms without understanding root cause
❌ Debugging production with live data (use staging)
❌ Commenting out code instead of using proper breakpoints
