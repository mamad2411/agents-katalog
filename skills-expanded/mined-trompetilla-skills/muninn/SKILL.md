---
name: muninn
version: 2.1.14
description: "Universal Context Protocol and Long-Term Memory for AI Agents. Muninn MCP provides project-local persistent storage for architectural decisions, development patterns, and technical context. Use when an agent needs to remember project history across sessions, retrieve relevant code snippets surgically (saving up to 95% tokens), or maintain architectural consistency. Features local semantic search via the sandboxed CXP engine and a zero-aggression security model. Triggers: context, memory, project-brain, persistent-learning, token-optimization, semantic-search."
author: blackknight
tags: mcp, context, memory, productivity, long-term-memory
runtime: node
permissions:
  - path: "~/.muninn/"
    access: "read-write"
    description: "Global configuration and project state storage."
  - path: "./.muninn/"
    access: "read-write"
    description: "Project-local memory storage and context indices."
install: "npm install -g muninn-core"
---

# Muninn MCP

**Universal Memory Layer for AI-Driven Development.**

Muninn MCP (Memory Context Protocol) is a standardized memory layer that ensures AI agents have access to project-specific knowledge. It bridges the gap between different AI sessions and tools by providing a shared, project-local "Brain".

## SECURITY & RISK MITIGATION (AUDIT READY)

Muninn MCP v2.1.14 is architected for maximum security and agent safety:

### 1. Command Injection Prevention (RCE)
- **Binary-Only Execution**: All calls to the internal `cxp` engine use `child_process.execFile`. This bypasses shell interpretation, making shell-injection impossible.
- **Input Sanitization**: All queries are sanitized via strict whitelist regex (`/[\w\s\-\.\?\!\(\)\[\]]/`).
- **Length Constraints**: Inputs are capped at 500 characters to prevent buffer-related exploits.

### 2. Environment Integrity (Zero-Aggression)
- **No Forced Modification**: Automatic writing to `.cursorrules` or `CLAUDE.md` is disabled.
- **Opt-in Only**: The `enforce_rules` tool is purely for manual use during project onboarding.
- **Passive Middleware**: Automatic context interception is disabled by default; Muninn acts as a high-fidelity library, not an intercepting proxy.

### 3. Local-First Privacy
- **100% Local**: No data, telemetry, or code ever leaves the host machine. Semantic search happens entirely on-device via the high-performance Rust engine.

## AGENT USAGE

Agents use Muninn MCP to maintain a "Project Brain":
1. **Sync**: Call `brain_check` at session start to load project-local knowledge.
2. **Learn**: Call `add_memory` for architectural decisions, bug fixes, or new patterns.
3. **Search**: Use `search_context` for deep semantic retrieval of relevant files and logic.

## Setup

### npm Installation (Recommended)
```bash
npm install -g muninn-core
```

### Manual Configuration
Add to your MCP settings (e.g. `claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "muninn": {
      "command": "npx",
      "args": ["-y", "muninn-core"]
    }
  }
}
```

---
*Maintained by BlackKnight. Version 2.1.14*
