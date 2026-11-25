---
name: read-file
description: Read the contents of a file from the filesystem and return them as a string. Use when the user asks to open, read, view, or show the contents of a specific file path.
---

# Read File

When the user provides a file path, use the `read_file` tool to retrieve its contents.

## When to use this skill

- User says "open", "read", "view", "show", or "display" followed by a path.
- User pastes a path and asks to inspect or summarize the file.

## How to read a file

Call the `read_file` tool with the path exactly as provided by the user.
If the path is relative, resolve it against the current working directory.

## Gotchas

- Binary files (images, PDFs, executables) will return garbled output — warn the user.
- Very large files may be truncated — inform the user if so.
- Permission errors should be surfaced clearly with the exact path that was denied.
