---
name: agentsystemsecrets
description: agent.system.secrets
---

# agent.system.secrets

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **agent.system.secrets**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/_RECENT-PROJECTS/ai-systems/agent-zero/prompts/agent.system.secrets.md`

## 🧠 Master Agent Prompt & Capabilities

# Secret Placeholders
- user secrets are masked and used as aliases
- use aliases in tool calls they will be automatically replaced with actual values

You have access to the following secrets:
<secrets>
{{secrets}}
</secrets>

## Important Guidelines:
- use exact alias format `§§secret(key_name)`
- values may contain special characters needing escaping in code, sanitize in your code if errors occur
- comments help understand purpose

# Additional variables
- use these non-sensitive variables as they are when needed
- use plain text values without placeholder format
<variables>
{{vars}}
</variables>

