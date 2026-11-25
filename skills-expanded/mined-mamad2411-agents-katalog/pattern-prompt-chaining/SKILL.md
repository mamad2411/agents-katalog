---
name: pattern-prompt-chaining
description: Decompose complex workflows into sequential, single-responsibility prompt steps where the structured output of each stage feeds the next.
metadata:
  category: agent-architecture
  tier: core
  chapter: 01
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Prompt Chaining Pattern

## 1. Overview & Intent

Decompose complex workflows into sequential, single-responsibility prompt steps where the structured output of each stage feeds the next.

> **Intent & Scope:** Use when tasks are too complex for a single prompt or require intermediate validation, transformation, or schema enforcement between steps.

---

## 2. Architectural Blueprint

```
[User Input] --> [Stage 1: Extraction] --> (Validated Schema)
                     --> [Stage 2: Transformation] --> (Intermediate JSON)
                     --> [Stage 3: Synthesis / Output] --> [Final Result]
```

---

## 3. Core Implementation Principles

- **Decompose by responsibility:** Each prompt in the chain should do exactly one thing well.\n- Enforce strict intermediate schemas (JSON / Pydantic) to prevent drift.\n- **Fail-fast error propagation:** If step N fails schema validation, retry or exit before invoking step N+1.\n- **Minimize state carried forward:** Pass only necessary extracted fields to downstream stages.

---

## 4. Reference Implementation Pattern

```python
import json
from typing import Dict, Any
from pydantic import BaseModel, Field

class ExtractedEntities(BaseModel):
    user_intent: str = Field(..., description="Primary user intent")
    entities: list[str] = Field(default_factory=list, description="Key named entities")

class FormattedReport(BaseModel):
    summary: str
    action_items: list[str]

def prompt_chain_pipeline(user_query: str, llm_client) -> FormattedReport:
    # Stage 1: Entity Extraction & Intent Classification
    prompt_1 = f"Analyze the following input and extract intent and key entities in JSON:\n{user_query}"
    resp_1 = llm_client.generate(prompt_1, response_format=ExtractedEntities)
    stage1_data = ExtractedEntities.model_validate_json(resp_1)
    
    # Stage 2: Synthesis and Action Plan
    prompt_2 = f"Generate an executive action plan based on:\nIntent: {stage1_data.user_intent}\nEntities: {stage1_data.entities}"
    resp_2 = llm_client.generate(prompt_2, response_format=FormattedReport)
    return FormattedReport.model_validate_json(resp_2)

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
