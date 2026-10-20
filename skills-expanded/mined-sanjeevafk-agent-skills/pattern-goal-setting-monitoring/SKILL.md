---
name: pattern-goal-setting-monitoring
description: Track long-running agent progress toward quantifiable goals with milestone checkpoints, status monitors, and early stopping triggers.
metadata:
  category: agent-architecture
  tier: advanced
  chapter: 11
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Goal Setting & Monitoring Pattern

## 1. Overview & Intent

Track long-running agent progress toward quantifiable goals with milestone checkpoints, status monitors, and early stopping triggers.

> **Intent & Scope:** Use when executing multi-hour, autonomous agent tasks (benchmarking, large refactors, scraping fleets) requiring health checks and drift detection.

---

## 2. Architectural Blueprint

```
[Overall Objective] --> [Milestone Tracker] --> [Current Step]
                             ^                        |
                             |                 (Telemetry Event)
                             +---- [Monitor / Health Check]
```

---

## 3. Core Implementation Principles

- Establish quantifiable completion metrics (e.g. 100% test pass, 0 linter errors, target token count).\n- Emit structured heartbeat events after each milestone execution.\n- **Detect goal drift:** calculate semantic similarity between current actions and primary objective.\n- **Implement early-exit guards:** terminate when goal criteria are fully met or when budget caps are reached.

---

## 4. Reference Implementation Pattern

```python
class GoalMonitor:
    def __init__(self, objective: str, milestones: list[str]):
        self.objective = objective
        self.milestones = {m: False for m in milestones}
        self.step_count = 0
        self.max_steps = 25

    def record_step(self, milestone_achieved: str = None) -> bool:
        self.step_count += 1
        if milestone_achieved and milestone_achieved in self.milestones:
            self.milestones[milestone_achieved] = True
            
        all_done = all(self.milestones.values())
        exceeded = self.step_count >= self.max_steps
        return all_done or not exceeded

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
