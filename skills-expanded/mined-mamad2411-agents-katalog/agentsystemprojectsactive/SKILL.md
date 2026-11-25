---
name: agentsystemprojectsactive
description: agent.system.projects.active
---

# agent.system.projects.active

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **agent.system.projects.active**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/_RECENT-PROJECTS/ai-systems/agent-zero/prompts/agent.system.projects.active.md`

## 🧠 Master Agent Prompt & Capabilities

## Active project
Path: {{project_path}}
Title: {{project_name}}
Description: {{project_description}}
{% if project_git_url %}Git URL: {{project_git_url}}{% endif %}


### Important project instructions MUST follow
- always work inside {{project_path}} directory
- do not rename project directory do not change meta files in .a0proj folder
- cleanup when code accidentaly creates files outside move them

{{project_instructions}}
