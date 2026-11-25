---
name: multi-agent-collaboration
description: A structural pattern where multiple specialized agents communicate and coordinate to solve a problem that is too complex for a single agent. Use when user asks to "build a multi-agent system", "agents working together", "agent collaboration", or mentions team of agents, distributed agents, or swarm.
---

# Multi-Agent Collaboration

Multi-Agent Collaboration (MAC) involves a team of agents, each with a specific role, tools, and persona. They work together by exchanging messages, handing off tasks, or debating solutions. This mimics human organizational structures (e.g., a software team with a PM, Dev, and QA).

## Use Cases

-   **Software Dev Team**: Product Manager -> Developer -> Reviewer -> QA.
-   **Debate**: Proposition Agent vs. Opposition Agent -> Moderator synthesizes.
-   **Creative Writing Room**: Idea Generator -> Plot Outliner -> Dialogue Specialist -> Editor.

## Implementation Pattern

```python
class Agent:
    def process(self, message):
        # ... logic ...
        return response

def collaboration_workflow(task):
    # Define Roles
    researcher = Agent(role="Researcher", tools=[search_tool])
    writer = Agent(role="Writer", tools=[editor_tool])
    reviewer = Agent(role="Reviewer", prompt="Critique for accuracy")

    # Flow
    # 1. Research
    facts = researcher.process(f"Gather facts on: {task}")
    
    # 2. Write Draft
    draft = writer.process(f"Write an article using these facts: {facts}")
    
    # 3. Review & Iterate
    feedback = reviewer.process(draft)
    if feedback.has_issues:
        final_draft = writer.process(f"Fix these issues: {feedback}")
    else:
        final_draft = draft
        
    return final_draft
```
