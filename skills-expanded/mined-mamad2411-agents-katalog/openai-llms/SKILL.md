---
name: openai-llms
description: >-
  Reference and APIs for retrieving OpenAI documentation programmatically for LLMs.
  USE FOR: OpenAI documentation and API.
  DO NOT USE FOR: OpenAI API Operations.
license: MIT
---

# openai-llms

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- **Documentation Search**: Locating specific OpenAI API, guides, concepts, or reference documentation articles.
- **Article Retrieval**: Fetching the full rendered markdown of a specific OpenAI docs page via its `llms.txt` or related context.

## WHEN NOT TO USE

- **OpenAI API Operations**: Interacting with live OpenAI APIs to generate text, images, or audio. Use appropriate API endpoints or SDKs for that.

## Core Process

1. **Identify the Need**: Determine whether you need to search for a topic or fetch a specific known documentation path.
2. **Execute the Query**: Use `webfetch` to fetch the data from the `llms.txt` reference or relevant URLs.
3. **Process Content**: Extract the relevant information to answer the user's query or inform the ongoing task. For full docs (`llms-full.txt`), use filtering or grep techniques as they are very large.

## Common Pitfalls

- **Fetching `llms-full.txt` without narrowing the scope**. Prefer the index or a targeted document when possible, and filter aggressively if you must use the full file.

## References

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

- [OpenAI Developers](https://developers.openai.com/llms.txt)
  USE FOR: High-level platform overview, getting started guidance, and the main documentation index.
- [OpenAI Developers Full Docs](https://developers.openai.com/llms-full.txt)
  USE FOR: Full single-file Markdown export of all developers docs (large, so needs to be filtered).
- [OpenAI API Docs](https://developers.openai.com/api/docs/llms.txt)
  USE FOR: Actions, Assistants, Bots, Concepts, Deprecations, GPTs, Guides, Libraries, MCP, Pricing, Quickstart, Supported Countries, Tutorials, UI Kit Demo.
- [OpenAI API Docs Full](https://developers.openai.com/api/docs/llms-full.txt)
  USE FOR: Full single-file export of API guides and conceptual docs (large, so needs to be filtered).
