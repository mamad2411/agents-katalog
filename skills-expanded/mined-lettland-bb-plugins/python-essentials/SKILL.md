---
name: python-essentials
description: Use when writing any Python — naming, typing, layout, async, packaging, the rules you don't break.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [python]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [python-testing, python-fastapi, python-django]
---

# Python Essentials

**Iron Law: annotate every public boundary, run `mypy --strict` or `pyright`, never `except:` bare. No `Any` as an escape hatch.**

**Versions:** LTS-equivalent `3.11` (Debian bookworm), `3.12` (Debian trixie) · Current `3.14` · Next `3.15` — _3.13 added free-threaded build + PEP 695 generic syntax + PEP 744 JIT; 3.14 added t-strings + PEP 649 deferred annotations. Pin via `requires-python` and `.python-version`._

## Naming (non-negotiable)

| Subject                  | Rule                                  | OK             | Not                      |
| ------------------------ | ------------------------------------- | -------------- | ------------------------ |
| Functions, vars, modules | `snake_case`                          | `get_user`     | `getUser`                |
| Classes                  | `PascalCase`                          | `OrderService` | `order_service`          |
| Constants                | `UPPER_SNAKE`                         | `MAX_RETRIES`  | `maxRetries`             |
| Internal                 | `_leading_underscore`                 | `_cache`       | `__cache` (name-mangles) |
| Reserved                 | `__dunder__` — language only          | `__init__`     | inventing `__custom__`   |
| Modules                  | short, lowercase, no `_` if avoidable | `auth`         | `auth_module`            |

## File layout

```
your-project/
├── pyproject.toml
├── src/yourpkg/        # src layout — forces install before tests find it
│   ├── __init__.py     # re-exports public API
│   └── _internal/      # everything else
├── tests/
└── .python-version
```

One module per coherent concept. Package when 3+ related modules. `__init__.py` re-exports the public API; everything else is `_private.py` or under `_internal/`.

## Pythonic vs Java-with-`def`

| Pythonic                          | Not                                        |
| --------------------------------- | ------------------------------------------ |
| `for item in collection:`         | `for i in range(len(collection)):`         |
| `for i, item in enumerate(coll):` | manual counter                             |
| `if x is None:`                   | `if x == None:`                            |
| `with open(p) as f:`              | `f = open(p); try: ... finally: f.close()` |
| `dict.get(key, default)`          | `key in d and d[key] or default`           |
| comprehensions                    | manual loop + `.append()`                  |
| `pathlib.Path`                    | `os.path.join`                             |
| `match`/`case` (3.10+)            | giant `if/elif` on type                    |
| `dataclass` / `BaseModel`         | bare `dict` as DTO                         |

## Typing — annotate everything at module boundaries

Use lowercase generics (3.9+): `list[int]`, `dict[str, int]`. The `typing.List` form is dead.

| Need                 | Type                           |
| -------------------- | ------------------------------ |
| Maybe `None`         | `T \| None` (3.10+)            |
| Union                | `T \| U`                       |
| Callable             | `Callable[[Arg], Ret]`         |
| Dict with known keys | `TypedDict`                    |
| Structural (duck)    | `Protocol`                     |
| Compile-time literal | `Literal["a", "b"]`            |
| Branded type         | `NewType("UserId", int)`       |
| Self-referential     | `Self` (3.11+)                 |
| Generic              | `def f[T](x: T) -> T:` (3.12+) |

**Strict mode is the default.** `mypy --strict` or `pyright`. Adopt incrementally with `# mypy: strict` per-module on legacy code. `Any` is forbidden in new code — narrow with `cast`, `assert isinstance`, or a `Protocol`.

```python
from typing import Protocol

class Persistable(Protocol):
    def save(self) -> None: ...

def persist(obj: Persistable) -> None:  # any matching class qualifies, no inheritance
    obj.save()
```

## Async essentials

Async is for I/O-bound concurrency. Not for CPU work (use a process pool), not for one-call-at-a-time (use sync).

```python
async with asyncio.TaskGroup() as tg:        # 3.11+ — prefer over gather()
    tg.create_task(fetch("a"))
    tg.create_task(fetch("b"))
# If either raised, group raises ExceptionGroup; siblings cancelled.
```

| Need                 | Use                                                                     |
| -------------------- | ----------------------------------------------------------------------- |
| Concurrent tasks     | `asyncio.TaskGroup` (3.11+); `gather` only when partial failure is fine |
| Run blocking code    | `await asyncio.to_thread(fn, *args)`                                    |
| Timeout              | `async with asyncio.timeout(5):` (3.11+)                                |
| Cancellable resource | `try/finally` or `async with`                                           |
| Backpressure         | `asyncio.Semaphore(N)`                                                  |
| Sleep                | `asyncio.sleep` — never `time.sleep`                                    |
| HTTP                 | `httpx` / `aiohttp` — never `requests`                                  |
| Lock                 | `asyncio.Lock` — never `threading.Lock`                                 |

`asyncio.run()` belongs in `main`, not libraries. Let the app drive the loop.

## Packaging — `pyproject.toml` only

`setup.py` is dead. Pick `uv` for new projects. Use **src layout** for libraries.

```toml
[project]
name = "yourpkg"
version = "0.1.0"
# If you use PEP 695 generic syntax (def f[T](x: T) -> T), bump this floor to >=3.12.
# Libraries should pin to the lowest version you actually test; apps can pin to current.
requires-python = ">=3.12"
dependencies = ["httpx>=0.27", "pydantic>=2"]

[project.optional-dependencies]
dev = ["pytest>=8", "mypy>=1.10", "ruff>=0.6"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
strict = true
```

| Tool                        | When                                                               |
| --------------------------- | ------------------------------------------------------------------ |
| `uv`                        | Default for new projects — fast, lockfile, drop-in                 |
| `ruff`                      | Lint AND format. Don't run `black` + `flake8` + `isort` separately |
| `pytest`                    | Test runner. `pytest-asyncio` for async                            |
| `mypy --strict` / `pyright` | Type check                                                         |
| poetry                      | Only if team is already on it                                      |

**Apps**: pin exact (`uv lock`). **Libraries**: range-pin (`httpx>=0.27,<1`). Always commit the lockfile.

## Anti-patterns

- Mutable default args: `def f(x=[]):` — list shared across calls. Use `x=None` and assign inside.
- `from x import *` outside `__init__.py`
- Bare `except:` or `except Exception:` swallowed — at minimum re-raise or log with context
- `eval` / `exec` on user input — arbitrary code execution
- Unpickling untrusted bytes — `pickle` deserialization is arbitrary code execution by design; use JSON or msgpack for untrusted input
- `yaml.load(s)` without a Loader — code execution. ALWAYS `yaml.safe_load(s)`
- `subprocess.run(cmd, shell=True)` with user input — shell injection. Pass a list (`shell=False`) so the kernel resolves args directly
- `print()` in production — use `logging` or `structlog`
- String-concatenating SQL — parameterize, always
- `global` inside a function — pass the value or use a class
- `os.path` over `pathlib`
- `Any` as the escape hatch
- `# type: ignore` without a comment explaining why
- `setup.py` in new projects
- A class with only `__init__` and one method — that's a function
- Late binding in lambdas in loops: `[lambda: i for i in range(3)]` — all return 2. Bind: `[lambda i=i: ...]`

## Red flags

| Thought                             | Reality                                           |
| ----------------------------------- | ------------------------------------------------- |
| "Types slow me down"                | They surface bugs you'd hit at 3am instead.       |
| "Duck typing is the Python way"     | `Protocol` gives you ducks AND static checks.     |
| "I'll add types later"              | Later = never. Add as you go.                     |
| "Just one global"                   | Two months later there are forty. Pass it in.     |
| "I'll catch Exception just in case" | You swallowed the bug. Catch what you handle.     |
| "asyncio.sleep(0) to yield"         | Code is structured wrong. Restructure.            |
| "It's just a script"                | Scripts that survive Friday afternoon need types. |

## Hand-off

For testing: `Skill(devkit:python-testing)`. For FastAPI: `Skill(devkit:python-fastapi)`. For Django: `Skill(devkit:python-django)`.
