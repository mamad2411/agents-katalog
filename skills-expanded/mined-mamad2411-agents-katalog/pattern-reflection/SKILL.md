---
name: pattern-reflection
description: Implement multi-turn self-critique loops where a critic agent evaluates generator output against verifiable criteria to refine results.
metadata:
  category: agent-architecture
  tier: core
  chapter: 04
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Reflection & Self-Correction Pattern

## 1. Overview & Intent

Implement multi-turn self-critique loops where a critic agent evaluates generator output against verifiable criteria to refine results.

> **Intent & Scope:** Use for high-precision generation (code synthesis, mathematical proofs, translation, regulatory filings) where first-pass accuracy is insufficient.

---

## 2. Architectural Blueprint

```
[Prompt] --> [Generator] --> [Draft Output]
                 ^                 |
                 |                 v
          (Refinement) <--- [Critic / Verifier] --(Pass?)--> [Final Result]
```

---

## 3. Core Implementation Principles

- **Separate roles:** The critic agent should have dedicated critique instructions and a critical persona.\n- Ground critiques in external evidence (linters, test runners, AST parsers) rather than pure LLM self-bias.\n- Enforce a maximum iteration cap (typically 3–5 cycles) to prevent infinite refinement loops.\n- **Track progress delta:** terminate early if consecutive iterations produce diminishing score improvements.

---

## 4. Reference Implementation Pattern

```python
from pydantic import BaseModel

class CritiqueResult(BaseModel):
    is_valid: bool
    score: int  # 1-10
    critique: str
    actionable_fixes: list[str]

def reflection_loop(task: str, max_iterations: int = 3) -> str:
    draft = generator_agent.create_initial_draft(task)
    for iteration in range(max_iterations):
        critique = critic_agent.evaluate(task, draft, response_model=CritiqueResult)
        if critique.is_valid and critique.score >= 8:
            return draft
        draft = generator_agent.refine(draft, critique.critique, critique.actionable_fixes)
    return draft

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
