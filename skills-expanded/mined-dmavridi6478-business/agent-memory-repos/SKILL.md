# Agent Memory Repos

7 open-source repos for giving AI agents persistent memory — so you never re-explain your project again. Rows 1, 3, 4, 5 curated by @joshualevi.ai; rows 2 and 6 added from a later @githubnow "daily briefing" batch; row 7 added from an @aigenesis.official "GitHub repos for AI agents" carousel (each confirmed live via GitHub search before being added — see stars/description).

## Repos

| # | Repo | Stars | What It Does |
|---|------|-------|--------------|
| 1 | [topoteretes/cognee](https://github.com/topoteretes/cognee) | 30k | Graph-based AI memory — builds knowledge graphs from your docs and chat history |
| 2 | [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | 36k | Self-evolving context database — unifies agent memory, knowledge RAG, and skills behind a `viking://` filesystem; content is tiered (abstract/overview/details) and loaded on demand to cut token spend. Also referenced in `claude-code-tooling`. |
| 3 | [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | 11k | Self-evolving memory OS — memory that learns and updates itself over time |
| 4 | [Gentleman-Programming/engram](https://github.com/Gentleman-Programming/engram) | 6k | MCP + SQLite persistent memory — plug-and-play memory server for Claude Code |
| 5 | [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) | 4k | Obsidian markdown memory for Claude Code — vault-based persistent context |
| 6 | [mksglu/context-mode](https://github.com/mksglu/context-mode) | 21k | Sandboxes MCP tool output (98% size reduction — a 315 KB response shrinks to 5.4 KB), tracks file edits/tasks/decisions in SQLite with FTS5 search to survive context compaction, and routes code execution across 17 platforms instead of dumping raw tool output through context |
| 7 | [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory) | — | Persistent memory for coding agents — stores patterns, outcomes, and past decisions so the agent improves with every run instead of resetting to zero each session. The source carousel showed a `Threesided-Studios/Agent-Memory` fork of this repo that was 94 commits behind upstream; cited here by the canonical upstream repo instead. |

## Quick Install

### cognee (graph memory)
```bash
pip install cognee
```

### MemOS (memory OS)
```bash
git clone --depth 1 https://github.com/MemTensor/MemOS ~/repos/MemOS
cd ~/repos/MemOS && pip install -e .
```

### engram (MCP + SQLite)
```bash
git clone --depth 1 https://github.com/Gentleman-Programming/engram ~/repos/engram
cd ~/repos/engram && npm install
# Add to Claude Code MCP config:
# { "engram": { "command": "node", "args": ["~/repos/engram/server.js"] } }
```

### obsidian-second-brain (vault memory)
```bash
git clone --depth 1 https://github.com/eugeniughelbur/obsidian-second-brain ~/repos/obsidian-second-brain
```

### OpenViking (context database)
```bash
git clone --depth 1 https://github.com/volcengine/OpenViking ~/repos/OpenViking
cd ~/repos/OpenViking && pip install -e .
```

### context-mode (MCP tool-output sandboxing + session index)
```bash
git clone --depth 1 https://github.com/mksglu/context-mode ~/repos/context-mode
cd ~/repos/context-mode && npm install
# Wires in via MCP + Claude Code hooks — see the repo's own setup docs for
# the hook config (it edits your existing hooks, so review the diff first).
```

### agentmemory (coding-agent persistent memory)
```bash
git clone --depth 1 https://github.com/rohitg00/agentmemory ~/repos/agentmemory
cd ~/repos/agentmemory && pip install -e .
```

## Claude Code Memory Prompt

```
Before starting any task, check your memory context:
1. Read CLAUDE.md for project-specific instructions
2. Check the memory store for relevant prior decisions
3. Summarize what you know about the current project before proceeding

After completing a task, save:
- What was built or changed
- Key decisions made and why
- What to remember for next time
```

## Choosing the Right Repo

| Use case | Best repo |
|----------|-----------|
| Complex knowledge graphs from docs | cognee |
| Self-improving agent memory | MemOS |
| Simple MCP memory for Claude Code | engram |
| Obsidian-based personal knowledge | obsidian-second-brain |
| Unified memory + RAG + skills, tiered/token-efficient loading | OpenViking |
| Cutting raw MCP tool-output bloat specifically (not memory per se) | context-mode |
| Coding agent that remembers patterns/outcomes/decisions across separate tasks | agentmemory |

## Batch 2 addition — not vendored here, documented for completeness

`AgriciDaniel/claude-obsidian` (14.7k★, Python) — a larger, more actively
maintained "self-organizing AI second brain for Obsidian + Claude Code" than
the `obsidian-second-brain` entry above (row 5), covering the same job
(drop in any source, Claude links/sorts/files it into a connected knowledge
graph). Already documented in this repo's README (65th Addition) —
not re-added as its own row here to avoid two competing "Obsidian memory"
recommendations; if starting fresh, prefer this one over row 5's smaller
repo given its size and update cadence.
