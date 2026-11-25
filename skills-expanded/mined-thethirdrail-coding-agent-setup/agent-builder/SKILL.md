---
name: agent-builder
description: |
  Create or maintain agent capabilities, skills, workflows, rules, automations, and custom MCP tools.
  Use when building, updating, validating, packaging, or installing agent skills, workflows, rules, automations, plugins, or custom MCP tools.
---
# Agent Builder

This is a router skill. Classify the request, choose one lane, then read only the lane reference needed for the current task. Compose lanes only when the user request genuinely crosses responsibilities.

## Intent Routing

| Intent | Load | Use When |
|---|---|---|
| Choose extension type | `agent-builder.md` | Read when deciding between skill, workflow, rule, automation, plugin, or MCP tool. |
| Skill creation and validation | `skill-builder.md` | Read when creating, modernizing, packaging, or installing skills. |
| Workflow creation | `workflow-builder.md` | Read when defining reusable operational workflows. |
| Rules and guardrails | `rule-builder.md` | Read when creating or updating reusable behavior rules. |
| Codex Starlark rules | `openai-rule-builder.md` | Read when editing Codex-compatible default.rules policy. |
| Automation templates | `automation-builder.md` | Read when creating recurring Codex automation templates. |
| Custom MCP tool build | `mcp-builder.md` | Read when no existing MCP server provides the needed capability. |

## Loading Protocol

1. Match the user request to the narrowest intent above.
2. Read `references/<lane>.md` for that intent before executing specialized steps.
3. Load scripts or assets from this skill only after the selected reference calls for them.
4. Keep outputs concise and state which lane was used when that matters for handoff or auditability.

## Consolidated Names

Former installable skills now routed here: `agent-builder`, `skill-builder`, `workflow-builder`, `rule-builder`, `openai-rule-builder`, `automation-builder`, `mcp-builder`.

Related routers: `mcp-ops`, `research-docs`.
