---
name: antigravity-plugin-create
description: Creates complete Antigravity plugin packages with scoped rules, skills, workflows, resources, scripts, hooks, MCP configuration, README, LICENSE, AGENTS.md, and plugin index files. Use when a user asks to generate a new Antigravity plugin or split a stack into focused plugins.
license: MIT
compatibility: "Antigravity plugin authoring; also useful for IDEs and coding agents that read .agents guidance."
---

# Antigravity Plugin Create

This skill creates practical, production-grade Antigravity plugins without bloating the agent context.

## Use this skill when

- A user asks to create an Antigravity plugin.
- A user asks for a plugin for a language, framework, database, platform, cloud, tool, or workflow.
- A user asks to split a stack into multiple plugins.
- A repository needs `.agents/AGENTS.md` and `.agents/plugins/_INDEX.md`.

## First decisions

1. Identify the target technology, platform, or workflow.
2. Identify the exact target version if version-specific behavior matters.
3. If the user explicitly requests a general plugin, avoid version-specific commands and APIs.
4. For stacks, apply the 95% rule and create separate plugins for frameworks, hosted services, cloud platforms, CI/CD, ORMs, and specialized integrations.
5. Search current official docs before generating version-specific plugin content.

## Output contract

Generate:

- or expand `.agents/AGENTS.md`
- or expand `.agents/plugins/_INDEX.md`
- `.agents/plugins/<plugin-name>/plugin.json`
- `.agents/plugins/<plugin-name>/README.md`
- `.agents/plugins/<plugin-name>/LICENSE`
- Rules, skills, workflows, resources, examples, scripts, `mcp_config.json`, and `hooks.json` only when useful.

Use [plugin-output-template.md](resources/plugin-output-template.md) for the response structure.

## Workflows

- Use [create-plugin-workflow.md](workflows/create-plugin-workflow.md) for ordinary new plugin generation.
- Use [split-stack-into-plugins-workflow.md](workflows/split-stack-into-plugins-workflow.md) when a request covers multiple technologies or a whole stack.

## Resources

- [plugin-output-template.md](resources/plugin-output-template.md)
- [plugin-scope-decision-tree.md](resources/plugin-scope-decision-tree.md)
- [plugin-quality-checklist.md](resources/plugin-quality-checklist.md)

## Creation checklist

Before finalizing:

- Names are lowercase kebab-case.
- JSON is valid.
- Skills have valid `SKILL.md` frontmatter.
- Workflows live inside the relevant skill.
- README explains included and omitted optional files.
- `_INDEX.md` is accurate and minimal.
- The plugin is safe by default.
- Version-specific guidance is backed by current official docs.
