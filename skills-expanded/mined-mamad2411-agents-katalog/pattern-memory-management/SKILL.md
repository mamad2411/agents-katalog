---
name: pattern-memory-management
description: "Implement tiered agent memory: short-term working context, sliding window buffers, episodic vector retrieval, and persistent key-value state."
metadata:
  category: agent-architecture
  tier: advanced
  chapter: 08
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Memory Management Pattern

## 1. Overview & Intent

Implement tiered agent memory: short-term working context, sliding window buffers, episodic vector retrieval, and persistent key-value state.

> **Intent & Scope:** Use when agents operate over long sessions, multiple user conversations, or require cross-session recall of facts and user preferences.

---

## 2. Architectural Blueprint

```
[Incoming Turn] ---> [Working Memory (In-Context)] <---> [Short-Term Buffer]
                             |                                    |
                             v                                    v
                     [Episodic Memory]                     [Persistent State]
                    (Vector / Semantic)                     (Key-Value / DB)
```

---

## 3. Core Implementation Principles

- **Tier memory cleanly:** distinction between working scratchpad, session chat history, and long-term storage.\n- **Summarize sliding windows:** periodically compress older dialogue turns to bound context tokens.\n- Extract semantic facts into key-value stores for deterministic retrieval.\n- Use vector indexes for fuzzy episodic recall, but ground mission-critical state in structured DBs.

---

## 4. Reference Implementation Pattern

```python
from typing import Dict, Any

class AgentMemoryStore:
    def __init__(self):
        self.working_scratchpad: Dict[str, Any] = {}
        self.session_history: list[Dict[str, str]] = []
        self.persistent_state: Dict[str, Any] = {}

    def update_state(self, key: str, value: Any):
        self.persistent_state[key] = value

    def compress_history(self, summarizer_llm, keep_last_n: int = 4):
        if len(self.session_history) > keep_last_n:
            to_compress = self.session_history[:-keep_last_n]
            summary = summarizer_llm.summarize(to_compress)
            self.session_history = [{"role": "system", "content": f"Prior context: {summary}"}] + self.session_history[-keep_last_n:]

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
