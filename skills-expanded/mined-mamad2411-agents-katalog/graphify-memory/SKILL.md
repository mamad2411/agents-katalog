---
name: graphify-memory
description: Read and write to the shared cross-agent memory graph using graphify.
---
# Graphify Memory Skill

Teaches the agent to read and write to the unified cross-agent memory graph (Token-Agnostic Handoff Protocol). This ensures that context persists between sessions and across different AI models (Antigravity, Claude Code, OpenCode).

## When to use this skill
- When starting a session in a project that uses shared memory.
- When you are about to run out of context or end a session, you must write a summary of what you did.
- Before making significant architectural decisions, to see what was previously decided.

## How to use Graphify

The project root must contain `graphify-out/graph.json` or you should be operating in a workspace that supports the graphify CLI.

### Querying Memory
To query historical context:
```bash
graphify query "topic" --graph graphify-out/graph.json
```

To find paths between concepts:
```bash
graphify path "concept A" "concept B" --graph graphify-out/graph.json
```

To explain a concept:
```bash
graphify explain "concept" --graph graphify-out/graph.json
```

### Writing to Memory
Always write your findings, completed tasks, and architectural decisions to the graph. Do not let context die in the session.

## Unified Memory Rules
1. Context window is ephemeral; disk is eternal.
2. If you learn a new pattern, add it to the graph.
3. If you fix a tricky bug, document the fix in the graph.
