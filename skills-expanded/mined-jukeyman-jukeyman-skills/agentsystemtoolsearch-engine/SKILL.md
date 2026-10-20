---
name: agentsystemtoolsearch_engine
description: agent.system.tool.search engine
---

# agent.system.tool.search engine

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **agent.system.tool.search engine**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/_RECENT-PROJECTS/ai-systems/agent-zero/prompts/agent.system.tool.search_engine.md`

## 🧠 Master Agent Prompt & Capabilities

### search_engine:
provide query arg get search results
returns list urls titles descriptions
**Example usage**:
~~~json
{
    "thoughts": [
        "...",
    ],
    "headline": "Searching web for video content",
    "tool_name": "search_engine",
    "tool_args": {
        "query": "Video of...",
    }
}
~~~

