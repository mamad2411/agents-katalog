---
name: vesalius-code-map
description: Ask Vesalius about a codebase through its MCP tools instead of grepping: usages, feature_map, outline, architecture, and dependency_cycles. Use when answering questions about who calls or uses something, where a feature lives, what a file contains, how a project is put together, or whether circular imports exist.
---

# Vesalius code map

Vesalius is a precomputed, on-device code graph of the repository. Its
tools return file and line evidence, usually in one call. Every tool is
read-only. Use Grep for literal text or regex instead.

## Tools

| Tool | Ask it | What comes back |
| --- | --- | --- |
| `usages` | Who calls X? What uses this file? What breaks if I rename X? | Uses as file and line plus code, grouped by the function they sit in, plus a completeness check. With a change of rename, signature, or remove: the edit list and the tests to run. |
| `feature_map` | Where are purchases handled? How is data persisted? | The core types and functions grouped by role, with decisive lines, framework and input/output calls, config links, and call sites. |
| `outline` | What is in this file, type, or function? | Declarations with signatures and line ranges, first doc sentences, and calls in order. Cheaper than reading the file. |
| `architecture` | How is this project put together? | Targets and their product types, packages, folders, dependency direction, cycles, and cross-target links. |
| `dependency_cycles` | Do we have circular imports? | Every cycle in scope with each edge's import line and where the imported names are used, plus what was scanned. |

Under the `full` MCP profile there is a sixth tool, `repo_report`, for
health score, diagnostics, hotspots, unused code, overview, and finding
files by name.

## Notes

- If a `usages` result says complete, do not re-grep it. If it lists
  unresolved sites, check only those.
- The server serves the repository Claude Code is working in. Pin one
  repository with `vesalius mcp --repo /path/to/repo` in a manual
  registration, or set `VESALIUS_REPO`.
- `vesalius doctor` checks the connection any time. `vesalius stats`
  shows what Claude asked.
