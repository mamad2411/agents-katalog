---
name: routing
description: A control flow pattern where a central component classifies an input request and directs it to the most appropriate specialized agent or tool. Use when user asks to "route between agents", "agent routing", "task dispatch", or mentions classifier routing, intent detection, or agent selection.
---

# Routing

Routing acts as the traffic controller for an agentic system. Instead of a single generalist agent trying to handle every type of user request, a "Router" (often a fast, lightweight LLM or a classifier) analyzes the intent of the incoming message and delegates it to a specialized handler. This creates a system that is modular, scalable, and easier to maintain.

## Use Cases

-   **Customer Service Dispatch**: Routing "My internet is down" to Tech Support and "How much is the upgrade?" to Sales.
-   **Model Selection**: Routing logic puzzles to o1 and creative writing to GPT-4.
-   **Tool Selection**: Deciding whether to use a Search tool, a Calculator, or a Database Query tool based on the question.

## Implementation Pattern

```python
def routing_workflow(user_query):
    # Step 1: Classification
    # The router's only job is to pick the right path.
    intent = classify_intent(
        prompt="Classify this query into: [SALES, SUPPORT, BILLING]",
        input=user_query
    )
    
    # Step 2: Delegation
    # Based on the intent, we call a specific sub-agent.
    if intent == "SALES":
        return sales_agent.run(user_query)
    elif intent == "SUPPORT":
        return support_agent.run(user_query)
    elif intent == "BILLING":
        return billing_agent.run(user_query)
    else:
        return default_agent.run(user_query)
```


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Wrong agent selected | Classifier underfitted | Add 50+ labeled examples per class; re-train or few-shot prompt |
| New query types not routed | No catch-all route | Add a "general" fallback route that handles out-of-distribution inputs |
| Routing adds too much latency | Heavy classifier | Use a lightweight keyword router as first stage; only call LLM when uncertain |
| Router and agent disagree on task scope | Misaligned schemas | Define a shared task schema; router populates it, agent consumes it |
