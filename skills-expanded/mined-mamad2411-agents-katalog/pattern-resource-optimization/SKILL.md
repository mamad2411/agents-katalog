---
name: pattern-resource-optimization
description: Optimize token usage, wall-clock latency, and financial costs via prompt caching, context pruning, model cascades, and rate throttling.
metadata:
  category: agent-architecture
  tier: enterprise
  chapter: 16
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Resource-Aware Optimization Pattern

## 1. Overview & Intent

Optimize token usage, wall-clock latency, and financial costs via prompt caching, context pruning, model cascades, and rate throttling.

> **Intent & Scope:** Use in high-throughput enterprise deployments where LLM API costs and response latency dominate operational overhead.

---

## 2. Architectural Blueprint

```
[Request] --> [Cache Check (Prompt Caching)] --(Hit)--> [Immediate Response]
                     | (Miss)
                     v
             [Model Cascade Router]
             |-- (Cheap Query)   --> [Flash / Haiku / Small Model]
             +-- (Complex Query) --> [Pro / Opus / Deep Reasoning Model]
```

---

## 3. Core Implementation Principles

- **Leverage prompt caching:** place static instructions and documents at the head of system prompts.\n- **Cascade models:** resolve 70%+ of queries with fast, small models before invoking frontier reasoning engines.\n- **Prune history aggressively:** trim redundant whitespaces, logs, and older turns from conversational context.\n- **Implement rate-limit smoothing:** queue requests with token-bucket algorithms to prevent provider throttling.

---

## 4. Reference Implementation Pattern

```python
class ModelCascade:
    def __init__(self, cheap_client, frontier_client):
        self.cheap_client = cheap_client
        self.frontier_client = frontier_client

    def execute(self, prompt: str, difficulty_threshold: float = 0.7) -> str:
        # Evaluate complexity cheaply
        complexity = self.cheap_client.score_complexity(prompt)
        if complexity < difficulty_threshold:
            return self.cheap_client.generate(prompt)
        return self.frontier_client.generate(prompt)

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
