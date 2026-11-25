---
name: evaluation
description: Systems for quantitatively and qualitatively measuring agent performance, reliability, and cost. Use when user asks to "evaluate agent performance", "benchmark my agent", "test agent quality", or mentions agent metrics, scoring, or performance assessment.
---

# Evaluation & Monitoring

Evaluation determines *how well* an agent performs (correctness, helpfulness, safety), usually on a test dataset. Monitoring determines *how the system is running* (latency, errors, cost) in a live environment. Both are essential for the lifecycle management of AI systems.

## Use Cases

-   **LLM-as-a-Judge**: Using GPT-4 to grade the answers of a smaller model.
-   **Latency Tracking**: Measuring the time-to-first-token (TTFT) and total generation time.
-   **Topic Clustering**: Analyzing user queries to see what topics are trending or failing.

## Implementation Pattern

```python
def evaluate_agent(agent, test_set):
    score = 0
    total = len(test_set)
    
    for case in test_set:
        # Run agent
        prediction = agent.run(case.input)
        
        # Evaluate vs Golden Answer
        # Simple exact match or fuzzy match
        if is_correct(prediction, case.expected):
            score += 1
        else:
            # Semantic Evaluation using an LLM Judge
            judge_score = llm_judge.evaluate(
                prediction, 
                case.expected
            )
            score += judge_score
            
    return score / total
```


## Examples

**Input**: "Evaluate whether our customer support agent is giving accurate answers."

**Evaluation run**:
```python
results = evaluator.run(
    agent=support_agent,
    test_cases=golden_dataset,  # 200 Q&A pairs
    metrics=["accuracy", "hallucination_rate", "latency_p95"]
)
# Output: accuracy=0.87, hallucination_rate=0.04, latency_p95=2.3s
```

**Interpretation**: Accuracy above threshold (0.85 ✅), hallucination rate acceptable (0.04 ✅), latency borderline — investigate slow tail cases.


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Evaluation results are inconsistent | Non-deterministic LLM judge | Set `temperature=0` on the evaluator model; add majority voting across 3 runs |
| Test set doesn't reflect real traffic | Golden dataset out of date | Sample 10% of live traffic weekly; add to golden set after human review |
| Scores improve but user complaints persist | Wrong metrics | Add user satisfaction proxy (thumbs up/down rate) to evaluation suite |
| Evaluation is slow | Running evaluations serially | Parallelize: batch 10 test cases per API call |
