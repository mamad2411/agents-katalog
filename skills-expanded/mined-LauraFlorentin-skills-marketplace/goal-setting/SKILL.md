---
name: goal-setting
description: An iterative pattern where an agent defines clear success criteria and continuously evaluates its progress, adjusting its actions until the goal is achieved. Use when user asks to "set agent goals", "define objectives for my agent", "goal decomposition", or mentions goal hierarchies, sub-goals, or objective functions.
---

# Goal Setting & Monitoring

Goal Setting is the process of defining *what* success looks like before starting work. Monitoring is the continuous loop of checking "Are we there yet?". Together, they allow an agent to maintain focus over long horizons. Instead of executing a single prompt, the agent enters a loop: **Act -> Observe -> Evaluate -> Adjust**.

## Use Cases

-   **Test-Driven Development (TDD)**: Goal = "All tests pass". Loop: Write code -> Run tests -> Fix errors -> Repeat.
-   **Research**: Goal = "Find 5 sources". Loop: Search -> Count sources -> Search more if < 5.
-   **Content Polish**: Goal = "Score > 8/10 on readability". Loop: Rewrite -> Evaluate -> Rewrite.

## Implementation Pattern

```python
def goal_loop(objective, criteria):
    # Step 1: Initialize
    current_state = get_initial_state()
    iterations = 0
    max_iterations = 10
    
    while iterations < max_iterations:
        # Step 2: Check Goal
        status = evaluator.check(
            goal=objective, 
            criteria=criteria, 
            current_state=current_state
        )
        
        if status.is_complete:
            return current_state
            
        print(f"Goal not met: {status.feedback}")
        
        # Step 3: Act to reduce gap
        # The agent sees the feedback and tries to fix it.
        action = planner.decide_next_step(
            goal=objective, 
            feedback=status.feedback
        )
        current_state = execute(action)
        
        iterations += 1
        
    raise TimeoutError("Goal not reached within iteration limit.")
```


## Examples

**Input**: "Help my agent understand its goal: improve customer retention by 10% in Q2."

**Goal decomposition output**:
```
Top-level goal: Increase Q2 retention by 10%
├── Sub-goal 1: Identify at-risk customers (churn score >0.7)
│   ├── Task: Pull last 90 days usage data
│   └── Task: Run churn prediction model
├── Sub-goal 2: Design intervention campaigns
│   ├── Task: Draft win-back email sequences
│   └── Task: Configure trigger conditions
└── Sub-goal 3: Measure impact
    └── Task: Track Week-1 / Week-4 retention cohorts
```


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Agent pursues irrelevant sub-goals | Goal too vague | Add measurable success criteria (KPI + target number + deadline) |
| Goal decomposition is too deep | No max depth set | Cap at 3 levels; use task locks for leaf nodes |
| Agent declares goal achieved prematurely | Missing verification step | Require explicit metric check before marking goal complete |
| Conflicting sub-goals | No dependency graph | Build a DAG of sub-goals; resolve conflicts before execution |
