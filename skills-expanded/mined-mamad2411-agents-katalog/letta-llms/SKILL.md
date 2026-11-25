---
name: letta-llms
description: >-
  USE FOR: Letta documentation search, Letta SDK references, retrieving Letta framework details, Letta agent APIs.
  DO NOT USE FOR: executing Letta agents, interacting with live Letta endpoints, general Python programming.
license: MIT
---

# letta-llms

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- **Documentation Search**: Locating specific Letta framework or SDK documentation articles.
- **Article Retrieval**: Fetching the full rendered markdown of a specific Letta docs page via its `llms.txt` or related context.

## WHEN NOT TO USE

- **Letta API Operations**: Interacting with live Letta APIs to manage or run agents. Use appropriate API endpoints or SDKs for that.

## Core Process

1. **Identify the Need**: Determine whether you need to search for a topic or fetch a specific known documentation path in the Letta documentation.
2. **Execute the Query**: Fetch the data from the llms.txt reference or relevant URLs.
3. **Process Content**: Extract the relevant information to answer the user's query or inform the ongoing task.

## Common Pitfalls

- **Fetching `llms-full.txt` without narrowing the scope**. Prefer the index or a targeted document when possible, and filter aggressively if you must use the full file.

## References

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

- [Letta Documentation Index](https://docs.letta.com/llms.txt)
  USE FOR: High-level overview, index of Letta documentation, navigation to specific guides, quick topic discovery,
  basic Letta concepts, architecture summaries, and identifying the right page before deep retrieval.
- [Letta Full Documentation](https://docs.letta.com/llms-full.txt)
  USE FOR: Deep technical reference, comprehensive Letta SDK details, full API documentation, endpoint behavior,
  configuration details, extensive code examples, troubleshooting details, and architecture implementation guidance.
  Note: this file is very large and needs to be filtered due to size.
