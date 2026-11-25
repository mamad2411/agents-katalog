---
name: understand
description: Analyze a codebase to produce an interactive knowledge graph for understanding architecture, components, and relationships
argument-hint: [--full] [--mode coremind|claude|generic]
---

# /understand

Analyze the current codebase and produce a `knowledge-graph.json` file in `.understand-anything/`. This file powers the interactive dashboard for exploring the project's architecture.

## Options

- `$ARGUMENTS` may contain:
  - `--full` — Force a full rebuild, ignoring any existing graph
  - `--mode coremind` — Use CoreMind specific layer patterns and 10-stage pipeline tour (default for CoreMind)
  - `--mode claude` — Analyze the Claude Code setup (~/.claude/) instead of a project
  - `--mode generic` — Use generic layer detection for any project
  - A directory path — Analyze a specific project directory

## Instructions

Run the `coremind_understand` Python engine:

```bash
cd ~/.claude/tools && python3 -m coremind_understand <project_root> [options from $ARGUMENTS]
```

**Default behavior:**
- If current directory is CoreMind (contains `src/coremind/`): uses `--mode coremind`
- If `$ARGUMENTS` contains `claude` or `setup`: uses `--mode claude` with `~/.claude` as target
- Otherwise: uses `--mode generic`

After the analysis completes, automatically run `/understand-dashboard` to launch the visualization.

## What it produces

- `.understand-anything/knowledge-graph.json` — The graph (nodes, edges, layers, tour)
- `.understand-anything/meta.json` — Analysis metadata (commit hash, timestamp)

## Schema compliance

The engine produces output that passes the Understand-Anything Zod schema validation with zero errors. All nodes have valid `type` (file|function|class|module|concept), `complexity` (simple|moderate|complex), and all edges have `direction` and `weight` fields.

## Incremental updates

If a graph already exists and the git commit hash hasn't changed, the engine reports "up to date" and exits. Use `--full` to force a complete re-analysis.
