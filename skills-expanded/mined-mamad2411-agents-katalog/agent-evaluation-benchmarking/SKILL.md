---
name: agent_evaluation_benchmarking
description: Use when evaluating AI agent performance, designing benchmarks, or measuring production agent quality. Covers benchmarks, metrics, evaluation frameworks, and regression testing for agentic systems.
---

# Agent Evaluation & Benchmarking

## Overview

Evaluating agents is harder than evaluating models. Agents have state, make multi-step decisions, use tools, and interact with external systems. This skill covers how to measure agent quality across correctness, reliability, efficiency, and safety dimensions.

**Core principle:** You can't improve what you don't measure. Agent evaluation must be continuous, automated, and grounded in real tasks.

## When to Use

- Choosing a benchmark for a new agentic system
- Designing custom evaluation tasks for your domain
- Setting up regression testing for agent behavior
- Measuring production agent quality (completion rate, latency, cost)
- Comparing two agent architectures or prompts
- Detecting degradation after model or code changes

## When NOT to Use

- Evaluating a single LLM call (use standard LLM evals)
- When you don't have ground truth or human judgment
- For purely creative/open-ended tasks without criteria

---

## 1. Evaluation Dimensions

| Dimension | Question | Metrics |
|-----------|----------|---------|
| **Correctness** | Did the agent solve the task? | Task success rate, accuracy |
| **Reliability** | Does it consistently succeed? | Pass@k, variance, flakiness |
| **Efficiency** | How many steps/cost? | Steps to completion, cost per task |
| **Safety** | Did it avoid harmful actions? | Guardrail trigger rate, harm incidents |
| **Helpfulness** | Was the output useful? | Human rating, downstream utility |
| **Latency** | How fast? | P50/P95/P99 completion time |

---

## 2. Public Benchmarks

### Software Engineering

| Benchmark | Task | Metric | URL |
|-----------|------|--------|-----|
| **SWE-bench** | Fix real GitHub issues | Resolved % | github.com/princeton-nlp/SWE-bench |
| **SWE-bench Verified** | Human-verified subset | Resolved % | Same |
| **SWE-bench Multimodal** | Issues with images | Resolved % | Same |

### General Agent Capabilities

| Benchmark | Task | Metric | URL |
|-----------|------|--------|-----|
| **GAIA** | Real-world questions (web, files, reasoning) | Accuracy | huggingface.co/gaia-benchmark |
| **AgentBench** | Multi-environment (OS, web, DB, etc.) | Success rate | github.com/THUDM/AgentBench |
| **WebArena** | Web navigation tasks | Success rate | github.com/xlang-ai/WebArena |
| **Mind2Web** | Web task execution | Element accuracy, task success | github.com/OSU-NLP-Group/Mind2Web |

### Reasoning & Planning

| Benchmark | Task | Metric |
|-----------|------|--------|
| **Plan-RewardBench** | Trajectory-level preference | Agreement with human judgments |
| **KDR** | Deep research tasks | Coverage, accuracy, citation quality |
| **HumanEval** | Code generation | Pass@k |
| **MBPP** | Python programming | Pass@k |

### Safety & Robustness

| Benchmark | Task | Metric |
|-----------|------|--------|
| **TraceSafe** | Multi-step tool-calling safety | Guardrail effectiveness |
| **AgentHarm** | Harmful task refusal | Refusal rate |
| **ToolEmu** | Tool-use emulation | Error detection rate |

---

## 3. Custom Evaluation Design

### Golden Dataset Pattern

```python
# golden_dataset.jsonl
{
  "id": "task-001",
  "query": "How do we handle JWT token refresh in this codebase?",
  "project": "my-app",
  "expected_memory_ids": ["mem-123", "mem-456"],
  "expected_answer_contains": ["refresh token", "expiry", "rotation"],
  "min_relevance": 0.8,
  "tags": ["auth", "jwt", "backend"]
}
```

### Evaluation Pipeline

```python
async def evaluate_agent(dataset: list[Task], agent: Agent) -> EvaluationReport:
    results = []
    
    for task in dataset:
        # Run agent
        response = await agent.run(task.query)
        
        # Score
        result = ScoreResult(
            task_id=task.id,
            success=check_success(response, task),
            recall=check_recall(response, task.expected_memory_ids),
            latency_ms=response.latency_ms,
            cost_usd=response.cost_usd,
            steps=len(response.actions),
        )
        results.append(result)
    
    return EvaluationReport(
        overall_success=mean(r.success for r in results),
        recall_at_10=mean(r.recall for r in results),
        avg_latency_ms=mean(r.latency_ms for r in results),
        avg_cost=mean(r.cost_usd for r in results),
        avg_steps=mean(r.steps for r in results),
    )
```

### Metrics Definitions

```python
def task_success(response: Response, task: Task) -> bool:
    """Binary: did the agent solve the task?"""
    return all(phrase in response.text for phrase in task.expected_answer_contains)

def recall_at_k(retrieved: list[str], relevant: list[str], k: int = 10) -> float:
    """Fraction of relevant items found in top-k."""
    return len(set(retrieved[:k]) & set(relevant)) / len(relevant)

def mean_reciprocal_rank(retrieved: list[str], relevant: list[str]) -> float:
    """Average of 1/rank for first relevant item."""
    for i, item in enumerate(retrieved):
        if item in relevant:
            return 1 / (i + 1)
    return 0.0
```

---

## 4. Regression Testing

### Continuous Evaluation

```yaml
# .github/workflows/agent-eval.yml
name: Agent Evaluation
on: [push, pull_request]
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e ".[test]"
      - run: pytest tests/evaluation/ --golden-dataset=data/golden.jsonl
      - run: python scripts/compare_baseline.py --report=eval-report.json
```

### Baseline Comparison

```python
def compare_to_baseline(new_report: EvaluationReport, baseline: EvaluationReport) -> bool:
    """Returns True if new results meet or exceed baseline."""
    checks = [
        new_report.overall_success >= baseline.overall_success * 0.98,  # Allow 2% regression
        new_report.recall_at_10 >= baseline.recall_at_10 * 0.95,
        new_report.avg_latency_ms <= baseline.avg_latency_ms * 1.10,  # Allow 10% slower
        new_report.avg_cost <= baseline.avg_cost * 1.05,
    ]
    return all(checks)
```

---

## 5. Human Evaluation

### Rubric-Based Scoring

| Criterion | 1 (Poor) | 3 (OK) | 5 (Excellent) |
|-----------|----------|--------|---------------|
| **Correctness** | Wrong answer | Partially correct | Fully correct |
| **Completeness** | Missing key info | Most info present | All relevant info |
| **Clarity** | Confusing | Understandable | Crystal clear |
| **Safety** | Harmful output | Minor issue | Fully safe |

### Inter-Rater Agreement

```python
from sklearn.metrics import cohen_kappa

# Measure agreement between human evaluators
kappa = cohen_kappa_scores(rater_a_scores, rater_b_scores)
# kappa > 0.6 is good, > 0.8 is excellent
```

---

## 6. Production Monitoring

### Key Production Metrics

```python
class AgentMetrics:
    def __init__(self):
        self.tasks_total = Counter("agent_tasks_total", ["status"])
        self.task_latency = Histogram("agent_task_latency_seconds")
        self.tool_calls = Counter("agent_tool_calls_total", ["tool", "status"])
        self.llm_tokens = Counter("agent_llm_tokens_total", ["model", "type"])
        self.memory_hits = Counter("agent_memory_hits_total", ["store"])
    
    def record_task(self, success: bool, latency_ms: float):
        status = "success" if success else "failure"
        self.tasks_total.labels(status=status).inc()
        self.task_latency.observe(latency_ms / 1000)
```

### Alerting Rules

```yaml
# Alert when agent success rate drops
- alert: AgentSuccessRateLow
  expr: rate(agent_tasks_total{status="success"}[5m]) / rate(agent_tasks_total[5m]) < 0.8
  for: 5m
  annotations:
    summary: "Agent success rate below 80%"
```

---

## 7. Evaluation Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Cherry-picked examples** | Only showing successes | Report full distribution |
| **Single metric** | Misses trade-offs | Report 4-6 dimensions |
| **Static benchmark** | Doesn't reflect drift | Re-evaluate monthly |
| **No baseline** | Can't detect regression | Save baseline on every release |
| **Synthetic only** | Not representative | Mix synthetic + real tasks |
| **Ignoring cost** | Expensive at scale | Always measure cost per task |

---

## 8. References

- [SWE-bench](https://github.com/princeton-nlp/SWE-bench)
- [GAIA Benchmark](https://huggingface.co/gaia-benchmark)
- [AgentBench](https://github.com/THUDM/AgentBench)
- [WebArena](https://github.com/xlang-ai/WebArena)
- [Plan-RewardBench](https://arxiv.org/abs/2604.08178)
- [KDR Framework](https://arxiv.org/abs/2604.07720)
- [TraceSafe](https://arxiv.org/abs/2604.07223)
- knowledge/12_agentic_ai_frontier_2026.md (Evaluation section)
- skills/32_agent_evaluation/SKILL.md
