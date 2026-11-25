---
name: file_operations
description: Write, list, search, and inspect files/directories in the local filesystem.
module: builtin_tools.file_ops
tools:
  - write_file
  - list_directory
  - search_files
  - file_info
  - move_file
  - copy_file
  - rename_path
  - make_directory
  - find_duplicates
---

# File Operations Skill

Bootstrap tool `read_file` is always available before skill activation.
This skill adds mutation and discovery operations.

## `write_file`
- Required: `path`, `content`
- Creates/overwrites UTF-8 text file

## `list_directory`
- Required: `path`
- Optional: `recursive` (default `false`)
- Returns entries with type and file size where available

## `search_files`
- Required: `path`, `pattern`
- Optional: `max_results` (default `20`)
- Pattern uses glob semantics (`*.py`, `**/*.md`)

## `file_info`
- Required: `path`
- Returns metadata: absolute path, type, size, timestamps

## `move_file`
- Required: `source`, `destination`
- Moves file/directory inside workspace

## `copy_file`
- Required: `source`, `destination`
- Copies file/directory inside workspace

## `rename_path`
- Required: `path`, `new_name`
- Renames target in place inside workspace

## `make_directory`
- Required: `path`
- Creates directory recursively inside workspace

## `find_duplicates`
- Required: `path`
- Optional: `max_files` (default `5000`)
- Reports duplicates by SHA-256 hash (read-only, no delete)
