---
name: agentsystemtoolexample_tool
description: agent.system.tool.example tool
---

# agent.system.tool.example tool

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **agent.system.tool.example tool**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/_RECENT-PROJECTS/ai-systems/agent-zero/agents/_example/prompts/agent.system.tool.example_tool.md`

## 🧠 Master Agent Prompt & Capabilities

### example_tool:
example tool to test functionality
this tool is automatically included to system prompt because the file name is "agent.system.tool.*.md"
usage:
~~~json
{
    "thoughts": [
        "Let's test the example tool...",
    ],
    "headline": "Testing example tool",
    "tool_name": "example_tool",
    "tool_args": {
        "test_input": "XYZ",
    }
}
~~~

