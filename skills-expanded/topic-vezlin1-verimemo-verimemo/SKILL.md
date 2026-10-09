---
name: verimemo
description: Manage and query project-scoped memory with VeriMemo. Use to search decisions/facts, explicitly remember, correct, forget, check memory health (doctor), or inspect project status. Automatic recall and turn capture happen in the background.
---

# VeriMemo Agent Skill

VeriMemo provides persistent, verified project memory stored as clean, human-readable Markdown. Project memory is advisory context—always prefer current user requests, live code, tests, and tool outputs over memory claims.

## Key Workflows

### 1. Search & Context Preview
Search historical decisions, architectural facts, and constraints:
```powershell
verimemo search "<query>" --cwd "$PWD"
verimemo context "<query>" --cwd "$PWD"
```
*Tip: Exact symbols, error codes, and configuration keys have 100% exact-lane recall.*

### 2. Explicit Memory Mutation
Manually capture, correct, or supersede knowledge (processed via Luna with `--wait`):
```powershell
# Remember a new verified fact or decision
verimemo remember "Adopted SQLite WAL mode for fast concurrency" --wait --cwd "$PWD"

# Correct outdated or mistaken knowledge
verimemo correct "Port changed from 3000 to 8080 in dev config" --wait --cwd "$PWD"

# Archive / supersede an obsolete fact
verimemo forget "Legacy Redis cache configuration" --wait --cwd "$PWD"
```

### 3. Health & Diagnostics
Diagnose project memory, hook integration, and background service:
```powershell
verimemo status --cwd "$PWD"
verimemo doctor --cwd "$PWD"
```

### 4. Integrity & Maintenance
Audit, reconcile, or clean up project memory:
```powershell
verimemo lint --reconcile --cwd "$PWD"
verimemo audit --attempts --cwd "$PWD"
verimemo storage path --cwd "$PWD"
```

## Native MCP Server
VeriMemo provides a Model Context Protocol (MCP) server for zero-overhead tool calling:
```powershell
verimemo mcp
```
*Tools exposed: `verimemo_search`, `verimemo_remember`, `verimemo_correct`, `verimemo_forget`, `verimemo_inspect`, `verimemo_doctor`.*

## References
- [Command Reference](references/commands.md) — Exhaustive CLI parameters and flags.
- [Memory Model & Architecture](references/memory-model.md) — Schema v2, temporal validity, confidence tiers, and lease fencing.
