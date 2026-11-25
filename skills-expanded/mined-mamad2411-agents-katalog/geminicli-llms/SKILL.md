---
name: geminicli-llms
description: >-
  Reference and APIs for retrieving Gemini CLI documentation programmatically for LLMs.
  USE FOR: searching Gemini CLI docs, Google Gemini models documentation, geminicli API reference, tool integrations, OpenCode integration with Gemini CLI.
  DO NOT USE FOR: calling live Gemini API endpoints, invoking models directly without CLI.
license: MIT
---

# geminicli-llms

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- **Documentation Search**: Locating specific Gemini CLI or Google Gemini documentation articles.
- **Article Retrieval**: Fetching the full rendered markdown of a specific Gemini CLI docs page via its `llms.txt` or related context.

## WHEN NOT TO USE

- **Live AI Generation**: Interacting with live Gemini APIs to generate text, images, or video. Use appropriate API endpoints or SDKs for that.

## Core Process

1. **Identify the Need**: Determine whether you need to search for a topic or fetch a specific known documentation path.
2. **Execute the Query**: Fetch the data from the llms.txt reference or relevant URLs.
3. **Process Content**: Extract the relevant information to answer the user's query or inform the ongoing task.

## Common Pitfalls

- **Fetching full `llms.txt` without narrowing the scope**. Note: This file contains the entire documentation corpus and needs to be filtered due to its massive size. Prefer targeted searches and filter aggressively.

## References

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

- [Gemini CLI Documentation (llms.txt)](https://geminicli.com/llms.txt)
  MUST be fetched/loaded when searching for Gemini CLI references, installation, usage, or tool integrations. Note: This file contains the entire documentation corpus and needs to be filtered due to its massive size.
  USE FOR:
  - Install and Get Started guides (setup, auth, first run, npm install, deployment)
  - CLI command and behavior references (commands, slash commands, keyboard shortcuts)
  - Core tools and workflows (shell, file edit/read, web fetch/search, todos, memory)
  - Configuration and customization topics (settings, models, themes, system prompt, `.geminiignore`)
  - Extension and integration guidance (MCP servers, IDE integration, hooks, subagents)
  - Runtime and safety controls (sandboxing, plan mode/read-only mode, telemetry)
