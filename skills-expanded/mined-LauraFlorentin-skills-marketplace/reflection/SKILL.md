---
name: reflection
description: A recursive pattern where an agent evaluates and critiques its own output to iteratively improve quality and catch errors. Use when user asks to "add self-reflection", "agent introspection", "self-critique", or mentions self-evaluation, meta-cognition, or quality self-assessment.
---

# Reflection

Reflection (also known as Self-Correction or Self-Refinement) gives an agent the ability to look at its work and ask, "Is this correct?" or "Can this be better?". Instead of accepting the first draft, the agent acts as its own critic, identifying flaws and generating an improved version. This significantly boosts performance on reasoning and coding tasks.

## Use Cases

-   **Code Repair**: Creating code -> Running it -> Reading the error -> Fixing the code.
-   **Writing Polish**: Drafting an email -> Critiquing tone and clarity -> Rewriting.
-   **Safety Check**: Generating a response -> Checking for policy violations -> Regenerating if unsafe.

## Implementation Pattern

```python
def reflection_workflow(task):
    # Step 1: Draft
    draft = llm_call(f"Write a draft for: {task}")
    
    # Step 2: Critique
    # The prompt explicitly asks to find problems, not just "rewrite".
    critique = llm_call(
        prompt="Critique this draft. List logical errors, tone issues, or missing info.",
        input=draft
    )
    
    # Step 3: Refine
    # The final generation sees both the draft and the specific feedback.
    final_version = llm_call(
        prompt="Rewrite the draft to address the following critique...",
        input={"draft": draft, "critique": critique}
    )
    
    return final_version
```
