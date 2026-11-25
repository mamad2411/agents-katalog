---
name: code_execution
description: Run Python code, scripts, calculations, and data processing
triggers: [calculate, python, script, code, run, execute, math, matplotlib, pandas, посчитай, скрипт, код]
tools: [code_interpreter]
platform: all
---

## Code execution

Use the code interpreter (sandboxed Python).

### Simple math

```python
result = 2 ** 10
print(f"2^10 = {result}")
```

### Data handling

```python
import json
data = {"name": "test", "values": [1, 2, 3]}
print(json.dumps(data, indent=2))
```

### Commonly allowed modules (safe mode)

- `math`, `statistics`
- `json`
- `re`
- `datetime`
- `collections`
- `itertools`, `functools`
- `random`

### Rules

1. Use `code_interpreter` for math and in-sandbox data work.
2. Use `shell` for filesystem operations on the host.
3. Imports are restricted — only allowed modules work.
4. Always `print()` results; otherwise output may be empty.
5. Prefer one coherent code block for multi-step logic.
