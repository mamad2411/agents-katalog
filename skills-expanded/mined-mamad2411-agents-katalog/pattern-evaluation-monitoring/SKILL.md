---
name: pattern-evaluation-monitoring
description: Continuously assess agent quality and detect behavioral regressions using LLM-as-a-Judge rubrics, pairwise evaluation, and golden datasets.
metadata:
  category: agent-architecture
  tier: enterprise
  chapter: 19
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Evaluation & Monitoring Pattern

## 1. Overview & Intent

Continuously assess agent quality and detect behavioral regressions using LLM-as-a-Judge rubrics, pairwise evaluation, and golden datasets.

> **Intent & Scope:** Use in CI/CD release pipelines and production monitoring to ensure model prompt updates or code changes don't cause silent degradations.

---

## 2. Architectural Blueprint

```
[Test Case: Input + Golden Reference] --> [Candidate Agent] --> [Actual Output]
                                                                      |
                                                                      v
                                                    [LLM-as-a-Judge Evaluator]
                                                    (Score Rubric: 1-5 scale)
                                                                      |
                                                                      v
                                                  [CI/CD Quality Gate (Pass/Fail)]
```

---

## 3. Core Implementation Principles

- Use clear, rubric-based criteria (Correctness, Conciseness, Instruction Adherence, Safety).\n- **Mitigate judge bias:** swap ordering in pairwise evaluations to eliminate positional preference.\n- Maintain versioned golden benchmark datasets reflecting real user edge cases.\n- Fail CI builds when agent success rate drops below established statistical thresholds.

---

## 4. Reference Implementation Pattern

```python
from pydantic import BaseModel

class EvaluationResult(BaseModel):
    score: int  # 1 to 5
    rationale: str
    passed: bool

def evaluate_with_judge(question: str, ground_truth: str, answer: str, judge_llm) -> EvaluationResult:
    prompt = f"""Evaluate the agent output against the ground truth.
Question: {question}
Ground Truth: {ground_truth}
Agent Output: {answer}

Score 1-5 and determine if output passed."""
    return judge_llm.generate(prompt, response_model=EvaluationResult)

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
