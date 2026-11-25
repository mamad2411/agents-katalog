---
name: resource-optimization
description: A routing pattern that optimizes for cost and latency by dynamically selecting the most efficient model or tool for a given task complexity. Use when user asks to "optimize agent resources", "reduce token usage", "efficient agent", or mentions cost optimization, latency reduction, or throughput.
---

# Resource-Aware Optimization

Not every task requires the smartest, most expensive model. Resource-Aware Optimization (or Dynamic Routing) classifies the complexity of a user request and routes it to the most appropriate model tier. This ensures you aren't using a sledgehammer to crack a nut, saving money and improving speed.

## Use Cases

-   **Tiered Chatbot**: 
    -   Simple (Greetings, FAQs) -> gpt-4o-mini
    -   Medium (Summarization, extraction) -> gpt-4o
    -   Complex (Coding, Reasoning) -> o1-preview
-   **Cascade**: Try Llama-70B -> if confidence < 0.8 -> Try GPT-4.
-   **SLA-based**: Free users -> Small Model. Paid users -> Large Model.

## Implementation Pattern

```python
def optimize_resources(task):
    # Step 1: Complexity Analysis
    # Use a very cheap model or heuristics
    complexity = classifier.classify(task)
    
    # Step 2: Dynamic Selection
    if complexity == "SIMPLE":
        model = "gpt-4o-mini"
    elif complexity == "HARD":
        model = "gpt-4o"
    else:
        model = "o1-preview" # For reasoning heavy tasks
        
    print(f"Routing to {model} for efficiency.")
    
    # Step 3: Execute
    return llm.generate(task, model=model)
```


## Examples

**Input**: "My agent costs $2 per run and I need it under $0.50."

**Optimization audit**:
| Step | Model Used | Tokens | Cost | Needed? |
|---|---|---|---|---|
| Document summary | GPT-4o | 12,000 | $0.18 | ✅ High complexity |
| Format conversion | GPT-4o | 4,000 | $0.06 | ❌ Switch to GPT-4o-mini |
| Final answer | GPT-4o | 8,000 | $0.12 | ✅ Customer-facing |

**After optimization**: format step uses GPT-4o-mini → saves $0.05/run → now $1.95/run. Further: cache repeated document summaries → estimated $1.40 savings.


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Costs still high after optimization | Uncached repeated calls | Implement semantic cache with 24h TTL for deterministic queries |
| Switching to smaller model degraded quality | Task above model capability | Use router: small model for routing, large model only for core reasoning |
| Latency increased after optimization | Added caching overhead | Use async cache warming; pre-populate cache at job start |
| Token count growing over time | Prompt not being trimmed | Summarize conversation history every 10 turns; inject summary only |
