---
name: pattern-reasoning-engines
description: "Structure agent problem solving with explicit reasoning paradigms: Chain-of-Thought (CoT), Tree of Thoughts (ToT), and self-verifying code execution."
metadata:
  category: agent-architecture
  tier: enterprise
  chapter: 17
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Reasoning Engines Pattern

## 1. Overview & Intent

Structure agent problem solving with explicit reasoning paradigms: Chain-of-Thought (CoT), Tree of Thoughts (ToT), and self-verifying code execution.

> **Intent & Scope:** Use for complex symbolic logic, algorithm design, multi-constraint scheduling, and mathematical derivation.

---

## 2. Architectural Blueprint

```
[Complex Problem] --> [Generate Multiple Thought Branches]
                              |-- [Branch A: Strategy 1]
                              |-- [Branch B: Strategy 2]
                              +-- [Branch C: Strategy 3]
                                         |
                                         v
                         [State Evaluator / Verifier]
                                         |
                                         v
                            [Best Path Execution]
```

---

## 3. Core Implementation Principles

- **Mandate explicit scratchpads:** prompt the model to reason through constraints before declaring an answer.\n- Use external execution verifiers (Python interpreters) to validate intermediate mathematical reasoning.\n- **Explore alternative hypotheses:** sample multiple reasoning paths and choose via self-consistency or heuristic scoring.\n- **Detect circular reasoning:** interrupt agent loops when thought chains repeat without new inferences.

---

## 4. Reference Implementation Pattern

```python
def chain_of_thought_solve(problem: str, llm):
    cot_prompt = f"""Solve the following problem step by step.
Format your response as:
<thinking>
[Break down constraints, formulate steps, and verify calculations]
</thinking>
<solution>
[Final concise answer]
</solution>

Problem: {problem}"""
    return llm.generate(cot_prompt)

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
