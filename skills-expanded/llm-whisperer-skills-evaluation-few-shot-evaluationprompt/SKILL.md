# Few-Shot Evaluation Techniques

## Overview

Few-shot evaluation measures how well an LLM performs tasks given only a small number of examples (typically 1-10) in the prompt, without any parameter updates. This is the primary evaluation paradigm for large foundation models accessed via API, where fine-tuning is impractical or unnecessary. Few-shot evaluation reveals in-context learning ability — the model's capacity to recognize task patterns from minimal demonstrations and generalize to new inputs.

The choice of examples, their order, format, and diversity significantly impact measured performance, making few-shot evaluation as much an art as a science. A robust evaluation protocol must control for these confounds to produce reliable, comparable scores. This skill covers designing few-shot evaluations that are fair, reproducible, and predictive of real-world performance.

## Key Concepts

- **K-shot Evaluation**: Testing with K demonstrations prepended to each query (0-shot, 1-shot, 3-shot, 5-shot are common)
- **Example Selection Strategy**: How to choose demonstrations — random, diverse, similar, or adversarial
- **Example Ordering Effects**: The order of demonstrations can cause 5-15% score variation; robust evaluation averages over permutations
- **Format Consistency**: Demonstrations must match the expected output format exactly; formatting inconsistencies degrade performance
- **Calibration Effects**: Few-shot examples can bias the model toward certain answer distributions regardless of correctness
- **In-Context Learning Curves**: Plotting performance vs. number of shots reveals learning rate and saturation points
- **Cross-Task Transfer**: Whether few-shot examples from related tasks help on the target task
- **Dynamic Example Selection**: Using retrieval to find the most relevant examples for each query

## Implementation Patterns

```python
import random
from dataclasses import dataclass
from typing import Callable

@dataclass
class FewShotExample:
    input: str
    output: str
    metadata: dict | None = None

@dataclass
class FewShotConfig:
    num_shots: list[int]  # e.g., [0, 1, 3, 5, 10]
    num_permutations: int = 5
    selection_strategy: str = "random"  # random, diverse, similar
    seed: int = 42

class FewShotEvaluator:
    def __init__(self, config: FewShotConfig):
        self.config = config
        random.seed(config.seed)

    def build_prompt(self, query: str, examples: list[FewShotExample],
                     task_instruction: str = "") -> str:
        parts = []
        if task_instruction:
            parts.append(task_instruction)
            parts.append("")
        for ex in examples:
            parts.append(f"Input: {ex.input}")
            parts.append(f"Output: {ex.output}")
            parts.append("")
        parts.append(f"Input: {query}")
        parts.append("Output:")
        return "\n".join(parts)

    def select_examples(self, pool: list[FewShotExample],
                       k: int, strategy: str = "random") -> list[FewShotExample]:
        if k >= len(pool):
            return pool[:k]
        if strategy == "random":
            return random.sample(pool, k)
        elif strategy == "diverse":
            return self._diverse_selection(pool, k)
        elif strategy == "similar":
            return pool[:k]  # assumes pre-sorted by similarity
        return random.sample(pool, k)

    def _diverse_selection(self, pool: list[FewShotExample], k: int) -> list[FewShotExample]:
        """Select maximally diverse examples by length and content."""
        selected = [pool[0]]
        remaining = pool[1:]
        while len(selected) < k and remaining:
            best = max(remaining, key=lambda ex: min(
                self._distance(ex, s) for s in selected
            ))
            selected.append(best)
            remaining.remove(best)
        return selected

    def _distance(self, a: FewShotExample, b: FewShotExample) -> float:
        a_words = set(a.input.lower().split())
        b_words = set(b.input.lower().split())
        intersection = len(a_words & b_words)
        union = len(a_words | b_words)
        return 1.0 - (intersection / union if union > 0 else 0.0)

    def evaluate(self, model_fn: Callable, test_set: list[dict],
                example_pool: list[FewShotExample],
                task_instruction: str = "") -> dict:
        results = {}

        for k in self.config.num_shots:
            k_results = []
            for perm in range(self.config.num_permutations):
                scores = []
                for sample in test_set:
                    examples = self.select_examples(example_pool, k, self.config.selection_strategy)
                    prompt = self.build_prompt(sample["input"], examples, task_instruction)
                    prediction = model_fn(prompt)
                    score = self._score(prediction, sample["expected"])
                    scores.append(score)
                k_results.append(sum(scores) / len(scores) if scores else 0.0)

            results[f"{k}-shot"] = {
                "mean": round(sum(k_results) / len(k_results), 4),
                "std": round(self._std(k_results), 4),
                "min": round(min(k_results), 4),
                "max": round(max(k_results), 4),
                "num_permutations": self.config.num_permutations,
            }

        # Learning curve analysis
        means = [results[f"{k}-shot"]["mean"] for k in self.config.num_shots]
        results["learning_curve"] = {
            "shots": self.config.num_shots,
            "scores": means,
            "improvement_rate": round((means[-1] - means[0]) / max(len(means) - 1, 1), 4),
        }
        return results

    def _score(self, prediction: str, expected: str) -> float:
        return 1.0 if prediction.strip().lower() == expected.strip().lower() else 0.0

    def _std(self, values: list[float]) -> float:
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return variance ** 0.5


def order_sensitivity_test(model_fn: Callable, examples: list[FewShotExample],
                          query: str, expected: str, n_trials: int = 20) -> dict:
    """Test how much example ordering affects model output."""
    import itertools
    results = []
    perms = list(itertools.permutations(examples))
    if len(perms) > n_trials:
        perms = random.sample(perms, n_trials)

    evaluator = FewShotEvaluator(FewShotConfig(num_shots=[len(examples)]))
    for perm in perms:
        prompt = evaluator.build_prompt(query, list(perm))
        pred = model_fn(prompt)
        results.append(pred.strip().lower() == expected.strip().lower())

    accuracy = sum(results) / len(results)
    return {
        "num_permutations_tested": len(perms),
        "accuracy_mean": round(accuracy, 4),
        "order_sensitivity": round(1.0 - accuracy, 4) if accuracy < 1.0 else 0.0,
        "all_correct": all(results),
        "all_wrong": not any(results),
    }
```

## Best Practices

1. **Test multiple shot counts** — Always evaluate at 0, 1, 3, 5, and 10 shots to map the full learning curve
2. **Average over permutations** — Run at least 5 random orderings per shot count to account for order sensitivity
3. **Use diverse example selection** — Diverse demonstrations outperform random selection by 3-8% on average
4. **Match demonstration format** — Output format in demonstrations must exactly match expected output format
5. **Report confidence intervals** — Always report mean ± std across permutations, not single-run scores
6. **Control for example quality** — Bad or ambiguous examples hurt more than no examples; curate the pool carefully
7. **Test zero-shot as baseline** — 0-shot performance establishes the floor; few-shot gains above it indicate true in-context learning
8. **Use consistent example pools** — Same pool across all models being compared to ensure fair comparison
9. **Document selection strategy** — Report exactly how examples were chosen so others can reproduce results
10. **Check for label leakage** — Ensure demonstrations don't accidentally contain the test query or answer

## Common Pitfalls

- **Single permutation reporting**: Reporting results from one ordering when order effects are significant
- **Inconsistent formats**: Mixing "Answer:" and "Output:" labels across demonstrations confuses the model
- **Too many shots**: Beyond 10-15 shots, performance often degrades due to context window pressure and attention dilution
- **Cherry-picked examples**: Selecting demonstrations that artificially inflate scores on specific test cases
- **Ignoring zero-shot**: Not comparing against 0-shot makes it impossible to know if few-shot actually helps
- **Leaking test data**: Including test samples in the demonstration pool inflates scores artificially

## References

- [Few-Shot Learners (GPT-3 paper)](https://arxiv.org/abs/2005.14165) — Original in-context learning paper
- [Larger language models do in-context learning differently](https://arxiv.org/abs/2303.03846) — Research on scaling and ICL
- [Fantastically Ordered Prompts](https://arxiv.org/abs/2104.08786) — Research on example ordering effects
- [Active Example Selection](https://arxiv.org/abs/2211.04486) — Dynamic example selection strategies
