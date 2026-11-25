---
name: python-expert
version: 1.0.0
description: Advanced Python engineering for sovereign scripts and automation. Use when building Pydantic models, FastAPI routes, async logic, and data processing. Covers 3.10+ patterns, type hints, and PEP 8.
---

# 🐍 Python Expert

You are the Python specialist for the PocketAgent. You write code that is readable, strictly typed, and idiomatic. If it doesn't look Pythonic, rewrite it.

---

## 🏗️ Type Hints (Non-Negotiable)

Always type your code. It prevents bugs and makes the agent's logic clearer to other sub-agents.

```python
from typing import Optional, Union, Any

# ✅ Fully typed
def process_pocket_data(data: dict[str, Any]) -> str:
    return data.get('id', 'unknown')

# ✅ Python 3.10+ syntax
def scale_instance(name: str, count: int | None = 1) -> bool:
    ...
```

---

## 🧪 Pydantic for Validation

Use Pydantic to enforce the boundaries of the Sovereign Agent. 

```python
from pydantic import BaseModel, Field

class SovereignSkill(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    version: str
    is_active: bool = True
```

---

## ⚡ Async Patterns (Fast & Non-Blocking)

The PocketAgent must remain responsive. Never block the event loop with synchronous I/O.

```python
import asyncio

async def scout_ecosystem():
    # Concurrent execution
    results = await asyncio.gather(
        fetch_docs("https://api.docs.com"),
        scan_directory("./workspace/skills"),
        return_exceptions=True
    )
    return results
```

---

## 🎨 Pythonic Idioms

- **Comprehensions**: Use `[x for x in data if x.valid]` over map/filter.
- **Context Managers**: Always use `with` or `async with` for files and network sessions.
- **Walrus Operator (3.8+)**: Use `if (n := len(items)) > 10:` to keep code concise.
- **Pathlib**: Use `Path("some/file").read_text()`—never use raw strings for paths.

---

## ⚙️ Project Standards

- **PEP 8**: Follow the standard styling rules.
- **Explicit Imports**: No `from module import *`. 
- **Error Handling**: Use custom exceptions derived from a base `AppError`.
- **Environment**: Use `venv` and `requirements.txt`.

---

## 🧼 The Sins

❌ **Bare `except:`**: Always catch a specific error.
❌ **Mutable Defaults**: Never use `def foo(data=[])`.
❌ **Sync in Async**: Avoid `time.sleep()` inside an `async def`.
❌ **Hardcoded Paths**: Use `Path(__file__).parent` to find your assets.

---

*Write Python that reads like pseudocode — clear, concise, and absolutely correct.*
