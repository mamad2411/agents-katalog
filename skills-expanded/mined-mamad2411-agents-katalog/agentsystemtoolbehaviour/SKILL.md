---
name: agentsystemtoolbehaviour
description: agent.system.tool.behaviour
---

# agent.system.tool.behaviour

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **agent.system.tool.behaviour**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/_RECENT-PROJECTS/ai-systems/agent-zero/prompts/agent.system.tool.behaviour.md`

## 🧠 Master Agent Prompt & Capabilities

### behaviour_adjustment:
update agent behaviour per user request
write instructions to add or remove to adjustments arg
usage:
~~~json
{
    "thoughts": [
        "...",
    ],
    "headline": "Adjusting agent behavior per user request",
    "tool_name": "behaviour_adjustment",
    "tool_args": {
        "adjustments": "remove...",
    }
}
~~~

