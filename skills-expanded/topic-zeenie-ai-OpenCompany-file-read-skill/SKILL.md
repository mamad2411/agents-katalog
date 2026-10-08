---
name: file-read-skill
description: Read raw file contents with line-based pagination support.
allowed-tools: file_read
metadata:
  author: opencompany
  version: "1.0"
  category: filesystem

---

# File Read Tool

Read raw file contents with line-based pagination. Uses the
workspace-contained native filesystem backend.

**Path sandbox:** all paths resolve inside the per-workflow workspace root. Use workspace-relative paths (e.g. `reports/data.csv`); `..` and `~` segments are rejected, and absolute paths are remapped into the workspace. Use `fs_search` with `mode: "ls"` to discover what exists.

## file_read Tool

### Schema Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file_path | string | Yes | Path to the file to read |
| offset | int | No | Line number to start from, 0-indexed (default: 0) |
| limit | int | No | Maximum lines to read (default: 2000, max: 10000) |

### Examples

**Read a file:**
```json
{"file_path": "/path/to/file.py"}
```

**Read with pagination:**
```json
{"file_path": "/path/to/large_file.py", "offset": 100, "limit": 50}
```

### Response Format

```json
{
  "content": "line one\nline two\n...",
  "line_count": 2,
  "file_path": "/path/to/file.py"
}
```

### Guidelines

1. Use offset/limit for large files instead of reading everything
2. `content` is the selected text slice, without added line numbers; text line
   endings are normalized to LF
3. `line_count` counts the lines in the returned slice, not the whole file
4. `file_path` is the normalized virtual path inside the workflow workspace
5. Non-UTF-8 files are returned as base64 text in `content`; the tool result
   does not include a separate `encoding` field, and line pagination is not
   applied to that base64 representation
