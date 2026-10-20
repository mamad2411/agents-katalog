---
name: guardrails-ai
description: "Guardrails AI — LLM output validation and guardrails. Define guardrails as XML/JSON specs, validate outputs against structural and semantic constraints, correct/retry on failure, and audit model behavior."
tags: [guardrails-ai, llm-safety, output-validation, guardrails, governance, python, zorai]
---
## Overview

Guardrails AI provides a guardrails framework for LLM applications with structured output validation, type safety, retry/reprompt logic, and risk management. Uses RAIL (Reliable AI Markup Language) specs or Pydantic models.

## Installation

```bash
uv pip install guardrails-ai
```

## Basic Guard

```python
import guardrails as gd

rail_spec = (
    '<rail version="0.1">'
    '<output>'
    '  <string name="summary" description="Brief summary" format="length: 1-100"/>'
    '  <integer name="sentiment" format="valid-choices: {1, 0, -1}"/>'
    '</output>'
    '<prompt>'
    'Summarize this text: {{text}}'
    '</prompt>'
    '</rail>'
)

guard = gd.Guard.from_rail_string(rail_spec)
raw, validated = guard(text="I loved this movie!")
print(validated)  # {"summary": "...", "sentiment": 1}
```

## Pydantic Guard

```python
from pydantic import BaseModel
from guardrails import Guard

class Extraction(BaseModel):
    name: str
    age: int = 0

guard = Guard.from_pydantic(Extraction)
result = guard("John is 25 years old")
```

## References
- [Guardrails AI docs](https://docs.guardrailsai.com/)
- [Guardrails GitHub](https://github.com/guardrails-ai/guardrails)