---
name: list_directory
description: Lists files and directories at the specified path.
---

# List Directory

This skill lists all files and directories at a given path, indicating whether each entry is a file or directory.

## Inputs
-   `dirPath`: (optional) Relative path to list. Defaults to `'.'`.
-   `baseDir`: (optional) The base directory to resolve `dirPath` from. Defaults to `process.cwd()`.

## Outputs
-   An array of strings, each prefixed with `[DIR]` or `[FILE]` followed by the entry name.
-   If the directory does not exist, returns `'Directory does not exist'`.
-   On error, returns a string with the error message.

## Instructions
1.  Use this skill to explore project structure before reading or writing files.
2.  Combine with `read_codebase` to understand the codebase layout.
