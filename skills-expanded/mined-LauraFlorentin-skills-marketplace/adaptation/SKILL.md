---
name: adaptation
description: A dynamic pattern where an agent system modifies its own behavior, prompts, or tools over time based on feedback or performance metrics. Use when user asks to "make my agent adaptive", "add learning capabilities", "self-improving agent", or mentions adaptive behavior, online learning, or feedback loops.
---

# Adaptation

Adaptation enables an AI system to evolve. Instead of being static, the system monitors its own performance (or receives user feedback) and updates its configuration. This can range from simple parameter tuning to rewriting its own system prompts or code.

## Use Cases

-   **Prompt Optimization**: An "Optimizer Agent" rewrites the prompt of a "Worker Agent" based on failure cases.
-   **Code Evolution**: An agent that maintains a library of helper functions and refactors them when they become inefficient.
-   **Style Transfer**: An agent that learns to mimic the writing style of the user over time.

## Implementation Pattern

```python
def adaptation_loop(task_history):
    # Step 1: Evaluate Performance
    # Analyze recent logs to find recurring failures or weak spots.
    performance_report = evaluator.analyze(task_history)
    
    if performance_report.score < threshold:
        # Step 2: Mutate / Optimize
        # The optimizer proposes a change to the system prompt.
        current_prompt = load_prompt()
        
        new_prompt = optimizer.run(
            prompt="Improve this prompt based on the failure analysis...",
            input={"current_prompt": current_prompt, "report": performance_report}
        )
        
        # Step 3: Update System
        save_prompt(new_prompt)
        print("System adapted with new prompt strategy.")
```
