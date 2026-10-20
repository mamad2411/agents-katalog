---
name: python-idioms
description: "Pythonic idioms - itertools, descriptors, 'there must be a better way'"
---

# Raymond Hettinger - Pythonic Idioms

Apply Raymond Hettinger's teaching style and Python expertise. Core Python developer, famous for transforming verbose code into elegant, idiomatic Python.

## Core Philosophy

### "There Must Be a Better Way"

Hettinger's signature phrase. When code feels verbose or awkward, Python probably has a better pattern.

```python
# BEFORE: Awkward iteration
for i in range(len(items)):
    print(i, items[i])

# AFTER: "There must be a better way"
for i, item in enumerate(items):
    print(i, item)
```

### Itertools for Everything

```python
from itertools import chain, groupby, islice, cycle, combinations

# Flatten nested lists
flat = list(chain.from_iterable(nested_lists))

# Group by key
for key, group in groupby(sorted(data, key=keyfunc), keyfunc):
    process(key, list(group))

# Take first n
first_ten = list(islice(generator, 10))

# All pairs
for a, b in combinations(items, 2):
    compare(a, b)
```

## Prescriptive Rules

### Use Named Tuples for Data

```python
# BAD: Magic indices
point = (3, 4)
print(point[0], point[1])

# GOOD: Named tuple
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
point = Point(3, 4)
print(point.x, point.y)

# BETTER (Python 3.6+): typing.NamedTuple
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
```

### Descriptors Over Property Repetition

```python
# BAD: Repeated property pattern
class Circle:
    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Must be positive")
        self._radius = value

    # Same pattern for diameter, area... repetitive!

# GOOD: Descriptor for reusable validation
class Positive:
    def __set_name__(self, owner, name):
        self.name = name
        self.private = f'_{name}'

    def __get__(self, obj, type=None):
        return getattr(obj, self.private, None)

    def __set__(self, obj, value):
        if value < 0:
            raise ValueError(f"{self.name} must be positive")
        setattr(obj, self.private, value)

class Circle:
    radius = Positive()
    diameter = Positive()
```

### Defaultdict and Counter

```python
# BAD: Manual defaulting
word_count = {}
for word in words:
    if word not in word_count:
        word_count[word] = 0
    word_count[word] += 1

# GOOD: Counter
from collections import Counter
word_count = Counter(words)

# BAD: Manual list building
groups = {}
for item in items:
    key = get_key(item)
    if key not in groups:
        groups[key] = []
    groups[key].append(item)

# GOOD: defaultdict
from collections import defaultdict
groups = defaultdict(list)
for item in items:
    groups[get_key(item)].append(item)
```

### Context Managers for Resources

```python
# Hettinger pattern: contextlib for simple cases
from contextlib import contextmanager

@contextmanager
def timer(name):
    start = time.time()
    yield
    print(f"{name}: {time.time() - start:.2f}s")

with timer("processing"):
    do_work()
```

### Decorator Patterns

```python
from functools import wraps, lru_cache

# Always use @wraps to preserve metadata
def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Use lru_cache for memoization
@lru_cache(maxsize=128)
def expensive_calculation(n):
    return sum(range(n))
```

## Hettinger's Greatest Hits

### Transform Loops

```python
# Filtering
# BAD
result = []
for x in items:
    if condition(x):
        result.append(x)

# GOOD
result = [x for x in items if condition(x)]
# or
result = list(filter(condition, items))

# Mapping
# BAD
result = []
for x in items:
    result.append(transform(x))

# GOOD
result = [transform(x) for x in items]
# or
result = list(map(transform, items))
```

### Multiple Assignment

```python
# Swap
a, b = b, a

# Unpack
first, *rest = items
first, *middle, last = items

# Ignore values
_, important, _ = get_triple()
```

### Dictionary Patterns

```python
# Merge dictionaries (Python 3.9+)
merged = dict1 | dict2

# Get with default
value = d.get(key, default)

# setdefault for accumulation
d.setdefault(key, []).append(value)

# Dictionary comprehension
squared = {x: x**2 for x in range(10)}
```

## Anti-Patterns

| Pattern | Hettinger Fix |
|---------|---------------|
| `for i in range(len(x))` | `for i, item in enumerate(x)` |
| `dict.keys()` iteration | Just `for key in dict` |
| Manual counter in loop | `enumerate()` or `Counter` |
| `if x in dict.keys()` | `if x in dict` |
| Building string in loop | `''.join(parts)` |
| `lambda x: func(x)` | Just `func` |

## Review Checklist

Before shipping Python code:

- [ ] Could this loop be a comprehension?
- [ ] Is there an itertools function for this?
- [ ] Are we using enumerate instead of range(len())?
- [ ] Could we use a named tuple or dataclass?
- [ ] Is repetitive property logic a descriptor candidate?
- [ ] Are we using Counter/defaultdict where appropriate?
- [ ] Do decorators preserve function metadata with @wraps?

## Key Quotes

> "There must be a better way."

> "If the implementation is hard to explain, it's a bad idea."

> "Transforming code to be more Pythonic is not about fewer lines—it's about clearer intent."
