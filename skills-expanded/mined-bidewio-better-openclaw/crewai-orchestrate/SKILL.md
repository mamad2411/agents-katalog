---
name: crewai-orchestrate
description: Multi-agent orchestration with CrewAI
version: 1.0.0
tags: [ai, agents, multi-agent, orchestration]
---

# CrewAI – Multi-Agent Orchestration

CrewAI orchestrates role-playing AI agents for collaborative tasks —
assign roles, goals, and tools to create AI teams.

- **GitHub**: github.com/crewAIInc/crewAI (30 000+ ⭐)
- **License**: MIT
- **Security**: Active development. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{CREWAI_API_URL}}` | CrewAI deployment API URL (if hosted) |

## Usage Examples

### Define and run a crew (Python)

```python
from crewai import Agent, Task, Crew

researcher = Agent(role="Researcher", goal="Find latest AI trends")
writer = Agent(role="Writer", goal="Write a summary article")

research_task = Task(description="Research AI agent frameworks", agent=researcher)
write_task = Task(description="Write article from research", agent=writer)

crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task])
result = crew.kickoff()
print(result)
```

## AI Agent Tips

- Agents have roles, goals, backstory, and tool access.
- Sequential and hierarchical process modes.
- Independent of LangChain — works with any LLM provider.
- Ideal for content creation, research, and analysis workflows.
