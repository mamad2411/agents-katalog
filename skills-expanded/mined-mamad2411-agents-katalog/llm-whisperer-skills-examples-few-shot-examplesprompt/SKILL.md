# Few-Shot Examples

## Overview

Few-shot learning with LLMs relies on providing carefully selected examples in the prompt to guide model behavior without any weight updates. The quality, diversity, and ordering of these examples significantly impact performance. This skill covers strategies for selecting, formatting, and optimizing few-shot examples to maximize task performance.

Effective few-shot prompting is both an art and a science: examples must be representative of the target task, diverse enough to cover edge cases, and formatted consistently to avoid confusing the model. Research shows that example selection can cause 20-40% variance in task accuracy, making it one of the highest-leverage optimization points for LLM applications.

## Key Concepts

- **Example Selection**: Choosing demonstrations that are representative, diverse, and relevant to the target input
- **Example Ordering**: The sequence of examples affects model attention and performance — place the most relevant examples last
- **Label Balance**: Ensuring examples cover all possible output classes proportionally
- **Semantic Similarity**: Selecting examples that are semantically close to the query input
- **Chain-of-Thought Examples**: Including reasoning steps in examples to elicit step-by-step thinking
- **Calibrated Confidence**: Using examples to calibrate model confidence and uncertainty estimation

## Implementation Patterns

### Select examples by semantic similarity

```python
import numpy as np
from sentence_transformers import SentenceTransformer

class FewShotSelector:
    def __init__(self, examples: list[dict], embedding_model: str = "all-MiniLM-L6-v2"):
        self.examples = examples
        self.encoder = SentenceTransformer(embedding_model)
        self.embeddings = self.encoder.encode(
            [ex["input"] for ex in examples],
            normalize_embeddings=True,
        )

    def select(self, query: str, k: int = 5, strategy: str = "similar") -> list[dict]:
        """Select k examples for the given query."""
        query_emb = self.encoder.encode([query], normalize_embeddings=True)[0]

        # Compute similarities
        scores = np.dot(self.embeddings, query_emb)

        if strategy == "similar":
            indices = np.argsort(scores)[-k:][::-1]
        elif strategy == "diverse":
            indices = self._diverse_selection(scores, k)
        elif strategy == "balanced":
            indices = self._balanced_selection(scores, k)
        else:
            indices = np.argsort(scores)[-k:][::-1]

        return [self.examples[i] for i in indices]

    def _diverse_selection(self, scores: np.ndarray, k: int) -> list[int]:
        """Select diverse examples using MMR (Maximal Marginal Relevance)."""
        selected = []
        remaining = set(range(len(scores)))

        # Start with most similar
        best = np.argmax(scores)
        selected.append(best)
        remaining.remove(best)

        while len(selected) < k and remaining:
            best_score = -float("inf")
            best_idx = -1

            for idx in remaining:
                # Relevance score
                rel = scores[idx]
                # Diversity penalty (min distance to already selected)
                div = min(
                    1 - np.dot(self.embeddings[idx], self.embeddings[s])
                    for s in selected
                )
                mmr = 0.7 * rel + 0.3 * div
                if mmr > best_score:
                    best_score = mmr
                    best_idx = idx

            selected.append(best_idx)
            remaining.remove(best_idx)

        return selected

    def _balanced_selection(self, scores: np.ndarray, k: int) -> list[int]:
        """Select examples with balanced label distribution."""
        labels = [ex.get("label", "") for ex in self.examples]
        unique_labels = list(set(labels))
        per_label = max(1, k // len(unique_labels))

        selected = []
        for label in unique_labels:
            label_indices = [i for i, l in enumerate(labels) if l == label]
            label_scores = [(i, scores[i]) for i in label_indices]
            label_scores.sort(key=lambda x: x[1], reverse=True)
            selected.extend([i for i, _ in label_scores[:per_label]])

        return selected[:k]
```

### Format few-shot prompt

```python
def build_few_shot_prompt(
    query: str,
    examples: list[dict],
    system_prompt: str = "",
    template: str = "Input: {input}\nOutput: {output}",
    separator: str = "\n\n",
) -> str:
    """Build a few-shot prompt from examples and query."""
    parts = []

    if system_prompt:
        parts.append(system_prompt)

    for ex in examples:
        parts.append(template.format(**ex))

    parts.append(template.format(input=query, output=""))

    return separator.join(parts)


# Example usage
examples = [
    {"input": "The movie was great!", "output": "positive"},
    {"input": "Terrible waste of time.", "output": "negative"},
    {"input": "It was okay, nothing special.", "output": "neutral"},
]

prompt = build_few_shot_prompt(
    query="I loved every minute of it!",
    examples=examples,
    system_prompt="Classify the sentiment of the following text.",
)
```

## Best Practices

1. Select 3-8 examples for most tasks — fewer may under-specify the task, more may cause context dilution
2. Place the most similar example to the query last, as recency bias makes the model attend more to recent examples
3. Include at least one example per output class to prevent label bias
4. Use chain-of-thought examples for reasoning tasks to elicit step-by-step thinking
5. Keep example formatting consistent — even small variations in formatting can confuse the model
6. Test example sensitivity by shuffling and reselecting — robust prompts should be stable across example choices
7. Use calibrated examples with confidence scores when you need the model to express uncertainty
8. Cache example embeddings and pre-compute similarity scores for production latency

## Common Pitfalls

- Using too many examples, consuming context window and reducing performance on long inputs
- Selecting examples that are too similar, failing to demonstrate the full range of expected behavior
- Including noisy or incorrect examples that teach the model wrong patterns
- Not testing with adversarial examples that might trigger unexpected behavior
- Using examples from a different distribution than the target task
- Ignoring label distribution in examples, leading to biased predictions

## References

- Liu et al., "What Makes Good In-Context Examples for GPT-3?" (2022)
- Min et al., "Rethinking the Role of Demonstrations" (2022)
- Lu et al., "Fantastically Ordered Prompts and Where to Find Them" (2022)
- Zhang et al., "Example Selection for In-Context Learning" (2022)
