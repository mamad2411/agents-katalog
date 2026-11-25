---
name: autogpt-autonomous
description: Autonomous AI task execution with AutoGPT
version: 1.0.0
tags: [ai, autonomous, agents, automation]
---

# AutoGPT – Autonomous AI Agent

AutoGPT chains LLM calls to autonomously execute tasks including
web browsing, code writing, file management, and more.

- **GitHub**: github.com/Significant-Gravitas/AutoGPT (177 000+ ⭐)
- **License**: MIT
- **Security**: Active community. Sandboxed execution. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{AUTOGPT_URL}}` | AutoGPT server URL (if using server mode) |

## Usage Examples

### Run via CLI

```bash
python -m autogpt --goal "Research the top 5 open-source databases and create a comparison table"
```

## AI Agent Tips

- Supports recursive task decomposition and execution.
- Persistent memory across sessions.
- Plugin system for web browsing, email, and code execution.
- Run in Docker for sandboxed, safe execution.
