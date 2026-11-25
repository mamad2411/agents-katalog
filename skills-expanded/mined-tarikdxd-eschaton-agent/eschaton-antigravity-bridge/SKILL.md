---
name: eschaton-antigravity-bridge
description: Connect to and orchestrate the user's local Antigravity desktop app as a co-agent with automatic project selection, live benchmark-researched model routing, and a strict 10% usage protection shield.
---

# Eschaton Antigravity Bridge Skill

Use this skill whenever the user wants you (Qoder, OpenCode, Claude Code, Cursor, etc.) to collaborate with their locally running **Antigravity** application.

## Setup
```bash
pip install -e .
eschaton connect
```

## Delegation Workflow
1. Always identify the active project path (`--project <path>`).
2. Choose an appropriate specialist role for Antigravity:
   - `co_architect` — System architecture, `/plan` design, multi-module strategy
   - `code_implementer` — Feature implementation across multiple files
   - `deep_debugger` — Root-cause analysis, failing test repair, terminal diagnostics
   - `ui_specialist` — Frontend UI/UX, styling, responsive components, browser verification
   - `reviewer_tester` — Code review, edge-case auditing, automated test generation
3. Delegate via MCP (`antigravity_delegate_task`) or CLI (`eschaton delegate`).
4. Respect the **10% Usage Shield**: if `allowed=false` is returned, do NOT force-send. Follow the returned `optimized_prompt_suggestion` or stop delegating once the 10% reserve floor is reached.
