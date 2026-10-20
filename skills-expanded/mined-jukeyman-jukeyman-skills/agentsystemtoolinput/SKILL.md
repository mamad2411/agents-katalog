---
name: agentsystemtoolinput
description: agent.system.tool.input
---

# agent.system.tool.input

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **agent.system.tool.input**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/_RECENT-PROJECTS/ai-systems/agent-zero/prompts/agent.system.tool.input.md`

## 🧠 Master Agent Prompt & Capabilities

### input:
use keyboard arg for terminal program input
use session arg for terminal session number
answer dialogues enter passwords etc
not for browser
usage:
~~~json
{
    "thoughts": [
        "The program asks for Y/N...",
    ],
    "headline": "Responding to terminal program prompt",
    "tool_name": "input",
    "tool_args": {
        "keyboard": "Y",
        "session": 0
    }
}
~~~

