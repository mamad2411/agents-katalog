---
name: python-protocols
description: "Fluent Python - data model, protocols, dunder methods, Pythonic design"
---

# Luciano Ramalho - Fluent Python

Apply Luciano Ramalho's expertise from "Fluent Python." Master Python's data model, protocols, and the patterns that make code truly Pythonic.

## Core Philosophy

### The Data Model Is Everything

Python's special methods (dunder methods) define how objects behave. Understanding them is the key to Pythonic code.

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector({self.x!r}, {self.y!r})'

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

# Now Vector works naturally with Python
v = Vector(3, 4)
abs(v)        # 5.0
bool(v)       # True
v + v         # Vector(6, 8)
v * 3         # Vector(9, 12)
```

### Protocols Over Inheritance

Python uses duck typing. Implement protocols (sets of methods) rather than inheriting from base classes.

```python
# The Sequence protocol: __len__ and __getitem__
class Deck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit)
                       for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

# Now Deck supports: iteration, slicing, in, reversed, sorted
deck = Deck()
len(deck)           # 52
deck[0]             # Card(rank='2', suit='spades')
deck[-1]            # Card(rank='A', suit='hearts')
deck[12::13]        # Four aces
Card('Q', 'hearts') in deck  # True
for card in deck:   # Iteration works
    print(card)
```

## Prescriptive Rules

### Implement __repr__ for All Classes

```python
# BAD: Default repr is useless
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# >>> Point(3, 4)
# <Point object at 0x...>

# GOOD: Informative repr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'{self.__class__.__name__}({self.x!r}, {self.y!r})'

# >>> Point(3, 4)
# Point(3, 4)
```

### Use @property for Computed Attributes

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError('Radius must be positive')
        self._radius = value

    @property
    def area(self):
        return 3.14159 * self._radius ** 2

    @property
    def diameter(self):
        return self._radius * 2
```

### Use __slots__ When Memory Matters

```python
class Pixel:
    __slots__ = ('x', 'y', 'color')

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

# Millions of Pixels? __slots__ saves significant memory
```

### Callable Objects

```python
# Classes can be callable
class Averager:
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        return sum(self.series) / len(self.series)

avg = Averager()
avg(10)  # 10.0
avg(11)  # 10.5
avg(12)  # 11.0
```

### Context Manager Protocol

```python
class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None

    def __enter__(self):
        self.connection = connect(self.connection_string)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        return False  # Don't suppress exceptions

with DatabaseConnection('...') as conn:
    conn.execute('SELECT ...')
```

## Key Protocols

| Protocol | Methods | Enables |
|----------|---------|---------|
| Container | `__contains__` | `in` operator |
| Sized | `__len__` | `len()` |
| Iterable | `__iter__` | `for` loops |
| Sequence | `__getitem__`, `__len__` | Indexing, slicing, iteration |
| Mapping | `__getitem__`, `__contains__`, `__iter__` | Dict-like access |
| Callable | `__call__` | `obj()` syntax |
| Context Manager | `__enter__`, `__exit__` | `with` statement |
| Hashable | `__hash__`, `__eq__` | Dict keys, set members |

## Anti-Patterns

| Pattern | Ramalho Fix |
|---------|-------------|
| Bare class with no `__repr__` | Always implement `__repr__` |
| Getter/setter methods | Use `@property` |
| `isinstance()` checks everywhere | Duck typing, protocols |
| Inheriting from `list`/`dict` | Compose with delegation |
| Mutable default arguments | Use `None` and create in `__init__` |

## Review Checklist

- [ ] Does every class have a useful `__repr__`?
- [ ] Are computed attributes using `@property`?
- [ ] Are we implementing protocols instead of inheriting?
- [ ] Is `__hash__` consistent with `__eq__`?
- [ ] Are context managers used for resource management?
- [ ] Is `__slots__` used for memory-critical classes?

## Key Insight

> "Pythonic code is not about tricks or idioms—it's about leveraging Python's data model. When you implement the right special methods, your objects integrate naturally with the language."
