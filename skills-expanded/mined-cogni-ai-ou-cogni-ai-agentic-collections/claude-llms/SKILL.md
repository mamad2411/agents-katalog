---
name: claude-llms
description: 'Reference and APIs for retrieving Anthropic Claude documentation programmatically for LLMs. You MUST load this skill when asked to search or retrieve Claude or Claude Code documentation.'
license: MIT
---

# claude-llms

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- **Documentation Search**: Locating specific Claude Code or Anthropic Claude documentation articles.
- **Article Retrieval**: Fetching the full rendered markdown of a specific Claude docs page via its `llms.txt` or related context.

## WHEN NOT TO USE

- **Claude API Operations**: Interacting with live Claude APIs to generate text. Use appropriate API endpoints or SDKs for that.

## Core Process

1. **Identify the Need**: Determine whether you need to search for a topic or fetch a specific known documentation path.
2. **Execute the Query**: Use `webfetch` to fetch the data from the llms.txt reference or relevant URLs.
3. **Process Content**: Extract the relevant information to answer the user's query or inform the ongoing task.

## References

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

- [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk.md)
  Includes: Get started, Capabilities (Built-in tools, Hooks, Subagents, MCP, Permissions, Sessions),
  Features (Agent SDK vs Client SDK, Agent SDK vs Claude Code CLI, Agent SDK vs Managed Agents),
  Compare the Agent SDK to other Claude tools, Guidelines.
  USE FOR: Agent SDK, SDK setup, Capabilities, Built-in tools, Hooks, Subagents, MCP,
  Permissions, Sessions, Client SDK comparisons, Managed Agents comparisons, SDK guidelines.
- [Anthropic Developer Documentation](https://platform.claude.com/llms.txt)
  USE FOR: Anthropic API, API quickstart, Models, Developer guides, Rate limits, Pricing,
  Streaming, Tool use, Prompting.
- [Anthropic Developer Documentation (Full)](https://platform.claude.com/llms-full.txt)
  (NOTE: This file is extremely large and SHOULD be filtered when loading).
  USE FOR: Full API reference, Exhaustive documentation, Endpoint details, Schema details,
  Parameter definitions, Error surfaces.
- [Claude Docs](https://claude.com/llms.txt)
  USE FOR: Claude usage, Claude plans, General AI capabilities, Claude UI features,
  Web app workflows, Product overview.
- [Claude Code Docs](https://code.claude.com/llms.txt)
  USE FOR: Claude Code CLI, CLI setup, Commands, Slash commands, Local development,
  Project setup, CLAUDE.md, MCP setup, Agent workflows.
