---
name: fs-search-skill
description: Search the filesystem with ls (list directory), glob (pattern match), or grep (search file contents).
allowed-tools: fs_search
metadata:
  author: opencompany
  version: "1.0"
  category: filesystem

---

# FS Search Tool

Search the filesystem: list directories, glob pattern match files, or grep file contents. Uses the workspace-contained native filesystem backend.

**Path sandbox:** all paths resolve inside the per-workflow workspace root. Use workspace-relative paths; `..` and `~` segments are rejected, and absolute paths are remapped into the workspace.

## fs_search Tool

### Schema Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| mode | string | No | `ls` (list directory), `glob` (pattern match), `grep` (search contents). Default: `ls` |
| path | string | No | Directory path to search in (default: `.`) |
| pattern | string | If glob/grep | Glob pattern (e.g., `**/*.py`) or grep search text |

### Examples

**List directory:**
```json
{"mode": "ls", "path": "/path/to/project"}
```

**Find Python files:**
```json
{"mode": "glob", "path": ".", "pattern": "**/*.py"}
```

**Search for a function:**
```json
{"mode": "grep", "path": ".", "pattern": "def my_function"}
```

**Find all config files:**
```json
{"mode": "glob", "path": "/etc", "pattern": "*.conf"}
```

### Response Format

**ls mode:**
```json
{
  "path": "/",
  "entries": [
    {
      "path": "/src/",
      "is_dir": true,
      "size": 0,
      "modified_at": "2026-07-24T10:30:00"
    },
    {
      "path": "/README.md",
      "is_dir": false,
      "size": 1234,
      "modified_at": "2026-07-24T10:31:00"
    }
  ],
  "count": 2
}
```

**glob mode:**
```json
{
  "path": "/",
  "pattern": "**/*.py",
  "matches": [
    {
      "path": "/src/main.py",
      "is_dir": false,
      "size": 1200,
      "modified_at": "2026-07-24T10:31:00"
    },
    {
      "path": "/tests/test_main.py",
      "is_dir": false,
      "size": 850,
      "modified_at": "2026-07-24T10:32:00"
    }
  ],
  "count": 2
}
```

**grep mode:**
```json
{
  "path": "/",
  "pattern": "def main",
  "matches": [
    {"path": "/src/main.py", "line": 42, "text": "def main():"}
  ],
  "count": 1
}
```

`path` values in entries and matches are normalized virtual paths rooted at
the workflow workspace. `size` and `modified_at` are best-effort metadata and
may be absent if the backend cannot stat an entry.

### Guidelines

1. Use `ls` to explore directory structure
2. Use `glob` to find files by name pattern (supports `**` recursive, `*` wildcard, `?` single char)
3. Use `grep` to search file contents (literal text, not regex)
4. Narrow a grep by choosing a more specific `path`; there is no
   `file_filter` parameter
5. The native backend does not impose a match-count cap; scope broad searches
   carefully because every matching result is returned
