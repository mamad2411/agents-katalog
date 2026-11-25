---
name: bun-llms
description: >-
  Reference and APIs for retrieving Bun documentation programmatically for LLMs.
  USE FOR: bun, bunjs, bun.sh, bun run, bun install, bun test, bun build, package manager, javascript runtime, bundler, test runner.
  DO NOT USE FOR: nodejs, npm, yarn, pnpm, deno. You MUST load this skill when asked to search or retrieve Bun documentation.
license: MIT
---

# Skill: bun-llms

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- **Documentation Search**: Locating specific Bun documentation articles, CLI commands, or API references.
- **Article Retrieval**: Fetching the full rendered markdown of a specific Bun docs page via its `llms.txt` or related context.

## WHEN NOT TO USE

- **Other Runtimes/Managers**: When the user explicitly asks for Node.js, Deno, npm, yarn, or pnpm documentation.

## Core Process

1. **Identify the Need**: Determine whether you need to search for a topic or fetch a specific known documentation path.
2. **Execute the Query**: Fetch the data from the llms.txt reference or relevant URLs.
3. **Process Content**: Extract the relevant information to answer the user's query or inform the ongoing task.

## Common Pitfalls

- **Fetching `llms-full.txt` without narrowing the scope**. Prefer the index or a targeted document when possible, and filter aggressively if you must use the full file.
- **Using this skill for non-Bun ecosystems**: Route Node.js, npm, yarn, pnpm, or Deno documentation requests to the appropriate skill instead of relying on Bun references.

## References

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

- [Bun Documentation Index](https://bun.com/llms.txt)
  USE FOR: Index of documentation, overview of features, API reference list, CLI commands, package management, bundler, test runner, getting started.
- [Bun Full Documentation](https://bun.com/llms-full.txt)
  USE FOR: Deep dives, comprehensive searching across all docs, offline reading. Note: This file needs to be filtered due to size.
