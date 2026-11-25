---
name: agentdb-init
description: Initialize an AgentDB Cognitive Container (.rvf file) in the current project. Sets up storage, embedder config, and the agentdb MCP server. Use when the user is starting a new project that needs vector memory, or asks to "set up agentdb" / "init agentdb".
---

# Initialize AgentDB

Sets up a fresh AgentDB instance for the current project. Creates a single-file `.rvf` Cognitive Container that holds vectors, indexes, learning state, and the audit log.

## When to use

- User asks to "set up agentdb", "init memory", "add a vector store"
- New project that needs persistent agent memory
- Existing project moving from in-memory state to durable memory

## Steps

1. Confirm the storage path (default: `./memory.rvf` at the project root, or `~/.agentdb/<project-name>.rvf` for global memory).
2. Pick the embedder (default: `Xenova/all-MiniLM-L6-v2` at 384d — fast, free, runs in-process).
3. Register the agentdb MCP server in Claude Code:
   ```bash
   claude mcp add agentdb -- npx agentdb@latest mcp start
   ```
4. Initialize the file via the MCP tool `agentdb_pattern_store` (the first store auto-creates the schema), or via CLI:
   ```bash
   npx agentdb@latest init ./memory.rvf
   ```
5. Add `*.rvf` to `.gitignore` unless the user explicitly wants memory checked into source control.
6. Confirm with a smoke test: store one pattern and search for it.

## Notes

- The `.rvf` is a single binary file. Back it up like a SQLite database.
- For multi-agent setups, share one `.rvf` per coordinated namespace; use separate files for trust-boundary isolation.
- All AgentDB operations after init go through the MCP tools (`agentdb_pattern_*`, `agentdb_reflexion_*`, etc.) or the npm library (`import { SelfLearningRvfBackend } from 'agentdb'`).

## Don't

- Don't commit the `.rvf` file by default — it can hold session-specific data, including content from messages.
- Don't run `init` on an existing `.rvf` file without confirming — it will refuse rather than overwrite, but a confused user might delete the existing file thinking it's stale.
