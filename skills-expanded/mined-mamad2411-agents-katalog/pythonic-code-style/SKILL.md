---
name: pythonic-code-style
description: Write, refactor, and review Python using current, verified Pythonic idioms instead of imported Java, C, or JavaScript patterns. Use when deciding what is Pythonic vs non-Pythonic in Python modules, scripts, tests, notebooks, CLIs, libraries, and APIs; when reviewing iteration, comprehensions, truthiness, exceptions, mappings, resources, string and path handling, mutation, typing, object design, imports, and structural pattern matching; and when Python version support must be checked before recommending modern syntax or standard-library features.
---

# Pythonic Code Style

Check the repo's supported Python version before recommending syntax or stdlib features. Read `pyproject.toml`, `.python-version`, CI config, Docker files, or tool config first.

Use [references/source-map.md](references/source-map.md) as the authority for source IDs:
- `D*` = direct documentation or PEP support
- `S*` = explicit synthesis from those direct sources
- `V*` = version gates
- `R*` = rule coverage rows

Use [references/patterns.md](references/patterns.md) only as a quick lookup sheet. The main skill and the source map are the normative files.
Use [references/contexts.md](references/contexts.md) when the task is shaped by modules, scripts, tests, notebooks, CLIs, libraries, or APIs.
Use [references/extended-examples.md](references/extended-examples.md) when you need full GOOD/BAD examples for `R10` through `R14`.

Treat "Pythonic" as readable, explicit code that uses Python's built-in iteration model, truthiness rules, protocols, and standard library instead of imported foreign ceremony. (Sources: D1, D10, D12, D13, S3)

## Context Routes

Load the matching section in `references/contexts.md` when the task is centered on one of these code shapes:
- modules
- scripts
- tests
- notebooks
- CLIs
- libraries
- APIs

## Rules

### R0. Version-gate every recommendation. (Sources: V1, V2, V3, V4, V5, S9)

Do not recommend syntax or stdlib features newer than the repo can run.

GOOD:

```python
# repo supports Python >= 3.10
def parse_age(value: str) -> int | None:
    ...

# repo supports Python >= 3.10
pairs = list(zip(left, right, strict=True))
```

BAD:

```python
# repo supports Python 3.9
def parse_age(value: str) -> int | None:
    ...

# repo supports Python 3.9
pairs = list(zip(left, right, strict=True))
```

### R1. Iterate over values, not indexes, unless the index itself is the subject. (Sources: D8, D9, D10, S1)

Prefer direct iteration, `enumerate()`, `zip(..., strict=True)` for equal-length invariants, and `mapping.items()` when you need both key and value.

GOOD:

```python
# direct iteration
for line in lines:
    print(line)

# enumerate when you need both index and value
for line_no, line in enumerate(lines, start=1):
    print(line_no, line)

# zip equal-length sequences
for before, after in zip(old_prices, new_prices, strict=True):
    compare(before, after)

# key and value together
for name, score in scores.items():
    print(name, score)
```

BAD:

```python
# indexing when the index is not the subject
for i in range(len(lines)):
    print(lines[i])

# manual counter
line_no = 1
for line in lines:
    print(line_no, line)
    line_no += 1

# parallel indexing
for i in range(len(old_prices)):
    compare(old_prices[i], new_prices[i])

# iterate keys, then re-index for values
for name in scores:
    print(name, scores[name])
```

### R2. Use comprehensions for result creation, not side effects or dense control flow. (Sources: D11, S4)

Prefer comprehensions for simple transforms and filters. Switch back to a loop when the logic branches heavily, mutates state, or becomes harder to scan.

GOOD:

```python
# simple result creation
normalized = [name.strip().lower() for name in names if name]

# when logic branches, use a loop
normalized = []
for name in names:
    if not name:
        continue
    cleaned = name.strip().lower()
    if cleaned in banned:
        continue
    normalized.append(cleaned)
```

BAD:

```python
# side-effect comprehension
[results.append(name.strip().lower()) for name in names if name]

# dense comprehension that hides branching
normalized = [
    name.strip().lower()
    for name in names
    if name
    if name.strip().lower() not in banned
]
```

### R3. Use truthiness for emptiness, but use `is None` for sentinel checks. (Sources: D2, D7, S2)

Empty sequences and collections are false. `None` is a separate sentinel and should be tested with identity.

GOOD:

```python
# emptiness
if not names:
    names = ["anonymous"]

# sentinel
if timeout is None:
    timeout = default_timeout

# explicit None identity
if value is not None:
    print(value)
```

BAD:

```python
# manual emptiness test
if len(names) == 0:
    names = ["anonymous"]

# conflates None with 0, '', [], and False
if not timeout:
    timeout = default_timeout

# equality instead of identity
if value != None:
    print(value)
```

### R4. Prefer EAFP when the action is the check, and catch the narrowest expected exception. (Sources: D3, D12)

Do not pre-check then immediately perform the same lookup or operation. Do not widen exceptions beyond the failure you expect.

GOOD:

```python
# lookup where absence is normal
try:
    user = users[user_id]
except KeyError:
    user = create_guest_user()

# parse where one failure is expected
try:
    age = int(raw_age)
except ValueError:
    age = None
```

BAD:

```python
# pre-check then lookup
if user_id in users:
    user = users[user_id]
else:
    user = create_guest_user()

# catches far more than the intended parse failure
try:
    age = int(raw_age)
except Exception:
    age = None
```

### R5. Choose the mapping idiom that matches the intent. (Sources: D16, D17, D29, D12, S5)

Use `dict.get()` for optional lookup with a default, `Counter` when the main job is counting, `setdefault()` for one-off insert-on-first-use, `defaultdict()` for repeated grouping or accumulation, and R4-style EAFP when absence is exceptional.

GOOD:

```python
# optional lookup with default
theme = config.get("theme", "light")

# counting
from collections import Counter

word_counts = Counter(words)

# one-off insert on first use
groups.setdefault(color, []).append(item)

# repeated grouping
from collections import defaultdict

groups = defaultdict(list)
for color, item in pairs:
    groups[color].append(item)
```

BAD:

```python
# manual counting
word_counts = {}
for word in words:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1

# manual defaulting
if "theme" in config:
    theme = config["theme"]
else:
    theme = "light"

# manual insert on first use
if color not in groups:
    groups[color] = []
groups[color].append(item)

# repeated manual grouping
groups = {}
for color, item in pairs:
    if color not in groups:
        groups[color] = []
    groups[color].append(item)
```

### R6. Use the standard library's resource, path, and string helpers. (Sources: D5, D6, D14, D15)

Prefer `with` for resources, `pathlib.Path` for filesystem paths, `''.join(...)` for repeated assembly, and `startswith()` or `endswith()` for prefix or suffix checks.

GOOD:

```python
# context manager for resources
with open("report.txt", encoding="utf-8") as f:
    text = f.read()

# Path objects for filesystem work
from pathlib import Path
path = Path("data") / "report.json"

# join pieces into one string
csv_line = ",".join(fields)

# helper for suffix checks
if filename.endswith(".csv"):
    load_csv(filename)
```

BAD:

```python
# manual open and close
f = open("report.txt", encoding="utf-8")
text = f.read()
f.close()

# raw string path assembly
path = "data" + "/" + "report.json"

# repeated concatenation
csv_line = ""
for i, field in enumerate(fields):
    if i:
        csv_line += ","
    csv_line += field

# slice-based suffix check
if filename[-4:] == ".csv":
    load_csv(filename)
```

### R7. Remember that in-place mutators return `None`. (Sources: D28)

If you need mutation, mutate clearly. If you need a transformed value, build one explicitly.

GOOD:

```python
# mutate in place
names.sort()

# another mutator
data.update(extra)
```

BAD:

```python
# mutator result is None
names = names.sort()

# mutator result is None
data = data.update(extra)
```

### R8. Prefer protocols and exact intent over rigid type checks. (Sources: D13, D23, D27, S3)

If behavior matters, code to the protocol. When you must type-check, use `isinstance()` instead of `type(x) is T` unless exact class identity is the real requirement.

GOOD:

```python
# protocol-friendly code
def total(values):
    return sum(values)

# use isinstance when an actual runtime check is required
if isinstance(value, (str, bytes)):
    handle_text_like(value)
```

BAD:

```python
# exact-type gate when any iterable would work
def total(values):
    if type(values) is not list:
        raise TypeError("list required")
    return sum(values)

# exact-type comparisons instead of isinstance
if type(value) is str or type(value) is bytes:
    handle_text_like(value)
```

### R9. Use plain attributes for plain data. Use `property()` only for managed attributes. Use `@dataclass` for record-like classes. (Sources: D24, D25, D26, S6)

Do not write Java-style getter and setter layers around plain state. Add a property only when attribute access needs behavior such as validation. Use `@dataclass` when the class mainly carries named fields.

GOOD:

```python
# plain data stays plain
class User:
    def __init__(self, name):
        self.name = name

# property only when the attribute is managed
class Celsius:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value < -273.15:
            raise ValueError("below absolute zero")
        self._value = new_value

# dataclass for record-like state
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
```

BAD:

```python
# getter and setter ceremony around plain data
class User:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

# Java-style accessor naming for managed attributes
class Celsius:
    def __init__(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def set_value(self, new_value):
        if new_value < -273.15:
            raise ValueError("below absolute zero")
        self._value = new_value

# manual record boilerplate
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x!r}, y={self.y!r})"

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
```

### R10. Make call sites readable with keyword-only parameters when names matter. (Sources: D19, S7)

When argument names carry meaning, force them at the call site. See `references/extended-examples.md#r10`.

### R11. Never use mutable default arguments. (Sources: D18)

Default values are evaluated once. Use `None`, then create the mutable object inside. See `references/extended-examples.md#r11`.

### R12. Keep typing modern and honest. (Sources: D21, D22, V1, V2)

Annotations are for readers and tools, not runtime enforcement. On supported Python, use built-in generics and `collections.abc` interfaces when the function accepts any object with that protocol. See `references/extended-examples.md#r12`.

### R13. Use `match` when structure is the subject, not as a decorative `if` chain. (Sources: D20, V3, S8)

Keep ordinary `if` and `elif` for simple scalar branching. Reach for `match` when you are dispatching on literals, mappings, sequences, or attribute patterns, and the structure itself is the subject. See `references/extended-examples.md#r13`.

### R14. Avoid wildcard imports. (Sources: D4)

Wildcard imports hide where names came from and make code harder to read and analyze. See `references/extended-examples.md#r14`.

### R15. Prefer f-strings for ordinary inline interpolation on supported Python. (Sources: D30, V5, S11)

On supported Python, prefer f-strings for straightforward inline interpolation. Keep other formatting styles when API semantics, deferred formatting, or translation workflows make them the better fit.

GOOD:

```python
# repo supports Python >= 3.6
message = f"Hello, {name}! You have {count} messages."

# readable formatting spec
summary = f"{ratio:.2%} complete"
```

BAD:

```python
message = "Hello, %s! You have %d messages." % (name, count)

message = "Hello, {}! You have {} messages.".format(name, count)
```

## Review Use

When calling something "not Pythonic", cite the rule ID and the source IDs that support it. Example: `R3 (D2, D7, S2)`.

If a point is only local taste and you cannot tie it to one of the rules above, do not present it as a Python fact.
