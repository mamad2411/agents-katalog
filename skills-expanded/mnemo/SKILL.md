---
name: mnemo
description: Memory engine + markdown notes + knowledge graph for AI coding agent
---

# Mnemo Skill Guide for Pi Agent

Mnemo provides persistent memory, knowledge graphs, and hybrid search (BM25 + Vector + RRF) for coding agents.

## Core Rules & Guardrails

1. **SMART RECALL GUARDRAIL (MAX 1x PER TURN)**: Call `memory_recall` ONLY when starting new features, major refactors, or checking past architectural decisions and domain rules. DO NOT call `memory_recall` for discovering filenames, reading source code, or language syntax (use standard file reading / inspection tools). If prompt already contains `<MNEMO_CONTEXT>`, DO NOT call recall again.
2. **MANDATORY AUTO-SAVE**: Automatically call `memory_save` after making important architectural decisions, finishing new features, or fixing non-trivial bugs WITHOUT waiting for explicit user prompts.
3. **Structured Format**: Provide structured notes containing Context + Decisions + Files Modified.

## Available Tools

- `memory_save`: Save structured decision/memory note + auto-embed + auto-extend knowledge graph.
- `memory_recall`: Hybrid semantic search for past decisions.
- `graph_query`: Query entity & dependency relationships in the Knowledge Graph.
- `file_info`: Extract AST skeleton, exports, and line numbers of code files.
- `graph_init`: Scan repository to build initial knowledge graph.
- `graph_analytics`: Calculate Louvain community clusters, modularity, and architectural God Nodes.
- `graph_impact`: Run impact analysis (BFS) before modifying critical files.
- `git_sync`: Ingest recent git commits into the knowledge graph.
- `memory_audit`: Audit and fix broken file links or stale notes.
- `adr_generate`: Generate Architecture Decision Records (ADRs) in `docs/adr/`.

## Slash Commands in Pi

- `/remember <text>`: Quickly record an architectural decision.
- `/recall <query>`: Search past notes directly in terminal.
- `/graph <entity>`: Query graph relationships.
- `/mnemo`: Show memory engine health & status.
