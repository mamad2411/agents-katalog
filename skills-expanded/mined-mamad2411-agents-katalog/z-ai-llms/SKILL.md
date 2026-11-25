---
name: z-ai-llms
description: >-
  Reference and APIs for retrieving z.AI documentation programmatically for LLMs.
  USE FOR: searching z.AI docs, GLM models documentation, z.AI API reference, CogVideoX, Vidu, OpenCode integration with z.AI.
  DO NOT USE FOR: calling live z.AI API endpoints, invoking GLM models directly.
license: MIT
---

# z-ai-llms

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- **Documentation Search**: Locating specific z.AI (GLM series) documentation articles.
- **Article Retrieval**: Fetching the full rendered markdown of a specific z.AI docs page via its `llms.txt` or related context.

## WHEN NOT TO USE

- **Live AI Generation**: Interacting with live z.AI APIs to generate text, images, or video. Use appropriate API endpoints or SDKs for that.

## Core Process

1. **Identify the Need**: Determine whether you need to search for a topic or fetch a specific known documentation path.
2. **Execute the Query**: Fetch the data from the llms.txt reference or relevant URLs.
3. **Process Content**: Extract the relevant information to answer the user's query or inform the ongoing task.

## Common Pitfalls

- **Fetching `llms-full.txt` without narrowing the scope**. Prefer the index or a targeted document when possible, and filter aggressively if you must use the full file.

## References

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

- [z.AI Documentation (llms.txt)](https://docs.z.ai/llms.txt)
  MUST be fetched/loaded when searching for z.AI API references, agents, audio, image/video generation capabilities, or tool integrations.
  USE FOR:
  - API Reference (Chat, Audio, Image, Video)
  - Agents (Translation, Slide/Poster)
  - Tool Integrations (Web Search, Web Reader, MCP Servers)
  - GLM Model Guides (GLM-5.1, GLM-5-Turbo, GLM-4.5)
  - Developer Tools Configurations (Claude Code, Cline, Cursor, OpenCode, n8n)

- [z.AI Full Documentation (llms-full.txt)](https://docs.z.ai/llms-full.txt)
  MUST be fetched/loaded when deep, exhaustive context is needed across the entire z.AI ecosystem. Note: This file contains the entire documentation corpus and needs to be filtered due to its massive size.
  USE FOR:
  - Comprehensive searches across all docs
  - Extracting specific, detailed code examples when llms.txt is insufficient
