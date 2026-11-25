---
name: osori
description: "Osori — Local project registry & context loader. Find, switch, list, add/remove projects, check status. Triggers: work on X, find project X, list projects, project status, project switch. | 오소리 — 로컬 프로젝트 레지스트리. 프로젝트 찾아, 프로젝트 목록, 작업하자, 프로젝트 추가, 프로젝트 상태."
---

# Osori (오소리)

Local project registry & context loader for AI agents.

## Prerequisites

- **macOS**: `mdfind` (Spotlight, built-in), `python3`, `git`, `gh` CLI
- **Linux**: `mdfind` unavailable → uses `find` as fallback automatically. `python3`, `git`, `gh` CLI required.

## Dependencies

- **python3** — Required. Used for JSON processing.
- **git** — Project detection and status checks.

## Registry

`${OSORI_REGISTRY:-$HOME/.openclaw/osori.json}`

Override with the `OSORI_REGISTRY` environment variable.

## Finding Projects (when path is unknown)

When the project path is unknown, search in order:

1. **Registry lookup** — Fuzzy match name in `osori.json`
2. **mdfind** (macOS only) — `mdfind "kMDItemFSName == '<name>'" | head -5`
3. **find fallback** — Search paths defined in `OSORI_SEARCH_PATHS` env var. If unset, ask the user for search paths.
   `find <search_paths> -maxdepth 4 -type d -name '<name>' 2>/dev/null`
4. **Ask the user** — If all methods fail, ask for the project path directly.
5. Offer to register the found project in the registry.

## Commands

### List
Show all registered projects. Supports `--tag`, `--lang` filters.
```
Read osori.json and display as a table.
```

### Switch
1. Search registry (fuzzy match)
2. If not found → run "Finding Projects" flow above
3. Load context:
   - `git status --short`
   - `git branch --show-current`
   - `git log --oneline -5`
   - `gh issue list -R <repo> --limit 5` (when repo is set)
4. Present summary

### Add
```bash
bash skills/osori/scripts/add-project.sh <path> [--tag <tag>] [--name <name>]
```
Auto-detects: git remote, language, description.

### Scan
```bash
bash skills/osori/scripts/scan-projects.sh <root-dir> [--depth 3]
```
Bulk-scan a directory for git repos and add them to the registry.

### Remove
Delete an entry from `osori.json` by name.

### Status
Run `git status` + `gh issue list` for one or all projects.

## Schema

```json
{
  "name": "string",
  "path": "/absolute/path",
  "repo": "owner/repo",
  "lang": "swift|typescript|python|rust|go|ruby|unknown",
  "tags": ["personal", "ios"],
  "description": "Short description",
  "addedAt": "YYYY-MM-DD"
}
```

## Auto-trigger Rules

- "work on X" / "X 프로젝트 작업하자" → switch X
- "find project X" / "X 찾아줘" / "X 경로" → registry search or discover
- "list projects" / "프로젝트 목록" → list
- "add project" / "프로젝트 추가" → add
- "project status" / "프로젝트 상태" → status all
