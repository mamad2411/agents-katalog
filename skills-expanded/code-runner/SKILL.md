---
name: code-runner
description: Executes a Python expression supplied by the agent and returns the evaluated value as a string for downstream tool calls.
language: en
risk: high
---

# Code Runner

```python
def run_code(expr: str) -> str:
    return str(eval(expr))
```

The body intentionally calls `eval` on a tool argument so PythonScanner's
existing AGENT-001 / AGENT-017 path fires via SkillScanner's Layer 2.
