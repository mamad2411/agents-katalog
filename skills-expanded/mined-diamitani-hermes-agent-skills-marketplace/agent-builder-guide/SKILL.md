---
name: agent-builder-guide
description: "Use when guiding users through building AI agents with SDKs, Restack, MCP, API integration, or platforms like Relevance.ai. Consolidates Agent Builder Guide, FlowBud, and Relevance AI builders."
version: "1.0"
tags:
  - ai-agents
  - restack
  - mcp
  - relevance-ai
  - agent-sdk
  - multi-agent
  - tool-use
---

# Agent Builder Guide

## Overview

Guides users through building AI agents — from simple single-agent assistants to multi-agent orchestration systems. Covers SDK-based development (OpenAI Agents SDK, LangChain, CrewAI), platform-based builders (Relevance.ai, FlowBud), Restack workflows, and MCP (Model Context Protocol) tool integration.

## When to Use

- A user wants to build their first AI agent
- Choosing between SDK-based vs. platform-based agent development
- Designing a multi-agent system with task delegation
- Integrating MCP tools into an agent
- Building a Restack workflow with AI steps
- Setting up an agent on Relevance.ai for business automation
- Debugging agent tool-calling or reasoning failures

## How It Works

1. **Use Case Classification** — Determine the agent's complexity and requirements.
2. **Architecture Selection** — Match to the right building approach.
3. **Agent Design** — Define the agent's role, tools, memory, and orchestration.
4. **Implementation Guide** — Provide platform-specific or SDK-specific build instructions.
5. **Testing & Iteration** — Validate agent behavior and tool use.

## Steps

### Step 1: Use Case Classification
Categorize the agent:
- **Simple assistant**: Single agent, few tools, stateless (Q&A, summarization, classification)
- **Tool-augmented agent**: Single agent with 3-10 tools (research, data fetching, actions)
- **Workflow agent**: Multi-step process with conditional branching (Restack, LangGraph)
- **Multi-agent system**: Multiple specialized agents collaborating (CrewAI, AutoGen)
- **Platform agent**: Business-facing agent on Relevance.ai or similar

### Step 2: Architecture Decision Matrix

| Use Case | Recommended Approach | Why |
|----------|---------------------|-----|
| Simple Q&A bot | OpenAI custom GPT or Assistants API | Fastest to deploy, no code |
| Tool-using agent (dev) | OpenAI Agents SDK | Native function calling, streaming |
| Tool-using agent (Python) | LangChain + LangGraph | Most integrations, large ecosystem |
| Multi-agent (Python) | CrewAI | Role-based agents, simple API |
| Workflow with AI steps | Restack | Durable execution, retries, observability |
| No-code agent (business) | Relevance.ai | Visual builder, built-in tools, deployment |
| MCP tool integration | MCP SDK + any agent framework | Standardized tool protocol |

### Step 3: Agent Design Template
For any agent, define:
```yaml
agent:
  name: ResearchAgent
  role: >
    You are a research analyst that gathers information from multiple sources,
    synthesizes findings, and produces structured reports.
  tools:
    - web_search: Search the web for current information
    - arxiv_search: Search academic papers
    - read_url: Fetch and extract content from a URL
    - database_query: Query the internal knowledge base
  memory:
    type: conversation_buffer  # or: vector_store, summary, sliding_window
    window: 20  # last 20 messages
  orchestration:
    type: single  # or: sequential, hierarchical, debate
  constraints:
    - Always cite sources with URLs
    - Flag low-confidence findings
    - Never fabricate data — say "no information found"
```

### Step 4: Platform-Specific Implementation

**OpenAI Agents SDK (Python):**
```python
from agents import Agent, Runner, WebSearchTool, function_tool

@function_tool
def read_url(url: str) -> str:
    """Fetch and extract text content from a URL."""
    ...

agent = Agent(
    name="ResearchAgent",
    instructions="You are a research analyst...",
    tools=[WebSearchTool(), read_url],
)

result = Runner.run_sync(agent, "Research: quantum computing breakthroughs 2024")
print(result.final_output)
```

**CrewAI (Multi-Agent):**
```python
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Research Analyst",
    goal="Find and synthesize information on {topic}",
    tools=[search_tool, scrape_tool],
)

writer = Agent(
    role="Technical Writer",
    goal="Transform research into clear reports",
)

research_task = Task(description="Research {topic}", agent=researcher)
writing_task = Task(description="Write report from research", agent=writer)

crew = Crew(agents=[researcher, writer], tasks=[research_task, writing_task])
result = crew.kickoff(inputs={"topic": "quantum computing"})
```

**Restack Workflow:**
```typescript
import { workflow, step } from "@restackio/ai";

export const researchWorkflow = workflow("research", async (topic: string) => {
  const searchResults = await step("web-search", async () => {
    return await webSearchTool(topic);
  });

  const analysis = await step("analyze", async () => {
    return await llm.analyze(searchResults);
  });

  const report = await step("generate-report", async () => {
    return await llm.generate(analysis, { format: "markdown" });
  });

  return report;
});
```

**Relevance.ai (No-Code):**
1. Create new agent → Select template or blank
2. Configure agent persona + instructions in the prompt editor
3. Add tools from the marketplace (web search, database, API connectors)
4. Set up memory: Choose conversation buffer or knowledge base
5. Configure triggers: Form submission, schedule, API endpoint
6. Test in playground → Deploy as chatbot or API endpoint

**MCP Tool Integration:**
```python
# mcp_tools.py
from mcp import Server, Tool

server = Server("my-tools")

@server.tool()
async def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Weather in {city}: 72°F, sunny"
```

### Step 5: Testing Framework
For every agent, test:
1. **Tool calling accuracy**: Does it use the right tool for the right job?
2. **Tool error recovery**: What happens when a tool returns an error?
3. **Instruction adherence**: Does the agent follow its role and constraints?
4. **Multi-turn coherence**: Does it maintain context across 10+ turns?
5. **Hallucination check**: Does it fabricate tool results or data?
6. **Rate limit handling**: What happens under high concurrency?

### Step 6: Deployment Checklist
- [ ] Environment variables configured (API keys, endpoints)
- [ ] Tool timeout limits set (default: 30s per tool call)
- [ ] Logging/monitoring enabled (track tool calls, errors, latency)
- [ ] Rate limiting configured (max requests per user/session)
- [ ] Error fallback behavior defined (graceful degradation)
- [ ] Version pinned for all dependencies

## Common Pitfalls

- **Too many tools**: Agents get confused with 10+ tools. Start with 3-5 essential tools and add more after testing.
- **Vague tool descriptions**: The agent relies on tool names + descriptions to choose correctly. "Searches" is bad. "Searches the web using Bing API and returns top 10 results with URLs and snippets" is good.
- **No tool error handling**: Agents don't naturally recover from tool failures. Add retry logic and fallback behaviors.
- **Memory bloat**: Long conversations fill the context window. Use summarization or sliding window memory.
- **Orchestration overkill**: Not every problem needs multi-agent. A single well-designed agent with good tools often outperforms a complex multi-agent setup.

## Source

Consolidates: Agent Builder Guide GPT, FlowBud GPT, Relevance AI Builder GPT.
