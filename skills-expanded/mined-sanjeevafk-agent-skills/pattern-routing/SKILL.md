---
name: pattern-routing
description: Dynamically route requests to specialized models, prompts, tools, or subagents based on intent classification and complexity grading.
metadata:
  category: agent-architecture
  tier: core
  chapter: 02
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Routing Pattern

## 1. Overview & Intent

Dynamically route requests to specialized models, prompts, tools, or subagents based on intent classification and complexity grading.

> **Intent & Scope:** Use when requests span multiple disparate domains, skill sets, or cost/latency tiers (e.g. routing simple FAQs to flash models and deep math to pro models).

---

## 2. Architectural Blueprint

```
[User Query] --> [Classifier / Router] 
                   |-- (Technical) --> [Code Specialist Agent]
                   |-- (Creative)  --> [Writing Specialist Agent]
                   |-- (Simple)    --> [Fast/Cheap Small LLM]
                   +-- (Complex)   --> [Deep Reasoning Model]
```

---

## 3. Core Implementation Principles

- Use fast, low-cost classifiers (Flash models or embeddings) to make routing decisions in <100ms.\n- Provide explicit routing criteria and distinct boundary definitions for each handler.\n- Always maintain a robust fallback route for ambiguous or multi-domain queries.\n- **Consider tiered routing:** first classify domain, then classify complexity level.

---

## 4. Reference Implementation Pattern

```python
from enum import Enum
from pydantic import BaseModel

class RouteDestination(str, Enum):
    DATABASE = "database"
    REASONING = "deep_reasoning"
    FALLBACK = "general_support"

class RouterDecision(BaseModel):
    route: RouteDestination
    confidence: float
    rationale: str

def route_query(query: str, classifier_llm) -> str:
    prompt = f"Categorize the query into DATABASE, REASONING, or FALLBACK:\nQuery: {query}"
    decision = classifier_llm.classify(prompt, response_model=RouterDecision)
    
    if decision.route == RouteDestination.DATABASE:
        return execute_sql_pipeline(query)
    elif decision.route == RouteDestination.REASONING:
        return execute_chain_of_thought(query)
    return execute_general_llm(query)

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
