---
name: capability-discovery
description: Inventory the capabilities already available in the current session so the SDLC team can reuse them. Use at pipeline start (Phase 0) to discover project-local agents and skills (.claude/agents, .claude/skills), agents/skills from other installed plugins, and connected MCP servers, plus the repo's CLAUDE.md. Produces a capability map the orchestrator uses to decide delegation.
---

# Capability Discovery

The team is additive in existing projects: prefer the plugin's own components, but reuse what a project already has when it helps.

## What to inventory
- **Project-local agents:** files in `.claude/agents/` (name + description).
- **Project-local skills:** dirs in `.claude/skills/` (name + description).
- **Other available agents/skills:** those exposed by other installed plugins in this session.
- **MCP servers/tools** currently connected.
- The repo's `CLAUDE.md` for stated workflow/tooling preferences.

## Output: capability map
List, per role/phase, any candidate project agent and any relevant project skills, plus available MCP servers (e.g. Notion).

## Delegation policy (the orchestrator applies this)
- **Agents:** the plugin's own agents are the priority/default. Borrow a project's agent ONLY when needed — there is no suitable plugin agent, or a domain-specific project agent is clearly required for the task.
- **Skills:** the plugin's own skills lead; agents ALSO draw on relevant project-local skills/conventions when present.
- The orchestrator announces which agent/skill it uses for each phase. Delegation is never silent.
