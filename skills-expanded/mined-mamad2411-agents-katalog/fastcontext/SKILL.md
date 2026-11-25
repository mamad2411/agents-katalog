---
name: fastcontext
description: This skill should be used when the user asks to "explore the codebase", "find related files", "understand the architecture", "search for implementations", "use FastContext", or when broad codebase context is needed before editing unfamiliar code. Runs Microsoft FastContext with in-process MLX inference on Apple Silicon.
---

# FastContext

FastContext is a specialized exploration agent that runs Read, Glob, and Grep operations in parallel using a local 4B model via MLX, returning compact file-path:line-range citations. The model runs in-process — no external server, no env vars.

## Prerequisite

The `fastcontext` MCP server must be registered in Claude Code. If the `fastcontext_explore` tool is not available, run the setup skill first — see `skills/setup/SKILL.md`.

## Usage

Call the `fastcontext_explore` MCP tool directly:

```
fastcontext_explore(query="Find all authentication middleware and session handling", max_turns=4)
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `query` | (required) | Natural-language description of what to find |
| `max_turns` | 4 | Exploration turns (1-10) |

### When to use

- **Unfamiliar code areas**: Before editing files not yet explored
- **Cross-cutting concerns**: Finding all files related to a feature
- **Architecture discovery**: Understanding module connections
- **Dependency tracing**: Finding callers or implementors of a function

### When NOT to use

- **Already-explored files**: Context is in the conversation
- **Single known file**: Direct Read is faster
- **Simple keyword search**: A single Grep suffices

## Query Examples

```
"Find all database migration files and the schema definition for the users table"
"Locate the API route handlers for /api/v2/users and their request validation"
"Find error handling patterns: custom error classes, error middleware, and error logging"
"Locate the CLI entry point and trace the command registration pattern"
```

## Interpreting Results

FastContext returns citations with file paths and line ranges:

```
src/auth/middleware.ts:15-42 (JWT validation middleware)
src/auth/session.ts:8-31 (Session store implementation)
```

Use these to make targeted Read calls for the specific lines needed.

## Adjusting max_turns

- **2**: Quick lookup, single file
- **4** (default): Standard exploration
- **6-8**: Deep exploration, large codebase
- **10**: Exhaustive cross-cutting search
