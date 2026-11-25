---
name: model-portability-adapter
description: Adapt skills, workflows, prompts, and tool instructions so they work across Claude, ChatGPT, Gemini, Codex, local agents, and other MCP-enabled systems. Use when the user wants cross-model compatibility or asks to make instructions vendor-neutral.
---

# Model Portability Adapter

Use this skill to make agent instructions portable across model providers and clients.

## Portability Principle

Write for agent capability, not provider branding.

Good:

- Use available file-reading tools.
- Use available command execution tools.
- Use available web/search tools.
- Use the client's artifact/document feature if present.

Avoid:

- Hardcoding one client's tool name.
- Assuming one model's memory, browsing, artifact, or MCP behavior.
- Depending on hidden system prompts.

## Compatibility Targets

This skill is intended for:

- Claude or Claude Code
- ChatGPT or custom GPT-style agents
- Gemini or Gems-style agents
- Codex or coding agents
- Local agents with MCP servers
- Multi-agent systems with their own tool registry

## Workflow

1. Identify the instruction type
   - Skill: behavior or domain process.
   - Workflow: ordered multi-step job.
   - Tool instruction: executable action mapping.
   - Prompt: one-off request or reusable template.

2. Remove vendor coupling
   - Replace exact tool names with capability names.
   - Replace client-specific UI assumptions with generic alternatives.
   - Keep any vendor-specific notes in an adapter section, not the core skill.

3. Normalize structure
   - Use clear frontmatter when supported.
   - Put trigger guidance in the description.
   - Keep the body procedural.
   - Include verification and output expectations.

4. Add adapter notes
   - Claude: can use `SKILL.md` style folders when the client supports skills.
   - ChatGPT: can paste the core instructions into custom instructions or project instructions.
   - Gemini: can use the core instructions as Gem or agent guidance.
   - Local MCP agents: map capability names to registered MCP tools.

5. Validate portability
   - Check that the skill still makes sense without exact tool names.
   - Check that a model without file tools can still ask for files or explain the blocker.
   - Check that a model with tools knows when to inspect, act, and verify.

## Rules

- Keep provider-specific details optional.
- Do not promise that every platform loads `SKILL.md` natively.
- Do not rely on one model's hidden behavior.
- Prefer short, explicit instructions over platform lore.

## Output Format

End with:

- Portable core
- Provider-specific notes
- Tool capability mapping
- Compatibility risks
