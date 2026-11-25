---
name: pattern-planning
description: "Structure agent behavior into explicit planning phases: static plan-and-solve, dynamic ReAct loops, or hierarchical DAG decomposition."
metadata:
  category: agent-architecture
  tier: core
  chapter: 06
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Planning & Task Decomposition Pattern

## 1. Overview & Intent

Structure agent behavior into explicit planning phases: static plan-and-solve, dynamic ReAct loops, or hierarchical DAG decomposition.

> **Intent & Scope:** Use when tasks require multi-step dependencies, exploration, backtracking, or dynamic adjustment based on intermediate discoveries.

---

## 2. Architectural Blueprint

```
[Goal] --> [Planner] --> [Step 1] --> [Step 2] --> [Step 3]
                            |            |            |
                         (Exec)       (Exec)       (Exec)
                            |            |            |
                            v            v            v
                         [Result]     [Failed] --> [Replanner] --> [New Plan]
```

---

## 3. Core Implementation Principles

- **Separate planning from execution:** generate the roadmap before invoking tools.\n- Maintain an explicit execution DAG with dependencies and completion statuses.\n- **Support dynamic replanning:** when a step fails or uncovers new data, revise downstream steps.\n- Limit plan depth (typically 5–10 steps) to preserve context and focus.

---

## 4. Reference Implementation Pattern

```python
from typing import List
from pydantic import BaseModel

class PlanStep(BaseModel):
    step_id: int
    action: str
    dependencies: List[int]
    status: str = "pending"  # pending, completed, failed

class ExecutionPlan(BaseModel):
    goal: str
    steps: List[PlanStep]

def execute_plan_with_replanning(goal: str):
    plan = planner_agent.generate_plan(goal)
    for step in plan.steps:
        success = execute_step(step)
        if not success:
            plan = planner_agent.replan(goal, current_plan=plan, failed_step=step)
            break

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
