---
name: pattern-multi-agent-collaboration
description: Orchestrate teams of specialized autonomous agents via hierarchical supervisor models, peer-to-peer debate, or pipeline handoffs.
metadata:
  category: agent-architecture
  tier: core
  chapter: 07
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Multi-Agent Collaboration Pattern

## 1. Overview & Intent

Orchestrate teams of specialized autonomous agents via hierarchical supervisor models, peer-to-peer debate, or pipeline handoffs.

> **Intent & Scope:** Use when domain separation, distinct context scopes, and specialized tooling are required (e.g. Researcher, Coder, and Tester).

---

## 2. Architectural Blueprint

```
                     +----------------------------+
                     |    Supervisor / Lead       |
                     +----------------------------+
                       /            |           \
                      v             v            v
             +------------+  +------------+  +------------+
             | Researcher |  | Developer  |  | QA Tester  |
             +------------+  +------------+  +------------+
```

---

## 3. Core Implementation Principles

- **Clear role boundaries:** assign each subagent a single domain persona, system prompt, and toolset.\n- **Context hygiene:** prevent child conversation logs from polluting the lead orchestrator's prompt.\n- **Structured communication protocols:** exchange JSON artifacts or standard message envelopes.\n- **Explicit termination conditions:** define when the collaboration ends to prevent circular agent banter.

---

## 4. Reference Implementation Pattern

```python
class MultiAgentTeam:
    def __init__(self, researcher, coder, reviewer):
        self.researcher = researcher
        self.coder = coder
        self.reviewer = reviewer

    def run_feature(self, feature_spec: str) -> str:
        # Step 1: Research specifications
        context = self.researcher.run(f"Research patterns for: {feature_spec}")
        # Step 2: Implement code
        code = self.coder.run(f"Implement based on context: {context}")
        # Step 3: Review and verify
        review = self.reviewer.run(f"Audit this implementation: {code}")
        return {"code": code, "audit": review}

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
