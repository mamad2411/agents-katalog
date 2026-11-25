---
name: pattern-human-in-the-loop
description: Interleave human feedback, approval gates, and clarification interrupts into autonomous agent loops for high-stakes decision points.
metadata:
  category: agent-architecture
  tier: production
  chapter: 13
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Human-in-the-Loop (HITL) Pattern

## 1. Overview & Intent

Interleave human feedback, approval gates, and clarification interrupts into autonomous agent loops for high-stakes decision points.

> **Intent & Scope:** Use when agents execute destructive operations (deployments, financial transactions, database drops) or face underspecified requirements.

---

## 2. Architectural Blueprint

```
[Agent Action Proposed] --> [Risk Assessment] 
                               |-- (Low Risk)  --> [Auto-Execute]
                               +-- (High Risk) --> [Interrupt / Modal Prompt]
                                                        |
                                            (Human Approves / Rejects)
                                                        |
                                                        v
                                            [Resume Execution Graph]
```

---

## 3. Core Implementation Principles

- Classify actions by risk tier (read-only vs reversible write vs destructive write).\n- Auto-approve low-risk actions to maintain developer velocity.\n- Format approval requests with clear diffs, blast radius estimations, and one-click actions.\n- Persist agent execution state across pauses so interrupts can resume without re-running prior steps.

---

## 4. Reference Implementation Pattern

```python
class ApprovalGate:
    DESTRUCTIVE_TOOLS = {"delete_database", "git_push_force", "wire_transfer"}

    @classmethod
    def check_permission(cls, tool_name: str, arguments: dict, user_interface) -> bool:
        if tool_name in cls.DESTRUCTIVE_TOOLS:
            prompt = f"Approval required for '{tool_name}' with arguments: {arguments}"
            return user_interface.request_confirmation(prompt)
        return True

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
