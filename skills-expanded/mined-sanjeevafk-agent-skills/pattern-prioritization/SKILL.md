---
name: pattern-prioritization
description: Structure autonomous agent task backlogs using dynamic impact-versus-urgency scoring, dependency topological sorting, and WIP constraints.
metadata:
  category: agent-architecture
  tier: enterprise
  chapter: 20
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Prioritization Pattern

## 1. Overview & Intent

Structure autonomous agent task backlogs using dynamic impact-versus-urgency scoring, dependency topological sorting, and WIP constraints.

> **Intent & Scope:** Use when agents manage backlogs of tasks, incoming issues, bugs, or multiple customer tickets without human project managers.

---

## 2. Architectural Blueprint

```
[Incoming Tasks / Issues] --> [Score Matrix: Impact x Urgency]
                                       |
                                       v
                        [Dependency Graph Resolver]
                                       |
                                       v
                        [Active Work-in-Progress (WIP) Queue]
```

---

## 3. Core Implementation Principles

- Score dynamically using standardized multi-factor formulas (Impact * Urgency / Effort).\n- Resolve task dependency graphs topologically so blockers are addressed first.\n- **Enforce Work-In-Progress (WIP) limits:** prevent agents from thrashing across too many concurrent goals.\n- Re-evaluate priorities when new critical information or blocker events emerge.

---

## 4. Reference Implementation Pattern

```python
from pydantic import BaseModel

class TaskItem(BaseModel):
    id: str
    description: str
    impact: int   # 1-10
    urgency: int  # 1-10
    effort: int   # 1-10

    @property
    def priority_score(self) -> float:
        return (self.impact * 2.0 + self.urgency * 1.5) / max(self.effort, 1)

def prioritize_tasks(tasks: list[TaskItem]) -> list[TaskItem]:
    return sorted(tasks, key=lambda t: t.priority_score, reverse=True)

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
