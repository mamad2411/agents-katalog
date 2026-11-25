---
name: agentsystemtoolbrowser
description: agent.system.tool.browser
---

# agent.system.tool.browser

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **agent.system.tool.browser**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/_RECENT-PROJECTS/ai-systems/agent-zero/prompts/agent.system.tool.browser.md`

## 🧠 Master Agent Prompt & Capabilities

### browser_agent:

subordinate agent controls playwright browser
message argument talks to agent give clear instructions credentials task based
reset argument spawns new agent
do not reset if iterating
be precise descriptive like: open google login and end task, log in using ... and end task
when following up start: considering open pages
dont use phrase wait for instructions use end task
downloads default in /a0/tmp/downloads
pass secrets and variables in message when needed

usage:
```json
{
  "thoughts": ["I need to log in to..."],
  "headline": "Opening new browser session for login",
  "tool_name": "browser_agent",
  "tool_args": {
    "message": "Open and log me into...",
    "reset": "true"
  }
}
```

```json
{
  "thoughts": ["I need to log in to..."],
  "headline": "Continuing with existing browser session",
  "tool_name": "browser_agent",
  "tool_args": {
    "message": "Considering open pages, click...",
    "reset": "false"
  }
}
```

