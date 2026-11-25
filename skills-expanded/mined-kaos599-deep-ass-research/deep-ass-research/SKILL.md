---
name: deep-ass-research
description: >
  Deep, multi-source, primary-sourced research into a backlinked Obsidian vault.
  Fans out scout/diver sub-agents that write atomic cited claim notes, adversarially
  verifies them, then synthesizes a Map-of-Content + report. Use when the user wants
  thorough, cited research on a topic, company, market, or literature, or says
  "deep research", "DAR", "Deep Ass Research", "research X properly", "build me a
  knowledge map of X", "look deeply into", "do a deep dive on".
---

# Deep Ass Research (DAR) — Claude Code adapter

This is the Claude Code entry point for the **portable DAR framework**. The methodology is host-agnostic and lives in `core/`; this file just binds DAR's capability verbs to Claude Code's tools and tells you how to spawn the roles.

## How to run

1. **Read `core/orchestration.md` and follow it exactly.** It is the runbook (preflight → charter → breadth → gate → depth → drift guard → verify → synthesize → deliver). Read its referenced files as needed: `core/capabilities.md`, `core/methodology.md`, `core/vault-layout.md`, `core/note-schemas.md`, `core/provenance.md`, and the chosen `core/modes/<mode>.md`.
2. **Spawn sub-agents** with the **Task / Agent tool** (`subagent_type: general-purpose`). For each role, read `core/roles/<role>.md` and paste its **full content** as the sub-agent prompt, then append a `## Task` block with the thread/claim context and the absolute vault path. (This mirrors the `bug-hunt-review` skill's dispatch pattern.) Run independent sub-agents **in parallel** by issuing multiple Task calls in one message.
3. **Track progress** in the vault files `_progress.md` and `_open-threads.md` (source of truth). You MAY also mirror `_progress.md` into TodoWrite for visibility.

## Capability bindings (Claude Code)

| Verb | Binding |
|---|---|
| `WRITE_FILE` | Write / Edit |
| `ASK_USER` | AskUserQuestion |
| `SPAWN_SUBAGENT` | Task / Agent tool (`general-purpose`), parallel via multiple calls |
| `SEARCH` | Tavily / Exa MCP if present, else built-in `WebSearch` |
| `FETCH` | Tavily extract / Exa fetch if present, else built-in `WebFetch` |
| `BROWSE` | TinyFish MCP (`run_web_automation`) |
| `READ_DOCS` | Context7 + Ref MCP, else `WebSearch`+`WebFetch` on official docs |

Record the actual bindings (and any degraded verbs) in `_session.md` during preflight.

## Optional acceleration (Workflow tool)

For determinism, resumability, and budget control, the **Depth → Drift → Verify → Synthesize** stretch MAY run via `adapters/claude-code/dar-pipeline.workflow.js` (native `Workflow` tool). If you use it: first read the role files in `core/roles/` and the chosen `core/modes/<mode>.md`, then invoke the Workflow passing them in `args` (the script sandbox can't read files): `args = {vault, mode, brief, threads, roles:{...}, playbook}`. Otherwise just follow steps 3–5 of `core/orchestration.md` directly. Running DAR implies opting into multi-agent orchestration — announce the approach before launching.

## Packaging

This directory works as a **drop-in skill** as-is. To distribute it as a **plugin** (registers the roles as real subagents, adds `/dar`, and auto-wires prerequisite MCP servers), see `adapters/claude-code/plugin/`.
