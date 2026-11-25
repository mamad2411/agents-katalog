---
name: eval-harness
description: Evaluation harness for LLM and code quality assessment. Covers Pass@k metrics, golden datasets, LLM-as-judge, benchmark suites, regression detection, and eval-driven development workflow.
origin: AI Dev Kit
disable-model-invocation: false
---

# Evaluation Harness

Systematic evaluation framework for LLM-powered systems and code generation quality. Covers Pass@k metrics, golden datasets, LLM-as-judge evaluation, benchmark suites, regression detection, and eval-driven development. Use this skill when building, measuring, or improving evaluation pipelines for AI features.

## When to Use

- Setting up evaluation infrastructure for LLM features
- Measuring code generation quality (Pass@k, accuracy)
- Building golden test datasets for RAG or agent systems
- Implementing LLM-as-judge evaluation pipelines
- Tracking regression across model or prompt changes
- Establishing eval-driven development (EDD) workflows
- Comparing model providers or configurations

## Core Concepts

### Pass@k Metrics

Pass@k measures the probability that at least one of k generated samples passes all test cases. It's the standard metric for code generation evaluation.

```
Pass@k = 1 - (C(n-c, k) / C(n, k))

Where:
  n = total number of generated samples per problem
  c = number of samples that pass all tests
  k = number of submissions allowed (typically 1, 10, 100)
```

**Implementation:**

```python
import numpy as np
from scipy.special import comb

def pass_at_k(n: int, c: int, k: int) -> float:
    """
    Unbiased estimator for Pass@k.
    n: total samples generated per problem
    c: number of correct samples
    k: top-k submissions considered
    """
    if n - c < k:
        return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

# Example: 20 samples generated, 12 pass all tests
n, c = 20, 12
print(f"Pass@1: {pass_at_k(n, c, 1):.4f}")  # 0.6000
print(f"Pass@10: {pass_at_k(n, c, 10):.4f}") # 0.9995
```

**Practical evaluation script:**

```python
import subprocess
import json
from pathlib import Path

def evaluate_pass_at_k(model_name: str, problems: list[dict], num_samples: int = 10) -> dict:
    """
    Evaluate a model's Pass@k on a set of coding problems.
    """
    results = []

    for problem in problems:
        problem_results = {"id": problem["id"], "samples": []}

        for i in range(num_samples):
            # Generate code from model
            generated = generate_code(model_name, problem["prompt"], temperature=0.8)

            # Write to temp file and run tests
            test_passed = run_unit_tests(problem["test_code"], generated)

            problem_results["samples"].append({
                "sample_id": i,
                "code": generated,
                "passed": test_passed,
            })

        correct_count = sum(1 for s in problem_results["samples"] if s["passed"])
        problem_results["pass@1"] = pass_at_k(num_samples, correct_count, 1)
        problem_results["pass@10"] = pass_at_k(num_samples, correct_count, 10)
        results.append(problem_results)

    # Aggregate
    avg_pass_1 = np.mean([r["pass@1"] for r in results])
    avg_pass_10 = np.mean([r["pass@10"] for r in results])

    return {
        "model": model_name,
        "num_problems": len(problems),
        "num_samples": num_samples,
        "pass@1": round(avg_pass_1, 4),
        "pass@10": round(avg_pass_10, 4),
        "per_problem": results,
    }

def generate_code(model: str, prompt: str, temperature: float) -> str:
    """Call the model API to generate code."""
    # Implementation depends on model provider
    pass

def run_unit_tests(test_code: str, solution_code: str) -> bool:
    """Execute test suite against generated solution."""
    combined = f"{solution_code}\n\n{test_code}"
    result = subprocess.run(
        ["python", "-m", "pytest", "-q", "--tb=no"],
        input=combined,
        text=True,
        capture_output=True,
        timeout=30,
    )
    return result.returncode == 0
```

### Golden Datasets

Curated input-output pairs used as ground truth for evaluation.

**Structure:**

```json
{
  "dataset_name": "api-code-generation",
  "version": "1.2.0",
  "created": "2025-01-15",
  "problems": [
    {
      "id": "prob-001",
      "category": "fastapi-endpoint",
      "difficulty": "medium",
      "prompt": "Create a FastAPI POST endpoint /users that validates input with Pydantic, creates a user record, and returns 201 with the user object.",
      "golden_solution": {
        "expected_files": ["routes/users.py"],
        "key_patterns": ["@router.post", "status_code=201", "BaseModel", "HTTPException"],
        "forbidden_patterns": ["global db", "print(", "except Exception"],
        "tests": ["test_create_user_valid", "test_create_user_missing_name", "test_create_user_duplicate_email"]
      },
      "acceptance_criteria": {
        "valid_request": { "status": 201, "response_keys": ["id", "name", "email"] },
        "missing_name": { "status": 422 },
        "duplicate_email": { "status": 409 },
        "invalid_email": { "status": 422 }
      }
    },
    {
      "id": "prob-002",
      "category": "react-component",
      "difficulty": "easy",
      "prompt": "Create a UserCard component that displays user name, email, and a delete button. Call onDelete callback when delete is clicked.",
      "golden_solution": {
        "expected_files": ["components/UserCard.tsx"],
        "key_patterns": ["export function UserCard", "onDelete", "prop-types or TypeScript interface"],
        "forbidden_patterns": ["any", "console.log"],
        "tests": ["renders user info", "calls onDelete"]
      }
    }
  ]
}
```

### LLM-as-Judge Evaluation

Using a strong LLM to evaluate outputs against rubrics. Useful when exact-match comparison is insufficient.

```python
import json
from openai import OpenAI

client = OpenAI()

def llm_judge_evaluate(
    prompt: str,
    candidate_output: str,
    golden_output: str,
    rubric: dict,
    judge_model: str = "gpt-4o",
) -> dict:
    """
    Evaluate candidate output using LLM-as-judge.
    Returns structured scores per rubric dimension.
    """
    rubric_str = json.dumps(rubric, indent=2)

    system_prompt = f"""You are an expert code evaluator. Evaluate the candidate code against the rubric.

Rubric dimensions (score 1-5 each):
{rubric_str}

Respond with ONLY a JSON object: {{"dimension_name": score, ...}}"""

    user_prompt = f"""Original prompt:
{prompt}

Golden reference:
{golden_output}

Candidate output:
{candidate_output}"""

    response = client.chat.completions.create(
        model=judge_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    scores = json.loads(response.choices[0].message.content)
    return scores

# Example rubric
CORRECTNESS_RUBRIC = {
    "correctness": "Does the code produce the expected output?",
    "completeness": "Are all requirements addressed?",
    "error_handling": "Are edge cases and errors handled appropriately?",
    "code_quality": "Is the code clean, readable, and well-structured?",
    "security": "Does the code avoid common security vulnerabilities?",
    "efficiency": "Is the algorithmic complexity reasonable?",
}

# Usage
result = llm_judge_evaluate(
    prompt="Create a function that parses a CSV file and returns column statistics.",
    candidate_output=open("candidate.py").read(),
    golden_solution=open("golden.py").read(),
    rubric=CORRECTNESS_RUBRIC,
)
print(json.dumps(result, indent=2))
```

### Benchmark Suites

Standardized test collections for consistent comparison across models and versions.

**HumanEval-style benchmark config:**

```yaml
# evals/benchmarks/humaneval.yaml
name: humaneval
version: "1.0"
source: "https://github.com/openai/human-eval"
num_problems: 164
languages: [python]
metrics: [pass@1, pass@10, pass@100]
timeout_seconds: 30
max_tokens: 512

# Custom internal benchmark
evals/benchmarks/internal-api.yaml
name: internal-api-coding
version: "2.1"
num_problems: 50
categories:
  - fastapi-endpoints
  - pydantic-models
  - sqlalchemy-queries
  - react-components
difficulty_distribution:
  easy: 15
  medium: 25
  hard: 10
metrics: [pass@1, pass@5, llm_judge_score]
```

## Eval-Driven Development (EDD) Workflow

EDD applies TDD principles to evaluation: define expected quality metrics first, then iterate until targets are met.

### Step 1: Define Quality Targets

```python
# evals/quality_targets.json
{
  "model": "gpt-4o",
  "targets": {
    "pass@1": 0.75,
    "pass@5": 0.90,
    "llm_judge_avg": 4.0,
    "zero_security_violations": true,
    "max_toxicity_score": 0.1
  },
  "regression_threshold": {
    "pass@1": -0.05,
    "pass@5": -0.03,
    "llm_judge_avg": -0.3
  }
}
```

### Step 2: Build Eval Pipeline

```python
# evals/pipeline.py
import json
import datetime
from pathlib import Path

class EvalPipeline:
    def __init__(self, config_path: str):
        self.config = json.loads(Path(config_path).read_text())
        self.results_dir = Path("evals/results")
        self.results_dir.mkdir(exist_ok=True)

    def run(self, model_name: str) -> dict:
        """Run full evaluation pipeline."""
        results = {
            "model": model_name,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "metrics": {},
        }

        # 1. Pass@k evaluation
        pass_k_results = self.run_pass_at_k(model_name)
        results["metrics"]["pass@1"] = pass_k_results["pass@1"]
        results["metrics"]["pass@5"] = pass_k_results["pass@5"]

        # 2. LLM-as-judge evaluation
        judge_results = self.run_llm_judge(model_name)
        results["metrics"]["llm_judge_avg"] = judge_results["average_score"]

        # 3. Security scan on generated code
        security_results = self.run_security_check(model_name)
        results["metrics"]["security_violations"] = security_results["violation_count"]

        # 4. Regression check
        self.check_regression(results["metrics"])

        # 5. Save results
        output_path = self.results_dir / f"{model_name}_{datetime.date.today()}.json"
        output_path.write_text(json.dumps(results, indent=2))

        return results

    def check_regression(self, current: dict) -> list[str]:
        """Compare against previous run and flag regressions."""
        previous = self.load_previous_results()
        if not previous:
            return []

        thresholds = self.config["targets"]["regression_threshold"]
        regressions = []

        for metric, threshold in thresholds.items():
            current_val = current.get(metric, 0)
            previous_val = previous["metrics"].get(metric, 0)
            delta = current_val - previous_val

            if delta < threshold:
                regressions.append(
                    f"REGRESSION: {metric} dropped from {previous_val:.4f} to {current_val:.4f} "
                    f"(threshold: {threshold})"
                )

        return regressions
```

### Step 3: Automated Regression Detection

```python
def detect_eval_regressions(current_results: dict, baseline_results: dict) -> dict:
    """
    Compare current eval results against baseline.
    Returns regression report with severity levels.
    """
    regressions = {
        "critical": [],
        "warning": [],
        "info": [],
    }

    metrics_to_check = {
        "pass@1": {"critical": -0.10, "warning": -0.05},
        "pass@5": {"critical": -0.08, "warning": -0.03},
        "llm_judge_avg": {"critical": -0.5, "warning": -0.3},
    }

    for metric, thresholds in metrics_to_check.items():
        current = current_results.get(metric, 0)
        baseline = baseline_results.get(metric, 0)
        delta = current - baseline

        if delta < thresholds["critical"]:
            regressions["critical"].append(
                f"{metric}: {baseline:.4f} → {current:.4f} (Δ {delta:+.4f})"
            )
        elif delta < thresholds["warning"]:
            regressions["warning"].append(
                f"{metric}: {baseline:.4f} → {current:.4f} (Δ {delta:+.4f})"
            )
        elif delta > 0:
            regressions["info"].append(
                f"{metric}: {baseline:.4f} → {current:.4f} (Δ {delta:+.4f}) ✓"
            )

    return regressions

# Example output
# {
#   "critical": ["pass@1: 0.7800 → 0.6200 (Δ -0.1600)"],
#   "warning": ["llm_judge_avg: 4.2000 → 3.8000 (Δ -0.4000)"],
#   "info": ["pass@5: 0.8900 → 0.9100 (Δ +0.0200) ✓"]
# }
```

## Eval Config Examples

### Full Eval Configuration

```yaml
# evals/config.yaml
eval_name: api-codegen-eval
model_under_test: claude-sonnet-4-20250514
dataset: datasets/internal-api-v2.json

generation:
  temperature: 0.8
  top_p: 0.95
  max_tokens: 2048
  num_samples: 20
  stop_sequences: ["\n\n\n", "```"]

execution:
  timeout_seconds: 30
  memory_limit_mb: 512
  network_access: false
  allowed_imports: ["fastapi", "pydantic", "sqlalchemy", "pytest"]

evaluation:
  pass_at_k: [1, 5, 10]
  llm_judge:
    model: gpt-4o
    rubric: rubrics/code-correctness.json
    temperature: 0

regression:
  baseline: evals/results/baseline.json
  fail_on_critical: true
  alert_thresholds:
    pass@1: -0.05
    pass@5: -0.03
```

### Scoring and Reporting

```python
def generate_eval_report(results: dict) -> str:
    """Generate human-readable evaluation report."""
    report = f"""
# Evaluation Report: {results['model']}
Date: {results['timestamp']}

## Summary

| Metric | Score | Target | Status |
|---|---|---|---|
| Pass@1 | {results['metrics']['pass@1']:.4f} | 0.75 | {'✅' if results['metrics']['pass@1'] >= 0.75 else '❌'} |
| Pass@5 | {results['metrics']['pass@5']:.4f} | 0.90 | {'✅' if results['metrics']['pass@5'] >= 0.90 else '❌'} |
| LLM Judge Avg | {results['metrics']['llm_judge_avg']:.2f} | 4.0 | {'✅' if results['metrics']['llm_judge_avg'] >= 4.0 else '❌'} |
| Security Violations | {results['metrics']['security_violations']} | 0 | {'✅' if results['metrics']['security_violations'] == 0 else '❌'} |

## Per-Problem Breakdown

"""
    for problem in results.get("per_problem", []):
        status = "✅" if problem["pass@1"] >= 0.5 else "❌"
        report += f"- {problem['id']}: Pass@1 = {problem['pass@1']:.4f} {status}\n"

    return report
```

## CI/CD Integration

```yaml
# .github/workflows/evals.yml
name: Evaluation Pipeline
on:
  push:
    branches: [main]
    paths: ['prompts/**', 'evals/**']
  schedule:
    - cron: '0 4 * * 1'  # Weekly full eval run

jobs:
  eval:
    runs-on: ubuntu-latest
    timeout-minutes: 60
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r evals/requirements.txt
      - name: Run eval pipeline
        run: |
          python -m evals.pipeline --model ${{ secrets.EVAL_MODEL }}
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      - name: Check regressions
        run: python -m evals.check_regression
      - uses: actions/upload-artifact@v4
        with:
          name: eval-results
          path: evals/results/
          retention-days: 90
```

## Common Pitfalls

| Pitfall | Consequence | Fix |
|---|---|---|
| Small dataset (< 20 problems) | High variance, unreliable metrics | Use ≥50 problems for stable estimates |
| No temperature sweep | Overfitting to one sampling config | Test at 0.0, 0.5, 0.8, 1.0 |
| Judging by exact string match | False negatives for equivalent solutions | Use test execution or LLM-as-judge |
| No regression baseline | Quality drift goes undetected | Always compare against previous run |
| Running evals only locally | CI environment differences | Run evals in CI with same config as prod |
| Ignoring failure modes | Only measuring success | Track error rate, timeout rate, exception types |

## Best Practices

1. **Start with a golden dataset** — 50+ problems with known solutions
2. **Measure Pass@k early** — establish baseline before any prompt changes
3. **Use LLM-as-judge for nuance** — exact-match is too strict for code quality
4. **Automate regression checks** — every prompt/model change triggers re-eval
5. **Track trends, not points** — plot metrics over time to see trajectories
6. **Fail CI on critical regression** — >10% Pass@1 drop should block merge
7. **Version your datasets** — tag releases, track what changed
8. **Separate test/train** — never evaluate on problems used during prompt engineering
9. **Run full eval weekly** — daily smoke tests, weekly deep eval
10. **Report publicly** — dashboards keep quality visible and accountable

## Success Metrics

- [ ] Golden dataset has ≥50 problems across multiple difficulty levels
- [ ] Pass@1 meets or exceeds target threshold
- [ ] LLM-as-judge average score ≥ 4.0 / 5.0
- [ ] Zero security violations in generated code
- [ ] No critical regressions between consecutive runs
- [ ] Eval pipeline runs automatically in CI/CD
- [ ] Evaluation results visible in dashboard or report

---

**Remember:** If you can't measure it, you can't improve it. Evaluation is the feedback loop that turns guessing into engineering.
