---
name: parallelization
description: A concurrency pattern where multiple agent tasks are executed at the same time to speed up processing or gather diverse perspectives. Use when user asks to "run agents in parallel", "parallelize tasks", "concurrent execution", or mentions parallel processing, fan-out, or batch execution.
---

# Parallelization

Parallelization allows an agentic system to perform multiple independent operations simultaneously. This is commonly used in distinct flavors: "Sectioning" (breaking a large task into independent chunks to process in parallel) and "Voting" (running the same task multiple times to get diverse outputs for consensus or increasing quality).

## Use Cases

-   **Batch Processing**: Grading 100 student essays concurrently.
-   **Multi-Perspective Analysis**: Asking a "Skeptic Agent", an "Optimist Agent", and a "Realist Agent" to review a plan simultaneously.
-   **Map-Reduce**: Identifying key themes in 50 documents by summarizing them all in parallel (Map) and then synthesizing the summaries (Reduce).

## Implementation Pattern

```python
import asyncio

async def parallel_workflow(topic):
    # Define independent tasks
    tasks = [
        research_agent.run(f"Research history of {topic}"),
        research_agent.run(f"Research economic impact of {topic}"),
        research_agent.run(f"Research cultural significance of {topic}")
    ]
    
    # Execute all concurrently
    # This takes as long as the slowest single task, not the sum of all tasks.
    results = await asyncio.gather(*tasks)
    
    # Synthesize results
    final_report = synthesize_agent.run(
        prompt="Combine these research findings into a report...",
        input=results
    )
    
    return final_report
```


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Race conditions | Shared mutable state | Use immutable message passing; collect results only in the aggregator |
| One slow task blocks completion | No partial results | Set a per-task timeout; return partial results after timeout |
| Rate limits hit with parallelization | Too many concurrent API calls | Add a semaphore (e.g., `asyncio.Semaphore(10)`) to cap concurrency |
| Results aggregated in wrong order | Non-deterministic completion order | Tag each result with its task ID; sort before aggregating |
