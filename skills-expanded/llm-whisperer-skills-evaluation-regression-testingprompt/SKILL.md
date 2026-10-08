# Regression Testing with Golden Datasets and Quality Gates

## Overview

Regression testing for LLM systems ensures that model updates, prompt changes, or infrastructure modifications don't degrade quality on known-good outputs. Unlike traditional software testing where outputs are deterministic, LLM regression testing must handle stochastic outputs, semantic equivalence, and gradual quality drift.

Golden datasets are curated collections of input-output pairs with human-verified quality labels. Quality gates are automated checkpoints that block deployments if regression metrics fall below thresholds. Together, they form a safety net that enables rapid iteration without sacrificing quality.

This skill covers building production-grade regression testing systems with golden dataset management, automated quality gates, drift detection, and CI/CD integration.

## Key Concepts

- **Golden datasets**: Curated test cases with expected outputs, quality scores, and edge case annotations
- **Semantic similarity**: Use embedding-based comparison rather than exact string matching for output validation
- **Quality gates**: Automated pass/fail thresholds on regression metrics that block deployments
- **Drift detection**: Statistical tests to detect gradual quality degradation over time
- **Snapshot testing**: Store known-good outputs and compare new outputs against them
- **A/B regression**: Compare new model version against current production on the same test set
- **Per-category gates**: Different quality thresholds for different task types (easy vs hard, safety-critical vs casual)
- **Automated triage**: Classify regressions as critical (blocks deploy) vs minor (warning only)

## Implementation Patterns

### Golden Dataset Management

```python
import json
import hashlib
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional
from datetime import datetime

@dataclass
class GoldenTestCase:
    id: str
    input_prompt: str
    expected_output: str
    category: str
    difficulty: str  # "easy", "medium", "hard"
    quality_score: float  # 0-1, human-verified
    embedding: Optional[list[float]] = None
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

class GoldenDatasetManager:
    def __init__(self, dataset_path: str):
        self.path = Path(dataset_path)
        self.cases: list[GoldenTestCase] = []
        if self.path.exists():
            self._load()

    def _load(self):
        data = json.loads(self.path.read_text())
        self.cases = [GoldenTestCase(**item) for item in data]

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(
            [c.to_dict() for c in self.cases], indent=2
        ))

    def add_case(self, input_prompt: str, expected_output: str,
                 category: str, difficulty: str = "medium",
                 quality_score: float = 1.0, tags: list[str] = None) -> GoldenTestCase:
        case_id = hashlib.sha256(input_prompt.encode()).hexdigest()[:12]
        case = GoldenTestCase(
            id=case_id,
            input_prompt=input_prompt,
            expected_output=expected_output,
            category=category,
            difficulty=difficulty,
            quality_score=quality_score,
            tags=tags or [],
        )
        self.cases.append(case)
        return case

    def get_by_category(self, category: str) -> list[GoldenTestCase]:
        return [c for c in self.cases if c.category == category]

    def get_by_difficulty(self, difficulty: str) -> list[GoldenTestCase]:
        return [c for c in self.cases if c.difficulty == difficulty]

    def get_statistics(self) -> dict:
        categories = {}
        for c in self.cases:
            categories.setdefault(c.category, 0)
            categories[c.category] += 1
        return {
            "total_cases": len(self.cases),
            "categories": categories,
            "avg_quality_score": sum(c.quality_score for c in self.cases) / len(self.cases) if self.cases else 0,
        }
```

### Semantic Similarity Checker

```python
import numpy as np

class SemanticSimilarityChecker:
    def __init__(self, embedding_model: str = "text-embedding-3-small"):
        self.embedding_model = embedding_model
        self.thresholds = {
            "exact_match": 1.0,
            "high_similarity": 0.9,
            "acceptable": 0.75,
            "low_similarity": 0.5,
        }

    async def compare(self, expected: str, actual: str) -> dict:
        expected_emb = await self._embed(expected)
        actual_emb = await self._embed(actual)

        similarity = self._cosine_similarity(expected_emb, actual_emb)

        if similarity >= self.thresholds["exact_match"]:
            verdict = "exact_match"
        elif similarity >= self.thresholds["high_similarity"]:
            verdict = "high_similarity"
        elif similarity >= self.thresholds["acceptable"]:
            verdict = "acceptable"
        elif similarity >= self.thresholds["low_similarity"]:
            verdict = "low_similarity"
        else:
            verdict = "regression"

        return {
            "similarity": round(similarity, 4),
            "verdict": verdict,
            "passed": verdict in ("exact_match", "high_similarity", "acceptable"),
        }

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        a, b = np.array(a), np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    async def _embed(self, text: str) -> list[float]:
        # Use your embedding provider
        pass
```

### Quality Gate System

```python
from dataclasses import dataclass

@dataclass
class QualityGate:
    name: str
    metric: str
    threshold: float
    comparison: str  # "gte", "lte", "eq"
    severity: str  # "critical" (blocks deploy) or "warning"
    category: Optional[str] = None  # If None, applies to all

class QualityGateEvaluator:
    def __init__(self, gates: list[QualityGate]):
        self.gates = gates

    def evaluate(self, metrics: dict) -> dict:
        results = []
        all_critical_passed = True

        for gate in self.gates:
            metric_key = f"{gate.category}_{gate.metric}" if gate.category else gate.metric
            actual = metrics.get(metric_key, metrics.get(gate.metric, 0))

            if gate.comparison == "gte":
                passed = actual >= gate.threshold
            elif gate.comparison == "lte":
                passed = actual <= gate.threshold
            else:
                passed = abs(actual - gate.threshold) < 1e-6

            if not passed and gate.severity == "critical":
                all_critical_passed = False

            results.append({
                "gate": gate.name,
                "metric": metric_key,
                "threshold": gate.threshold,
                "actual": actual,
                "passed": passed,
                "severity": gate.severity,
            })

        return {
            "overall_passed": all_critical_passed,
            "gates": results,
            "failed_critical": [r for r in results if not r["passed"] and r["severity"] == "critical"],
            "failed_warnings": [r for r in results if not r["passed"] and r["severity"] == "warning"],
        }
```

### Drift Detection

```python
import numpy as np
from scipy import stats

class DriftDetector:
    def __init__(self, window_size: int = 100, p_value_threshold: float = 0.05):
        self.window_size = window_size
        self.p_value_threshold = p_value_threshold
        self.baseline_scores: list[float] = []
        self.recent_scores: list[float] = []

    def set_baseline(self, scores: list[float]):
        self.baseline_scores = scores

    def add_score(self, score: float):
        self.recent_scores.append(score)
        if len(self.recent_scores) > self.window_size:
            self.recent_scores.pop(0)

    def check_drift(self) -> dict:
        if len(self.recent_scores) < 10 or len(self.baseline_scores) < 10:
            return {"drift_detected": False, "reason": "Insufficient data"}

        t_stat, p_value = stats.ttest_ind(self.baseline_scores, self.recent_scores)

        baseline_mean = np.mean(self.baseline_scores)
        recent_mean = np.mean(self.recent_scores)
        delta = recent_mean - baseline_mean

        drift_detected = p_value < self.p_value_threshold and delta < 0

        return {
            "drift_detected": drift_detected,
            "baseline_mean": round(baseline_mean, 4),
            "recent_mean": round(recent_mean, 4),
            "delta": round(delta, 4),
            "p_value": round(p_value, 6),
            "t_statistic": round(t_stat, 4),
            "direction": "degraded" if delta < 0 else "improved" if delta > 0 else "stable",
        }
```

### CI/CD Integration

```python
class RegressionTestRunner:
    def __init__(self, golden_dataset: GoldenDatasetManager,
                 gate_evaluator: QualityGateEvaluator,
                 similarity_checker: SemanticSimilarityChecker):
        self.dataset = golden_dataset
        self.gates = gate_evaluator
        self.similarity = similarity_checker

    async def run_regression(self, model_client) -> dict:
        results = []
        for case in self.dataset.cases:
            response = await model_client.generate(case.input_prompt)
            comparison = await self.similarity.compare(case.expected_output, response)

            results.append({
                "case_id": case.id,
                "category": case.category,
                "difficulty": case.difficulty,
                "similarity": comparison["similarity"],
                "verdict": comparison["verdict"],
                "passed": comparison["passed"],
            })

        # Compute metrics
        metrics = self._compute_metrics(results)

        # Evaluate gates
        gate_result = self.gates.evaluate(metrics)

        return {
            "metrics": metrics,
            "gate_result": gate_result,
            "details": results,
            "deployment_allowed": gate_result["overall_passed"],
        }

    def _compute_metrics(self, results: list[dict]) -> dict:
        passed = [r for r in results if r["passed"]]
        metrics = {
            "overall_pass_rate": len(passed) / len(results) if results else 0,
            "overall_avg_similarity": sum(r["similarity"] for r in results) / len(results) if results else 0,
        }

        # Per-category metrics
        categories = set(r["category"] for r in results)
        for cat in categories:
            cat_results = [r for r in results if r["category"] == cat]
            cat_passed = [r for r in cat_results if r["passed"]]
            metrics[f"{cat}_pass_rate"] = len(cat_passed) / len(cat_results) if cat_results else 0
            metrics[f"{cat}_avg_similarity"] = sum(r["similarity"] for r in cat_results) / len(cat_results) if cat_results else 0

        return metrics
```

## Best Practices

1. Start with 50-100 golden test cases covering your core use cases, then expand to 500+
2. Use semantic similarity (embedding cosine) rather than exact match for output comparison
3. Set different quality thresholds per category — safety-critical tasks need higher bars
4. Run regression tests on every model update, prompt change, and infrastructure modification
5. Store golden datasets in version control alongside the code they test
6. Implement gradual rollout — run regression on 10% of traffic before full deployment
7. Track per-case pass rates over time to identify flaky test cases
8. Use A/B comparison rather than absolute scores when evaluating model updates
9. Automate golden dataset expansion from human feedback in production
10. Keep golden dataset review cycles — stale test cases become noise

## Common Pitfalls

- Using exact string matching for LLM outputs — produces false positives due to paraphrasing
- Not updating golden datasets as requirements evolve — stale tests block valid improvements
- Setting quality thresholds too high — causes deployment gridlock from minor variations
- Ignoring category-level regression — aggregate scores can mask category-specific degradation
- Not controlling for temperature — set temperature=0 for deterministic regression testing
- Missing embedding cache — re-embedding golden outputs on every run wastes compute
- Not versioning golden datasets alongside code — leads to test/code mismatch
- Treating all regressions equally — safety regressions should block, style regressions should warn

## References

- "Regression Testing for AI: Challenges and Strategies" (Google, 2024)
- "Semantic Similarity for LLM Output Validation" (Various, 2024)
- LLM evaluation frameworks: lm-eval-harness, OpenCompass
- Embedding models for similarity: text-embedding-3-small, BGE, E5
