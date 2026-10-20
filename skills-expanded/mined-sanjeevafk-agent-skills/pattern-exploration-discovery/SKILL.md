---
name: pattern-exploration-discovery
description: "Implement autonomous scientific inquiry and research loops: hypothesis formulation, experiment design, simulation, and iterative synthesis."
metadata:
  category: agent-architecture
  tier: enterprise
  chapter: 21
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Exploration & Discovery Pattern

## 1. Overview & Intent

Implement autonomous scientific inquiry and research loops: hypothesis formulation, experiment design, simulation, and iterative synthesis.

> **Intent & Scope:** Use for automated literature research, algorithmic tuning, prompt discovery, or self-directed scientific experimentation (AgentLaboratory).

---

## 2. Architectural Blueprint

```
[Research Domain] --> [Hypothesis Generator] --> [Experiment Designer]
                              ^                            |
                              |                    [Execution Sandbox]
                              |                            |
                              +--- [Outcome Synthesis] <---+
```

---

## 3. Core Implementation Principles

- Formulate testable, falsifiable hypotheses with explicit success criteria.\n- Design bounded, repeatable experiments executed in isolated sandboxes.\n- **Synthesize negative results:** failed experiments provide constraints that guide future hypothesis generation.\n- Maintain structured literature and experimental logs to avoid exploring circular dead ends.

---

## 4. Reference Implementation Pattern

```python
class DiscoveryAgent:
    def __init__(self, hypothesis_engine, lab_runner):
        self.hypothesis_engine = hypothesis_engine
        self.lab_runner = lab_runner
        self.history = []

    def run_discovery_cycle(self, domain_spec: str):
        # Step 1: Formulate hypothesis
        hypothesis = self.hypothesis_engine.generate(domain_spec, prior_history=self.history)
        # Step 2: Execute experiment
        result = self.lab_runner.run_experiment(hypothesis)
        # Step 3: Record findings
        self.history.append({"hypothesis": hypothesis, "outcome": result})
        return result

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
