---
name: example-skill
description: Minimal OMC skill exercising one Skill() call and one MCP tool reference.
argument-hint: "<topic>"
---

This skill demonstrates the translator. First it calls Skill("oh-my-claudecode:planner") to plan the work.

Then it reads state via mcp__plugin_oh-my-claudecode_t__state_read for context.

The oh-my-claudecode: namespace prefix should also be normalized in commentary.
