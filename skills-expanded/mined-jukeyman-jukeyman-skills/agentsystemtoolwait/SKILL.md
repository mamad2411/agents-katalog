---
name: agentsystemtoolwait
description: agent.system.tool.wait
---

# agent.system.tool.wait

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **agent.system.tool.wait**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/_RECENT-PROJECTS/ai-systems/agent-zero/prompts/agent.system.tool.wait.md`

## 🧠 Master Agent Prompt & Capabilities

### wait
pause execution for a set time or until a timestamp
use args "seconds" "minutes" "hours" "days" for duration
use "until" with ISO timestamp for a specific time
usage:

1 wait duration
~~~json
{
    "thoughts": [
        "I need to wait..."
    ],
    "headline": "...",
    "tool_name": "wait",
    "tool_args": { 
        "minutes": 1, 
        "seconds": 30 
    }
}
~~~

2 wait timestamp
~~~json
{
    "thoughts": [
        "I will wait until..."
    ],
    "headline": "...",
    "tool_name": "wait",
    "tool_args": { 
        "until": "2025-10-20T10:00:00Z" 
    }
}
~~~

