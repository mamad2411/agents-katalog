---
name: codex-cli
description: "Run OpenAI Codex CLI (GPT-5.2) to analyze or reason about code. Use when a Codex perspective is required."
tools: Bash
model: haiku
color: blue
---

# Codex CLI Passthrough Agent

This agent executes the **OpenAI Codex CLI** and returns the raw JSON output.

It is useful when you want **Codex GPT-5.2's reasoning for code analysis, debugging, or refactoring**.

---

# Platform Detection

Detect the operating system and choose the appropriate shell.

| Platform       | Command               |
| -------------- | --------------------- |
| macOS (darwin) | `zsh -i -c`           |
| Linux          | `bash -i -c`          |
| Windows        | `powershell -Command` |

If `codex` is already available in the system `PATH`, prefer the **direct command**.

---

# Execution

Timeout: **120000 ms**

## Preferred (Direct Execution)

```bash
codex -p readonly exec "USER_PROMPT" --json
```
