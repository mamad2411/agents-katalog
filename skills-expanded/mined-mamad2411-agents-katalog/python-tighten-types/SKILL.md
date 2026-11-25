---
name: python-tighten-types
description: Systematically review Python source files and tighten type annotations. Finds missing class attribute annotations, replaces loose dicts with Pydantic models, adds overloads, and removes redundant in-body annotations.
user-invocable: true
license: MIT
compatibility: Designed for Claude Code or similar AI coding agents, and for projects using Python.
metadata:
  author: honnibal
  version: "1.0.0"
  openclaw:
    emoji: "\U0001F3AD"
    homepage: https://github.com/honnibal/claude-skills
---

# Tighten Python Type Annotations

Systematically review Python source files, identify weak or missing type annotations, and propose precise fixes.

## Scope

- If the user names specific files or directories, scope work to those.
- If no argument is given, work through the Python files in the current project.
- For large codebases, ask the user which modules to start with.

## Workflow

1. **Survey** — Glob for `*.py` files in scope. Read each file. Build a mental model of the module's types before proposing changes.
2. **Analyse** — For each file, apply the checklist below. Collect all findings before editing so you can see cross-cutting patterns.
3. **Edit** — Make changes file by file. After editing a file, briefly summarize what changed and why.
4. **Verify** — Run the project's type checker after editing. Report any new errors introduced and fix them.

## Checklist

### 1. Missing class attribute annotations

```python
# Before
class Pipeline:
    def __init__(self, nlp, name):
        self.nlp = nlp
        self.name = name
        self._cache = {}

# After
class Pipeline:
    nlp: Language
    name: str
    _cache: dict[str, Any]

    def __init__(self, nlp: Language, name: str) -> None:
        self.nlp = nlp
        self.name = name
        self._cache = {}
```

### 2. Import types from third-party libraries

Replace vague annotations with concrete library types:

- Pydantic: `BaseModel`, `Field`, `ConfigDict`
- FastAPI / Starlette: `Request`, `Response`, `JSONResponse`
- PyTorch: `Tensor`, `Module`, `nn.Parameter`
- numpy: `np.ndarray`, `np.floating`, `np.integer`

Use `TYPE_CHECKING` imports to avoid runtime import cycles:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.language import Language
```

### 3. Structured dicts → Pydantic models (or TypedDicts)

Look for dictionaries constructed, passed around, or destructured with an assumed set of keys.

**Signals:** literal string keys used consistently, multiple functions accepting/returning same dict shape, a function building a dict incrementally then returning it.

**Choosing:** Prefer `BaseModel` when the dict crosses a system boundary (API, config, serialisation). Prefer `TypedDict` for internal data structures never validated or serialised.

### 4. `@overload` for narrowable unions

```python
# Before
def load(path: str, as_bytes: bool = False) -> str | bytes: ...

# After
@overload
def load(path: str, as_bytes: Literal[False] = ...) -> str: ...
@overload
def load(path: str, as_bytes: Literal[True]) -> bytes: ...
def load(path: str, as_bytes: bool = False) -> str | bytes: ...
```

### 5. Redundant in-body type annotations

Type annotations inside function bodies that compensate for loose types upstream. Investigate and fix the root cause.

### 6. Style modernisation

- Replace `Optional[X]` with `X | None` (Python 3.10+)
- Replace `typing.List`, `typing.Dict` with built-in generics
- Add `-> None` return annotations to methods that lack them
- Use `Self` (from `typing` in 3.11+ or `typing_extensions`)

## Critical Rules

- Read before editing. Never propose type changes to code you haven't read.
- Don't break runtime behaviour. Pydantic model introductions change runtime behaviour.
- Preserve public API compatibility. Changing `dict` to `SomeModel` is a breaking change.
- Run the type checker after changes. Don't introduce new errors.
- Ask when uncertain about whether a dict should become a model or TypedDict.

## Cross-References

- `python-code-quality` — mypy configuration, type hints patterns
- `python-documentation` — docstring conventions
