---
name: codeworker-codegraph
description: Use when Codex needs to understand, search, or modify a codebase with CodeWorker available. Use for symbol search, callers/callees, imports, impact analysis, local RAG context, and before broad grep/read exploration in CodeWorker projects or any project indexed by CodeWorker.
---

# CodeWorker CodeGraph

Use CodeWorker's local graph index before broad file scanning. The goal is the same discipline as `colbymchenry/codegraph`: find symbol entry points, inspect relationships, then read only the files that still need detail.

## Workflow

1. Locate the CodeWorker root. In this repo it is the directory containing `webui/rag/index.py`.
2. Build or refresh the index when needed:

```powershell
runtime\WinPython\python\python.exe C:\Users\Admin\.codex\skills\codeworker-codegraph\scripts\query_codeworker_graph.py --project <project-root> --rebuild --status
```

3. Query the graph before scanning files:

```powershell
runtime\WinPython\python\python.exe C:\Users\Admin\.codex\skills\codeworker-codegraph\scripts\query_codeworker_graph.py --project <project-root> --query "login auth flow"
```

4. Use the returned entry points and relationships to choose targeted file reads. Prefer:
   - `code_nodes` entry points for symbol locations.
   - `code_edges` relationships for `contains`, `imports`, `calls`, and `extends`.
   - RAG matches only after the graph narrows the search.

5. Before editing shared code, query the likely symbol or file again and check callers/importers in the relationship list.

## Output Discipline

- Treat graph context as a navigation map, not a full proof. Read the target source before editing.
- If graph data is missing or stale, rebuild once. If it still lacks the symbol, fall back to `rg`.
- Preserve CodeWorker's offline/local privacy model. Do not send code to cloud services just to build graph context.

## Useful Script Options

- `--project <path>`: project to index or query.
- `--query <text>`: symbol, file, or task search terms.
- `--rebuild`: rebuild CodeWorker's local RAG and code graph index.
- `--status`: print graph node/edge/unresolved counts.
- `--json`: return machine-readable JSON instead of markdown context.
- `--data-dir <path>`: override CodeWorker's `data` directory.

When working directly inside the CodeWorker repo before installing the skill, the same helper is also available at `plugins\codeworker-codegraph\scripts\query_codeworker_graph.py`.
