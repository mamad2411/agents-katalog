---
name: core-file-ops
description: Perform batch file operations safely with search, replacement, renaming, or refactoring.
---

File operation task: $ARGUMENTS

Gather context about the files involved:

```bash
# Understand scope
echo "=== Current directory ==="
ls -la
echo "=== Git status ==="
git status --short
```

Identify what kind of operation is needed and execute it:

**Search & inspect**
- Find files by name, extension, or content pattern
- Show file sizes, counts, structure

**Transform & rewrite**
- Batch rename, move, or reorganize files
- Convert formats (JSON↔YAML, CSV↔TSV, etc.)
- Find-and-replace across multiple files

**Generate & scaffold**
- Create files from a template or pattern
- Scaffold directory structures

**Analyze**
- Diff two files or directories
- Detect duplicates, orphans, or broken references
- Summarize large files (line count, structure, top entries)

Rules:
1. **Preview before destructive actions** — show what will change and get confirmation before deleting, moving, or overwriting files.
2. **Prefer targeted edits** — use Edit tool for small changes; only rewrite whole files when necessary.
3. **Preserve git history** — use `git mv` instead of raw `mv` when renaming tracked files.
4. After completion, show a summary: files affected, before/after if relevant.
