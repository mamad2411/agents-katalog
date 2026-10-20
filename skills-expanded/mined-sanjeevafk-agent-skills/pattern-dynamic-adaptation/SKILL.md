---
name: pattern-dynamic-adaptation
description: Enable agents to adapt system prompts, heuristics, and tool parameters dynamically based on environmental feedback and error signals.
metadata:
  category: agent-architecture
  tier: advanced
  chapter: 09
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Dynamic Adaptation & Learning Pattern

## 1. Overview & Intent

Enable agents to adapt system prompts, heuristics, and tool parameters dynamically based on environmental feedback and error signals.

> **Intent & Scope:** Use for self-optimizing pipelines (e.g. OpenEvolve, prompt mutation, auto-tuning prompts) that improve execution accuracy over successive runs.

---

## 2. Architectural Blueprint

```
[Task Execution] --> [Outcome Evaluator] --> [Performance Signal]
       ^                                            |
       +------ [Prompt / Heuristic Mutator] <-------+
```

---

## 3. Core Implementation Principles

- **Isolate tunable parameters:** separate core business logic from adaptable prompts and thresholds.\n- **Record longitudinal traces:** store prompt versions alongside outcome scores.\n- **Use genetic or reflective mutation:** generate variant prompts and benchmark against golden validation sets.\n- **Rollback guardrails:** reject mutations that degrade baseline performance.

---

## 4. Reference Implementation Pattern

```python
class AdaptivePromptEngine:
    def __init__(self, base_prompt: str):
        self.current_prompt = base_prompt
        self.version = 1

    def adapt_from_failure(self, failed_input: str, error_trace: str, optimizer_llm):
        mutation_prompt = f"""Given prompt v{self.version}, which failed on input: {failed_input}
Error: {error_trace}
Refine the system prompt instructions to handle this edge case without regressing."""
        new_prompt = optimizer_llm.generate(mutation_prompt)
        self.current_prompt = new_prompt
        self.version += 1

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
