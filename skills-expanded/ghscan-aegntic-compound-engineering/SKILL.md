---
name: create-agent-skill
description: Create or edit Claude Code skills with expert guidance on structure and best practices
argument-hint:
  - skill description or requirements
platforms:
  claude:
    allowed-tools: Skill(create-agent-skills)
    disable-model-invocation: true
---

Invoke the create-agent-skills skill for: $ARGUMENTS
