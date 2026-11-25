---
name: python-advanced
description: "Advanced Python - generators, coroutines, metaprogramming, execution model"
---

# David Beazley - Advanced Python

Apply David Beazley's deep technical expertise. Author of Python Cookbook and Python Essential Reference, master of generators, coroutines, and metaprogramming.

## Core Philosophy

### Understand the Execution Model

Beazley emphasizes understanding how Python actually executes code—not just what it does, but how.

```python
# Understanding generator execution
def countdown(n):
    print("Starting countdown")
    while n > 0:
        yield n  # Suspends here, resumes on next()
        n -= 1
    print("Done")

# Nothing executes until iteration begins
gen = countdown(5)  # No output yet!
next(gen)  # "Starting countdown", returns 5
next(gen)  # Returns 4 (resumes after yield)
```

### Generators Are the Foundation

Everything in async Python builds on generators.

```python
# Generator for lazy evaluation
def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield line.strip()

# Pipeline processing
def grep(pattern, lines):
    for line in lines:
        if pattern in line:
            yield line

def upper(lines):
    for line in lines:
        yield line.upper()

# Compose pipelines (memory efficient)
lines = read_large_file('huge.log')
matches = grep('ERROR', lines)
results = upper(matches)
```

## Prescriptive Rules

### Generator Expressions Over List Comprehensions

```python
# BAD: Creates entire list in memory
total = sum([x * x for x in range(1000000)])

# GOOD: Generator expression, processes one at a time
total = sum(x * x for x in range(1000000))

# BAD: Multiple passes over data
data = [process(x) for x in items]
filtered = [x for x in data if condition(x)]

# GOOD: Single pass with generator pipeline
processed = (process(x) for x in items)
filtered = (x for x in processed if condition(x))
```

### Context Managers for Resource Safety

```python
from contextlib import contextmanager, ExitStack

# Simple context manager
@contextmanager
def managed_resource(name):
    print(f"Acquiring {name}")
    resource = acquire(name)
    try:
        yield resource
    finally:
        print(f"Releasing {name}")
        resource.release()

# Multiple resources with ExitStack
with ExitStack() as stack:
    files = [stack.enter_context(open(f)) for f in filenames]
    # All files automatically closed on exit
```

### Coroutines for Async Patterns

```python
# Modern async/await (built on coroutines)
import asyncio

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def fetch_all(urls):
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)

# Run async code
results = asyncio.run(fetch_all(urls))
```

### Metaprogramming with Purpose

```python
# Descriptors for managed attributes
class TypedProperty:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type

    def __get__(self, obj, cls):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Expected {self.expected_type}")
        obj.__dict__[self.name] = value

# Class decorator for auto-generating
def auto_repr(cls):
    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'{cls.__name__}({attrs})'
    cls.__repr__ = __repr__
    return cls
```

### Closures and Function Factories

```python
# Closure captures state
def make_counter(start=0):
    count = start
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

# Function factory
def make_validator(min_val, max_val):
    def validate(value):
        if not (min_val <= value <= max_val):
            raise ValueError(f"Must be between {min_val} and {max_val}")
        return value
    return validate

age_validator = make_validator(0, 150)
```

## Advanced Patterns

### yield from for Delegation

```python
# Flatten nested structures
def flatten(items):
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

# Coroutine delegation
def grouper(results, key):
    while True:
        results[key] = yield from accumulator()
```

### __slots__ for Memory Efficiency

```python
# Default: each instance has a dict
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
# Each instance: ~300+ bytes

# With slots: fixed attributes, no dict
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y
# Each instance: ~50 bytes
```

### weakref for Cache Management

```python
import weakref

class ExpensiveObject:
    _cache = weakref.WeakValueDictionary()

    def __new__(cls, key):
        if key in cls._cache:
            return cls._cache[key]
        obj = super().__new__(cls)
        cls._cache[key] = obj
        return obj
```

## Anti-Patterns

| Pattern | Beazley Fix |
|---------|-------------|
| Large list comprehension | Generator expression |
| Manual file cleanup | Context manager |
| Callback pyramids | async/await |
| Copy-paste validation | Descriptors |
| Global state | Closures |

## Review Checklist

- [ ] Are large collections lazily evaluated?
- [ ] Are resources managed with context managers?
- [ ] Is async code using modern async/await?
- [ ] Could repetitive patterns use metaprogramming?
- [ ] Are closures used instead of global state?
- [ ] Is memory-critical code using __slots__?

## Key Insight

> "Python's power comes from understanding its execution model. Generators aren't just syntax—they're the foundation of Python's approach to iteration, coroutines, and async programming."
