---
name: prioritization
description: A management pattern where an agent assesses the urgency and importance of incoming tasks to organize a dynamic execution queue. Use when user asks to "prioritize tasks", "rank agent actions", "task ordering", or mentions priority queues, urgency scoring, or triage.
---

# Prioritization

Prioritization allows an agent to work smarter, not just harder. Instead of processing tasks First-In-First-Out (FIFO), a "Manager Agent" analyzes each request's urgency and business value. It assigns a priority score (P0, P1, P2) and reorders the queue effectively. This is vital for resource-constrained environments.

## Use Cases

-   **Ticket Triage**: Analyzing support tickets and tagging them as "Critical" (Server Down) or "Low" (Typo).
-   **Inbox Management**: Sorting emails by "Needs Reply", "Read Later", and "Spam".
-   **Agent Dispatch**: A Project Manager agent assigning urgent bugs to Senior Dev Agents and documentation tasks to Junior Agents.

## Implementation Pattern

```python
def prioritization_loop(task_queue):
    while True:
        # Step 1: Ingest
        new_request = ingest_request()
        
        # Step 2: Assess Priority
        # Manager agent determines importance
        priority_score = manager_agent.evaluate(
            prompt="Rate urgency 1-10",
            input=new_request
        )
        
        # Step 3: Insert into Priority Queue
        task_queue.push(new_request, priority=priority_score)
        
        # Step 4: Process Highest Priority
        next_task = task_queue.pop()
        worker_agent.run(next_task)
```


## Examples

**Input**: "I have 12 tasks to do today. Help me prioritize."

**RICE scoring output**:
| Task | Reach | Impact | Confidence | Effort | RICE Score |
|---|---|---|---|---|---|
| Fix login bug | 5000 | 3 | 90% | 1 | 13,500 |
| Add dark mode | 800 | 2 | 70% | 5 | 224 |
| Write docs | 200 | 1 | 80% | 2 | 80 |

**Recommendation**: Fix the login bug first — 60× higher RICE score than the next item.

---

**Input**: "We have 30 backlog items for this sprint. What goes in?"

**Output**: MoSCoW matrix with Must/Should/Could/Won't labels, sprint capacity check, and a risk-adjusted ordered list.


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| All items score similarly | Inputs too vague | Ask for specific numbers (user count, revenue impact) before scoring |
| Stakeholders reject prioritization | No buy-in on criteria | Surface the scoring rubric *before* running; get alignment on weights |
| High-priority item blocked | Dependency not captured | Add a dependency pre-check step before finalizing the ordered list |
| Scores feel arbitrary | Missing confidence calibration | Require a confidence percentage for each estimate |
