---
name: pattern-tool-use
description: Equip LLMs with deterministic execution interfaces, typed parameter schemas, sandboxed execution, and structured error feedback.
metadata:
  category: agent-architecture
  tier: core
  chapter: 05
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Tool Use Pattern

## 1. Overview & Intent

Equip LLMs with deterministic execution interfaces, typed parameter schemas, sandboxed execution, and structured error feedback.

> **Intent & Scope:** Use when models need external capabilities: real-time data, computational math, disk I/O, database access, or remote API execution.

---

## 2. Architectural Blueprint

```
[Agent] --(Tool Call: args)--> [Schema Validator] --(Valid)--> [Executor / Sandbox]
   ^                                                                 |
   +------------------(Observation / Tool Output / Error)------------+
```

---

## 3. Core Implementation Principles

- Use strict schema typing (Pydantic / JSON Schema) for all tool parameters.\n- Provide rich docstrings detailing when to call the tool, argument types, and side effects.\n- Sanitize tool errors and return them to the model context so it can self-repair broken arguments.\n- Sandbox high-risk tools (file system writes, shell commands, database updates).

---

## 4. Reference Implementation Pattern

```python
from pydantic import BaseModel, Field

class CalculatorArgs(BaseModel):
    expression: str = Field(..., description="Mathematical expression to evaluate, e.g. '(14 * 2.5) / 10'")

def calculate(args: CalculatorArgs) -> str:
    allowed_chars = set("0123456789+-*/(). ")
    if not set(args.expression).issubset(allowed_chars):
        return "Error: Expression contains forbidden characters."
    try:
        result = eval(args.expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Execution Error: {e}"

```

---

## 5. Verification & Failure Modes

- **Verification Checklist:**
  - [ ] Inputs are validated via strict typed schemas before processing.
  - [ ] Error cascades and timeouts are bounded.
  - [ ] Intermediate artifacts and trace telemetry are logged.
  - [ ] Verification criteria are objectively evaluated before task completion.

- **Common Failure Modes:**
  - **Cascading Hallucination:** Unchecked intermediate model drift polluting downstream stages.
  - **Infinite Looping:** Lack of maximum iteration guards or convergence detection.
  - **Context Bloat:** Carrying unpruned conversational history or verbose tool errors across turns.
