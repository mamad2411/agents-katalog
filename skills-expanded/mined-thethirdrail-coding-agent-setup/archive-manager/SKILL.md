---
name: archive-manager
description: |
  Route code, docs, git, graph, and memory archive retrieval or indexing through one on-demand context skill.
  Use when preserving, searching, indexing, or retrieving project context, history, docs, code structure, graph data, or durable memory.
---
# Archive Manager

This is a router skill. Classify the request, choose one lane, then read only the lane reference needed for the current task. Compose lanes only when the user request genuinely crosses responsibilities.

## Intent Routing

| Intent | Load | Use When |
|---|---|---|
| Code symbols and text search | `archive-code.md` | Read when finding definitions, references, or text patterns. |
| Document semantic memory | `archive-docs.md` | Read when storing or searching long-form docs and research. |
| Git history and change tracing | `archive-git.md` | Read when asking when or why repository behavior changed. |
| Structural code graph | `archive-graph.md` | Read when relationships among files, functions, or classes matter. |
| Durable project memory | `archive-memory.md` | Read when recording or retrieving decisions and durable notes. |
| Archive routing policy | `archive-manager.md` | Read when the correct archive lane is unclear or multiple lanes may compose. |

## Loading Protocol

1. Match the user request to the narrowest intent above.
2. Read `references/<lane>.md` for that intent before executing specialized steps.
3. Load scripts or assets from this skill only after the selected reference calls for them.
4. Keep outputs concise and state which lane was used when that matters for handoff or auditability.

## Consolidated Names

Former installable skills now routed here: `archive-manager`, `archive-code`, `archive-docs`, `archive-git`, `archive-graph`, `archive-memory`.

Related routers: `research-docs`, `mcp-ops`.
